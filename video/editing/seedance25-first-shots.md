# Seedance 2.5 — first four clips, 2026-10-10

Owner authorized video generation, specifically Seedance 2.5 with ambient audio.
Only the four reviewed synthetic stills were uploaded to APIMart. No dialogue,
clinical audio, identifying records or credentials were included in media payloads.

## Results

| Shot | Reference | Actual duration | Actual USD charge |
|---|---|---|---|
| M01 | m01-v03-A-oblique.png | 6.048 s | 1.305 |
| M02 | m02-window-reference-v02-cup.png | 5.056 s | 1.089 |
| M03 | m03-v02-C-village-fields.png | 5.056 s | 1.089 |
| M04 | m04-clinic-reference-v02-cool.png | 5.056 s | 1.089 |

Total: **4.572 USD**, four successful jobs, no generation retries. Initial balance
was 10 USD. The displayed estimate was 4.536 USD; completed tasks provide the
actual charge above. Model `seedance-2.5`, resolution `720p`, first-frame role,
adaptive aspect ratio, generated audio enabled, MP4 output. No extra service selected.

## Files

- Source clips: `video/renders/seedance25/m0N/m0N-seedance25-v01.mp4`.
- Separate source ambience: `video/renders/seedance25/m0N/m0N-ambience.wav`.
- Review reel: `video/renders/seedance25/four-shots-review-v01.mp4`, 21 seconds,
  raised ambience levels with short edge fades, without the call or music.
- Integrated review: `video/renders/opening-v06-seedance25-ambience.mp4`, 69 seconds.
- Contact sheets and stream checks: each shot's folder.
- Exact prompts, durations and images: `video/script/seedance25-shots-v01.json`.

The integrated review replaces only the four illustrated placeholders at 0–6,
11–16, 27–32 and 37–42 seconds. It retains the paced conversation, text cards,
music and existing logo transition timing from v05. The logo remains unapproved;
this is not an assertion that its previously reported sync issue is solved.

Source mean levels measured at -42.2/-41.8/-43.7/-37.5 dBFS for M01–M04;
the native tracks were very quiet. Review-reel gains are +8/+10/+15/+6 dB;
integrated ambience gains are +3/+7/+12/+3 dB, with edge fades. The resulting
exterior bed is approximately -31.7 dBFS mean before summing with the main mix.
Original isolated audio remains available for adjustment. A final limiter guards
against mix overload. These are provisional listening levels, not approved sound design.

## Validation and limits

All four clips decode, contain audio and meet requested duration. Nine sampled
frames per shot inspected: no face/person added; M01 reaches, grips, lifts and
exits; other shots retain their main scene content. M04's camera push is visibly
stronger than the requested near-imperceptible two percent and merits owner review.
Frame sheets do not establish naturalness of tremor or audio quality. No automated
claim is made that generated ambience is free of speech/music; listening review
of the supplied reel is still required before locking the audio.

Renders and provider responses stay ignored, including M03's source over 5 MiB.
No Git add, commit, upload to repository, or expanded binary exception.

## Provider documentation consulted

- https://docs.apimart.ai/en/api-reference/videos/seedance-2-5/generation.md
- https://docs.apimart.ai/en/api-reference/uploads/images.md
- https://docs.apimart.ai/en/api-reference/tasks/status.md

Upload/generate/status tool: `video/tools/seedance25.py`. POST requests are guarded
against accidental resubmission and are never automatically retried. Rebuild the
local review exports with `python video/tools/assemble_seedance25.py`; this does
not call the API or incur generation charges.
