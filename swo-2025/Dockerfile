# Base image using rocker/rstudio
FROM rocker/rstudio:4.2.3

# Install system dependencies (Python3 and pip)
RUN apt-get update && apt-get install -y \
    python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Radian - modern R console
RUN pip3 install -U radian
# Base image
FROM rocker/rstudio:4.2.3

# Install system dependencies: Python3, pip, Docker, Git, pandoc, and other libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        git \
        ca-certificates \
        curl \
        gnupg \
        lsb-release \
        libclang-dev \
        libcurl4-openssl-dev \
        openssh-client \
        libgdal-dev \
        libgeos-dev \
        libproj-dev \
        libudunits2-dev \
        libssl-dev \
        libxml2-dev \
        apt-transport-https \
        software-properties-common \
        pandoc \
        pandoc-citeproc \
        texlive-latex-extra \
        lmodern \
        perl && \
    # Install Docker Engine (see official Docker instructions for Ubuntu)
    install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc && \
    chmod a+r /etc/apt/keyrings/docker.asc && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        docker-ce \
        docker-ce-cli \
        containerd.io \
        docker-buildx-plugin \
        docker-compose-plugin && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Optionally, get latest pandoc binary (if you want a newer version than apt provides)
# RUN curl -L https://github.com/jgm/pandoc/releases/download/3.1.13.2/pandoc-3.1.13.2-1-amd64.deb -o /tmp/pandoc.deb && \
#     dpkg -i /tmp/pandoc.deb && rm /tmp/pandoc.deb

# Install radian (modern R console)
RUN pip3 install -U radian

# Install R Language Server for VS Code integration
RUN Rscript -e "install.packages('languageserver', repos='https://cloud.r-project.org/')"

# Install required R packages from CRAN
RUN Rscript -e "install.packages(c('ggplot2', 'GGally', 'viridis', 'dplyr', 'cowplot', 'parallel', 'tidyr', 'patchwork', 'reshape2', 'iterators', 'remotes', 'data.table', 'magrittr', 'sp', 'raster', 'ggthemes', 'splines', 'rgdal', 'rgeos', 'sf', 'terra'), repos='https://cloud.r-project.org/')"

# Install FLCore and other FLR-related packages
RUN Rscript -e "install.packages('FLCore', repos='http://flr-project.org/R')"
RUN Rscript -e "remotes::install_github('PacificCommunity/ofp-sam-flr4mfcl')"
RUN Rscript -e "remotes::install_github('PacificCommunity/ofp-sam-CondorBox')"

# Install specific versions of VAST and FishStatsUtils from GitHub
RUN Rscript -e "remotes::install_github('James-Thorson-NOAA/VAST@3.7.1')"
RUN Rscript -e "remotes::install_github('James-Thorson-NOAA/FishStatsUtils@2.9.1')"

# (Optional) Install ofp.sam.vast.utils if needed
RUN Rscript -e "remotes::install_github('PacificCommunity/ofp-sam-vast-utils')"

# Install docker-compose (standalone, pinned to version 2.23.0)
RUN curl -L "https://github.com/docker/compose/releases/download/2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# Set permissions for RStudio Server and VS Code integration
RUN chmod -R 777 /var/lib/rstudio-server && chmod -R 777 /home/rstudio && chown -R rstudio:rstudio /home/rstudio

# Enable GitHub Copilot for RStudio (if applicable)
RUN echo "copilot-enabled=1" >> /etc/rstudio/rsession.conf

