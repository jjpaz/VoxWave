"""Local, repeatable edit of the synthetic opening take; no API calls.

Requires ffmpeg on PATH. Keeps the original take, fits all 11 turns into
50 seconds without clipping speech, and filters both voices together.
"""
import array
import argparse
import json
import math
from pathlib import Path
import subprocess
import wave

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "renders"
RATE = 44100
TOTAL = RATE * 50
SPEED = 0.92


def ffmpeg(*args, data=None):
    return subprocess.run(
        ["ffmpeg", "-hide_banner", "-v", "error", *args],
        input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
    ).stdout


def save_wave(path, samples):
    with wave.open(str(path), "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(RATE)
        output.writeframes(samples.tobytes())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', choices=['v01', 'v02'], default='v01')
    args = parser.parse_args()
    prefix = f"opening-dialogue-{args.version}"
    metadata = json.loads((OUT / f"{prefix}-timestamps.json").read_text(encoding="utf-8-sig"))
    segments = metadata["voice_segments"]
    assert len(segments) == 11
    assert [s["dialogue_input_index"] for s in segments] == list(range(11))
    raw = array.array("h", ffmpeg("-i", str(OUT / f"{prefix}-raw.mp3"),
                                 "-f", "s16le", "-ac", "1", "-ar", str(RATE), "pipe:1"))
    clips = []
    for i, segment in enumerate(segments):
        start = round(segment["start_time_seconds"] * RATE)
        end = round(segments[i + 1]["start_time_seconds"] * RATE) if i < 10 else len(raw)
        assert 0 <= start < end <= len(raw)
        clip = array.array("h", ffmpeg(
            "-f", "s16le", "-ar", str(RATE), "-ac", "1", "-i", "pipe:0",
            "-af", f"atempo={SPEED}", "-f", "s16le", "pipe:1", data=raw[start:end].tobytes()))
        assert len(clip) > RATE // 5 and max(abs(x) for x in clip) > 100
        # Five-millisecond edge fades prevent discontinuities at the edits.
        fade = RATE // 200
        for j in range(fade):
            clip[j] = round(clip[j] * j / fade)
            clip[-1-j] = round(clip[-1-j] * j / fade)
        clips.append(clip)
    lead, tail = 3 * RATE, round(0.25 * RATE)
    available = TOTAL - lead - tail - sum(map(len, clips))
    assert available > 0, "Take too long: revise pauses instead of truncating speech"
    weights = [0.6, 0.9, 1.0, 1.1, 0.9, 0.9, 1.0, 0.8, 0.6, 0.6]
    gaps = [round(available * w / sum(weights)) for w in weights]
    gaps[-1] += available - sum(gaps)
    assert all(0.3 * RATE <= gap <= 1.8 * RATE for gap in gaps)
    speech = array.array("h", [0]) * lead
    cues = []
    for i, clip in enumerate(clips):
        start = len(speech) / RATE
        speech.extend(clip)
        cues.append({"input_index": i, "voice_id": segments[i]["voice_id"],
                     "start": start, "end": len(speech) / RATE})
        if i < 10:
            speech.extend(array.array("h", [0]) * gaps[i])
    speech.extend(array.array("h", [0]) * tail)
    assert len(speech) == TOTAL
    save_wave(OUT / f"{prefix}-clean-50s.wav", speech)
    phone = array.array("h", ffmpeg(
        "-f", "s16le", "-ar", str(RATE), "-ac", "1", "-i", "pipe:0",
        "-af", "highpass=f=300,lowpass=f=3400", "-f", "s16le", "pipe:1", data=speech.tobytes()))
    assert len(phone) == TOTAL
    save_wave(OUT / f"{prefix}-phone-50s.wav", phone)
    # Waveform data follows dialogue only, before the final background gain.
    frame_size = RATE // 30
    rms = [math.sqrt(sum(x*x for x in phone[i:i+frame_size]) / frame_size) / 32768
           for i in range(0, TOTAL, frame_size)]
    assert len(rms) == 1500 and max(rms) > 0 and max(rms[:85]) == 0
    (OUT / f"{prefix}-edit.json").write_text(json.dumps({
        "duration": 50, "speed": SPEED, "lead_seconds": 3, "cues": cues,
        "waveform_fps": 30, "waveform_rms": rms,
        "ring": "Provisional local synthesis, not a branded melody; align to picture later."
    }, indent=2), encoding="utf-8")
    preview = array.array("h", phone)
    # Quiet generic two-pulse feature-phone placeholder, only before speech.
    for start_s in (0.2, 1.35):
        start, length = round(start_s * RATE), round(0.6 * RATE)
        for j in range(length):
            t = j / RATE
            envelope = min(1, t / 0.015, (0.6 - t) / 0.025)
            value = 1000 * envelope * (math.sin(2*math.pi*880*t) + 0.5*math.sin(2*math.pi*1320*t))
            preview[start+j] = round(value)
    save_wave(OUT / f"{prefix}-preview-50s.wav", preview)
    ffmpeg("-y", "-i", str(OUT / f"{prefix}-preview-50s.wav"),
           "-c:a", "libmp3lame", "-b:a", "128k", str(OUT / f"{prefix}-preview-50s.mp3"))
    print(json.dumps({"duration": len(speech)/RATE, "turns": len(cues),
                      "gap_seconds": [round(x/RATE, 3) for x in gaps],
                      "last_word_segment_end": cues[-1]["end"], "waveform_frames": len(rms)}))


if __name__ == "__main__":
    main()
