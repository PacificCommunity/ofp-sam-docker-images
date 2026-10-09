# KIMSA local CPU runtime

This candidate combines the existing R/RTMB company image, official CPU llama.cpp b11429, official Node v24.21.0 and one pinned public Qwen3 0.6B GGUF. It contains no KIMSA source, private profiles, credentials or user data. The Dockerfile pins all three Linux amd64 images by their child manifest digest.

The recipe is currently **source only: unbuilt and unqualified**. The existing repository workflow builds and publishes a changed image folder after a main-branch push. Review and a successful build must precede use of a newly published digest in company jobs.

## Build checks

The build first runs all 25 inert model-input fixtures. It then performs one verified HTTPS acquisition of the public model, with no automatic retry. The entire 522,640,096-byte body must match SHA256 `7f4030143c1c477224c5434f8272c662a8b042079a0a584f0a27a1684fe2e1fa` before an exclusive read-only publication. A late or failed final receipt revokes that publication. The acquisition has a cooperative 110-second acceptance limit inside an external 120-second process timeout; this does not guarantee cleanup after abrupt loss or a kernel stall. The model stays at `/opt/kimsa/models/qwen3-0.6b.gguf`, mode 0444, in a mode 0555 directory. There is no startup download.

Build smoke checks require Linux amd64, R >= 4.5, RTMB, jsonlite >= 2.0.0, the unchanged base R library paths/package versions, Node exactly v24.21.0 and the pinned llama-server version/revision. Actual executable file hashes and model hash are written to `/opt/kimsa/provenance/build-smoke.json`. `--version` checks prove only that these executable starts work in the built image. They do not qualify model loading, the server API, KIMSA integration or scientific results.

All 18 inert CPU-closure fixtures must also pass. Before starting llama-server, the smoke inventories the pinned server stage's flat `llama`, `llama-server`, and CPU shared-library families. Ordinary files are hashed completely. Library aliases may contain only an existing library basename in the same directory; the report retains each literal target, ordered alias chain and exact ordinary target digest. Escapes, dangling/cyclic aliases, directory/executable aliases, special files, unexpected entries and GPU backend names are refused. The source allowlist is not a claim that actual layer contents or the complete system ELF dependency closure have been observed. An unexpected actual member fails the build for further review.

The previous base entrypoint and optional runtime updater are disabled. R library paths and installed base dependencies remain inherited. There are no apt/R/Node package updates, npm/yarn operations, build secrets or private Git installs.

## Commands

The default command is `python3`, so Kflow2 can supply a reviewed task command. Nothing starts a server automatically. A manually authorised company task can start the fixed loopback CPU server with:

```sh
python3 -B /opt/kimsa/runtime/serve.py
```

The launcher uses 127.0.0.1:8080, two CPU threads, one slot, a 4096-token context, zero GPU layers, offline mode and disabled prompt cache reuse. `LD_LIBRARY_PATH=/opt/llama` applies to that child only. It does not expose a network service outside the container or add a qualified model profile to KIMSA. Any different context, argv, route or client contract needs a separate frozen execution plan.

## Provenance and remaining gates

`provenance/runtime-provenance.json` records the immutable image digests, publisher source revisions and exact model/manifest hashes. `metadata/metadata-v2/` retains the bounded primary OCI index/manifest/config responses and public source/license text. Its successful metadata retrieval used normal system TLS; the earlier local Python trust-store refusals remain in `metadata/` as contrary evidence. No image layers, runtime binaries or model body were downloaded or executed on the Mac.

The GGUF comes from the public Ollama Qwen3 artifact. Its manifest attaches an Apache-2.0 license; the upstream Qwen model card and license were also checked at an exact revision. This is provenance for the named publisher artifact, not an assertion that quantized bytes equal the original upstream weight files. Attached and upstream license/copyright text is preserved alongside llama.cpp's MIT license and the Node image's own license text. Base image notices remain inherited.

After an actual CI build, freeze the resulting immutable image digest. Company Condor checks must then verify the complete existing eight builder tests with actual Node and zero skips, unchanged R checks, model/server API compatibility, saved generation and a separate saved replay. These remain unrun for this candidate. Existing jobs retain their original image and identities.

Image inputs/build work are distinct from job-generated outputs. The existing output/file/log/resource limits remain in force; this recipe makes no output-cap exemption, hard memory, speed or image-pull timing claim. Failed partial runtime/model jobs and uncertain jobs do not become accepted input parents through this recipe.
