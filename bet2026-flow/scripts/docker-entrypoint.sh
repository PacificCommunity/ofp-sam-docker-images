#!/usr/bin/env bash
set -e

# CondorBox transfers job_env.txt into the job sandbox. Load it before runtime
# package checks so GIT_PAT, GITHUB_PAT, and package override variables work.
if [[ -f job_env.txt ]]; then
  set -a
  # shellcheck source=/dev/null
  source job_env.txt
  set +a
fi

if [[ -z "${R_LIBS_USER:-}" ]]; then
  export R_LIBS_USER="${KFLOW_RUNTIME_LIBRARY:-/home/rstudio/R/site-library}"
fi

if bash /usr/local/bin/30-update-kflow-runtime-packages; then
  :
else
  update_status=$?
  if [[ "$update_status" -eq 42 ]]; then
    echo "[kflow-runtime-update] A required package is missing and no GitHub token was provided. Set GIT_PAT or GITHUB_PAT, or use an image with private packages preinstalled." >&2
    exit "$update_status"
  fi
  if [[ "$update_status" -eq 43 ]]; then
    echo "[kflow-runtime-update] A required package is missing and no writable runtime R library is available. Set R_LIBS_USER to a writable path." >&2
    exit "$update_status"
  fi
  echo "[kflow-runtime-update] Startup package update failed; continuing with bundled packages." >&2
fi

if [[ "$#" -eq 0 ]]; then
  set -- /init
fi

exec "$@"

