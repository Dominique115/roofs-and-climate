"""Add chart narratives and local station supplement; keep regional data intact."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
JMA='https://www.data.jma.go.jp/stats/etrn/view/nml_amd_ym.php?block_no=1306&day=4&month=&prec_no=52&view=p1&year='
station_rows=[
 [1,281.8,-1.0,340,148],[2,204.5,-0.8,251,173],[3,195.8,2.5,149,125],
 [4,151.6,8.8,19,32],[5,128.8,14.9,1,0],[6,187.1,19.0,0,0],
 [7,277.7,22.7,0,0],[8,190.5,23.6,0,0],[9,214.5,19.4,0,0],
 [10,167.9,13.2,0,0],[11,181.6,7.1,12,5],[12,282.8,1.7,201,84]]
station=dict(source_url=JMA,source='Japan Meteorological Agency; Shirakawa, Gifu; block 1306',period='1991-2020',annual_precip_mm=2458.2,annual_mean_temp_c=10.9,annual_snowfall_depth_total_cm=972,annual_normal_greatest_snow_depth_cm=177,monthly=[dict(zip(['month','precip_mm','temp_c','snowfall_depth_total_cm','normal_monthly_greatest_snow_depth_cm'],r)) for r in station_rows],notes='Snowfall depth totals are accumulated fresh snow depth, not snow water equivalent or roof load. Greatest snow depth is a separate normal statistic. Annual normals are published separately and need not equal sums of rounded monthly normals. Wind excluded because station exposure and measurement height are not matched to NASA WS10M.')

def story(id,months,series,title,text,feature,sources,scope,caveat=''):
 return dict(id=id,months=months,series=series,title=title,text=text,roof_feature=feature,sources=sources,evidence_scope=scope,caveat=caveat,month_assignment='Editorial selection of months for exploring a documented function; not a measured seasonal performance threshold.')

stories={
 'shirakawa':[
 story('snow',[11,12,1,2,3],'precipitation','A steep roof for snowy winters','Steep roof slopes help limit snow accumulation and the risk of damage. Snow can still cling to the thatch, so residents also remove roof snow.','roof slope',['https://kankou.shirakawa-go.org/2688.htm'],'documented local function','Show JMA snowfall in the detail panel; precipitation bars alone cannot identify snow.'),
 story('summer-airflow',[6,7,8],'temperature','Summer orientation and airflow','The village describes roof orientation as helping manage seasonal sunlight and wind. The open attic structure lets light and breezes reach spaces once used for raising silkworms.','roof orientation and attic openings',['https://kankou.shirakawa-go.org/1539.htm','https://kankou.shirakawa-go.org/2688.htm'],'documented local qualitative explanation','No indoor cooling amount or material-specific thermal performance has been established.')],
 'bermuda':[
 story('water-collection',list(range(1,13)),'precipitation','The roof supplies water','Roof gutters and water glides channel rainfall toward storage tanks. Explore any month to see the rainfall context for this water collection system.','roof gutters and water glides',['https://planning.gov.bm/wp-content/uploads/2018/11/Traditional-Building-Guide.pdf'],'documented local function','Rainfall occurs throughout the year in this dataset. Do not label selected months a monsoon or assume rainfall equals collected water.'),
 story('reflective-surface',[7,8,9],'temperature','Why a reflective surface can matter','A light, reflective roof surface can absorb less sunlight and reduce heat transfer into a building. This is a general physical principle relevant to examining a white roof.','white surface',['https://www.energystar.gov/products/cool-roofs'],'general mechanism; local performance unverified','This does not establish Bermuda-specific reflectance, indoor cooling, energy savings or the historical reason for the white finish. Air temperature is not solar radiation.')],
 'alberobello':[
 story('cistern',[9,10,11,12,1,2,3,4],'precipitation','Rain directed toward a cistern','UNESCO describes eaves that route roof runoff through a channelled slab toward a cistern beneath the house. The wetter months provide a useful moment to explore this feature.','eaves and cistern route',['https://whc.unesco.org/en/list/787/'],'documented local function','The collection function is not restricted to these months. A climatic cause for the conical shape has not been established.')]
}

def enrich(records):
 from expand_research import additional,EVIDENCE_UPDATES
 from collection_additions import narratives
 combined={**stories,**additional(story),**narratives(story)}
 photos=json.loads((ROOT/'photos.json').read_text()) if (ROOT/'photos.json').exists() else {}
 galleries=json.loads((ROOT/'galleries.json').read_text()) if (ROOT/'galleries.json').exists() else {}
 for r in records:
  if r['id'] in photos:
   r['photo']=photos[r['id']]
   r['photo_status']='Selected Commons photograph; credit and licence recorded in photo metadata'
  r['photo_gallery']=galleries.get(r['id'],[photos[r['id']]] if r['id'] in photos else [])
  r['chart_annotations']=combined.get(r['id'],[])
  if r['id'] in EVIDENCE_UPDATES:
   r['climate_evidence'],r['evidence_scope']=EVIDENCE_UPDATES[r['id']]
  r['preferred_chart_climate']='NASA regional monthly climatology; provisional'
  if r['id']=='shirakawa':
   r['local_station_climatology']=station
   r['preferred_chart_climate']='JMA Shirakawa station monthly normals 1991-2020'
   r['climate_quality_note']='Use JMA station supplement for the location story. Retain NASA baseline for consistently sourced cross-location comparisons; do not silently mix series.'
  r['explanation_status']='Draft sourced text available' if r['chart_annotations'] else 'No seasonal chart explanation approved; research still needed'
 return records

if __name__=='__main__':
 path=ROOT/'dataset.json'
 data=enrich(json.loads(path.read_text()))
 path.write_text(json.dumps(data,indent=2,ensure_ascii=False))
 lines=['# Seasonal chart explanations for review','','Chart: blue precipitation bars; orange temperature line. Desktop hover reveals values and relevant text; click pins the explanation. Label: Long-term monthly averages, 1991–2020. Month selections below are editorial navigation, not scientific season boundaries.','','## Local data improvement','','Use the official JMA Shirakawa station supplement for its story chart. Annual precipitation is 2458.2 mm and mean temperature 10.9 °C. The regional NASA values remain in the dataset for consistent comparisons. Snowfall is stored separately in centimetres of fresh snow depth, never substituted for precipitation in millimetres.','',f'[JMA station table]({JMA})','','## Draft hover text','']
 for r in data:
  for s in r['chart_annotations']:
   lines += [f"### {r['place']}: {s['title']}",f"Months: {', '.join(str(m) for m in s['months'])}. Series: {s['series']}. Feature to highlight: {s['roof_feature']}.",'',s['text'],'',f"Evidence: {s['evidence_scope']}. {s['caveat']}",'',*['[Source]('+url+')' for url in s['sources']],'']
 lines += ['## Remaining research','','Glaumbaer and Holasovice remain without seasonal narratives. Wae Rebo and Glaumbaer retain priority local climate checks. Hahoe and Taos narratives are explicitly labelled as building-tradition explanations, not performance measurements of the pictured houses. Photos show local examples, sometimes different buildings rather than the identical building from another angle. Credits and licences are recorded per image. A reflective-surface mechanism is available for Bermuda as general educational context, not verified local cooling performance.']
 (ROOT/'seasonal-review.md').write_text('\n'.join(lines))
 print(f'Updated {len(data)} cases; {sum(len(r["chart_annotations"]) for r in data)} narratives; 12 JMA station months.')
