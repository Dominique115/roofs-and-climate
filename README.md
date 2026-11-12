# Under the same sky

An interactive field guide to traditional roofs and climate: **13 locations, 22 credited photographs, and 17 sourced explanations**.

## Open the explorer

[Open the public website](https://dominique115.github.io/roofs-and-climate/).

Download `index.html` and open it in a desktop browser. The HTML embeds the climate dataset and photographs, so the explorer works offline. External research and attribution links require internet access.

- Blue bars show monthly precipitation and the orange line shows temperature.
- Hover or focus a month to explore; click to pin its explanation.
- Use arrow keys to move between months and Escape to release a pinned month.
- Select photo thumbnails or enlarge a photo for closer inspection.
- Shirakawa-go includes autumn and winter photographs and a local weather-station data option.

## Research and data

- `dataset.json`: roof records, climate summaries, monthly values, narrative evidence and image metadata.
- `raw/`: original NASA POWER monthly API responses.
- `review.md`: location comparison and source notes.
- `seasonal-review.md`: seasonal narrative text and qualifications.
- `research-sources.md`: research findings and limits.
- `photos.json` and `galleries.json`: photographer credits, source pages and image reuse licences.
- `photos/`: the selected photograph files.

The common climate baseline is **1991–2020**. NASA POWER provides regional estimates; a Japan Meteorological Agency station supplement is used for Shirakawa-go when selected. Wae Rebo and Glaumbaer still need local climate verification. These recent climate averages do not represent weather at the time a building tradition originated or a historical photo was taken.

Narratives distinguish documented local functions, explanations of a wider building tradition and general physical mechanisms. Missing evidence is left explicit. The collection is exploratory and does not establish causation or provide structural design guidance.

## Rebuild

Python 3 and the files already in this repository are sufficient; no packages are required for the build.

```bash
python3 assemble.py
python3 enrich.py
python3 build_html.py
```

Edit `explorer.template.html` for the interface; `index.html` is the generated standalone file. Narrative definitions are in `enrich.py`, `expand_research.py` and `collection_additions.py`. Update the local photo manifests and files before rebuilding to change images. The `select_*.py` and `add_seasonal_photos.py` scripts are research-session helpers that require their original temporary search responses; they are not needed to rebuild the site.

## Credits and reuse

Photographs retain their individual Creative Commons licences or public-domain status. Author, original-file and licence links appear in the explorer and in the image manifests. Keep those credits and observe each image's licence when reusing or modifying images. No blanket licence is granted over third-party media or source publications by this repository.

Primary climate sources: [NASA POWER](https://power.larc.nasa.gov/docs/services/api/temporal/monthly/) and [Japan Meteorological Agency](https://www.data.jma.go.jp/stats/etrn/view/nml_amd_ym.php?block_no=1306&prec_no=52&view=p1&year=).

Research assembled November 12, 2026.
