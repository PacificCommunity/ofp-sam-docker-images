FROM rocker/r-ver:4.5.0

# 1. Set non-interactive mode and Nouméa timezone
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Pacific/Noumea

# 2. Install system libraries required for R and geospatial packages
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
    && rm -rf /var/lib/apt/lists/*


# 3. Install Quarto CLI (latest stable release)
RUN wget -qO- https://quarto.org/download/latest/quarto-linux-amd64.deb > quarto.deb \
    && dpkg -i quarto.deb || apt-get -fy install \
    && rm quarto.deb

# 4. Install latest CRAN R packages
RUN install2.r --error --skipinstalled \
    data.table magrittr dplyr tidyr purrr splines sp sf units oce

# 5. Install latest R packages from CRAN and GitHub
RUN Rscript -e "install.packages(c('ggplot2','sp', 'TMB', 'splines', 'purrr', 'data.table', 'magrittr', 'ggthemes', 'rmdformats', 'oce', 'sf', 'units', 'sdmTMB', 'kableExtra','GGally', 'rmarkdown', 'viridis', 'dplyr', 'cowplot', 'parallel', 'tidyr', 'patchwork', 'reshape2', 'iterators', 'remotes', 'tidyverse'), repos='https://cloud.r-project.org/')"
RUN Rscript -e "remotes::install_github('james-thorson/VAST@main', INSTALL_opts='--no-staged-install')"
RUN Rscript -e "remotes::install_github('james-thorson/FishStatsUtils@main', INSTALL_opts='--no-staged-install')"
RUN Rscript -e "remotes::install_github('vast-lib/tinyVAST', dependencies = TRUE)"
RUN Rscript -e "install.packages('INLA', repos=c(getOption('repos'), INLA='https://inla.r-inla-download.org/R/stable'), dep=TRUE)"



# 6. Set working directory
WORKDIR /workspace

# 7. (Optional) Expose a port for apps or servers if needed
EXPOSE 8080

# 8. Set default entrypoint
CMD ["bash"]
