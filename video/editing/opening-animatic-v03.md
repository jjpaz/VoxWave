# Opening animatic v03 — new brand transition

Owner instruction, 2026-10-10: combine subtle music and ambience. Use ending A
(farewell before question) provisionally. Replace the reference-video transition
with a new animation: longer opening fluctuations driven by a male narrator,
“Meet VoxWave” while the symbol forms, letters rising in a wave, and two sound
effect alternatives. Edward's voice ID is not yet available; a male example is
explicitly authorised.

## Narration trial

George — Warm, Captivating Storyteller, `JBFqnCBsd6RMkjVDRZzb` is temporary.
One ElevenLabs eleven_v3 request produced the two lines; no voice cloning or
clinical material was sent. Request: `video/script/brand-narration-v01.request.json`.

Proposed response to the final question: “In the voices we hear every day.”
Then: “Meet VoxWave.” Exact first-line copy is a creative trial, not final owner
approval or a claim of clinical validation. Narrator is clean and foregrounded,
not telephone-filtered. Mother/daughter performance is unchanged and still due
for later intonation/pause review.

## Working timeline (69 seconds total)

| Time | Beat |
|---|---|
| 0–50 | Previous v02 A opening; farewell before the question |
| 50–56 | “What if the answer was always there?” |
| 56–57 | Existing orange waveform moves smoothly to the centre |
| 57.35–59.85 | George: “In the voices we hear every day.” |
| 57–61.2 | Longer preliminary fluctuations, amplitude driven by narrator RMS |
| 61.2–65.1 | Three contours transform into the official symbol |
| 62.5–64.7 | Background gradually becomes near-white |
| 63.15–65.48 | “Meet VoxWave” clip, including its trailing quiet |
| 64.65–66.4 | Seven official letter shapes rise with staggered wave motion |
| 67–69 | Static final logo hold |

The symbol is built from the exact paths in `Logo-oficial.svg`, using the
existing split-path data only after verifying each string against that source.
Cubic curves are flattened at subpixel screen precision for rendering. The
source SVG is unchanged. Letter counters remain transparent; no replacement
font is used. The final logo position/scale is stable. The original reference
MP4 is not part of this new closing sequence.

## Sound comparison

Both exports share identical picture, narration, phone call, synthesized room/air
ambience and quiet sustained musical pad. Only the transition effects differ:

- `organic`: soft air rise followed by a warm two-tone finish.
- `technology`: restrained rising electronic pulse and brighter finish.

Effects form one sound gesture; there is no separate sound per letter. Effects
and beds are local synthetic sketches, not final production scoring or recordings
of the depicted locations. Bed is reduced during the narrator's clips. Only the
narrator drives the logo's audio response; effects/music do not.

Full exports: `video/renders/opening-animatic-v03-{organic,technology}.mp4`.
19-second closing extracts: `video/renders/logo-comparison-v03-{organic,technology}.mp4`.
Reproduce locally: `python video/tools/render_brand_transition.py`.
Source media and renders remain excluded from Git.

## Validation

Four local unit tests cover SVG relative subpaths, cubic endpoints, canonical
path matching/letter counters, and envelope decay to silence. Runtime assertions
verify unclipped audio, placement of both narration clips and identical final
hold frames. Representative frames inspected through fluctuation, morph, letter
rise and final hold. FFprobe and full decode check the delivered containers.
Listening judgement, narrator choice, response wording and final sound selection
remain for owner review. All four scene illustrations are still placeholders.
