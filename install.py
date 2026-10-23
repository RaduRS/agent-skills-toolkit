#!/usr/bin/env python3
"""Offline, user-level installer. Python 3.9+; standard library only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
from datetime import datetime, timezone

NAMES = (
    'spec-driven-development', 'planning-and-task-breakdown',
    'api-and-interface-design', 'test-driven-development',
    'debugging-and-error-recovery', 'security-and-hardening',
    'codebase-design', 'verification-before-completion',
    'ui-ux-pro-max', 'vercel-react-best-practices',
)
ROOT = Path(__file__).resolve().parent


def is_link(path):
    return path.is_symlink() or getattr(path, 'is_junction', lambda: False)()


def plain_path(path):
    path = Path(os.path.abspath(path.expanduser()))
    for parent in (path, *path.parents):
        if is_link(parent):
            raise ValueError('Refusing symlink/junction path: ' + str(parent))
    return path


def inventory(folder):
    result = {}
    if is_link(folder) or not folder.is_dir():
        raise ValueError('Expected ordinary directory: ' + str(folder))
    for path in folder.rglob('*'):
        if is_link(path):
            raise ValueError('Refusing symlink/junction: ' + str(path))
        if path.is_file():
            result[path.relative_to(folder).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
        elif not path.is_dir():
            raise ValueError('Unsupported filesystem entry: ' + str(path))
    return result


def payload():
    manifest = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
    if manifest['skills'] != list(NAMES):
        raise ValueError('Manifest skill allowlist mismatch')
    expected = manifest['installed_files']
    if set(expected) != set(NAMES):
        raise ValueError('Manifest file groups mismatch')
    for name in NAMES:
        if inventory(ROOT / 'skills' / name) != expected[name]:
            raise ValueError('Bundle checksum/inventory mismatch: ' + name)
    return expected


def check_installed(destination, expected):
    for name in NAMES:
        if inventory(destination / name) != expected[name]:
            raise ValueError('Installed files modified or incomplete: ' + name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['install', 'verify', 'backup'], nargs='?', default='install')
    parser.add_argument('--destination', type=Path, default=Path.home() / '.agents' / 'skills')
    parser.add_argument('--add-missing', action='store_true', help='Skip identical installed skills; install missing only; refuse any modified collision')
    args = parser.parse_args()
    if args.add_missing and args.action != 'install':
        parser.error('--add-missing applies only to install')
    expected = payload()  # Validate every source before any mutation.
    destination = plain_path(args.destination)
    if destination == Path(destination.anchor):
        raise ValueError('Refusing a filesystem root as destination')
    if args.action == 'verify':
        check_installed(destination, expected)
        print('Verified ten installed skills and every supporting file at ' + str(destination))
        return
    if args.action == 'backup':
        # Explicit command is consent to move these ten unchanged owned folders.
        # No deletion, broad cleanup, overwrite or fallback path.
        check_installed(destination, expected)
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        backup = plain_path(destination.parent / 'skill-backups' / ('agent-skills-toolkit-' + stamp))
        backup.mkdir(parents=True, exist_ok=False)
        for name in NAMES:
            shutil.move(str(destination / name), str(backup / name))
        print('Moved ten unchanged skills to recoverable backup: ' + str(backup))
        return
    conflicts = [name for name in NAMES if os.path.lexists(destination / name)]
    if args.add_missing:
        for name in conflicts:
            if inventory(destination / name) != expected[name]:
                raise ValueError('Modified existing destination; nothing installed: ' + name)
    if conflicts and not args.add_missing:
        raise ValueError('Nothing installed. Existing destinations: ' + ', '.join(conflicts)
                         + '. See README update/backup instructions.')
    destination.mkdir(parents=True, exist_ok=True)
    # mkdir(exist_ok=False) prevents replacing a destination created after preflight.
    # On interruption, preserve partial files for inspection; never silently clean up.
    for name in NAMES:
        if args.add_missing and name in conflicts:
            continue
        target = destination / name
        target.mkdir(exist_ok=False)
        for relative in expected[name]:
            source = ROOT / 'skills' / name / relative
            output = target / relative
            output.parent.mkdir(parents=True, exist_ok=True)
            with output.open('xb') as handle:
                handle.write(source.read_bytes())
    check_installed(destination, expected)
    print('Installed and verified ten skills at ' + str(destination))
    print('Available on the next Codex turn; restart Codex if they do not appear.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as error:
        print('Stopped: ' + str(error), file=sys.stderr)
        sys.exit(1)
