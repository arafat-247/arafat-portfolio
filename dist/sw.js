const VERSION='21.17.0';
const STATIC='portfolio-static-'+VERSION;
const PAGES='portfolio-pages-'+VERSION;
const CORE=[
  '/portfolio.css?v='+VERSION,
  '/portfolio.js?v='+VERSION,
  '/assets/portraits/byline.avif'
];

self.addEventListener('install',event=>{
  event.waitUntil(caches.open(STATIC).then(cache=>Promise.allSettled(CORE.map(url=>cache.add(url)))));
  self.skipWaiting();
});

self.addEventListener('activate',event=>{
  event.waitUntil((async()=>{
    const keys=await caches.keys();
    await Promise.all(keys.filter(key=>key!==STATIC&&key!==PAGES).map(key=>caches.delete(key)));
    if(self.registration.navigationPreload)await self.registration.navigationPreload.enable();
    await self.clients.claim();
  })());
});

async function staticResponse(request,event){
  const cache=await caches.open(STATIC);
  const cached=await cache.match(request);
  const update=fetch(request).then(response=>{
    if(response&&response.ok)cache.put(request,response.clone());
    return response;
  }).catch(()=>null);
  if(cached){
    event.waitUntil(update);
    return cached;
  }
  return (await update)||Response.error();
}

async function pageResponse(request,event){
  const cache=await caches.open(PAGES);
  const cached=await cache.match(request);
  const update=(async()=>{
    const preload=await event.preloadResponse;
    const response=preload||await fetch(request);
    if(response&&response.ok)await cache.put(request,response.clone());
    return response;
  })().catch(()=>null);

  if(cached){
    event.waitUntil(update);
    return cached;
  }
  return (await update)||Response.error();
}

self.addEventListener('fetch',event=>{
  const request=event.request;
  if(request.method!=='GET')return;
  const url=new URL(request.url);
  if(url.origin!==self.location.origin)return;
  if(request.mode==='navigate'){
    event.respondWith(pageResponse(request,event));
    return;
  }
  if(['style','script','image','font'].includes(request.destination)){
    event.respondWith(staticResponse(request,event));
  }
});
