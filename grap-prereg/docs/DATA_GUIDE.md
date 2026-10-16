# Getting the real data (run only AFTER `make lock`)
1. **PM2.5** - CPCB CCR portal (airquality.cpcb.gov.in) -> Delhi stations, daily/hourly -> average across stations, require >= 75% coverage.
2. **GRAP stage dates** - CAQM orders (caqm.nic.in): record the date each Stage III/IV was invoked and revoked -> `grap_stage` (0-4) per day.
3. **Meteorology** - ERA5 (Copernicus CDS), Delhi bounding box: 10 m wind, boundary-layer height, 2 m temp, dewpoint -> RH, total precip; daily means.
4. Save to `data/raw/`, merge to `data/interim/daily.csv` with columns:
   `date, pm25, grap_stage, wind, blh, temp, rh, precip`, then `make real`.
Do NOT plot PM2.5 against grap_stage before running the locked pipeline.
