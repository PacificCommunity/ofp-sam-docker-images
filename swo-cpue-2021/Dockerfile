# Use R 4.0.5 base image (closest R version to April 2021)
FROM rocker/r-ver:4.0.5

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
    echo 'options(repos = c(CRAN = "https://cloud.r-project.org"))' >> /etc/R/Rprofile.site

# Install devtools package (for install_github)
RUN R -e "install.packages('devtools')"

# Install Bioconductor dependencies required for INLA
RUN R -e "if (!requireNamespace('BiocManager', quietly=TRUE)) install.packages('BiocManager')"
RUN R -e "BiocManager::install(c('graph', 'Rgraphviz'), ask=FALSE, update=FALSE)"

# Install ofp-sam-vast-utils at the April 2021 version
RUN R -e "devtools::install_github('PacificCommunity/ofp-sam-vast-utils')"

# Install FishStatsUtils 2.9.1 and VAST 3.7.1 with dependencies
RUN R -e "devtools::install_github('James-Thorson-NOAA/FishStatsUtils@2.9.1', dependencies=TRUE)"
RUN R -e "devtools::install_github('James-Thorson-NOAA/VAST@3.7.1', dependencies=TRUE)"

# Downgrade key packages to April 2021 versions - this will overwrite the newer versions
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/sp/sp_1.4-5.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/raster/raster_3.4-5.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/rgdal/rgdal_1.5-23.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/rgeos/rgeos_0.5-5.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/maptools/maptools_1.1-1.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/plotKML/plotKML_0.7-1.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/RandomFields/RandomFields_3.3.8.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/RandomFieldsUtils/RandomFieldsUtils_0.5.3.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/TMBhelper/TMBhelper_1.3.0.tar.gz', repos=NULL, type='source')"

# Downgrade core packages to April 2021 versions
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/Matrix/Matrix_1.3-2.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/TMB/TMB_1.7.20.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/RcppArmadillo/RcppArmadillo_0.10.4.0.0.tar.gz', repos=NULL, type='source')"

# Downgrade INLA to April 2021 version
RUN R -e "install.packages('https://inla.r-inla-download.org/R/stable/src/contrib/Archive/INLA/INLA_21.02.23.tar.gz', repos=NULL, type='source')"

# Downgrade data manipulation packages to April 2021 versions
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/data.table/data.table_1.14.0.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/magrittr/magrittr_2.0.1.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/dplyr/dplyr_1.0.5.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/tidyr/tidyr_1.1.3.tar.gz', repos=NULL, type='source')"

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