import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
const source=await readFile(new URL('../site/admin/github.js',import.meta.url),'utf8');
const {GitHub}=await import('data:text/javascript;base64,'+Buffer.from(source).toString('base64'));
test('Atomic save retains base tree and never force pushes',async()=>{
 const calls=[];globalThis.fetch=async(url,options)=>{calls.push({url,options,body:options.body?JSON.parse(options.body):null});return{ok:true,status:201,json:async()=>({sha:url.endsWith('/git/trees')?'new-tree':'new-commit'})}};
 const api=new GitHub('owner/repo','main','test-token');api.head='old-commit';api.tree='old-tree';await api.commit([{path:'content/posts.json',data:{posts:[]}}],'Save');
 assert.equal(calls[0].body.base_tree,'old-tree');assert.deepEqual(calls[1].body.parents,['old-commit']);assert.equal(calls[2].body.force,false);assert.equal(api.head,'new-commit');api.disconnect();assert.equal(api.token,'');
});
test('A rejected branch update does not advance local state',async()=>{
 globalThis.fetch=async(url)=>url.includes('/git/refs/')?{ok:false,status:422,json:async()=>({message:'Not a fast forward'})}:{ok:true,status:201,json:async()=>({sha:'new-sha'})};
 const api=new GitHub('owner/repo','main','test-token');api.head='old';api.tree='tree';await assert.rejects(()=>api.commit([{path:'content/posts.json',data:{}}],'Save'));assert.equal(api.head,'old');
});
test('Refresh request uses a normal content commit instead of Actions permission',async()=>{
 const calls=[];globalThis.fetch=async(url,options)=>{calls.push({url,body:options.body?JSON.parse(options.body):null});return{ok:true,status:201,json:async()=>({sha:url.endsWith('/git/trees')?'refresh-tree':'refresh-commit'})}};
 const api=new GitHub('owner/repo','main','test-token');api.head='old-commit';api.tree='old-tree';await api.dispatch(true);
 assert.equal(calls[0].url.endsWith('/git/trees'),true);assert.equal(calls[0].body.tree[0].path,'content/refresh-request.json');assert.equal(JSON.parse(calls[0].body.tree[0].content).deep_scan,true);assert.equal(calls[2].body.force,false);
});
