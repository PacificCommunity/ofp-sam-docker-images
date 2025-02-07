![Workflow Status](https://github.com/PacificCommunity/ofp-sam-docker-images/actions/workflows/build-and-push.yml/badge.svg)

For reproducibility, each top-level directory contains a Dockerfile and associated files to build a Docker image. The GitHub Actions workflow automatically builds and pushes these images to GitHub Container Registry (GHCR) under the `PacificCommunity` organisation.

# Overview

This repository includes a GitHub Actions workflow that:

1. Detects changed top-level directories (e.g., `skj-2025/`, `yft-2025/`).
2. Builds Docker images for each changed directory.
3. Pushes them to GitHub Container Registry (GHCR) under the `pacificcommunity` organisation.
4. Either uses a user-specified version (provided via `workflow_dispatch`) or automatically increments the minor version if previous tags exist.

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

# Adding or Updating Docker Images

## Adding a New Docker Image

1. Create a **new folder** at the top level of this repository, for example `tuna-2025/`.
2. Put a **Dockerfile** inside that folder.
3. Commit and push your changes (this will trigger the GitHub Actions workflow). 
   - The GitHub Actions workflow will detect the new directory, build a new Docker image, and push it to GHCR.

## Updating an Existing Docker Image

1. **Modify** the Dockerfile in one of the existing folders (e.g. `skj-2025/Dockerfile`).
2. Commit and push your changes  (this will trigger the GitHub Actions workflow).   
   - The workflow detects changes in that directory’s Dockerfile and automatically rebuilds and pushes an updated image to GHCR.

# Automatic GitHub Actions Trigger

- **Workflow trigger**:  
  Whenever you push changes (especially Dockerfile changes), GitHub Actions automatically runs the build-and-push workflow. If anything goes wrong in the build or push process, the workflow will **fail**, and you can check the logs in the “Actions” tab for details.

- **Failing workflow**:  
  If the Docker build fails, version detection fails, or pushing to GHCR fails, you will see a **red “X”** in the GitHub Actions run. View the logs to diagnose and fix the issue before retrying.
