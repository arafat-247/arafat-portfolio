import {strict as assert} from 'node:assert';
import {test} from 'node:test';
import {assistantRelease} from '../site/assistant/assistant.mjs';

const asset = (name='ArafatAssistant-Windows-x64.zip', url='https://github.com/arafat-247/arafat-portfolio/releases/download/assistant-v0.3.1/ArafatAssistant-Windows-x64.zip') => ({name,browser_download_url:url});
const release = (tag, date, assets) => ({tag_name:tag,published_at:date,assets});

test('missing builds do not create a download', () => {
  assert.equal(assistantRelease(null),null);
  assert.equal(assistantRelease([]),null);
  assert.equal(assistantRelease([release('assistant-v0.2.9','2026-10-28',[asset()])]),null);
  assert.equal(assistantRelease([release('portfolio-v20','2026-10-28',[asset()])]),null);
});
test('only assistant releases with the actual package qualify', () => {
  const build = release('assistant-v0.3.1','2026-10-28',[asset()]);
  assert.equal(assistantRelease([build]).asset.name,'ArafatAssistant-Windows-x64.zip');
  assert.equal(assistantRelease([{...build,draft:true}]),null);
  assert.equal(assistantRelease([{...build,assets:[]}]),null);
});
test('unrelated and malicious destinations are rejected', () => {
  for(const url of ['javascript:alert(1)','https://example.com/app.zip','https://github.com/another/repo/releases/download/v1/app.zip']) {
    assert.equal(assistantRelease([release('assistant-v0.3.1','2026-10-28',[asset(undefined,url)])]),null);
  }
});
test('the newest downloadable assistant build wins', () => {
  const older=release('assistant-v0.3.1','2026-10-27',[asset()]);
  const newer=release('assistant-v0.3.2','2026-10-28',[asset(),asset('ArafatAssistant-Windows-x64.zip.sha256')]);
  const empty=release('assistant-v0.3.3','2026-10-29',[]);
  const result=assistantRelease([older,empty,newer]);
  assert.equal(result.release.tag_name,'assistant-v0.3.2');
  assert.equal(result.checksum.name,'ArafatAssistant-Windows-x64.zip.sha256');
});
