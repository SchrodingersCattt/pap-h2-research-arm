# Input contract

The target is the 1666 K cohort for DAP-2, PAP-2 and PAP-H2, with three
independent velocity seeds and 192 initial A sites per trajectory. The input
record specifies atom identities, frame spacing, provenance and checksums.

The source cohort contains nine 1666 K trajectory files and nine matched 300 K
reference files (20,798,481,520 bytes in total). All 18 files were read and
their SHA-256 values matched the frozen source receipt. The corresponding
atom-resolved molecular histories and reaction-event records comprise another
18 files; their SHA-256 values also matched the same receipt. The independent
event-to-support join uses the following small, identified source records:

| Record | Size (bytes) | SHA-256 |
| --- | ---: | --- |
| `e2_first_exit_atom_links.csv` | 2,028,770 | `504569f95ccd475ed1fba6f555fb8f72c606f40e07e46ea6527d0b5802434b7a` |
| `a_k_neighborhoods.csv` | 316,921 | `e4522ad5280503d57b13af773e34040faebae6e38dbf3e564dff30ab966668d0` |
| `k_cl6_sites.csv` | 211,268 | `a2bc522b5cb3374d5825c2133227fe0b341ff4ee66dcf6e67879a19b4f55fdd7` |
| `e3_event_structure.csv` | 722,550 | `0dc3b43e818f983d0f7dc377e9736e960d852d0b8e50692abf14d7cc5e984582` |

| Input | Role |
| --- | --- |
| Crystal structures, atom identity and 300 K equilibration | Build fixed A-site neighborhoods and reference K–Cl cutoff |
| Nine 1666 K production trajectories, sampled every 10 fs | Recover chemical first exits and geometric time series |
| Molecular history generation and geometric timing recipe | Resolve 500 fs persistent first exits and 500 fs support loss |

The analysis joins chemical first exits to the median persistent loss of each
site's eight fixed neighboring K–Cl6 units. Seed identity remains explicit in
the per-site records. Net N–H loss identifies a bond operation rather than the
immediate acceptor of the transferred hydrogen.