"""Append seasonal imagery and photos for new places without replacing past selections."""
import json,re,html
from pathlib import Path
ROOT=Path(__file__).resolve().parent
primary=json.loads((ROOT/'photos.json').read_text())
galleries=json.loads((ROOT/'galleries.json').read_text())
def pick(query,pid,key,label):
 page=json.loads(Path(f'/tmp/roof-photo-{query}.json').read_text())['query']['pages'][str(pid)]
 info=page['imageinfo'][0];m=info['extmetadata']
 clean=lambda field:html.unescape(re.sub('<[^>]+>','',m.get(field,{}).get('value',''))).strip()
 return dict(title=page['title'].removeprefix('File:'),source_page=info['descriptionurl'],image_url=info.get('thumburl',info['url']).split('?')[0],original_url=info['url'],photographer=clean('Artist'),license=clean('LicenseShortName'),license_url=clean('LicenseUrl') or 'https://commons.wikimedia.org/wiki/Commons:Public_domain',description=clean('ImageDescription'),local_file=f'photos/{key}.jpg',modifications='Unaltered source thumbnail; displayed scaled without cropping.',captured_date=clean('DateTimeOriginal'),view_label=label,retrieved_date='2026-11-12')
new={
 'jeju':pick('jeju',120126680,'jeju','Courtyard & thatch'),
 'samoa':pick('samoa',22981067,'samoa','Open-sided fale'),
 'chickee':pick('chickee',150537918,'chickee','Historic view · 1960')}
for key,p in new.items():primary[key]=p;galleries[key]=[p]
winter=pick('shirakawa-winter',91838106,'shirakawa-winter','Winter · February')
galleries['shirakawa']=[p for p in galleries['shirakawa'] if p.get('view_label')!='Winter · February']+[winter]
galleries['shirakawa'][0].update(view_label='Autumn · roof detail',captured_date='2016-10-24',season_months=[9,10,11])
galleries['shirakawa'][1].update(view_label='Autumn · gable view',captured_date='2016-10-24',season_months=[9,10,11])
winter['season_months']=[12,1,2,3]
for name,data in [('photos.json',primary),('galleries.json',galleries)]:ROOT.joinpath(name).write_text(json.dumps(data,indent=2,ensure_ascii=False))
print(json.dumps([*new.values(),winter],indent=2,ensure_ascii=False))
