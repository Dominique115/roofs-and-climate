# Raw climate responses

Original NASA POWER monthly API responses for the collection's representative locations, covering 1991–2020. Exact request URLs are preserved in `../dataset.json`.

Parameters: T2M (degrees Celsius), PRECTOTCORR (millimetres per day), and WS10M (metres per second at 10 metres). The assembly script converts precipitation rates to monthly totals using the actual number of days in each month.

These are regional estimates, not individual building measurements. The separate Shirakawa station supplement comes from Japan Meteorological Agency data recorded in `../enrich.py` and cited in the dataset.
