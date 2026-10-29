const REPO='arafat-247/arafat-portfolio';
export function voiceRelease(releases) {
  if(!Array.isArray(releases)) return null;
  for(const release of releases.filter(r=>r && !r.draft && /^assistant-voice-v0\.1\.\d+$/.test(r.tag_name||'')).sort((a,b)=>String(b.published_at||'').localeCompare(String(a.published_at||'')))) {
    const prefix=`https://github.com/${REPO}/releases/download/${release.tag_name}/`;
    const assets=Array.isArray(release.assets)?release.assets:[];
    const asset=assets.find(a=>a.name==='ArafatVoice-Android.apk' && a.browser_download_url===prefix+'ArafatVoice-Android.apk');
    const checksum=assets.find(a=>a.name==='ArafatVoice-Android.apk.sha256' && a.browser_download_url===prefix+'ArafatVoice-Android.apk.sha256');
    if(asset) return {release,asset,checksum};
  }
  return null;
}
async function initialise() {
  const status=document.querySelector('#build-status'),link=document.querySelector('#download-link'),detail=document.querySelector('#release-detail');
  try {
    const response=await fetch(`https://api.github.com/repos/${REPO}/releases?per_page=100`,{headers:{Accept:'application/vnd.github+json'},signal:AbortSignal.timeout(12000)});
    if(!response.ok) throw new Error();
    const build=voiceRelease(await response.json());
    if(!build) { status.textContent='The voice-only APK has not been published yet.'; link.textContent='Waiting for voice build'; detail.textContent='Use View builds to check progress. The older full-control APK is a separate app.'; return; }
    status.textContent='A checked voice-only preview is available.'; link.href=build.asset.browser_download_url; link.removeAttribute('aria-disabled'); link.textContent='Download Arafat Voice APK ↓';
    detail.textContent=`${Math.ceil(build.asset.size/1024)} KB · ${build.release.tag_name} · Voice dictation and text only.`;
    if(build.checksum) { const checksum=document.querySelector('#checksum-link'); checksum.href=build.checksum.browser_download_url; checksum.hidden=false; }
  } catch { status.textContent='The build status could not be checked.'; link.textContent='Use View builds'; detail.textContent='The source guide links to the checked voice-only release. Keep phone protections enabled.'; }
}
if(typeof document!=='undefined') initialise();
