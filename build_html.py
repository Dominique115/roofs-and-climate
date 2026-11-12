"""Build one offline HTML file, embedding the dataset and licensed photographs."""
import base64,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
data=json.loads((ROOT/'dataset.json').read_text())
photos=json.loads((ROOT/'photos.json').read_text())
galleries=json.loads((ROOT/'galleries.json').read_text())
for row in data:
 row['photo_gallery']=[]
 for photo in galleries[row['id']]:
  p=dict(photo)
  p['embedded_url']='data:image/jpeg;base64,'+base64.b64encode((ROOT/p['local_file']).read_bytes()).decode()
  row['photo_gallery'].append(p)
 row['photo']=photos[row['id']]
payload=json.dumps(data,ensure_ascii=False).replace('</','<\\/')
(ROOT/'index.html').write_text((ROOT/'explorer.template.html').read_text().replace('__DATA__',payload))
print('Built index.html with '+str(sum(len(r['photo_gallery']) for r in data))+' embedded photographs.')
