# Use the rocker/rstudio base image
FROM rocker/rstudio:4.5.2

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    lsb-release \
    libclang-dev \
    libcurl4-openssl-dev \
    libxml2-dev \
    libcairo2-dev \
    libpng-dev \
    libjpeg-dev \
    libtiff5-dev \
    libgtk2.0-dev \
    libssl-dev \
    libssh2-1-dev \
    libgit2-dev \
    libfontconfig1-dev \
    libfreetype6-dev \
    libfribidi-dev \
    libharfbuzz-dev \
    zlib1g-dev \
    texlive-xetex \
    texlive-latex-extra \
    texlive-fonts-recommended \
    pandoc \
    make \
    openssh-client \
    git \
    rsync \
    tar \
    procps \
    bc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install docker-compose
RUN curl -L "https://github.com/docker/compose/releases/download/2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# Install required R packages
RUN Rscript -e "install.packages(c(
  'svglite','ggplot2','rmdformats','kableExtra','GGally','rmarkdown',
  'viridis','dplyr','cowplot','parallel','tidyr','patchwork','reshape2',
  'iterators','remotes','tidyverse','data.table','here',
  'shiny','shinyjs','shinydashboard','shinyWidgets','shinyFiles',
  'DT','plotly','future','promises','later','htmltools','stringr',
  'purrr','tibble','scales','MASS','rstudioapi'
), repos='https://cloud.r-project.org/')"

RUN Rscript -e "install.packages('FLCore', repos = c('https://flr.r-universe.dev', 'https://cloud.r-project.org'))"
RUN Rscript -e "remotes::install_github('PacificCommunity/ofp-sam-flr4mfcl')"
RUN Rscript -e "remotes::install_github('PacificCommunity/ofp-sam-CondorBox')"
RUN Rscript -e "remotes::install_github('PacificCommunity/tandoori')"

# Ensure correct permissions for RStudio Server
RUN chmod -R 777 /var/lib/rstudio-server && chmod -R 777 /home/rstudio

# Create /home/mfcl directory and copy mfclo64
RUN mkdir -p /home/mfcl
COPY mfclo64 /home/mfcl/mfclo64
RUN chmod 0755 /home/mfcl/mfclo64

# Enable GitHub Copilot for RStudio (if applicable)
RUN echo "copilot-enabled=1" >> /etc/rstudio/rsession.conf

EXPOSE 3838 3839
