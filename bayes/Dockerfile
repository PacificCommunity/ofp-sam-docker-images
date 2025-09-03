FROM rocker/r-ver:4.5.1

# 1. Disable interactive prompts and set Noumea timezone
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Pacific/Noumea

# 2. Install system libraries needed for R package building
RUN apt-get update && apt-get install -y --no-install-recommends \
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
  && rm -rf /var/lib/apt/lists/*

# 3. Install R packages in stages to handle dependencies properly
# 3a. Install basic dependencies first
RUN R -e "install.packages(c('miniUI', 'pkgdown'), repos='https://cloud.r-project.org', dependencies=TRUE)"

# 3b. Install font/graphics related packages
RUN R -e "install.packages(c('systemfonts', 'textshaping', 'ragg'), repos='https://cloud.r-project.org', dependencies=TRUE)"

# 3c. Install main packages including cowplot and tidyr
RUN R -e "install.packages(c('devtools','remotes','ggplot2','patchwork','stringr','progressr'), repos='https://cloud.r-project.org', dependencies=TRUE)" \
 && R -e "install.packages(c('here','dplyr','bayesplot','posterior','cowplot','tidyr'), dependencies=TRUE, repos='https://cloud.r-project.org')"

# 3d. Install cmdstanr
RUN R -e "install.packages('cmdstanr', repos=c('https://stan-dev.r-universe.dev', getOption('repos')), dependencies=TRUE)"

# 4. Install CmdStan and set environment variables properly
RUN R -e "dir.create('/tmp/cmdstan', recursive = TRUE, showWarnings = FALSE); \
    cmdstanr::install_cmdstan(dir = '/tmp/cmdstan', cores = 2, overwrite = TRUE)" && \
    CMDSTAN_PATH=$(find /tmp/cmdstan -name 'cmdstan-*' -type d | head -1) && \
    echo "CMDSTAN=$CMDSTAN_PATH" >> /etc/environment && \
    echo "export CMDSTAN=$CMDSTAN_PATH" >> /etc/bash.bashrc && \
    R -e "cmdstanr::set_cmdstan_path('$CMDSTAN_PATH')"

# 4b. Set environment variable for current Docker build and runtime
ENV CMDSTAN=/tmp/cmdstan/cmdstan-2.37.0

# 5. Install SBC package from GitHub
RUN R -e "devtools::install_github('hyunjimoon/SBC')"

# 6. Verify CmdStan installation
RUN R -e "cat('CmdStan path:', cmdstanr::cmdstan_path(), '\n'); \
    cat('CmdStan version:', cmdstanr::cmdstan_version(), '\n'); \
    cmdstanr::check_cmdstan()"

# 7. Set working directory for your model files
WORKDIR /workspace

# 8. Expose a port if you plan to run any web interfaces
EXPOSE 8080

# 9. Default entrypoint
CMD ["bash"]
