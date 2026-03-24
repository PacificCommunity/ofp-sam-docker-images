FROM rocker/rstudio:4.5.2

RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    lsb-release \
    make \
    cmake \
    pkg-config \
    openssh-client \
    git \
    rsync \
    tar \
    procps \
    bc \
    pandoc \
    default-jdk \
    gdal-bin \
    libabsl-dev \
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
    libprotobuf-dev \
    librsvg2-dev \
    libssh2-1-dev \
    libssl-dev \
    libtiff5-dev \
    libudunits2-dev \
    libwebp-dev \
    libxml2-dev \
    protobuf-compiler \
    zlib1g-dev \
    texlive-xetex \
    texlive-latex-extra \
    texlive-fonts-recommended \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -L "https://github.com/docker/compose/releases/download/2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

RUN Rscript -e "options(repos = c(CRAN='https://cloud.r-project.org/')); install.packages(c( \
  'Rcpp','cpp11','cli','glue','rlang','lifecycle','vctrs','withr', \
  'jsonlite','curl','openssl','sys','processx','callr','desc','pkgload', \
  'fs','cachem','memoise','mime','base64enc','digest','fastmap', \
  'yaml','evaluate','xfun','highr','knitr','htmltools','jquerylib', \
  'fontawesome','later','promises','httpuv','htmlwidgets','purrr','tibble' \
))"

RUN Rscript -e "options(repos = c(CRAN='https://cloud.r-project.org/')); install.packages(c('sass','bslib','rmarkdown','shiny'))"

RUN Rscript -e "options(repos = c(CRAN='https://cloud.r-project.org/')); install.packages(c( \
  'shinyjs','shinydashboard','shinyWidgets','shinyFiles', \
  'DT','plotly','future','rstudioapi','stringr','scales','MASS', \
  'ggplot2','cowplot','dplyr','tidyr','viridis','patchwork','reshape2', \
  'rmdformats','kableExtra','GGally','tidyverse','data.table','here', \
  'remotes','iterators','svglite','ragg','textshaping','systemfonts', \
  'magick','rsvg' \
))"

RUN Rscript -e "install.packages('FLCore', repos = c('https://flr.r-universe.dev', 'https://cloud.r-project.org'))"
RUN Rscript -e "remotes::install_github('PacificCommunity/ofp-sam-flr4mfcl')"
RUN Rscript -e "remotes::install_github('PacificCommunity/ofp-sam-CondorBox')"
RUN Rscript -e "remotes::install_github('PacificCommunity/tandoori')"

RUN chmod -R 777 /var/lib/rstudio-server && chmod -R 777 /home/rstudio

RUN mkdir -p /home/mfcl
COPY mfclo64 /home/mfcl/mfclo64
RUN chmod 0755 /home/mfcl/mfclo64

RUN echo "copilot-enabled=1" >> /etc/rstudio/rsession.conf

EXPOSE 3838 3839


