# syntax=docker/dockerfile:1.7

FROM rocker/rstudio:4.5.3

ARG QUARTO_VERSION=1.9.38
ARG MFCLRTMB_REF=main
ARG MFCLKIT_REF=main
ARG MFCLSHINY_REF=main
ARG KFLOWKIT_REF=main

ENV MFCLRTMB_REF=${MFCLRTMB_REF}
ENV MFCLKIT_REF=${MFCLKIT_REF}
ENV MFCLSHINY_REF=${MFCLSHINY_REF}
ENV KFLOWKIT_REF=${KFLOWKIT_REF}
ENV KFLOW_RUNTIME_PACKAGES="mfclrtmb=PacificCommunity/ofp-sam-mfclrtmb@${MFCLRTMB_REF},mfclkit=PacificCommunity/ofp-sam-mfclkit@${MFCLKIT_REF},mfclshiny=PacificCommunity/mfclshiny@${MFCLSHINY_REF},KflowKit=kyuhank/KflowKit@${KFLOWKIT_REF}"
ENV KFLOW_RUNTIME_UPDATE=auto
ENV KFLOW_RUNTIME_UPDATE_INTERVAL_HOURS=24
ENV KFLOW_RUNTIME_LIBRARY=/home/rstudio/R/site-library

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

RUN curl -L \
    "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.deb" \
    -o /tmp/quarto.deb && \
    apt-get update && apt-get install -y /tmp/quarto.deb && \
    rm -f /tmp/quarto.deb && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN Rscript -e "options(repos = c(CRAN='https://cloud.r-project.org/')); install.packages(c( \
  'Rcpp','cpp11','cli','glue','rlang','lifecycle','vctrs','withr', \
  'jsonlite','curl','openssl','sys','processx','callr','desc','pkgload', \
  'fs','cachem','memoise','mime','base64enc','digest','fastmap', \
  'yaml','evaluate','xfun','highr','knitr','htmltools','jquerylib', \
  'fontawesome','later','promises','httpuv','htmlwidgets','purrr','tibble' \
))"

RUN Rscript -e "options(repos = c(CRAN='https://cloud.r-project.org/')); install.packages(c( \
  'sass','bslib','rmarkdown','shiny' \
))"

RUN Rscript -e "options(repos = c(CRAN='https://cloud.r-project.org/')); install.packages(c( \
  'shinyjs','shinydashboard','shinyWidgets','shinyFiles', \
  'DT','plotly','future','rstudioapi','stringr','scales','MASS', \
  'ggplot2','cowplot','dplyr','tidyr','viridis','patchwork','reshape2', \
  'rmdformats','kableExtra','GGally','tidyverse','data.table','here', \
  'remotes','iterators','svglite','ragg','textshaping','systemfonts', \
  'magick','rsvg','rpart.plot','partykit','vip','broom','yardstick' \
))"

RUN Rscript -e "install.packages( \
  'FLCore', \
  repos = c('https://flr.r-universe.dev', 'https://cloud.r-project.org') \
)"

RUN Rscript -e "remotes::install_github('PacificCommunity/ofp-sam-flr4mfcl', upgrade = 'never')"
RUN Rscript -e "remotes::install_github('PacificCommunity/ofp-sam-CondorBox', upgrade = 'never')"
RUN Rscript -e "remotes::install_github('PacificCommunity/tandoori', upgrade = 'never')"

COPY scripts/update-kflow-runtime-packages.R /usr/local/bin/update-kflow-runtime-packages.R
COPY scripts/30-update-kflow-runtime-packages /usr/local/bin/30-update-kflow-runtime-packages
COPY scripts/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

RUN --mount=type=secret,id=github_pat \
    export GITHUB_PAT="$(cat /run/secrets/github_pat 2>/dev/null || true)" && \
    if [ -z "$GITHUB_PAT" ]; then \
      echo "[bet2026-flow-build] github_pat secret is required to preinstall private workflow packages." >&2; \
      exit 1; \
    fi && \
    KFLOW_RUNTIME_LIBRARY=/usr/local/lib/R/site-library \
    KFLOW_RUNTIME_FORCE_UPDATE=1 \
    KFLOW_RUNTIME_UPDATE_INTERVAL_HOURS=0 \
    Rscript /usr/local/bin/update-kflow-runtime-packages.R

RUN chmod -R 777 /var/lib/rstudio-server && \
    chmod -R 777 /home/rstudio

RUN mkdir -p /home/mfcl

COPY mfclo64_2026_02_04_vsn2278 \
     /home/mfcl/mfclo64_2026_02_04_vsn2278

RUN chmod 0755 /home/mfcl/mfclo64_2026_02_04_vsn2278 \
  /usr/local/bin/30-update-kflow-runtime-packages \
  /usr/local/bin/docker-entrypoint.sh

RUN ln -sf /home/mfcl/mfclo64_2026_02_04_vsn2278 /home/mfcl/mfclo64_2026 && \
    ln -sf /home/mfcl/mfclo64_2026_02_04_vsn2278 /home/mfcl/mfclo64

RUN echo "copilot-enabled=1" >> /etc/rstudio/rsession.conf

EXPOSE 3838 3839

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["/init"]

