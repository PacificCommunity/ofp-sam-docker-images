FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Pacific/Noumea

# Configure timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    git \
    sudo \
    vim \
    nano \
    less \
    build-essential \
    gfortran \
    pkg-config \
    cmake \
    python3 \
    python3-pip \
    python3-venv \
    locales \
    software-properties-common \
    dirmngr \
    ca-certificates \
    gnupg \
    lsb-release \
    openssh-server \
    bash-completion \
    tzdata \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    libudunits2-dev \
    libnetcdf-dev \
    gdal-bin \
    libfontconfig1-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libglu1-mesa-dev \
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

# Configure locale
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 && \
    dpkg-reconfigure -f noninteractive locales

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# Install R 4.1.2 using r-glibc (compatible with GLIBC 2.35)
RUN R_VERSION=4.1.2 && \
    curl -LO https://github.com/r-hub/R/releases/download/v${R_VERSION}/r-${R_VERSION}-glibc_1_$(dpkg --print-architecture).deb && \
    dpkg -i r-${R_VERSION}-glibc_1_$(dpkg --print-architecture).deb && \
    ln -s /opt/R/${R_VERSION}-glibc/bin/R /usr/local/bin/R && \
    ln -s /opt/R/${R_VERSION}-glibc/bin/Rscript /usr/local/bin/Rscript && \
    rm r-${R_VERSION}-glibc_1_$(dpkg --print-architecture).deb

# Install Docker CLI and radian
RUN curl -fsSL https://get.docker.com | sh && \
    pip3 install -U radian

# Configure CRAN repository
RUN mkdir -p /etc/R && \
    echo 'local({' > /etc/R/Rprofile.site && \
    echo '  r <- getOption("repos")' >> /etc/R/Rprofile.site && \
    echo '  r["CRAN"] <- "https://cloud.r-project.org"' >> /etc/R/Rprofile.site && \
    echo '  options(repos = r)' >> /etc/R/Rprofile.site && \
    echo '})' >> /etc/R/Rprofile.site

# Install basic R packages
RUN R -e "install.packages(c('devtools', 'remotes'), repos='https://cloud.r-project.org')"

# Install Bioconductor
RUN R -e "if (!requireNamespace('BiocManager', quietly=TRUE)) install.packages('BiocManager', repos='https://cloud.r-project.org')" && \
    R -e "BiocManager::install(c('graph', 'Rgraphviz'), ask=FALSE, update=FALSE)"

# Step 1: Install basic compilation dependencies
RUN R -e "install.packages(c('Rcpp', 'RcppArmadillo'), repos='https://cloud.r-project.org')"

# Step 2: Install compatible Matrix + TMB versions (CRITICAL for VAST 3.7.1)
# First install Matrix
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/Matrix/Matrix_1.5-4.tar.gz', repos=NULL, type='source')"

# Verify Matrix installation before proceeding
RUN R -e "cat('Matrix version:', as.character(packageVersion('Matrix')), '\n')"

# Install TMB with error handling
RUN R -e "tryCatch({ \
    install.packages('https://cran.r-project.org/src/contrib/Archive/TMB/TMB_1.9.6.tar.gz', repos=NULL, type='source'); \
    cat('TMB installation successful\n') \
}, error = function(e) { \
    cat('TMB installation failed, trying alternative method\n'); \
    install.packages('TMB', repos='https://cloud.r-project.org'); \
})"

# Step 3: Install legacy spatial packages with specific versions for compatibility
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/sp/sp_1.4-5.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/raster/raster_3.4-5.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/rgdal/rgdal_1.5-23.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/rgeos/rgeos_0.5-9.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/maptools/maptools_1.1-8.tar.gz', repos=NULL, type='source')"

# Step 4: Install supporting packages
RUN R -e "install.packages(c('XML', 'spacetime', 'colorspace', 'plotrix', 'dismo', 'aqp', 'pixmap', 'plyr', 'colorRamps', 'scales', 'gstat', 'zoo', 'RColorBrewer', 'RSAGA', 'classInt'), repos='https://cloud.r-project.org')"

# Step 5: Install legacy packages from archives
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/plotKML/plotKML_0.5-9.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/units/units_0.7-2.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/RandomFieldsUtils/RandomFieldsUtils_0.5.3.tar.gz', repos=NULL, type='source')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/RandomFields/RandomFields_3.3.8.tar.gz', repos=NULL, type='source')" 

# Step 6: Install INLA
RUN R -e "install.packages('https://inla.r-inla-download.org/R/stable/src/contrib/INLA_22.05.07.tar.gz', repos=NULL, type='source')"

# Step 7: Install core spatial and statistical R packages (compatible versions)
RUN R -e "install.packages(c('sf', 'terra', 'stars', 'ggplot2', 'dplyr', 'tidyr', 'data.table', 'magrittr', 'ggthemes', 'rmdformats', 'purrr', 'reshape2', 'cowplot', 'patchwork'), repos='https://cloud.r-project.org')"

# Step 8: Install tidyverse and extra packages
RUN R -e "install.packages(c('tidyverse', 'gstat', 'automap', 'geoR', 'fields', 'kableExtra', 'viridis'), repos='https://cloud.r-project.org')"

# Step 9: Install oce dependencies and oce
RUN R -e "install.packages(c('gsw', 'testthat', 'knitr', 'rmarkdown', 'ncdf4'), repos='https://cloud.r-project.org')" && \
    R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/oce/oce_1.5-0.tar.gz', repos=NULL, type='source')"

# Step 10: Verify Matrix/TMB installation before proceeding
RUN R -e "tryCatch({ \
    cat('Matrix version:', as.character(packageVersion('Matrix')), '\n'); \
    cat('TMB version:', as.character(packageVersion('TMB')), '\n'); \
    cat('Both packages are installed successfully\n') \
}, error = function(e) { \
    cat('Package verification failed:', e\$message, '\n'); \
    if(!requireNamespace('TMB', quietly=TRUE)) { \
        cat('TMB not found, installing from CRAN\n'); \
        install.packages('TMB', repos='https://cloud.r-project.org'); \
        cat('TMB version:', as.character(packageVersion('TMB')), '\n'); \
    } \
})"

# Step 11: Install VAST ecosystem (AFTER Matrix/TMB compatibility is ensured)
RUN --mount=type=secret,id=github_token,env=GITHUB_PAT \
    R -e "devtools::install_github('James-Thorson-NOAA/FishStatsUtils@2.9.1', dependencies = TRUE, upgrade = FALSE, force=TRUE)" && \
    R -e "devtools::install_github('James-Thorson-NOAA/VAST@3.7.1', dependencies = TRUE, upgrade = FALSE, force=TRUE)" && \
    R -e "devtools::install_github('PacificCommunity/ofp-sam-vast-utils', dependencies = FALSE)"

# Install Quarto CLI
RUN curl -L https://github.com/quarto-dev/quarto-cli/releases/download/v1.2.335/quarto-1.2.335-linux-amd64.deb -o quarto.deb && \
    dpkg -i quarto.deb && \
    rm quarto.deb

# Set up workspace and permissions
RUN mkdir -p /workspace && chmod -R 777 /workspace && \
    mkdir -p /opt/R/4.1.2-glibc/lib/R/library && chmod -R 777 /opt/R/4.1.2-glibc/lib/R/library

# Create analyst user
RUN useradd -m -u 1000 -U -s /bin/bash analyst && \
    echo "analyst ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    echo 'analyst:analyst' | chpasswd && \
    mkdir -p /var/run/sshd

USER analyst
WORKDIR /workspace

# Configure radian
RUN echo 'if [ -z "$INSIDE_RADIAN" ] && [ -z "$RSTUDIO" ] && [ "$TERM_PROGRAM" != "vscode" ]; then exec radian; fi' > /home/analyst/.radian_profile

EXPOSE 22

CMD ["/bin/bash"]
