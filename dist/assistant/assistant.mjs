const REPO = 'arafat-247/arafat-portfolio';
const DOWNLOAD_PREFIX = `https://github.com/${REPO}/releases/download/`;

export function assistantRelease(releases) {
  if (!Array.isArray(releases)) return null;
  const candidates = releases.filter(r => !r.draft && /^assistant-v0\.2\.\d+$/.test(r.tag_name || ''))
    .sort((a,b) => String(b.published_at || '').localeCompare(String(a.published_at || '')));
  for (const release of candidates) {
    const asset = (release.assets || []).find(a => a.name === 'ArafatAssistant-Windows-x64.zip' && String(a.browser_download_url || '').startsWith(DOWNLOAD_PREFIX));
    if (!asset) continue;
    const checksum = (release.assets || []).find(a => a.name === 'ArafatAssistant-Windows-x64.zip.sha256' && String(a.browser_download_url || '').startsWith(DOWNLOAD_PREFIX));
    return { release, asset, checksum };
  }
  return null;
}

async function initialise() {
  const status = document.querySelector('#build-status');
  const link = document.querySelector('#download-link');
  const detail = document.querySelector('#release-detail');
  const checksumLink = document.querySelector('#checksum-link');
  try {
    const response = await fetch(`https://api.github.com/repos/${REPO}/releases?per_page=100`, {headers:{Accept:'application/vnd.github+json'},signal:AbortSignal.timeout(12000)});
    if (!response.ok) throw new Error(`GitHub returned ${response.status}`);
    const build = assistantRelease(await response.json());
    if (!build) {
      status.textContent = 'The first tested download is not available yet.';
      link.textContent = 'Waiting for Windows build';
      detail.textContent = 'Open View builds to see the current run. The download appears after its checks pass and a release is published.';
      return;
    }
    link.href = build.asset.browser_download_url;
    link.removeAttribute('aria-disabled');
    link.textContent = 'Download Windows preview ↓';
    status.textContent = 'A tested package is available.';
    const size = Number.isFinite(build.asset.size) ? `${Math.round(build.asset.size / 1024 / 1024)} MB · ` : '';
    detail.textContent = `${size}${build.release.tag_name} · Read QUICK_START.txt after extracting.`;
    if (build.checksum) {
      checksumLink.href = build.checksum.browser_download_url;
      checksumLink.target = '_blank';
      checksumLink.rel = 'noopener noreferrer';
      checksumLink.hidden = false;
    }
  } catch {
    status.textContent = 'The build status could not be checked.';
    link.textContent = 'Check the GitHub builds';
    detail.textContent = 'Use View builds to check for a download. GitHub may be unavailable or limiting requests.';
  }
}

if (typeof document !== 'undefined') initialise();
