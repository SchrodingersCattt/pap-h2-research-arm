# PAP-H2 research ARM

This repository defines an agent task examining early chemical changes and
local coordination loss in three energetic perovskite materials. The task
interface, input contract, and base container definition are versioned here.

The agent goal is qualitative: recover the ordering between persistent
A-site chemical first exits and loss of neighboring local K–Cl coordination,
and identify the leading persistent first-exit operations under matched
conditions. The agent must produce per-site evidence, not just state a verdict
or copy a published percentage. “Local coordination loss” does not mean bulk
crystal collapse; net N–H loss does not itself identify the H acceptor.

## Task files

- [`task/task_spec.json`](task/task_spec.json): public task interface,
  experiment steps, and evidence outputs.
- [`task/INPUTS.md`](task/INPUTS.md): input roles and provenance requirements.
- [`environment/Dockerfile`](environment/Dockerfile): Paper2ARM-compatible
  fallback container declaration. Harbor/LBG uses its prebuilt image instead
  of building this file.
- [`docs/docker.md`](docs/docker.md): verified image metadata and local Docker
  build/run instructions.
