FROM rocker/r-ver:4.6.0@sha256:6f05a1a8b8c52328f181593923909b01cbfd14c9caea93bf75ddc65e806d8eac

LABEL org.opencontainers.image.source="https://github.com/PacificCommunity/ofp-sam-docker-images"
LABEL org.opencontainers.image.title="Fisheries workflow"
LABEL org.opencontainers.image.description="R, RTMB and Quarto runtime for the fisheries workflow demonstration"

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    MAKEFLAGS=-j2 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python-is-python3 ca-certificates curl build-essential fonts-dejavu-core \
    pkg-config libuv1-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl --fail --location --retry 3 \
    https://github.com/quarto-dev/quarto-cli/releases/download/v1.9.37/quarto-1.9.37-linux-amd64.tar.gz \
    --output /tmp/quarto.tar.gz \
    && echo '78fcd90e983e3e7dbe3f0d1921cc10253c1eca7b92c20dd4bc2a3c1bca0a9af5  /tmp/quarto.tar.gz' | sha256sum --check \
    && tar --extract --gzip --file /tmp/quarto.tar.gz --directory /opt \
    && ln -s /opt/quarto-1.9.37/bin/quarto /usr/local/bin/quarto \
    && rm /tmp/quarto.tar.gz

COPY packages.lock.json install-runtime.py smoke.qmd /opt/fisheries-runtime/
RUN python /opt/fisheries-runtime/install-runtime.py

WORKDIR /workspace
CMD ["python"]
