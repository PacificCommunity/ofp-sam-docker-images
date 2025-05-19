# Use R 4.2.3 base image for legacy spatial/statistical package compatibility
FROM rocker/r-ver:4.2.3

# Install system dependencies and development libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        git \
        curl \
        libcurl4-openssl-dev \
        libssl-dev \
        libxml2-dev \
        libgdal-dev \
        libgeos-dev \
        libproj-dev \
        libudunits2-dev \
        libfontconfig1-dev \
        libharfbuzz-dev \
        libfribidi-dev \
        pkg-config \
        texlive-latex-extra \
        pandoc \
        pandoc-citeproc \
        librsvg2-bin \
        ghostscript \
        inkscape \
        ca-certificates \
        gdal-bin && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Docker CLI (client only, no daemon)
RUN curl -fsSL https://get.docker.com | sh

# Install radian for a modern R console experience
RUN pip3 install -U radian

# Set default CRAN repository for R
RUN mkdir -p /etc/R && \
    echo 'options(repos = c(CRAN = \"https://cloud.r-project.org\"))' >> /etc/R/Rprofile.site

# Install devtools package (for install_github)
RUN R -e "install.packages('devtools')"

# Install Bioconductor dependencies required for INLA
RUN R -e "if (!requireNamespace('BiocManager', quietly=TRUE)) install.packages('BiocManager')"
RUN R -e "BiocManager::install(c('graph', 'Rgraphviz'), ask=FALSE, update=FALSE)"

# Install fmesher from CRAN (required for INLA and VAST)
RUN R -e "install.packages('fmesher')"

# Install legacy spatial/statistical dependencies from CRAN Archive
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/sp/sp_1.6-1.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/raster/raster_3.5-21.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/rgdal/rgdal_1.6-7.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/rgeos/rgeos_0.6-4.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/maptools/maptools_1.1-8.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/plotrix/plotrix_3.8-2.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/deldir/deldir_1.0-6.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/mixtools/mixtools_1.2.0.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/shape/shape_1.4.6.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/MatrixModels/MatrixModels_0.5-1.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/pander/pander_0.6.5.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/corpcor/corpcor_1.6.10.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/ThorsonUtilities/ThorsonUtilities_1.0.1.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/TMBhelper/TMBhelper_1.4.2.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/RANN/RANN_2.6.1.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/formatR/formatR_1.14.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/rnaturalearth/rnaturalearth_0.1.0.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/rnaturalearthdata/rnaturalearthdata_0.1.0.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/splancs/splancs_2.01-43.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/DHARMa/DHARMa_0.4.6.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/effects/effects_4.2-2.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/SpatialDeltaGLMM/SpatialDeltaGLMM_1.0.7.tar.gz', repos=NULL, type='source')"

# Install RandomFields and related dependencies
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/RandomFields/RandomFields_3.3.8.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/RandomFieldsUtils/RandomFieldsUtils_1.1.0.tar.gz', repos=NULL, type='source')"
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/plotKML/plotKML_0.5-9.tar.gz', repos=NULL, type='source')"

# Install INLA (22.05.07) for VAST 3.7.1 compatibility (source)
RUN R -e "install.packages('https://inla.r-inla-download.org/R/stable/src/contrib/INLA_22.05.07.tar.gz', repos=NULL, type='source')"

# Install core spatial and statistical R packages
RUN R -e "install.packages(c('TMB', 'RcppArmadillo', 'Matrix', 'sf', 'terra', 'stars', 'ggplot2', 'dplyr', 'tidyr', 'data.table', 'magrittr', 'ggthemes'))"

# Install FishStatsUtils 2.9.1 using devtools
RUN R -e "devtools::install_github('James-Thorson-NOAA/FishStatsUtils@2.9.1', dependencies = FALSE)"

# Install VAST 3.7.1 using devtools
RUN R -e "devtools::install_github('James-Thorson-NOAA/VAST@3.7.1', dependencies = FALSE)"

# Install additional utility package for VAST analyses
RUN R -e "devtools::install_github('PacificCommunity/ofp-sam-vast-utils', dependencies = FALSE)"

# Set working directory for user projects
WORKDIR /workspace

# Set permissions for the workspace directory
RUN chmod -R 777 /workspace

# Create a non-root user for security best practices
RUN useradd -m -u 1000 -U analyst
USER analyst