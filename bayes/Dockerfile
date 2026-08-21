FROM rocker/r-ver:4.5.1

ARG QUARTO_VERSION=1.9.38

# 1. Disable interactive prompts and set Noumea timezone
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Pacific/Noumea

# 2. Install system libraries needed for R package building
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    gfortran \
    liblapack-dev \
    libblas-dev \
    libcurl4-openssl-dev \
    libxml2-dev \
    libssl-dev \
    pkg-config \
    wget \
    git \
    libfontconfig1-dev \
    libfreetype6-dev \
    libpng-dev \
    libtiff5-dev \
    libjpeg-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    pandoc \
    latexmk \
    latexdiff \
    lmodern \
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-plain-generic \
    ghostscript \
    poppler-utils \
  && rm -rf /var/lib/apt/lists/*

# Install Quarto for reviewer responses and other publication documents.
RUN curl -fsSL \
    "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.deb" \
    -o /tmp/quarto.deb \
  && apt-get update \
  && apt-get install -y --no-install-recommends /tmp/quarto.deb \
  && rm -f /tmp/quarto.deb \
  && rm -rf /var/lib/apt/lists/*

# 3. Install R packages in stages to handle dependencies properly
# 3a. Install basic dependencies first
RUN R -e "install.packages(c('miniUI', 'pkgdown'), repos='https://cloud.r-project.org', dependencies=TRUE)"

# 3b. Install font/graphics related packages
RUN R -e "install.packages(c('systemfonts', 'textshaping', 'ragg'), repos='https://cloud.r-project.org', dependencies=TRUE)"

# 3c. Install main packages including cowplot and tidyr
RUN R -e "install.packages(c('devtools','remotes','ggplot2','patchwork','stringr','progressr','GGally','reshape2'), repos='https://cloud.r-project.org', dependencies=TRUE)" \
 && R -e "install.packages(c('here','dplyr','bayesplot','posterior','cowplot','tidyr','rmarkdown','rmdformats','knitr'), dependencies=TRUE, repos='https://cloud.r-project.org')"

# 3d. Install cmdstanr
RUN R -e "install.packages('cmdstanr', repos=c('https://stan-dev.r-universe.dev', getOption('repos')), dependencies=TRUE)"

# 4. Install CmdStan to /usr/local instead of /tmp
RUN R -e "dir.create('/usr/local/cmdstan', recursive = TRUE, showWarnings = FALSE); \
    cmdstanr::install_cmdstan(dir = '/usr/local/cmdstan', cores = 2, overwrite = TRUE)" && \
    CMDSTAN_PATH=$(find /usr/local/cmdstan -name 'cmdstan-*' -type d | head -1) && \
    echo "CMDSTAN=$CMDSTAN_PATH" >> /etc/environment && \
    echo "export CMDSTAN=$CMDSTAN_PATH" >> /etc/bash.bashrc

ENV CMDSTAN=/usr/local/cmdstan/cmdstan-2.37.0

RUN ls -la /usr/local/cmdstan/


# 5. Install SBC package from GitHub
RUN R -e "devtools::install_github('hyunjimoon/SBC')"

# 6. Verify CmdStan installation (CORRECTED - removed check_cmdstan())
RUN R -e "cat('CmdStan path:', cmdstanr::cmdstan_path(), '\n'); \
    cat('CmdStan version:', cmdstanr::cmdstan_version(), '\n'); \
    cat('CmdStan installation verified successfully!\n')"

# Verify the document-rendering toolchain used by manuscript workflows.
RUN pandoc --version \
 && quarto --version \
 && pdflatex --version \
 && latexmk -v \
 && latexdiff --version 2>&1 | grep -q LATEXDIFF \
 && pdfinfo -v \
 && kpsewhich natbib.sty \
 && kpsewhich microtype.sty \
 && kpsewhich makecell.sty \
 && kpsewhich booktabs.sty

# 7. Set working directory for your model files
WORKDIR /workspace

# 8. Expose a port if you plan to run any web interfaces
EXPOSE 8080

# 9. Default entrypoint
CMD ["bash"]
