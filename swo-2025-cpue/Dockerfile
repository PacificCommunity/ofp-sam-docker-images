# Base image: Ubuntu 18.04 LTS for GLIBC 2.27 compatibility with HTCondor hosts
FROM ubuntu:18.04

# Prevent interactive prompts and set locale/timezone for Nouméa
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=en_US.UTF-8
ENV TZ=Pacific/Noumea

RUN apt-get update && \
    apt-get install -y --no-install-recommends locales tzdata && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 && \
    ln -fs /usr/share/zoneinfo/Pacific/Noumea /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install build tools, libraries, and dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential gfortran wget curl git sudo openssh-server \
      libreadline-dev libbz2-dev liblzma-dev libpcre2-dev libcairo2-dev \
      libcurl4-openssl-dev libssl-dev libxml2-dev libgdal-dev libgeos-dev \
      libproj-dev libudunits2-dev libnetcdf-dev libfontconfig1-dev \
      libharfbuzz-dev libfribidi-dev libxt-dev libx11-dev libglu1-mesa-dev \
      pkg-config python3-pip python3-venv \
      texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra \
      lmodern texlive-base texlive-binaries pandoc pandoc-citeproc \
      librsvg2-bin ghostscript inkscape ca-certificates gdal-bin \
      default-jre default-jdk && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install OpenBLAS and LAPACK to resolve BLAS/LAPACK linking errors
RUN apt-get update && \
    apt-get install -y libopenblas-dev liblapack-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set BLAS/LAPACK environment for R build
ENV BLAS_LIBS="-lopenblas"
ENV LAPACK_LIBS="-llapack"

# Download and extract R 4.1.2 source
RUN cd /tmp && \
    wget https://cran.r-project.org/src/base/R-4/R-4.1.2.tar.gz && \
    tar -xzf R-4.1.2.tar.gz

# Configure, compile, and install R with shared library and BLAS/LAPACK
RUN cd /tmp/R-4.1.2 && \
    ./configure --enable-R-shlib \
                --enable-memory-profiling \
                --with-blas \
                --with-lapack && \
    make LDFLAGS="-L/usr/lib/x86_64-linux-gnu -lopenblas -llapack" -j$(nproc) && \
    make install && \
    cd / && rm -rf /tmp/R-4.1.2*

# Set default CRAN repository
RUN mkdir -p /etc/R && \
    echo 'options(repos = c(CRAN="https://cloud.r-project.org"))' >> /etc/R/Rprofile.site

# Install devtools and BiocManager with explicit CRAN mirror
RUN R -e "install.packages(c('devtools','BiocManager'), dependencies=TRUE, repos='https://cloud.r-project.org')" && \
    R -e "BiocManager::install(c('graph','Rgraphviz'), ask=FALSE, update=FALSE)"


# Install legacy spatial packages required by VAST ecosystem
RUN R -e "install.packages(c( \
  'https://cran.r-project.org/src/contrib/Archive/sp/sp_1.4-5.tar.gz', \
  'https://cran.r-project.org/src/contrib/Archive/raster/raster_3.4-5.tar.gz', \
  'https://cran.r-project.org/src/contrib/Archive/rgdal/rgdal_1.5-23.tar.gz', \
  'https://cran.r-project.org/src/contrib/Archive/rgeos/rgeos_0.5-9.tar.gz', \
  'https://cran.r-project.org/src/contrib/Archive/maptools/maptools_1.1-8.tar.gz' \
), repos=NULL, type='source')" 

# Install core modern spatial/statistical packages
RUN R -e "install.packages(c( \
  'TMB','RcppArmadillo','Matrix','sf','terra','stars','ggplot2','dplyr', \
  'tidyr','data.table','magrittr','ggthemes','rmdformats','tidyverse', \
  'purrr','reshape2','cowplot','patchwork' \
))"

# Install INLA, FishStatsUtils, VAST, and supporting utilities
RUN R -e "install.packages('https://inla.r-inla-download.org/R/stable/src/contrib/INLA_22.05.07.tar.gz', repos=NULL, type='source')" && \
    R -e "devtools::install_github('James-Thorson-NOAA/FishStatsUtils@2.9.1', dependencies=TRUE, upgrade=FALSE, force=TRUE)" && \
    R -e "devtools::install_github('James-Thorson-NOAA/VAST@3.7.1', dependencies=TRUE, upgrade=FALSE, force=TRUE)" && \
    R -e "remotes::install_github('PacificCommunity/ofp-sam-vast-utils', dependencies=FALSE)"

# Install oceanographic package oce and extra dependencies
RUN R -e "install.packages(c('gsw','testthat','knitr','rmarkdown','ncdf4'), dependencies=TRUE)" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/oce/oce_1.5-0.tar.gz', repos=NULL, type='source')"

# Install additional spatial/visualization packages
RUN R -e "install.packages(c('gstat','automap','geoR','fields','kableExtra','viridis'), dependencies=TRUE)"

# Install Quarto CLI v1.2.335
RUN curl -L https://github.com/quarto-dev/quarto-cli/releases/download/v1.2.335/quarto-1.2.335-linux-amd64.deb -o quarto.deb && \
    dpkg -i quarto.deb && rm quarto.deb

# Create workspace directory and set permissions
RUN mkdir -p /workspace && chmod -R 777 /workspace && \
    chmod -R 777 /usr/local/lib/R/site-library

# Add non-root user 'analyst' with passwordless sudo
RUN useradd -m -u 1000 -U -s /bin/bash analyst && \
    echo "analyst ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Configure SSH for remote access and expose port
RUN echo 'analyst:analyst' | chpasswd && mkdir /var/run/sshd
EXPOSE 22

# Switch to non-root user and set working directory
USER analyst
WORKDIR /workspace

# Default command
CMD ["/bin/bash"]

