#!/usr/bin/env bash
set -e

# CondorBox transfers job_env.txt into the job sandbox; load it before startup
# checks so runtime package updates can see tokens such as GIT_PAT.
if [[ -f job_env.txt ]]; then
  set -a
  # shellcheck source=/dev/null
  source job_env.txt
  set +a
fi

if bash /usr/local/bin/30-update-mfclrtmb; then
  :
else
  update_status=$?
  if [[ "$update_status" -eq 42 ]]; then
    echo "[mfclrtmb-update] mfclrtmb is not installed and no GitHub token was provided. Set GIT_PAT or GITHUB_PAT, or use an image built with mfclrtmb preinstalled." >&2
    exit "$update_status"
  fi
  echo "[mfclrtmb-update] Startup update failed; continuing container startup." >&2
fi

if [[ "$#" -eq 0 ]]; then
  set -- /init
fi

exec "$@"