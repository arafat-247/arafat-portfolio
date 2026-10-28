import {strict as assert} from 'node:assert';
import {test} from 'node:test';
import {androidRelease} from '../site/android/android.mjs';
const asset=(tag='assistant-android-v0.1.1')=>({name:'ArafatAssistant-Android.apk',browser_download_url:`https://github.com/arafat-247/arafat-portfolio/releases/download/${tag}/ArafatAssistant-Android.apk`});
const release=(tag='assistant-android-v0.1.1',date='2026-10-29')=>({tag_name:tag,published_at:date,assets:[asset(tag)]});
test('only actual published Android APKs qualify',()=>{
  assert.equal(androidRelease(null),null); assert.equal(androidRelease([]),null);
  assert.equal(androidRelease([release('assistant-v0.3.20')]),null);
  assert.equal(androidRelease([{...release(),draft:true}]),null);
  assert.equal(androidRelease([{...release(),assets:[]}]),null);
  assert.equal(androidRelease([release()]).asset.name,'ArafatAssistant-Android.apk');
});
test('links must belong to the matching repository release',()=>{
  for(const url of ['javascript:alert(1)','https://example.com/app.apk',asset('assistant-android-v0.1.2').browser_download_url]) assert.equal(androidRelease([{...release(),assets:[{...asset(),browser_download_url:url}]}]),null);
});
test('newest usable Android release wins',()=>{
  const good=release('assistant-android-v0.1.2','2026-10-30');
  assert.equal(androidRelease([release(),good,{...release('assistant-android-v0.1.3','2026-10-31'),assets:[]}]).release.tag_name,good.tag_name);
});
