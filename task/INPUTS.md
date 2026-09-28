# Input and release contract (review draft)

The proposed target is the 1666 K cohort for DAP-2, PAP-2 and PAP-H2, with
three independent velocity seeds and 192 initial A sites per trajectory. The
agent's eventual instructions must name concrete, versioned, publicly
retrievable inputs. None of the resources below has a verified public archive
yet; no internal filesystem path or private network connection is an access
method.

| Required resource | Role | Release status |
| --- | --- | --- |
| Crystal structures, atom identity and 300 K equilibration | Build fixed A-site neighborhoods and reference K–Cl cutoff | Public bundle to verify |
| Nine 1666 K production trajectories, sampled every 10 fs | Recover chemical first exits and geometric time series | Public bundle to verify |
| Model and reference data used to produce the trajectories | Reproduce model training and dynamics in a full end-to-end task | Public route and version to verify |
| Molecular history generation and geometric timing recipe | Resolve 500 fs persistent first exits and 500 fs support loss | Portable implementation to review |

The underlying study already has separate chemical histories, a geometric
analysis and compact plot tables. The plot tables can check published
aggregates, but cannot rebuild the event-to-support join. An analysis-only
task can start from **real** released trajectory or per-event inputs if it is
named as such; a full task must also include the model-training and dynamics
stages that generated its data. Do not score claims about immediate transfer
to intact perchlorate from net N–H loss alone.

Release each large asset outside Git with a stable URL or accession, checksum,
size and use terms; declare its resolution and atom-ID schema. Until at least
one complete input route is public and independently tested, this repository
remains a review draft and makes no end-to-end reproducibility claim.