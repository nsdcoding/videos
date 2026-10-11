const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
p.on('pageerror',e=>console.log('PAGEERR',e.message));
await p.goto('http://localhost:8124/render/index.html');await p.waitForFunction('window.READY===true');
const L=await p.evaluate(()=>[...document.querySelectorAll('#world > div')].map(d=>[d.t0,d.t1]).filter(x=>x[0]>73));
const st=await p.$('#stage');
for(const [a,c] of L){const t=a+Math.min(c-a,8)*0.8; await p.evaluate(t=>renderFrame(t),t);
 await st.screenshot({path:`/tmp/claude-0/mt/f_${t.toFixed(1).padStart(6,'0')}.jpg`,type:'jpeg',quality:70});}
await b.close();})()
