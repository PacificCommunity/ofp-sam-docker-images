FROM python:3.12-alpine@sha256:b64631e04e4920160c50fbe8d8df828f7f35f06f425cb44aa09bca53e708a35a

LABEL org.opencontainers.image.source="https://github.com/PacificCommunity/ofp-sam-docker-images"
LABEL org.opencontainers.image.title="Fisheries workflow"
LABEL org.opencontainers.image.description="Python and SQLite runtime for the fisheries workflow paper and demonstration"

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /workspace

RUN python - <<'PY'
import asyncio
import concurrent.futures
import csv
import hashlib
import html
import io
import json
import math
import multiprocessing
import platform
import random
import sqlite3
import ssl
import statistics
import urllib.request
import zipfile
import zlib

assert platform.python_version() == "3.12.14", platform.python_version()
assert sqlite3.sqlite_version == "3.53.4", sqlite3.sqlite_version
assert ssl.create_default_context().get_ca_certs(), "No trusted CA certificates"
with sqlite3.connect(":memory:") as connection:
    connection.execute("CREATE TABLE catches (catch REAL, effort REAL)")
    connection.executemany("INSERT INTO catches VALUES (?, ?)", [(10, 2), (20, 3)])
    assert connection.execute("SELECT SUM(catch) / SUM(effort) FROM catches").fetchone() == (6.0,)
with zipfile.ZipFile(io.BytesIO(), "w", zipfile.ZIP_DEFLATED) as archive:
    archive.writestr("runtime.json", json.dumps({"sqlite": sqlite3.sqlite_version}))
print(json.dumps({"python": platform.python_version(), "sqlite": sqlite3.sqlite_version,
                  "platform": platform.system(), "architecture": platform.machine(),
                  "openssl": ssl.OPENSSL_VERSION, "zlib": zlib.ZLIB_RUNTIME_VERSION}))
PY

CMD ["python"]
