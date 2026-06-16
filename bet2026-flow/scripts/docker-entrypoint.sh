#!/usr/bin/env bash
set -e

# Kflow transfers job_env.sh into the job sandbox. CondorBox-based workflows
# may still provide job_env.txt. Load either before runtime package checks.
for env_file in job_env.sh job_env.txt; do
  if [[ -f "$env_file" ]]; then
    set -a
    # shellcheck source=/dev/null
    source "$env_file"
    set +a
    break
  fi
done

if [[ -z "${R_LIBS_USER:-}" ]]; then
  export R_LIBS_USER="${KFLOW_RUNTIME_LIBRARY:-/home/rstudio/R/site-library}"
fi

if bash /usr/local/bin/30-update-kflow-runtime-packages; then
  :
else
  update_status=$?
  case "${KFLOW_RUNTIME_REQUIRE_PRIVATE_PACKAGES:-false}" in
    1|true|TRUE|yes|YES|on|ON) exit "$update_status" ;;
  esac
  if [[ "$update_status" -eq 42 ]]; then
    echo "[kflow-runtime-update] A required private package is missing and no GitHub token was provided. Set GIT_PAT or GITHUB_PAT at runtime, or leave KFLOW_RUNTIME_REQUIRE_PRIVATE_PACKAGES=false for smoke workflows." >&2
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
