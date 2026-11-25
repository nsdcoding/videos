const {chromium}=require('playwright');const {spawn}=require('child_process');
(async()=>{
 const mode=process.argv[2];const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
 p.on('console',m=>console.log('console:',m.text()));p.on('pageerror',e=>console.log('ERR',e.message));
 await p.goto('file://'+__dirname+'/'+(process.env.PAGE||'promo.html'));await p.evaluate(()=>document.fonts.ready);
 await p.evaluate(()=>Promise.all([...document.images].map(i=>i.complete?1:new Promise(r=>i.onload=r))));
 await p.waitForTimeout(500);
 if(mode==='test'){for(const t of process.argv.slice(3)){await p.evaluate(t=>render(+t),t);await p.screenshot({path:`test_${t}.png`});}}
 else{const fps=30,dur=+process.argv[3];
  const ff=spawn('ffmpeg',['-y','-f','image2pipe','-framerate',''+fps,'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p','video.mp4'],{stdio:['pipe','ignore','inherit']});
  for(let f=0;f<Math.round(dur*fps);f++){await p.evaluate(t=>render(t),f/fps);const buf=await p.screenshot({type:'jpeg',quality:95});
   if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r)); if(f%60==0)console.log('frame',f);}
  ff.stdin.end();await new Promise(r=>ff.on('close',r));}
 await b.close();})();
