# Container environment

`environment/Dockerfile` selects the Paper2ARM base image and sets the working
directory. It has exactly two instructions:

```dockerfile
FROM dp-harbor-registry.cn-zhangjiakou.cr.aliyuncs.com/public/paper2arm-env:v1.0-20260708
WORKDIR /app
```

The Dockerfile does not copy this repository into the image or install the
analysis tools, trajectories or Python dependencies. The base image is an
execution environment, not the scientific workflow or a containerized copy
of the research machine. Task inputs and produced files live outside the
image; write submission artifacts under `/app/outputs`.

## What has been verified

The registry returned HTTP 200 for the exact image tag's Docker manifest on
2026-09-28, with digest
`sha256:e56af8bcfc37be6ee859a7867ad2a3a941f9b576445a56378c6a4a5a017b57d2`.
Its image configuration declares Linux/amd64, `/root/code` as the base
working directory and `/bin/bash` as the default command. The Dockerfile
changes the working directory to `/app`. The manifest contains seven layers
(about 1.34 GB of compressed layers). A registry manifest check establishes
that the image exists and is anonymously readable; it does not establish
which scientific programs are installed or that it runs on a given host.

## Local use (PowerShell with Docker Engine)

From the root of this ARM repository, build the small local wrapper image:

```powershell
docker build --pull -f environment/Dockerfile -t pap-h2-arm-base .
docker run --rm pap-h2-arm-base python3 --version
```

The first build downloads the base image; the Dockerfile itself adds no
software. The second command checks Python in **your** running container.
Mount the repository to work with files without baking data into the image:

```powershell
docker run --rm -it --mount "type=bind,source=$((Get-Location).Path),target=/app" -w /app pap-h2-arm-base /bin/bash
```

Inside that shell, use the task specification and input contract to obtain
inputs and generate `/app/outputs/site_events.csv` and
`/app/outputs/summary.json`. A bind mount keeps those outputs on the host;
`outputs/` is ignored by Git. Running the base image alone does not execute
the task or score its outputs.

## Harbor/LBG use

The Paper2ARM reference specifies this prebuilt image as the agent sandbox.
On LBG the task Dockerfile is not built; Harbor starts from the image itself,
passes the public instruction to the agent, and reads submission files from
`/app/outputs`. A separate verifier reads those files and writes its reward
under `/logs/verifier`. The local Docker commands above check the base
environment; they do not substitute for a Harbor execution or verifier test.