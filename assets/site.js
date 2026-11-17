/* Nelamedha — language switch and the satellite viewer */
(function(){
  var KEY='nelamedha-lang',root=document.documentElement;
  function stored(){try{return localStorage.getItem(KEY)}catch(e){return null}}
  function setLang(l,save){
    root.classList.toggle('lang-te',l==='te');root.lang=l==='te'?'te':'en';
    if(save){try{localStorage.setItem(KEY,l)}catch(e){}}
    var t=document.querySelector('title');if(t&&t.dataset[l])t.textContent=t.dataset[l];
    document.querySelectorAll('[data-alt-en]').forEach(function(el){el.setAttribute('alt',el.dataset[l==='te'?'altTe':'altEn'])});
    document.querySelectorAll('.lang').forEach(function(b){b.setAttribute('aria-label',l==='te'?'Read in English':'తెలుగులో చదవండి')});
    document.dispatchEvent(new CustomEvent('langchange',{detail:l}));
  }
  var q=new URLSearchParams(location.search).get('lang');
  var first=q==='te'||q==='en'?q:(stored()||'en');
  setLang(first,q==='te'||q==='en');
  document.addEventListener('click',function(e){var b=e.target.closest('.lang');if(!b)return;setLang(root.classList.contains('lang-te')?'en':'te',true)});
  window.nmLang=function(){return root.classList.contains('lang-te')?'te':'en'};
})();

/* the farm from above: pick a year, or compare two with a sliding line */
function nmSat(id){
  var box=document.getElementById(id);if(!box)return;
  var D=JSON.parse(box.querySelector('script[type="application/json"]').textContent);
  var P=D.pics,st={i:P.length-1,j:3,cmp:false,split:.5,drag:false,tmr:null};
  var q=function(s){return box.querySelector(s)};
  var A=q('.sat-a'),B=q('.sat-b'),F=q('.sat-fade'),svg=q('svg'),split=q('.sat-split');
  var L=function(){return nmLang()};
  var MON={en:['January','February','March','April','May','June','July','August','September','October','November','December'],
           te:['జనవరి','ఫిబ్రవరి','మార్చి','ఏప్రిల్','మే','జూన్','జూలై','ఆగస్టు','సెప్టెంబరు','అక్టోబరు','నవంబరు','డిసెంబరు']};
  function date(s,short){var a=s.split('-').map(Number),m=MON[L()][a[1]-1];if(short)return (L()==='en'?m.slice(0,3):m)+' '+a[0];return a[2]+' '+m+' '+a[0]}
  function overlay(){
    var w=box.querySelector('.sat-view').clientWidth||640,u=D.w/w,pts=D.farm.map(function(p){return p.join(',')}).join(' ');
    if(!q('#'+id+'-marks').checked){svg.innerHTML='';return}
    var s='<polygon points="'+pts+'" style="fill:none;stroke:var(--ov-halo);stroke-width:'+(4.5*u)+'px"/><polygon points="'+pts+'" style="fill:none;stroke:var(--ov-line);stroke-width:'+(2*u)+'px"/>';
    D.marks.forEach(function(m){s+='<circle cx="'+m.x+'" cy="'+m.y+'" r="'+(3*u)+'" style="fill:var(--ov-text);stroke:#14160F;stroke-width:'+u+'px"/><text x="'+(m.x+5*u)+'" y="'+(m.y-5*u)+'" class="ovt" style="font-size:'+(12*u)+'px;stroke-width:'+(2.6*u)+'px">'+m[L()]+'</text>'});
    var bar=50/D.mpp;s+='<g transform="translate('+(10*u)+' '+(D.h-14*u)+')"><rect width="'+bar+'" height="'+(5*u)+'" style="fill:var(--ov-text);stroke:#14160F;stroke-width:'+u+'px"/><rect width="'+bar/2+'" height="'+(5*u)+'" style="fill:#14160F"/><text y="'+(-6*u)+'" class="ovt" style="font-size:'+(11*u)+'px;stroke-width:'+(2.6*u)+'px">50 m</text></g>';
    s+='<g transform="translate('+(D.w-18*u)+' '+(36*u)+')"><path d="M0 '+(-18*u)+' L'+(7*u)+' 0 L0 '+(-5*u)+' L'+(-7*u)+' 0Z" style="fill:var(--ov-text);stroke:#14160F;stroke-width:'+u+'px"/><text y="'+(13*u)+'" text-anchor="middle" class="ovt" style="font-size:'+(11*u)+'px;stroke-width:'+(2.6*u)+'px">N</text></g>';
    svg.innerHTML=s}
  function chips(){
    var mk=function(sel,row){return P.map(function(p,k){return '<button class="chip" type="button" data-row="'+row+'" data-k="'+k+'" aria-pressed="'+(k===sel)+'">'+date(p.d,1)+'</button>'}).join('')};
    q('.rowL .chips').innerHTML=mk(st.cmp?st.j:st.i,'L');q('.rowR .chips').innerHTML=mk(st.i,'R');
    q('.rowL .row-l').innerHTML=st.cmp?'<span class="en">Left</span><span class="te">ఎడమ</span>':'<span class="en">Year</span><span class="te">సంవత్సరం</span>';
    q('.rowR').hidden=!st.cmp}
  function note(){
    var one=function(p,who){return '<div>'+(who?'<p class="row-l">'+who+'</p>':'')+'<h3>'+date(p.d)+'</h3><p class="meta">'+p.meta[L()]+'</p><p>'+p.note[L()]+'</p></div>'};
    var n=q('.note');n.className='note'+(st.cmp?' two-n':'');
    n.innerHTML=st.cmp?one(P[st.j],L()==='te'?'ఎడమ':'Left')+one(P[st.i],L()==='te'?'కుడి':'Right'):one(P[st.i])}
  function apply(){B.style.clipPath='inset(0 0 0 '+(st.split*100).toFixed(2)+'%)';split.style.left=(st.split*100).toFixed(2)+'%'}
  function show(anim){
    var li=st.cmp?st.j:st.i,src=D.base+P[li].f;
    if(anim&&A.getAttribute('src')&&A.getAttribute('src')!==src&&!matchMedia('(prefers-reduced-motion:reduce)').matches){F.src=A.src;F.style.transition='none';F.style.opacity='1';void F.offsetWidth;F.style.transition='';F.style.opacity='0'}
    A.src=src;A.alt=(L()==='te'?'పైనుంచి పొలం, ':'The farm from above, ')+date(P[li].d);
    B.hidden=!st.cmp;split.hidden=!st.cmp;if(st.cmp){B.src=D.base+P[st.i].f;B.alt=(L()==='te'?'పైనుంచి పొలం, ':'The farm from above, ')+date(P[st.i].d)}
    q('.stamp').textContent=date(P[li].d,1);var r=q('.stamp.r');r.hidden=!st.cmp;r.textContent=date(P[st.i].d,1);
    apply();chips();note()}
  function stop(){if(st.tmr){clearInterval(st.tmr);st.tmr=null}var b=q('.play');b.setAttribute('aria-pressed','false');b.innerHTML='<span class="en">Play</span><span class="te">ఆడించు</span>'}
  box.addEventListener('click',function(e){var c=e.target.closest('[data-row]');if(!c)return;stop();var k=+c.dataset.k;if(c.dataset.row==='L'&&st.cmp)st.j=k;else st.i=k;show(true)});
  q('#'+id+'-cmp').addEventListener('change',function(e){stop();st.cmp=e.target.checked;if(st.cmp&&st.j===st.i)st.j=st.i>3?3:P.length-1;st.split=.5;show(false)});
  q('#'+id+'-marks').addEventListener('change',overlay);
  q('.play').addEventListener('click',function(e){if(st.tmr){stop();return}if(st.cmp){q('#'+id+'-cmp').checked=false;st.cmp=false}
    var b=q('.play');b.setAttribute('aria-pressed','true');b.innerHTML='<span class="en">Pause</span><span class="te">ఆపు</span>';if(st.i>=P.length-1)st.i=-1;
    var step=function(){st.i++;show(true);if(st.i>=P.length-1)stop()};step();st.tmr=setInterval(step,1900)});
  var v=q('.sat-view'),set=function(e){var r=v.getBoundingClientRect();st.split=Math.max(0,Math.min(1,(e.clientX-r.left)/r.width));apply()};
  v.addEventListener('pointerdown',function(e){if(!st.cmp)return;st.drag=true;try{v.setPointerCapture(e.pointerId)}catch(_){}set(e)});
  v.addEventListener('pointermove',function(e){if(st.drag)set(e)});
  ['pointerup','pointercancel'].forEach(function(t){v.addEventListener(t,function(){st.drag=false})});
  q('.sat-knob').addEventListener('keydown',function(e){var d=e.key==='ArrowLeft'?-.05:e.key==='ArrowRight'?.05:0;if(d){e.preventDefault();st.split=Math.max(0,Math.min(1,st.split+d));apply()}});
  document.addEventListener('langchange',function(){show(false);overlay()});
  if(window.ResizeObserver)new ResizeObserver(overlay).observe(v);
  show(false);overlay();
}
