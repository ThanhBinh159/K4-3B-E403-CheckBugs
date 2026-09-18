"""Allowlisted clean archive: never include private env, data or raw traces."""
import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
DIRS = {'codebase', 'eval', 'evidence', 'validation', 'reflection', 'submission', 'slides', 'tools', 'docs'}
TOP = {'README.md', 'spec.md', '.gitignore', '.env.example', 'demo-slides.pdf'}
EXTENSIONS = {'.md', '.json', '.py', '.js', '.css', '.html', '.svg', '.mmd', '.pdf'}


def allowed(path):
    rel = path.relative_to(ROOT)
    if '__pycache__' in rel.parts or any(p in {'runs', 'logs', '.git', 'tmp', 'data', 'node_modules'} for p in rel.parts):
        return False
    return (len(rel.parts) == 1 and rel.name in TOP) or (rel.parts[0] in DIRS and path.suffix in EXTENSIONS)


def main():
    output = ROOT / 'output'
    output.mkdir(exist_ok=True)
    files = sorted(p for p in ROOT.rglob('*') if p.is_file() and allowed(p))
    manifest = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    archive = output / 'VLearn-GroundedTutor-submission.zip'
    with ZipFile(archive, 'w', ZIP_DEFLATED) as package:
        for path in files:
            package.write(path, path.relative_to(ROOT).as_posix())
        package.writestr('submission/manifest-sha256.json', json.dumps(manifest, indent=2))
    with ZipFile(archive) as package:
        assert package.testzip() is None
        assert '.env' not in package.namelist()
        assert not any(name.startswith(('data/', 'logs/', 'eval/runs/', 'tmp/')) for name in package.namelist())
    print(f'Clean ZIP: {archive}, {len(files)} files plus SHA-256 manifest.')


if __name__ == '__main__':
    main()
