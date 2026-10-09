FROM --platform=linux/amd64 ghcr.io/ggml-org/llama.cpp:server-b11429@sha256:a7c742ec2070a17d715c02d4329c049a984c81c3234f9ab14bdb14e46b077317 AS llama_cpu
FROM --platform=linux/amd64 docker.io/library/node:24.21.0-bookworm-slim@sha256:51b1100cc2a83d370c6a60952e3f2989c8a43159d0e38586e090f3b3326efefd AS node_cpu

FROM --platform=linux/amd64 ghcr.io/pacificcommunity/tuna-flow:v2.5@sha256:c87f1f6d9d4f62dc447844b58afe35f96af175bf933cb6cffbbbe39a59172360 AS public_model
USER root
ENV PYTHONDONTWRITEBYTECODE=1 KFLOW_RUNTIME_UPDATE=off
ENTRYPOINT []
COPY runtime/fetch_model.py runtime/test_fetch_model.py /opt/model-build/
RUN mkdir -m 0700 /opt/model-fixtures /opt/model-input && \
    timeout --signal=TERM --kill-after=5s 120s python3 -B /opt/model-build/test_fetch_model.py --output-dir /opt/model-fixtures && \
    timeout --signal=TERM --kill-after=5s 120s python3 -B /opt/model-build/fetch_model.py --output-dir /opt/model-input

FROM --platform=linux/amd64 ghcr.io/pacificcommunity/tuna-flow:v2.5@sha256:c87f1f6d9d4f62dc447844b58afe35f96af175bf933cb6cffbbbe39a59172360
USER root
ENV PYTHONDONTWRITEBYTECODE=1 KFLOW_RUNTIME_UPDATE=off
ENTRYPOINT []
COPY runtime/smoke.py runtime/serve.py runtime/test_smoke.py /opt/kimsa/runtime/
COPY provenance/ /opt/kimsa/provenance/
COPY licenses/ /opt/kimsa/licenses/
RUN timeout --signal=TERM --kill-after=5s 60s python3 -B /opt/kimsa/runtime/smoke.py --mode baseline --output /opt/kimsa/provenance/base-runtime.json
RUN mkdir -m 0700 /opt/cpu-closure-fixtures && \
    timeout --signal=TERM --kill-after=5s 120s python3 -B /opt/kimsa/runtime/test_smoke.py --output-dir /opt/cpu-closure-fixtures && \
    cp /opt/cpu-closure-fixtures/FIXTURES.json /opt/kimsa/provenance/cpu-closure-fixtures.json
COPY --from=llama_cpu /app/ /opt/llama/
COPY --from=node_cpu /usr/local/bin/node /usr/local/bin/node
COPY --from=node_cpu /usr/local/LICENSE /opt/kimsa/licenses/Node-LICENSE.txt
COPY --from=public_model /opt/model-input/qwen3-0.6b.gguf /opt/kimsa/models/qwen3-0.6b.gguf
COPY --from=public_model /opt/model-input/MODEL-INPUT.json /opt/kimsa/provenance/MODEL-INPUT.json
COPY --from=public_model /opt/model-fixtures/FIXTURES.json /opt/kimsa/provenance/model-input-fixtures.json
RUN chmod 0555 /opt/kimsa/models && chmod 0444 /opt/kimsa/models/qwen3-0.6b.gguf && \
    timeout --signal=TERM --kill-after=5s 60s python3 -B /opt/kimsa/runtime/smoke.py --mode final --baseline /opt/kimsa/provenance/base-runtime.json --output /opt/kimsa/provenance/build-smoke.json
WORKDIR /workspace
CMD ["python3"]
