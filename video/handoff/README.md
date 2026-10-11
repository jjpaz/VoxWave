# VoxWave opening v08 — editable handoff

This handoff contains the 72.2-second cinematic opening, its source clips, clean
and filtered synthetic dialogue, native narration, separate mix stems, reference
keyframes, editable Python graphics and the final reference export. It is not a
Shotcut timeline. The existing Remotion block is a separate part of the pitch.

## Open and verify

Install Git LFS, then clone the handoff branch and run from the repository root:

```sh
git lfs install
git lfs pull
python video/tools/verify_handoff.py
```

The manifest checks the exact original bytes of all 29 delivered media/metadata
files. Run it before editing or rendering. A SHA mismatch after intentionally
editing an asset is expected; review and update the manifest when accepting it.
All paths are relative to the repository. Downloads of GitHub ZIP files may
contain LFS pointers instead of media: prefer a clone followed by `git lfs pull`.

## Edit and rebuild without paid services

Requires Python, Pillow (tested with 12.2.0), FFmpeg and ffprobe on PATH. Install
Pillow in your own environment with `python -m pip install Pillow==12.2.0`.
The original render uses Windows Segoe UI fonts installed in C:/Windows/Fonts.
On another OS, set VOXWAVE_FONT_REGULAR and VOXWAVE_FONT_BOLD to licensed font
files. Different fonts can change text widths and appearance. Font files are
not redistributed in this handoff.

Edit timings, card text and shot order in `video/tools/finalize_opening_v08.py`.
Edit logo motion in `render_original_transition.py` and `render_brand_transition.py`.
Dialogue source and timing data are included; rebuilding dialogue explicitly
uses `python video/tools/assemble_opening_audio.py --version v02`.

```sh
python video/tools/test_brand_transition.py
python video/tools/finalize_opening_v08.py
python video/tools/verify_opening_v08.py
```

These render/verification commands write derived files in `video/renders`,
including replacing the local v08 reference export and mix. Work on a branch
and preserve your baseline first. They do not invoke paid generation APIs.
Do not run `seedance25.py` or other provider-generation commands just to rebuild.

The four source clips are in `renders/seedance25-phone-v02/m01` and
`renders/seedance25/m02`, `m03`, `m04`. Raw and clean audio permit editing beyond
the final MP4. `renders/v08` includes separate narration, music/SFX bed, mix,
graphics and logo tail. Narration's timed file drives the logo waveform;
change it consistently if replacing the narration. Logo geometry also uses
`video/voxwave-video-pitch/src/brand/logo.ts` and the canonical SVG in `video/assets`.

## Storage and scope

Git tracks code, text, SVG and timing metadata. The 24 explicitly listed binary
assets use Git LFS; no large legacy asset is silently migrated and no history
is rewritten. No delivered file requires separate shared storage due to its size.
Older experiments, alternate generations and QA images remain in the verified
local backup rather than being deleted. Provider responses, upload URLs,
credentials, private/team photographs and unrelated private project history
are excluded from the public contribution to Marco.

The source record identifies the footage/keyframes and dialogue as synthetic,
the voices as generated, and the logo as the supplied official VoxWave asset.
No clinical recording is included. This handoff does not add a license grant
or claim clinical validation. Creative approval and voice performance remain
the team's decision.

Marco's existing Remotion source must stay intact. The contribution is intended
for a separate `opening-v08/` folder and branch/PR, not a replacement of his main
branch. The local private repository's full history must never be pushed there.
