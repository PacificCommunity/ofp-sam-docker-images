![Workflow Status](https://github.com/PacificCommunity/ofp-sam-docker-images/actions/workflows/build-and-push.yml/badge.svg)

# Overview

This repository includes a GitHub Actions workflow that:

1. Detects changed top-level directories (e.g., `skj-2025/`, `yft-2025/`).
2. Builds Docker images for each changed directory.
3. Pushes them to GitHub Container Registry (GHCR) under the `pacificcommunity` organization.
4. Either uses a user-specified version (provided via workflow_dispatch) or automatically increments the minor version if previous tags exist.

# Key Features

- **Auto-incrementing version**:
  - Scans GHCR for the highest existing tag (e.g., `v1.4` or `1.4`) and increments to `1.5`.
  - Defaults to `1.0` if no valid version is found or the package does not exist.
- **User-specified version**:
  - If you manually dispatch the workflow and enter a version (e.g., `2.3`), that overrides auto-increment.
- **Top-level directory detection**:
  - Each changed directory is treated as a separate container image.
- **Lowercase Docker repository owner**:
  - Avoids Docker’s “repository name must be lowercase” errors.
- **Secure ephemeral Docker config**:
  - Credentials stored in a temporary directory to avoid leftover unencrypted passwords in the default Docker config.
