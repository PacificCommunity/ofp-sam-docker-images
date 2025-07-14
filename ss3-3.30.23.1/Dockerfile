FROM rocker/r-ver:4.5.0

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
  && rm -rf /var/lib/apt/lists/*

# 3. Download and install optimized Stock Synthesis 3 binary v3.30.23.1
RUN wget -q -O ss3_opt_linux \
    https://github.com/nmfs-ost/ss3-source-code/releases/download/v3.30.23.1/ss3_opt_linux \
  && chmod +x ss3_opt_linux \
  && mv ss3_opt_linux /usr/local/bin/ss3

# 4. Install R packages from CRAN and GitHub
RUN R -e "install.packages(c('devtools','remotes','pak'), repos='https://cloud.r-project.org')" \
 && R -e "install.packages(c('here','dplyr'), dependencies=TRUE, repos='https://cloud.r-project.org')" \
 && R -e "pak::pkg_install('r4ss/r4ss')"

# 5. Set working directory for your model files
WORKDIR /workspace

# 6. Expose a port if you plan to run any web interfaces
EXPOSE 8080

# 7. Default entrypoint
CMD ["bash"]
