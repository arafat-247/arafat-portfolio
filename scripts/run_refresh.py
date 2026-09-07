import os, subprocess
from types import SimpleNamespace
from core import *
from sync import run
event=os.environ.get('EVENT_NAME','workflow_dispatch')
state=read(CONTENT/'sync-state.json',{})
changed=subprocess.run(['git','diff-tree','--root','--no-commit-id','--name-only','-r','HEAD'],capture_output=True,text=True,check=True).stdout.splitlines()
manual_request='content/refresh-request.json' in changed
request=read(CONTENT/'refresh-request.json',{}) if manual_request else {}
deep=os.environ.get('DEEP_SCAN','false').lower()=='true' or os.environ.get('EVENT_SCHEDULE')=='43 2 * * *' or bool(request.get('deep_scan'))
# While the first archive is incomplete, every suitable run advances it.
backfill=not state.get('listing_complete') or int(state.get('pending',0))>0
if event!='push' or 'content/imports.json' in changed or manual_request or backfill or not state.get('last_completed'):
    run(SimpleNamespace(full=deep,pages=180,limit=180 if deep else 60,delay=.35,workers=4))
else:print('Editorial save: deploy existing archive immediately; scheduled refresh continues separately.')
