"""Check scaffold and tracked files without reading private file contents."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ['README.md', 'AGENTS.md', '.gitignore'] + [
    'docs/' + name + '.md' for name in
    ['PROJECT_CONTEXT', 'STATUS', 'DECISIONS', 'ROADMAP', 'RESEARCH', 'ARCHITECTURE', 'CODEX_SETUP']
]
DIRS = ['video/' + name for name in ['script', 'storyboard', 'prompts/seedance',
        'prompts/image-generation', 'references', 'assets', 'renders', 'editing']]
DIRS += ['platform/' + name for name in ['frontend', 'mobile', 'backend', 'api', 'tests',
         'voice-analysis/preprocessing', 'voice-analysis/features', 'voice-analysis/models',
         'voice-analysis/inference']] + ['hardware', 'docs']

def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, check=True, capture_output=True).stdout

def main():
    errors = [f'Missing: {name}' for name in REQUIRED + DIRS if not (ROOT / name).exists()]
    tracked = [p for p in git('ls-files', '-z').decode().split('\0') if p]
    if not tracked:
        errors.append('No tracked/staged files; stage the intended scaffold first.')
    ignored = git('ls-files', '-ci', '--exclude-standard', '-z').decode().split('\0')
    errors += [f'Tracked but excluded: {name}' for name in ignored if name]
    for name in tracked:
        path = ROOT / name
        if path.is_file() and path.stat().st_size > 5 * 1024 * 1024:
            errors.append(f'File exceeds 5 MiB: {name}')
    probes = ['.env', '.env.local', 'secrets/token.txt', 'datasets/restricted.json',
              'platform/tests/patient.wav', 'video/renders/final/demo.mp4',
              'platform/voice-analysis/models/model.onnx', 'local-data/patient.json']
    for name in probes:
        result = subprocess.run(['git', 'check-ignore', '-q', '--no-index', name], cwd=ROOT)
        if result.returncode != 0:
            errors.append(f'Exclusion missing: {name}')
    if errors:
        print('\n'.join(errors))
        return 1
    print(f'OK: structure, exclusions and {len(tracked)} tracked/staged files checked.')
    print('Manual content review remains required before publishing.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
