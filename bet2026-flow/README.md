# bet2026-flow

Docker image for running the BET 2026 Kflow workflow:

```text
ghcr.io/pacificcommunity/bet2026-flow:latest
```

The image includes the BET MFCL executable, Quarto, FLR/MFCL dependencies, and
startup tooling for private workflow packages used by Kflow jobs:

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
- `KFLOW_RUNTIME_FORCE_UPDATE=1`: force reinstall from GitHub.
- `KFLOW_RUNTIME_REQUIRE_PRIVATE_PACKAGES=false`: skip missing private packages
  when no token is available.
- `KFLOW_RUNTIME_PACKAGES`: override package repo/ref specs.
- `GIT_PAT` or `GITHUB_PAT`: token with read access to the private package repos.

Package refs can be pinned at runtime with `KFLOW_RUNTIME_PACKAGES`:

```bash
KFLOW_RUNTIME_PACKAGES="\
mfclrtmb=PacificCommunity/ofp-sam-mfclrtmb@<sha-or-tag>,\
mfclkit=PacificCommunity/ofp-sam-mfclkit@<sha-or-tag>,\
mfclshiny=PacificCommunity/mfclshiny@<sha-or-tag>,\
KflowKit=kyuhank/KflowKit@<sha-or-tag>"
```

Build the public base image without private secrets:

```bash
docker build bet2026-flow/
```
