# PAP-H2 research ARM

This repository defines an analysis-level agent task for the 1666 K
DAP-2, PAP-2, and PAP-H2 event records. The small, atom-identified inputs,
task contract, and base container definition are versioned here.

The agent recomputes two quantities from those records. The first is the
fraction of persistent A-site first exits that precede the median 500 fs loss
of the eight neighboring [K(ClO4)6] units, with equal times counted separately.
The second is the seed-mean share of each exact single-operation first-exit
class, including N–H loss. The agent must produce per-site evidence. A
published percentage is not an input, and a verdict without the site table
does not complete the task.

Local [K(ClO4)6] support loss is not bulk crystal collapse. Net N–H loss
identifies a bond operation, not the acceptor of the transferred hydrogen.
The tables do not support a trajectory rerun, an Arrhenius fit, a continuous
shape measure, or an experimental thermal comparison.

## Task files

- [`task/task_spec.json`](task/task_spec.json): public task interface,
  experiment steps, and evidence outputs.
- [`task/INPUTS.md`](task/INPUTS.md): bundled real-input provenance and hashes.
- [`scripts/reproduce.py`](scripts/reproduce.py): independent event-to-support
  join, seed-resolved ordering, and exact-operation branch shares, using
  Python's standard library.
- [`environment/Dockerfile`](environment/Dockerfile): Paper2ARM-compatible
  fallback container declaration. Harbor/LBG uses its prebuilt image instead
  of building this file.
- [`docs/docker.md`](docs/docker.md): verified image metadata and local Docker
  build/run instructions.

To run the analysis from the repository root with Python 3:

```sh
python3 scripts/reproduce.py --inputs task/data --output outputs
python3 -m unittest discover -s tests -p 'test_*.py'
```

The generated `outputs/site_events.csv` and `outputs/summary.json` are ignored
by Git. The input tables define an event-level reanalysis; they are not
instructions to regenerate the underlying molecular-dynamics trajectories.
