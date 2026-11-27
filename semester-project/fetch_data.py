"""Retrieve the two source snapshots used by the semester-project notebook."""
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

snapshot = Path(__file__).resolve().parent / "data" / "raw" / "snapshot_2026-11-05"
inputs = ("owid-co2-data.csv", "worldbank_gdp_per_capita.json")
manifest = json.loads((snapshot / "manifest.json").read_text(encoding="utf-8-sig"))

for name in inputs:
    entry = manifest["files"][name]
    destination = snapshot / name
    if destination.is_file():
        payload = destination.read_bytes()
    else:
        with urlopen(entry["url"], timeout=60) as response:
            payload = response.read()
    if hashlib.sha256(payload).hexdigest() != entry["sha256"]:
        raise SystemExit(f"Checksum mismatch for {name}. Use the exact snapshot from the team archive.")
    if not destination.is_file():
        destination.write_bytes(payload)
    print(f"Verified {name}")
