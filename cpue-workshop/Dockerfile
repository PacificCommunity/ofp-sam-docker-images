FROM python:3.12-alpine@sha256:b64631e04e4920160c50fbe8d8df828f7f35f06f425cb44aa09bca53e708a35a

LABEL org.opencontainers.image.source="https://github.com/PacificCommunity/ofp-sam-docker-images"
LABEL org.opencontainers.image.description="Minimal Python and SQLite runtime for the synthetic longline CPUE workflow"

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /work
RUN python -c "import csv, hashlib, html, json, math, sqlite3; assert sqlite3.connect(':memory:').execute('select 1').fetchone() == (1,)"
CMD ["python", "run.py"]
