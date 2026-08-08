# tuna-flow private runtime

`v2.7` is a sealed, reproducible runtime for MFCL assessment workflows and
report rendering. It is published as a **private** GitHub Container Registry
package:

```text
ghcr.io/pacificcommunity/tuna-flow-private:v2.7
```

The existing public `tuna-flow:v2.5` and `tuna-flow:v2.6` images are unchanged.

## Contents

The image contains Quarto, LaTeX, MFCL utilities, report-rendering tools, and
the workflow packages required by the current assessment repositories:

- `FLCore`, `FLR4MFCL`, `CondorBox`, and `tandoori`;
- `KflowKit`, `mfclrtmb`, `mfclkit`, and `mfclshiny`; and
- their required compiled R dependencies, including `TMB` and `RTMB`.

All package sources are installed when the image is built and pinned to exact
Git commits. Jobs do not install or update R packages at startup.

The MFCL executable is preserved from the `v2.5` image:

- path: `/home/mfcl/mfclo64`;
- version: `2.5.0-strict-tag-nb-dm-report`;
- source: `kyuhank/ofp-sam-mfcl@1321ccd`;
- SHA-256: `f5bc1e232a86e51f920bce7271d8e0930d0b160e4d18dc46de44078f0fa24cd0`.

The executable record is available at `/home/mfcl/mfclo64.version`. Compatible
paths `/home/mfcl/mfclo64_2026` and
`/home/mfcl/mfclo64_2026_07_18_v25_strict_tag_nb_dm_report` are also provided.
The historical 2023 diagnostic executable remains available at
`/home/mfcl/mfclo64_2023_diagnostic_2.2.2.0`.

## GitHub Actions and security

The build workflow receives `BUILD_GITHUB_PAT` only as a BuildKit secret while
installing private R packages. The token is neither printed nor copied into an
image layer. After installation, the Docker build verifies every pinned package
commit and verifies the MFCL executable checksum. The workflow then starts the
finished image and checks the executable and required R packages before push.

The package must remain private. Report workflows should authenticate only on
protected branches or release jobs with a read-only `GHCR_READ_TOKEN`; do not
grant a public repository direct Actions access to this package, because that
can expose package access to forked pull-request workflows.

Build `v2.7` with GitHub Actions using the required secrets:

- `BUILD_GITHUB_PAT`: read access to the private R-package repositories;
- `GHCR_TOKEN`: write access to this private container package.

For a local BuildKit build, provide the source-package token as a secret rather
than a build argument:

```bash
DOCKER_BUILDKIT=1 docker build \
  --secret id=github_pat,env=BUILD_GITHUB_PAT \
  -t tuna-flow-private:v2.7 tuna-flow/
```
