# Custom RStudio Docker Image with MFCL 2.2.7.2

This Docker image is based on the `rocker/rstudio:4.3.1` image and includes additional dependencies, R packages, and a custom `mfclo64` (version 2.2.7.2) file stored in `/home/mfcl/`.

## 📦 Installed Dependencies
The following dependencies are installed in the image:

- System libraries required for R packages:
  - `libclang-dev`, `libcurl4-openssl-dev`, `libxml2-dev`
  - `texlive-xetex`, `texlive-latex-extra`, `texlive-fonts-recommended`
  - `pandoc`, `make`, `openssh-client`
- `docker-compose` (version 2.23.0)
- R packages:
  - `ggplot2`, `rmdformats`, `GGally`, `rmarkdown`, `viridis`, `dplyr`, `cowplot`, `parallel`, `tidyr`, `patchwork`, `reshape2`, `iterators`, `remotes`, `tidyverse`
  - `FLCore` (from FLR repository)
  - `ofp-sam-flr4mfcl` (from PacificCommunity GitHub)
  - `ofp-sam-CondorBox` (from PacificCommunity GitHub)

## 🔹 Additional Customization
The following modifications were made to the `Dockerfile`:

1. **Created a new directory** `/home/mfcl/`:
   ```dockerfile
   RUN mkdir -p /home/mfcl


