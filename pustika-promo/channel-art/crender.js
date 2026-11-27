const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:2560,height:1440}});
 await p.goto('file://'+__dirname+'/channel.html');await p.evaluate(()=>document.fonts.ready);
 await p.evaluate(()=>Promise.all([...document.images].map(i=>i.complete?1:new Promise(r=>i.onload=r))));await p.waitForTimeout(400);
 await p.screenshot({path:'channel_art.png'});
 await p.evaluate(()=>document.body.classList.add('guide'));await p.screenshot({path:'channel_guide.png'});
 await b.close()})();
