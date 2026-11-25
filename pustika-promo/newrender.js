const SUBS=[[0.5,2.06,'हज़ार से ज़्यादा हिंदी किताबें'],[2.08,3.08,'पढ़िए भी, सुनिए भी'],[3.1,4.45,'पुस्तिका डॉट को डॉट इन पर']];
const S=1/1.79;
const set=(el,css)=>Object.assign(el.style,css);
function render(t){
 drawParticles($('pc'),t,'#E7C77A',1);
 // logo intro 0-0.8
 const l=P(t,0,.38), lk=eBack(l), out1=eIO(P(t,.42,.8));
 set($('logo'),{transform:`translateY(${(1-eOut(l))*50}px) scale(${lerp(.3,1,lk)*(1+out1*1.6)}) rotate(${(1-eOut(l))*-10}deg)`,opacity:clamp(l*4)*(1-out1)});
 set($('shine'),{left:`${lerp(-60,160,eIO(P(t,.15,.55)))}%`});
 ['r1','r2','r3'].forEach((id,i)=>{const k=P(t,.02+i*.12,.8+i*.12);const s=lerp(300,1500,eOut(k));
  set($(id),{width:s+'px',height:s+'px',marginLeft:-s/2+'px',marginTop:-s/2+'px',opacity:(1-k)*.9*(k>0?1:0)})});
 $('tag1').style.display='none';
 $('s1').style.display=t<0.85?'block':'none';
 // cream wipe
 const w=eIO(P(t,.42,.8));
 set($('cream'),{position:'absolute',inset:0,clipPath:`circle(${w*1200}px at 50% 48%)`,display:(t>.4&&t<3.45)?'block':'none'});
 drawParticles($('cc'),t+3,'#8E5FA8',.35);
 // counter 0.55-2.25
 const ck=eOut(P(t,.6,1.5)), n=Math.round(ck*1000);
 $('count').textContent=n>=1000?'1000+':n;
 const ex2=eIO(P(t,1.85,2.25));
 set($('count'),{opacity:P(t,.5,.7)*(1-ex2),transform:`translateY(${-ex2*160}px) scale(${lerp(.85,1,eOut(P(t,.5,.9)))*(1+.05*Math.sin(Math.PI*P(t,1.5,1.75)))*(1-ex2*.3)})`});
 set($('underline'),{transform:`scaleX(${eOut(P(t,1.45,1.7))})`,opacity:1-ex2});
 const lb=eOut(P(t,.7,1.05));
 set($('countLbl'),{opacity:lb*(1-ex2),transform:`translateY(${(1-lb)*40-ex2*120}px)`,clipPath:`inset(0 ${(1-lb)*50}% 0 ${(1-lb)*50}%)`});
 const sb=eOut(P(t,1.55,1.85));
 set($('countSub'),{opacity:sb*(1-ex2),transform:`translateY(${(1-sb)*20-ex2*100}px)`,letterSpacing:lerp(20,6,sb)+'px'});
 CV.forEach((c,i)=>{const k=eOut(P(t,.5+i*.08,1.0+i*.08)),ex=eIO(P(t,1.8+i*.03,2.2+i*.03));
  const fx=lerp(c.from[0],c.x,k),fy=lerp(c.from[1],c.y,k),ox=(c.x+c.w/2-960)*ex*1.4,oy=(c.y+c.h/2-520)*ex*1.4;
  const bob=Math.sin(t*3+i)*8,par=(t-1)*(i%2?14:-14);
  set(covEls[i],{left:0,top:0,transform:`translate(${fx+ox+par}px,${fy+oy+bob}px) rotate(${lerp(c.r*4,c.r,k)+Math.sin(t*2+i)*2}deg) scale(${1-ex*.3})`,opacity:k*(1-ex),display:t<2.3?'block':'none'})});
 $('s2').style.display=t<2.3?'block':'none';
 // phone 1.9-3.45
 const pin=eOut(P(t,1.9,2.4));
 const tiltY=lerp(-28,0,pin)+Math.sin(t*1.5)*2.5;
 set($('phone'),{transform:`translate(0px,${(1-pin)*900}px) rotateY(${tiltY}deg) rotateX(${(1-pin)*20}deg) scale(${1+.04*P(t,2.4,3.4)})`,display:t>1.85?'block':'none'});
 const sc=300*eIO(P(t,2.45,3.0));
 $('scroller').style.transform=`translateY(${-sc}px)`;
 set($('stripBox'),{top:(1924*S)+'px'});
 let tv=0,ty=0;if(t>=2.38&&t<=3.1){tv=Math.min(P(t,2.38,2.47),1-P(t,3.0,3.1));ty=lerp(560,250,eIO(P(t,2.45,3.0)))}
 set($('touch'),{opacity:tv*.95,transform:`translate(${230-28}px,${ty-28}px)`});
 const pl=eBack(P(t,2.7,3.0));
 set($('player'),{transform:`translateY(${(1-pl)*120}px)`,opacity:clamp(pl*2)});
 $('pbi').style.width=(20+P(t,2.7,3.4)*15)+'%';
 // cards
 const cr=eBack(P(t,2.05,2.4));
 set($('cardRead'),{left:'200px',top:'300px',opacity:clamp(P(t,2.05,2.2)),transform:`translateX(${(1-cr)*-260}px) rotate(${(1-cr)*-6}deg)`});
 document.querySelectorAll('#cardRead .draw').forEach((p,i)=>{p.style.strokeDashoffset=p.dataset.L*(1-eOut(P(t,2.1+i*.04,2.5+i*.04)))});
 const cl=eBack(P(t,2.55,2.9));
 set($('cardListen'),{left:'1300px',top:'300px',opacity:clamp(P(t,2.55,2.7)),transform:`translateX(${(1-cl)*260}px) rotate(${(1-cl)*6}deg)`});
 document.querySelectorAll('#cardListen .draw2').forEach((p,i)=>{p.style.strokeDashoffset=p.dataset.L*(1-eOut(P(t,2.6+i*.05,3.0+i*.05)))});
 wv.forEach((b,i)=>{const amp=P(t,2.65,2.9);b.style.height=(8+amp*(Math.abs(Math.sin(t*9+i*.7))*34+Math.abs(Math.sin(t*4.5+i*1.9))*22))+'px'});
 ['topicHead','topicSub','chips'].forEach(id=>$(id).style.display='none');
 // outro 3.0-7.0
 const ow=eIO(P(t,3.0,3.4));
 set($('outro'),{position:'absolute',inset:0,clipPath:`circle(${ow*1300}px at 50% 47%)`,display:t>2.98?'block':'none'});
 drawParticles($('oc'),t,'#E7C77A',1);
 const ol=eBack(P(t,3.15,3.5));
 set($('oLogo'),{opacity:clamp(P(t,3.15,3.3)),transform:`translateY(${(1-ol)*-80}px) scale(${lerp(.4,1,ol)}) rotate(${(1-ol)*-15}deg)`});
 const pk=eBack(P(t,3.2,3.5));
 set($('pill'),{opacity:clamp(P(t,3.2,3.32)),transform:`scaleX(${lerp(.15,1,pk)})`});
 const full='pustika.co.in',nch=Math.floor(clamp((t-3.3)/1.0)*full.length),s=full.slice(0,nch);
 const blink=(t>4.45)?(Math.floor(t*2.2)%2?0:1):1;
 $('url').innerHTML=s.slice(0,7)+(s.length>7?`<span class="tld">${s.slice(7)}</span>`:'')+`<span id="caret" style="opacity:${blink*clamp(P(t,3.25,3.35))}"></span>`;
 const ot=eOut(P(t,4.5,4.9));
 set($('oTag'),{opacity:ot,transform:`translateY(${(1-ot)*30}px)`});
 const ot2=eOut(P(t,4.8,5.15));
 set($('oTag2'),{opacity:ot2,letterSpacing:lerp(24,8,ot2)+'px'});
 ocEls.forEach((el,i)=>{const k=eBack(P(t,4.95+i*.07,5.45+i*.07)),x=960+(i-2.5)*150-60,y=lerp(1150,810,k)+Math.sin(t*1.5+i)*6;
  set(el,{left:0,top:0,transform:`translate(${x}px,${y}px) rotate(${(i-2.5)*3}deg)`,opacity:clamp(k*2)})});
 if(t>4.45)$('pill').style.transform=`scale(${1+Math.sin((t-4.45)*3)*.012})`;
 // subtitles
 let st='',so=0;
 for(const [a,b,x] of SUBS){if(t>=a-.05&&t<=b+.05){st=x;so=Math.min(P(t,a-.05,a+.05),1-P(t,b-.02,b+.05))}}
 $('sub').textContent=st;set($('sub'),{opacity:so,display:st?'block':'none',transform:'translateX(-50%)'});
}
window.render=render;
