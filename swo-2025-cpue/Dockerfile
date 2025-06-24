FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Pacific/Noumea

# Configure timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install system dependencies in one layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Basic tools
    curl \
    wget \
    git \
    sudo \
    vim \
    nano \
    less \
    # Build tools
    build-essential \
    gfortran \
    pkg-config \
    cmake \
    # Python
    python3 \
    python3-pip \
    python3-venv \
    # Locale support
    locales \
    # System libraries
    software-properties-common \
    dirmngr \
    ca-certificates \
    gnupg \
    lsb-release \
    openssh-server \
    bash-completion \
    tzdata \
    # R compilation dependencies
    libreadline-dev \
    libx11-dev \
    libxt-dev \
    libpng-dev \
    libjpeg-dev \
    libcairo2-dev \
    libssl-dev \
    libxml2-dev \
    libbz2-dev \
    liblzma-dev \
    libpcre2-dev \
    libcurl4-openssl-dev \
    # Spatial libraries
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    libudunits2-dev \
    libnetcdf-dev \
    gdal-bin \
    # Graphics libraries
    libfontconfig1-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libglu1-mesa-dev \
    # Document processing
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-latex-recommended \
    texlive-base \
    texlive-binaries \
    lmodern \
    pandoc \
    librsvg2-bin \
    ghostscript \
    inkscape && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Configure locale properly
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 && \
    dpkg-reconfigure -f noninteractive locales

# Set locale environment variables
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# Compile and install R 4.1.2 from source
RUN cd /tmp && \
    wget https://cran.r-project.org/src/base/R-4/R-4.1.2.tar.gz && \
    tar -xzf R-4.1.2.tar.gz && \
    cd R-4.1.2 && \
    ./configure --enable-R-shlib --with-blas --with-lapack && \
    make && \
    make install && \
    rm -rf /tmp/R-4.1.2*

# Install Docker CLI (client only)
RUN curl -fsSL https://get.docker.com | sh

# Install radian for enhanced R console
RUN pip3 install -U radian

# Configure CRAN repository for R
RUN mkdir -p /etc/R && \
    echo 'local({' > /etc/R/Rprofile.site && \
    echo '  r <- getOption("repos")' >> /etc/R/Rprofile.site && \
    echo '  r["CRAN"] <- "https://cloud.r-project.org"' >> /etc/R/Rprofile.site && \
    echo '  options(repos = r)' >> /etc/R/Rprofile.site && \
    echo '})' >> /etc/R/Rprofile.site

# Install essential R packages with correct Matrix version
RUN R -e "install.packages('devtools', repos='https://cloud.r-project.org')"

# Install Bioconductor and dependencies
RUN R -e "if (!requireNamespace('BiocManager', quietly=TRUE)) install.packages('BiocManager', repos='https://cloud.r-project.org')" && \
    R -e "BiocManager::install(c('graph', 'Rgraphviz'), ask=FALSE, update=FALSE)"

# Install legacy spatial packages (order matters for dependencies)
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/sp/sp_1.4-5.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/raster/raster_3.4-5.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/rgdal/rgdal_1.5-23.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/rgeos/rgeos_0.5-9.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/maptools/maptools_1.1-8.tar.gz', repos=NULL, type='source')"

# Install supporting spatial and statistical packages
RUN R -e "install.packages(c('XML', 'spacetime', 'colorspace', 'plotrix', 'dismo', 'aqp', 'pixmap', 'plyr', 'colorRamps', 'scales', 'gstat', 'zoo', 'RColorBrewer', 'RSAGA', 'classInt'), repos='https://cloud.r-project.org')"

# Install additional legacy packages from archives
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/plotKML/plotKML_0.5-9.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/units/units_0.7-2.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/RandomFieldsUtils/RandomFieldsUtils_0.5.3.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/RandomFields/RandomFields_3.3.8.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/TMBhelper/TMBhelper_1.4.2.tar.gz', repos=NULL, type='source')"

# Install INLA (compatible with VAST 3.7.1 and FishStatsUtils 2.9.1)
RUN R -e "install.packages('https://inla.r-inla-download.org/R/stable/src/contrib/INLA_22.05.07.tar.gz', repos=NULL, type='source')"

# Install core modern packages with compatible Matrix version
RUN R -e "install.packages(c('TMB', 'RcppArmadillo'), repos='https://cloud.r-project.org')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/Matrix/Matrix_1.6-5.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages(c('sf', 'terra', 'stars'), repos='https://cloud.r-project.org')"

# Install data science and visualization packages
RUN R -e "install.packages(c('tidyverse', 'ggplot2', 'dplyr', 'tidyr', 'data.table', 'magrittr', 'purrr'), repos='https://cloud.r-project.org')" && \
    R -e "install.packages(c('reshape2', 'cowplot', 'patchwork', 'kableExtra', 'viridis', 'ggthemes', 'rmdformats'), repos='https://cloud.r-project.org')"

# Install oceanographic and additional spatial packages
RUN R -e "install.packages(c('gsw', 'testthat', 'knitr', 'rmarkdown', 'ncdf4', 'automap', 'geoR', 'fields', 'DHARMa'), repos='https://cloud.r-project.org')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/oce/oce_1.5-0.tar.gz', repos=NULL, type='source')"

# Install VAST ecosystem packages
RUN R -e "devtools::install_github('James-Thorson-NOAA/FishStatsUtils@2.9.1', dependencies = TRUE, upgrade = FALSE, force=TRUE)" && \
    R -e "devtools::install_github('James-Thorson-NOAA/VAST@3.7.1', dependencies = TRUE, upgrade = FALSE, force=TRUE)"

# Install additional VAST utilities
RUN R -e "if (!requireNamespace('remotes', quietly=TRUE)) install.packages('remotes', repos='https://cloud.r-project.org')" && \
    R -e "remotes::install_github('PacificCommunity/ofp-sam-vast-utils', dependencies = FALSE)"

# Install Quarto CLI
RUN curl -L https://github.com/quarto-dev/quarto-cli/releases/download/v1.2.335/quarto-1.2.335-linux-amd64.deb -o quarto.deb && \
    dpkg -i quarto.deb && \
    rm quarto.deb

# Set up workspace and permissions (correct R library path for source installation)
RUN mkdir -p /workspace && chmod -R 777 /workspace && \
    mkdir -p /usr/local/lib/R/library && chmod -R 777 /usr/local/lib/R/library

# Create analyst user with sudo privileges
RUN useradd -m -u 1000 -U -s /bin/bash analyst && \
    echo "analyst ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    echo 'analyst:analyst' | chpasswd && \
    mkdir -p /var/run/sshd

# Switch to analyst user
USER analyst
WORKDIR /workspace

# Configure radian as default R terminal
RUN echo 'if [ -z "$INSIDE_RADIAN" ] && [ -z "$RSTUDIO" ] && [ "$TERM_PROGRAM" != "vscode" ]; then exec radian; fi' > /home/analyst/.radian_profile

EXPOSE 22

CMD ["/bin/bash"]
