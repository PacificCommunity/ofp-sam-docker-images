# Use the rocker/rstudio base image
FROM rocker/rstudio:4.5.0

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gfortran \
    liblapack-dev \
    libblas-dev \
    libcurl4-openssl-dev \
    libxml2-dev \
    cmake \
    libnlopt-dev \
    libssl-dev \
    pkg-config \
    wget \
    git \
    libudunits2-dev \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    libgsl-dev \
    libv8-dev \
    libnetcdf-dev \
    libglpk-dev \
    libfreetype6-dev \
    libpng-dev \
    libtiff5-dev \
    && update-ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install docker-compose
RUN curl -L "https://github.com/docker/compose/releases/download/2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

    # Set default CRAN repository for R
RUN mkdir -p /etc/R && \
    echo 'options(repos = c(CRAN = \"https://cloud.r-project.org\"))' >> /etc/R/Rprofile.site

    # Install required R packages in proper order
RUN Rscript -e "install.packages(c('iterators','remotes','tidyverse','magrittr','data.table','sp','sf','randomForest','sdmTMB'), repos='https://cloud.r-project.org/')"
RUN Rscript -e  "remotes::install_github('flr/FLCore')"
RUN Rscript -e "remotes::install_github('PacificCommunity/ofp-sam-flr4mfcl')"
RUN Rscript -e "remotes::install_github('PacificCommunity/ofp-sam-frqit')"
RUN Rscript -e "remotes::install_github('pbs-assess/sdmTMBextra')"
RUN Rscript -e "install.packages('INLA', repos=c(getOption('repos'), INLA='https://inla.r-inla-download.org/R/stable'), dependencies=TRUE)"
RUN Rscript -e "install.packages('tidyverse', repos = 'https://cloud.r-project.org', dependencies = TRUE)"

# Ensure correct permissions for RStudio Server
RUN chmod -R 777 /var/lib/rstudio-server && chmod -R 777 /home/rstudio

# Enable GitHub Copilot for RStudio (if applicable)
RUN echo "copilot-enabled=1" >> /etc/rstudio/rsession.conf
