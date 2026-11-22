# BikeFlow NYC — GBFS status collector (B0)

GitHub Actions saves a Citi Bike GBFS `station_status` snapshot every 15 minutes to
`data/station_status/YYYY-MM-DD/HHMMSS.csv.gz` (UTC). Loaded into the main project by
`scripts/backfill_status.py` (B4) in https://github.com/xuechunz38-stack/bikeflow-nyc.
