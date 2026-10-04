# Fisheries workflow

Python and SQLite runtime for the fisheries workflow paper and its demonstration:
data preparation, CPUE standardisation, stock assessment and management strategy
evaluation. The demonstration uses Python's standard library; no packages are
installed when an analysis starts.

The image preserves Python 3.12.14 and SQLite 3.53.4 with the same digest-pinned
Python base used for the recorded example runs. The build checks these versions,
SQLite queries, compressed archives and trusted HTTPS certificates.
Analysis code and synthetic data are supplied by a separate demo checkout or
release, so their revisions can be recorded independently of the runtime.

Image: `ghcr.io/pacificcommunity/fisheries-workflow`.
The repository's publishing workflow creates a version tag and `latest`.
For reproducible runs, use the published `@sha256:…` digest rather than `latest`.
The published image uses Linux amd64, matching the recorded runs. Docker on an
ARM machine needs amd64 emulation for the commands below.

## Run the demonstration

From a checkout or unpacked release containing `run.py`, `workflow/` and `data/`:

```bash
mkdir -p outputs
docker run --rm --platform linux/amd64 --network none --user "$(id -u):$(id -g)" \
  --volume "$PWD:/workspace:ro" --volume "$PWD/outputs:/outputs" \
  --workdir /workspace \
  ghcr.io/pacificcommunity/fisheries-workflow:v1.0 \
  python run.py --output /outputs
```

Open `outputs/assessment_report/report.html`. Run the native checks with the same
source mounted into the image:

```bash
docker run --rm --platform linux/amd64 --network none \
  --volume "$PWD:/workspace:ro" --workdir /workspace \
  ghcr.io/pacificcommunity/fisheries-workflow:v1.0 \
  python -m unittest discover -s tests -v
```

The image can also run `cloud/run.py` with the demonstration's separately
configured service. Its execution record should include the exact image digest.
In GitHub Actions, use a `docker run` step; Alpine is unsuitable as a job-level
container for JavaScript Actions.
