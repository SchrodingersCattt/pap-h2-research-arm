"""Reconstruct the 1666 K chemical-to-local-support ordering from event records."""

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median


MATERIALS = ("DAP-2", "PAP-2", "PAP-H2")
SEEDS = (26083101, 26083102, 26083103)


def read_unique(path: Path, columns: tuple[str, ...], key: tuple[str, ...]) -> dict:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not set(columns).issubset(reader.fieldnames or []):
            raise ValueError(f"missing columns in {path.name}")
        rows = {}
        for row in reader:
            identity = tuple(row[field] for field in key)
            if identity in rows:
                raise ValueError(f"duplicate key in {path.name}: {identity}")
            rows[identity] = row
    return rows


def atom_ids(value: str) -> set[int]:
    return {int(item) for item in value.split(";") if item}


def reproduce(inputs: Path, output: Path) -> dict:
    exits = read_unique(
        inputs / "exits.csv",
        ("material", "temperature_K", "seed", "site", "parent_heavy_ids_zero_based", "exit_frame", "operation"),
        ("material", "temperature_K", "seed", "site"),
    )
    maps = read_unique(
        inputs / "neighborhoods.csv",
        ("material", "temperature_K", "seed", "a_site", "a_heavy_atom_ids_zero_based", "k_rows", "neighborhood_size"),
        ("material", "temperature_K", "seed", "a_site"),
    )
    sites = read_unique(
        inputs / "k_sites.csv",
        ("material", "temperature_K", "seed", "k_row", "loss_500fs_start_frame", "loss_500fs_right_censored"),
        ("material", "temperature_K", "seed", "k_row"),
    )
    expected = {(material, "1666", str(seed), str(site)) for material in MATERIALS for seed in SEEDS for site in range(192)}
    if set(exits) != expected or set(maps) != expected or len(sites) != 1728:
        raise ValueError("input coverage must contain 192 A and K sites for each of nine seeds")

    output.mkdir(parents=True, exist_ok=True)
    rows = []
    grouped = defaultdict(list)
    for key in sorted(expected, key=lambda item: (item[0], int(item[2]), int(item[3]))):
        event = exits[key]
        neighborhood = maps[key]
        if atom_ids(event["parent_heavy_ids_zero_based"]) != atom_ids(neighborhood["a_heavy_atom_ids_zero_based"]):
            raise ValueError(f"A-site atom IDs disagree at {key}")
        k_rows = [int(item) for item in neighborhood["k_rows"].split(";")]
        if len(k_rows) != 8 or len(set(k_rows)) != 8 or int(neighborhood["neighborhood_size"]) != 8:
            raise ValueError(f"expected eight distinct neighboring K sites at {key}")
        losses = []
        for k_row in k_rows:
            k_key = key[:3] + (str(k_row),)
            if k_key not in sites:
                raise ValueError(f"missing K site {k_key}")
            site = sites[k_key]
            if site["loss_500fs_right_censored"] not in ("True", "False"):
                raise ValueError(f"invalid censoring flag at {k_key}")
            if site["loss_500fs_right_censored"] == "False":
                losses.append(float(site["loss_500fs_start_frame"]))
        onset = median(losses) if losses else None
        censored = len(losses) < 4
        chemical_frame = int(event["exit_frame"])
        result = {
            "material": key[0],
            "seed": key[2],
            "site_id": key[3],
            "chemical_onset_ps": chemical_frame * 0.01,
            "support_onset_ps": onset * 0.01 if onset is not None else "",
            "support_right_censored": censored,
            "first_exit_operation": event["operation"],
        }
        rows.append(result)
        grouped[key[:3]].append(result)

    with (output / "site_events.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    per_seed = []
    per_material = []
    for material in MATERIALS:
        material_rows = []
        for seed in SEEDS:
            group = grouped[(material, "1666", str(seed))]
            observed = [row for row in group if row["support_onset_ps"] != "" and not row["support_right_censored"]]
            chemistry_first = sum(row["chemical_onset_ps"] < row["support_onset_ps"] for row in observed)
            per_seed.append({
                "material": material,
                "seed": seed,
                "initial_sites": len(group),
                "observed_pairs": len(observed),
                "chemistry_first_pairs": chemistry_first,
                "chemistry_first_fraction": chemistry_first / len(observed) if observed else None,
            })
            material_rows.extend(group)
        counts = Counter(row["first_exit_operation"] for row in material_rows)
        seed_fractions = [row["chemistry_first_fraction"] for row in per_seed if row["material"] == material]
        per_material.append({
            "material": material,
            "seed_mean_chemistry_first_fraction": sum(seed_fractions) / len(seed_fractions),
            "leading_operation": counts.most_common(1)[0][0],
            "operation_counts": dict(sorted(counts.items())),
        })
    majority = all(row["chemistry_first_fraction"] > 0.5 for row in per_seed)
    interpretation = (
        "Persistent A-site chemistry generally precedes neighboring local K–Cl coordination loss."
        if majority else "The event ordering differs across seeds."
    )
    summary = {"per_seed": per_seed, "per_material": per_material, "interpretation": interpretation}
    (output / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, default=Path(__file__).resolve().parents[1] / "task" / "data")
    parser.add_argument("--output", type=Path, default=Path("/app/outputs"))
    args = parser.parse_args()
    reproduce(args.inputs, args.output)