"""B0: save one Citi Bike GBFS station_status snapshot as a gzipped CSV.

Output: data/station_status/YYYY-MM-DD/HHMMSS.csv.gz (UTC date and time).
Columns: station_id, last_reported (Unix seconds), num_bikes_available,
num_ebikes_available, num_docks_available, is_renting, is_returning,
fetched_at (UTC, ISO 8601). Standard library only.
"""

import csv
import gzip
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

URL = "https://gbfs.citibikenyc.com/gbfs/en/station_status.json"
OUT_DIR = Path("data/station_status")
COLUMNS = [
    "station_id",
    "last_reported",
    "num_bikes_available",
    "num_ebikes_available",
    "num_docks_available",
    "is_renting",
    "is_returning",
    "fetched_at",
]


def fetch() -> dict:
    with urllib.request.urlopen(URL, timeout=60) as resp:
        return json.load(resp)


def save(payload: dict, fetched_at: datetime) -> Path:
    day_dir = OUT_DIR / fetched_at.strftime("%Y-%m-%d")
    day_dir.mkdir(parents=True, exist_ok=True)
    path = day_dir / f"{fetched_at.strftime('%H%M%S')}.csv.gz"
    stamp = fetched_at.isoformat(timespec="seconds")
    with gzip.open(path, "wt", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS)
        for s in payload["data"]["stations"]:
            writer.writerow(
                [
                    s.get("station_id"),
                    s.get("last_reported"),
                    s.get("num_bikes_available"),
                    s.get("num_ebikes_available"),
                    s.get("num_docks_available"),
                    s.get("is_renting"),
                    s.get("is_returning"),
                    stamp,
                ]
            )
    return path


if __name__ == "__main__":
    out = save(fetch(), datetime.now(timezone.utc))
    print(f"wrote {out}")
