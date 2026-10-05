"""Checks that ordering and branch shares are recomputed from the site records."""

import csv
import importlib.util
import json
import shutil
import tempfile
import unittest
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("arm_reproduce", ROOT / "scripts" / "reproduce.py")
reproduce_module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(reproduce_module)
BRANCH_OPERATIONS = reproduce_module.BRANCH_OPERATIONS
REMAINDER = reproduce_module.REMAINDER
SITE_COUNT = reproduce_module.SITE_COUNT
branch_shares = reproduce_module.branch_shares
interpretation_is_supported = reproduce_module.interpretation_is_supported
reproduce = reproduce_module.reproduce
supported_interpretation = reproduce_module.supported_interpretation


def load_site_events(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        row["chemical_onset_ps"] = float(row["chemical_onset_ps"])
        row["support_onset_ps"] = float(row["support_onset_ps"]) if row["support_onset_ps"] else ""
        row["support_right_censored"] = row["support_right_censored"] == "True"
    return rows


def ordering_from_rows(rows: list[dict]) -> tuple[int, int, int]:
    observed = [row for row in rows if row["support_onset_ps"] != "" and not row["support_right_censored"]]
    chemistry_first = sum(row["chemical_onset_ps"] < row["support_onset_ps"] for row in observed)
    equal_times = sum(row["chemical_onset_ps"] == row["support_onset_ps"] for row in observed)
    return len(observed), chemistry_first, equal_times


class ReproduceTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.inputs = self.root / "inputs"
        self.inputs.mkdir()
        for name in ("exits.csv", "neighborhoods.csv", "k_sites.csv"):
            shutil.copyfile(ROOT / "task" / "data" / name, self.inputs / name)

    def test_summary_matches_site_records(self):
        summary = reproduce(self.inputs, self.root / "output")
        rows = load_site_events(self.root / "output" / "site_events.csv")
        self.assertEqual(len(rows), 1728)
        self.assertEqual(len(summary["per_seed"]), 9)
        events, chemistry_first, equal_times = ordering_from_rows(rows)
        pooled = summary["pooled"]
        self.assertEqual(pooled["events"], events)
        self.assertEqual(pooled["chemistry_first_events"], chemistry_first)
        self.assertEqual(pooled["equality_events"], equal_times)
        self.assertAlmostEqual(pooled["chemistry_first_fraction"], chemistry_first / events)

        grouped = defaultdict(list)
        for row in rows:
            grouped[(row["material"], row["seed"])].append(row)
        for seed_row in summary["per_seed"]:
            group = grouped[(seed_row["material"], str(seed_row["seed"]))]
            self.assertEqual(seed_row["initial_sites"], SITE_COUNT)
            observed, first, equal = ordering_from_rows(group)
            self.assertEqual(seed_row["observed_pairs"], observed)
            self.assertEqual(seed_row["chemistry_first_pairs"], first)
            self.assertEqual(seed_row["equality_pairs"], equal)
            shares = branch_shares(seed_row["material"], [row["first_exit_operation"] for row in group])
            for label, share in shares.items():
                self.assertAlmostEqual(seed_row["branch_shares"][label], share)

        by_material = defaultdict(list)
        for seed_row in summary["per_seed"]:
            by_material[seed_row["material"]].append(seed_row)
        for material_row in summary["per_material"]:
            seed_rows = by_material[material_row["material"]]
            labels = set(material_row["branches"])
            self.assertIn("N-H loss", labels)
            self.assertIn(REMAINDER, labels)
            self.assertEqual(
                {label: recorded["operations"] for label, recorded in material_row["branches"].items()},
                {
                    **{label: list(names) for label, names in BRANCH_OPERATIONS[material_row["material"]].items()},
                    REMAINDER: [],
                },
            )
            for label in labels:
                values = [row["branch_shares"][label] for row in seed_rows]
                recorded = material_row["branches"][label]
                self.assertAlmostEqual(recorded["seed_mean_share"], sum(values) / len(values))
            for seed_row in seed_rows:
                self.assertAlmostEqual(sum(seed_row["branch_shares"].values()), 1.0)
            nh_share = material_row["branches"]["N-H loss"]["seed_mean_share"]
            other = max(
                share["seed_mean_share"]
                for label, share in material_row["branches"].items()
                if label != "N-H loss"
            )
            self.assertGreater(nh_share, other)
        self.assertTrue(interpretation_is_supported(summary))

    def test_duplicate_event_is_rejected(self):
        path = self.inputs / "exits.csv"
        lines = path.read_text(encoding="utf-8").splitlines()
        path.write_text("\n".join([*lines, lines[1]]) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "duplicate key"):
            reproduce(self.inputs, self.root / "output")

    def test_dropped_site_is_rejected(self):
        path = self.inputs / "exits.csv"
        lines = path.read_text(encoding="utf-8").splitlines()
        path.write_text("\n".join([lines[0], *lines[2:]]) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "input coverage"):
            reproduce(self.inputs, self.root / "output")

    def test_atom_identity_disagreement_is_rejected(self):
        path = self.inputs / "neighborhoods.csv"
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            columns = reader.fieldnames
            rows = list(reader)
        rows[0]["a_heavy_atom_ids_zero_based"] = "999999"
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        with self.assertRaisesRegex(ValueError, "A-site atom IDs disagree"):
            reproduce(self.inputs, self.root / "output")

    def test_unsupported_interpretation_is_rejected(self):
        summary = reproduce(self.inputs, self.root / "output")
        summary["interpretation"] = (
            "Bulk framework collapse follows chemistry, and net N-H loss identifies the perchlorate acceptor."
        )
        self.assertFalse(interpretation_is_supported(summary))

        for row in summary["per_seed"]:
            row["chemistry_first_fraction"] = 0.1
        self.assertNotIn("precedes the median", supported_interpretation(summary))
        summary["interpretation"] = (
            "Exact single N-H loss is the largest persistent first-exit class in each material. "
            "Persistent A-site chemistry precedes the median 500 fs loss of neighboring "
            "[K(ClO4)6] support. This is a local timing comparison under the shared 500 fs window."
        )
        self.assertFalse(interpretation_is_supported(summary))
        written = json.loads((self.root / "output" / "summary.json").read_text(encoding="utf-8"))
        self.assertTrue(interpretation_is_supported(written))


if __name__ == "__main__":
    unittest.main()
