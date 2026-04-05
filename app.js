const YRS=['2019','2020','2021','2022','2023','2024','NOW','Q3 2026','2027','2028'];

const Z=[
  {id:'kokapet',name:'Kokapet',rank:1,lat:17.407,lng:78.330,radius:2100,type:'luxury',hni:true,nri:true,
   seg:'Luxury · HNI · NRI',col:'#ff3a00',roiY:28,roi3:47,price:8500,ry:3.8,
   range:'₹1.2 Cr - ₹8 Cr',lst:342,nri:38,sv:180,
   vd:'The single best HNI and NRI investment in Hyderabad - no debate.',
   sm:'Kokapet sits directly adjacent to the Financial District - Goldman Sachs, Microsoft, Amazon and Google all maintain their largest India campuses here. This creates a permanently captive luxury rental and resale market. NRI buyers account for 38% of all purchases, the highest in the city, which is the strongest possible signal of future resale demand.',
   pros:['Goldman Sachs, Microsoft, Amazon within 2 km - corporate rental demand unmatched citywide','38% NRI buyer share - highest in Hyderabad - guarantees robust resale demand at all times','HMDA-approved zero-encumbrance titles - zero legal risk, zero litigation history'],
   cons:['₹1.2 Cr minimum entry - locks out sub-₹50 L budgets entirely','Appreciation moderating to 18-22% YoY from 2026 onward as the zone matures','Secondary lane infrastructure still incomplete - dust and access issues persist'],
   gi:[{t:'IT Corridor Extension',b:'1,200 acres notified adjacent to Financial District under HMDA Master Plan 2031 - 40,000 new IT jobs within 3 km'},{t:'ORR Phase-2 Exit Ramp',b:'Dedicated ORR ramp for Kokapet under construction - completion Q3 2026, cuts airport commute by 12 minutes'},{t:'HMWSSB Water Grid Phase-2',b:'Dedicated water pipeline for Kokapet-Narsingi - ₹440 Cr approved, addresses the only major infrastructure gap'}],
   tl:{p:[4200,4100,4800,5900,7100,7900,8500,9800,11200,12800],a:[20,18,42,65,80,88,95,97,98,99],n:[12,14,18,25,31,35,38,40,42,44]}},

  {id:'gachibowli',name:'Gachibowli',rank:2,lat:17.440,lng:78.349,radius:1950,type:'luxury',hni:true,nri:true,
   seg:'IT Premium · NRI · Rental Yield',col:'#ff8c00',roiY:22,roi3:36,price:9200,ry:4.2,
   range:'₹1.5 Cr - ₹12 Cr',lst:218,nri:31,sv:140,
   vd:'The safest, most liquid premium market - never had a down quarter since 2016.',
   sm:'Gachibowli is the established IT hub and the most liquid premium zone in Hyderabad. 4.2% net rental yield means your money works from purchase day. It has never recorded a down quarter in sales since 2016 - no other zone can claim that. For NRIs who want a guaranteed income-generating asset, this is the definitive choice.',
   pros:['4.2% net rental yield - highest in Hyderabad - immediate income from purchase day','Zero down quarters in sales since 2016 - most liquid, easiest exit of all premium zones','International schools, hospitals, malls within 3 km - strongest end-user demand base'],
   cons:['Highest entry at ₹9,200/sqft avg - ₹1.5 Cr floor is the most expensive entry point','Peak appreciation is behind - upside now 22% YoY vs 35% three years ago','HITEC City main corridor congestion is a permanent structural problem'],
   gi:[{t:'Metro Rail Phase-2 Station',b:'Gachibowli metro station funded under Phase-2 - construction begins Q2 2026, operational by 2029'},{t:'HITECH City Expansion 800 Acres',b:'800-acre IT park notified adjacent to Gachibowli - 50,000 additional jobs projected on completion'},{t:'Biodiversity Junction Flyover',b:'TS-iPass approved flyover at the most congested junction - completion Dec 2026'}],
   tl:{p:[5800,5600,6200,7100,7900,8600,9200,10100,11000,12000],a:[55,50,62,71,80,85,90,92,93,94],n:[20,22,25,27,29,30,31,32,33,34]}},

  {id:'miyapur',name:'Miyapur',rank:3,lat:17.498,lng:78.340,radius:2300,type:'mid',hni:false,nri:true,
   seg:'Mid-range · Metro-linked · Family',col:'#ffd700',roiY:19,roi3:31,price:5800,ry:3.2,
   range:'₹55 L - ₹2.5 Cr',lst:489,nri:18,sv:220,
   vd:'#1 in sales volume citywide - maximum liquidity, lowest resale risk.',
   sm:'Miyapur leads all Hyderabad localities in raw quarterly sales at 220 units - you can always exit when needed. Metro terminus connectivity gives a permanent commute advantage no competitor can replicate. NRIs from USA and UK specifically target Miyapur for under-₹1 Cr family apartments. Entry at ₹55 L reaches the widest buyer pool.',
   pros:['220 units/quarter - highest sales velocity citywide - easiest exit, minimum holding risk','Metro terminus gives permanent, unbeatable commute advantage over competing zones','Entry from ₹55 L - widest NRI buyer pool, largest resale market in Hyderabad'],
   cons:['Appreciation ceiling lower at 19% YoY vs Kokapet or Kompally','Older building stock is mixed quality - individual project due diligence is mandatory','2BHK segment showing saturation signals - 3BHK and above is the play going forward'],
   gi:[{t:'Metro Extension to Patancheru',b:'Metro extended from Miyapur terminus - land acquisition 80% complete, 12 new stations opening a 15 km corridor'},{t:'HMDA 3x FAR Designation',b:'Miyapur-Bachupally designated high-density residential - 3x Floor Area Ratio unlocks major vertical development'},{t:'TSRTC Multimodal Hub ₹85 Cr',b:'Multimodal hub approved adjacent to Miyapur metro - integrates TSRTC, Metro and feeder buses into one terminal'}],
   tl:{p:[3200,3100,3600,4100,4700,5200,5800,6400,7000,7700],a:[40,38,55,68,78,85,90,93,95,96],n:[8,9,11,14,16,17,18,19,21,23]}},

  {id:'kompally',name:'Kompally',rank:4,lat:17.562,lng:78.476,radius:2600,type:'emerging',hni:false,nri:false,
   seg:'Emerging · ORR Belt · Land Play',col:'#00ced1',roiY:24,roi3:52,price:4100,ry:2.8,
   range:'₹40 L - ₹1.8 Cr',lst:628,nri:14,sv:195,
   vd:'52% 3-year ROI - fastest appreciating zone in North Hyderabad - still undervalued.',
   sm:'Kompally has delivered the highest raw 3-year ROI (52%) of any tracked zone. Driven by ORR access, IT campus proximity, and dramatically underpriced land. Plots at ₹40-60K per sq yard are the last affordable large-land opportunity within ORR limits. The upside from here remains substantial.',
   pros:['52% 3-year ROI - best raw appreciation of any tracked zone in the entire city','Land still at ₹40-60K/sq yard - last affordable ORR-adjacent land in Hyderabad','TCS, Infosys, Wipro campuses within 15 km - employee housing demand rapidly building'],
   cons:['Social infrastructure - malls, schools - is 3-5 years away from maturity','Illiquidity: takes 60-90 days longer to sell vs HITEC City belt','Some announced projects are behind schedule - execution risk is real'],
   gi:[{t:'Medchal Municipal Corp Upgrade',b:'Kompally elevated to Medchal-Malkajgiri Municipal Corp - GHMC-level development spending now applies'},{t:'400-Acre IT SEZ',b:'Telangana IT Dept notified 400-acre SEZ - 3 anchor tenants in negotiation, 25,000 direct jobs projected'},{t:'NH-44 6-Lane Expansion',b:'6-lane widening of NH-44 underway - doubles capacity, land values expected to jump 15-20% on completion in 2027'}],
   tl:{p:[1900,1850,2200,2700,3100,3600,4100,4900,5700,6600],a:[15,14,22,35,52,68,78,85,88,90],n:[4,4,6,8,10,12,14,16,18,21]}},

  {id:'jubilee',name:'Jubilee Hills',rank:5,lat:17.432,lng:78.408,radius:1600,type:'luxury',hni:true,nri:false,
   seg:'Ultra-Premium · Legacy · HNI',col:'#e040fb',roiY:14,roi3:28,price:12500,ry:2.9,
   range:'₹3 Cr - ₹50 Cr+',lst:98,nri:22,sv:42,
   vd:"Hyderabad's most prestigious address - capital preservation, not growth.",
   sm:"Jubilee Hills is Hyderabad's Malabar Hill - the city's most prestigious address. Supply is permanently constrained: no large land parcels remain. This is not a growth play. It is a capital preservation and social-signalling asset that retains value in all market conditions. HNI demand from industry, film and politics is structural.",
   pros:['Permanently constrained supply - no new large developments possible - protects value floor indefinitely','Most prestigious address in Hyderabad - HNI demand from industry, film, politics is structural','25% NRI share from Gulf diaspora - steady Hyderabadi diaspora demand is consistent'],
   cons:['14% YoY appreciation - lowest of all premium zones - this is not a growth investment','₹3 Cr minimum entry - smallest addressable buyer pool, hardest exit in a downturn','Aging building stock dominates - finding quality new inventory at fair price is genuinely difficult'],
   gi:[{t:'Road Widening - Road No.36',b:'GHMC widening of 5 key roads - addresses chronic congestion, ₹120 Cr allocation'},{t:'Heritage Zone Notification',b:'Jubilee Hills notified as planned residential heritage zone under HMDA 2031 - prevents commercial encroachment permanently'},{t:'Underground Cabling',b:'TSSPDCL underground cabling project approved - eliminates overhead wires, reduces outage risk'}],
   tl:{p:[8200,7900,8500,9200,10100,11200,12500,13400,14500,15800],a:[30,28,35,42,52,60,68,70,72,74],n:[15,16,17,19,20,21,22,23,24,25]}},

  {id:'manikonda',name:'Manikonda',rank:6,lat:17.394,lng:78.385,radius:1900,type:'mid',hni:false,nri:true,
   seg:'Affordable Premium · NRI Rental',col:'#26c6da',roiY:21,roi3:38,price:5200,ry:3.5,
   range:'₹50 L - ₹2.2 Cr',lst:410,nri:24,sv:175,
   vd:'Best value-for-money zone in the HITEC City belt - 21% ROI at ₹5,200/sqft.',
   sm:'Manikonda is the underrated gem of the HITEC City belt. It sits between Financial District and Gachibowli, captures the same corporate tenant base, but at prices 40% lower. NRI buyer share at 24% is driven by Gulf diaspora. At ₹50 L entry it delivers the best ROI-per-rupee of any zone in this price range.',
   pros:['40% cheaper than adjacent Financial District at identical corporate rental demand','24% NRI buyer share driven by Gulf diaspora - durable rental demand above city average','21% YoY ROI at sub-₹6K/sqft - best value of any zone in the south-west quadrant'],
   cons:['Sewage and drainage infrastructure lags behind pace of development - quality-of-life issue','Traffic on Manikonda main road is severely congested during peak hours','GHMC jurisdiction boundaries create inconsistent service delivery across parts of the zone'],
   gi:[{t:'Manikonda-Rajendranagar Flyover',b:'GHMC approved elevated corridor to ORR - reduces peak-hour travel time by 20 minutes'},{t:'Drainage Master Plan ₹280 Cr',b:'Storm water drainage project approved for Manikonda zone - addresses the key quality-of-life complaint'},{t:'HMDA Layout Regularisation',b:'Bulk regularisation of HMDA-approved layouts completed 2025 - clears title ambiguity on 2,800+ plots'}],
   tl:{p:[2800,2700,3100,3600,4100,4700,5200,5900,6700,7600],a:[25,22,32,45,58,70,78,83,87,90],n:[10,11,13,16,18,21,24,26,28,30]}},

  {id:'uppal',name:'Uppal / Nacharam',rank:7,lat:17.405,lng:78.559,radius:2200,type:'emerging',hni:false,nri:false,
   seg:'East Corridor · Affordable · IT-linked',col:'#66bb6a',roiY:17,roi3:34,price:3900,ry:3.0,
   range:'₹35 L - ₹1.5 Cr',lst:520,nri:11,sv:160,
   vd:"East Hyderabad's fastest growing affordable zone - metro-backed, IT-anchored.",
   sm:'Uppal and Nacharam form East Hyderabad\'s fastest-growing affordable belt. Metro connection to Miyapur puts this zone on the same rapid-transit network as HITEC City. Wipro SEZ, Hyderabad Central University, and the upcoming Knowledge City anchor demand on the eastern side. Entry at ₹35 L is the lowest of any metro-connected zone.',
   pros:['Metro-connected to HITEC City via LB Nagar line - puts affordable east Hyderabad on same network','₹35 L entry - lowest of any metro-connected zone - widest buyer funnel in the city','Wipro SEZ and Hyderabad Knowledge City anchoring east-side IT demand as a structural driver'],
   cons:['11% NRI buyer share - lowest of all tracked zones - limited NRI resale market','Social infrastructure quality significantly below west-Hyderabad benchmark','ORR connectivity requires transfers - commute to Financial District is 45+ minutes'],
   gi:[{t:'Hyderabad Knowledge City ₹3,200 Cr',b:'Breaking ground 2026 - adjacent to Uppal belt, 30,000 jobs projected'},{t:'Metro Phase-2 Extension',b:'Metro extended from Uppal to LB Nagar to Nagole - continuous eastern corridor to city centre'},{t:'Nacharam Industrial SEZ',b:'Nacharam Industrial Area upgraded to multi-product SEZ - attracts pharma and electronics manufacturing'}],
   tl:{p:[2100,2050,2300,2600,2900,3400,3900,4400,5000,5700],a:[20,18,25,34,46,58,68,75,80,84],n:[4,4,5,6,7,8,11,12,14,16]}},

  {id:'shamshabad',name:'Shamshabad / Pharma City',rank:8,lat:17.240,lng:78.429,radius:3300,type:'commercial',hni:true,nri:false,
   seg:'Industrial · Long-term · Land',col:'#9b59b6',roiY:16,roi3:38,price:3200,ry:2.1,
   range:'₹30 L - ₹2 Cr',lst:410,nri:9,sv:98,
   vd:"India's largest pharma cluster. A 10-year land play - 3-5x by 2035.",
   sm:"A 32,000-acre National Investment & Manufacturing Zone - Pharma City - the largest in India. Investors buying land within 5 km of the Pharma City gate today are positioned for 3-5x by 2035 as 200+ pharma companies and 20,000+ workers relocate here. Airport at 8 minutes is unmatched at this price point anywhere in Hyderabad.",
   pros:['Pharma City NIMZ - 32,000 acres, ₹1.12 lakh Cr committed - government-backed, non-negotiable','Airport at 8 minutes - no other zone offers this proximity at this price, ever','Lowest entry at ₹3,200/sqft for a future-premium zone - maximum upside per rupee invested'],
   cons:['Long gestation: 8-12 year play - not suitable for investors needing a sub-5-year exit','Pharma City Phase-1 execution is 2 years behind original schedule - bureaucratic risk is real','Very low current liquidity - difficult near-term exit if capital is needed urgently'],
   gi:[{t:'Pharma City NIMZ ₹1.12 Lakh Cr',b:'32,000-acre NIMZ - 200+ companies onboarded, 1.5 lakh direct jobs at full build-out'},{t:'MMTS Rail Extension ₹620 Cr',b:'Union Budget 2025 approved MMTS extension to Shamshabad - changes the commute equation entirely'},{t:"India's 2nd Largest Logistics Park",b:'8,000-acre logistics park adjacent to RGIA - 60,000 direct jobs, captive residential demand for entire belt'}],
   tl:{p:[1800,1750,1900,2100,2400,2800,3200,3700,4300,5100],a:[10,9,12,18,28,40,55,65,72,80],n:[2,2,3,4,6,7,9,11,13,16]}}
];

function setLoadState(message, tone, autoHide){
  const el=document.getElementById('load-state');
  if(!el) return;
  el.className='load-state';
  if(tone) el.classList.add(tone);
  el.textContent=message;
  if(autoHide){
    setTimeout(()=>el.classList.add('hide'),1800);
  }
}

// MAP
const map=L.map('map',{center:[17.41,78.42],zoom:11,zoomControl:true});
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',{attribution:'© OpenStreetMap | CARTO',subdomains:'abcd',maxZoom:20}).addTo(map);

let circ={},lblMk={},actLayer='roi',tlIdx=6,actZ=null,playing=false,ptmr=null,cmpMode=false,cmpPick=[],chReg={};
let pipelineMeta={};

function debugSummaryText(){
  const meta=pipelineMeta || {};
  const totals=meta.scrape_summary?.totals || {};
  const methods=Array.isArray(meta.actual_prediction_methods) && meta.actual_prediction_methods.length
    ? meta.actual_prediction_methods.join(', ')
    : (meta.prediction_engine || 'unknown');
  return [
    `Mode: ${meta.pipeline_mode || 'UNKNOWN'}`,
    `Methods: ${methods}`,
    `Last refresh: ${formatAge(meta.last_updated)}`,
    `Listings live/cached/fallback: ${totals.listings_live ?? 0}/${totals.listings_cached ?? 0}/${totals.listings_fallback ?? 0}`,
    `RERA live/cached/fallback: ${totals.rera_live ?? 0}/${totals.rera_cached ?? 0}/${totals.rera_fallback ?? 0}`,
    `Govt feeds live/cached/fallback: ${totals.govt_live ?? 0}/${totals.govt_cached ?? 0}/${totals.govt_fallback ?? 0}`,
    `Govt alerts: ${meta.scrape_summary?.govt_alerts?.count ?? 0}`,
    `Refresh command: cd pipeline && python pipeline.py`,
  ].join('\n');
}

function debugRow(label, value){
  return `<div class="debug-row"><span class="debug-k">${label}</span><span class="debug-v">${value}</span></div>`;
}

function renderDebugPanel(){
  const body=document.getElementById('debug-body');
  if(!body) return;
  const summary=debugSummaryText().split('\n');
  body.innerHTML=[
    debugRow('Mode', summary[0].replace('Mode: ', '')),
    debugRow('Methods', summary[1].replace('Methods: ', '')),
    debugRow('Last refresh', summary[2].replace('Last refresh: ', '')),
    debugRow('Listings live/cached/fallback', summary[3].replace('Listings live/cached/fallback: ', '')),
    debugRow('RERA live/cached/fallback', summary[4].replace('RERA live/cached/fallback: ', '')),
    debugRow('Govt feeds live/cached/fallback', summary[5].replace('Govt feeds live/cached/fallback: ', '')),
    debugRow('Govt alerts', summary[6].replace('Govt alerts: ', '')),
    debugRow('Refresh command', '<code>cd pipeline && python pipeline.py</code>'),
  ].join('');
}

async function copyDebugSummary(){
  const btn=document.getElementById('debug-copy');
  const text=debugSummaryText();
  try{
    if(navigator.clipboard?.writeText){
      await navigator.clipboard.writeText(text);
    }else{
      const ta=document.createElement('textarea');
      ta.value=text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
    }
    if(btn){
      btn.textContent='Copied';
      btn.classList.add('ok');
      setTimeout(()=>{
        btn.textContent='Copy';
        btn.classList.remove('ok');
      },1400);
    }
  }catch(_err){
    if(btn){
      btn.textContent='Copy failed';
      setTimeout(()=>btn.textContent='Copy',1400);
    }
  }
}

function toggleDebugPanel(){
  const panel=document.getElementById('debug-panel');
  const btn=document.getElementById('dbg-btn');
  if(!panel || !btn) return;
  const open=!panel.classList.contains('open');
  panel.classList.toggle('open', open);
  btn.classList.toggle('open', open);
  btn.setAttribute('aria-expanded', String(open));
}

function qualityTone(entry){
  const status=typeof entry==='string' ? entry : entry?.status;
  const fetchState=typeof entry==='string' ? '' : entry?.fetch_state;
  if(status==='live' && fetchState==='cache') return 'cache';
  return status==='live' ? 'live' : 'fallback';
}

function qualityLabel(label, entry){
  const status=typeof entry==='string' ? entry : entry?.status;
  const fetchState=typeof entry==='string' ? '' : entry?.fetch_state;
  if(status==='live' && fetchState==='cache') return `${label}: Cached`;
  return `${label}: ${status==='live' ? 'Live' : 'Fallback'}`;
}

function sourceLabel(source){
  const labels={
    '99acres.com':'99acres',
    'magicbricks.com':'MagicBricks',
    'rera.telangana.gov.in':'Telangana RERA',
    'baseline_estimate':'Internal baseline estimate',
    'baseline':'Internal city baseline',
    'unknown':'Unknown source'
  };
  return labels[source] || source || 'Unknown source';
}

function sourceUrl(source){
  const urls={
    '99acres.com':'https://www.99acres.com/',
    'magicbricks.com':'https://www.magicbricks.com/',
    'rera.telangana.gov.in':'https://rera.telangana.gov.in/'
  };
  return urls[source] || '';
}

function renderSourceMeta(label, source){
  const niceLabel=sourceLabel(source);
  const url=sourceUrl(source);
  if(url){
    return `<div class="meta">${label}: <a class="qlink" href="${url}" target="_blank" rel="noopener noreferrer">${niceLabel}</a></div>`;
  }
  return `<div class="meta">${label}: <span class="qsrc">${niceLabel}</span></div>`;
}

function fallbackReason(entry, channel){
  const source=entry?.source;
  const status=entry?.status;
  const fetchState=entry?.fetch_state;
  if(entry?.fallback_reason){
    return entry.fallback_reason;
  }
  if(status==='live' && fetchState==='cache'){
    return `${channel} is using the most recent cached response because the live request failed this run.`;
  }
  if(status==='live'){
    return `${channel} fetched successfully from the primary source in this run.`;
  }
  if(source==='baseline_estimate'){
    return `${channel} portal was unavailable during this run, so the dashboard is using the internal locality baseline.`;
  }
  if(source==='baseline'){
    return `${channel} is using the internal city baseline because no fresh scrape was available.`;
  }
  if(source==='rera.telangana.gov.in'){
    return `${channel} fell back because the RERA response was unavailable or empty for this run.`;
  }
  return `${channel} used fallback data for this refresh.`;
}

function sourceMetaLine(entry){
  if(!entry) return 'Freshness unknown';
  if(entry.fetch_state==='cache' && entry.cache_age_minutes!=null){
    return `Cached ${entry.cache_age_minutes}m old | Updated ${formatAge(entry.scraped_at)}`;
  }
  return `Updated ${formatAge(entry.scraped_at)}`;
}

function sourceStateLabel(entry){
  if(!entry) return 'Unknown';
  if(entry.status==='live' && entry.fetch_state==='cache') return 'Cached response';
  if(entry.status==='live') return 'Fresh response';
  return 'Fallback baseline';
}

function govtFeedSummary(){
  const checks=pipelineMeta?.scrape_summary?.govt_alerts?.source_checks || [];
  if(!checks.length) return 'Government feed checks not available in this run.';
  const live=checks.filter(c=>c.status==='live' && c.fetch_state!=='cache').length;
  const cached=checks.filter(c=>c.fetch_state==='cache').length;
  const fallback=checks.filter(c=>c.status!=='live').length;
  return `Govt feeds ${live} live | ${cached} cached | ${fallback} fallback`;
}

function renderGovtFeedLines(){
  const checks=pipelineMeta?.scrape_summary?.govt_alerts?.source_checks || [];
  if(!checks.length){
    return `<div class="meta">No government source checks were recorded for this refresh.</div>`;
  }
  return checks.map(check=>{
    const tone=qualityTone(check);
    const label=qualityLabel(check.name, check);
    const link=check.url ? `<a class="qlink" href="${check.url}" target="_blank" rel="noopener noreferrer">${check.name}</a>` : `<span class="qsrc">${check.name}</span>`;
    const freshness=check.fetch_state==='cache' && check.cache_age_minutes!=null
      ? `Cached ${check.cache_age_minutes}m old`
      : (check.status==='live' ? 'Fresh response' : 'Unavailable this run');
    const reason=check.fallback_reason ? `<div class="meta">${check.fallback_reason}</div>` : '';
    return `<div class="govsrc">
      <div class="govsrc-top">
        <span class="qs ${tone}">${label}</span>
        <span class="meta">${freshness}</span>
      </div>
      <div class="meta">Source: ${link}</div>
      ${reason}
    </div>`;
  }).join('');
}

function scrapeAgeSummary(localities){
  const stamps=Object.values(localities || {}).flatMap(loc=>[
    loc?.listings?.scraped_at,
    loc?.rera?.scraped_at
  ]).filter(Boolean).map(v=>new Date(v).getTime()).filter(Number.isFinite);
  if(!stamps.length) return '';
  const newest=Math.max(...stamps);
  const oldest=Math.min(...stamps);
  return ` | Freshness window: ${formatAge(new Date(newest).toISOString())} newest / ${formatAge(new Date(oldest).toISOString())} oldest`;
}

function formatAge(isoString){
  if(!isoString) return 'time unknown';
  const ts=new Date(isoString);
  if(!Number.isFinite(ts.getTime())) return 'time unknown';
  const mins=Math.max(0, Math.round((Date.now()-ts.getTime())/60000));
  if(mins < 1) return 'just now';
  if(mins < 60) return `${mins}m ago`;
  const hours=Math.round(mins/60);
  if(hours < 24) return `${hours}h ago`;
  const days=Math.round(hours/24);
  return `${days}d ago`;
}

function zoneQualitySummary(z){
  if(!z.dq) return 'Using built-in dashboard seed data.';
  const listings = z.dq.listings;
  const rera = z.dq.rera;
  const method = z.dq.prediction_method || 'unknown';
  return `${qualityLabel('Listings', listings)} | ${qualityLabel('RERA', rera)} | Prediction ${method}`;
}

function compactAge(isoString){
  const age=formatAge(isoString);
  return age==='time unknown' ? 'n/a' : age;
}

function zoneMapQuality(z){
  const listings=z.dq?.listings?.status || 'fallback';
  const rera=z.dq?.rera?.status || 'fallback';
  const listingsFetch=z.dq?.listings?.fetch_state || '';
  const reraFetch=z.dq?.rera?.fetch_state || '';
  if(listings==='live' && rera==='live' && (listingsFetch==='cache' || reraFetch==='cache')){
    return {tone:'cache', label:'CCH'};
  }
  if(listings==='live' && rera==='live'){
    return {tone:'live', label:'LIVE'};
  }
  if(listings==='fallback' && rera==='fallback'){
    return {tone:'fallback', label:'FB'};
  }
  return {tone:'mixed', label:'MIX'};
}

function zCol(z,layer){
  if(layer==='nri'){let p=z.nri;return p>30?'#4a9eff':p>20?'#00ced1':p>12?'#20b2aa':'#2f4f6f';}
  if(layer==='sales'){let v=z.sv;return v>200?'#ff3a00':v>150?'#ff8c00':v>100?'#ffd700':'#20b2aa';}
  return z.col;
}

function buildMap(){
  Z.forEach(z=>{
    const c=L.circle([z.lat,z.lng],{radius:z.radius,fillColor:z.col,fillOpacity:.28,color:z.col,weight:2,opacity:.7}).addTo(map);
    c.on('click',()=>onZone(z.id));
    circ[z.id]=c;
    const q=zoneMapQuality(z);
    const ic=L.divIcon({className:'zone-lbl',iconAnchor:[0,0],
      html:`<div class="zlbl" style="color:${z.col};border-color:${z.col}66" onclick="onZone('${z.id}')" title="${zoneQualitySummary(z)}">
        <span class="zq ${q.tone}">${q.label}</span>#${z.rank} ${z.name} <span style="color:#00c896">₹${z.price.toLocaleString()}</span>
      </div>`});
    lblMk[z.id]=L.marker([z.lat+0.015,z.lng],{icon:ic}).addTo(map);
  });
}

// SIDEBAR
function renderSB(f='all'){
  let show=Z;
  if(f==='luxury'||f==='mid'||f==='commercial'||f==='emerging') show=Z.filter(z=>z.type===f);
  else if(f==='hni') show=Z.filter(z=>z.hni);
  else if(f==='nri') show=Z.filter(z=>z.nri>=18);
  document.getElementById('zlist').innerHTML=show.map(z=>{
    const nriLvl=z.nri>30?'Very High':z.nri>20?'High':z.nri>12?'Medium':'Low';
    const hi=z.nri>20;
    const cs=cmpPick.includes(z.id)?'cs':(actZ===z.id&&!cmpMode?'on':'');
    return`<div class="zc r${Math.min(z.rank,3)} ${cs}" onclick="onZone('${z.id}')">
      <div class="zrk">#${z.rank}</div>
      <div class="zn">${z.name}</div><div class="zsg">${z.seg}</div>
      <div class="zst">
        <div class="zt"><div class="zl">3Y ROI</div><div class="zv g">${z.roi3}%</div></div>
        <div class="zt"><div class="zl">₹/sqft</div><div class="zv o">₹${z.price.toLocaleString()}</div></div>
        <div class="zt"><div class="zl">NRI %</div><div class="zv b">${z.nri}%</div></div>
      </div>
      <div class="qrow">
        <span class="qs ${qualityTone(z.dq?.listings)}">${qualityLabel('Listings', z.dq?.listings)}</span>
        <span class="qs ${qualityTone(z.dq?.rera)}">${qualityLabel('RERA', z.dq?.rera)}</span>
      </div>
      <div class="qage">Updated L ${compactAge(z.dq?.listings?.scraped_at)} | R ${compactAge(z.dq?.rera?.scraped_at)}</div>
      <span class="np ${hi?'hi':''}">NRI: ${nriLvl}</span>
    </div>`;
  }).join('');
}

// ZONE CLICK
function onZone(id){
  if(cmpMode){
    if(cmpPick.includes(id)) cmpPick=cmpPick.filter(x=>x!==id);
    else{if(cmpPick.length>=2){cmpPick.shift();}cmpPick.push(id);}
    renderSB();
    if(cmpPick.length===1){document.getElementById('cmpl').innerHTML=cmpCol(Z.find(z=>z.id===cmpPick[0]));document.getElementById('cmpr').innerHTML='<div style="color:#364862;font-size:12px;padding-top:50px;text-align:center;">Select second zone -></div>';}
    if(cmpPick.length===2) renderCmp();
    return;
  }
  actZ=id;
  const z=Z.find(v=>v.id===id);
  if(!z)return;
  renderSB();
  map.panTo([z.lat,z.lng],{animate:true});
  showDetail(z);
}

// DETAIL PANEL
function showDetail(z){
  ['pc','nc'].forEach(k=>{if(chReg[k]){chReg[k].destroy();delete chReg[k];}});
  const rbC=['','rb1','rb2','rb3','rb4','rb5','rb6','rb7','rb8'][z.rank]||'rb4';
  const rbL=['','Rank #1','Rank #2','Rank #3','Rank #4','Rank #5','Rank #6','Rank #7','Rank #8'][z.rank];
  document.getElementById('dpc').innerHTML=`
    <div class="dph"><span class="dpx" onclick="closeDp()">X</span>
      <div class="rb ${rbC}">${rbL}</div>
      <div class="dpn">${z.name}</div><div class="dpvd">${z.vd}</div>
    </div>
    <div class="dps"><h4>Returns at a Glance</h4>
      <div class="rg">
        <div class="rb2x"><div class="rv">${z.roiY}%</div><div class="rl">YoY ROI</div></div>
        <div class="rb2x"><div class="rv">${z.roi3}%</div><div class="rl">3-Year ROI</div></div>
        <div class="rb2x"><div class="rv o">${z.nri}%</div><div class="rl">NRI Buyers</div></div>
      </div>
    </div>
    <div class="dps"><h4>Why This Rank</h4>
      <div class="sb2">${z.sm}</div>
      <div class="meta">Range: ${z.range} | Listings: ${z.lst} | Sales: ${z.sv} units/qtr | Rental yield: ${z.ry}%</div>
    </div>
    <div class="dps"><h4>Source Quality</h4>
      <div class="qpanel">
        <div class="qbadges">
          <span class="qs ${qualityTone(z.dq?.listings)}">${qualityLabel('Listings', z.dq?.listings)}</span>
          <span class="qs ${qualityTone(z.dq?.rera)}">${qualityLabel('RERA', z.dq?.rera)}</span>
        </div>
        <div class="meta">${zoneQualitySummary(z)}</div>
        <div class="qgrid">
          <div class="qcard">
            <div class="qcard-k">Listings</div>
            <div class="qcard-v">${sourceStateLabel(z.dq?.listings)}</div>
            <div class="meta">${sourceMetaLine(z.dq?.listings)}</div>
            ${renderSourceMeta('Source', z.dq?.listings?.source)}
            <div class="meta">${fallbackReason(z.dq?.listings, 'Listings')}</div>
          </div>
          <div class="qcard">
            <div class="qcard-k">RERA</div>
            <div class="qcard-v">${sourceStateLabel(z.dq?.rera)}</div>
            <div class="meta">${sourceMetaLine(z.dq?.rera)}</div>
            ${renderSourceMeta('Source', z.dq?.rera?.source)}
            <div class="meta">${fallbackReason(z.dq?.rera, 'RERA')}</div>
          </div>
        </div>
        <div class="qcard qcard-full">
          <div class="qcard-k">Government Feed</div>
          <div class="qcard-v">${govtFeedSummary()}</div>
          <div class="meta">Alerts linked to this zone: ${z.dq?.govt_alert_count ?? 0}</div>
          ${renderGovtFeedLines()}
        </div>
        <div class="meta">Pipeline refreshed: ${formatAge(pipelineMeta?.last_updated)}</div>
      </div>
    </div>
    <div class="dps"><h4>Pros vs Cons</h4>
      <div class="pcg">
        <div class="pcc pros"><h5>Pros</h5>${z.pros.map(p=>`<div class="pi">${p}</div>`).join('')}</div>
        <div class="pcc cons"><h5>Cons</h5>${z.cons.map(c=>`<div class="pi">${c}</div>`).join('')}</div>
      </div>
    </div>
    <div class="dps"><h4>Government Initiatives</h4>
      ${z.gi.map(g=>`<div class="gi"><div class="git">${g.t}</div><div class="gib">${g.b}</div></div>`).join('')}
    </div>
    <div class="dps"><h4>Price Trend ₹/sqft <span style="color:#ff6b35;font-size:7px">dashed = MiroFish AI</span></h4>
      <div class="cw"><canvas id="pch"></canvas></div>
    </div>
    <div class="dps"><h4>NRI Buyer % Over Time</h4>
      <div class="cw"><canvas id="nch"></canvas></div>
    </div>`;
  document.getElementById('dp').classList.add('open');
  setTimeout(()=>drawCharts(z),60);
}
function closeDp(){document.getElementById('dp').classList.remove('open');actZ=null;renderSB();}

function drawCharts(z){
  const gc='#0d1826',tc='#364862';
  const pCanvas=document.getElementById('pch');
  const pCtx=pCanvas ? pCanvas.getContext('2d') : null;
  if(pCtx){
    chReg.pc=new Chart(pCtx,{type:'line',data:{labels:YRS,datasets:[{data:z.tl.p,tension:.4,fill:true,pointRadius:4,
      backgroundColor:z.col+'12',borderWidth:2,
      borderColor:ctx=>ctx.p1DataIndex>=7?'#ff6b35':z.col,
      pointBackgroundColor:z.tl.p.map((_,i)=>i>=7?'#ff6b35':z.col),
      segment:{borderDash:ctx=>ctx.p1DataIndex>=6?[5,4]:[]}}]},
      options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},
        tooltip:{callbacks:{label:ctx=>'₹'+ctx.raw.toLocaleString('en-IN')+'/sqft'+(ctx.dataIndex>=7?' (AI)':'')}}},
        scales:{x:{ticks:{color:tc,font:{size:7}},grid:{color:gc}},y:{ticks:{color:tc,font:{size:7},callback:v=>'₹'+v.toLocaleString('en-IN')},grid:{color:gc}}}}});
  }
  const nCanvas=document.getElementById('nch');
  const nCtx=nCanvas ? nCanvas.getContext('2d') : null;
  if(nCtx){
    chReg.nc=new Chart(nCtx,{type:'bar',data:{labels:YRS,datasets:[{data:z.tl.n,
      backgroundColor:z.tl.n.map((_,i)=>i>=7?'rgba(255,107,53,.5)':'rgba(74,158,255,.5)'),
      borderColor:z.tl.n.map((_,i)=>i>=7?'#ff6b35':'#4a9eff'),borderWidth:1}]},
      options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},
        tooltip:{callbacks:{label:ctx=>ctx.raw+'% NRI'+(ctx.dataIndex>=7?' (AI)':'')}}},
        scales:{x:{ticks:{color:tc,font:{size:7}},grid:{color:gc}},y:{ticks:{color:tc,font:{size:7},callback:v=>v+'%'},grid:{color:gc}}}}});
  }
}

// COMPARE
document.getElementById('cmp-btn').addEventListener('click',()=>{
  cmpMode=true;cmpPick=[];actZ=null;closeDp();
  document.getElementById('cmp').classList.add('open');
  document.getElementById('cmp-btn').style.display='none';
  renderSB();
});
function closeCompare(){
  cmpMode=false;cmpPick=[];
  document.getElementById('cmp').classList.remove('open');
  document.getElementById('cmp-btn').style.display='';
  renderSB();
}
function cmpMetric(label,value,cls,isWinner){
  return `<div class="str"><span class="stl">${label}</span><span class="stv ${cls||''}">${value}${isWinner?'<span class="win">WIN</span>':''}</span></div>`;
}

function cmpSummary(z,other){
  const edges=[];
  if(z.roi3>other.roi3) edges.push('higher 3Y ROI');
  if(z.roiY>other.roiY) edges.push('stronger current momentum');
  if(z.ry>other.ry) edges.push('better rental yield');
  if(z.nri>other.nri) edges.push('deeper NRI demand');
  if(z.sv>other.sv) edges.push('faster sales velocity');
  if(z.price<other.price) edges.push('lower entry price');
  if(!edges.length) return 'Profile is broadly balanced against the comparison zone.';
  return `Edge: ${edges.slice(0,2).join(' | ')}.`;
}

function cmpCol(z,other){
  if(!z)return'';
  const em=['','#1','#2','#3','#4','#5','#6','#7','#8'][z.rank];
  const wins = other ? {
    roiY: z.roiY > other.roiY,
    roi3: z.roi3 > other.roi3,
    ry: z.ry > other.ry,
    price: z.price < other.price,
    nri: z.nri > other.nri,
    sv: z.sv > other.sv,
    lst: z.lst > other.lst,
  } : {};
  return`<div style="font-size:9px;color:#364862;margin-bottom:4px">${em} RANK ${z.rank}</div>
    <div class="cmpn" style="color:${z.col}">${z.name}</div>
    <div class="cmps">${z.seg}</div>
    <div class="cmpv">${z.vd}</div>
    <div class="meta" style="margin-bottom:12px">${other?cmpSummary(z,other):'Select another zone to compare strengths side by side.'}</div>
    <div class="cmpsec"><h4>Returns</h4>
      ${cmpMetric('YoY Appreciation',`${z.roiY}%`,'g',wins.roiY)}
      ${cmpMetric('3-Year ROI',`${z.roi3}%`,'g',wins.roi3)}
      ${cmpMetric('Rental Yield',`${z.ry}%`,'b',wins.ry)}
      ${cmpMetric('Avg ₹/sqft',`₹${z.price.toLocaleString()}`,'o',wins.price)}
      ${cmpMetric('Price Range',z.range,'',false)}
    </div>
    <div class="cmpsec"><h4>Market Activity</h4>
      ${cmpMetric('NRI Buyer Share',`${z.nri}%`,'b',wins.nri)}
      ${cmpMetric('Sales Velocity',`${z.sv} units/qtr`,'',wins.sv)}
      ${cmpMetric('Active Listings',`${z.lst}`,'',wins.lst)}
      ${cmpMetric('HNI Recommended',z.hni?'Yes':'No',z.hni?'g':'o',false)}
    </div>
    <div class="cmpsec"><h4>Pros</h4>${z.pros.map(p=>`<div class="pi" style="margin-bottom:5px">${p}</div>`).join('')}</div>
    <div class="cmpsec"><h4 style="color:#ff4757">Cons</h4>${z.cons.map(c=>`<div class="pi" style="color:#ff5a5a">${c}</div>`).join('')}</div>
    <div class="cmpsec"><h4>Govt Initiatives</h4>${z.gi.map(g=>`<div class="gi"><div class="git">${g.t}</div><div class="gib">${g.b}</div></div>`).join('')}</div>`;
}
function renderCmp(){
  const [a,b]=cmpPick.map(id=>Z.find(z=>z.id===id));
  if(!a||!b)return;
  document.getElementById('cmpl').innerHTML=cmpCol(a,b);
  document.getElementById('cmpr').innerHTML=cmpCol(b,a);
}

// CALCULATOR
const calcP=document.getElementById('cp');
document.getElementById('calc-btn').addEventListener('click',()=>calcP.classList.toggle('open'));
const izSel=document.getElementById('izone');
Z.forEach(z=>{const o=document.createElement('option');o.value=z.id;o.textContent=`#${z.rank} ${z.name} (${z.roi3}% 3Y ROI)`;izSel.appendChild(o);});
function runCalc(){
  const amt=parseFloat(document.getElementById('iamt').value)||5000000;
  const yrs=parseInt(document.getElementById('iyrs').value)||3;
  const z=Z.find(v=>v.id===document.getElementById('izone').value);
  if(!z)return;
  const rate=(z.roiY/100)*(yrs>5?0.75:yrs>3?0.85:1);
  const val=amt*Math.pow(1+rate,yrs);
  const profit=val-amt;
  const roi=((val-amt)/amt)*100;
  const rent=amt*z.ry/100;
  const fmt=v=>'₹'+Math.round(v).toLocaleString('en-IN');
  document.getElementById('cr-i').textContent=fmt(amt);
  document.getElementById('cr-v').textContent=fmt(val);
  document.getElementById('cr-p').textContent=fmt(profit);
  document.getElementById('cr-r').textContent=roi.toFixed(1)+'%';
  document.getElementById('cr-y').textContent=fmt(rent)+'/yr';
  document.getElementById('cres').style.display='block';
}
document.addEventListener('click',e=>{if(!calcP.contains(e.target)&&e.target.id!=='calc-btn')calcP.classList.remove('open');});

// LAYER BUTTONS
document.querySelectorAll('.mb').forEach(b=>{
  b.addEventListener('click',()=>{
    actLayer=b.dataset.layer;
    document.querySelectorAll('.mb').forEach(x=>x.classList.remove('on'));
    b.classList.add('on');
    Z.forEach(z=>{
      const c=zCol(z,actLayer);
      if(circ[z.id]) circ[z.id].setStyle({fillColor:c,color:c});
    });
  });
});

// FILTER BUTTONS
document.querySelectorAll('[data-qf]').forEach(b=>{
  b.addEventListener('click',()=>{
    document.querySelectorAll('[data-qf]').forEach(x=>x.classList.remove('on'));
    b.classList.add('on');
    renderSB(b.dataset.qf);
  });
});

// TIMELINE
const slider=document.getElementById('ts');
function applyTL(idx){
  tlIdx=idx;const yr=YRS[idx];
  const mc=document.getElementById('mc'),ml=document.getElementById('tlml'),dl=document.getElementById('tld');
  if(idx<6){mc.className='mc-h';mc.textContent='HISTORICAL - '+yr;ml.className='tlm tlm-h';ml.textContent='HISTORICAL: '+yr;dl.textContent='Past development activity, construction completions, and government milestones - '+yr;}
  else if(idx===6){mc.className='mc-c';mc.textContent='CURRENT STATE - Q1 2026';ml.className='tlm tlm-c';ml.textContent='CURRENT: Q1 2026';dl.textContent='Live market - current prices, active listings, and investor activity';}
  else{mc.className='mc-p';mc.textContent='AI PREDICTION - '+yr;ml.className='tlm tlm-p';ml.textContent='AI PREDICTION: '+yr;dl.textContent='MiroFish multi-agent simulation - predicted appreciation, activity, and NRI demand for '+yr;}
  Z.forEach(z=>{
    const act=z.tl.a[idx]/100,r=z.radius*(0.45+0.55*act);
    const fo=idx<6?0.12+0.22*act:idx===6?0.28:0.15+0.2*act;
    if(circ[z.id]){
      circ[z.id].setRadius(r);
      circ[z.id].setStyle({fillOpacity:fo,opacity:idx<6?0.45:0.72});
    }
  });
  if(actZ){const z=Z.find(v=>v.id===actZ);if(z)setTimeout(()=>drawCharts(z),40);}
}
slider.addEventListener('input',e=>applyTL(parseInt(e.target.value)));
const pb=document.getElementById('pbtn');
pb.addEventListener('click',()=>{
  playing=!playing;pb.textContent=playing?'Pause':'Play';
  if(playing){ptmr=setInterval(()=>{let v=parseInt(slider.value)+1;if(v>9)v=0;slider.value=v;applyTL(v);},1100);}
  else clearInterval(ptmr);
});

// LIVE DATA PIPELINE LOADER
// Tries to load pipeline/output/data.json generated by pipeline.py
// If found -> updates zone prices, predictions, city stats, govt alerts
// If not found -> uses hardcoded data silently (no blocking errors shown to user)

function mergeLiveZone(z, live) {
  if (live.name) z.name = live.name;
  if (live.rank) z.rank = live.rank;
  if (live.type) z.type = live.type;
  if (live.segment) z.seg = live.segment;
  if (live.color) z.col = live.color;
  if (live.avgPrice) z.price = live.avgPrice;
  if (live.priceRange) z.range = live.priceRange;
  if (live.roiYoY) z.roiY = live.roiYoY;
  if (live.roi3Y) z.roi3 = live.roi3Y;
  if (live.nriPct) z.nri = live.nriPct;
  if (live.salesVel) z.sv = live.salesVel;
  if (live.listings) z.lst = live.listings;
  if (live.verdict) z.vd = live.verdict;
  if (live.summary) z.sm = live.summary;
  if (live.pros) z.pros = live.pros;
  if (live.cons) z.cons = live.cons;
  if (live.govtInit) z.gi = live.govtInit;
  if (live.dataQuality) z.dq = live.dataQuality;

  if (live.tl) {
    if (live.tl.price && live.tl.price.length === 10) z.tl.p = live.tl.price;
    if (live.tl.nri && live.tl.nri.length === 10) z.tl.n = live.tl.nri;
    if (live.tl.activity && live.tl.activity.length === 10) z.tl.a = live.tl.activity;
  }

  if (live.govtAlerts && live.govtAlerts.length > 0) {
    live.govtAlerts.slice(0, 2).forEach(a => {
      const exists = z.gi.find(g => g.t === a.title || g.t === ('Alert: ' + a.title));
      if (!exists) z.gi.push({ t: 'Alert: ' + a.title, b: a.body });
    });
  }
}

function updateTopbarStats(cityStats, meta) {
  pipelineMeta=meta || {};
  renderDebugPanel();
  const statMap = {
    'sp-price': { v: 'Rs ' + cityStats.avg_price_sqft.toLocaleString('en-IN') },
    'sp-sales': { v: cityStats.quarterly_sales.toLocaleString('en-IN') + ' units' },
    'sp-nri': { v: 'Rs ' + cityStats.nri_investment_cr.toLocaleString('en-IN') + ' Cr' },
    'sp-projects': { v: cityStats.active_projects.toLocaleString('en-IN') },
    'sp-unsold': { v: cityStats.unsold_inventory.toLocaleString('en-IN') + ' units' },
  };
  Object.entries(statMap).forEach(([id, cfg]) => {
    const el = document.getElementById(id);
    if (el) el.textContent = cfg.v;
  });

  const badge = document.getElementById('live-badge');
  if (badge) {
    const ts = new Date(meta.last_updated);
    const ago = Number.isFinite(ts.getTime()) ? Math.max(0, Math.round((Date.now() - ts) / 60000)) : null;
    const methods = Array.isArray(meta.actual_prediction_methods)
      ? meta.actual_prediction_methods.join(', ')
      : (meta.prediction_engine || 'unknown');

    if (meta.pipeline_mode === 'LIVE') {
      badge.textContent = `LIVE DATA - ${formatAge(meta.last_updated)}`;
      badge.style.color = '#00c896';
      setLoadState('Pipeline data loaded. Map and rankings refreshed.', 'ok', true);
    } else if (meta.pipeline_mode === 'FALLBACK') {
      badge.textContent = `FALLBACK DATA - ${formatAge(meta.last_updated)}`;
      badge.style.color = '#ffb347';
      setLoadState('Pipeline loaded with fallback predictions.', 'warn', true);
    } else {
      badge.textContent = `DEMO DATA - ${formatAge(meta.last_updated)}`;
      badge.style.color = '#ffd700';
      setLoadState('Using generated demo-mode data from the pipeline.', 'warn', true);
    }

    const totals = meta.scrape_summary?.totals;
    const totalsText = totals
      ? ` | Listings live/cached/fallback: ${totals.listings_live}/${totals.listings_cached ?? 0}/${totals.listings_fallback} | RERA live/cached/fallback: ${totals.rera_live}/${totals.rera_cached ?? 0}/${totals.rera_fallback} | Govt feeds live/cached/fallback: ${totals.govt_live ?? 0}/${totals.govt_cached ?? 0}/${totals.govt_fallback ?? 0}`
      : '';
    const agesText = scrapeAgeSummary(meta.scrape_summary?.localities || {});
    badge.title = `Pipeline: ${meta.pipeline_mode || 'UNKNOWN'} | Methods: ${methods}${totalsText}${agesText}`;
  }
}

async function loadLiveData() {
  setLoadState('Loading pipeline data and refreshing zone metrics...', '', false);
  try {
    const resp = await fetch('pipeline/output/data.json');
    if (!resp.ok) throw new Error('No data.json yet');
    const data = await resp.json();
    pipelineMeta=data.metadata || {};
    renderDebugPanel();

    const liveZones = data.zones || {};
    Z.forEach(z => {
      if (liveZones[z.id]) mergeLiveZone(z, liveZones[z.id]);
    });

    if (data.city_stats) updateTopbarStats(data.city_stats, data.metadata || {});

    Object.values(circ).forEach(c => map.removeLayer(c));
    Object.values(lblMk).forEach(m => map.removeLayer(m));
    circ={};
    lblMk={};
    buildMap();
    renderSB();

    if (actZ) {
      const z = Z.find(v => v.id === actZ);
      if (z) showDetail(z);
    }

    console.log('[HydROI] Live data loaded from pipeline/output/data.json');
  } catch (e) {
    renderDebugPanel();
    const badge = document.getElementById('live-badge');
    if (badge) {
      badge.textContent = 'DEMO DATA - run pipeline.py to activate live feed';
      badge.style.color = '#3a4a6a';
    }
    setLoadState('Using built-in demo data. Run pipeline.py to refresh the live feed.', 'warn', true);
    console.log('[HydROI] Using hardcoded data (pipeline not run yet):', e.message);
  }
}

// INIT
document.getElementById('dbg-btn')?.addEventListener('click', toggleDebugPanel);
document.getElementById('debug-copy')?.addEventListener('click', copyDebugSummary);
buildMap();
renderSB();
setTimeout(()=>onZone('kokapet'),700);
loadLiveData();
