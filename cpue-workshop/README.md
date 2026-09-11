# CPUE workshop runtime

Python 3.12 and SQLite for the [synthetic CPUE workflow](https://github.com/kyuhank/cpue-actions-demo).
No package installation at startup. The base image is pinned by digest.
Analysis code is checked out separately; no data, credentials or Kflow2 code are bundled.

After checking out the demo repository:

```bash
docker run --rm --network none --user "$(id -u):$(id -g)" \
  -v "$PWD:/work" -w /work \
  -e TOY_CODE_COMMIT="$(git rev-parse HEAD)" \
  -e TOY_DATA_COMMIT="$(git rev-parse HEAD)" \
  ghcr.io/pacificcommunity/cpue-workshop:v1.0 python run.py
```

Open `outputs/report.html`. In Actions, run `python pipeline/extract.py`,
`python pipeline/cpue.py`, `python pipeline/assessment.py` or `python pipeline/report.py`
as the container command for each dependent job. Pass both checkout SHAs and run IDs
as environment variables. Use a `docker run` step: Alpine is not suitable as a
job-level container for JavaScript-based Actions.
