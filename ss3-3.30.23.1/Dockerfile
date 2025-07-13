FROM ubuntu:22.04

# Avoid interactive prompts and set Noumea timezone
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Pacific/Noumea

# 1. Install system dependencies (including libraries required by dplyr and others)
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    gfortran \
    liblapack-dev \
    libblas-dev \
    libcurl4-openssl-dev \      # for curl (dplyr dependency)
    libxml2-dev \               # for xml2 (here may suggest rprojroot)
    libssl-dev \                # for openssl
    pkg-config \                # helper for configuration
    r-base \
    r-base-dev \
    git \
  && rm -rf /var/lib/apt/lists/*

# 2. Download and install optimized SS3 binary
RUN wget -q -O ss3_opt_linux \
    https://github.com/nmfs-ost/ss3-source-code/releases/download/v3.30.23.1/ss3_opt_linux \
  && chmod +x ss3_opt_linux \
  && mv ss3_opt_linux /usr/local/bin/ss3

# 3. Install R packages from CRAN
RUN R -e "install.packages(c('devtools','remotes'), repos='https://cloud.r-project.org/')" \
 && R -e "install.packages(c('r4ss','here','dplyr'), dependencies=TRUE, repos='https://cloud.r-project.org/')"

# 4. Set working directory for model files
WORKDIR /workspace

# 5. Expose port for potential web interfaces
EXPOSE 8080

# Default entrypoint
CMD ["bash"]
