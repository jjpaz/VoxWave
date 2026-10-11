# Opening animatic v04 — original outline motion

The owner rejected v03 and supplied `voxwave_render.py` and
`voxwave_logo_reveal.html` from Downloads. Both were inspected as reference data,
not executed or treated as instructions. Unmodified copies are in
`video/references/motion/original-source/`; no external upload was made.

## Visual direction

Orange closed outline first, followed by navy and blue outlines with independent
phases. They converge, trace the official symbol contours, and only then fill.
This restores the original's mechanism instead of the rejected early solid ribbons.
The original scale, colors, contour sampling and quadratic smoothing are retained.
Pre-morph motion is extended 1.2 seconds. The real narration drives the envelope;
1.25-second release gives the drawn line inertia during the spoken pause without
stretching the recording. Seven official letter outlines rise in sequence.

| Time | Event |
|---|---|
| 0–50 s | Existing four shot studies and approved English problem cards |
| 50–56 s | What if the answer was always there? |
| 56–57 s | Orange line moves into center |
| 57.6–60.16 s | In the voices we hear every day. |
| 57.8–59.4 s | Navy and blue outlines enter progressively |
| 61.7–63.6 s | Outlines transform into the symbol |
| 62.8–64.48 s | Meet VoxWave. |
| 63.3–64.3 s | Background transitions to white |
| 63.6–64.4 s | Symbol fills |
| 64.1–65.83 s | Letters rise in a wave |
| 67–69 s | Stable final logo |

## Voice and sound

Two paid ElevenLabs generations: `opening-dialogue-v03` and
`brand-narration-v02`. Requests contain fictional dialogue, public catalogue voice
IDs and no credentials. The selected mother/daughter IDs remain unchanged;
George is still a temporary narrator, not Edward.

Removed repeated acting/slow tags and previous postproduction speed changes.
The full conversation remains continuous, without inserted gaps between replies.
The generated MP3 decodes to 32.24 s and plays from 3 to 35.24 s. Both speakers
receive the same 300–3400 Hz telephone filter. This deliberately exposes a longer
ambient-only passage before the question; it is a voice and animation review,
not a locked final pacing decision. Naturalness still needs the owner's listening
review; technical decoding does not establish performance quality.

Soft organic transformation effect selected by owner. Subtle synthesized air and
musical bed remain combined; no technology-effect alternate in v04.

## Outputs and reproduction

- `video/renders/logo-comparison-v04-soft.mp4`: question and full closing, 19 s.
- `video/renders/opening-animatic-v04-soft.mp4`: full 69 s animatic.
- `video/renders/opening-dialogue-v03-raw.mp3`: clean native-speed call.
- `video/renders/opening-dialogue-v03-phone.wav`: filtered native-speed call.
- `video/renders/brand-narration-v02-raw.mp3`: clean native-speed narrator.
- `video/renders/opening-animatic-v04-verification.json`: measured cues and geometry.

Re-render with `python video/tools/render_original_transition.py` once generated
audio is present. It makes no API calls. Renders remain ignored. Previous final
versions are retained. Four cinematic shots remain labelled illustrated
storyboards, not generated Seedance footage.

Verification: canonical SVG path checks, seven letters with preserved counters,
frame-identical final hold, voice ordering, native timing and no clipped mix
samples. Contact-sheet visual inspection checks colored outlines, late fill and
the final wordmark. Final media must decode with FFmpeg before delivery.
