const VERSION='21.13.0';
const STATIC='portfolio-static-'+VERSION;
const PAGES='portfolio-pages-'+VERSION;
const CORE=[
  '/portfolio.css?v='+VERSION,
  '/portfolio.js?v='+VERSION,
  '/assets/portraits/byline.avif',
  '/assets/home/reference-desk-bg.webp'
];

self.addEventListener('install',event=>{
  event.waitUntil(caches.open(STATIC).then(cache=>Promise.allSettled(CORE.map(url=>cache.add(url)))));
  self.skipWaiting();
});

self.addEventListener('activate',event=>{
  event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(key=>key!==STATIC&&key!==PAGES).map(key=>caches.delete(key)))).then(()=>self.clients.claim()));
});

async function staticResponse(request){
  const cache=await caches.open(STATIC);
  const cached=await cache.match(request);
  if(cached){
    fetch(request).then(response=>{if(response&&response.ok)cache.put(request,response.clone())}).catch(()=>{});
    return cached;
  }
  const response=await fetch(request);
  if(response&&response.ok)cache.put(request,response.clone());
  return response;
}

async function pageResponse(request){
  const cache=await caches.open(PAGES);
  const cached=await cache.match(request);
  const network=fetch(request).then(response=>{
    if(response&&response.ok)cache.put(request,response.clone());
    return response;
  });
  if(!cached)return network;
  const timeout=new Promise(resolve=>setTimeout(()=>resolve(null),1400));
  try{
    const quick=await Promise.race([network,timeout]);
    return quick||cached;
  }catch(error){
    return cached;
  }
}

self.addEventListener('fetch',event=>{
  const request=event.request;
  if(request.method!=='GET')return;
  const url=new URL(request.url);
  if(url.origin!==self.location.origin)return;
  if(request.mode==='navigate'){
    event.respondWith(pageResponse(request));
    return;
  }
  if(['style','script','image','font'].includes(request.destination)){
    event.respondWith(staticResponse(request));
  }
});
