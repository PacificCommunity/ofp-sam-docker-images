# Fisheries workflow

R, RTMB and Quarto environment for the fisheries workflow demonstration.
All data preparation, GLM CPUE analyses, surplus-production assessments,
MSE projections and QMD report jobs run inside this image. Packages are
installed when the image is built, so an analysis needs no package downloads.

The runtime contains R 4.6.0, RTMB 2.0, TMB 1.9.25, jsonlite 2.0.0,
Quarto 1.9.37 and its R reporting packages. Python coordinates jobs, records
and SQLite files. Its observed version and all main R package versions are
saved in `/opt/fisheries-runtime/runtime.json`. The image build checks a small
RTMB fit and a genuine Quarto HTML render. Source packages and Quarto are
verified against the SHA-256 values in the recipe and package lock.

Analysis code and synthetic data are supplied by the demo checkout or release,
so their revisions can be recorded independently of the software image.
The publishing workflow creates the next version tag and `latest`.
This revision is intended for `ghcr.io/pacificcommunity/fisheries-workflow:v1.1`.
Use the resolved digest for execution and retain it with each job record.
The published image uses Linux amd64; ARM machines require amd64 emulation.

## Run the demonstration

From a checkout or unpacked release:

```bash
image="ghcr.io/pacificcommunity/fisheries-workflow:v1.1"
docker pull --platform linux/amd64 "$image"
runtime_image="$(docker inspect --format '{{index .RepoDigests 0}}' "$image")"
mkdir -p outputs
docker run --rm --platform linux/amd64 --network none \
  --user "$(id -u):$(id -g)" \
  --env PAPER_RUNTIME_IMAGE="$runtime_image" \
  --volume "$PWD:/workspace:ro" --volume "$PWD/outputs:/outputs" \
  --workdir /workspace "$runtime_image" \
  python run.py --output /outputs
```

Open `outputs/assessment_report/report.html`. Each report retains the inputs
and source records used by its corresponding analysis. To check the mounted
source, use the same resolved image and `PAPER_RUNTIME_IMAGE` environment
variable with `python -m unittest discover -s tests -v`.

The hosted demonstration pulls the immutable image and runs `cloud/run.py`
inside it. Offline reader files display preserved results; they do not execute
new analyses. Keep the image and original source/input files to repeat a run.
