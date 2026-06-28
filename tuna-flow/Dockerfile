# syntax=docker/dockerfile:1.7

FROM rocker/rstudio:4.6.0

ARG QUARTO_VERSION=1.9.38
ARG MFCL_EXECUTABLE_VERSION=v2278
ARG MFCL_EXECUTABLE_DATE=2026-06-16
ARG MFCL_EXECUTABLE_SHA256=8aedcb3fa803609a26f4ba209c0910054cc44b9daa3ad8300c8878cd4390d6cf
ARG MFCLSHINY_REF=fec9ab16b1f7627428d88f65d9cd5c0b55d104b1

LABEL org.pacificcommunity.mfcl.executable="mfclo64"
LABEL org.pacificcommunity.mfcl.version="${MFCL_EXECUTABLE_VERSION}"
LABEL org.pacificcommunity.mfcl.date="${MFCL_EXECUTABLE_DATE}"
LABEL org.pacificcommunity.mfcl.sha256="${MFCL_EXECUTABLE_SHA256}"
LABEL org.pacificcommunity.mfclshiny.ref="${MFCLSHINY_REF}"

ENV KFLOW_RUNTIME_UPDATE=off
ENV KFLOW_RUNTIME_UPDATE_INTERVAL_HOURS=24
ENV KFLOW_RUNTIME_QUIET_INSTALL=true
ENV KFLOW_RUNTIME_LIBRARY=/home/rstudio/R/site-library
ENV KFLOW_RUNTIME_REQUIRE_PRIVATE_PACKAGES=false
ENV MFCL_EXECUTABLE=/home/mfcl/mfclo64
ENV MFCL_EXECUTABLE_VERSION=${MFCL_EXECUTABLE_VERSION}
ENV MFCL_EXECUTABLE_DATE=${MFCL_EXECUTABLE_DATE}
ENV MFCLSHINY_GITHUB_REF=${MFCLSHINY_REF}

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
  'jsonlite','curl','openssl','sys','processx','callr','desc','pkgload', \
  'fs','cachem','memoise','mime','base64enc','digest','fastmap', \
  'yaml','evaluate','xfun','highr','knitr','htmltools','jquerylib', \
  'fontawesome','later','promises','httpuv','htmlwidgets','purrr','tibble' \
))"

RUN Rscript -e "options(repos = c(CRAN='https://cloud.r-project.org/')); install.packages('shiny')"

RUN Rscript -e "options(repos = c(CRAN='https://cloud.r-project.org/')); install.packages(c( \
  'shinyjs','shinydashboard','shinyWidgets','shinyFiles', \
  'DT','plotly','future','rstudioapi','stringr','scales','MASS', \
  'ggplot2','cowplot','dplyr','tidyr','viridis','patchwork','reshape2', \
  'rmdformats','kableExtra','GGally','tidyverse','data.table','here', \
  'remotes','iterators','maps', \
  'rpart.plot','partykit','vip','broom','yardstick','sf' \
))"

RUN Rscript -e "install.packages( \
  'FLCore', \
  repos = c('https://flr.r-universe.dev', 'https://cloud.r-project.org') \
)"

RUN Rscript -e "remotes::install_github('PacificCommunity/ofp-sam-flr4mfcl', upgrade = 'never')"
RUN Rscript -e "remotes::install_github('PacificCommunity/ofp-sam-CondorBox', upgrade = 'never')"
RUN Rscript -e "remotes::install_github('PacificCommunity/tandoori', upgrade = 'never')"

RUN Rscript -e "required <- c( \
  'fs','sass','bslib','rmarkdown','shiny','htmlwidgets', \
  'shinyjs','shinydashboard','shinyWidgets','shinyFiles', \
  'DT','plotly','rmdformats','kableExtra','tidyverse', \
  'jsonlite','curl','yaml','remotes','data.table','ggplot2','dplyr','tidyr', \
  'rpart.plot','partykit','vip','broom','yardstick','sf','maps' \
); missing <- setdiff(required, rownames(installed.packages())); if (length(missing)) stop('Missing required R packages: ', paste(missing, collapse = ', '), call. = FALSE)"

RUN --mount=type=secret,id=github_pat,required=false \
    --mount=type=secret,id=mfclshiny_tarball,required=false \
    set -e; \
    if [ -s /run/secrets/mfclshiny_tarball ]; then \
      cp /run/secrets/mfclshiny_tarball /tmp/mfclshiny.tar.gz; \
      Rscript -e "remotes::install_local('/tmp/mfclshiny.tar.gz', upgrade = 'never', force = TRUE)"; \
      rm -f /tmp/mfclshiny.tar.gz; \
    else \
      GITHUB_PAT="$(cat /run/secrets/github_pat 2>/dev/null || true)"; \
      export GITHUB_PAT; \
      git -c "http.https://github.com/.extraheader=Authorization: Bearer ${GITHUB_PAT}" \
        clone --quiet --depth 50 https://github.com/PacificCommunity/mfclshiny.git /tmp/mfclshiny; \
      git -C /tmp/mfclshiny checkout --quiet "${MFCLSHINY_GITHUB_REF}" || \
        { git -C /tmp/mfclshiny fetch --quiet --depth 1 origin "${MFCLSHINY_GITHUB_REF}" && \
          git -C /tmp/mfclshiny checkout --quiet FETCH_HEAD; }; \
      Rscript -e "remotes::install_local('/tmp/mfclshiny', upgrade = 'never', force = TRUE)"; \
      rm -rf /tmp/mfclshiny; \
    fi; \
    Rscript -e "desc_path <- system.file('DESCRIPTION', package = 'mfclshiny'); fields <- as.list(read.dcf(desc_path)[1, ]); ref <- Sys.getenv('MFCLSHINY_GITHUB_REF'); remote <- list(RemoteType = 'github', RemoteHost = 'api.github.com', RemoteRepo = 'mfclshiny', RemoteUsername = 'PacificCommunity', RemoteRef = ref, RemoteSha = ref); fields[names(remote)] <- remote; write.dcf(as.data.frame(fields, stringsAsFactors = FALSE, check.names = FALSE), desc_path); meta_path <- system.file('Meta', 'package.rds', package = 'mfclshiny'); if (file.exists(meta_path)) { meta <- readRDS(meta_path); meta[['DESCRIPTION']][names(remote)] <- unlist(remote); saveRDS(meta, meta_path) }"

COPY scripts/update-kflow-runtime-packages.R /usr/local/bin/update-kflow-runtime-packages.R
COPY scripts/30-update-kflow-runtime-packages /usr/local/bin/30-update-kflow-runtime-packages
COPY scripts/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

RUN chmod -R 777 /var/lib/rstudio-server && \
    chmod -R 777 /home/rstudio

RUN mkdir -p /home/mfcl

COPY mfclo64 /home/mfcl/mfclo64
COPY mfclo64.version /home/mfcl/mfclo64.version

RUN chmod 0755 /home/mfcl/mfclo64 \
      /usr/local/bin/30-update-kflow-runtime-packages \
      /usr/local/bin/docker-entrypoint.sh && \
    echo "${MFCL_EXECUTABLE_SHA256}  /home/mfcl/mfclo64" | sha256sum -c -

RUN ln -sf /home/mfcl/mfclo64 /home/mfcl/mfclo64_2026 && \
    ln -sf /home/mfcl/mfclo64 /home/mfcl/mfclo64_2026_06_16_v2278

RUN echo "copilot-enabled=1" >> /etc/rstudio/rsession.conf

EXPOSE 3838 3839

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["/init"]
