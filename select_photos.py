import json,re,html
from pathlib import Path
ROOT=Path(__file__).resolve().parent
selections={'shirakawa':77449838,'ghadames':18054309,'alberobello':166537904,'waerebo':175226941,'glaumbaer':156425463,'hahoe':4555664,'bermuda':2947967,'tulou':38135133,'taos':160055593,'holasovice':58156203}
photos={}
for key,pageid in selections.items():
 src=Path('/tmp')/('roof-photo-search.json' if key=='shirakawa' else f'roof-photo-{key}.json')
 page=json.loads(src.read_text())['query']['pages'][str(pageid)]
 info=page['imageinfo'][0]; meta=info['extmetadata']
 clean=lambda field:html.unescape(re.sub('<[^>]+>','',meta.get(field,{}).get('value',''))).strip()
 photos[key]=dict(title=page['title'].removeprefix('File:'),source_page=info['descriptionurl'],image_url=info.get('thumburl',info['url']).split('?')[0],original_url=info['url'],photographer=clean('Artist'),license=clean('LicenseShortName'),license_url=clean('LicenseUrl'),description=clean('ImageDescription'),local_file=f'photos/{key}.jpg',modifications='Unaltered Wikimedia thumbnail; displayed scaled to fit without cropping.',retrieved_date='2026-11-12')
photos['bermuda']['photographer']='Aodhdubh (English Wikipedia)'
ROOT.joinpath('photos').mkdir(exist_ok=True)
ROOT.joinpath('photos.json').write_text(json.dumps(photos,indent=2,ensure_ascii=False))
print(json.dumps({k:{'photographer':p['photographer'],'url':p['image_url']} for k,p in photos.items()},indent=2))
