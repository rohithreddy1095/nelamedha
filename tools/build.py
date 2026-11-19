"""Builds the Nelamedha site: four pages in English and Telugu, sharing one header, contact block and footer.
Run from the repository root:  python3 tools/build.py
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600'
         '&family=Source+Sans+3:wght@400;600&family=JetBrains+Mono:wght@400;500&family=Noto+Sans+Telugu:wght@400;600'
         '&family=Noto+Serif+Telugu:wght@600&display=swap">')
ICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%235A3A22'/%3E"
        "%3Cpath d='M32 50V26M32 34c-9 0-13-6-13-13 9 0 13 6 13 13zm0-5c8 0 12-5 12-12-8 0-12 5-12 12z' fill='none' stroke='%23E9DFC8' stroke-width='4' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E")

def t(en, te, tag='span', cls='', attrs=''):
    """The same words in English and Telugu; the page shows one at a time."""
    c = (' ' + cls) if cls else ''
    return f'<{tag} class="en{c}"{attrs}>{en}</{tag}><{tag} class="te{c}"{attrs} lang="te">{te}</{tag}>'

def head(pre, title_en, title_te, desc, path):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title data-en="{title_en}" data-te="{title_te}">{title_en}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title_en}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://nelamedha.in/{path}">
<link rel="canonical" href="https://nelamedha.in/{path}">
<link rel="icon" href="{ICON}">
{FONTS}
<link rel="stylesheet" href="{pre}assets/site.css">
</head>
<body>
<a class="skip" href="#main">{t("Skip to content","విషయానికి వెళ్ళండి")}</a>
'''

def header(pre, cur):
    items = [('', 'Home', 'మొదటి పేజీ'), ('farm/', 'The farm', 'పొలం'), ('projects/', 'Projects', 'పనులు'), ('research/', 'Research', 'పరిశోధన'), ('gallery/', 'Photos', 'ఫోటోలు')]
    links = ''.join(f'<a href="{pre}{h or "./"}"{" aria-current=page" if h == cur else ""}>{t(en, te)}</a>' for h, en, te in items)
    return f'''<div class="wrap">
  <header class="top">
    <a class="mark" href="{pre}./">Nelamedha <small lang="te">నేలమేధ</small></a>
    <nav class="nav" aria-label="Main">{links}<a href="#contact">{t("Contact","సంప్రదించండి")}</a><button class="lang" type="button" aria-label="తెలుగులో చదవండి">{t("తెలుగు","English")}</button></nav>
  </header>
</div>
<main id="main">
'''

from urllib.parse import quote
WA_EN = 'https://wa.me/918680929591?text=' + quote('Hello, I found Nelamedha at nelamedha.in and would like to know more.')
WA_TE = 'https://wa.me/918680929591?text=' + quote('నమస్తే, nelamedha.in లో నేలమేధ గురించి చూశాను. మరిన్ని వివరాలు తెలుసుకోవాలనుకుంటున్నాను.')
WA_ICON = ('<svg aria-hidden="true" viewBox="0 0 24 24" width="18" height="18" style="vertical-align:-3px;margin-right:8px"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7a2.8 2.8 0 0 0 1.8-1.3 2.3 2.3 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>')

def contact():
    return f'''</main>
<section class="contact" id="contact"><div class="wrap two">
  <div>
    {t("Talk to us","మాతో మాట్లాడండి","h2")}
    {t("If you are planting a food forest, building with earth, want to try the sensors on your own land, or want to research with us, write or call.",
       "మీరు ఆహార అడవి నాటుతున్నా, మట్టితో ఇల్లు కడుతున్నా, మీ నేలపై సెన్సర్లు ప్రయత్నించాలనుకున్నా, లేదా మాతో కలిసి పరిశోధన చేయాలనుకున్నా, రాయండి లేదా ఫోన్ చేయండి.","p","sub")}
  </div>
  <dl>
    <div><dt>{t("Founder","వ్యవస్థాపకుడు")}</dt><dd class="plain">{t("Modugu Rohith Reddy","మోదుగు రోహిత్ రెడ్డి")}</dd></div>
    <div><dt>{t("Email","ఈమెయిల్")}</dt><dd>rohithreddy1095@gmail.com</dd></div>
    <div><dt>{t("Phone","ఫోన్")}</dt><dd>+91 86809 29591</dd></div>
    <div><a class="btn wa en" href="{WA_EN}" target="_blank" rel="noopener">{WA_ICON}Message on WhatsApp</a><a class="btn wa te" lang="te" href="{WA_TE}" target="_blank" rel="noopener">{WA_ICON}వాట్సాప్‌లో మెసేజ్ చేయండి</a></div>
  </dl>
</div></section>
'''

def footer(pre, extra_en='', extra_te=''):
    return f'''<footer><div class="wrap"><p>{t("Nelamedha · rural technology research · Ganugabanda, Suryapet district, Telangana · Being registered as a non-profit research foundation, 2026" + extra_en,
      "నేలమేధ · గ్రామీణ సాంకేతిక పరిశోధన · గానుగబండ, సూర్యాపేట జిల్లా, తెలంగాణ · లాభాపేక్ష లేని పరిశోధన సంస్థగా నమోదవుతోంది, 2026" + extra_te)}</p></div></footer>
<script src="{pre}assets/site.js"></script>
'''

def page(path, html):
    out = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w').write(html + '</body>\n</html>\n')
    print('wrote', path, len(html))

# ---------- shared pieces of content ----------
HERO = open(os.path.join(ROOT, 'tools', 'hero.svg')).read()
SAT = [  # the seven sharp pictures: date, file, satellite line, what changed
 ('2011-04-01', 'IKONOS (GeoEye) · 1 m pixels, shown at 1.1 m', 'IKONOS (GeoEye) · 1 మీ. పిక్సెల్స్, 1.1 మీ.గా చూపబడింది',
  'Paddy, just after the rabi harvest: the plots are pale stubble in the April sun. A row of trees already lines the track.',
  'రబీ కోతలు అయిన వెంటనే వరి మడులు: ఏప్రిల్ ఎండలో మోళ్లు తెల్లగా కనిపిస్తున్నాయి. దారి వెంబడి చెట్ల వరుస అప్పటికే ఉంది.'),
 ('2013-05-16', 'WorldView-2 (Maxar) · 0.5 m pixels, shown at 0.6 m', 'WorldView-2 (Maxar) · 0.5 మీ. పిక్సెల్స్, 0.6 మీ.గా చూపబడింది',
  'The same plots in May, darker than the bare fields round them: still damp, or carrying a summer crop. The banks between the plots run where the farm’s edges are today.',
  'మే నెలలో అవే మడులు, చుట్టూ ఉన్న ఖాళీ పొలాల కంటే ముదురుగా: ఇంకా తడిగా ఉన్నాయి, లేదా వేసవి పంట ఉంది. మడుల మధ్య గట్లు ఈరోజు పొలం హద్దులు ఉన్న చోటే ఉన్నాయి.'),
 ('2017-03-10', 'WorldView-2 (Maxar) · 0.5 m pixels, shown at 1.1 m', 'WorldView-2 (Maxar) · 0.5 మీ. పిక్సెల్స్, 1.1 మీ.గా చూపబడింది',
  'Rabi paddy, green from edge to edge. The land is still paddy, like everything round it.',
  'రబీ వరి, ఈ చివర నుంచి ఆ చివర వరకు పచ్చగా. చుట్టూ ఉన్నట్లే ఈ నేల కూడా ఇంకా వరి పొలమే.'),
 ('2021-02-06', 'WorldView-2 (Maxar) · 0.5 m pixels, shown at 0.6 m', 'WorldView-2 (Maxar) · 0.5 మీ. పిక్సెల్స్, 0.6 మీ.గా చూపబడింది',
  'Still paddy in February 2021, the last sharp picture before the change. Sentinel-2 dates the change to after the harvest of late 2021.',
  '2021 ఫిబ్రవరిలోనూ వరి పొలమే. మార్పుకు ముందు చివరి స్పష్టమైన చిత్రం ఇది. 2021 చివర్లో కోతల తర్వాత మార్పు మొదలైందని సెంటినెల్-2 చూపిస్తుంది.'),
 ('2022-06-07', 'WorldView-2 (Maxar) · 0.5 m pixels, shown at 0.6 m', 'WorldView-2 (Maxar) · 0.5 మీ. పిక్సెల్స్, 0.6 మీ.గా చూపబడింది',
  'The change has happened: the west part is a dark green block with rows of young plants, and east of a path across the middle, saplings stand in rows on bare ground.',
  'మార్పు జరిగిపోయింది: పడమటి భాగం లేత మొక్కల వరుసలతో ముదురు పచ్చగా ఉంది; మధ్యలో ఉన్న దారికి తూర్పున, ఖాళీ నేలపై మొక్కలు వరుసలుగా నిలిచాయి.'),
 ('2023-12-22', 'WorldView-2 (Maxar) · 0.5 m pixels, shown at 0.6 m', 'WorldView-2 (Maxar) · 0.5 మీ. పిక్సెల్స్, 0.6 మీ.గా చూపబడింది',
  'An orchard in rows over the whole farm. Most of the west part is bare red-brown earth, freshly worked, and a building stands with a red roof.',
  'పొలమంతా వరుసల్లో తోట. పడమటి భాగంలో ఎక్కువ భాగం కొత్తగా దున్నిన ఎర్రటి నేల; ఎర్ర పైకప్పుతో ఒక కట్టడం నిలిచింది.'),
 ('2025-04-29', 'WorldView-3 (Vantor) · 0.31 m pixels, shown at 0.6 m', 'WorldView-3 (Vantor) · 0.31 మీ. పిక్సెల్స్, 0.6 మీ.గా చూపబడింది',
  'Green almost wall to wall in April, in the heart of the dry season, while the fields round it are bare. The blue-roofed cow shed by the track is new since December 2023.',
  'వేసవి మధ్యలో ఏప్రిల్‌లోనూ దాదాపు పొలమంతా పచ్చగా ఉంది, చుట్టూ పొలాలు ఖాళీగా ఉన్నా. దారి పక్కన నీలి పైకప్పు పశువుల పాక 2023 డిసెంబరు తర్వాత వచ్చింది.'),
]
FARM = [(202,252),(247,156),(317,186),(341,145),(439,188),(367,333),(346,336),(336,328),(259,291)]   # traced on the 2023 picture, in picture pixels
SAT_DATA = {'base': '../assets/img/sat/', 'w': 640, 'h': 480, 'mpp': 0.5716, 'farm': [list(p) for p in FARM],
            'marks': [{'x': 220, 'y': 250, 'en': 'cow shed', 'te': 'పశువుల పాక'}],
            'pics': [{'d': d, 'f': d + '.webp', 'meta': {'en': me, 'te': mt}, 'note': {'en': ne, 'te': nt}} for d, me, mt, ne, nt in SAT]}

LOG = [  # newest first: when, title, what
 ('Nov 2026', 'నవంబరు 2026', 'Nelamedha takes shape', 'నేలమేధ రూపుదిద్దుకుంది',
  'The name, and this website at nelamedha.in.', 'పేరు, nelamedha.in లో ఈ వెబ్‌సైట్.'),
 ('Nov 2026', 'నవంబరు 2026', 'The farmhouse plan, in 3D', 'ఫాంహౌస్ ప్రణాళిక, 3Dలో',
  'The no-cement house for the farm, priced part by part, with a build-along you can step through job by job.',
  'సిమెంటు లేని ఫాంహౌస్ ప్రణాళిక, ప్రతి భాగం ధరతో, పని పని చొప్పున చూడగలిగే 3D నిర్మాణంతో.'),
 ('2026', '2026', 'Sensors on the bench', 'బెంచ్‌పై సెన్సర్లు',
  'Soil-moisture sensors reading through a Jetson Orin Nano, the first step of ClawMesh.',
  'జెట్సన్ ఓరిన్ నానో ద్వారా నేల తేమ సెన్సర్ల రీడింగ్: క్లామెష్‌లో మొదటి అడుగు.'),
 ('2024–25', '2024–25', 'The cow shed', 'పశువుల పాక',
  'Built by the track at the west corner, between the December 2023 and April 2025 pictures.',
  'పడమటి మూలలో దారి పక్కన, 2023 డిసెంబరు, 2025 ఏప్రిల్ చిత్రాల మధ్య కట్టబడింది.'),
 ('Dec 2023', 'డిసెంబరు 2023', 'An orchard in rows', 'వరుసల్లో తోట',
  'Trees in rows across the whole farm, and the first building.', 'పొలమంతా వరుసల్లో చెట్లు, మొదటి కట్టడం.'),
 ('Jun 2022', 'జూన్ 2022', 'Saplings on bare ground', 'ఖాళీ నేలపై మొక్కలు',
  'Young plants in rows where the paddy plots were.', 'వరి మడులు ఉన్నచోట వరుసలుగా లేత మొక్కలు.'),
 ('Dec 2021', 'డిసెంబరు 2021', 'The farm leaves the paddy year', 'పొలం వరి చక్రం నుంచి బయటకు',
  'After the harvest of late 2021 the land no longer greens and dries with the paddy round it.',
  '2021 చివరి కోతల తర్వాత, చుట్టూ ఉన్న వరితో పాటు ఈ నేల పచ్చబడటం, ఎండటం ఆగిపోయింది.'),
 ('2011–2021', '2011–2021', 'Paddy', 'వరి పొలం',
  'Paddy plots, two crops a year, like the land round it.', 'చుట్టూ ఉన్న నేలలాగే, ఏడాదికి రెండు పంటల వరి మడులు.'),
]
def log_html(items):
    return '<ol class="log">' + ''.join(
        f'<li><time>{t(we, wt)}</time>{t(he, ht, "h3")}{t(pe, pt, "p")}</li>' for we, wt, he, ht, pe, pt in items) + '</ol>'

def pic(d, en, te, w=640, h=480, lazy=True):
    return (f'<img src="{{pre}}assets/img/sat/{d}.webp" width="{w}" height="{h}" {"loading=lazy " if lazy else ""}'
            f'alt="{en}" data-alt-en="{en}" data-alt-te="{te}">')

# ---------- home ----------
pre = ''
home = head(pre, 'Nelamedha · soil, with intelligence', 'నేలమేధ · నేలతో, మేధతో',
            'Nelamedha researches rural technology for natural farming and self-sustaining living: food forests, building with earth, and farm automation with small computers and AI, on a farm in Suryapet, Telangana.', '')
home += header(pre, '')
home += f'''<div class="wrap">
  <div class="hero">
    <div>
      {t("Rural technology research · Suryapet, Telangana","గ్రామీణ సాంకేతిక పరిశోధన · సూర్యాపేట, తెలంగాణ","p","kicker")}
      {t("Soil, with intelligence.","నేలతో, మేధతో.","h1")}
      {t('<b>nela</b> నేల soil, land · <b>medha</b> మేధ intelligence','<b>నేల</b> భూమి, మట్టి · <b>మేధ</b> తెలివి','p','gloss')}
      {t("Nelamedha researches rural technology that helps natural farming on the ground. On a working farm in Telangana we grow a food forest, build with earth, and teach small computers to look after the land, working towards a way of life that sustains itself end to end. What works here is written down and shared.",
         "సహజ వ్యవసాయానికి నేల మీద నిజంగా ఉపయోగపడే గ్రామీణ సాంకేతికతపై నేలమేధ పరిశోధన చేస్తుంది. తెలంగాణలోని ఒక పని చేసే పొలంలో మేము ఆహార అడవిని పెంచుతున్నాం, మట్టితో ఇల్లు కడుతున్నాం, నేలను చూసుకునేలా చిన్న కంప్యూటర్లకు నేర్పిస్తున్నాం; మొదటి నుంచి చివరి వరకు తనను తాను నిలబెట్టుకునే జీవన విధానం వైపు. ఇక్కడ పనిచేసేది రాసి, అందరితో పంచుకుంటాం.","p","lede")}
      <p style="display:flex;flex-wrap:wrap;gap:12px;margin:26px 0 0"><a class="btn" href="farm/">{t("The farm’s story →","పొలం కథ →")}</a><a class="btn" href="research/" style="background:var(--paper-2);color:var(--ink);border:1px solid var(--line)">{t("Research directions","పరిశోధన దిశలు")}</a></p>
    </div>
    <figure class="fig">{HERO}
      <figcaption>{t("Canopy, roots, soil, and a sensor that reports what the roots are getting.","చెట్ల పందిరి, వేర్లు, నేల, వేర్లకు ఏమి అందుతుందో చెప్పే ఒక సెన్సర్.")}</figcaption>
    </figure>
  </div>
</div>
<section id="work"><div class="wrap">
  {t("Three kinds of work, one piece of ground","ఒకే నేలపై మూడు రకాల పని","h2")}
  {t("Each one feeds the next. The forest gives food, the earth under it becomes walls, and the machines keep watch so that a few people can look after a lot of land.",
     "ఒకటి మరొకదానికి తోడ్పడుతుంది. అడవి ఆహారం ఇస్తుంది, దాని కింది మట్టి గోడలవుతుంది, కొద్దిమంది ఎక్కువ నేలను చూసుకోగలిగేలా యంత్రాలు కాపలా కాస్తాయి.","p","sub")}
  <div class="three">
    <article class="card"><span class="n">01</span>{t("Food forest","ఆహార అడవి","h3")}{t("Trees planted in layers on what was paddy land until 2021, so the ground stays covered and feeds itself.","2021 వరకు వరి పొలంగా ఉన్న నేలపై పొరలు పొరలుగా నాటిన చెట్లు. నేల ఎప్పుడూ కప్పి ఉంటుంది, తనను తాను పోషించుకుంటుంది.","p")}<p class="more"><a href="farm/">{t("See it from space →","అంతరిక్షం నుంచి చూడండి →")}</a></p></article>
    <article class="card"><span class="n">02</span>{t("Building with earth","మట్టితో నిర్మాణం","h3")}{t("A house on the farm with no cement: cob, adobe and pressed-block walls under a tiled roof, running on rain, sun and biogas.","సిమెంటు లేని ఇల్లు: మట్టి ముద్దల గోడ, ఎండబెట్టిన మట్టి ఇటుకలు, ఒత్తిన మట్టి బ్లాకులు, పెంకుల పైకప్పు. వాన నీరు, సౌర శక్తి, బయోగ్యాస్‌తో నడుస్తుంది.","p")}<p class="more"><a href="projects/#house">{t("The plan →","ప్రణాళిక →")}</a></p></article>
    <article class="card"><span class="n">03</span>{t("Farm automation","పొలం ఆటోమేషన్","h3")}{t("Soil-moisture sensors and small computers in the field, with AI that suggests the next job and a person who approves anything risky.","పొలంలో నేల తేమ సెన్సర్లు, చిన్న కంప్యూటర్లు. తదుపరి పని ఏమిటో AI సూచిస్తుంది; ప్రమాదం ఉన్న ఏ పనినైనా ఒక మనిషి ఆమోదిస్తారు.","p")}<p class="more"><a href="projects/#clawmesh">{t("ClawMesh →","క్లామెష్ →")}</a></p></article>
  </div>
</div></section>
<section><div class="wrap">
  {t("From paddy to food forest in four years","నాలుగేళ్లలో వరి పొలం నుంచి ఆహార అడవి వరకు","h2")}
  {t("The same ground, photographed from satellites in February 2021 and April 2025.","ఒకే నేల, 2021 ఫిబ్రవరిలో, 2025 ఏప్రిల్‌లో ఉపగ్రహాల నుంచి తీసిన చిత్రాలు.","p","sub")}
  <div class="two">
    <figure class="fig">{pic("2021-02-06","The farm in February 2021: paddy","2021 ఫిబ్రవరిలో పొలం: వరి")}<figcaption>{t("February 2021: paddy, like everything round it","ఫిబ్రవరి 2021: చుట్టూ ఉన్నట్లే వరి")}</figcaption></figure>
    <figure class="fig">{pic("2025-04-29","The farm in April 2025: a food forest","2025 ఏప్రిల్‌లో పొలం: ఆహార అడవి")}<figcaption>{t("April 2025: green in the dry season, the fields round it bare","ఏప్రిల్ 2025: వేసవిలోనూ పచ్చగా, చుట్టూ పొలాలు ఖాళీగా")}</figcaption></figure>
  </div>
  <p style="margin:24px 0 0"><a class="btn" href="farm/">{t("All seven pictures, 2011 to 2025 →","2011 నుంచి 2025 వరకు ఏడు చిత్రాలు →")}</a></p>
</div></section>
<section><div class="wrap two">
  <div>
    {t("Next: a greenhouse that runs itself","తదుపరి: తనంతట తాను నడిచే గ్రీన్‌హౌస్","h2")}
    {t("Sensors, valves, fans and a small computer on the farm, powered by the sun and working without the internet. A greenhouse is the easiest place to learn what can be automated; what works there moves out to the forest.",
       "సెన్సర్లు, వాల్వులు, ఫ్యాన్లు, ఒక చిన్న కంప్యూటర్, సౌర శక్తితో, ఇంటర్నెట్ లేకుండా పనిచేసేలా. ఏది ఆటోమేట్ చేయవచ్చో నేర్చుకోవడానికి గ్రీన్‌హౌస్ సులువైన చోటు; అక్కడ పనిచేసింది అడవిలోకి వెళ్తుంది.","p","sub")}
    <p><a class="btn" href="research/">{t("Research directions →","పరిశోధన దిశలు →")}</a></p>
  </div>
  <div>
    {t("Latest","తాజా సమాచారం","h3")}
    <div style="margin-top:16px">{log_html(LOG[:3])}</div>
    <p style="margin:18px 0 0"><a href="projects/#progress">{t("All progress →","మొత్తం పురోగతి →")}</a></p>
  </div>
</div></section>
'''
home = home.replace('{pre}', pre) + contact() + footer(pre)
page('index.html', home)

# ---------- the farm ----------
pre = '../'
CH = [('2017–21', 0.20, 0.16, 0.24), ('2022', 0.47, None, None), ('2023', 0.42, None, None), ('2024', 0.35, None, None), ('2025', 0.51, None, None), ('2026', 0.44, None, None)]
def chart():
    W, H, pl, pb, pt = 640, 260, 40, 34, 14
    bw = (W - pl - 20) / len(CH)
    Y = lambda v: pt + (H - pt - pb) * (1 - v / 0.6)
    s = f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Average greenness in April and May. 2017 to 2021: about 0.2, the same as the fields round it. Then 0.47, 0.42, 0.35, 0.51 and 0.44 from 2022 to 2026, while the fields stay near 0.2.">'
    s += f'<rect x="{pl}" y="{Y(0.26):.1f}" width="{W-pl-20}" height="{Y(0.19)-Y(0.26):.1f}" class="bar-field"/>'
    for v in (0, 0.2, 0.4, 0.6):
        s += f'<line class="axis" x1="{pl}" x2="{W-20}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/><text x="{pl-6}" y="{Y(v)+4:.1f}" text-anchor="end">{v:g}</text>'
    for k, (lab, v, lo, hi) in enumerate(CH):
        x = pl + k * bw + bw * 0.22
        s += f'<rect x="{x:.1f}" y="{Y(v):.1f}" width="{bw*0.56:.1f}" height="{Y(0)-Y(v):.1f}" rx="3" class="bar-farm"/>'
        if lo is not None:
            cx = x + bw * 0.28
            s += f'<line x1="{cx:.1f}" x2="{cx:.1f}" y1="{Y(hi):.1f}" y2="{Y(lo):.1f}" style="stroke:var(--ink);stroke-width:2"/>'
        s += f'<text x="{x+bw*0.28:.1f}" y="{Y(v)-8:.1f}" text-anchor="middle" style="fill:var(--ink)">{v:.2f}</text><text x="{x+bw*0.28:.1f}" y="{H-12}" text-anchor="middle">{lab}</text>'
    return s + '</svg>'

farm = head(pre, 'The farm · Nelamedha', 'పొలం · నేలమేధ', 'Mr Green Farms from above: every sharp satellite picture from 2011 to 2025, from paddy plots to a food forest.', 'farm/')
farm += header(pre, 'farm/')
farm += f'''<div class="wrap">
  <div class="page-head">
    {t("The farm","పొలం","p","kicker")}
    {t("Mr Green Farms, from above","మిస్టర్ గ్రీన్ ఫార్మ్స్, పైనుంచి","h1")}
    {t("Every sharp satellite picture of the farm we could find, from 2011 to 2025. The same ground goes from paddy plots to a food forest. What we write under each picture is our reading of it.",
       "2011 నుంచి 2025 వరకు మాకు దొరికిన పొలం స్పష్టమైన ఉపగ్రహ చిత్రాలన్నీ ఇక్కడ ఉన్నాయి. అదే నేల వరి మడుల నుంచి ఆహార అడవిగా మారింది. ప్రతి చిత్రం కింద రాసింది మేము దాన్ని చదివిన తీరు.","p","lede")}
  </div>
  <div class="sat" id="sat">
    <script type="application/json">{json.dumps(SAT_DATA, ensure_ascii=False)}</script>
    <div class="sat-view">
      <img class="sat-a" alt="" width="640" height="480"><img class="sat-b" alt="" hidden width="640" height="480"><img class="sat-fade" alt="" aria-hidden="true" width="640" height="480">
      <svg viewBox="0 0 640 480" preserveAspectRatio="none" aria-hidden="true"></svg>
      <div class="sat-split" hidden><button class="sat-knob" type="button" aria-label="Move the line between the two years (arrow keys)">⇆</button></div>
      <div class="stamp"></div><div class="stamp r" hidden></div>
    </div>
    <div class="sat-side">
      <div class="rowL"><p class="row-l"></p><div class="chips"></div></div>
      <div class="rowR" hidden><p class="row-l">{t("Right","కుడి")}</p><div class="chips"></div></div>
      <div class="note" aria-live="polite"></div>
      <div class="tools"><button class="chip play" type="button" aria-pressed="false">{t("Play","ఆడించు")}</button>
        <label><input type="checkbox" id="sat-cmp"> {t("Compare two years","రెండు సంవత్సరాలు పోల్చండి")}</label>
        <label><input type="checkbox" id="sat-marks" checked> {t("Outline","హద్దు")}</label></div>
      {t("Yellow line: the farm, traced on the 2023 picture.","పసుపు గీత: 2023 చిత్రంపై గీసిన పొలం హద్దు.","p","fine")}
    </div>
  </div>
  {t('Pictures from the past versions of Esri’s World Imagery map (<a href="https://livingatlas.arcgis.com/wayback/">Esri World Imagery Wayback</a>), © GeoEye, Maxar and Vantor. Dates and satellites come from each picture’s own record; each is placed to within 5 to 25 m.',
     'ఎస్రీ వరల్డ్ ఇమేజరీ మ్యాప్ పాత వెర్షన్ల నుంచి చిత్రాలు (<a href="https://livingatlas.arcgis.com/wayback/">Esri World Imagery Wayback</a>), © GeoEye, Maxar, Vantor. తేదీలు, ఉపగ్రహాలు ప్రతి చిత్రం రికార్డు నుంచి; ప్రతి చిత్రం 5 నుంచి 25 మీటర్ల లోపు ఖచ్చితత్వంతో ఉంటుంది.',"p","fine")}
</div>
<section><div class="wrap two">
  <div>
    {t("What the satellites measured","ఉపగ్రహాలు కొలిచింది","h2")}
    {t('Between the sharp pictures, the Sentinel-2 satellites pass every few days and measure how green each 10 m square is (NDVI: about 0.1 for bare ground, 0.6 to 0.9 for a full crop or dense trees, <a href="https://usgs.gov/land-resources/eros/phenology/science/ndvi-foundation-remote-sensing-phenology">USGS</a>).',
       'స్పష్టమైన చిత్రాల మధ్య కాలంలో సెంటినెల్-2 ఉపగ్రహాలు కొన్ని రోజులకోసారి వెళ్తూ, ప్రతి 10 మీటర్ల చతురస్రం ఎంత పచ్చగా ఉందో కొలుస్తాయి (NDVI: ఖాళీ నేలకు సుమారు 0.1, నిండు పంట లేదా దట్టమైన చెట్లకు 0.6 నుంచి 0.9, <a href="https://usgs.gov/land-resources/eros/phenology/science/ndvi-foundation-remote-sensing-phenology">USGS</a>).',"p","sub")}
    <ul style="display:grid;gap:12px;padding-left:1.2rem;margin:0">
      {t("<b>Paddy until late 2021.</b> From 2017 to November 2021 the farm’s greenness rose and fell with the paddy round it, twice a year. From December 2021 it went its own way.",
         "<b>2021 చివరి వరకు వరి.</b> 2017 నుంచి 2021 నవంబరు వరకు పొలం పచ్చదనం చుట్టూ ఉన్న వరితో పాటే ఏడాదికి రెండుసార్లు పెరిగి తగ్గింది. 2021 డిసెంబరు నుంచి అది తన దారిన తాను వెళ్ళింది.","li")}
      {t("<b>Green in the dry season since 2022.</b> In April and May, when the fields round it are bare at about 0.2, the farm has averaged between 0.35 and 0.51 each year.",
         "<b>2022 నుంచి వేసవిలోనూ పచ్చగా.</b> ఏప్రిల్, మే నెలల్లో చుట్టూ పొలాలు సుమారు 0.2 వద్ద ఖాళీగా ఉన్నప్పుడు, పొలం ప్రతి ఏడాది సగటున 0.35 నుంచి 0.51 మధ్య ఉంది.","li")}
      {t("<b>The cheruvu keeps its distance.</b> In clear passes since 2017, its open water came no closer than about 375 m to the farm, on 20 December 2025. A flood under cloud would not show.",
         "<b>చెరువు దూరంగానే ఉంది.</b> 2017 నుంచి మబ్బులు లేని చిత్రాల్లో, చెరువు నీరు పొలానికి సుమారు 375 మీటర్ల కంటే దగ్గరగా రాలేదు (20 డిసెంబరు 2025న). మబ్బుల కింద వచ్చిన వరద కనిపించదు.","li")}
    </ul>
  </div>
  <figure class="fig chart">
    {t("Greenness in April and May","ఏప్రిల్, మే నెలల్లో పచ్చదనం","h3")}
    <div style="margin-top:12px">{chart()}</div>
    <div class="key"><span><i style="background:var(--leaf)"></i>{t("the farm","పొలం")}</span><span><i style="background:var(--clay);opacity:.75"></i>{t("the fields round it (0.19–0.26)","చుట్టూ పొలాలు (0.19–0.26)")}</span></div>
    <figcaption>{t("Contains modified Copernicus Sentinel data 2017–2026, from Element 84 Earth Search; worked out by Nelamedha.","మార్చిన కోపర్నికస్ సెంటినెల్ డేటా 2017–2026, Element 84 Earth Search నుంచి; లెక్కలు నేలమేధ చేసినవి.")}</figcaption>
  </figure>
</div></section>
<section><div class="wrap two">
  <div>
    {t("Where it is","ఎక్కడ ఉంది","h2")}
    {t("The farm sits beside a cheruvu in paddy country, where most of the year’s rain falls between June and September. The west part, by the track, is low and holds water; the rest is higher ground. Visitors are welcome by arrangement.",
       "పొలం వరి పండే ప్రాంతంలో ఒక చెరువు పక్కన ఉంది; ఇక్కడ ఏడాది వర్షంలో ఎక్కువ భాగం జూన్ నుంచి సెప్టెంబరు మధ్య పడుతుంది. దారి పక్కన ఉన్న పడమటి భాగం పల్లంగా ఉండి నీరు నిలుస్తుంది; మిగతాది ఎత్తైన నేల. ముందుగా చెప్పి రావాలనుకునేవారికి స్వాగతం.","p","sub")}
  </div>
  <dl class="facts">
    <div><dt>{t("Village","గ్రామం")}</dt><dd>{t("Ganugabanda","గానుగబండ")}</dd></div>
    <div><dt>{t("Mandal","మండలం")}</dt><dd>{t("Garidepally","గరిడేపల్లి")}</dd></div>
    <div><dt>{t("District","జిల్లా")}</dt><dd>{t("Suryapet, Telangana","సూర్యాపేట, తెలంగాణ")}</dd></div>
    <div><dt>{t("Beside","పక్కన")}</dt><dd>{t("Yathavakilla Cheruvu","యతవకిళ్ల చెరువు")}</dd></div>
    <div style="grid-column:1/-1"><dt>{t("On the map","మ్యాప్‌లో")}</dt><dd><a href="https://www.openstreetmap.org/?mlat=16.83333&amp;mlon=79.77910#map=16/16.83333/79.77910">16.8333° N, 79.7791° E ↗</a></dd></div>
  </dl>
</div></section>
'''
farm = farm.replace('{pre}', pre) + contact() + footer(pre) + '<script>nmSat("sat")</script>\n'
page('farm/index.html', farm)

# ---------- projects ----------
PROJ = [
 ('forest', 'ok', 'Growing since 2022', '2022 నుంచి పెరుగుతోంది', 'Food forest', 'ఆహార అడవి',
  'Paddy until late 2021. Since then, trees in rows across the farm, with the canopy closing over most of it by April 2025.',
  '2021 చివరి వరకు వరి. అప్పటి నుంచి పొలమంతా వరుసల్లో చెట్లు; 2025 ఏప్రిల్ నాటికి దాదాపు పొలమంతా చెట్ల పందిరి కమ్ముకుంది.',
  'Next: map every tree and its layer, and measure the soil moisture under the canopy.',
  'తదుపరి: ప్రతి చెట్టునూ, దాని పొరనూ మ్యాప్ చేయడం; పందిరి కింద నేల తేమను కొలవడం.',
  '../farm/', 'The farm from above →', 'పైనుంచి పొలం →'),
 ('house', 'wip', 'Designed, build next', 'రూపకల్పన పూర్తి, తర్వాత నిర్మాణం', 'The earth house', 'మట్టి ఇల్లు',
  'A one-bedroom house of about 750 sq ft with no cement anywhere: one wall each of cob, adobe and lime-stabilised pressed blocks, under a Mangalore-tile roof on timber. Rain from the roof, solar with batteries, biogas for cooking.',
  'సుమారు 750 చ.అ. ఒక పడకగది ఇల్లు, ఎక్కడా సిమెంటు లేకుండా: మట్టి ముద్దల గోడ, ఎండబెట్టిన మట్టి ఇటుకలు, సున్నం కలిపి ఒత్తిన బ్లాకులు, ఒక్కో రకం ఒక్కో గోడ; కలప మీద మంగళూరు పెంకుల పైకప్పు. పైకప్పు వాన నీరు, బ్యాటరీలతో సౌర శక్తి, వంటకు బయోగ్యాస్.',
  'Next: settle the site on the higher ground, test the soil, and build.',
  'తదుపరి: ఎత్తైన నేలపై స్థలం ఖరారు, మట్టి పరీక్ష, నిర్మాణం.',
  'https://rohithreddy1095.github.io/earth-illustrated/#farmhouse', 'The plan and the 3D build-along ↗', 'ప్రణాళిక, 3D నిర్మాణం ↗'),
 ('clawmesh', 'wip', 'Bench prototype', 'బెంచ్ నమూనా', 'ClawMesh', 'క్లామెష్',
  'Software that ties a laptop, a Jetson, sensors and pumps into one mesh. Capacitive soil-moisture sensors already read through an ADS1115 converter on a Jetson Orin Nano. Every action carries who asked for it and who approved it.',
  'ల్యాప్‌టాప్, జెట్సన్, సెన్సర్లు, పంపులను ఒకే మెష్‌గా కలిపే సాఫ్ట్‌వేర్. జెట్సన్ ఓరిన్ నానోపై ADS1115 కన్వర్టర్ ద్వారా నేల తేమ సెన్సర్లు ఇప్పటికే చదువుతున్నాయి. ప్రతి పనికీ ఎవరు అడిగారో, ఎవరు ఆమోదించారో రికార్డు ఉంటుంది.',
  'Next: the first node out in the field on the farm.', 'తదుపరి: పొలంలో మొదటి నోడ్.',
  'https://github.com/rohithreddy1095/clawmesh', 'Code on GitHub ↗', 'GitHubలో కోడ్ ↗'),
 ('lakes', 'ok', 'Working proof of concept', 'పనిచేసే నమూనా', 'Lakes & Land', 'చెరువులు & నేల',
  'Pick any lake or tank and get a satellite report: how much of it no longer fills, what is on that ground now, and a year-by-year replay since the 1980s or 1990s. In English and Telugu, on free open data.',
  'ఏ చెరువునైనా ఎంచుకోండి, ఉపగ్రహ నివేదిక వస్తుంది: దానిలో ఎంత భాగం ఇప్పుడు నిండటం లేదు, ఆ నేలపై ఇప్పుడు ఏముంది, 1980లు లేదా 1990ల నుంచి ఏడాది వారీగా. ఇంగ్లీషు, తెలుగులో, ఉచిత ఓపెన్ డేటాతో.',
  'Next: a report for the cheruvu beside the farm.', 'తదుపరి: పొలం పక్కన ఉన్న చెరువుకు నివేదిక.',
  'https://github.com/rohithreddy1095/lakes-and-land', 'Code on GitHub ↗', 'GitHubలో కోడ్ ↗'),
 ('earth', 'ok', 'Published', 'ప్రచురించబడింది', 'Earth, Illustrated', 'ఎర్త్, ఇలస్ట్రేటెడ్',
  'An interactive reference to natural building: walls, roofs, foundations and the farmhouse, every number with its source.',
  'సహజ నిర్మాణంపై ఇంటరాక్టివ్ గైడ్: గోడలు, పైకప్పులు, పునాదులు, ఫాంహౌస్; ప్రతి సంఖ్యకూ దాని ఆధారం.',
  'Next: keep adding what the house teaches us as it goes up.', 'తదుపరి: ఇల్లు కడుతున్నప్పుడు నేర్చుకున్నది జోడిస్తూ ఉండటం.',
  'https://rohithreddy1095.github.io/earth-illustrated/', 'Read it ↗', 'చదవండి ↗'),
]
pre = '../'
proj = head(pre, 'Projects · Nelamedha', 'పనులు · నేలమేధ', 'What Nelamedha is working on: the food forest, the earth house, ClawMesh, Lakes & Land and Earth, Illustrated, with a log of progress.', 'projects/')
proj += header(pre, 'projects/')
cards = ''.join(f'''<article class="card" id="{i}"><span class="pill {s}">{t(se, st)}</span>{t(he, ht, "h3")}{t(pe, pt, "p")}{t(ne, nt, "p", attrs=' style="color:var(--muted)"')}<p class="more"><a href="{href}">{t(le, lt)}</a></p></article>'''
                for i, s, se, st, he, ht, pe, pt, ne, nt, href, le, lt in PROJ)
proj += f'''<div class="wrap">
  <div class="page-head">
    {t("Projects","పనులు","p","kicker")}
    {t("What we are working on","మేము చేస్తున్న పనులు","h1")}
    {t("Five pieces of work, from the trees in the ground to the code that watches them. Each says where it stands and what comes next.",
       "నేలలోని చెట్ల నుంచి వాటిని చూసుకునే కోడ్ వరకు ఐదు పనులు. ప్రతిదీ ఎక్కడ ఉందో, తర్వాత ఏమిటో చెబుతుంది.","p","lede")}
  </div>
  <div class="three" style="padding-bottom:56px">{cards}</div>
</div>
<section id="progress"><div class="wrap two">
  <div>
    {t("Progress","పురోగతి","h2")}
    {t("What has happened on the farm and in the work, newest first. The early entries come from the satellite pictures.",
       "పొలంలో, పనిలో జరిగింది, కొత్తది ముందు. మొదటి వివరాలు ఉపగ్రహ చిత్రాల నుంచి.","p","sub")}
  </div>
  {log_html(LOG)}
</div></section>
'''
proj = proj.replace('{pre}', pre) + contact() + footer(pre)
page('projects/index.html', proj)

# ---------- research ----------
GH = f'''<svg viewBox="0 0 720 400" role="img" aria-label="A greenhouse cut open: shade net and misters overhead, a fan at one end, plant beds with soil sensors and drip lines, a camera, small sensor nodes, a computer box, a solar panel and a water tank.">
  <rect width="720" height="400" fill="#DCE7E4"/>
  <rect y="300" width="720" height="100" fill="#6B4A2E"/><rect y="300" width="720" height="10" fill="#4E7A45"/>
  <path d="M90 300 V170 Q250 70 410 170 V300" fill="#F4F7F2" fill-opacity=".55" stroke="#4B5A50" stroke-width="4"/>
  <path d="M96 168 Q250 76 404 168" fill="none" stroke="#2F3B33" stroke-width="7" stroke-dasharray="3 5" opacity=".7"/>
  <g fill="#2F5D7C"><circle cx="170" cy="150" r="5"/><circle cx="250" cy="122" r="5"/><circle cx="330" cy="150" r="5"/></g>
  <g stroke="#7FB3D5" stroke-width="2" stroke-linecap="round"><path d="M164 160l-8 14M170 160v16M176 160l8 14M244 132l-8 14M250 132v16M256 132l8 14M324 160l-8 14M330 160v16M336 160l8 14"/></g>
  <rect x="384" y="196" width="20" height="44" rx="3" fill="#4B5A50"/><circle cx="394" cy="218" r="8" fill="none" stroke="#DCE7E4" stroke-width="2"/>
  <g><rect x="120" y="262" width="250" height="38" fill="#5A3A22"/>
    <g fill="#3F6B3A"><path d="M140 262c0-18 8-26 14-30 4 12 0 22-14 30z"/><path d="M185 262c0-22 10-32 16-36 4 14 0 28-16 36z"/><path d="M232 262c0-18 8-26 14-30 4 12 0 22-14 30z"/><path d="M278 262c0-22 10-32 16-36 4 14 0 28-16 36z"/><path d="M325 262c0-18 8-26 14-30 4 12 0 22-14 30z"/></g>
    <path d="M120 266 H370" stroke="#2F5D7C" stroke-width="3"/>
    <g fill="#A8562B"><rect x="206" y="270" width="8" height="24" rx="2"/><rect x="300" y="270" width="8" height="24" rx="2"/></g></g>
  <rect x="232" y="186" width="24" height="16" rx="3" fill="#2A211A"/><circle cx="244" cy="194" r="4.5" fill="#8DB8D6"/>
  <g fill="#2F5D7C"><rect x="150" y="226" width="22" height="16" rx="3"/><rect x="330" y="226" width="22" height="16" rx="3"/></g>
  <rect x="470" y="216" width="56" height="44" rx="5" fill="#2A211A"/><rect x="478" y="226" width="40" height="6" rx="2" fill="#8FBF7F"/><rect x="478" y="238" width="24" height="6" rx="2" fill="#8DB8D6"/>
  <path d="M498 260 V300" stroke="#2A211A" stroke-width="4"/>
  <g stroke="#2F5D7C" stroke-width="2" fill="none" stroke-dasharray="5 4"><path d="M172 234 H470"/><path d="M352 234 H470"/></g>
  <g><path d="M560 300 V150" stroke="#4B5A50" stroke-width="5"/><path d="M520 150 L610 124 L620 156 L530 182Z" fill="#2E4A7A" stroke="#DCE7E4" stroke-width="2"/></g>
  <path d="M560 210 H526" stroke="#A8562B" stroke-width="2.5"/>
  <g><rect x="620" y="210" width="60" height="90" rx="6" fill="#4F86B8"/><path d="M620 236 H680" stroke="#DCE7E4" stroke-width="2" opacity=".6"/></g>
  <path d="M620 290 H560 Q540 290 540 296 H370" stroke="#2F5D7C" stroke-width="3" fill="none"/>
  <g font-family="JetBrains Mono, monospace" font-size="20" fill="#2A211A">
    {"".join(f'<text x="{x}" y="{y}"{(" text-anchor=" + chr(34) + a + chr(34)) if a else ""} class="en">{en}</text><text x="{x}" y="{y}"{(" text-anchor=" + chr(34) + a + chr(34)) if a else ""} class="te" style="font-family:Noto Sans Telugu,sans-serif">{te}</text>' for x, y, a, en, te in [
      (250, 56, 'middle', 'shade net and misters', 'నీడ వల, పొగమంచు స్ప్రేలు'), (394, 186, 'middle', 'fan', 'ఫ్యాన్'),
      (262, 182, '', 'camera', 'కెమెరా'), (100, 218, '', 'sensor node', 'సెన్సర్ నోడ్'),
      (130, 338, '', 'soil sensors and drip line', 'నేల సెన్సర్లు, డ్రిప్ లైన్'), (498, 204, 'middle', 'computer', 'కంప్యూటర్'),
      (570, 108, 'middle', 'solar panel', 'సౌర ఫలకం'), (650, 200, 'middle', 'water tank', 'నీటి ట్యాంకు')])}
  </g>
</svg>'''
PH = [('done', 'On the bench', 'బెంచ్‌పై', 'Soil-moisture sensors reading through a Jetson. Done.', 'జెట్సన్ ద్వారా నేల తేమ సెన్సర్లు. పూర్తయింది.'),
      ('now', 'One nursery bed', 'ఒక నర్సరీ మడి', 'Drip line, a valve and sensors on a single bed, watered by the system with a person approving.', 'ఒక మడిపై డ్రిప్ లైన్, వాల్వ్, సెన్సర్లు; మనిషి ఆమోదంతో వ్యవస్థే నీళ్లు పెడుతుంది.'),
      ('', 'The greenhouse', 'గ్రీన్‌హౌస్', 'A shade-net house with misters, fans, shade control and cameras.', 'పొగమంచు స్ప్రేలు, ఫ్యాన్లు, నీడ నియంత్రణ, కెమెరాలతో నీడ వల ఇల్లు.'),
      ('', 'Out into the forest', 'అడవిలోకి', 'The same nodes spread through the food forest.', 'అవే నోడ్లు ఆహార అడవి అంతటా.')]
Q = [('How much water does a nursery bed need in a Suryapet summer, day by day?', 'సూర్యాపేట వేసవిలో ఒక నర్సరీ మడికి రోజుకు ఎంత నీరు కావాలి?'),
     ('Can a camera and a small model spot stress before the leaves show it?', 'ఆకులు చూపించక ముందే ఒక కెమెరా, చిన్న మోడల్ మొక్క ఒత్తిడిని గుర్తించగలవా?'),
     ('Which jobs can run on their own, and which should always wait for a person?', 'ఏ పనులు వాటంతట అవే జరగవచ్చు, ఏవి ఎప్పుడూ మనిషి కోసం ఆగాలి?'),
     ('Can it all run on the sun, with no internet?', 'ఇదంతా ఇంటర్నెట్ లేకుండా, సౌర శక్తితో నడవగలదా?')]
DIR = [('idea', 'Idea', 'ఆలోచన', 'Walls that measure themselves', 'తమను తామే కొలుచుకునే గోడలు',
        'The house will have one wall each of cob, adobe and pressed blocks. Sensors inside each can show which keeps the rooms coolest through a summer.',
        'ఇంట్లో మట్టి ముద్ద, మట్టి ఇటుక, ఒత్తిన బ్లాకు, ఒక్కో రకం ఒక్కో గోడ ఉంటుంది. ప్రతి గోడ లోపలి సెన్సర్లు, వేసవిలో ఏ గోడ గదులను ఎక్కువ చల్లగా ఉంచుతుందో చూపగలవు.'),
       ('idea', 'Idea', 'ఆలోచన', 'Counting the carbon', 'కార్బన్ లెక్క',
        'Bheema bamboo covers about a third of the farm, with the food forest on the rest. We want to measure how much carbon they really hold, with sample plots, sensors and satellites, and find out whether small farms like ours can earn carbon credits.',
        'పొలంలో దాదాపు మూడో వంతు భీమ వెదురు, మిగతా భాగంలో ఆహార అడవి ఉన్నాయి. అవి నిజంగా ఎంత కార్బన్‌ను నిల్వ చేస్తాయో నమూనా ప్లాట్లు, సెన్సర్లు, ఉపగ్రహాలతో కొలవాలనుకుంటున్నాం; మా లాంటి చిన్న పొలాలు కార్బన్ క్రెడిట్లు పొందగలవో తెలుసుకోవాలనుకుంటున్నాం.'),
       ('wip', 'Starting', 'మొదలవుతోంది', 'Moisture under the forest', 'అడవి కింద తేమ',
        'A mesh of soil sensors under the canopy, to water only where and when the roots need it.',
        'పందిరి కింద నేల సెన్సర్ల మెష్, వేర్లకు ఎక్కడ, ఎప్పుడు అవసరమో అక్కడ మాత్రమే నీళ్లు పెట్టడానికి.'),
       ('idea', 'Idea', 'ఆలోచన', 'Every litre, all year', 'ఏడాది పొడవునా ప్రతి లీటరు',
        'Rain on the roof, the tank and the pump: measuring the water the farm takes in and the water it uses.',
        'పైకప్పుపై వాన, ట్యాంకు, పంపు: పొలానికి వచ్చే నీటినీ, వాడే నీటినీ కొలవడం.'),
       ('ok', 'Running', 'నడుస్తోంది', 'Watching from space', 'అంతరిక్షం నుంచి చూడటం',
        'Satellite passes every few days for the farm and the cheruvu beside it, with Lakes & Land.',
        'చెరువులు & నేల ద్వారా, కొన్ని రోజులకోసారి పొలం, పక్కనున్న చెరువు ఉపగ్రహ చిత్రాలు.'),
       ('ok', 'Running', 'నడుస్తోంది', 'AI on small devices', 'చిన్న పరికరాలపై AI',
        'Language and vision models running offline on a Jetson in the field, so the farm does not depend on the internet.',
        'ఇంటర్నెట్‌పై ఆధారపడకుండా, పొలంలో జెట్సన్‌పై ఆఫ్‌లైన్‌గా నడిచే భాష, దృష్టి మోడళ్లు.')]
pre = '../'
res = head(pre, 'Research · Nelamedha', 'పరిశోధన · నేలమేధ', 'Research directions at Nelamedha: a greenhouse run by edge hardware, walls that measure themselves, soil moisture under the forest, water, satellites and AI on small devices.', 'research/')
res += header(pre, 'research/')
res += f'''<div class="wrap">
  <div class="page-head">
    {t("Research directions","పరిశోధన దిశలు","p","kicker")}
    {t("What we want to find out","మేము తెలుసుకోవాలనుకునేది","h1")}
    {t("Rural technology for natural farming and self-sustaining living: the questions we are working on, or about to. Each is tried on the farm first, with open hardware and open code.",
       "సహజ వ్యవసాయానికి, స్వయం సమృద్ధ జీవనానికి గ్రామీణ సాంకేతికత: మేము పని చేస్తున్న, లేదా త్వరలో మొదలుపెట్టే ప్రశ్నలు. ప్రతిదీ ముందు పొలంలోనే, ఓపెన్ హార్డ్‌వేర్, ఓపెన్ కోడ్‌తో ప్రయత్నిస్తాం.","p","lede")}
  </div>
</div>
<section id="greenhouse"><div class="wrap">
  <span class="pill wip">{t("Starting","మొదలవుతోంది")}</span>
  {t("A greenhouse that runs itself","తనంతట తాను నడిచే గ్రీన్‌హౌస్","h2", attrs=' style="margin-top:14px"')}
  {t("A greenhouse is the easiest place to start: the space is small, and everything going in and out can be measured. Sensors report, a small computer on the farm decides, valves, misters and fans act, and anything risky waits for a person to approve it. What works here moves out to the food forest.",
     "మొదలుపెట్టడానికి గ్రీన్‌హౌస్ సులువైన చోటు: స్థలం చిన్నది, లోపలికి వెళ్ళేదీ బయటకు వచ్చేదీ అంతా కొలవవచ్చు. సెన్సర్లు చెబుతాయి, పొలంలోని చిన్న కంప్యూటర్ నిర్ణయిస్తుంది, వాల్వులు, స్ప్రేలు, ఫ్యాన్లు పని చేస్తాయి; ప్రమాదం ఉన్న పని మనిషి ఆమోదం కోసం ఆగుతుంది. ఇక్కడ పనిచేసింది ఆహార అడవిలోకి వెళ్తుంది.","p","sub")}
  <figure class="fig">{GH}<figcaption>{t("A sketch of the idea, not a design yet.","ఆలోచన చిత్రం మాత్రమే, ఇంకా డిజైన్ కాదు.")}</figcaption></figure>
  <div style="margin-top:36px">{t("How it grows","ఎలా ఎదుగుతుంది","h3")}</div>
  <ol class="phases" style="margin-top:14px">{"".join(f'<li class="{c}">{t(he, ht, "h3")}{t(pe, pt, "p")}</li>' for c, he, ht, pe, pt in PH)}</ol>
  <div style="margin-top:36px">{t("Questions it should answer","ఇది జవాబివ్వాల్సిన ప్రశ్నలు","h3")}</div>
  <ul style="display:grid;gap:8px;padding-left:1.2rem;margin:14px 0 0">{"".join(t(e, te_, "li") for e, te_ in Q)}</ul>
</div></section>
<section><div class="wrap">
  {t("Other directions","ఇతర దిశలు","h2")}
  {t("Smaller questions running alongside, all tied to the same piece of ground.","వీటితో పాటే నడిచే చిన్న ప్రశ్నలు, అన్నీ అదే నేలకు సంబంధించినవి.","p","sub")}
  <div class="three">{"".join(f'<article class="card"><span class="pill {c}">{t(se, st)}</span>{t(he, ht, "h3")}{t(pe, pt, "p")}</article>' for c, se, st, he, ht, pe, pt in DIR)}</div>
</div></section>
<section><div class="wrap two">
  <div>
    {t("Research with us","మాతో పరిశోధన చేయండి","h2")}
    {t("Students, researchers and builders are welcome to try ideas here, on real ground. Write to us with what you would like to test.",
       "విద్యార్థులు, పరిశోధకులు, నిర్మాణకారులు ఇక్కడ నిజమైన నేలపై తమ ఆలోచనలు ప్రయత్నించడానికి స్వాగతం. మీరు ఏమి పరీక్షించాలనుకుంటున్నారో మాకు రాయండి.","p","sub")}
  </div>
  <p style="display:flex;flex-wrap:wrap;gap:12px"><a class="btn wa en" href="{WA_EN}" target="_blank" rel="noopener">{WA_ICON}Message on WhatsApp</a><a class="btn wa te" lang="te" href="{WA_TE}" target="_blank" rel="noopener">{WA_ICON}వాట్సాప్‌లో మెసేజ్ చేయండి</a><a class="btn" href="#contact" style="background:var(--paper-2);color:var(--ink);border:1px solid var(--line)">{t("Email or call","ఈమెయిల్ లేదా ఫోన్")}</a></p>
</div></section>
'''
res = res.replace('{pre}', pre) + contact() + footer(pre)
page('research/index.html', res)

# ---------- photos ----------
pre = '../'
gal = head(pre, 'Photos · Nelamedha', 'ఫోటోలు · నేలమేధ', 'Photographs of Mr Green Farms over the years: the food forest, the land and the work.', 'gallery/')
gal += header(pre, 'gallery/')
gal += f'''<div class="wrap">
  <div class="page-head">
    {t("Photos","ఫోటోలు","p","kicker")}
    {t("The farm, on the ground","నేల మీద నుంచి పొలం","h1")}
    {t("Photographs from the farm, newest first, added as the years go by. Tap one to see it large.",
       "పొలం ఫోటోలు, కొత్తవి ముందు, ఏళ్లు గడిచే కొద్దీ జోడిస్తూ ఉంటాం. పెద్దగా చూడటానికి ఫోటోపై నొక్కండి.","p","lede")}
  </div>
  <div id="gallery" class="gallery" data-src="photos.json" aria-live="polite">
    {t("Loading photos…","ఫోటోలు వస్తున్నాయి…","p","fine")}
  </div>
  <template id="gallery-empty">{t("The first photos from the farm are on their way. Until then, see the farm from above on the <a href='../farm/'>farm page</a>.",
     "పొలం నుంచి మొదటి ఫోటోలు త్వరలో వస్తాయి. అప్పటి వరకు <a href='../farm/'>పొలం పేజీ</a>లో పైనుంచి పొలాన్ని చూడండి.","p","sub")}</template>
</div>
<dialog class="lightbox" id="lightbox" aria-label="Photo">
  <figure><img alt=""><figcaption></figcaption></figure>
  <button class="lb-x" type="button" aria-label="Close">×</button>
  <button class="lb-p" type="button" aria-label="Previous photo">‹</button>
  <button class="lb-n" type="button" aria-label="Next photo">›</button>
</dialog>
<div style="height:56px"></div>
'''
gal = gal.replace('{pre}', pre) + contact() + footer(pre) + '<script>nmGallery("gallery")</script>\n'
page('gallery/index.html', gal)
