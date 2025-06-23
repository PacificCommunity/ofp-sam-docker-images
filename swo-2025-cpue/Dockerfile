###############################################################################
# HTCondor-Safe Docker Image: Ubuntu 22.04 + R 4.1.2 + VAST 3.7.1
###############################################################################
FROM ubuntu:22.04

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Define build arguments
ARG R_VERSION=4.1.2
ARG MAKE_FLAGS=-j4

###############################################################################
# 1. Install system build dependencies and libraries
###############################################################################
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gfortran rsync \
    libreadline-dev libbz2-dev liblzma-dev libpcre2-dev zlib1g-dev \
    libcurl4-openssl-dev libssl-dev libxml2-dev libicu-dev \
    libpng-dev libjpeg-dev libcairo2-dev libtiff5-dev libfreetype6-dev \
    libxt-dev libx11-dev libblas-dev liblapack-dev \
    libgdal-dev libgeos-dev libproj-dev libudunits2-dev libnetcdf-dev \
    libfontconfig1-dev libharfbuzz-dev libfribidi-dev \
    git curl wget sudo openssh-server bash-completion locales tzdata \
    python3-pip python3-dev python3-setuptools python3-wheel python3-venv \
    texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra \
    texlive-latex-recommended texlive-base texlive-binaries lmodern \
    pandoc librsvg2-bin ghostscript inkscape gdal-bin libglu1-mesa-dev \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

###############################################################################
# 2. Compile and install R 4.1.2 from source with recommended packages
###############################################################################
WORKDIR /tmp
RUN curl -fsSL https://cran.r-project.org/src/base/R-4/R-${R_VERSION}.tar.gz -o R-${R_VERSION}.tar.gz \
  && tar -xzf R-${R_VERSION}.tar.gz \
  && cd R-${R_VERSION} \
  && ./tools/rsync-recommended \
  && ./configure --prefix=/usr/local --enable-R-shlib \
       --with-blas --with-lapack --with-readline \
       --with-recommended-packages=yes --enable-memory-profiling \
       --enable-byte-compiled-packages --with-x --with-cairo \
       --with-libpng --with-jpeglib --with-libtiff \
  && make ${MAKE_FLAGS} && make install \
  && cd /tmp && rm -rf R-${R_VERSION}*

# Verify R and glibc versions
RUN echo "--- R Version ---" && R --version | head -1 \
  && echo "--- glibc Version ---" && ldd --version | head -1

###############################################################################
# 3. Set locale & timezone
###############################################################################
RUN locale-gen en_US.UTF-8 \
  && update-locale LANG=en_US.UTF-8 \
  && ln -fs /usr/share/zoneinfo/Pacific/Noumea /etc/localtime \
  && dpkg-reconfigure -f noninteractive tzdata
ENV LANG=en_US.UTF-8 TZ=Pacific/Noumea

###############################################################################
# 4. Install Docker CLI & radian console
###############################################################################
RUN curl -fsSL https://get.docker.com | sh \
  && pip3 install --no-cache-dir radian==0.6.4

###############################################################################
# 5. Configure R CRAN mirror and options
###############################################################################
RUN mkdir -p /etc/R /usr/local/lib/R/etc \
  && echo "local({r<-getOption('repos'); r['CRAN']<-'https://cloud.r-project.org'; options(repos=r)})" \
     > /etc/R/Rprofile.site \
  && cp /etc/R/Rprofile.site /usr/local/lib/R/etc/ \
  && echo "options(timeout=300, download.file.method='libcurl', Ncpus=4)" \
     >> /etc/R/Rprofile.site

###############################################################################
# 6. Install core development packages
###############################################################################
RUN R -e "install.packages(c('devtools','remotes'), dependencies=TRUE)"

# Install Bioconductor prereqs
RUN R -e "if (!requireNamespace('BiocManager', quietly=TRUE)) install.packages('BiocManager')" \
  && R -e "BiocManager::install(c('graph','Rgraphviz'), ask=FALSE, update=FALSE)"

###############################################################################
# 7. Install legacy spatial/statistical packages (exact archived versions)
###############################################################################
RUN R -e "install.packages(c( \
     'https://cran.r-project.org/src/contrib/Archive/sp/sp_1.4-5.tar.gz', \
     'https://cran.r-project.org/src/contrib/Archive/raster/raster_3.4-5.tar.gz', \
     'https://cran.r-project.org/src/contrib/Archive/rgdal/rgdal_1.5-23.tar.gz', \
     'https://cran.r-project.org/src/contrib/Archive/rgeos/rgeos_0.5-9.tar.gz', \
     'https://cran.r-project.org/src/contrib/Archive/maptools/maptools_1.1-8.tar.gz'), \
     repos=NULL, type='source')" \
  && R -e "install.packages(c('XML','spacetime','colorspace','plotrix','dismo','aqp', \
      'pixmap','plyr','colorRamps','scales','gstat','zoo','RColorBrewer','RSAGA','classInt'), \
      dependencies=TRUE)"

# Additional archived helpers
RUN R -e "install.packages(c( \
     'https://cran.r-project.org/src/contrib/Archive/plotKML/plotKML_0.5-9.tar.gz', \
     'https://cran.r-project.org/src/contrib/Archive/units/units_0.7-2.tar.gz', \
     'https://cran.r-project.org/src/contrib/Archive/RandomFieldsUtils/RandomFieldsUtils_0.5.3.tar.gz', \
     'https://cran.r-project.org/src/contrib/Archive/RandomFields/RandomFields_3.3.8.tar.gz', \
     'https://cran.r-project.org/src/contrib/Archive/TMBhelper/TMBhelper_1.4.2.tar.gz'), \
     repos=NULL, type='source')"

###############################################################################
# 8. Install INLA
###############################################################################
RUN R -e "install.packages('https://inla.r-inla-download.org/R/stable/src/contrib/INLA_22.05.07.tar.gz', \
    repos=NULL, type='source')"

###############################################################################
# 9. Modern spatial / tidyverse stack
###############################################################################
RUN R -e "install.packages(c('TMB','RcppArmadillo','Matrix','sf','terra','stars','ggplot2', \
      'dplyr','tidyr','data.table','magrittr','ggthemes','rmdformats','purrr','reshape2', \
      'cowplot','patchwork','kableExtra','viridis','tidyverse'), dependencies=TRUE)"

###############################################################################
# 10. Install VAST & FishStatsUtils from GitHub
###############################################################################
RUN R -e "remotes::install_github('James-Thorson-NOAA/FishStatsUtils@2.9.1', \
      dependencies=TRUE, upgrade='never', force=TRUE)" \
  && R -e "remotes::install_github('James-Thorson-NOAA/VAST@3.7.1', \
      dependencies=TRUE, upgrade='never', force=TRUE)" \
  && R -e "remotes::install_github('PacificCommunity/ofp-sam-vast-utils', dependencies=FALSE)"

###############################################################################
# 11. Oceanographic & additional packages
###############################################################################
RUN R -e "install.packages(c('gsw','testthat','knitr','rmarkdown','ncdf4'), \
      dependencies=TRUE)" \
  && R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/oce/oce_1.5-0.tar.gz', \
      repos=NULL, type='source')" \
  && R -e "install.packages(c('gstat','automap','geoR','fields'), dependencies=TRUE)"

###############################################################################
# 12. Quarto CLI for document rendering
###############################################################################
RUN curl -L https://github.com/quarto-dev/quarto-cli/releases/download/v1.2.335/quarto-1.2.335-linux-amd64.deb \
     -o quarto.deb \
  && dpkg -i quarto.deb || apt-get install -fy \
  && rm quarto.deb

###############################################################################
# 13. Create workspace and user for HTCondor
###############################################################################
RUN mkdir -p /workspace /usr/local/lib/R/site-library \
  && chmod -R 777 /workspace /usr/local/lib/R/site-library \
  && useradd -m -u 1000 -U -s /bin/bash analyst \
  && echo "analyst ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers \
  && echo 'analyst:analyst' | chpasswd \
  && mkdir -p /var/run/sshd

###############################################################################
# 14. Final verification
###############################################################################
RUN echo "=== Final Checks ===" \
  && R --version \
  && R -e "library(VAST); cat('VAST', packageVersion('VAST'), '\n')" \
  && R -e "library(FishStatsUtils); cat('FSU', packageVersion('FishStatsUtils'), '\n')" \
  && ldd --version | head -1

# Expose SSH and switch to non-root user
EXPOSE 22
USER analyst
WORKDIR /workspace
CMD ["/bin/bash"]
