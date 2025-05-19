# Use minimal R 4.3.2 base image for maximum compatibility with modern packages
FROM rocker/r-ver:4.3.2

# Install system dependencies and development libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        git \
        curl \
        libcurl4-openssl-dev \
        libssl-dev \
        libxml2-dev \
        libgdal-dev \
        libgeos-dev \
        libproj-dev \
        libudunits2-dev \
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
        gdal-bin && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Docker CLI (client only, no daemon)
RUN curl -fsSL https://get.docker.com | sh

# Install radian for a modern R console experience
RUN pip3 install -U radian

# Set default CRAN repository for R (create directory if needed)
RUN mkdir -p /etc/R && \
    echo 'options(repos = c(CRAN = "https://cloud.r-project.org"))' >> /etc/R/Rprofile.site

# Install devtools package (for install_github)
RUN R -e "install.packages('devtools')"

# Install Bioconductor dependencies required for INLA
RUN R -e "if (!requireNamespace('BiocManager', quietly=TRUE)) install.packages('BiocManager')"
RUN R -e "BiocManager::install(c('graph', 'Rgraphviz'), ask=FALSE, update=FALSE)"

# Install fmesher from CRAN (required for INLA and VAST)
RUN R -e "install.packages('fmesher')"

# Install INLA from the official repository
RUN R -e "install.packages('INLA', repos=c(getOption('repos'), INLA='https://inla.r-inla-download.org/R/stable'), dep=TRUE)"

# Install core spatial and statistical R packages
RUN R -e "install.packages(c('TMB', 'RcppArmadillo', 'Matrix', \
    'sf', 'sp', 'terra', 'stars', 'ggplot2', 'dplyr', 'tidyr', 'data.table', 'magrittr', 'ggthemes'))"

# Install archived rgdal and rgeos for legacy dependencies
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/rgdal/rgdal_1.6-7.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/rgeos/rgeos_0.6-4.tar.gz', repos=NULL, type='source')"

# Install FishStatsUtils 2.9.1 using devtools (no v in tag)
RUN R -e "devtools::install_github('James-Thorson-NOAA/FishStatsUtils@2.9.1')"

# Install VAST 3.7.1 using devtools (no v in tag)
RUN R -e "devtools::install_github('James-Thorson-NOAA/VAST@3.7.1')"

# Install additional utility package for VAST analyses
RUN R -e "devtools::install_github('PacificCommunity/ofp-sam-vast-utils')"

# Set working directory for user projects
WORKDIR /workspace

# Set permissions for the workspace directory
RUN chmod -R 777 /workspace

# Create a non-root user for security best practices
RUN useradd -m -u 1000 -U analyst
USER analyst


