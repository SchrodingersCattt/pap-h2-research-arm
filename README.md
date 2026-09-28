# PAP-H2 research ARM

**Status: review draft, not yet a runnable Harbor task.** This repository is a
clean, public authoring surface for an agent task that examines early chemical
changes and local coordination loss in three energetic perovskite materials.
It does not contain credentials, private compute settings, large trajectories,
trained models, or an unpublished grader.

The intended agent goal is qualitative: recover the ordering between persistent
A-site chemical first exits and loss of neighboring local K–Cl coordination,
and identify the leading persistent first-exit operations under matched
conditions. The agent must produce per-site evidence, not just state a verdict
or copy a published percentage. “Local coordination loss” does not mean bulk
crystal collapse; net N–H loss does not itself identify the H acceptor.

## Review this first

- [`task/task_spec.json`](task/task_spec.json): proposed public task interface,
  experiment steps, and evidence outputs.
- [`task/INPUTS.md`](task/INPUTS.md): actual inputs needed and current blockers.
- [`environment/Dockerfile`](environment/Dockerfile): Paper2ARM-compatible
  fallback container declaration. Harbor/LBG uses its prebuilt image instead
  of building this file.

The first iteration reviews the task boundary before packaging a checker or
publishing data. **Do not submit this directory to Harbor yet.** In particular,
the raw nine-trajectory cohort, corresponding 300 K references, atom-resolved
event/geometry join and its producer are not yet available by a verified public
download. Plot-ready summary CSVs are not substitutes for those inputs.

Next iteration: publish versioned inputs with checksums and terms, restore the
event-to-support computation, compile the public instruction/step/resource
projections, then build and run independent positive/adversarial grading tests.
Source paper text and grader gold must not appear in a public instruction or
public Git history. A public `tests/` directory cannot hide answer keys.