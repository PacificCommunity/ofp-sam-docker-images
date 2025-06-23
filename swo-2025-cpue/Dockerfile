# Use Ubuntu 18.04 for better glibc compatibility (glibc 2.27)
# This avoids glibc 2.33+ requirements that cause HTCondor failures
FROM ubuntu:18.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies with error handling
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        # Essential build tools and libraries
        build-essential \
        gfortran \
        libblas-dev \
        liblapack-dev \
        # R and development tools
        r-base \
        r-base-dev \
        # Python and utilities
        python3-pip \
        python3-dev \
        git \
        curl \
        wget \
        sudo \
        openssh-server \
        bash-completion \
        locales \
        tzdata \
        vim \
        nano \
        less \
        python3-venv \
        # R package dependencies (critical for compilation)
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
        libfreetype6-dev \
        libpng-dev \
        libtiff5-dev \
        libjpeg-dev \
        pkg-config \
        # LaTeX and document processing
        texlive-latex-extra \
        texlive-fonts-recommended \
        texlive-fonts-extra \
        lmodern \
        texlive-latex-recommended \
        texlive-base \
        texlive-binaries \
        pandoc \
        pandoc-citeproc \
        librsvg2-bin \
        ghostscript \
        inkscape \
        # Additional system libraries
        ca-certificates \
        gdal-bin \
        libglu1-mesa-dev \
        libx11-dev \
        # Fix potential missing dependencies
        libcairo2-dev \
        libxt-dev && \
    # Clean up to reduce image size
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set locale and timezone for New Caledonia
RUN locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 && \
    ln -fs /usr/share/zoneinfo/Pacific/Noumea /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV TZ=Pacific/Noumea

# Install radian for better R console experience
# Pin version to avoid compatibility issues
RUN pip3 install --no-cache-dir radian==0.6.4

# Configure R repository and basic settings
RUN mkdir -p /etc/R && \
    echo 'options(repos = c(CRAN = "https://cloud.r-project.org"))' >> /etc/R/Rprofile.site && \
    echo 'options(timeout = 300)' >> /etc/R/Rprofile.site && \
    echo 'options(download.file.method = "libcurl")' >> /etc/R/Rprofile.site

# Install essential R packages first (with error handling)
RUN R -e "if (!require('devtools')) { \
    install.packages('devtools', dependencies=TRUE); \
    if (!require('devtools')) stop('Failed to install devtools') \
    }"

# Install remotes package for GitHub installations
RUN R -e "if (!require('remotes')) { \
    install.packages('remotes', dependencies=TRUE); \
    if (!require('remotes')) stop('Failed to install remotes') \
    }"

# Install Bioconductor and required packages
RUN R -e "if (!requireNamespace('BiocManager', quietly=TRUE)) { \
    install.packages('BiocManager'); \
    } \
    BiocManager::install(c('graph', 'Rgraphviz'), ask=FALSE, update=FALSE)"

# Install legacy spatial packages in correct order (critical for VAST compatibility)
# These specific versions are required for VAST 3.7.1 and FishStatsUtils 2.9.1
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/sp/sp_1.4-5.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/raster/raster_3.4-5.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/rgdal/rgdal_1.5-23.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/rgeos/rgeos_0.5-9.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/maptools/maptools_1.1-8.tar.gz', repos=NULL, type='source')"

# Install supporting spatial and statistical packages
RUN R -e "install.packages(c('XML', 'spacetime', 'colorspace', 'plotrix', 'dismo', 'aqp', 'pixmap', 'plyr', 'colorRamps', 'scales', 'gstat', 'zoo', 'RColorBrewer', 'RSAGA', 'classInt'), dependencies=TRUE)"

# Install additional archived packages required for VAST
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/plotKML/plotKML_0.5-9.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/units/units_0.7-2.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/RandomFieldsUtils/RandomFieldsUtils_0.5.3.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/RandomFields/RandomFields_3.3.8.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/TMBhelper/TMBhelper_1.4.2.tar.gz', repos=NULL, type='source')"

# Install INLA (specific version compatible with VAST 3.7.1)
RUN R -e "install.packages('https://inla.r-inla-download.org/R/stable/src/contrib/INLA_22.05.07.tar.gz', repos=NULL, type='source')"

# Install modern spatial and statistical packages
RUN R -e "install.packages(c('TMB', 'RcppArmadillo', 'Matrix', 'sf', 'terra', 'stars'), dependencies=TRUE)"

# Install tidyverse and visualization packages
RUN R -e "install.packages(c('ggplot2', 'dplyr', 'tidyr', 'data.table', 'magrittr', 'ggthemes', 'rmdformats', 'purrr', 'reshape2', 'cowplot', 'patchwork', 'kableExtra', 'viridis'), dependencies=TRUE)"

# Install tidyverse meta-package (if individual packages succeeded)
RUN R -e "install.packages('tidyverse', dependencies=TRUE)"

# Install VAST ecosystem packages from GitHub
RUN R -e "remotes::install_github('James-Thorson-NOAA/FishStatsUtils@2.9.1', dependencies=TRUE, upgrade=FALSE, force=TRUE)" && \
    R -e "remotes::install_github('James-Thorson-NOAA/VAST@3.7.1', dependencies=TRUE, upgrade=FALSE, force=TRUE)" && \
    R -e "remotes::install_github('PacificCommunity/ofp-sam-vast-utils', dependencies=FALSE)"

# Install oceanographic packages
RUN R -e "install.packages(c('gsw', 'testthat', 'knitr', 'rmarkdown', 'ncdf4'), dependencies=TRUE)" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/oce/oce_1.5-0.tar.gz', repos=NULL, type='source')"

# Install additional spatial analysis packages
RUN R -e "install.packages(c('gstat', 'automap', 'geoR', 'fields'), dependencies=TRUE)"

# Install Quarto CLI (compatible version for Ubuntu 18.04)
RUN curl -L https://github.com/quarto-dev/quarto-cli/releases/download/v1.2.335/quarto-1.2.335-linux-amd64.deb -o quarto.deb && \
    dpkg -i quarto.deb || apt-get install -f -y && \
    rm quarto.deb

# Create workspace directory with proper permissions
RUN mkdir -p /workspace && \
    chmod -R 777 /workspace && \
    chmod -R 777 /usr/local/lib/R/site-library

# Create analyst user for HTCondor compatibility
RUN useradd -m -u 1000 -U -s /bin/bash analyst && \
    echo "analyst ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    echo 'analyst:analyst' | chpasswd && \
    mkdir -p /var/run/sshd

# Verify critical installations
RUN R -e "if (!require('VAST')) stop('VAST installation failed')" && \
    R -e "if (!require('FishStatsUtils')) stop('FishStatsUtils installation failed')" && \
    ldd --version

EXPOSE 22

USER analyst
WORKDIR /workspace

