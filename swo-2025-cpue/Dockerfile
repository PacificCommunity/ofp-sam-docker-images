###############################################################################
#  Dockerfile – Ubuntu 18.04  (glibc 2.27)  +  R 4.1.2 (built from source)
#  Compatible with:  VAST 3.7.1  |  FishStatsUtils 2.9.1  |  legacy spatial pkgs
###############################################################################

FROM ubuntu:18.04

# --------------------------------------------------------------------
# ── 0.  Global build settings ───────────────────────────────────────
# --------------------------------------------------------------------
ENV DEBIAN_FRONTEND=noninteractive
ARG MAKE_NPROC=4            # change to $(nproc) for max parallel build
ENV R_VERSION=4.1.2

# --------------------------------------------------------------------
# ── 1.  Base OS tooling & libraries (build + runtime)  ───────────────
# --------------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    ## Build chain
    build-essential        gfortran         \
    ## Core libs for R compilation
    libreadline-dev        libbz2-dev       \
    liblzma-dev            libpcre2-dev     \
    zlib1g-dev             libncurses5-dev  \
    libcurl4-openssl-dev   libssl-dev       \
    libxml2-dev            libicu-dev       \
    ## Optional but strongly recommended graphics/libs
    libpng-dev             libjpeg-dev      \
    libcairo2-dev          libtiff5-dev     \
    libfreetype6-dev       libx11-dev       libxt-dev \
    ## BLAS / LAPACK
    libblas-dev            liblapack-dev    \
    ## Spatial / NetCDF stack
    libgdal-dev            libgeos-dev      libproj-dev \
    libudunits2-dev        libnetcdf-dev    \
    ## Runtime utilities
    git curl wget sudo nano less vim tzdata locales \
    ## Python (for radian)
    python3-pip python3-setuptools python3-wheel \
    ## Misc
    ca-certificates pkg-config gnupg2 && \
    rm -rf /var/lib/apt/lists/*

# --------------------------------------------------------------------
# ── 2.  Build + install R 4.1.2 from source  ────────────────────────
# --------------------------------------------------------------------
WORKDIR /tmp

RUN curl -fsSL https://cran.r-project.org/src/base/R-4/R-${R_VERSION}.tar.gz -o R-${R_VERSION}.tar.gz && \
    tar -xzf R-${R_VERSION}.tar.gz && \
    cd R-${R_VERSION} && \
    ./configure \
        --prefix=/usr/local \
        --enable-R-shlib \
        --with-blas --with-lapack \
        --with-readline \
        --with-recommended-packages && \
    make -j${MAKE_NPROC} && make install && \
    cd /tmp && rm -rf R-${R_VERSION}* && \
    strip /usr/local/bin/R && strip /usr/local/lib/R/bin/exec/R

# Quick sanity check
RUN R --version | head -1   # should print “R version 4.1.2 (2021-11-01) …”

# --------------------------------------------------------------------
# ── 3.  Locale & time-zone (Pacific/Noumea)  ────────────────────────
# --------------------------------------------------------------------
RUN locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 && \
    ln -fs /usr/share/zoneinfo/Pacific/Noumea /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV TZ=Pacific/Noumea

# --------------------------------------------------------------------
# ── 4.  radian – modern R console  ──────────────────────────────────
# --------------------------------------------------------------------
RUN pip3 install --no-cache-dir radian==0.6.4

# --------------------------------------------------------------------
# ── 5.  R global options  ───────────────────────────────────────────
# --------------------------------------------------------------------
RUN mkdir -p /etc/R && \
    echo "options(repos = c(CRAN='https://cloud.r-project.org'))" >> /etc/R/Rprofile.site && \
    echo "options(timeout = 300, download.file.method = 'libcurl')" >> /etc/R/Rprofile.site

# --------------------------------------------------------------------
# ── 6.  Base R helper packages (devtools, remotes, Bioc)  ───────────
# --------------------------------------------------------------------
RUN R -e "install.packages(c('devtools','remotes'), dependencies = TRUE)" && \
    R -e "if(!requireNamespace('BiocManager', quietly=TRUE)) install.packages('BiocManager')" && \
    R -e "BiocManager::install(c('graph','Rgraphviz'), ask=FALSE, update=FALSE)"

# --------------------------------------------------------------------
# ── 7.  Legacy spatial libs needed by VAST 3.7.1  ───────────────────
# --------------------------------------------------------------------
RUN R -e "install.packages(c(                                    \
        'https://cran.r-project.org/src/contrib/Archive/sp/sp_1.4-5.tar.gz',      \
        'https://cran.r-project.org/src/contrib/Archive/raster/raster_3.4-5.tar.gz',  \
        'https://cran.r-project.org/src/contrib/Archive/rgdal/rgdal_1.5-23.tar.gz',  \
        'https://cran.r-project.org/src/contrib/Archive/rgeos/rgeos_0.5-9.tar.gz',   \
        'https://cran.r-project.org/src/contrib/Archive/maptools/maptools_1.1-8.tar.gz'), \
        repos = NULL, type = 'source')" && \
    R -e "install.packages(c('XML','spacetime','colorspace','plotrix','dismo','aqp', \
                             'pixmap','plyr','colorRamps','scales','gstat','zoo',   \
                             'RColorBrewer','RSAGA','classInt'), dependencies=TRUE)"

# Additional archived helpers
RUN R -e "install.packages(c(                                          \
        'https://cran.r-project.org/src/contrib/Archive/plotKML/plotKML_0.5-9.tar.gz', \
        'https://cran.r-project.org/src/contrib/Archive/units/units_0.7-2.tar.gz',     \
        'https://cran.r-project.org/src/contrib/Archive/RandomFieldsUtils/RandomFieldsUtils_0.5.3.tar.gz', \
        'https://cran.r-project.org/src/contrib/Archive/RandomFields/RandomFields_3.3.8.tar.gz',           \
        'https://cran.r-project.org/src/contrib/Archive/TMBhelper/TMBhelper_1.4.2.tar.gz'),                \
        repos = NULL, type = 'source')"

# --------------------------------------------------------------------
# ── 8.  INLA (specific, VAST-compatible build)  ─────────────────────
# --------------------------------------------------------------------
RUN R -e "install.packages('https://inla.r-inla-download.org/R/stable/src/contrib/INLA_22.05.07.tar.gz', \
        repos=NULL, type='source')"

# --------------------------------------------------------------------
# ── 9.  Modern spatial / tidyverse stack  ───────────────────────────
# --------------------------------------------------------------------
RUN R -e "install.packages(c('TMB','RcppArmadillo','Matrix','sf','terra','stars', \
                             'ggplot2','dplyr','tidyr','data.table','magrittr',  \
                             'ggthemes','rmdformats','purrr','reshape2','cowplot','patchwork', \
                             'kableExtra','viridis','tidyverse'), dependencies=TRUE)"

# --------------------------------------------------------------------
# ── 10.  VAST 3.7.1 + FishStatsUtils 2.9.1  ─────────────────────────
# --------------------------------------------------------------------
RUN R -e "remotes::install_github('James-Thorson-NOAA/FishStatsUtils@2.9.1', \
        dependencies=TRUE, upgrade='never', force=TRUE)" && \
    R -e "remotes::install_github('James-Thorson-NOAA/VAST@3.7.1',        \
        dependencies=TRUE, upgrade='never', force=TRUE)" && \
    R -e "remotes::install_github('PacificCommunity/ofp-sam-vast-utils',  \
        dependencies=FALSE)"

# --------------------------------------------------------------------
# ── 11.  Oce + misc science libs  ───────────────────────────────────
# --------------------------------------------------------------------
RUN R -e "install.packages(c('gsw','testthat','knitr','rmarkdown','ncdf4'), dependencies=TRUE)" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/oce/oce_1.5-0.tar.gz', \
        repos=NULL, type='source')" && \
    R -e "install.packages(c('gstat','automap','geoR','fields'), dependencies=TRUE)"

# --------------------------------------------------------------------
# ── 12.  Quarto CLI 1.2.335 (last 18.04-compatible)  ─────────────────
# --------------------------------------------------------------------
RUN curl -L https://github.com/quarto-dev/quarto-cli/releases/download/v1.2.335/quarto-1.2.335-linux-amd64.deb \
        -o quarto.deb && dpkg -i quarto.deb || apt-get install -fy && rm quarto.deb

# --------------------------------------------------------------------
# ── 13.  Workspace & user for HTCondor  ─────────────────────────────
# --------------------------------------------------------------------
RUN mkdir -p /workspace && chmod -R 777 /workspace /usr/local/lib/R/site-library

# Create analyst user (UID 1000) with password-less sudo
RUN useradd -m -u 1000 -U -s /bin/bash analyst && \
    echo "analyst ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    echo "analyst:analyst" | chpasswd && \
    mkdir -p /var/run/sshd

# --------------------------------------------------------------------
# ── 14.  Final sanity check  ────────────────────────────────────────
# --------------------------------------------------------------------
RUN R -q -e "cat('VAST loaded-OK → ', as.character(packageVersion('VAST')), '\n')" && \
    ldd --version | head -1           # prints “ldd … 2.27”

EXPOSE 22
USER analyst
WORKDIR /workspace
CMD ["/bin/bash"]
