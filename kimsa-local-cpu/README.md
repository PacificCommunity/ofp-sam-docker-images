# KIMSA local CPU runtime

This Linux amd64 image combines the existing R/RTMB environment with CPU llama.cpp, Node.js and a bundled Qwen3 0.6B model for company Condor jobs. It provides the runtime for local LLM and Node-based UI work.

The Dockerfile adds public runtime files, provenance, licences, tools and the public model. KIMSA is loaded privately in the company job workspace.

## Usage

Choose this image in the company job configuration:

```text
ghcr.io/pacificcommunity/kimsa-local-cpu:v1.0@sha256:f8c2c211084793c405278a451d6f7a580a98237ab27a741cab17f806cc1c4deb
```

The default command is `python3`. Start the server inside the job with:

```sh
python3 -B /opt/kimsa/runtime/serve.py
```

The launcher uses `127.0.0.1:8080` inside the container, two CPU threads, one slot and a 4096-token context. It requests offline mode and performs no startup download. The read-only model is stored at `/opt/kimsa/models/qwen3-0.6b.gguf`.

## Checks and sources

The [CI build](https://github.com/PacificCommunity/ofp-sam-docker-images/actions/runs/37919250129) passed all 49 fixtures with zero skips, verified the complete model hash, and passed version-start checks for Node v24.21.0 and llama.cpp b11429. R, RTMB and jsonlite versions and library paths matched the base image.

Company checks for model loading, API compatibility, KIMSA integration, the eight UI builder tests, generation, saving and replay remain pending.

See [runtime provenance](provenance/runtime-provenance.json) for pinned versions and hashes, [metadata](metadata/) for source records and build history, and [licences](licenses/) for notices.
