import re,sys,json
S,P=sys.argv[1],sys.argv[2]
t=open(S+'/template.html').read(); data=json.load(open(S+'/data.json'))
sec=lambda i: re.search(r'  <section class="panel" id="%s".*?</section>\n'%i,t,re.S).group(0)
foot=re.search(r'<footer>.*?</footer>',t,re.S).group(0)
SRC_F='<p><b>Source.</b> <a href="https://ssd-api.jpl.nasa.gov/doc/fireball.html">NASA/JPL CNEOS Fireball Data API</a> (US Government work, public domain), retrieved 6 Nov 2026. 888 of 1,074 reported events have a location and are shown.</p>\n  <p><b>Notes.</b> These are bolides that exploded in the atmosphere, not ground impacts, so they leave no crater. Impact energy is NASA\'s estimate from the radiated light. Sensor coverage has changed over time, so the yearly counts are not a clean trend.</p>'
SRC_C='<p><b>Source.</b> <a href="https://en.wikipedia.org/wiki/List_of_impact_structures_on_Earth">Wikipedia, List of impact structures on Earth</a> (CC BY-SA 4.0). 195 of 204 confirmed structures have coordinates and are shown.</p>\n  <p><b>Notes.</b> Crater ages are uncertain. When only a range is known, the crater is placed at the midpoint. When only an upper limit is known (e.g. "less than 60 Ma"), it is placed at that limit, so it may be younger than shown. Some locations are approximate.</p>'
cfg={
 'craters':dict(other='fireballs',title='Impact Craters Through Time',h1='Impact craters through geologic time',
   intro='The scars that rocks from space have left on Earth over two billion years, from Vredefort in South Africa to the craters of the last 11,700 years. Press play to watch them appear period by period.',
   src=SRC_C,keep=['craters','craterFrames']),
 'fireballs':dict(other='craters',title='Fireballs Since 1988',h1='Fireballs in Earth\'s atmosphere, 1988 to today',
   intro='Every year, small asteroids explode high in the atmosphere. US government sensors have located 888 of them since 1988, including the 441-kiloton Chelyabinsk airburst in 2013. Press play to watch them year by year.',
   src=SRC_F,keep=['fireballs','years']),
}
for k,c in cfg.items():
    h=t.replace(sec(c['other']),'')
    h=re.sub(r'<title>.*?</title>','<title>%s</title>'%c['title'],h)
    h=re.sub(r'    <h2 id="\w+-h">.*?</h2>\n','',h); h=h.replace('aria-labelledby="%s-h"'%k,'aria-label="%s"'%c['h1'].replace("'",'\u2019'))
    h=re.sub(r'<h1>.*?</h1>','<h1>%s</h1>'%c['h1'],h)
    h=re.sub(r'(<header>.*?<p>).*?(</p>)',lambda m:m.group(1)+c['intro']+m.group(2),h,flags=re.S)
    h=h.replace(foot,'<footer>\n  '+c['src']+'\n</footer>')
    h=h.replace('@media (min-width: 1100px) { .grid { grid-template-columns: 1fr 1fr; } }\n','')
    h=h.replace('main { max-width: 1480px;','main { max-width: 1200px;')
    h=h.replace('.map { height: 380px; }','.map { height: 560px; }\n@media (max-width: 700px) { .map { height: 320px; } }')
    h=h.replace('const craterPts = DATA.craters.map','const craterPts = (DATA.craters || []).map')
    h=h.replace('const fireballPts = DATA.fireballs.map','const fireballPts = (DATA.fireballs || []).map')
    h=h.replace('let topo;','PANELS.splice(0, PANELS.length, ...PANELS.filter(p => p.id === %s));\nlet topo;'%json.dumps(k))
    h=h.replace("DATA.craterFrames.map(","(DATA.craterFrames || []).map(").replace("frames: DATA.years.map(","frames: (DATA.years || []).map(")
    d={x:data[x] for x in c['keep']}
    h=h.replace('/*DATA*/null',json.dumps(d,separators=(',',':')))
    assert c['other']+'-map' not in h
    open(f'{P}/{k}.html','w').write(h); print(k,len(h))
    GREY = ('\n<style>/* grey variant: earlier impacts fade to slate, controls neutral */\n'
      ':root { --past: #7d8696; --past-alpha: 0.55; --crater: #4f5768; --fireball: #4f5768; }\n'
      '@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --past: #8c95a6; --past-alpha: 0.5; --crater: #b4bcc9; --fireball: #b4bcc9; } }\n'
      ':root[data-theme="dark"] { --past: #8c95a6; --past-alpha: 0.5; --crater: #b4bcc9; --fireball: #b4bcc9; }\n</style>\n</head>')
    g=h.replace('</head>',GREY,1).replace('<title>'+c['title']+'</title>','<title>'+c['title']+' (Grey)</title>')
    open(f'{P}/{k}-grey.html','w').write(g); print(k+'-grey',len(g))
