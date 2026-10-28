const REPO='arafat-247/arafat-portfolio';
export function androidRelease(releases) {
  if(!Array.isArray(releases)) return null;
  for(const release of releases.filter(r=>!r.draft && /^assistant-android-v0\.1\.\d+$/.test(r.tag_name||'')).sort((a,b)=>String(b.published_at||'').localeCompare(String(a.published_at||'')))) {
    const prefix=`https://github.com/${REPO}/releases/download/${release.tag_name}/`;
    const asset=(release.assets||[]).find(a=>a.name==='ArafatAssistant-Android.apk' && a.browser_download_url===prefix+'ArafatAssistant-Android.apk');
    const checksum=(release.assets||[]).find(a=>a.name==='ArafatAssistant-Android.apk.sha256' && a.browser_download_url===prefix+'ArafatAssistant-Android.apk.sha256');
    if(asset) return {release,asset,checksum};
  }
  return null;
}
async function initialise() {
  const status=document.querySelector('#build-status'),link=document.querySelector('#download-link'),detail=document.querySelector('#release-detail');
  try {
    const response=await fetch(`https://api.github.com/repos/${REPO}/releases?per_page=100`,{headers:{Accept:'application/vnd.github+json'},signal:AbortSignal.timeout(12000)});
    if(!response.ok) throw new Error();
    const build=androidRelease(await response.json());
    if(!build) { status.textContent='The first checked APK is not available yet.'; link.textContent='Waiting for Android build'; detail.textContent='Use View builds to check progress. The APK appears after its tests pass and a release is published.'; return; }
    status.textContent='A checked Android preview is available.'; link.href=build.asset.browser_download_url; link.removeAttribute('aria-disabled'); link.textContent='Download Android APK ↓';
    detail.textContent=`${Math.round(build.asset.size/1024/1024)} MB · ${build.release.tag_name} · Read the setup guide before enabling app controls.`;
    if(build.checksum) { const c=document.querySelector('#checksum-link'); c.href=build.checksum.browser_download_url; c.hidden=false; }
  } catch { status.textContent='The build status could not be checked.'; link.textContent='Check the GitHub builds'; detail.textContent='Use View builds or the source guide to find the Android preview release.'; }
}
if(typeof document!=='undefined') initialise();
