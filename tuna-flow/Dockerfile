# syntax=docker/dockerfile:1.7

FROM rocker/rstudio:4.6.0

ARG QUARTO_VERSION=1.9.38
ARG VIP_COMMIT=c5b90e78c64adc440f6742f69d364c3a711e10e1
ARG FLCORE_COMMIT=0642117cb7b66d398abc084f814c7c8b4a12dc8d
ARG FLR4MFCL_COMMIT=5a29a9b3246bd19dcff350ded7e0e5099145da5e
ARG CONDORBOX_COMMIT=9ceeb908fdb46b30e00e04aa531184e1727b3227
ARG TANDOORI_COMMIT=270031c8ff9afa15fa836a9d082152eddaa84363
ARG KFLOWKIT_COMMIT=934ceccce062d1d659348ac95f9e8c8e20bcf979
ARG MFCLRTMB_COMMIT=92f2878b9d1e17cc2a8b4b011bd791e562ddd477
ARG MFCLKIT_COMMIT=44abaaa05692db7ae3e0ec0e52250c51714d1e50
ARG MFCLSHINY_COMMIT=d76d3cebb3007c633ae64ee8f96cb75632b7d79c
ARG MFCL_EXECUTABLE_VERSION=v25-strict-tag-nb-dm-report
ARG MFCL_EXECUTABLE_FULL_VERSION=2.5.0-strict-tag-nb-dm-report
ARG MFCL_EXECUTABLE_DATE=2026-07-18
ARG MFCL_EXECUTABLE_SHA256=f5bc1e232a86e51f920bce7271d8e0930d0b160e4d18dc46de44078f0fa24cd0
ARG MFCL_EXECUTABLE_VARIANT=strict-tag-nb-dm-report
ARG MFCL_EXECUTABLE_SOURCE=kyuhank/ofp-sam-mfcl@1321ccd
ARG MFCL_2023_DIAGNOSTIC_VERSION=2.2.2.0
ARG MFCL_2023_DIAGNOSTIC_SOURCE=PacificCommunity/ofp-sam-bet-2023-diagnostic@81fc412
ARG MFCL_2023_DIAGNOSTIC_SHA256=b872c4d049a305d6d89600aea50ffb5d714ab1e5083c44cc712464612dd66aa2

LABEL org.pacificcommunity.mfcl.executable="mfclo64"
LABEL org.pacificcommunity.mfcl.version="${MFCL_EXECUTABLE_FULL_VERSION}"
LABEL org.pacificcommunity.mfcl.version_code="${MFCL_EXECUTABLE_VERSION}"
LABEL org.pacificcommunity.mfcl.date="${MFCL_EXECUTABLE_DATE}"
LABEL org.pacificcommunity.mfcl.sha256="${MFCL_EXECUTABLE_SHA256}"
LABEL org.pacificcommunity.mfcl.variant="${MFCL_EXECUTABLE_VARIANT}"
LABEL org.pacificcommunity.mfcl.source="${MFCL_EXECUTABLE_SOURCE}"
LABEL org.pacificcommunity.mfcl.2023_diagnostic.version="${MFCL_2023_DIAGNOSTIC_VERSION}"
LABEL org.pacificcommunity.mfcl.2023_diagnostic.source="${MFCL_2023_DIAGNOSTIC_SOURCE}"
LABEL org.pacificcommunity.mfcl.2023_diagnostic.sha256="${MFCL_2023_DIAGNOSTIC_SHA256}"

ENV KFLOW_RUNTIME_UPDATE=off
ENV KFLOW_RUNTIME_PACKAGES=none
ENV MFCL_EXECUTABLE=/home/mfcl/mfclo64
ENV MFCL_EXECUTABLE_VERSION=${MFCL_EXECUTABLE_VERSION}
ENV MFCL_EXECUTABLE_FULL_VERSION=${MFCL_EXECUTABLE_FULL_VERSION}
ENV MFCL_EXECUTABLE_DATE=${MFCL_EXECUTABLE_DATE}
ENV MFCL_EXECUTABLE_SHA256=${MFCL_EXECUTABLE_SHA256}
ENV MFCL_EXECUTABLE_VARIANT=${MFCL_EXECUTABLE_VARIANT}
ENV MFCL_EXECUTABLE_SOURCE=${MFCL_EXECUTABLE_SOURCE}
ENV MFCL_2023_DIAGNOSTIC_EXECUTABLE=/home/mfcl/mfclo64_2023_diagnostic_2.2.2.0
ENV MFCL_2023_DIAGNOSTIC_VERSION=${MFCL_2023_DIAGNOSTIC_VERSION}

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    make \
    cmake \
    pkg-config \
    unzip \
    openssh-client \
    optipng \
    pngquant \
    git \
    rsync \
    tar \
    procps \
    bc \
    pandoc \
    imagemagick \
    jpegoptim \
    libcairo2-dev \
    libcurl4-openssl-dev \
    libfontconfig1-dev \
    libfreetype6-dev \
    libfribidi-dev \
    libgdal-dev \
    libgeos-dev \
    libgit2-dev \
    libharfbuzz-dev \
    libjpeg-dev \
    libpng-dev \
    libproj-dev \
    libssh2-1-dev \
    libssl-dev \
    libtiff5-dev \
    libudunits2-dev \
    libuv1-dev \
    libwebp-dev \
    libxml2-dev \
    webp \
    zlib1g-dev \
    lmodern \
    texlive-xetex \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-plain-generic \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN kpsewhich soul.sty >/dev/null && \
    kpsewhich tocloft.sty >/dev/null && \
    kpsewhich lmodern.sty >/dev/null

RUN set -eux; \
    for url in \
      https://ctan.math.illinois.edu/fonts/fontawesome5.zip \
      https://ctan.math.utah.edu/ctan/tex-archive/fonts/fontawesome5.zip \
      https://mirrors.rit.edu/CTAN/fonts/fontawesome5.zip \
      https://mirrors.ctan.org/fonts/fontawesome5.zip; do \
      curl -fsSL --connect-timeout 15 --max-time 60 --retry 2 --retry-delay 2 \
        "$url" -o /tmp/fontawesome5.zip && break; \
      rm -f /tmp/fontawesome5.zip; \
    done; \
    test -s /tmp/fontawesome5.zip && \
    unzip -q /tmp/fontawesome5.zip -d /tmp && \
    install -d \
      /usr/local/share/texmf/tex/latex/fontawesome5 \
      /usr/local/share/texmf/fonts/type1/public/fontawesome5 \
      /usr/local/share/texmf/fonts/tfm/public/fontawesome5 \
      /usr/local/share/texmf/fonts/opentype/public/fontawesome5 \
      /usr/local/share/texmf/fonts/enc/dvips/fontawesome5 \
      /usr/local/share/texmf/fonts/map/dvips/fontawesome5 && \
    cp -a /tmp/fontawesome5/tex/. /usr/local/share/texmf/tex/latex/fontawesome5/ && \
    cp -a /tmp/fontawesome5/type1/. /usr/local/share/texmf/fonts/type1/public/fontawesome5/ && \
    cp -a /tmp/fontawesome5/tfm/. /usr/local/share/texmf/fonts/tfm/public/fontawesome5/ && \
    cp -a /tmp/fontawesome5/opentype/. /usr/local/share/texmf/fonts/opentype/public/fontawesome5/ && \
    cp -a /tmp/fontawesome5/enc/. /usr/local/share/texmf/fonts/enc/dvips/fontawesome5/ && \
    cp -a /tmp/fontawesome5/map/. /usr/local/share/texmf/fonts/map/dvips/fontawesome5/ && \
    rm -rf /tmp/fontawesome5 /tmp/fontawesome5.zip && \
    mktexlsr && \
    updmap-sys --enable Map=fontawesome5.map && \
    kpsewhich fontawesome5.sty >/dev/null

RUN curl -L \
    "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.deb" \
    -o /tmp/quarto.deb && \
    apt-get update && apt-get install -y /tmp/quarto.deb && \
    rm -f /tmp/quarto.deb && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN Rscript -e "options(repos = c(CRAN='https://cloud.r-project.org/')); install.packages(c( \
  'Rcpp','cpp11','cli','glue','rlang','lifecycle','vctrs','withr', \
  'jsonlite','curl','openssl','sys','processx','callr','desc','pkgload','testthat', \
  'fs','cachem','memoise','mime','base64enc','digest','fastmap', \
  'yaml','evaluate','xfun','highr','knitr','htmltools','jquerylib', \
  'fontawesome','later','promises','httpuv','htmlwidgets','purrr','tibble' \
))"

RUN Rscript -e "options(repos = c(CRAN='https://cloud.r-project.org/')); install.packages(c( \
  'RcppEigen','TMB','RTMB' \
))"

RUN Rscript -e "options(repos = c(CRAN='https://cloud.r-project.org/')); install.packages('shiny')"

RUN Rscript -e "options(repos = c(CRAN='https://cloud.r-project.org/')); install.packages(c( \
  'shinyjs','shinydashboard','shinyWidgets','shinyFiles', \
  'DT','plotly','future','rstudioapi','stringr','scales','MASS', \
  'ggplot2','cowplot','dplyr','tidyr','viridis','patchwork','reshape2', \
  'rmdformats','kableExtra','GGally','tidyverse','data.table','here','ragg', \
  'remotes','iterators','maps', \
  'rpart.plot','partykit','broom','yardstick','sf' \
))"

# vip 0.4.6 is temporarily unavailable from CRAN for R 4.6. Install the
# matching upstream release commit explicitly to keep its existing API stable.
RUN Rscript -e "options(repos = c(CRAN='https://cloud.r-project.org/')); install.packages('foreach'); \
if (!requireNamespace('foreach', quietly = TRUE)) stop('foreach installation failed', call. = FALSE)"

RUN Rscript -e "remotes::install_github( \
  paste0('koalaverse/vip@', '${VIP_COMMIT}'), \
  dependencies = FALSE, upgrade = 'never' \
); if (!requireNamespace('vip', quietly = TRUE)) stop('vip installation failed', call. = FALSE); \
if (as.character(utils::packageVersion('vip')) != '0.4.6') stop('Unexpected vip version: ', utils::packageVersion('vip'), call. = FALSE)"

RUN Rscript -e "remotes::install_github('flr/FLCore@${FLCORE_COMMIT}', dependencies = FALSE, upgrade = 'never')"
RUN Rscript -e "remotes::install_github('PacificCommunity/ofp-sam-flr4mfcl@${FLR4MFCL_COMMIT}', dependencies = FALSE, upgrade = 'never')"
RUN Rscript -e "remotes::install_github('PacificCommunity/ofp-sam-CondorBox@${CONDORBOX_COMMIT}', dependencies = FALSE, upgrade = 'never')"
RUN Rscript -e "remotes::install_github('PacificCommunity/tandoori@${TANDOORI_COMMIT}', dependencies = FALSE, upgrade = 'never')"

# The token is mounted only while this layer is built. It is neither copied into
# the image nor printed. All private packages are pinned to immutable commits.
RUN --mount=type=secret,id=github_pat,required=true \
    Rscript -e "token <- trimws(readLines('/run/secrets/github_pat', warn = FALSE)[1]); \
      if (!nzchar(token)) stop('github_pat build secret is empty', call. = FALSE); \
      install <- function(repo) remotes::install_github(repo, auth_token = token, dependencies = FALSE, upgrade = 'never'); \
      install('kyuhank/KflowKit@${KFLOWKIT_COMMIT}'); \
      install('PacificCommunity/ofp-sam-mfclrtmb@${MFCLRTMB_COMMIT}'); \
      install('PacificCommunity/ofp-sam-mfclkit@${MFCLKIT_COMMIT}'); \
      install('PacificCommunity/mfclshiny@${MFCLSHINY_COMMIT}')"

RUN Rscript -e "required <- c( \
  'fs','sass','bslib','rmarkdown','shiny','htmlwidgets', \
  'shinyjs','shinydashboard','shinyWidgets','shinyFiles', \
  'DT','plotly','rmdformats','kableExtra','tidyverse', \
  'jsonlite','curl','yaml','remotes','data.table','ggplot2','dplyr','tidyr', \
  'rpart.plot','partykit','vip','broom','yardstick','sf','maps', \
  'RcppEigen','TMB','RTMB','FLCore','FLR4MFCL','CondorBox','tandoori', \
  'KflowKit','mfclrtmb','mfclkit','mfclshiny' \
); missing <- setdiff(required, rownames(installed.packages())); if (length(missing)) stop('Missing required R packages: ', paste(missing, collapse = ', '), call. = FALSE)"

COPY scripts/verify-bundled-r-packages.R /usr/local/bin/verify-bundled-r-packages.R
COPY scripts/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

RUN Rscript /usr/local/bin/verify-bundled-r-packages.R \
    --flcore=${FLCORE_COMMIT} \
    --flr4mfcl=${FLR4MFCL_COMMIT} \
    --condorbox=${CONDORBOX_COMMIT} \
    --tandoori=${TANDOORI_COMMIT} \
    --kflowkit=${KFLOWKIT_COMMIT} \
    --mfclrtmb=${MFCLRTMB_COMMIT} \
    --mfclkit=${MFCLKIT_COMMIT} \
    --mfclshiny=${MFCLSHINY_COMMIT}

RUN chmod -R 777 /var/lib/rstudio-server && \
    chmod -R 777 /home/rstudio

RUN mkdir -p /home/mfcl

COPY mfclo64 /home/mfcl/mfclo64
COPY mfclo64.version /home/mfcl/mfclo64.version
COPY mfclo64_2023_diagnostic_2.2.2.0 /home/mfcl/mfclo64_2023_diagnostic_2.2.2.0
COPY mfclo64_2023_diagnostic_2.2.2.0.version /home/mfcl/mfclo64_2023_diagnostic_2.2.2.0.version

RUN chmod 0755 /home/mfcl/mfclo64 \
      /home/mfcl/mfclo64_2023_diagnostic_2.2.2.0 \
      /usr/local/bin/docker-entrypoint.sh && \
    echo "${MFCL_EXECUTABLE_SHA256}  /home/mfcl/mfclo64" | sha256sum -c - && \
    echo "${MFCL_2023_DIAGNOSTIC_SHA256}  /home/mfcl/mfclo64_2023_diagnostic_2.2.2.0" | sha256sum -c -

RUN ln -sf /home/mfcl/mfclo64 /home/mfcl/mfclo64_2026 && \
    ln -sf /home/mfcl/mfclo64 /home/mfcl/mfclo64_2026_07_18_v25_strict_tag_nb_dm_report && \
    ln -sf /home/mfcl/mfclo64_2023_diagnostic_2.2.2.0 /home/mfcl/mfclo64_2023_diagnostic

RUN echo "copilot-enabled=1" >> /etc/rstudio/rsession.conf

EXPOSE 3838 3839

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["/init"]
