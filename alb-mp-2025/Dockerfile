# Use the rocker/rstudio base image
FROM rocker/rstudio:4.5.0

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    openssl \
    gnupg \
    lsb-release \
    libclang-dev \
    libcurl4-openssl-dev \
    libxml2-dev \
    libssl-dev \
    libxml2-dev \
    libgit2-dev git build-essential \
    libcairo2-dev \
    libpng-dev \
    libjpeg-dev \
    libtiff5-dev \
    libgtk2.0-dev \
    make \
    openssh-client \
    bc \
    && update-ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install docker-compose
RUN curl -L "https://github.com/docker/compose/releases/download/2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# Install required R packages in proper order
RUN Rscript -e "install.packages(c('iterators','remotes','tidyverse','magrittr'), repos='https://cloud.r-project.org/')"
RUN Rscript -e  "remotes::install_github('flr/FLCore')"
RUN Rscript -e "remotes::install_github('PacificCommunity/ofp-sam-flr4mfcl')"
RUN Rscript -e "remotes::install_github('PacificCommunity/ofp-sam-frqit')"

# Ensure correct permissions for RStudio Server
RUN chmod -R 777 /var/lib/rstudio-server && chmod -R 777 /home/rstudio

# Enable GitHub Copilot for RStudio (if applicable)
RUN echo "copilot-enabled=1" >> /etc/rstudio/rsession.conf
