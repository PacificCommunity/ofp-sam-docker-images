FROM rocker/r-ver:4.5.0

# 1. Set non-interactive mode and Nouméa timezone
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Pacific/Noumea

# 2. Install system libraries for R, spatial, and PDF/OCR/image support
RUN apt-get update && apt-get install -y --no-install-recommends \
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
    libv8-dev \
    libnetcdf-dev \
    libglpk-dev \         
    fonts-dejavu \
    fonts-liberation \
    libfreetype6-dev \
    libpng-dev \
    libtiff5-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. Install Quarto CLI
RUN wget -qO- https://quarto.org/download/latest/quarto-linux-amd64.deb > quarto.deb \
    && dpkg -i quarto.deb || apt-get -fy install \
    && rm quarto.deb

# 4. Install core R packages (from CRAN)
RUN install2.r --error --skipinstalled \
    data.table \
    magrittr \
    dplyr \
    tidyr \
    purrr \
    splines \
    sp \
    sf \
    units \
    oce \
    remotes \
    ggplot2 \
    TMB \
    ggthemes \
    rmdformats \
    kableExtra \
    GGally \
    rmarkdown \
    viridis \
    cowplot \
    parallel \
    patchwork \
    reshape2 \
    iterators \
    tidyverse \
    igraph

# 5. Install R packages from GitHub and special repositories
RUN Rscript -e "remotes::install_github('james-thorson/VAST@main', INSTALL_opts='--no-staged-install')" \
    && Rscript -e "remotes::install_github('james-thorson/FishStatsUtils@main', INSTALL_opts='--no-staged-install')" \
    && Rscript -e "remotes::install_github('vast-lib/tinyVAST', dependencies=TRUE)" \
    && Rscript -e "remotes::install_github('pbs-assess/sdmTMB')" \
    && Rscript -e "install.packages('INLA', repos=c(getOption('repos'), INLA='https://inla.r-inla-download.org/R/stable'), dependencies=TRUE)"

# 6. Install the TinyTeX LaTeX distribution for PDF output support
RUN quarto install tinytex

# 7. Set working directory
WORKDIR /workspace

# 8. (Optional) Expose a port for apps or servers if needed
EXPOSE 8080

# 9. Set default entrypoint
CMD ["bash"]
