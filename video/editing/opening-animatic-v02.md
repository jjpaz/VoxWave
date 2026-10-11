# Opening animatic v02 — comparison exports

Owner feedback, 2026-10-10: 50 seconds is guidance, not a fixed duration. Keep
the current dialogue performance for now; its unusual intonations and artificial
pauses will be revised later. Speech must end before the logo transition.

## Shared changes

- Duration: 63 seconds, 1280×720, 30 fps.
- Shot placeholders: phone 0–6; home 11–16; road 27–32; clinic 37–42.
  The last three were previously only three seconds long; now each has five.
- Text layout retained. Longest card 16–27 (11 seconds). Exact closing question:
  “What if the answer was always there?”
- Dialogue remains the existing v02 edit: no new generation, phrase edits or
  additional stretching. Last speech segment ends at 49.75 seconds.
- Voice gain 0.27 versus 0.6 previously (about 6.94 dB quieter). Both voices retain
  the same telephone filter. Ring level unchanged from animatic v01.
- Waveform uses the real dialogue RMS with 220 ms attack and 550 ms release.
  Smooth analytical mirrored curves replace jagged local RMS profiles; stroke
  increases from 2–3 pixels to 6 pixels. No activity floor in silence. Sound beds
  do not drive the waveform. It settles after speech stops.
- Waveform moves to centre from 55.7 s, then blends into the exact first frame of
  the selected reference portion over 56.55–57 s. Reference playback at 57–63 uses
  original frames 106–285 at normal speed. This graphic transition occurs after
  the call ends. Reference logo remains unchanged.

## Controlled comparison

| Ending | Access card | Final question | Speech relative to question |
|---|---|---|---|
| A | 42–50 | 50–56 | Farewell finishes before the question |
| B | 42–47 | 47–56 | Farewell overlaps the beginning of the question |

Both versions show waveform alone from 56–57 and the reference from 57–63.
Both retain the same total duration and exactly the same dialogue audio timing.
The difference in access/question duration isolates the final question's entrance
without changing voice performance.

Each ending has two sound-bed versions:

- `ambience`: low-level locally synthesized air/room-tone sketch, slightly more
  open during the road placeholder. No recorded real location is implied.
- `music`: very quiet locally synthesized sustained open chord, with no beat or
  melody and a little air underneath. A production sketch, not final scoring.

Files: `video/renders/opening-animatic-v02-{A,B}-{ambience,music}.mp4`.
Render: `python video/tools/render_opening_variants.py` (Pillow, FFmpeg and local
v02 audio/reference required). No API calls or paid generations. Renders stay
ignored by Git. v01 remains available for comparison.

## Remaining work

Owner selection of ending and sound direction; later revise voice intonation and
pauses, then recalibrate waveform to that revised audio. Four visual studies remain
placeholders pending Seedance. Confirm visual pacing before generating footage.
