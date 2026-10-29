"""Check the delivered manifest and DEX, rather than relying on source-only declarations."""
import pathlib
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile

apk = pathlib.Path(sys.argv[1])
analyser = sys.argv[2]
manifest = subprocess.check_output([analyser, 'manifest', 'print', str(apk)], text=True)
print(manifest)
root = ET.fromstring(manifest)
ns = '{http://schemas.android.com/apk/res/android}'
assert root.get('package') == 'com.arafat.assistant.voice'
assert [e.get(ns+'name') for e in root.findall('uses-permission')] == ['android.permission.INTERNET']
app = root.find('application')
assert app is not None
assert app.get(ns+'testOnly', 'false') == 'false'
assert app.get(ns+'usesCleartextTraffic') == 'false'
for kind in ('service', 'receiver', 'provider', 'activity-alias'):
    assert not app.findall(kind), f'Unexpected {kind} in voice APK'
assert len(app.findall('activity')) == 1
assert app.find('activity').get(ns+'name') == 'com.arafat.assistant.VoiceActivity'
with zipfile.ZipFile(apk) as archive:
    assert archive.testzip() is None
    dex = b''.join(archive.read(n) for n in archive.namelist() if n.endswith('.dex'))
    for forbidden in (b'Lcom/arafat/assistant/DeviceService;', b'Lcom/arafat/assistant/Agent;', b'Lcom/arafat/assistant/PlanClient;'):
        assert forbidden not in dex, f'Control dependency in voice APK: {forbidden}'
defined = subprocess.check_output([analyser, 'dex', 'packages', '--defined-only', str(apk)], text=True)
print(defined)
# Desugaring may reference Android framework APIs that this app does not implement.
# Check actual definitions as well as the no-service manifest and absent control code.
assert not any(line.strip().endswith('android.accessibilityservice.AccessibilityService') for line in defined.splitlines())
print('Voice APK verified: INTERNET only; no services or device-control classes.')
