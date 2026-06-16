# tuna-flow

Docker image for running tuna assessment Kflow workflows:

```text
ghcr.io/pacificcommunity/tuna-flow:latest
```

The image includes the MFCL executable, Quarto, FLR/MFCL dependencies, and
startup tooling for optional private workflow packages used by specific Kflow
job stages:

- `mfclrtmb` from `PacificCommunity/ofp-sam-mfclrtmb`
- `mfclkit` from `PacificCommunity/ofp-sam-mfclkit`
- `mfclshiny` from `PacificCommunity/mfclshiny`
- `KflowKit` from `kyuhank/KflowKit`

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
