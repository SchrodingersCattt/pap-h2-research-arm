"""Export the three atom-identified, 1666 K event inputs without machine paths.

Run against the source analysis directory; published task inputs are the
selected scientific columns, not the source machine's provenance strings.
"""

import argparse
import csv
import hashlib
from pathlib import Path


SOURCES = {
    "e2_first_exit_atom_links.csv": (
        "504569f95ccd475ed1fba6f555fb8f72c606f40e07e46ea6527d0b5802434b7a",
        "exits.csv",
        ("material", "temperature_K", "seed", "site", "parent_heavy_ids_zero_based", "exit_frame", "operation"),
    ),
    "a_k_neighborhoods.csv": (
        "e4522ad5280503d57b13af773e34040faebae6e38dbf3e564dff30ab966668d0",
        "neighborhoods.csv",
        ("material", "temperature_K", "seed", "a_site", "a_heavy_atom_ids_zero_based", "k_rows", "neighborhood_size"),
    ),
    "k_cl6_sites.csv": (
        "a2bc522b5cb3374d5825c2133227fe0b341ff4ee66dcf6e67879a19b4f55fdd7",
        "k_sites.csv",
        ("material", "temperature_K", "seed", "k_row", "loss_500fs_start_frame", "loss_500fs_right_censored"),
    ),
}


def export(source: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for filename, (expected, output, fields) in SOURCES.items():
        raw = (source / filename).read_bytes()
        if hashlib.sha256(raw).hexdigest() != expected:
            raise ValueError(f"source hash mismatch: {filename}")
        with (source / filename).open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        if len(rows) != 1728:
            raise ValueError(f"expected 1728 rows in {filename}, got {len(rows)}")
        if not set(fields).issubset(rows[0]):
            raise ValueError(f"missing scientific fields in {filename}")
        with (destination / output).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            writer.writerows({field: row[field] for field in fields} for row in rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    export(args.source, args.destination)