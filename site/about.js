AR.loadConfig().then(config=>{
  const host=document.querySelector('#recognition-list');if(!host)return;
  const items=config.recognition||[];
  host.innerHTML=items.length?items.map(x=>`<div class="recognition-item"><span>${AR.esc(x.year||'')}</span><div><strong>${AR.esc(x.title||'')}</strong><small>${AR.esc(x.organisation||'')}</small></div></div>`).join(''):'<div class="recognition-item"><span>—</span><div><strong>Selected recognition will appear here.</strong></div></div>';
}).catch(()=>{});
