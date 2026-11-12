import json,re,html
from pathlib import Path
ROOT=Path(__file__).resolve().parent
primary=json.loads((ROOT/'photos.json').read_text())
additional={'shirakawa':77450013,'ghadames':153122337,'alberobello':166537913,'waerebo':175226943,'glaumbaer':156813092,'tulou':38135135,'taos':160055604,'holasovice':58156191}
galleries={k:[p] for k,p in primary.items()}
for key,pid in additional.items():
 src=Path('/tmp')/('roof-photo-search.json' if key=='shirakawa' else f'roof-photo-{key}.json')
 page=json.loads(src.read_text())['query']['pages'][str(pid)]
 info=page['imageinfo'][0]; meta=info['extmetadata']
 clean=lambda field:html.unescape(re.sub('<[^>]+>','',meta.get(field,{}).get('value',''))).strip()
 p=dict(title=page['title'].removeprefix('File:'),source_page=info['descriptionurl'],image_url=info.get('thumburl',info['url']).split('?')[0],original_url=info['url'],photographer=clean('Artist'),license=clean('LicenseShortName'),license_url=clean('LicenseUrl'),description=clean('ImageDescription'),local_file=f'photos/{key}-2.jpg',modifications='Unaltered Wikimedia thumbnail; displayed scaled to fit without cropping.',retrieved_date='2026-11-12')
 assert p['photographer'] and p['license_url']
 galleries[key].append(p)
(ROOT/'galleries.json').write_text(json.dumps(galleries,indent=2,ensure_ascii=False))
print('Selected 18 photos across ten locations.')
