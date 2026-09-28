# Input contract

The target is the 1666 K cohort for DAP-2, PAP-2 and PAP-H2, with three
independent velocity seeds and 192 initial A sites per trajectory. The input
record specifies atom identities, frame spacing, provenance and checksums.

| Input | Role |
| --- | --- |
| Crystal structures, atom identity and 300 K equilibration | Build fixed A-site neighborhoods and reference K–Cl cutoff |
| Nine 1666 K production trajectories, sampled every 10 fs | Recover chemical first exits and geometric time series |
| Molecular history generation and geometric timing recipe | Resolve 500 fs persistent first exits and 500 fs support loss |

The analysis joins chemical first exits to the median persistent loss of each
site's eight fixed neighboring K–Cl6 units. Seed identity remains explicit in
the per-site records. Net N–H loss identifies a bond operation rather than the
immediate acceptor of the transferred hydrogen.