FROM ubuntu:22.04

# Set non-interactive mode and timezone
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Pacific/Noumea

# Configure timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install basic system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    build-essential \
    python3 \
    python3-pip \
    software-properties-common \
    dirmngr \
    ca-certificates \
    gnupg \
    lsb-release

# Install R 4.1.2 from official repository (more reliable than r-hub)
RUN wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | tee -a /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc && \
    add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/" && \
    apt-get update && \
    apt-get install -y r-base=4.1.2* r-base-dev=4.1.2*

# Install comprehensive system dependencies and development libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
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
        librsvg2-bin \
        ghostscript \
        inkscape \
        gdal-bin \
        libglu1-mesa-dev \
        libx11-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Configure locale and timezone for New Caledonia
RUN locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 && \
    ln -fs /usr/share/zoneinfo/Pacific/Noumea /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

ENV LANG=en_US.UTF-8

# Install additional LaTeX packages
RUN apt-get update && \
    apt-get install -y \
        texlive-fonts-recommended \
        texlive-fonts-extra \
        lmodern \
        texlive-latex-recommended \
        texlive-base \
        texlive-binaries && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Docker CLI (client only, no daemon)
RUN curl -fsSL https://get.docker.com | sh

# Install radian for enhanced R console experience
RUN pip3 install -U radian

# Configure CRAN repository for R (with explicit repos setting)
RUN mkdir -p /etc/R && \
    echo 'local({' >> /etc/R/Rprofile.site && \
    echo '  r <- getOption("repos")' >> /etc/R/Rprofile.site && \
    echo '  r["CRAN"] <- "https://cloud.r-project.org"' >> /etc/R/Rprofile.site && \
    echo '  options(repos = r)' >> /etc/R/Rprofile.site && \
    echo '})' >> /etc/R/Rprofile.site

# Install devtools package (essential for GitHub installations)
RUN R -e "install.packages('devtools', repos='https://cloud.r-project.org')"

# Install Bioconductor and required dependencies for INLA
RUN R -e "if (!requireNamespace('BiocManager', quietly=TRUE)) install.packages('BiocManager', repos='https://cloud.r-project.org')"
RUN R -e "BiocManager::install(c('graph', 'Rgraphviz'), ask=FALSE, update=FALSE)"

# Install legacy spatial packages in correct dependency order
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/sp/sp_1.4-5.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/raster/raster_3.4-5.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/rgdal/rgdal_1.5-23.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/rgeos/rgeos_0.5-9.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/maptools/maptools_1.1-8.tar.gz', repos=NULL, type='source')"

# Install supporting spatial and statistical packages
RUN R -e "install.packages(c('XML', 'spacetime', 'colorspace', 'plotrix', 'dismo', 'aqp', 'pixmap', 'plyr', 'colorRamps', 'scales', 'gstat', 'zoo', 'RColorBrewer', 'RSAGA', 'classInt'), repos='https://cloud.r-project.org')"

# Install additional legacy packages from archives
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/plotKML/plotKML_0.5-9.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/units/units_0.7-2.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/RandomFieldsUtils/RandomFieldsUtils_0.5.3.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/RandomFields/RandomFields_3.3.8.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/TMBhelper/TMBhelper_1.4.2.tar.gz', repos=NULL, type='source')"

# Install INLA 22.05.07 (compatible with VAST 3.7.1 and FishStatsUtils 2.9.1)
RUN R -e "install.packages('https://inla.r-inla-download.org/R/stable/src/contrib/INLA_22.05.07.tar.gz', repos=NULL, type='source')"

# Install core modern spatial and statistical packages
RUN R -e "install.packages(c('TMB', 'RcppArmadillo', 'Matrix', 'sf', 'terra', 'stars'), repos='https://cloud.r-project.org')"

# Install data manipulation and visualization packages
RUN R -e "install.packages(c('ggplot2', 'dplyr', 'tidyr', 'data.table', 'magrittr', 'ggthemes', 'rmdformats'), repos='https://cloud.r-project.org')"

# Install tidyverse (comprehensive data science toolkit)
RUN R -e "install.packages('tidyverse', repos='https://cloud.r-project.org')"

# Install additional visualization and utility packages
RUN R -e "install.packages(c('purrr', 'reshape2', 'cowplot', 'patchwork', 'kableExtra', 'viridis'), repos='https://cloud.r-project.org')"

# Install FishStatsUtils 2.9.1 and VAST 3.7.1 from GitHub
RUN R -e "devtools::install_github('James-Thorson-NOAA/FishStatsUtils@2.9.1', dependencies = TRUE, upgrade = FALSE, force=TRUE)"
RUN R -e "devtools::install_github('James-Thorson-NOAA/VAST@3.7.1', dependencies = TRUE, upgrade = FALSE, force=TRUE)"

# Install additional VAST utilities
RUN R -e "if (!requireNamespace('remotes', quietly=TRUE)) install.packages('remotes', repos='https://cloud.r-project.org')"
RUN R -e "remotes::install_github('PacificCommunity/ofp-sam-vast-utils', dependencies = FALSE)"

# Install oceanographic analysis packages
RUN R -e "install.packages(c('gsw', 'testthat', 'knitr', 'rmarkdown', 'ncdf4'), repos='https://cloud.r-project.org')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/oce/oce_1.5-0.tar.gz', repos=NULL, type='source')"

# Install additional spatial analysis packages
RUN R -e "install.packages(c('automap', 'geoR', 'fields'), repos='https://cloud.r-project.org')"

# Install Quarto CLI (compatible with R 4.1.2)
RUN curl -L https://github.com/quarto-dev/quarto-cli/releases/download/v1.2.335/quarto-1.2.335-linux-amd64.deb -o quarto.deb && \
    dpkg -i quarto.deb && \
    rm quarto.deb

# Create workspace directory with proper permissions
RUN mkdir -p /workspace && chmod -R 777 /workspace

# Fix R library permissions (corrected path)
RUN chmod -R 777 /usr/local/lib/R/site-library

# Create analyst user with sudo privileges for development container
RUN useradd -m -u 1000 -U -s /bin/bash analyst && \
    echo "analyst ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Configure SSH server for remote access (default password: analyst)
RUN echo 'analyst:analyst' | chpasswd && \
    mkdir -p /var/run/sshd

# Expose SSH port
EXPOSE 22

# Switch to analyst user and set working directory
USER analyst
WORKDIR /workspace

# Configure radian as default R terminal for enhanced experience
RUN echo 'if [ -z "$INSIDE_RADIAN" ] && [ -z "$RSTUDIO" ] && [ "$TERM_PROGRAM" != "vscode" ]; then exec radian; fi' > /home/analyst/.radian_profile

# Start SSH daemon
CMD ["/usr/sbin/sshd", "-D"]
