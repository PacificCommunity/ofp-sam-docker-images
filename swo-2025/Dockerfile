# Use the rocker/rstudio base image
FROM rocker/rstudio:4.2.3

# Install required dependencies including OpenSSH client and spatial libraries
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    lsb-release \
    libclang-dev \
    libcurl4-openssl-dev \
    openssh-client \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    libudunits2-dev \
    libssl-dev \
    libxml2-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install docker-compose (pinned to version 2.23.0)
RUN curl -L "https://github.com/docker/compose/releases/download/2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# Install required R packages from CRAN
RUN Rscript -e "install.packages(c('ggplot2', 'GGally', 'viridis', 'dplyr', 'cowplot', 'parallel', 'tidyr', 'patchwork', 'reshape2', 'iterators', 'remotes', 'data.table', 'magrittr', 'sp', 'raster', 'ggthemes', 'splines', 'rgdal', 'rgeos', 'sf', 'terra'), repos='https://cloud.r-project.org/')"

# Install FLCore and other FLR-related packages
RUN Rscript -e "install.packages('FLCore', repos='http://flr-project.org/R')"
RUN Rscript -e "remotes::install_github('PacificCommunity/ofp-sam-flr4mfcl')"
RUN Rscript -e "remotes::install_github('PacificCommunity/ofp-sam-CondorBox')"

# Install specific versions of VAST and FishStatsUtils from GitHub
RUN Rscript -e "remotes::install_github('James-Thorson-NOAA/VAST@3.7.1')"
RUN Rscript -e "remotes::install_github('James-Thorson-NOAA/FishStatsUtils@2.9.1')"

# (Optional) Install ofp.sam.vast.utils if needed
RUN Rscript -e "remotes::install_github('PacificCommunity/ofp-sam-vast-utils')"

# Ensure correct permissions for RStudio Server
RUN chmod -R 777 /var/lib/rstudio-server && chmod -R 777 /home/rstudio

# Enable GitHub Copilot for RStudio (if applicable)
RUN echo "copilot-enabled=1" >> /etc/rstudio/rsession.conf

