# Use R 4.3.2 base image for compatibility with VAST 3.7.1, FishStatsUtils 2.9.1, and legacy spatial packages
FROM rocker/r-ver:4.2.3

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
        libx11-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set locale and timezone for New Caledonia (Pacific/Noumea)
RUN locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 && \
    ln -fs /usr/share/zoneinfo/Pacific/Noumea /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

ENV LANG en_US.UTF-8
ENV TZ Pacific/Noumea

# Install Docker CLI (client only, no daemon)
RUN curl -fsSL https://get.docker.com | sh

# Install radian for a modern R console experience
RUN pip3 install -U radian

# Set default CRAN repository for R
RUN mkdir -p /etc/R && \
    echo 'options(repos = c(CRAN = \"https://cloud.r-project.org\"))' >> /etc/R/Rprofile.site

# Install devtools package (for install_github)
RUN R -e "install.packages('devtools')"

# Install Bioconductor dependencies required for INLA
RUN R -e "if (!requireNamespace('BiocManager', quietly=TRUE)) install.packages('BiocManager')"
RUN R -e "BiocManager::install(c('graph', 'Rgraphviz'), ask=FALSE, update=FALSE)"

# Legacy spatial/statistical dependencies (order matters)
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/sp/sp_1.6-1.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/raster/raster_3.5-21.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/rgdal/rgdal_1.6-7.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/rgeos/rgeos_0.6-4.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/maptools/maptools_1.1-8.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/plotKML/plotKML_0.5-9.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/RandomFieldsUtils/RandomFieldsUtils_1.1.0.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/RandomFields/RandomFields_3.3.8.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/TMBhelper/TMBhelper_1.4.2.tar.gz', repos=NULL, type='source')"

# INLA 22.05.07 (compatible with VAST 3.7.1 and FishStatsUtils 2.9.1)
RUN R -e "install.packages('https://inla.r-inla-download.org/R/stable/src/contrib/INLA_22.05.07.tar.gz', repos=NULL, type='source')"

# Install core spatial and statistical R packages (compatible versions)
RUN R -e "install.packages(c('TMB', 'RcppArmadillo', 'Matrix', 'sf', 'terra', 'stars', 'ggplot2', 'dplyr', 'tidyr', 'data.table', 'magrittr', 'ggthemes'))"

# Install FishStatsUtils 2.9.1 and VAST 3.7.1
RUN R -e "devtools::install_github('James-Thorson-NOAA/FishStatsUtils@2.9.1', dependencies = TRUE, upgrade = FALSE, force=TRUE)"
RUN R -e "devtools::install_github('James-Thorson-NOAA/VAST@3.7.1', dependencies = TRUE, upgrade = FALSE, force=TRUE)"


# Install oce (latest GitHub version for best compatibility)
RUN R -e "if (!require('remotes')) install.packages('remotes'); remotes::install_github('dankelley/oce@develop')"

# Install tidyverse and extra spatial/statistical packages
RUN R -e "install.packages('tidyverse')"
RUN R -e "install.packages(c('gstat', 'automap', 'geoR', 'fields'))"

# Create workspace directory and set permissions
RUN mkdir -p /workspace && chmod -R 777 /workspace
RUN chmod -R 777 /usr/local/lib/R/site-library

# Create analyst user with passwordless sudo for devcontainer
RUN useradd -m -u 1000 -U -s /bin/bash analyst && \
    echo "analyst ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Set up SSH server for remote access (default password: analyst)
RUN echo 'analyst:analyst' | chpasswd && \
    mkdir /var/run/sshd

EXPOSE 22

USER analyst
WORKDIR /workspace

# Set radian as the default R terminal for analyst
RUN echo 'if [ -z \"$INSIDE_RADIAN\" ] && [ -z \"$RSTUDIO\" ] && [ \"$TERM_PROGRAM\" != \"vscode\" ]; then exec radian; fi' > /home/analyst/.radian_profile

CMD ["/usr/sbin/sshd", "-D"]

