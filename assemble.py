import json, calendar, statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent
# Coordinates are approximate representative points, not surveyed building locations.
cases = [
 ('shirakawa','Shirakawa-go','Japan',36.257,136.906,'Gassho: steep thatched gable','Thatch; timber',60,'Snow shedding explicitly documented by Japan National Tourism Organization.','Attic space supported silkworm cultivation.','roof-specific climate function documented','https://www.japan.travel/en/world-heritage/the-historic-villages-of-shirakawa-go-and-gokayama/','https://whc.unesco.org/en/list/734/'),
 ('ghadames','Ghadames','Libya',30.133,9.5,'Flat roof terraces with parapets','Earth; palm timber',None,'UNESCO describes settlement-wide adaptation to desert conditions; no isolated roof-performance measurement.','Terraces provided circulation and social space for women.','settlement-level climate context documented','https://whc.unesco.org/en/list/362/','https://whc.unesco.org/en/list/362/'),
 ('alberobello','Alberobello','Italy',40.783,17.237,'Conical corbelled stone roof','Limestone slabs',None,'Roof eaves channel rainwater toward an underground cistern; climate origin of cone shape is not established.','Local limestone and dry-stone craft; agricultural shelters and dwellings.','roof-specific water function documented','https://whc.unesco.org/en/list/787/','https://whc.unesco.org/en/list/787/'),
 ('waerebo','Wae Rebo','Indonesia',-8.769,120.284,'Tall conical roof extending nearly to ground','Thatch; bamboo; timber',None,'Rain-shedding role is a research hypothesis, not established by the cited source.','Five levels accommodate living, storage, food reserves and ancestral offerings.','climate explanation unverified','https://www.indonesia.travel/au/en/destination/bali-nusa-tenggara/east-nusa-tenggara/wae-rebo','https://the.akdn/en/akdn/en/how-we-work/our-agencies/aga-khan-trust-culture/akaa/preservation-mbaru-niang'),
 ('glaumbaer','Glaumbaer','Iceland',65.61125,-19.50475,'Multiple pitched turf roofs','Turf; timber',None,'National Museum submission describes climatic adaptation of the turf tradition; roof insulation is not quantified.','Turf availability and evolution of connected farm buildings.','tradition-level climate context documented','https://whc.unesco.org/en/tentativelists/5589/','https://whc.unesco.org/en/tentativelists/5589/'),
 ('hahoe','Hahoe','South Korea',36.539,128.519,'Tile and thatched roofs in one village','Tile or thatch; timber',None,'No roof-specific climatic explanation established in the cited sources.','Roof materials reflect historical social status; useful within-location contrast.','climate explanation unverified','https://english1.visitkorea.or.kr/enu/ATR/SI_ENG_3_2.jsp','https://whc.unesco.org/en/list/1324/'),
 ('bermuda','St George, Bermuda','Bermuda (UK territory)',32.381,-64.677,'White stepped pitched roof with water glides','Limestone roofing; white coating',None,'Government building guide documents rooftop rainfall collection and conveyance to storage.','Domestic water supply and local building tradition.','roof-specific water function documented','https://planning.gov.bm/wp-content/uploads/2018/11/Traditional-Building-Guide.pdf','https://whc.unesco.org/en/list/983/'),
 ('tulou','Tianluokeng, Fujian','China',24.587,117.055,'Pitched tiled roof with wide eaves','Tiles; timber',None,'Protection of earthen walls from rain is a hypothesis for follow-up; cited description establishes wide eaves, not causal origin.','Communal clan housing, defence and Feng Shui.','climate explanation unverified','https://whc.unesco.org/en/list/1113/','https://whc.unesco.org/en/list/1113/'),
 ('taos','Taos Pueblo','United States',36.438,-105.546,'Terraced flat roofs','Timber and earthen roof assembly; verify detailed specification',None,'Dry-climate explanation is unverified; UNESCO also notes rain and snow erosion threats.','Living Pueblo community; roof access and terraced dwellings.','climate explanation unverified','https://whc.unesco.org/en/list/492/','https://home.nps.gov/articles/000/taos-pueblo-world-heritage-site.htm'),
 ('holasovice','Holasovice','Czech Republic',48.969,14.273,'Gabled roofs; ornate facade gables','Roof covering not coded',None,'No climate explanation established; decorative facade gables are not roof pitch measurements.','Folk Baroque decoration and rural prosperity.','climate explanation unverified','https://whc.unesco.org/en/list/861/','https://www.jiznicechy.cz/en/targets/33-holasovice-unesco-barocco-rurale'),
]

from collection_additions import cases as extra_cases
cases += extra_cases

def make():
 records=[]
 for c in cases:
  keys=['id','place','country','latitude','longitude','roof_form','materials','reported_pitch_degrees','climate_evidence','cultural_context','evidence_scope','architecture_source_url','photo_reference_page']
  r=dict(zip(keys,c))
  raw=json.loads((ROOT/'raw'/f'{c[0]}.json').read_text())
  p=raw['properties']['parameter']
  for param in ['T2M','PRECTOTCORR','WS10M']:
   vals=[p[param][f'{y}{m:02}'] for y in range(1991,2021) for m in range(1,13)]
   assert len(vals)==360 and all(v != raw['header']['fill_value'] for v in vals), (c[0],param)
  monthly=[]
  for m in range(1,13):
   avg=lambda key: statistics.mean(p[key][f'{y}{m:02}'] for y in range(1991,2021))
   rain=statistics.mean(p['PRECTOTCORR'][f'{y}{m:02}']*calendar.monthrange(y,m)[1] for y in range(1991,2021))
   monthly.append(dict(month=m,temp_c=round(avg('T2M'),2),precip_mm=round(rain,2),wind_10m_ms=round(avg('WS10M'),2)))
  # Day weighting uses each actual year's calendar; precipitation rate is mm/day.
  total_days=sum(366 if calendar.isleap(y) else 365 for y in range(1991,2021))
  weighted=lambda key: sum(p[key][f'{y}{m:02}']*calendar.monthrange(y,m)[1] for y in range(1991,2021) for m in range(1,13))/total_days
  r.update(climate_period='1991-2020',annual_mean_temp_c=round(weighted('T2M'),1),annual_precip_mm=round(sum(p['PRECTOTCORR'][f'{y}{m:02}']*calendar.monthrange(y,m)[1] for y in range(1991,2021) for m in range(1,13))/30),annual_mean_wind_10m_ms=round(weighted('WS10M'),1),coldest_month_temp_c=round(min(x['temp_c'] for x in monthly),1),warmest_month_temp_c=round(max(x['temp_c'] for x in monthly),1),monthly_climatology=monthly,climate_api_url=api_url(c),retrieved_date='2026-11-12',photo_status='Reference page only; individual photo and reuse licence not yet selected',coordinate_status='Approximate representative point; Glaumbaer from National Museum submission',snowfall_mm=None,extreme_wind_ms=None)
  r['climate_quality_note']='Regional grid estimate; local station comparison pending.'
  if c[0]=='waerebo':
   r['climate_quality_note']='Priority check: grid mean temperature is 27.1 C, while official tourism source describes a cool mountain village around 1100 m elevation. Do not present as measured village climate.'
  if c[0]=='glaumbaer':
   r['climate_quality_note']='Priority check: regional grid includes terrain unlike lowland farm site; verify temperature and precipitation with nearby Icelandic station.'
  records.append(r)
 from enrich import enrich
 records=enrich(records)
 (ROOT/'dataset.json').write_text(json.dumps(records,indent=2,ensure_ascii=False))
 lines=['# Roof and climate dataset — first review','', f'{len(records)} selected locations; one record represents a local roof tradition or ensemble, not a sampled building. Climate values are NASA POWER regional grid estimates for 1991–2020.','', '| Place | Roof | Mean temp °C | Rain + snow water equivalent mm/year | Mean wind at 10 m m/s | Evidence scope |','|---|---|---:|---:|---:|---|']
 for r in records:
  lines.append(f"| {r['place']} | {r['roof_form']} | {r['annual_mean_temp_c']} | {r['annual_precip_mm']} | {r['annual_mean_wind_10m_ms']} | {r['evidence_scope']} |")
 lines += ['', 'Priority climate checks: Wae Rebo (regional temperature conflicts with the official cool-mountain description) and Glaumbaer (terrain representation). All values remain regional estimates, not village observations.', '', '## Evidence and image references','']
 for r in records:
  lines += [f"### {r['place']}",r['climate_evidence'],r['cultural_context'],f"[Architecture source]({r['architecture_source_url']}) · [Photo reference page]({r['photo_reference_page']})",'']
  urls=list(dict.fromkeys(u for s in r['chart_annotations'] for u in s['sources']))
  lines += ['Seasonal evidence: '+ ' · '.join(f'[Source {i+1}]({u})' for i,u in enumerate(urls)),''] if urls else []
 lines += ['## Method and limits','', 'NASA POWER monthly T2M (°C), PRECTOTCORR (mm/day) and WS10M (m/s) were downloaded for 1991–2020. Each monthly precipitation rate was multiplied by the actual number of days in its month, annual totals summed and the 30 annual totals averaged. Temperature and wind annual means are weighted by days. Monthly climatologies average each calendar month over 30 years. Raw responses and exact API URLs are preserved. All 360 monthly values per parameter per location were checked for missing-value flags.', '', 'POWER meteorology derives from MERRA-2; its roughly 0.5° latitude by 0.625° longitude grid is much larger than a village. Mountain, valley and island estimates may differ materially from local observations; verify them against local stations before making site-specific claims. Values describe a recent baseline, not climate when these traditions originated. Mean wind does not represent gusts, cyclone risk or roof-level exposure. Precipitation includes rain and snow water equivalent; snowfall, snow load and extremes are missing. No pitch values were inferred from photographs. The Shirakawa 60° value is a general tourism-source description, not a measurement of every roof. Materials and roof forms describe traditions, not all present buildings. Selected Commons photographs, photographer credits and reuse licences are recorded in photos.json and embedded in the HTML explorer. The selected examples are purposive and geographically unbalanced; they cannot establish causation or population-wide correlations. Hahoe contains two roof materials under the same regional climate and must not be treated as two independent climate samples.', '', '[NASA POWER monthly API documentation](https://power.larc.nasa.gov/docs/services/api/temporal/monthly/)']
 (ROOT/'review.md').write_text('\n'.join(lines))
 print('\n'.join(lines[:15]))

def api_url(c):
 return f'https://power.larc.nasa.gov/api/temporal/monthly/point?parameters=T2M,PRECTOTCORR,WS10M&community=AG&longitude={c[4]}&latitude={c[3]}&start=1991&end=2020&format=JSON'

if __name__=='__main__': make()
