FROM rocker/rstudio:4.5.1

# Set environment variables early
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Pacific/Noumea
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# Install system dependencies and development libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        git \
        curl \
        sudo \
        openssh-server \
        bash-completion \
        locales \
        tzdata \
        vim \
        nano \
        less \
        python3-venv \
        libcurl4-openssl-dev \
        libssl-dev \
        libxml2-dev \
        libgdal-dev \
        libgeos-dev \
        libproj-dev \
        libudunits2-dev \
        libnetcdf-dev \
        libfontconfig1-dev \
        libharfbuzz-dev \
        libfribidi-dev \
        pkg-config \
        texlive-latex-extra \
        pandoc \
        pandoc-citeproc \
        librsvg2-bin \
        ghostscript \
        inkscape \
        ca-certificates \
        gdal-bin \
        libglu1-mesa-dev \
        libx11-dev \
        gawk \
        bison \
        gcc \
        make \
        wget \
        tar \
        build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 && \
    ln -fs /usr/share/zoneinfo/Pacific/Noumea /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

RUN apt-get update && \
    apt-get install -y \
        texlive-fonts-recommended \
        texlive-fonts-extra \
        lmodern \
        texlive-latex-extra \
        texlive-latex-recommended \
        texlive-base \
        texlive-binaries && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Docker CLI (client only, no daemon)
RUN curl -fsSL https://get.docker.com | sh

# Install radian for a modern R console experience
RUN pip3 install -U radian

# Set default CRAN repository for R
RUN mkdir -p /etc/R && \
    echo 'options(repos = c(CRAN = "https://cloud.r-project.org"))' >> /etc/R/Rprofile.site

# Install devtools and remotes packages
RUN R -e "install.packages(c('devtools', 'remotes'))"

# Install Bioconductor dependencies required for INLA
RUN R -e "if (!requireNamespace('BiocManager', quietly=TRUE)) install.packages('BiocManager')"
RUN R -e "BiocManager::install(c('graph', 'Rgraphviz'), ask=FALSE, update=FALSE)"

# Install modern spatial packages (replacing legacy archived versions)
RUN R -e "install.packages(c('sp', 'sf', 'terra', 'stars', 'raster', 'units'))"

# Install core statistical and spatial dependencies
RUN R -e "install.packages(c('XML', 'spacetime', 'colorspace', 'plotrix', 'dismo', 'aqp', 'pixmap', 'plyr', 'colorRamps', 'scales', 'gstat', 'zoo', 'RColorBrewer', 'classInt'))"

# Install INLA (latest stable version)
RUN R -e "install.packages('INLA', repos=c(getOption('repos'), INLA='https://inla.r-inla-download.org/R/stable'), dep=TRUE)"

# Install core spatial and statistical R packages (latest compatible versions)
RUN R -e "install.packages(c('TMB', 'RcppArmadillo', 'Matrix', 'ggplot2', 'dplyr', 'tidyr', 'data.table', 'magrittr', 'ggthemes', 'rmdformats', 'tidyverse', 'purrr', 'reshape2', 'cowplot', 'patchwork'))"

# Install additional spatial/statistical packages
RUN R -e "install.packages(c('fmesher', 'abind', 'effects', 'alphahull', 'corpcor', 'corrplot', 'DHARMa', 'ecodist', 'fastcluster', 'RANN', 'rnaturalearth', 'rnaturalearthdata', 'seriation', 'shape', 'viridisLite', 'marginaleffects'))"

# Accept GITHUB_PAT as build argument for authenticated GitHub API requests
ARG GITHUB_PAT
ENV GITHUB_PAT=${GITHUB_PAT}

# Install latest VAST 4.0.0 (which includes FishStatsUtils merged in)
RUN R -e "devtools::install_github('James-Thorson-NOAA/VAST@4.0.0', dependencies=TRUE, upgrade=FALSE, force=TRUE)"

# Install PacificCommunity package
RUN R -e "devtools::install_github('PacificCommunity/ofp-sam-vast-utils', dependencies=FALSE)"
    
# Install oce (latest version)
RUN R -e "install.packages(c('gsw', 'testthat', 'knitr', 'rmarkdown', 'ncdf4', 'oce'))"

# Install additional requested packages
RUN R -e "install.packages(c('automap', 'geoR', 'fields', 'kableExtra', 'viridis'))"

# Install latest Quarto CLI
RUN curl -L https://github.com/quarto-dev/quarto-cli/releases/latest/download/quarto-linux-amd64.deb -o quarto.deb && \
    dpkg -i quarto.deb && \
    rm quarto.deb

# Create analyst user with UID 1001 (avoiding conflict with existing rstudio user)
RUN useradd -m -u 1001 -U -s /bin/bash analyst && \
    echo "analyst ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Create workspace directory and set proper ownership and permissions
RUN mkdir -p /workspace && \
    chown -R analyst:analyst /workspace && \
    chmod -R 755 /workspace

# Create analysis directory structure with proper permissions for data processing
RUN mkdir -p /workspace/analysis/eu/data/processed && \
    chown -R analyst:analyst /workspace/analysis && \
    chmod -R 755 /workspace/analysis

# Set R library permissions for package installation
RUN chmod -R 777 /usr/local/lib/R/site-library

# Set up SSH server for remote access (default password: analyst)
RUN echo 'analyst:analyst' | chpasswd && \
    mkdir /var/run/sshd

EXPOSE 22

# Switch to analyst user and set working directory
USER analyst
WORKDIR /workspace

CMD ["/bin/bash"]
