"""Commit durable archives before deploying. No force push or silent conflict merge."""
import subprocess
def git(*args):return subprocess.run(['git',*args],check=True,capture_output=True,text=True).stdout.strip()
def main():
    git('config','user.name','Portfolio archive bot');git('config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
    # The full package includes a ready-built dist tree. Stage its regenerated
    # files too, so tracked output cannot leave a dirty tree before rebase.
    git('add','content','site/assets','dist')
    if not git('diff','--cached','--name-only'):return
    git('commit','-m','Save permanent portfolio archive [skip ci]')
    # A concurrent admin commit is replayed only when Git can merge cleanly.
    # A conflict fails this run and the next run tries again from fresh content.
    git('pull','--rebase','origin','main')
    git('push','origin','HEAD:main')
if __name__=='__main__':main()
