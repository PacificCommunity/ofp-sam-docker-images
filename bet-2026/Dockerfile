# Use the rocker/rstudio base image
FROM rocker/rstudio:4.5.2

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    lsb-release \
    make \
    openssh-client \
    git \
    rsync \
    tar \
    procps \
    bc \
    pandoc \
    default-jdk \
    gdal-bin \
    libclang-dev \
    libcairo2-dev \
    libcurl4-openssl-dev \
    libfontconfig1-dev \
    libfreetype6-dev \
    libfribidi-dev \
    libgdal-dev \
    libgeos-dev \
    libgit2-dev \
    libgtk2.0-dev \
    libharfbuzz-dev \
    libjpeg-dev \
    libmagick++-dev \
    libpng-dev \
    libproj-dev \
    librsvg2-dev \
    libssh2-1-dev \
    libssl-dev \
    libtiff5-dev \
    libudunits2-dev \
    libwebp-dev \
    libxml2-dev \
    zlib1g-dev \
    texlive-xetex \
    texlive-latex-extra \
    texlive-fonts-recommended \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install docker-compose
RUN curl -L "https://github.com/docker/compose/releases/download/2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# Install core R dependencies first
RUN Rscript -e "install.packages(c( \
  'fs','cachem','memoise','mime','sass','base64enc','digest','fastmap', \
  'jquerylib','fontawesome','yaml','evaluate','xfun','highr','knitr', \
  'bslib','htmltools','later','promises','httpuv','htmlwidgets', \
  'Rcpp','cpp11','cli','glue','rlang','lifecycle','vctrs','withr', \
  'jsonlite','curl','openssl','sys','processx','callr','desc','pkgload' \
), repos='https://cloud.r-project.org/', dependencies=TRUE)"

# Install Shiny, plotting, and workflow packages
RUN Rscript -e "install.packages(c( \
  'shiny','shinyjs','shinydashboard','shinyWidgets','shinyFiles', \
  'DT','plotly','future','rstudioapi','stringr','purrr','tibble', \
  'scales','MASS','ggplot2','cowplot','dplyr','tidyr','viridis', \
  'patchwork','reshape2','rmarkdown','rmdformats','kableExtra', \
  'GGally','tidyverse','data.table','here','remotes','iterators', \
  'svglite','ragg','textshaping','systemfonts','magick','rsvg' \
), repos='https://cloud.r-project.org/', dependencies=TRUE)"

# Install project-specific R packages
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
