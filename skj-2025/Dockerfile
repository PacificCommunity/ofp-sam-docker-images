# Use the rocker/rstudio base image
FROM rocker/rstudio:4.3.1

# Install required dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    lsb-release \
    libclang-dev \
    libcurl4-openssl-dev \
    libxml2-dev \
    texlive-xetex \
    texlive-latex-extra \
    texlive-fonts-recommended \
    pandoc \
    make \
    openssh-client \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install docker-compose (pinned to version 2.23.0)
RUN curl -L "https://github.com/docker/compose/releases/download/2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# Install required R packages
RUN Rscript -e "install.packages(c('ggplot2', 'rmdformats', 'kableExtra','GGally', 'rmarkdown', 'viridis', 'dplyr', 'cowplot', 'parallel', 'tidyr', 'patchwork', 'reshape2', 'iterators', 'remotes', 'tidyverse'), repos='https://cloud.r-project.org/')"
RUN Rscript -e "install.packages('FLCore', repos='http://flr-project.org/R')"
RUN Rscript -e "remotes::install_github('PacificCommunity/ofp-sam-flr4mfcl')"
RUN Rscript -e "remotes::install_github('PacificCommunity/ofp-sam-CondorBox')"

# Ensure correct permissions for RStudio Server
RUN chmod -R 777 /var/lib/rstudio-server && chmod -R 777 /home/rstudio

# Enable GitHub Copilot for RStudio (if applicable)
RUN echo "copilot-enabled=1" >> /etc/rstudio/rsession.conf

# Create /home/mfcl directory and copy mfclo64 into it
RUN mkdir -p /home/mfcl
COPY mfclo64 /home/mfcl/mfclo64

# Ensure mfclo64 has execution permissions
RUN chmod +x /home/mfcl/mfclo64


