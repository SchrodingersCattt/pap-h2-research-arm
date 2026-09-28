"""Small checks for the event-to-support join, without a published answer key."""

import csv
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.reproduce import reproduce  # noqa: E402


class ReproduceTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.inputs = self.root / "inputs"
        self.inputs.mkdir()
        for name in ("exits.csv", "neighborhoods.csv", "k_sites.csv"):
            shutil.copyfile(ROOT / "task" / "data" / name, self.inputs / name)

    def test_complete_cohort(self):
        summary = reproduce(self.inputs, self.root / "output")
        with (self.root / "output" / "site_events.csv").open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 1728)
        self.assertEqual(len(summary["per_seed"]), 9)
        self.assertTrue(all(row["initial_sites"] == 192 for row in summary["per_seed"]))
        self.assertTrue(all(0 <= row["chemistry_first_fraction"] <= 1 for row in summary["per_seed"]))

    def test_duplicate_event_is_rejected(self):
        path = self.inputs / "exits.csv"
        lines = path.read_text(encoding="utf-8").splitlines()
        path.write_text("\n".join([*lines, lines[1]]) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "duplicate key"):
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


if __name__ == "__main__":
    unittest.main()