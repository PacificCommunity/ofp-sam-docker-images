# Use Ubuntu 18.04 LTS base image for better GLIBC compatibility with HTCondor systems
# Ubuntu 18.04 uses GLIBC 2.27 which is compatible with older HTCondor environments
FROM ubuntu:18.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Set locale and timezone for Noumea, New Caledonia (Pacific/Noumea)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        locales \
        tzdata && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 && \
    ln -fs /usr/share/zoneinfo/Pacific/Noumea /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV LANG=en_US.UTF-8
ENV TZ=Pacific/Noumea

# Install system dependencies required for R compilation and spatial packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gfortran \
        libblas-dev \
        liblapack-dev \
        libreadline-dev \
        libbz2-dev \
        liblzma-dev \
        libpcre2-dev \
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
        libcairo2-dev \
        libxt-dev \
        libx11-dev \
        libglu1-mesa-dev \
        pkg-config \
        wget \
        curl \
        git \
        sudo \
        openssh-server \
        bash-completion \
        vim \
        nano \
        less \
        python3-pip \
        python3-venv \
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
        ca-certificates \
        gdal-bin \
        default-jre \
        default-jdk && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Download and compile R 4.1.2 from source for maximum compatibility
RUN cd /tmp && \
    wget https://cran.r-project.org/src/base/R-4/R-4.1.2.tar.gz && \
    tar -xzf R-4.1.2.tar.gz && \
    cd R-4.1.2 && \
    # Configure R build with recommended options for statistical computing
    ./configure --enable-R-shlib \
                --enable-memory-profiling \
                --with-blas \
                --with-lapack \
                --with-readline \
                --with-recommended-packages \
                --enable-BLAS-shlib && \
    # Compile R (this may take 15-30 minutes)
    make -j$(nproc) && \
    make install && \
    # Clean up source files to reduce image size
    cd / && rm -rf /tmp/R-4.1.2*

# Install Docker CLI (client only, no daemon) for container management
RUN curl -fsSL https://get.docker.com | sh

# Install radian for enhanced R console experience
RUN pip3 install -U radian

# Set default CRAN repository for R package installations
RUN mkdir -p /etc/R && \
    echo 'options(repos = c(CRAN = "https://cloud.r-project.org"))' >> /etc/R/Rprofile.site

# Install essential R packages for development and package management
RUN R -e "install.packages('devtools', dependencies=TRUE)"

# Install Bioconductor manager and required dependencies for INLA
RUN R -e "if (!requireNamespace('BiocManager', quietly=TRUE)) install.packages('BiocManager')"
RUN R -e "BiocManager::install(c('graph', 'Rgraphviz'), ask=FALSE, update=FALSE)"

# Install legacy spatial packages with specific versions for compatibility
# These packages are no longer maintained but required for VAST ecosystem
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/sp/sp_1.4-5.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/raster/raster_3.4-5.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/rgdal/rgdal_1.5-23.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/rgeos/rgeos_0.5-9.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/maptools/maptools_1.1-8.tar.gz', repos=NULL, type='source')"

# Install supporting spatial and statistical packages
RUN R -e "install.packages(c('XML', 'spacetime', 'colorspace', 'plotrix', 'dismo', 'aqp', 'pixmap', 'plyr', 'colorRamps', 'scales', 'gstat', 'zoo', 'RColorBrewer', 'RSAGA', 'classInt'))"

# Install additional legacy packages required for VAST workflow
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/plotKML/plotKML_0.5-9.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/units/units_0.7-2.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/RandomFieldsUtils/RandomFieldsUtils_0.5.3.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/RandomFields/RandomFields_3.3.8.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/TMBhelper/TMBhelper_1.4.2.tar.gz', repos=NULL, type='source')"

# Install INLA 22.05.07 - specific version compatible with VAST 3.7.1
RUN R -e "install.packages('https://inla.r-inla-download.org/R/stable/src/contrib/INLA_22.05.07.tar.gz', repos=NULL, type='source')"

# Install core modern spatial and statistical packages
RUN R -e "install.packages(c('TMB', 'RcppArmadillo', 'Matrix', 'sf', 'terra', 'stars', 'ggplot2', 'dplyr', 'tidyr', 'data.table', 'magrittr', 'ggthemes', 'rmdformats', 'tidyverse', 'purrr', 'reshape2', 'cowplot', 'patchwork'))"

# Install FishStatsUtils 2.9.1 and VAST 3.7.1 from GitHub
# These are the specific versions required for the analysis workflow
RUN R -e "devtools::install_github('James-Thorson-NOAA/FishStatsUtils@2.9.1', dependencies = TRUE, upgrade = FALSE, force=TRUE)"
RUN R -e "devtools::install_github('James-Thorson-NOAA/VAST@3.7.1', dependencies = TRUE, upgrade = FALSE, force=TRUE)"

# Install additional VAST utilities from Pacific Community
RUN R -e "remotes::install_github('PacificCommunity/ofp-sam-vast-utils', dependencies = FALSE)"

# Install oceanographic analysis package (oce) with dependencies
RUN R -e "install.packages(c('gsw', 'testthat', 'knitr', 'rmarkdown', 'ncdf4'))"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/oce/oce_1.5-0.tar.gz', repos=NULL, type='source')"

# Install additional spatial analysis and geostatistics packages
RUN R -e "install.packages(c('gstat', 'automap', 'geoR', 'fields'))"

# Install visualization and data manipulation packages
RUN R -e "install.packages(c('kableExtra', 'viridis'))"

# Install Quarto CLI version 1.2.335 (compatible with R 4.1.2)
RUN curl -L https://github.com/quarto-dev/quarto-cli/releases/download/v1.2.335/quarto-1.2.335-linux-amd64.deb -o quarto.deb && \
    dpkg -i quarto.deb && \
    rm quarto.deb

# Create and configure workspace directory with proper permissions
RUN mkdir -p /workspace && chmod -R 777 /workspace
RUN chmod -R 777 /usr/local/lib/R/site-library

# Create analyst user with passwordless sudo access for development container
RUN useradd -m -u 1000 -U -s /bin/bash analyst && \
    echo "analyst ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Configure SSH server for remote access (default password: analyst)
RUN echo 'analyst:analyst' | chpasswd && \
    mkdir /var/run/sshd

# Expose SSH port for remote development access
EXPOSE 22

# Switch to analyst user and set working directory
USER analyst
WORKDIR /workspace

# Set default command to bash shell
CMD ["/bin/bash"]

