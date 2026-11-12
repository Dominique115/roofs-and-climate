"""Additional sourced narratives. Called by enrich.py for repeatable builds."""
REPORT='https://s3.amazonaws.com/media.archnet.org/system/publications/contents/9538/original/DTP102021.pdf?1397037668='
HANOK='https://contents.history.go.kr/front/tz/view.do?levelId=tz_b74'
GHADAMES='https://hrcak.srce.hr/file/280321'
TULOU='https://www.sciencedirect.com/science/article/pii/S221067071931008X'
PUEBLO='https://www.fs.usda.gov/eng/facilities/documents/adobe_arch.pdf'

def additional(story):
 return {
 'waerebo':[
 story('cone-runoff',[11,12,1,2,3],'precipitation','A cone that sheds rain','The 2013 conservation review describes the thatch and palm-fibre covering as shedding rain directly onto the surrounding ground. It records no gutters or rainwater collection system in the rebuilding.','conical roof and its low edge',[REPORT+'#page=14'],'on-site conservation review, printed page 13','The report identifies November–March as the wet season. The regional climate series remains provisional for this mountain village.'),
 story('thatch-and-air',[4,5,6,7,8,9,10],'temperature','Thatch and a tall ventilating interior','The reviewer describes thick thatch as buffering daytime heat and cooler nights. Rising warm air and kitchen smoke move up through the tall interior, providing natural ventilation.','thick thatch and tall roof volume',[REPORT+'#page=14'],'on-site observations, printed page 13','Short site-visit readings are not a year-round experiment and do not isolate the roof from the rest of the house. Local monthly climate still needs checking.')],
 'tulou':[
 story('eaves-rain',[3,4,5,6,7,8,9],'precipitation','An umbrella for earthen walls','Research on Fujian Tulou describes wide roof eaves as protecting load-bearing rammed-earth walls from rainfall. Wind-driven rain can still reach the wall and cause erosion.','projecting tiled eaves above earthen walls',[TULOU,'https://www.sciencedirect.com/science/article/pii/S0950061820319942'],'research on the Fujian Tulou building tradition','These studies do not establish performance for every Tianluokeng building. Monthly totals cannot describe storm intensity or wind-driven rain.')],
 'hahoe':[
 story('hanok-summer',[6,7,8],'temperature','Eaves that shade summer sunlight','The National Institute of Korean History explains that hanok eave slope and projection help block high summer sunlight. This is a documented principle of the house tradition represented at Hahoe.','projecting eaves',[HANOK],'hanok tradition; not a measurement of the pictured house','The photo may show a different roof material or orientation. Eave performance depends on geometry and solar position, not temperature alone.'),
 story('hanok-winter',[11,12,1,2],'temperature','Lower winter sun reaches indoors','The same account explains that hanok eaves admit lower winter sunlight. Roof geometry works with the rest of the house to respond to changing seasons.','eave projection and openings below',[HANOK],'hanok tradition; not a measurement of the pictured house','This does not mean that tile roofs alone warm houses or explain historical differences between tile and thatch.')],
 'ghadames':[
 story('roof-night',[5,6,7,8,9],'temperature','A terrace for summer nights','A case study documents rooftop space used for sitting and sleeping on summer nights. Parapet walls provide privacy and shelter from hot winds and dust.','open terrace and high parapets',[GHADAMES+'#page=7'],'Ghadames house case study, printed page 1965','This describes a documented use of space, not a measured cooling effect of every flat roof.'),
 story('roof-vent',[6,7,8,9],'temperature','Roof openings release accumulated heat','The study describes roof openings used for air circulation and night-time heat release. The openings can be closed in winter.','roof apertures',[GHADAMES+'#page=7'],'Ghadames house case study, printed page 1965','Roof openings may not be visible in the selected photographs. The monthly chart does not measure night-time ventilation or indoor comfort.')],
 'taos':[
 story('pueblo-drainage',[7,8,9],'precipitation','Flat roofs still need drainage','A US Forest Service guide describes traditional Pueblo roofs with parapets draining through projecting wooden spouts called canales. The drainage route is an important feature to look for on earthen buildings.','projecting drainage spouts at the roof edge',[PUEBLO],'Pueblo architectural tradition; not a Taos-specific roof survey','This guide also covers later Pueblo-style construction. Do not assume every visible beam is a drain or that flat roofs have no slope. No dry-climate origin claim is established.')]
 }

EVIDENCE_UPDATES={
 'waerebo':('Conservation reviewer documents conical-roof runoff, thatch thermal buffering and convection through the tall interior.','documented site observations; short visit'),
 'tulou':('Research documents wide eaves protecting rammed earth from rain, with residual wind-driven rain erosion risk.','documented building-tradition function'),
 'hahoe':('National Institute of Korean History explains seasonal solar shading by hanok eaves; not measured at the photographed building.','documented tradition-level explanation'),
 'ghadames':('House case study documents summer rooftop sleeping and ventilation through roof apertures.','documented house case study'),
 'taos':('US Forest Service guide documents canales draining Pueblo roofs; application to a particular Taos roof needs verification.','Pueblo-tradition evidence, not site-specific')}
