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

# 4. Install CmdStan in the Docker image
# Set HOME environment and install CmdStan
ENV HOME=/opt/cmdstan
RUN mkdir -p /opt/cmdstan \
 && R -e "cmdstanr::install_cmdstan(cores = parallel::detectCores())" \
 && echo "CMDSTAN=/opt/cmdstan/.cmdstan/cmdstan-$(R -e 'cat(cmdstanr::cmdstan_version())')" >> /etc/environment

# 5. Install SBC package from GitHub
RUN R -e "devtools::install_github('hyunjimoon/SBC')"

# 6. Set working directory for your model files
WORKDIR /workspace

# 7. Expose a port if you plan to run any web interfaces
EXPOSE 8080

# 8. Default entrypoint
CMD ["bash"]

