FROM ghcr.io/pacificcommunity/bayes:v1.5@sha256:bf5ddfb295ca0828d9502e48dc85757f7ef1850a06e147fbb23d1e079050d8e8

ARG QUARTO_VERSION=1.9.38
ARG QUARTO_SHA256=ea8c897368791ad9f200010c087ea3111b2e556b12a960487dd4e216902aa102

# Preserve the complete R/CmdStan environment from bayes:v1.5. Version 1.6
# adds document-rendering tools only; it does not reinstall or update R packages.
RUN mkdir -p /usr/local/share/bayes-image \
 && Rscript -e "ip <- installed.packages(); ip <- ip[order(ip[, 'Package'], ip[, 'LibPath']), c('Package', 'Version', 'LibPath'), drop = FALSE]; write.table(ip, '/usr/local/share/bayes-image/r-packages-v1.5.tsv', sep = '\t', row.names = FALSE, quote = FALSE)" \
 && dpkg-query -W -f='${binary:Package}\t${Version}\n' | LC_ALL=C sort > /usr/local/share/bayes-image/debian-packages-v1.5.tsv

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Pacific/Noumea

# Add only the system tools needed to render manuscripts, supplements,
# reviewer responses, and latexdiff PDFs. --no-upgrade prevents changes to
# packages already installed in the immutable v1.5 base image.
RUN apt-get update \
 && apt-get install -y --no-install-recommends --no-upgrade \
      pandoc \
      latexmk \
      latexdiff \
      lmodern \
      texlive-latex-base \
      texlive-latex-recommended \
      texlive-latex-extra \
      texlive-fonts-recommended \
      texlive-plain-generic \
      ghostscript \
      poppler-utils \
 && rm -rf /var/lib/apt/lists/*

# Install the standalone Quarto CLI without using R package installation.
RUN mkdir -p "/opt/quarto/${QUARTO_VERSION}" \
 && download_ok=0 \
 && for attempt in 1 2 3 4 5; do \
      rm -f /tmp/quarto.tar.gz; \
      wget --tries=3 --timeout=60 \
        "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.tar.gz" \
        -O /tmp/quarto.tar.gz \
      && echo "${QUARTO_SHA256}  /tmp/quarto.tar.gz" | sha256sum --check \
      && download_ok=1 \
      && break; \
      echo "Quarto download attempt ${attempt} failed; retrying" >&2; \
    done \
 && test "${download_ok}" = 1 \
 && tar -xzf /tmp/quarto.tar.gz -C "/opt/quarto/${QUARTO_VERSION}" --strip-components=1 \
 && ln -s "/opt/quarto/${QUARTO_VERSION}/bin/quarto" /usr/local/bin/quarto \
 && rm -f /tmp/quarto.tar.gz

# Verify both the rendering toolchain and exact preservation of the v1.5 R
# package set. The latter intentionally fails the image build if any R
# package or version changes.
RUN pandoc --version \
 && quarto --version \
 && pdflatex --version \
 && latexmk -v \
 && latexdiff --version 2>&1 | grep -q LATEXDIFF \
 && pdfinfo -v \
 && kpsewhich natbib.sty \
 && kpsewhich microtype.sty \
 && kpsewhich makecell.sty \
 && kpsewhich booktabs.sty \
 && Rscript -e "ip <- installed.packages(); ip <- ip[order(ip[, 'Package'], ip[, 'LibPath']), c('Package', 'Version', 'LibPath'), drop = FALSE]; current <- tempfile(); write.table(ip, current, sep = '\t', row.names = FALSE, quote = FALSE); stopifnot(identical(readLines('/usr/local/share/bayes-image/r-packages-v1.5.tsv'), readLines(current)))" \
 && dpkg-query -W -f='${binary:Package}\t${Version}\n' | LC_ALL=C sort > /tmp/debian-packages-current.tsv \
 && LC_ALL=C comm -23 /usr/local/share/bayes-image/debian-packages-v1.5.tsv /tmp/debian-packages-current.tsv > /tmp/debian-packages-changed.tsv \
 && test ! -s /tmp/debian-packages-changed.tsv \
 && rm -f /tmp/debian-packages-current.tsv /tmp/debian-packages-changed.tsv

WORKDIR /workspace

EXPOSE 8080

CMD ["bash"]
