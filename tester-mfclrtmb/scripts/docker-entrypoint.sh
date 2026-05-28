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

if ! bash /usr/local/bin/30-update-mfclrtmb; then
  echo "[mfclrtmb-update] Startup update failed; continuing container startup." >&2
fi

if [[ "$#" -eq 0 ]]; then
  set -- /init
fi

exec "$@"