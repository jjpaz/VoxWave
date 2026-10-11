"""Verify downloaded handoff media against the committed SHA-256 manifest."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[2]

def main():
    manifest = json.loads((ROOT / 'video/handoff/assets.json').read_text(encoding='utf-8'))
    errors = []
    for item in manifest['assets']:
        path = ROOT / item['path']
        if not path.is_file():
            errors.append(f"Missing: {item['path']}")
            continue
        data = path.read_bytes()
        if data.startswith(b'version https://git-lfs.github.com/spec/v1\n'):
            errors.append(f"LFS media not downloaded: {item['path']}; run git lfs pull")
        elif len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
            errors.append(f"Modified or damaged: {item['path']}")
    if errors:
        print('\n'.join(errors))
        return 1
    print(f"OK: {len(manifest['assets'])} handoff assets verified by SHA-256.")
    return 0

if __name__ == '__main__':
    sys.exit(main())
