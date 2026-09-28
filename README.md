# PAP-H2 research ARM

This repository defines an analysis-level agent task examining early chemical
changes and local coordination loss in three energetic perovskite materials.
The small, atom-identified event inputs, task contract and base container
definition are versioned here.

The agent goal is qualitative: recover the ordering between persistent
A-site chemical first exits and loss of neighboring local K–Cl coordination,
and identify the leading persistent first-exit operations under matched
conditions. The agent must produce per-site evidence, not just state a verdict
or copy a published percentage. “Local coordination loss” does not mean bulk
crystal collapse; net N–H loss does not itself identify the H acceptor.

## Task files

- [`task/task_spec.json`](task/task_spec.json): public task interface,
  experiment steps, and evidence outputs.
- [`task/INPUTS.md`](task/INPUTS.md): bundled real-input provenance and hashes.
- [`scripts/reproduce.py`](scripts/reproduce.py): independent event-to-support
  join and per-seed qualitative analysis, using Python's standard library.
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
