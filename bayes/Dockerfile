FROM rocker/r-ver:4.5.1

# 1. Disable interactive prompts and set Noumea timezone
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Pacific/Noumea

# 2. Install system libraries needed for R package building
RUN apt-get update && apt-get install -y --no-install-recommends \
    gfortran \
    liblapack-dev \
    libblas-dev \
    libcurl4-openssl-dev \
    libxml2-dev \
    libssl-dev \
    pkg-config \
    wget \
    git \
    libfontconfig1-dev \
    libfreetype6-dev \
    libpng-dev \
    libtiff5-dev \
    libjpeg-dev \
    libharfbuzz-dev \
    libfribidi-dev \
  && rm -rf /var/lib/apt/lists/*

# 3. Install R packages in stages to handle dependencies properly
# 3a. Install basic dependencies first
RUN R -e "install.packages(c('miniUI', 'pkgdown'), repos='https://cloud.r-project.org', dependencies=TRUE)"

# 3b. Install font/graphics related packages
RUN R -e "install.packages(c('systemfonts', 'textshaping', 'ragg'), repos='https://cloud.r-project.org', dependencies=TRUE)"

# 3c. Install main packages
RUN R -e "install.packages(c('devtools','remotes','ggplot2','patchwork','stringr','progressr'), repos='https://cloud.r-project.org', dependencies=TRUE)" \
 && R -e "install.packages(c('here','dplyr','bayesplot','posterior'), dependencies=TRUE, repos='https://cloud.r-project.org')"

# 3d. Install cmdstanr and GitHub packages
RUN R -e "install.packages('cmdstanr', repos=c('https://stan-dev.r-universe.dev', getOption('repos')))" \ 
 && R -e "devtools::install_github('hyunjimoon/SBC')"

# 4. Set working directory for your model files
WORKDIR /workspace

# 5. Expose a port if you plan to run any web interfaces
EXPOSE 8080

# 6. Default entrypoint
CMD ["bash"]

