# Input contract

The bundled 1666 K cohort covers DAP-2, PAP-2 and PAP-H2, each with three
independent velocity seeds and 192 initial A sites per seed. The inputs are
selected, path-free scientific fields from atom-identified first-exit and
independent local-geometry ledgers. They retain observed events, not simulated
or invented examples. The total size is 333,936 bytes.

| Bundled input | Role | SHA-256 |
| --- | --- | --- |
| [`data/exits.csv`](data/exits.csv) | First persistent A-site exit: heavy-atom identity, onset at 10 fs resolution and operation | `cf2cbe2c19ffa591a86f83503f56608f09c981292e710ac24595ed6491cccf1b` |
| [`data/neighborhoods.csv`](data/neighborhoods.csv) | Fixed atom-identity join from each A site to eight neighboring K units | `9acafb0ec24bbef0350cd584f98bd430ce6e7fc288ad11ec8fc499fb50b6fc05` |
| [`data/k_sites.csv`](data/k_sites.csv) | Independent, 100 fs-grid K–Cl6 500 fs persistent-loss onset and censoring | `cba8c8243a161c35c491a11d214d62d4be1b9135d683bb8f7999bb5017cc03e9` |

`scripts/prepare_inputs.py` records the source SHA-256 values and selects
these fields from the archived event ledgers. It excludes source machine paths,
run logs and already-joined timing results.

The analysis joins chemical first exits to the median persistent loss of each
site's eight fixed neighboring K–Cl6 units. Seed identity remains explicit in
the per-site records. Net N–H loss identifies a bond operation rather than the
immediate acceptor of the transferred hydrogen.