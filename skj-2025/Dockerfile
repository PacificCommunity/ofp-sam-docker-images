# Use the rocker/rstudio base image
FROM rocker/rstudio:4.3.1

# Switch to root user to install necessary packages
USER root

# Install required dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    lsb-release

# Install Docker Engine and CLI using Docker's official convenience script
RUN curl -fsSL https://get.docker.com -o get-docker.sh && \
    sh get-docker.sh && \
    rm get-docker.sh

# Install docker-compose (pinned to version 2.23.0)
RUN curl -L "https://github.com/docker/compose/releases/download/2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# Install required R packages
RUN Rscript -e "install.packages(c('ggplot2', 'dplyr', 'GGally', 'cowplot', 'parallel', 'tidyr', 'patchwork', 'reshape2', 'iterators', 'remotes'), repos='https://cloud.r-project.org/')"
RUN Rscript -e "install.packages('FLCore', repos='http://flr-project.org/R')"
RUN Rscript -e "remotes::install_github('PacificCommunity/ofp-sam-flr4mfcl')"
RUN Rscript -e "remotes::install_github('PacificCommunity/ofp-sam-CondorBox')"

# Clean up unnecessary cache files
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Enable GitHub Copilot for RStudio (if applicable)
RUN echo "copilot-enabled=1" >> /etc/rstudio/rsession.conf

# Revert to the original default user (usually 'rstudio')
USER rstudio

# Expose the default port for RStudio Server
EXPOSE 8787


