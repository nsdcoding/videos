const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const mode=process.argv[2];const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
 p.on('pageerror',e=>console.log('ERR',e.message));
 await p.goto('file://'+__dirname+'/banner.html');await p.evaluate(()=>document.fonts.ready);
 await p.evaluate(()=>Promise.all([...document.images].map(i=>i.complete?1:new Promise(r=>i.onload=r))));await p.waitForTimeout(400);
 const clip={x:0,y:0,width:1920,height:1080};
 if(mode==='test'){for(const t of process.argv.slice(3)){await p.evaluate(t=>render(+t),t);await p.screenshot({path:`b_${t}.png`,omitBackground:true});}}
 else{fs.mkdirSync('bf',{recursive:true});const fps=30,n=Math.round(+process.argv[3]*fps);
  for(let f=0;f<n;f++){await p.evaluate(t=>render(t),f/fps);await p.screenshot({path:`bf/${String(f).padStart(4,'0')}.png`,omitBackground:true});}}
 await b.close()})();
