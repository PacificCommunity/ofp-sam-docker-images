# tuna-flow

Docker image for running tuna assessment Kflow workflows:

```text
ghcr.io/pacificcommunity/tuna-flow:v2.4
ghcr.io/pacificcommunity/tuna-flow:v2.3
ghcr.io/pacificcommunity/tuna-flow:v2.2
ghcr.io/pacificcommunity/tuna-flow:latest
```

The image includes the MFCL executable, Quarto, FLR/MFCL dependencies, and
startup tooling for optional private workflow packages used by specific Kflow
job stages:

- `mfclrtmb` from `PacificCommunity/ofp-sam-mfclrtmb`
- `mfclkit` from `PacificCommunity/ofp-sam-mfclkit`
- `mfclshiny` from `PacificCommunity/mfclshiny`
- `KflowKit` from `kyuhank/KflowKit`

Current MFCL executable:

- installed path: `/home/mfcl/mfclo64`
- MULTIFAN-CL base version: `2.2.7.9`
- image executable version: `2.4.0-strict-tag-nb`
- version code: `v24-strict-tag-nb`
- custom build date: `2026-07-14`
- source: `kyuhank/ofp-sam-mfcl@fe1fc5e`
- base source: `PacificCommunity/ofp-sam-mfcl@de4abeca920063bf234ce66ec3a0f043c56e885f`
- variant: `strict-tag-nb`
- sha256:
  `bb7cf890bc143313e418abb76c714b27bf08f3c61a22a4c2f532d39e69c4145c`
- in-image record: `/home/mfcl/mfclo64.version`
- compatibility paths:
  - `/home/mfcl/mfclo64_2026`
  - `/home/mfcl/mfclo64_2026_07_14_v24_strict_tag_nb`

`tuna-flow:v2.4` contains a custom build based on MULTIFAN-CL 2.2.7.9 with an
experimental strict conditional post-mixing tag bootstrap interface. The
ordinary assessment path is unchanged when the strict tag environment variables
are not set. The local qualification artifact showed byte-identical inactive
behaviour against the 2.2.7.9 base and validated the native conditional tag
cell export, sparse negative-binomial draw, truth preflight, receipt checks, and
a short frozen-refit optimizer smoke test.

The strict tag sidecar is compact because it stores only non-zero pseudo cells.
It is used by `mfclkit` self-test diagnostics when the fitted model flags match
the supported native v6 interface. Unsupported tag likelihood routes continue
to use the established mechanistic `sim_realtag` process simulator.

Image tag `v2.3` remains available for the native real-tag expectation build,
and `v2.2` remains available for the unmodified 2026-07-11 executable.

Historical MFCL executable for reproducing the 2023 BET diagnostic step:

- installed path: `/home/mfcl/mfclo64_2023_diagnostic_2.2.2.0`
- compatibility path: `/home/mfcl/mfclo64_2023_diagnostic`
- version record from `MFCL/plot-11.par.rep`: `2.2.2.0`
- source: `PacificCommunity/ofp-sam-bet-2023-diagnostic@81fc412`, path `MFCL/mfclo64`
- sha256:
  `b872c4d049a305d6d89600aea50ffb5d714ab1e5083c44cc712464612dd66aa2`
- in-image record: `/home/mfcl/mfclo64_2023_diagnostic_2.2.2.0.version`

The default `MFCL_EXECUTABLE` remains the current 2026 executable. Workflows that
need to reproduce the 2023 diagnostic model should explicitly set
`PROGRAM_PATH=/home/mfcl/mfclo64_2023_diagnostic_2.2.2.0` for that step only.

Version `v1.6` also includes report image optimization tools used by BET plot
jobs:

- `pngquant` for high-reduction lossy PNG compression.
- `optipng` and ImageMagick for PNG cleanup and fallback recompression.
- `cwebp` for compact HTML figure sidecars.
- `jpegoptim` and ImageMagick JPEG conversion for compact PDF sidecars.

Keeping these tools in the image is preferred over installing them inside each
Kflow job. Jobs start faster, logs stay cleaner, and every submitter uses the
same optimizer versions.

Version `v2.1` preinstalls the public RTMB toolchain used by `mfclrtmb`:

- `RcppEigen`
- `TMB`
- `RTMB`

`mfclrtmb` itself remains a runtime-installed private package, like
`mfclshiny` and `mfclkit`, so Kflow jobs can pin a branch or commit without
rebuilding the public image. Baking these public dependencies into the image
avoids rebuilding `TMB` and `RTMB` from source in every Suva job.

The image intentionally keeps the workflow-critical command-line tools but avoids
large optional stacks that are not needed by current Kflow BET stepwise/results
jobs, such as GDAL/PROJ/GEOS, Java, and R-only image packages like `magick`,
`rsvg`, and `ragg`. It also avoids the very large `texlive-fonts-extra` bundle
while installing the small `fontawesome5` LaTeX package needed by Quarto/PDF
rendering. This keeps the full Kflow runtime smaller while preserving MFCL runs,
Quarto report rendering, and PNG/WebP/JPEG optimization.

This image is safe to publish publicly: private package source code and GitHub
tokens are not baked into the image. Private packages are installed or updated
only when `KFLOW_RUNTIME_UPDATE=auto` is set and `GIT_PAT` or `GITHUB_PAT` is
provided at runtime.
Tokens should be passed through the job environment or another runtime secret
mechanism, not as Docker build arguments.

By default `KFLOW_RUNTIME_UPDATE=off`, so public smoke workflows never contact
private GitHub repositories. Set `KFLOW_RUNTIME_REQUIRE_PRIVATE_PACKAGES=true`
when a job must fail fast unless all private helper packages are installed.

Useful runtime variables:

- `KFLOW_RUNTIME_UPDATE=off`: do not contact private GitHub repositories.
- `KFLOW_RUNTIME_UPDATE=auto`: enable startup checks when a token is present.
- `KFLOW_RUNTIME_UPDATE_INTERVAL_HOURS=24`: minimum time between checks.
- `KFLOW_RUNTIME_QUIET_INSTALL=true`: reduce R package build output when an
  update actually installs a package.
- `KFLOW_RUNTIME_FORCE_UPDATE=1`: force reinstall from GitHub.
- `KFLOW_RUNTIME_REQUIRE_PRIVATE_PACKAGES=false`: skip missing private packages
  when no token is available.
- `KFLOW_RUNTIME_PACKAGES`: package repo/ref specs to check or install. When it
  is unset or empty, the container uses the packages already baked into the
  image and does not contact GitHub.
- `KFLOW_RUNTIME_PACKAGES=none`: explicitly skip private package checks; useful
  for report-only jobs that only render existing figures/tables.
- `GIT_PAT` or `GITHUB_PAT`: token with read access to the private package repos.

If GitHub returns `401`, `403`, or `404` for an optional private package, the
container keeps the installed package if present, otherwise skips that package.
Set `KFLOW_RUNTIME_REQUIRE_PRIVATE_PACKAGES=true` only for workflows that must
fail immediately when a private package cannot be checked or installed.

Package refs can be pinned at runtime with `KFLOW_RUNTIME_PACKAGES`:

```bash
KFLOW_RUNTIME_PACKAGES="\
mfclkit=PacificCommunity/ofp-sam-mfclkit@<sha-or-tag>,\
mfclshiny=PacificCommunity/mfclshiny@<sha-or-tag>"
```

Use only the packages a stage actually needs. For example, model-input recipe
jobs usually need `mfclkit`, `MFCL_BACKEND=mfclrtmb` jobs add `mfclrtmb`, plot
jobs using mfclshiny request `mfclshiny`, and report rendering jobs can leave
`KFLOW_RUNTIME_PACKAGES` unset or set it to `none`.

Build the public base image without private secrets:

```bash
docker build tuna-flow/
```
