
const LENS=[6,14,16,96,100,104,85,76,156,301,20,24,39,74,7,90,160,31,86,22,70,48,28,204,270,66,31,52,193,35,74,53,15,7,111,23,134,20,42,23,74,69,167,41,65,115,207,25,137,113,14,19,247,10,137,74,32,42,31,171,90,66,204,42,229,17,391,108,15,230,22,157,260,23,310,25,102,7,437,63,149,55,144,38,210,130,138,68,8,589,21,59,44,142,336,204,116,90,310,230,35,159,148,158,144,371,638,355,350,198,134,142,313,341,27,82,237,211,26,261,240,205,292,466,472,649,536,289,57,13,230,351,159,294,488,397,351,286,47,162,87,348,405,302,259,448,43,369,118,151,361,18,201,439,306,354,34,438,466,267,13,450,20,14,80,147,200,234,259,234,488,48,280,299,19,21,408,63,22,63,218,21,254,210,63,246,145,32,211,154,220,589,177,68,184,129,18,33,70,204,71,119,137,277,121,462,76,196,31,227,61,219,267,124,43,265,361,164,173,214,16,275,120,191,52,160,56,149,61,199,398,231,209,370,395,168,4,219,7,134,184,76,32,24,98,207,17,337,80,16,200,22,255,33,546,36,206,15,235,23,224,114,351,93,21,82,107,186,473,180,304,35,61];
const NUM=[["1",3],["2020",15],["1000",37],["55.5",49],["2",54],["25",57],["3",71],["350",73],["1",91],["2",95],["2",95],["2",106],["7",106],["7",107],["7",107],["2",107],["2",107],["7",112],["2",115],["6.25",118],["1",125],["3",125],["7",125],["6.25",125],["2017",125],["6.25",126],["3",126],["7",126],["6.25",126],["3",130],["5",137],["2",138],["2",143],["2",144],["2",151],["4",152],["5",157],["2",160],["6",161],["1",164],["2",175],["5",177],["5",177],["1933",177],["1975",177],["1975",178],["30",183],["2014",183],["2001",195],["2008",201],["2001",213],["2008",232],["50",232],["70",235],["3",247],["10",255],["2009",255],["2008",257],["10",262],["4",265]];
const CATS=[
 {id:"anchor",label:"Signature sites",c:"--c1",idx:[4,5,6,7,8,92,93,94,95,96,167,168,169,170,171]},
 {id:"finney",label:"Finney reprint",c:"--c2",idx:[231,232,233,234,235]},
 {id:"case",label:"Case-change targets",c:"--c3",idx:[73,106,107,112,126,128,136,209]},
 {id:"addr",label:"Address strings",c:"--c4",idx:[106,107,112,126]},
 {id:"head",label:"Headings",c:"--c5",idx:[2,3,54,71,88,91,115,130,152,157,161,163,164,175,176,182,209,215,247,250,252,254,256,258,260,265]},
 {id:"him",label:"\u201chimself\u201d",c:"--c6",idx:[126,205,215,218,219,248]},
 {id:"signs",label:"\u201csigns\u201d",c:"--c7",idx:[20,42,220,222,223,225,226,227,228,230,236,244,246,273]},
 {id:"num",label:"Contains numerals",c:"--c8",idx:[...new Set(NUM.map(x=>x[1]))]}
];
const css=v=>getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const W=1000,H=430,ML=52,MR=16,MT=14,MB=34;
const IW=W-ML-MR, IH=H-MT-MB;
const maxY=Math.max(...LENS);
const x=i=>ML+(i/(LENS.length-1))*IW;
const y=v=>MT+IH-(v/maxY)*IH;
const svg=document.getElementById("plot");
const NS="http://www.w3.org/2000/svg";
function el(n,a){const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);return e;}
function build(){
 const on=new Set(CATS.filter(c=>c.on!==false).map(c=>c.id));
 svg.textContent="";
 for(let g=0;g<=4;g++){const v=maxY*g/4;
  svg.appendChild(el("line",{x1:ML,x2:W-MR,y1:y(v),y2:y(v),stroke:css("--line"),"stroke-width":1}));
  const t=el("text",{x:ML-8,y:y(v)+4,fill:css("--mut"),"font-size":11,"text-anchor":"end"});
  t.textContent=Math.round(v);svg.appendChild(t);}
 [1,50,100,150,200,273].forEach(n=>{
  const t=el("text",{x:x(n-1),y:H-MB+18,fill:css("--mut"),"font-size":11,"text-anchor":"middle"});
  t.textContent=n;svg.appendChild(t);});
 const xl=el("text",{x:ML+IW/2,y:H-4,fill:css("--mut"),"font-size":11.5,"text-anchor":"middle"});
 xl.textContent="paragraph ordinal";svg.appendChild(xl);
 const yl=el("text",{x:14,y:MT+IH/2,fill:css("--mut"),"font-size":11.5,"text-anchor":"middle",transform:"rotate(-90 14 "+(MT+IH/2)+")"});
 yl.textContent="characters";svg.appendChild(yl);
 LENS.forEach((v,i)=>{svg.appendChild(el("circle",{cx:x(i),cy:y(v),r:2.4,fill:css("--mut"),opacity:.5}));});
 CATS.forEach(c=>{if(!on.has(c.id))return;const col=css(c.c);
  c.idx.forEach(p=>{const i=p-1,v=LENS[i];
   const ci=el("circle",{cx:x(i),cy:y(v),r:4.6,fill:col,"fill-opacity":.85,stroke:css("--panel"),"stroke-width":1.2});
   ci.setAttribute("data-p",p);ci.setAttribute("data-c",c.label);ci.setAttribute("data-l",v);
   ci.style.cursor="pointer";svg.appendChild(ci);});});
}
const ro=document.getElementById("readout");
svg.addEventListener("pointerover",e=>{const t=e.target;if(t.tagName!=="circle"||!t.dataset.p)return;
 ro.innerHTML="¶<b>"+t.dataset.p+"</b> — "+t.dataset.l+" characters — <b>"+t.dataset.c+"</b>";});
const legend=document.getElementById("legend");
CATS.forEach(c=>{const b=document.createElement("button");b.className="chip";b.setAttribute("aria-pressed","true");
 const s=document.createElement("span");s.className="sw";s.style.background=css(c.c);
 b.appendChild(s);b.appendChild(document.createTextNode(c.label));
 b.onclick=()=>{c.on=c.on===false;b.setAttribute("aria-pressed",String(c.on));build();};
 legend.appendChild(b);});
const nums=document.getElementById("nums");
NUM.forEach(([v,p])=>{const d=document.createElement("span");d.className="n";
 d.innerHTML=v+' <span class="p">¶'+p+"</span>";
 d.onclick=()=>{ro.innerHTML="<b>"+v+"</b> appears in ¶"+p+" ("+LENS[p-1]+" characters)";};
 nums.appendChild(d);});
build();
