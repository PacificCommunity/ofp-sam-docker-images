#!/usr/bin/env bash
set -e

# Kflow transfers job_env.sh into the job sandbox. CondorBox-based workflows
# may still provide job_env.txt. Load either before starting the requested job.
for env_file in job_env.sh job_env.txt; do
  if [[ -f "$env_file" ]]; then
    set -a
    # shellcheck source=/dev/null
    source "$env_file"
    set +a
    break
  fi
done

# The report and workflow packages are fixed at image build time. Do not install
# or update packages during container startup: a runtime job must be reproducible
# without a GitHub/CRAN token or network access.

if [[ "$#" -eq 0 ]]; then
  set -- /init
fi

exec "$@"
