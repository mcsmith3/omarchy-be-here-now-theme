#!/usr/bin/env python3
"""Install the Be Here Now pixel-dissolve screensaver.

Works on a stock Omarchy install and alongside other themes that share the
theme-aware screensaver dispatcher (for example Expanse or Kingston).
"""
import argparse
import datetime
import getpass
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
ANCHOR = 'case "$theme_name" in\n'
BRANCH = '''  be-here-now)
    launcher="$HOME/.local/share/omarchy-be-here-now/launch-screensaver"
    ;;
'''
STOCK_LAUNCH = 'omarchy-launch-screensaver")'
EXPANSE_LAUNCH = '\\"$HOME/.local/share/omarchy-expanse/launch-screensaver\\"")'
DISPATCH_LAUNCH = '\\"$HOME/.local/share/omarchy-theme-screensaver/launch-screensaver\\"")'
ASSETS = ('shell.qml', 'pixel-dissolve.frag', 'pixel-dissolve.frag.qsb', 'launch-screensaver')


def patch_service(text):
    """Point the idle service at the shared theme dispatcher."""
    if DISPATCH_LAUNCH in text:
        return text
    matches = [c for c in (STOCK_LAUNCH, EXPANSE_LAUNCH) if text.count(c) == 1]
    if len(matches) != 1:
        raise ValueError('Unsupported Omarchy idle service; no files changed.')
    return text.replace(matches[0], DISPATCH_LAUNCH, 1)


def patch_dispatcher(text):
    """Add the be-here-now route to an existing dispatcher."""
    if BRANCH in text:
        return text
    if '  be-here-now)' in text:
        raise ValueError('An unfamiliar Be Here Now dispatch entry already exists.')
    if text.count(ANCHOR) != 1:
        raise ValueError('Unsupported screensaver dispatcher; no files changed.')
    return text.replace(ANCHOR, ANCHOR + BRANCH, 1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='check compatibility without making changes')
    args = parser.parse_args()
    home = Path.home()

    omarchy = Path(os.environ.get('OMARCHY_PATH', '/usr/share/omarchy'))
    plugin_id = getpass.getuser() + '.idle'
    plugin = home / '.config/omarchy/plugins' / plugin_id
    if plugin.exists():
        manifest = json.loads((plugin / 'manifest.json').read_text())
        if manifest.get('omarchy', {}).get('clonedFrom') != 'omarchy.idle':
            raise ValueError(f'{plugin} is not a clone of omarchy.idle.')
        service = (plugin / 'Service.qml').read_text()
    else:
        service = (omarchy / 'shell/plugins/services/idle/Service.qml').read_text()
    new_service = patch_service(service)

    dispatcher = home / '.local/share/omarchy-theme-screensaver/launch-screensaver'
    current = dispatcher.read_text() if dispatcher.exists() else (ROOT / 'screensaver/dispatch-screensaver').read_text()
    new_dispatcher = patch_dispatcher(current)
    subprocess.run(['bash', '-n'], input=new_dispatcher, text=True, check=True)

    for command in ('qs', 'omarchy', 'omarchy-shell', 'omarchy-launch-screensaver', 'flock', 'hyprctl', 'jq'):
        if not shutil.which(command):
            raise ValueError(f'Missing command: {command}')
    for asset in ASSETS:
        if not (ROOT / 'screensaver' / asset).is_file():
            raise ValueError(f'Missing screensaver asset: {asset}')
    qml = (ROOT / 'screensaver/shell.qml').read_text()
    for image in re.findall(r'file: "([^"]+)"', qml):
        if not (ROOT / 'backgrounds' / image).is_file():
            raise ValueError(f'Missing background: {image}')

    if args.check:
        print('Compatible idle service and dispatcher; backgrounds and shader are ready. No files changed.')
        return

    status = json.loads(subprocess.check_output(['omarchy-shell', 'lock', 'status'], text=True))
    if status.get('locked') or status.get('requested') or status.get('secure'):
        raise ValueError('Unlock the session before installing.')

    runtime = home / '.local/share/omarchy-be-here-now'
    backup = home / '.local/state/omarchy/backups' / (
        'be-here-now-screensaver-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
    backup.mkdir(parents=True)
    if plugin.exists():
        shutil.copytree(plugin, backup / 'idle-plugin')
    if dispatcher.exists():
        shutil.copy2(dispatcher, backup / 'launch-screensaver')
    if runtime.exists():
        shutil.copytree(runtime, backup / 'runtime')

    # Theme runtime: QML, shader, launcher and the backgrounds.
    config = runtime / 'org.omarchy.screensaver'
    config.mkdir(parents=True, exist_ok=True)
    for asset in ASSETS:
        shutil.copy2(ROOT / 'screensaver' / asset, config / asset)
    images = config / 'images'
    if images.is_symlink():
        images.unlink()
    shutil.copytree(ROOT / 'backgrounds', images, dirs_exist_ok=True)
    shutil.copy2(ROOT / 'screensaver/launch-screensaver', runtime / 'launch-screensaver')
    (runtime / 'launch-screensaver').chmod(0o755)

    # Shared dispatcher, created or extended.
    dispatcher.parent.mkdir(parents=True, exist_ok=True)
    temporary = dispatcher.with_name('launch-screensaver.new')
    temporary.write_text(new_dispatcher)
    temporary.chmod(0o755)
    temporary.replace(dispatcher)

    # Idle service: only touched when it does not use the dispatcher yet.
    restart = False
    if new_service != service or not plugin.exists():
        if not plugin.exists():
            subprocess.run(['omarchy', 'plugin', 'clone', 'omarchy.idle'], check=True)
        target = plugin / 'Service.qml'
        temporary = target.with_name('Service.qml.new')
        temporary.write_text(patch_service(target.read_text()))
        temporary.replace(target)
        subprocess.run(['omarchy-shell', 'shell', 'rescanPlugins'], check=True)
        subprocess.run(['omarchy', 'plugin', 'enable', plugin_id], check=True)
        restart = True

    print(f'Installed the Be Here Now screensaver. Backup: {backup}')
    if restart:
        print('Activate it with: omarchy restart shell')
    else:
        print('The idle service already uses the dispatcher; no shell restart needed.')
    print(f'Preview: {runtime}/launch-screensaver --preview')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        sys.exit(str(error))
