"""Package only the current application, with no old releases or secrets."""
import hashlib, json, zipfile
from pathlib import Path
from core import ROOT, OUT
def package(destination):
    files=[]
    for dirname in ('content','tests','dist'):
        files.extend(p for p in (ROOT/dirname).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    for name in ('core.py','sync.py','migrate.py','build.py','validate.py','persist.py','run_refresh.py','package_release.py'):
        files.append(ROOT/'scripts'/name)
    for name in ('portfolio.css','portfolio.js'):files.append(ROOT/'site'/name)
    files.extend(p for p in (ROOT/'site/admin').rglob('*') if p.is_file())
    files.extend(p for p in (ROOT/'site/assets').rglob('*') if p.is_file() and 'photography-src' not in p.parts)
    # Original V14 indexes remain available for one-time migration; no old UI ships.
    for name in ('articles.json','photography.json','journal-index.json','site_config.json'):
        files.append(ROOT/'site/data'/name)
    for name in ('START-HERE.md','README.md','VALIDATION.md','requirements.txt','.github/workflows/deploy.yml','.gitignore','VERSION.txt'):
        files.append(ROOT/name)
    unique=sorted(set(files));destination=Path(destination);destination.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED) as z:
        for p in unique:
            if not p.is_file():raise ValueError('Missing release file: '+str(p))
            z.write(p,'arafat-portfolio-v15/'+str(p.relative_to(ROOT)))
        manifest={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in unique}
        z.writestr('arafat-portfolio-v15/MANIFEST-SHA256.json',json.dumps(manifest,indent=2))
    with zipfile.ZipFile(destination) as z:
        if z.testzip():raise ValueError('ZIP integrity check failed.')
    print(destination);print(len(unique)+1,'files;',destination.stat().st_size,'bytes')
if __name__=='__main__':
    import sys
    package(sys.argv[1])
