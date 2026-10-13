#!/usr/bin/env python3
"""Generate the working prototype index.html from extracted listings.json."""
import json, re, os

SRC = os.path.expanduser('~/workspace/real-estate-round-up-extraction/listings.json')
OUT_DIR = os.path.expanduser('~/workspace/real-estate-round-up-site')

data = json.load(open(SRC))
recs = data['listings']

def clean(s):
    if not s: return s
    s = s.replace('\u2011', '-').replace('\u00ad', '')
    s = re.sub(r'\s+', ' ', s).strip()
    return s

pub = []
for r in recs:
    desc = clean(r.get('description') or '')
    # tidy tail: remove the printed "MLS# nnn. $x." at the very end (shown as fields instead)
    desc = re.sub(r'\s*MLS#?\s*\d{5,}\.?\s*\$[\d,]+\.?\s*$', '', desc).strip()
    desc = re.sub(r'\s*#\d{5,}\.?\s*\$[\d,]+\.?\s*$', '', desc).strip()
    agent = r.get('agent') or {}
    pub.append({
        'page': r.get('page'),
        'address': clean(r.get('address')),
        'town': clean(r.get('town')),
        'description': desc,
        'price': r.get('price'),
        'alt_prices': r.get('alt_prices'),
        'mls': r.get('mls'),
        'beds': r.get('beds'),
        'baths': r.get('baths'),
        'sqft': r.get('sqft'),
        'acres': r.get('acres'),
        'status': clean(r.get('status')),
        'agent': {'name': clean(agent.get('name')), 'phone': clean(agent.get('phone')), 'email': clean(agent.get('email'))},
        'brokerage': clean(r.get('brokerage')),
        'confidence': r.get('confidence'),
    })

# sort: status-priority then price desc default handled client-side; keep magazine order (page)
pub.sort(key=lambda x: (x['page'] or 99))
listings_js = json.dumps(pub, ensure_ascii=False, separators=(',', ':'))

html = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Real Estate Roundup — Lincoln County & Otero County, New Mexico</title>
<meta name="description" content="The Real Estate Roundup: homes, land and mountain property for sale in Ruidoso, Alto, Capitan, Alamogordo, Cloudcroft and across Lincoln and Otero County, New Mexico. 26 years in print.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700;800;900&family=Archivo+Expanded:wght@700;900&display=swap" rel="stylesheet">
<style>
:root{--pine:#123528;--forest:#1E5A41;--brass:#D9A441;--sand:#E8DDD0;--rust:#B4552D;--ink:#1c2420;--paper:#faf7f2}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Archivo',system-ui,sans-serif;background:var(--paper);color:var(--ink)}
a{color:inherit}
.wrap{max-width:1240px;margin:0 auto;padding:0 20px}
header.top{position:sticky;top:0;z-index:50;background:var(--pine);color:#fff;box-shadow:0 2px 14px rgba(0,0,0,.25)}
.top-in{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:12px 0}
.wordmark{font-weight:900;letter-spacing:.04em;font-size:20px;line-height:1.05}
.wordmark small{display:block;font-size:10px;letter-spacing:.32em;color:var(--brass);font-weight:700}
nav.main{display:flex;gap:22px;font-size:13px;font-weight:700;letter-spacing:.12em;text-transform:uppercase}
nav.main a{text-decoration:none;opacity:.92} nav.main a:hover{color:var(--brass)}
.hero{position:relative;background:var(--pine);color:#fff;overflow:hidden}
.hero img.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.45}
.hero .shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(18,53,40,.35),rgba(18,53,40,.88))}
.hero-in{position:relative;padding:84px 0 70px;max-width:760px}
.kicker{color:var(--brass);font-weight:800;letter-spacing:.3em;font-size:12px;text-transform:uppercase}
.hero h1{font-size:52px;font-weight:900;line-height:1.02;margin:14px 0 16px}
.hero p{font-size:18px;line-height:1.55;opacity:.95;max-width:620px}
.hero .stats{display:flex;gap:34px;margin-top:30px;flex-wrap:wrap}
.hero .stats b{display:block;font-size:30px;color:var(--brass);font-weight:900}
.hero .stats span{font-size:12px;letter-spacing:.18em;text-transform:uppercase;opacity:.85}
section{padding:56px 0}
h2.sec{font-size:32px;font-weight:900;color:var(--pine);margin-bottom:6px}
p.sec-sub{color:#5a665f;margin-bottom:26px;max-width:700px;line-height:1.5}
.editions{display:grid;grid-template-columns:1fr 1fr;gap:20px}
@media(max-width:760px){.editions{grid-template-columns:1fr}.hero h1{font-size:38px}nav.main{display:none}}
.ed{border-radius:16px;padding:28px;color:#fff;position:relative;overflow:hidden}
.ed.lincoln{background:linear-gradient(135deg,var(--pine),var(--forest))}
.ed.otero{background:linear-gradient(135deg,#7a3418,var(--rust))}
.ed .tag{font-size:11px;letter-spacing:.28em;font-weight:800;text-transform:uppercase;opacity:.85}
.ed h3{font-size:26px;font-weight:900;margin:8px 0 8px}
.ed p{line-height:1.5;opacity:.94;font-size:15px}
.ed a.btn{display:inline-block;margin-top:16px;background:var(--brass);color:var(--pine);font-weight:800;padding:11px 18px;border-radius:999px;text-decoration:none;font-size:14px}
.ed a.btn.ghost{background:transparent;border:2px solid rgba(255,255,255,.75);color:#fff}
.controls{position:sticky;top:64px;z-index:40;background:var(--paper);padding:14px 0 10px;border-bottom:1px solid #e3dccc}
.controls .row{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.controls input[type=search]{flex:1;min-width:210px;padding:12px 14px;border:1.5px solid #cfc4ae;border-radius:10px;font:inherit;font-size:15px;background:#fff}
.controls select{padding:12px;border:1.5px solid #cfc4ae;border-radius:10px;font:inherit;background:#fff}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
.chip{border:1.5px solid var(--forest);color:var(--forest);background:#fff;border-radius:999px;padding:6px 13px;font-size:13px;font-weight:700;cursor:pointer}
.chip.on{background:var(--forest);color:#fff}
.count-line{margin:16px 0 4px;color:#5a665f;font-size:14px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:18px;margin-top:14px}
.card{background:#fff;border:1px solid #e6ddcb;border-radius:14px;overflow:hidden;cursor:pointer;display:flex;flex-direction:column;transition:transform .12s,box-shadow .12s}
.card:hover{transform:translateY(-3px);box-shadow:0 12px 28px rgba(18,53,40,.16)}
.card .band{background:linear-gradient(120deg,var(--pine),var(--forest));color:#fff;padding:16px 18px;position:relative}
.card .band .price{font-size:25px;font-weight:900}
.card .band .town{font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:var(--brass);font-weight:800;margin-top:2px}
.badge{position:absolute;top:12px;right:12px;background:var(--rust);color:#fff;font-size:10px;font-weight:800;letter-spacing:.08em;padding:4px 9px;border-radius:999px;text-transform:uppercase}
.badge.gold{background:var(--brass);color:var(--pine)}
.card .body{padding:15px 18px 17px;display:flex;flex-direction:column;gap:8px;flex:1}
.card .addr{font-weight:800;font-size:16px;color:var(--pine)}
.card .specs{font-size:13px;color:#43534a;font-weight:600}
.card .desc{font-size:13.5px;line-height:1.5;color:#4c584f;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.card .mls{margin-top:auto;font-size:11.5px;color:#8a938b;letter-spacing:.06em}
.more{display:block;margin:28px auto 0;background:var(--pine);color:#fff;border:0;font:inherit;font-weight:800;padding:13px 30px;border-radius:999px;cursor:pointer}
.note{font-size:12.5px;color:#7a857c;margin-top:14px;line-height:1.5}
.advert{background:var(--pine);color:#fff;border-radius:18px;padding:34px}
.advert h3{font-size:26px;font-weight:900;margin-bottom:8px}
.advert p{line-height:1.55;opacity:.93;max-width:640px}
.advert button{margin-top:16px;background:var(--brass);color:var(--pine);border:0;font:inherit;font-weight:800;padding:12px 20px;border-radius:999px;cursor:pointer}
.advert .phone{margin-top:14px;font-size:22px;font-weight:900;color:var(--brass);display:none}
footer{background:#0d271e;color:#cfe0d4;padding:36px 0;margin-top:20px}
footer .fm{font-weight:900;color:#fff;font-size:18px}
footer p{font-size:13px;line-height:1.6;opacity:.85;margin-top:8px;max-width:640px}
.modal-bg{position:fixed;inset:0;background:rgba(10,25,18,.66);display:none;z-index:100;align-items:flex-start;justify-content:center;overflow:auto;padding:26px 14px}
.modal{background:#fff;border-radius:16px;max-width:680px;width:100%;padding:30px;position:relative}
.modal .x{position:absolute;top:14px;right:16px;font-size:26px;background:none;border:0;cursor:pointer;color:#667}
.modal .mprice{font-size:32px;font-weight:900;color:var(--pine)}
.modal .maddr{font-weight:800;font-size:19px;margin-top:2px}
.modal .mspecs{color:#43534a;font-weight:700;margin:10px 0;font-size:14px}
.modal .mdesc{line-height:1.65;font-size:15px;color:#333d36;white-space:pre-wrap}
.modal .agentbox{background:var(--sand);border-radius:12px;padding:16px 18px;margin-top:18px}
.modal .agentbox b{color:var(--pine)}
.modal .agentbox a{font-weight:800;color:var(--forest)}
.modal .fine{font-size:12px;color:#7a857c;margin-top:14px;line-height:1.5}
</style>
</head>
<body>
<header class="top"><div class="wrap top-in">
  <div class="wordmark">THE REAL ESTATE ROUNDUP<small>LINCOLN &amp; OTERO COUNTY · NEW MEXICO</small></div>
  <nav class="main"><a href="#editions">Editions</a><a href="#listings">Listings</a><a href="#advertise">Advertise</a></nav>
</div></header>

<div class="hero"><img class="bg" src="hero.jpg" alt="Sierra Blanca over Ruidoso, New Mexico"><div class="shade"></div>
  <div class="wrap hero-in">
    <div class="kicker">26 years in print · Est. Ruidoso, New Mexico</div>
    <h1>Mountain property, from the people who print it.</h1>
    <p>Every listing in the October 2026 Lincoln County Edition of The Real Estate Roundup — searchable, sortable, and straight from the magazine’s own pages.</p>
    <div class="stats">
      <div><b id="stat-count">—</b><span>Listings this issue</span></div>
      <div><b id="stat-median">—</b><span>Median price</span></div>
      <div><b>15+</b><span>Communities covered</span></div>
    </div>
  </div>
</div>

<section id="editions"><div class="wrap">
  <h2 class="sec">This month’s editions</h2>
  <p class="sec-sub">Two magazines, one mountain region. The Lincoln County Edition listings are live below; the Otero County Edition joins them as soon as its print files arrive.</p>
  <div class="editions">
    <div class="ed lincoln"><div class="tag">October 2026 · Vol 26 No 10</div><h3>The Real Estate Roundup — Lincoln County Edition</h3>
      <p>Ruidoso, Alto, Capitan, Carrizozo, Lincoln, Nogal and the Hondo Valley — 358 listings extracted from the October issue.</p>
      <a class="btn" href="#listings">Browse the listings</a>
      <a class="btn ghost" href="https://issuu.com/therealestateroundup" target="_blank" rel="noopener">Read the digital edition</a></div>
    <div class="ed otero"><div class="tag">October 2026 · Vol 21 No 10</div><h3>The Real Estate Roundup — Otero County Edition</h3>
      <p>Alamogordo, Cloudcroft, Tularosa, La Luz, High Rolls and Timberon. Searchable listings are on the way — the full issue is available digitally now.</p>
      <a class="btn" href="https://issuu.com/therealestateroundup" target="_blank" rel="noopener">Read the digital edition</a></div>
  </div>
</div></section>

<section id="listings" style="padding-top:6px"><div class="wrap">
  <h2 class="sec">October 2026 listings — Lincoln County</h2>
  <p class="sec-sub">As printed in the October 2026 issue. Listings change hands fast in the mountains — always confirm availability with the listing agent.</p>
  <div class="controls">
    <div class="row">
      <input type="search" id="q" placeholder="Search address, town, keyword, or MLS #…">
      <select id="status"><option value="">Any status</option></select>
      <select id="sort"><option value="page">Magazine order</option><option value="plo">Price: low to high</option><option value="phi">Price: high to low</option><option value="beds">Most bedrooms</option></select>
    </div>
    <div class="chips" id="chips"></div>
  </div>
  <div class="count-line" id="count"></div>
  <div class="grid" id="grid"></div>
  <button class="more" id="more">Show more listings</button>
  <p class="note">Property details are reproduced from the October 2026 print edition of The Real Estate Roundup. Photos for these listings will appear as they are processed from the print files. To ask about a property, contact its listing agent or brokerage directly — contact details are on each listing.</p>
</div></section>

<section id="advertise"><div class="wrap">
  <div class="advert">
    <h3>Advertise in The Real Estate Roundup</h3>
    <p>Reach buyers across Lincoln and Otero County in print every month — and now online. Brokers, agents and local businesses: talk to us about rates and deadlines for the next issue.</p>
    <button id="reveal">Advertise in The Real Estate Roundup — show phone number</button>
    <div class="phone" id="phone"></div>
  </div>
</div></section>

<footer><div class="wrap">
  <div class="fm">The Real Estate Roundup</div>
  <p>Published monthly in Ruidoso, New Mexico — Lincoln County Edition and Otero County Edition. 26 years serving the Sacramento Mountains real estate community. Listings belong to their respective brokerages; contact the listing agent for current availability and details.</p>
</div></footer>

<div class="modal-bg" id="mbg"><div class="modal" role="dialog" aria-modal="true">
  <button class="x" id="mx" aria-label="Close">×</button>
  <div id="mcontent"></div>
</div></div>

<script>
const LISTINGS = __LISTINGS__;
const $=s=>document.querySelector(s);
const money=n=>n==null?'Price in magazine':('$'+n.toLocaleString('en-US'));
let townFilter='', shown=48;
// stats
$('#stat-count').textContent = LISTINGS.length;
const prices = LISTINGS.map(l=>l.price).filter(Boolean).sort((a,b)=>a-b);
$('#stat-median').textContent = money(prices[Math.floor(prices.length/2)]);
// town chips
const townCounts={}; LISTINGS.forEach(l=>{ if(l.town) townCounts[l.town]=(townCounts[l.town]||0)+1; });
const topTowns=Object.entries(townCounts).sort((a,b)=>b[1]-a[1]).slice(0,8);
const chipsEl=$('#chips');
function chip(label,val){const b=document.createElement('button');b.className='chip'+(townFilter===val?' on':'');b.textContent=label;b.onclick=()=>{townFilter=val;shown=48;render();};chipsEl.appendChild(b);}
function drawChips(){chipsEl.innerHTML='';chip('All areas','');topTowns.forEach(([t,c])=>chip(t+' ('+c+')',t));}
// status options
const statuses=[...new Set(LISTINGS.map(l=>l.status).filter(Boolean))];
statuses.forEach(s=>{const o=document.createElement('option');o.value=s;o.textContent=s.charAt(0)+s.slice(1).toLowerCase();$('#status').appendChild(o);});
function specs(l){const p=[];if(l.beds)p.push(l.beds+' bd');if(l.baths)p.push(l.baths+' ba');if(l.sqft)p.push(l.sqft.toLocaleString()+' sq ft');if(l.acres)p.push(l.acres+' acres');return p.join(' · ');}
function filtered(){
  const q=$('#q').value.trim().toLowerCase(), st=$('#status').value, so=$('#sort').value;
  let out=LISTINGS.filter(l=>{
    if(townFilter && l.town!==townFilter) return false;
    if(st && l.status!==st) return false;
    if(q){const hay=((l.address||'')+' '+(l.town||'')+' '+(l.description||'')+' '+(l.mls||'')+' '+(l.brokerage||'')).toLowerCase(); if(!hay.includes(q)) return false;}
    return true;});
  if(so==='plo') out.sort((a,b)=>(a.price||1e12)-(b.price||1e12));
  if(so==='phi') out.sort((a,b)=>(b.price||0)-(a.price||0));
  if(so==='beds') out.sort((a,b)=>(b.beds||0)-(a.beds||0));
  return out;
}
function badgeClass(s){return /sold/i.test(s)?'badge':'badge gold';}
function render(){
  drawChips();
  const out=filtered();
  $('#count').textContent = out.length+' listing'+(out.length===1?'':'s')+(townFilter?(' in '+townFilter):'');
  const g=$('#grid'); g.innerHTML='';
  out.slice(0,shown).forEach(l=>{
    const i=LISTINGS.indexOf(l);
    const c=document.createElement('div'); c.className='card'; c.onclick=()=>openModal(i);
    c.innerHTML=`<div class="band"><div class="price">${money(l.price)}</div><div class="town">${l.town||'Lincoln County'}</div>${l.status?`<span class="${badgeClass(l.status)}">${l.status}</span>`:''}</div>
    <div class="body">${l.address?`<div class="addr">${l.address}</div>`:''}${specs(l)?`<div class="specs">${specs(l)}</div>`:''}<div class="desc">${l.description||''}</div><div class="mls">${l.mls?('MLS #'+l.mls+' · '):''}Page ${l.page||'—'} · October 2026</div></div>`;
    g.appendChild(c);});
  $('#more').style.display = out.length>shown ? 'block':'none';
}
function openModal(i){
  const l=LISTINGS[i]; const a=l.agent||{};
  const contact=[a.name?`<div><b>Listing agent:</b> ${a.name}</div>`:'', a.phone?`<div><b>Phone:</b> <a href="tel:${a.phone.replace(/[^0-9+]/g,'')}">${a.phone}</a></div>`:'', a.email?`<div><b>Email:</b> <a href="mailto:${a.email}">${a.email}</a></div>`:'', l.brokerage?`<div><b>Brokerage:</b> ${l.brokerage}</div>`:''].join('');
  $('#mcontent').innerHTML=`<div class="mprice">${money(l.price)}</div>
  ${l.address?`<div class="maddr">${l.address}${l.town?(' · '+l.town+', NM'):''}</div>`:(l.town?`<div class="maddr">${l.town}, New Mexico</div>`:'')}
  ${specs(l)?`<div class="mspecs">${specs(l)}</div>`:''}
  <div class="mdesc">${l.description||''}</div>
  ${contact?`<div class="agentbox">${contact}</div>`:`<div class="agentbox">For this listing, contact the brokerage named in the October 2026 print edition${l.mls?(' — reference MLS #'+l.mls):''}.</div>`}
  <div class="fine">${l.mls?('MLS #'+l.mls+' · '):''}As printed on page ${l.page||'—'} of the October 2026 Lincoln County Edition of The Real Estate Roundup. Details and availability can change — confirm with the listing agent.</div>`;
  $('#mbg').style.display='flex';
}
$('#mx').onclick=()=>$('#mbg').style.display='none';
$('#mbg').onclick=e=>{if(e.target.id==='mbg')$('#mbg').style.display='none';};
document.addEventListener('keydown',e=>{if(e.key==='Escape')$('#mbg').style.display='none';});
$('#more').onclick=()=>{shown+=48;render();};
['q','status','sort'].forEach(id=>$('#'+id).addEventListener('input',()=>{shown=48;render();}));
$('#reveal').onclick=()=>{const p=$('#phone');p.textContent=['575','937','1345'].join('-');p.style.display='block';$('#reveal').style.display='none';};
render();
</script>
</body>
</html>
"""

html = html.replace('__LISTINGS__', listings_js)
os.makedirs(OUT_DIR, exist_ok=True)
with open(os.path.join(OUT_DIR, 'index.html'), 'w') as f:
    f.write(html)
print(f"index.html written: {len(html)/1024:.0f} KB, {len(pub)} listings")
towns = {}
for p in pub:
    if p['town']: towns[p['town']] = towns.get(p['town'], 0) + 1
print("towns:", sorted(towns.items(), key=lambda x: -x[1])[:8])
