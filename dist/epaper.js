(()=>{'use strict';
const $=s=>document.querySelector(s);
const epaperButton=$('[data-epaper-view]'),epaperDialog=$('#epaper-dialog'),epaperSheet=$('.epaper-sheet'),epaperStage=$('.epaper-stage'),epaperStatus=$('[data-epaper-status]');
let epaperScale=1,epaperNatural={width:920,height:1260};
function setEpaperStatus(message){if(epaperStatus)epaperStatus.textContent=message||''}
function measureEpaper(){
 if(!epaperSheet)return epaperNatural;
 const previous=epaperSheet.style.getPropertyValue('--epaper-scale');
 epaperSheet.style.setProperty('--epaper-scale','1');
 epaperNatural={width:epaperSheet.offsetWidth||920,height:epaperSheet.scrollHeight||1260};
 if(previous)epaperSheet.style.setProperty('--epaper-scale',previous);else epaperSheet.style.removeProperty('--epaper-scale');
 return epaperNatural;
}
function setEpaperScale(value){
 if(!epaperSheet)return;
 const natural=measureEpaper();
 epaperScale=Math.max(.25,Math.min(1.5,value));
 epaperSheet.style.setProperty('--epaper-scale',epaperScale.toFixed(3));
 if(epaperStage){
  epaperStage.style.width=Math.ceil(natural.width*epaperScale)+'px';
  epaperStage.style.height=Math.ceil(natural.height*epaperScale)+'px';
 }
}
function fitEpaper(){
 if(!epaperDialog||!epaperSheet)return;
 const viewport=epaperDialog.querySelector('.epaper-viewport');
 const natural=measureEpaper();
 const compact=window.matchMedia('(max-width:800px)').matches;
 const availableWidth=Math.max(240,viewport.clientWidth-(compact?8:28));
 const availableHeight=Math.max(320,viewport.clientHeight-(compact?8:28));
 const scale=Math.min(1,availableWidth/natural.width,availableHeight/natural.height);
 setEpaperScale(scale);
 if(epaperStage){
  epaperStage.style.marginLeft='auto';
  epaperStage.style.marginRight='auto';
 }
 viewport.scrollTo({top:0,left:0});
 setEpaperStatus('Fit to screen');
}
function loadExternalScript(src,test){
 if(test())return Promise.resolve();
 return new Promise((resolve,reject)=>{
  const existing=document.querySelector(`script[src="${src}"]`);
  if(existing){
   existing.addEventListener('load',resolve,{once:true});
   existing.addEventListener('error',reject,{once:true});
   return;
  }
  const script=document.createElement('script');
  script.src=src;script.async=true;script.crossOrigin='anonymous';
  script.onload=resolve;script.onerror=()=>reject(new Error('Could not load export library'));
  document.head.appendChild(script);
 });
}
async function ensureEpaperExportLibraries(){
 await loadExternalScript('https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js',()=>typeof window.html2canvas==='function');
 await loadExternalScript('https://cdn.jsdelivr.net/npm/jspdf@2.5.1/dist/jspdf.umd.min.js',()=>!!window.jspdf?.jsPDF);
}
function epaperFilename(extension){
 const title=$('.reading h1')?.textContent.trim()||'article';
 const slug=title.toLowerCase().normalize('NFKD').replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,80)||'article';
 return `${slug}-epaper.${extension}`;
}
async function renderEpaperCanvas(){
 if(!epaperSheet)throw new Error('E-paper sheet is unavailable');
 await ensureEpaperExportLibraries();
 setEpaperStatus('Preparing HD export…');
 const oldScale=epaperScale;
 const oldTransition=epaperSheet.style.transition;
 epaperSheet.style.transition='none';
 setEpaperScale(1);
 await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));
 try{
  return await window.html2canvas(epaperSheet,{
   scale:3,
   useCORS:true,
   backgroundColor:'#f4f0e7',
   logging:false,
   imageTimeout:15000,
   width:epaperSheet.scrollWidth,
   height:epaperSheet.scrollHeight,
   windowWidth:epaperSheet.scrollWidth,
   windowHeight:epaperSheet.scrollHeight
  });
 }finally{
  epaperSheet.style.transition=oldTransition;
  setEpaperScale(oldScale);
 }
}
async function downloadEpaperImage(){
 const button=$('[data-download-epaper-image]');
 try{
  if(button)button.disabled=true;
  const canvas=await renderEpaperCanvas();
  const blob=await new Promise((resolve,reject)=>canvas.toBlob(value=>value?resolve(value):reject(new Error('Image export failed')),'image/png'));
  const filename=epaperFilename('png');
  const url=URL.createObjectURL(blob),link=document.createElement('a');
  link.href=url;
  link.download=filename;
  link.rel='noopener';
  link.style.display='none';
  document.body.appendChild(link);
  link.click();
  link.remove();
  setTimeout(()=>URL.revokeObjectURL(url),5000);
  setEpaperStatus(`PNG downloaded · ${canvas.width} × ${canvas.height}px`);
 }catch(error){
  console.error(error);setEpaperStatus('Image download failed. Please try again.');
 }finally{if(button)button.disabled=false}
}
async function downloadEpaperPdf(){
 const button=$('[data-download-epaper-pdf]');
 try{
  if(button)button.disabled=true;
  const canvas=await renderEpaperCanvas();
  const {jsPDF}=window.jspdf;
  const widthPt=canvas.width*.24,heightPt=canvas.height*.24;
  const pdf=new jsPDF({orientation:widthPt>heightPt?'landscape':'portrait',unit:'pt',format:[widthPt,heightPt],compress:true});
  pdf.addImage(canvas.toDataURL('image/png'),'PNG',0,0,widthPt,heightPt,undefined,'FAST');
  pdf.save(epaperFilename('pdf'));
  setEpaperStatus('HD PDF saved');
 }catch(error){
  console.error(error);setEpaperStatus('PDF download failed. Please try again.');
 }finally{if(button)button.disabled=false}
}
epaperButton?.addEventListener('click',()=>{
 if(!epaperDialog)return;
 epaperDialog.showModal();
 setEpaperStatus('');
 requestAnimationFrame(()=>requestAnimationFrame(fitEpaper));
});
$('[data-close-epaper]')?.addEventListener('click',()=>epaperDialog?.close());
$('[data-epaper-zoom-in]')?.addEventListener('click',()=>{setEpaperScale(epaperScale+.1);setEpaperStatus(Math.round(epaperScale*100)+'%')});
$('[data-epaper-zoom-out]')?.addEventListener('click',()=>{setEpaperScale(epaperScale-.1);setEpaperStatus(Math.round(epaperScale*100)+'%')});
$('[data-epaper-fit]')?.addEventListener('click',fitEpaper);
$('[data-download-epaper-image]')?.addEventListener('click',downloadEpaperImage);
$('[data-download-epaper-pdf]')?.addEventListener('click',downloadEpaperPdf);
epaperDialog?.addEventListener('click',event=>{if(event.target===epaperDialog)epaperDialog.close()});
epaperDialog?.addEventListener('close',()=>{setEpaperScale(1);setEpaperStatus('')});
window.addEventListener('resize',()=>{if(epaperDialog?.open)fitEpaper()},{passive:true});
})();
