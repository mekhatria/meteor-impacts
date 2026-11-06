import json,sys,collections
S=sys.argv[1]; P=sys.argv[2]
c=json.load(open(P+'/craters.json'))
periods=[("Archean",4000,2500),("Paleoproterozoic",2500,1600),("Mesoproterozoic",1600,1000),("Neoproterozoic",1000,538.8),("Cambrian",538.8,485.4),("Ordovician",485.4,443.8),("Silurian",443.8,419.2),("Devonian",419.2,358.9),("Carboniferous",358.9,298.9),("Permian",298.9,251.9),("Triassic",251.9,201.4),("Jurassic",201.4,145),("Cretaceous",145,66),("Paleogene",66,23.03),("Neogene",23.03,2.58),("Pleistocene",2.58,0.0117),("Holocene",0.0117,0)]
cr=[];skip=collections.Counter()
for r in c:
    if r['lat'] is None: skip['no coords']+=1; continue
    if r['age_ma'] is not None: a=r['age_ma'];how='stated'
    elif r['age_min_ma'] is not None and r['age_max_ma'] is not None: a=(r['age_min_ma']+r['age_max_ma'])/2;how='midpoint of range'
    elif r['age_max_ma'] is not None: a=r['age_max_ma'];how='upper bound (could be younger)'
    else: skip['no age']+=1; continue
    f=next(i for i,(n,s,e) in enumerate(periods) if s>a>=e)
    cr.append(dict(name=r['name'],country=r['country'],lat=r['lat'],lon=r['lon'],z=r['diameter_km'],age=a,ageText=r['age_text'],how=how,f=f,approx=r['coord_source'] and 'approximate' in r['coord_source']))
used=sorted(set(x['f'] for x in cr)); remap={o:i for i,o in enumerate(used)}
for x in cr: x['f']=remap[x['f']]
def rng(s,e):
    if e==0: return "last 11,700 years"
    if s<10: return f"{s*1000:,.0f} thousand to {e*1000:,.0f} thousand years ago" if s<1 else f"{s:g} million to {e*1000:,.1f} thousand years ago"
    return f"{s:,g} to {e:,g} million years ago"
cf=[dict(label=periods[o][0],range=("more than 2,500 million years ago" if periods[o][0]=="Archean" else rng(periods[o][1],periods[o][2]))) for o in used]
print('craters',len(cr),dict(skip),[ (f['label'],sum(x['f']==i for x in cr)) for i,f in enumerate(cf)])
d=json.load(open(P+'/cneos_fireballs_raw.json')); F=d['fields']
fb=[]
for row in d['data']:
    r=dict(zip(F,row))
    if r['lat'] is None or r['impact-e'] is None: continue
    lat=float(r['lat'])*(1 if r['lat-dir']=='N' else -1); lon=float(r['lon'])*(1 if r['lon-dir']=='E' else -1)
    fb.append(dict(date=r['date'],y=int(r['date'][:4]),lat=lat,lon=lon,z=float(r['impact-e']),rad=float(r['energy']),alt=float(r['alt']) if r['alt'] else None,vel=float(r['vel']) if r['vel'] else None))
fb.sort(key=lambda x:x['date'])
yrs=list(range(fb[0]['y'],fb[-1]['y']+1))
print('fireballs',len(fb),yrs[0],yrs[-1],'max',max(fb,key=lambda x:x['z']))
json.dump(dict(craters=cr,craterFrames=cf,fireballs=fb,years=yrs),open(S+'/data.json','w'),separators=(',',':'))
