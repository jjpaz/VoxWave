# Opening animatic v01

Created 2026-10-10. Local review video: `video/renders/opening-animatic-v01.mp4`.
50.000 seconds, 1280×720, 30 fps, H.264/AAC. This is a timing/layout mockup,
not finished AI footage. All visible text and speech are in English.

## Timing

| Seconds | Picture |
|---|---|
| 0–5 | M01: illustrated phone/hand placeholder |
| 5–10 | Full magnitude sentence, white on black |
| 10–13 | M02: illustrated home placeholder |
| 13–23 | Full fastest-growing/2050 sentence; source scope in footer |
| 23–26 | M03: illustrated rural-road placeholder |
| 26–31 | Full symptom-recognition sentence |
| 31–34 | M04: illustrated waiting-area placeholder |
| 34–39 | Full specialist-access sentence |
| 39–44 | Provisional question: “What if the answer was here all along?” |
| 44–45 | Reactive waveform alone, moves to centre |
| 45–50 | Owner's supplied waveform-to-logo reference, frames 136–285 |

The reference is 286 frames (9.533333 s); its final 150 frames fit the five-second
closing slot without changing playback speed. It is used as supplied, not redrawn.
The handoff at 45 s is a provisional edit into the reference's graphic animation.
The precise vector morph/continuity can be refined after timing review.

## Audio and waveform

Uses the 50-second v02 conversation: mother `5u41aNhyCU6hXOcjPPv0`, daughter
`ogwqBH5bbF03DSbNiRNN`. Telephone filter covers both voices. Final preview gain
is 0.6 (about −4.4 dB) relative to the audio audition. Generic provisional ring
remains at the beginning; no music is added.

Waveform amplitude follows ten-millisecond RMS windows from the filtered dialogue
master on its global timeline, with a stylized mirrored curve. It is a volume
visualization, not a diagnostic signal or a literal sample-by-sample oscillogram.
It has no simulated minimum speech activity and excludes the ringtone. From 45 s,
the owner reference takes over as deliberate graphic motion while speech continues.

## Local reproduction

`python video/tools/render_opening_animatic.py`

Requires local Pillow, FFmpeg, Segoe UI font files on Windows, the locally generated
v02 WAV masters, and the owner's local reference MP4. No API calls, installation
or generation credits are used by this renderer. The existing Remotion project
has no installed dependencies in this checkout; the first review export therefore
uses this local renderer. It does not modify the existing Block2 composition.

Sources and factual scope: `video/script/opening-copy-shortlist.md`.
All renders, inspection frames and media remain ignored by Git.

## Verified and pending

- FFprobe reports both video and audio at exactly 50 s, 30 fps, 1280×720.
- Inspected representative frames of all four placeholders, five text states,
  the waveform-only beat, and the logo transition/hold. Text stays within frame.
- Source audio checks confirm silent opening of the dialogue master and nonzero
  RMS speech values; there are no API calls in the rendering script.
- Owner playback review remains necessary for reading pace, voice prominence and
  artistic timing. No Seedance shots have been generated. The placeholder style
  and their English production labels are not part of the final cinematic footage.
