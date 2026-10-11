# Opening voice casting

Current casting (owner update, 2026-10-10): mother `5u41aNhyCU6hXOcjPPv0`; daughter `ogwqBH5bbF03DSbNiRNN`, replacing Sarah. Full dialogue v02 generated successfully: original 39.12 s; edited WAV 50 s, 11 turns, last turn ends at 49.75 s. Identical telephone filter on both speakers. Source request: `opening-dialogue-v02.request.json`. Output: `video/renders/opening-dialogue-v02-preview-50s.mp3`; clean and filtered WAV masters and waveform data also retained locally. Earlier entries below are casting history, not current selection. Audio decode and timing validated; listening review pending.

Checked: 2026-10-10. Selection based on ElevenLabs account catalogue metadata. A first three-turn Julie/Sarah test has now been generated; performance remains pending owner audition.

| Role | Candidate | Voice ID | Reason |
|---|---|---|---|
| Mother — owner selection, replaces Julie | Name not yet queried | 5u41aNhyCU6hXOcjPPv0 | Explicit owner preference after test v01. |
| Mother | Julie - Warm, Mature | g12yXXabMWeFoLMzxPrF | English, American accent, older voice; described as warm, soft and intimate. |
| Daughter | Sarah - Mature, Reassuring, Confident | EXAVITQu4vr4xnSDxMaL | English, American accent, young adult; described as warm and reassuring. |
| Daughter alternative | Jessica Anne Bogart - A VO Professional; now cloned! | lxYfHSkYm1EzQzGhdbfc | English, American accent, middle-aged; described as conversational and calm. |

These are provider catalogue voices for fictional characters, not newly designed original voices. Do not claim the voices themselves were created for VoxWave. Their delivery and suitability still require an audio test. No disease-related vocal impairment should be imitated.

Suggested first test: the first three dialogue turns in voiceover.md, using Julie and Sarah. Generate clean speech before local telephone processing. Use understated delivery, with no music or effects. Keep the exact script for the first test; evaluate the British wording “Mum” with the American voices before changing it.

## Connection check

Revision v02 uses the owner's mother voice and Sarah, with slower-delivery tags, ellipses and short pauses. Tags are performance suggestions, not guaranteed timings. Final direction: natural nuance and listening space; telephone filter on both voices. Julie is retained above only as casting history.

v02 result: HTTP 200, 213621-byte clean MP3, measured duration 13.28 s. Files: `video/renders/voice-test-v02-clean.mp3` and `video/renders/voice-test-v02-phone.mp3`. The telephone filter (300–3400 Hz) covers the entire mix, hence both speakers. Decoding succeeded; artistic quality awaits listening. One new generation, no video generation.

- ElevenLabs: authenticated GET /v2/voices succeeded; candidate voices are listed in the account. Generation permissions, model compatibility and remaining credits have not yet been tested.
- APIMart: after the owner's top-up on 2026-10-10, authenticated GET /v1/models succeeded (316 models). The catalogue includes seedance-1-0-pro-fast, seedance-1-0-pro-quality, seedance-1-5-pro, seedance-2.0, seedance-2.0-face, seedance-2.0-fast, seedance-2.0-fast-face, seedance-2.0-mini and seedance-2.5. The earlier HTTP 402 balance gate is resolved. Generation endpoint identifiers, pricing and actual generation access still require verification; catalogue IDs may differ from documented generation IDs.
- First audio test: one successful eleven_v3 dialogue request, using `voice-test-v01.request.json`. Clean output: `video/renders/voice-test-v01-clean.mp3`, 7.36 seconds, mono 44.1 kHz MP3, 118744 bytes. Local telephone-filter copy: `video/renders/voice-test-v01-phone.mp3` (300 Hz high-pass and 3400 Hz low-pass). Both files are ignored by Git. FFprobe read the stream and FFmpeg decoded it successfully; no listening-based quality claim is made. Exact credit usage was not queried. No video was generated and no keys were written to the repository.

## References

- Voice catalogue API: https://elevenlabs.io/docs/api-reference/voices/search
- APIMart setup: https://docs.apimart.ai/en/quickstart
