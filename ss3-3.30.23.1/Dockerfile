FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive TZ=Pacific/Noumea

# 1. System deps required for R-build
RUN apt-get update && apt-get install -y --no-install-recommends \
     build-essential \
     gfortran \
     libreadline-dev \
     libx11-dev \
     libxt-dev \
     libpng-dev \
     libjpeg-dev \
     libcairo2-dev \
     libbz2-dev \
     liblzma-dev \
     libpcre2-dev \
     libcurl4-openssl-dev \
     libxml2-dev \
     libssl-dev \
     pkg-config \
     wget \
     git \
  && rm -rf /var/lib/apt/lists/*

# 2. Download and compile R 4.5.0
RUN wget -qO R-4.5.0.tar.gz https://cran.r-project.org/src/base/R-4/R-4.5.0.tar.gz \
  && tar -xf R-4.5.0.tar.gz \
  && cd R-4.5.0 \
  && ./configure --enable-R-shlib --with-blas --with-lapack \
  && make -j$(nproc) \
  && make install \
  && cd .. \
  && rm -rf R-4.5.0 R-4.5.0.tar.gz

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
