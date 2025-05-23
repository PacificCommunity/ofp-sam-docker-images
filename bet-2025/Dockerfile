# Use the rocker/rstudio base image
FROM rocker/rstudio:4.3.1

# Install required dependencies including OpenSSH client
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    lsb-release \
    libclang-dev \
    libcurl4-openssl-dev \
    openssh-client \
    && apt-get clean && rm -rf /var/lib/apt/lists/*


# Install docker-compose (pinned to version 2.23.0)
RUN curl -L "https://github.com/docker/compose/releases/download/2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# Install required R packages
RUN Rscript -e "install.packages(c('ggplot2', 'dplyr', 'cowplot', 'viridis', 'parallel', 'tidyr', 'patchwork', 'reshape2', 'iterators', 'remotes'), repos='https://cloud.r-project.org/')"
RUN Rscript -e "install.packages('FLCore', repos='http://flr-project.org/R')"
RUN Rscript -e "remotes::install_github('PacificCommunity/ofp-sam-flr4mfcl')"
RUN Rscript -e "remotes::install_github('PacificCommunity/ofp-sam-CondorBox')"

# Ensure correct permissions for RStudio Server
RUN chmod -R 777 /var/lib/rstudio-server && chmod -R 777 /home/rstudio

# Enable GitHub Copilot for RStudio (if applicable)
RUN echo "copilot-enabled=1" >> /etc/rstudio/rsession.conf



