
const DATA = [
  {w:`grycoin`,      c:`Currency`, p:88,  n:52, q:`II. Second Layer: Grycoin - A Peer-to-Peer Electronic Message System`},
  {w:`Satoshi`,      c:`Names`,    p:184, n:47, q:`There is an interesting coincidence."Satoshi" is an almost perfect anagram of "THOMAS".`},
  {w:`burn`,         c:`Currency`, p:50,  n:23, q:`And they burned fossil fuel to destroy their civilization as well?`},
  {w:`ALS`,          c:`The body`, p:250, n:17, q:`a) ALS Condition`},
  {w:`satommi`,      c:`Currency`, p:104, n:14, q:`And while I am at it, I name the basic unit satommi. One hundred million satommis for one grycoin.`},
  {w:`signs`,        c:`The trail`,p:20,  n:14, q:`I recognize the signs.`},
  {w:`carbon budget`,c:`Currency`, p:65,  n:10, q:`I can make it clear that humanity is NOT allowed to overshoot the carbon budget.`},
  {w:`Thomas`,       c:`Names`,    p:6,   n:10, q:`For those who don't know me, I am Thomas, though more people know me under the name I created from that.`},
  {w:`reverse Turing test`, c:`The machine`, p:71, n:6, q:`3. Reverse Turing Test`},
  {w:`Aoi`,          c:`Names`,    p:19,  n:5,  q:`How about Aoi?`},
  {w:`RPOW`,         c:`The trail`,p:217, n:4,  q:`I had made an attempt to make my own proof-of-work based currency, called RPOW.`},
  {w:`simulation`,   c:`The machine`, p:10, n:3, q:`I wonder if I live in the real world right now or if this is a simulation.`},
  {w:`singularity`,  c:`The machine`, p:10, n:3, q:`Obviously, the singularity has happened, or I would not be back.`},
  {w:`Artificial Omnipotent Intelligence`, c:`The machine`, p:22, n:3, q:`Artificial Omnipotent Intelligence, obviously.`},
  {w:`Bitcointalk`,  c:`The trail`,p:204, n:2,  q:`And who was it again quoting Lois Lane from Superman with exactly that question on bitcointalk?`},
  {w:`brain wallet`, c:`The body`, p:5,   n:1,  q:`First thing I check is my brain wallet. Oh yes. There they are. All the words I need to use my keys.`},
  {w:`half marathon`,c:`The body`, p:30,  n:1,  q:`Want to try a half marathon, Tom?`}
];

const CATS = [`All`].concat([...new Set(DATA.map(d => d.c))]);
const wall  = document.getElementById(`wall`);
const chips = document.getElementById(`chips`);
const pterm = document.getElementById(`pterm`);
const pmeta = document.getElementById(`pmeta`);
const pquote= document.getElementById(`pquote`);

let cat = `All`, query = ``, sel = 0;

function tier(n){ return n >= 20 ? 1 : n >= 8 ? 2 : 3; }
function tilt(i){ return ((i * 37) % 5 - 2) * 0.7; }

function buildChips(){
  chips.textContent = ``;
  CATS.forEach(name => {
    const b = document.createElement(`button`);
    b.className = `chip`;
    b.type = `button`;
    b.textContent = name;
    b.setAttribute(`aria-pressed`, String(name === cat));
    b.addEventListener(`click`, () => { cat = name; buildChips(); render(); });
    chips.appendChild(b);
  });
  const tally = document.createElement(`span`);
  tally.className = `count`;
  const shown = visible().length;
  tally.textContent = shown + (shown === 1 ? ` word` : ` words`);
  chips.appendChild(tally);
}

function visible(){
  return DATA.filter(d => cat === `All` || d.c === cat);
}

function show(idx){
  const d = DATA[idx];
  if(!d) return;
  sel = idx;
  pterm.textContent = d.w;
  pmeta.innerHTML = `<b>${d.c}</b> · ${d.n} ${d.n === 1 ? `appearance` : `appearances`} · paragraph ${d.p}`;
  pquote.innerHTML = ``;
  pquote.appendChild(document.createTextNode(`“` + d.q + `”`));
  const src = document.createElement(`span`);
  src.className = `src`;
  src.textContent = `Second, ¶${d.p}`;
  pquote.appendChild(src);
}

function render(){
  wall.textContent = ``;
  const list = visible();
  const keep = list.findIndex(d => DATA.indexOf(d) === sel);
  list.forEach((d, i) => {
    const idx = DATA.indexOf(d);
    const b = document.createElement(`button`);
    b.type = `button`;
    b.className = `tile t` + tier(d.n);
    b.style.setProperty(`--tilt`, tilt(i) + `deg`);
    b.setAttribute(`role`, `listitem`);
    b.setAttribute(`aria-pressed`, String(idx === sel));
    const w = document.createElement(`span`);
    w.className = `w`;
    w.textContent = d.w;
    const ref = document.createElement(`span`);
    ref.className = `ref`;
    ref.textContent = `¶${d.p} · ${d.n}`;
    b.appendChild(w);
    b.appendChild(ref);
    b.addEventListener(`click`, () => { show(idx); render(); });
    wall.appendChild(b);
  });
  if(!list.length){
    const p = document.createElement(`p`);
    p.className = `empty`;
    p.textContent = `Nothing here yet.`;
    wall.appendChild(p);
  }
  if(keep === -1 && list.length) show(DATA.indexOf(list[0]));
  if(list.length && keep !== -1) show(DATA.indexOf(list[keep]));
}

buildChips();
render();
