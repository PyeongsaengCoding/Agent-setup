#!/usr/bin/env python3
"""Start server.py with the Python runtime the installed Hermes uses."""
import json, os, pathlib, subprocess

home = pathlib.Path(os.environ.get('HERMES_HOME', pathlib.Path.home() / '.hermes'))
entry = home / 'hermes-agent/.hermes/bin/hermes'
command = json.loads(subprocess.check_output([str(entry), '--print-runtime-command'], text=True, timeout=15))
server = pathlib.Path(__file__).with_name('server.py')
os.execv(command[0], [command[0], '-I', str(server)])
