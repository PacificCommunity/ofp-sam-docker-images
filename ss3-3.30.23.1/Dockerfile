FROM ubuntu:22.04

# Disable interactive prompts and set Noumea timezone
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Pacific/Noumea

# 1. Add CRAN key and repository for R 4.5.0
RUN apt-get update && apt-get install -y --no-install-recommends \
      wget \
      software-properties-common \
      dirmngr \
  && wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc \
       | tee /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc \
  && add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu jammy-cran40/" \
  && rm -rf /var/lib/apt/lists/*

# 2. Install system libraries and R 4.5.0
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \        # compilers and build tools
      gfortran \               # Fortran compiler needed by SS3
      liblapack-dev \          # Linear algebra library
      libblas-dev \            # Basic linear algebra library
      libcurl4-openssl-dev \   # libcurl for R packages
      libxml2-dev \            # libxml2 for XML support in R
      libssl-dev \             # OpenSSL headers for HTTPS
      pkg-config \             # pkg-config for library detection
      r-base=4.5.0-* \         # R interpreter (version 4.5.0)
      r-base-dev=4.5.0-* \     # R development headers
      git \                    # Version control
  && rm -rf /var/lib/apt/lists/*

# 3. Download and install the optimized SS3 binary
RUN wget -q -O ss3_opt_linux \
      https://github.com/nmfs-ost/ss3-source-code/releases/download/v3.30.23.1/ss3_opt_linux \
  && chmod +x ss3_opt_linux \
  && mv ss3_opt_linux /usr/local/bin/ss3

# 4. Install R packages required for SS3 workflows
RUN R -e "install.packages(c('devtools','remotes'), repos='https://cloud.r-project.org')" \
 && R -e "install.packages(c('r4ss','here','dplyr'), dependencies=TRUE, repos='https://cloud.r-project.org')"

# 5. Set working directory for model files
WORKDIR /workspace

# 6. Expose port for any potential web interface (optional)
EXPOSE 8080

# 7. Default command: start a Bash shell
CMD ["bash"]
