FROM ubuntu:22.04

# Avoid interactive prompts and set Noumea timezone
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Pacific/Noumea

# Update and install required packages
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    gfortran \
    liblapack-dev \
    libblas-dev \
    r-base \
    r-base-dev \
    git \
  && rm -rf /var/lib/apt/lists/*

# Download only the optimized SS3 v3.30.23.1 binary
RUN wget -q -O ss3_opt_linux \
    https://github.com/nmfs-ost/ss3-source-code/releases/download/v3.30.23.1/ss3_opt_linux \
  && chmod +x ss3_opt_linux \
  && mv ss3_opt_linux /usr/local/bin/ss3

# Install R package for SS3 interaction
RUN R -e "install.packages(c('devtools','remotes'), repos='https://cran.rstudio.com/')" \
 && R -e "remotes::install_github('r4ss/r4ss')"

# Set working directory for models
WORKDIR /workspace

# Expose port for potential web interfaces
EXPOSE 8080

# Default entrypoint
CMD ["bash"]
