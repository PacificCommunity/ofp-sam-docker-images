###############################################################################
# HTCondor-Compatible Docker Image: Ubuntu 22.04 + R 4.1.2 + VAST 3.7.1
# 
# This image solves the glibc compatibility issue by using Ubuntu 22.04 
# (glibc 2.35) as base while compiling R 4.1.2 from source to maintain
# exact compatibility with VAST 3.7.1 and FishStatsUtils 2.9.1
###############################################################################

FROM ubuntu:22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# R version and build configuration
ARG R_VERSION=4.1.2
ARG NPROC=4

###############################################################################
# 1. Install system dependencies and build tools
###############################################################################

RUN apt-get update && apt-get install -y --no-install-recommends \
    # Essential build tools for compiling R from source
    build-essential \
    gfortran \
    # R compilation dependencies (required for configure step)
    libreadline-dev \
    libbz2-dev \
    liblzma-dev \
    libpcre2-dev \
    zlib1g-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    libicu-dev \
    # Graphics and image processing libraries
    libpng-dev \
    libjpeg-dev \
    libcairo2-dev \
    libtiff5-dev \
    libfreetype6-dev \
    # X11 and GUI support
    libxt-dev \
    libx11-dev \
    # Linear algebra libraries
    libblas-dev \
    liblapack-dev \
    # Spatial analysis libraries (required for VAST spatial packages)
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    libudunits2-dev \
    libnetcdf-dev \
    # Font and text rendering
    libfontconfig1-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    # Development tools and utilities
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
    pkg-config \
    ca-certificates \
    # Python for radian R console
    python3-pip \
    python3-dev \
    python3-setuptools \
    python3-wheel \
    python3-venv \
    # LaTeX and document processing
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-latex-recommended \
    texlive-base \
    texlive-binaries \
    lmodern \
    # Document conversion tools
    pandoc \
    librsvg2-bin \
    ghostscript \
    inkscape \
    # Additional spatial tools
    gdal-bin \
    # OpenGL libraries
    libglu1-mesa-dev && \
    # Clean up package cache to reduce image size
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

###############################################################################
# 2. Compile and install R 4.1.2 from source (FIXED: Better configuration)
###############################################################################

WORKDIR /tmp

# Download, compile, and install R 4.1.2 with proper recommended packages
RUN curl -fsSL https://cran.r-project.org/src/base/R-4/R-${R_VERSION}.tar.gz -o R-${R_VERSION}.tar.gz && \
    tar -xzf R-${R_VERSION}.tar.gz && \
    cd R-${R_VERSION} && \
    # Configure R build with explicit paths and options
    ./configure \
        --prefix=/usr/local \
        --enable-R-shlib \
        --enable-memory-profiling \
        --with-blas \
        --with-lapack \
        --with-readline \
        --with-recommended-packages=yes \
        --enable-byte-compiled-packages \
        --with-x \
        --with-cairo \
        --with-libpng \
        --with-jpeglib \
        --with-libtiff && \
    # Compile using multiple cores for faster build
    make -j${NPROC} && \
    # Install R system-wide
    make install && \
    # CRITICAL: Install recommended packages separately to ensure they're available
    make install-recommended && \
    # Clean up source files
    cd /tmp && \
    rm -rf R-${R_VERSION}*

# Verify R installation has essential packages
RUN echo "=== R Version Check ===" && \
    R --version | head -1 && \
    echo "=== glibc Version Check ===" && \
    ldd --version | head -1 && \
    echo "=== R Base Packages Check ===" && \
    R --slave -e "cat('Base packages available:', length(.packages(all.available=TRUE)), '\n')" && \
    R --slave -e "if(!require('utils', quietly=TRUE)) stop('utils package missing')" && \
    R --slave -e "if(!require('stats', quietly=TRUE)) stop('stats package missing')" && \
    echo "=== R Library Paths ===" && \
    R --slave -e "cat(.libPaths(), sep='\n')"

###############################################################################
# 3. System locale and timezone configuration
###############################################################################

# Set up locale for New Caledonia
RUN locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 && \
    ln -fs /usr/share/zoneinfo/Pacific/Noumea /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

# Set environment variables
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV TZ=Pacific/Noumea

###############################################################################
# 4. Install additional tools
###############################################################################

# Install Docker CLI (client only, no daemon)
RUN curl -fsSL https://get.docker.com | sh

# Install radian for modern R console experience
RUN pip3 install --no-cache-dir radian==0.6.4

###############################################################################
# 5. Configure R environment
###############################################################################

# Create R configuration directories and set CRAN mirror
RUN mkdir -p /etc/R /usr/local/lib/R/etc && \
    # Set in system-wide Rprofile.site
    echo 'local({r <- getOption("repos"); r["CRAN"] <- "https://cloud.r-project.org"; options(repos=r)})' > /etc/R/Rprofile.site && \
    echo 'options(timeout = 300)' >> /etc/R/Rprofile.site && \
    echo 'options(download.file.method = "libcurl")' >> /etc/R/Rprofile.site && \
    echo 'options(Ncpus = 4)' >> /etc/R/Rprofile.site && \
    # Also set in R installation directory
    cp /etc/R/Rprofile.site /usr/local/lib/R/etc/Rprofile.site

# Test R configuration and package installation capability
RUN echo "=== Testing R Configuration ===" && \
    R --slave -e "cat('CRAN repo:', getOption('repos')['CRAN'], '\n')" && \
    echo "=== Testing install.packages function ===" && \
    R --slave -e "if(!exists('install.packages')) stop('install.packages function not found')" && \
    echo "=== R configuration test passed ==="

###############################################################################
# 6. Install essential R packages
###############################################################################

# Install development tools first (required for GitHub packages)
RUN R -e "install.packages(c('devtools', 'remotes'), dependencies = TRUE, repos = 'https://cloud.r-project.org')"

# Install Bioconductor and required packages for INLA
RUN R -e "if (!requireNamespace('BiocManager', quietly=TRUE)) install.packages('BiocManager', repos = 'https://cloud.r-project.org')" && \
    R -e "BiocManager::install(c('graph', 'Rgraphviz'), ask=FALSE, update=FALSE)"

###############################################################################
# 7. Install legacy spatial packages (CRITICAL ORDER for VAST compatibility)
###############################################################################

# These specific archived versions are required for VAST 3.7.1 compatibility
# Order matters due to package dependencies
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/sp/sp_1.4-5.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/raster/raster_3.4-5.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/rgdal/rgdal_1.5-23.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/rgeos/rgeos_0.5-9.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/maptools/maptools_1.1-8.tar.gz', repos=NULL, type='source')"

# Install supporting spatial and statistical packages
RUN R -e "install.packages(c('XML', 'spacetime', 'colorspace', 'plotrix', 'dismo', 'aqp', 'pixmap', 'plyr', 'colorRamps', 'scales', 'gstat', 'zoo', 'RColorBrewer', 'RSAGA', 'classInt'), dependencies=TRUE, repos = 'https://cloud.r-project.org')"

# Install additional archived packages required for VAST ecosystem
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/plotKML/plotKML_0.5-9.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/units/units_0.7-2.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/RandomFieldsUtils/RandomFieldsUtils_0.5.3.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/RandomFields/RandomFields_3.3.8.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/TMBhelper/TMBhelper_1.4.2.tar.gz', repos=NULL, type='source')"

###############################################################################
# 8. Install INLA (specific version compatible with VAST 3.7.1)
###############################################################################

RUN R -e "install.packages('https://inla.r-inla-download.org/R/stable/src/contrib/INLA_22.05.07.tar.gz', repos=NULL, type='source')"

###############################################################################
# 9. Install modern spatial and statistical packages
###############################################################################

# Core packages for spatial analysis and statistics
RUN R -e "install.packages(c('TMB', 'RcppArmadillo', 'Matrix', 'sf', 'terra', 'stars'), dependencies=TRUE, repos = 'https://cloud.r-project.org')"

# Data manipulation and visualization packages
RUN R -e "install.packages(c('ggplot2', 'dplyr', 'tidyr', 'data.table', 'magrittr', 'ggthemes', 'rmdformats', 'purrr', 'reshape2', 'cowplot', 'patchwork', 'kableExtra', 'viridis'), dependencies=TRUE, repos = 'https://cloud.r-project.org')"

# Install tidyverse meta-package
RUN R -e "install.packages('tidyverse', dependencies=TRUE, repos = 'https://cloud.r-project.org')"

###############################################################################
# 10. Install VAST ecosystem (CRITICAL: exact versions for reproducibility)
###############################################################################

# Install FishStatsUtils 2.9.1 and VAST 3.7.1 with exact version pinning
RUN R -e "remotes::install_github('James-Thorson-NOAA/FishStatsUtils@2.9.1', dependencies=TRUE, upgrade='never', force=TRUE)" && \
    R -e "remotes::install_github('James-Thorson-NOAA/VAST@3.7.1', dependencies=TRUE, upgrade='never', force=TRUE)"

# Install Pacific Community VAST utilities
RUN R -e "remotes::install_github('PacificCommunity/ofp-sam-vast-utils', dependencies=FALSE)"

###############################################################################
# 11. Install oceanographic and additional analysis packages
###############################################################################

# Oceanographic analysis packages
RUN R -e "install.packages(c('gsw', 'testthat', 'knitr', 'rmarkdown', 'ncdf4'), dependencies=TRUE, repos = 'https://cloud.r-project.org')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/oce/oce_1.5-0.tar.gz', repos=NULL, type='source')"

# Additional spatial analysis packages
RUN R -e "install.packages(c('gstat', 'automap', 'geoR', 'fields'), dependencies=TRUE, repos = 'https://cloud.r-project.org')"

###############################################################################
# 12. Install Quarto CLI for document generation
###############################################################################

# Install Quarto CLI (compatible version for Ubuntu 22.04)
RUN curl -L https://github.com/quarto-dev/quarto-cli/releases/download/v1.2.335/quarto-1.2.335-linux-amd64.deb -o quarto.deb && \
    dpkg -i quarto.deb || apt-get install -f -y && \
    rm quarto.deb

###############################################################################
# 13. Create workspace and user configuration
###############################################################################

# Create workspace directory with proper permissions
RUN mkdir -p /workspace && \
    chmod -R 777 /workspace && \
    chmod -R 777 /usr/local/lib/R/site-library

# Create analyst user for HTCondor compatibility (UID 1000)
RUN useradd -m -u 1000 -U -s /bin/bash analyst && \
    echo "analyst ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    echo 'analyst:analyst' | chpasswd && \
    mkdir -p /var/run/sshd

###############################################################################
# 14. Final verification and health checks
###############################################################################

# Verify critical installations work correctly
RUN echo "=== Final System Check ===" && \
    R --version && \
    echo "=== VAST Installation Check ===" && \
    R -e "library(VAST); cat('VAST version:', as.character(packageVersion('VAST')), '\n')" && \
    echo "=== FishStatsUtils Installation Check ===" && \
    R -e "library(FishStatsUtils); cat('FishStatsUtils version:', as.character(packageVersion('FishStatsUtils')), '\n')" && \
    echo "=== glibc Version (HTCondor Compatibility) ===" && \
    ldd --version | head -1

###############################################################################
# 15. Container configuration
###############################################################################

# Expose SSH port for remote access
EXPOSE 22

# Switch to analyst user for security
USER analyst

# Set working directory
WORKDIR /workspace

# Default command to start bash shell
CMD ["/bin/bash"]
