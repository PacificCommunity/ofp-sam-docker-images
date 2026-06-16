# bet2026-flow

Docker image for running the BET 2026 Kflow workflow:

```text
ghcr.io/pacificcommunity/bet2026-flow:latest
```

The image includes the BET MFCL executable, Quarto, FLR/MFCL dependencies, and
private workflow packages used by Kflow jobs:

- `mfclrtmb` from `PacificCommunity/ofp-sam-mfclrtmb`
- `mfclkit` from `PacificCommunity/ofp-sam-mfclkit`
- `mfclshiny` from `PacificCommunity/mfclshiny`
- `KflowKit` from `kyuhank/KflowKit`

Private packages are installed at build time using the `github_pat` BuildKit
secret. At container startup, the image can also update only those private
packages when `GIT_PAT` or `GITHUB_PAT` is available.

Useful runtime variables:

- `KFLOW_RUNTIME_UPDATE=auto`: enable startup checks. Use `never` to disable.
- `KFLOW_RUNTIME_UPDATE_INTERVAL_HOURS=24`: minimum time between checks.
- `KFLOW_RUNTIME_FORCE_UPDATE=1`: force reinstall from GitHub.
- `KFLOW_RUNTIME_PACKAGES`: override package repo/ref specs.

Build-time refs can be pinned with:

```bash
docker build \
  --secret id=github_pat,env=GITHUB_PAT \
  --build-arg MFCLRTMB_REF=<sha-or-tag> \
  --build-arg MFCLKIT_REF=<sha-or-tag> \
  --build-arg MFCLSHINY_REF=<sha-or-tag> \
  --build-arg KFLOWKIT_REF=<sha-or-tag> \
  bet2026-flow/
```

