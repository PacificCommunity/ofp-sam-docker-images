# tuna-flow

Docker image for running tuna assessment Kflow workflows:

```text
ghcr.io/pacificcommunity/tuna-flow:latest
```

The image includes the MFCL executable, Quarto, FLR/MFCL dependencies, and
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

If GitHub returns `401`, `403`, or `404` for an optional private package, the
container keeps the installed package if present, otherwise skips that package.
Set `KFLOW_RUNTIME_REQUIRE_PRIVATE_PACKAGES=true` only for workflows that must
fail immediately when a private package cannot be checked or installed.

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
docker build tuna-flow/
```
