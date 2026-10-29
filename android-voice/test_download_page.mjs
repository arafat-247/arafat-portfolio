import {strict as assert} from 'node:assert';
import {test} from 'node:test';
import {voiceRelease} from '../site/voice/voice.mjs';
const tag='assistant-voice-v0.1.1';
const asset=(name='ArafatVoice-Android.apk',release=tag)=>({name,browser_download_url:`https://github.com/arafat-247/arafat-portfolio/releases/download/${release}/${name}`});
const release=(version=tag,date='2026-10-29')=>({tag_name:version,published_at:date,assets:[asset('ArafatVoice-Android.apk',version)]});
test('voice download never selects the full-control app or an unpublished asset',()=>{
  for(const input of [null,[],[null],[release('assistant-android-v0.1.10')],[{...release(),draft:true}],[{...release(),assets:[]}],[{...release(),assets:[asset('ArafatAssistant-Android.apk')]}]]) assert.equal(voiceRelease(input),null);
  assert.equal(voiceRelease([release()]).asset.name,'ArafatVoice-Android.apk');
});
test('voice assets must belong to the exact repository and matching release',()=>{
  for(const url of ['javascript:alert(1)','https://example.com/app.apk',asset('ArafatVoice-Android.apk','assistant-voice-v0.1.2').browser_download_url]) assert.equal(voiceRelease([{...release(),assets:[{...asset(),browser_download_url:url}]}]),null);
});
test('newest usable voice release wins with its own checksum',()=>{
  const latest={...release('assistant-voice-v0.1.2','2026-10-30'),assets:[asset('ArafatVoice-Android.apk','assistant-voice-v0.1.2'),asset('ArafatVoice-Android.apk.sha256','assistant-voice-v0.1.2')]};
  const picked=voiceRelease([release(),latest,{...release('assistant-voice-v0.1.3','2026-10-31'),assets:[]}]);
  assert.equal(picked.release.tag_name,latest.tag_name); assert.equal(picked.checksum.name,'ArafatVoice-Android.apk.sha256');
});
