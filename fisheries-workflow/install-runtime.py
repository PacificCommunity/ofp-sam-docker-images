"""Install checked R source packages and verify the complete execution image."""
import hashlib
import json
from pathlib import Path
import platform
import shutil
import sqlite3
import subprocess
import tempfile
import urllib.request

ROOT = Path(__file__).resolve().parent
lock = json.loads((ROOT / 'packages.lock.json').read_text())
with tempfile.TemporaryDirectory() as directory:
    for package in lock['packages']:
        archive = Path(directory, package['filename'])
        with urllib.request.urlopen(package['url'], timeout=120) as response:
            archive.write_bytes(response.read())
        assert hashlib.sha256(archive.read_bytes()).hexdigest() == package['sha256'], package['name']
        subprocess.run(['R', 'CMD', 'INSTALL', '--no-multiarch', str(archive)], check=True)
    subprocess.run(['Rscript', '--vanilla', '-e', '''
library(RTMB)
stopifnot(as.character(getRversion()) == "4.6.0")
stopifnot(as.character(packageVersion("RTMB")) == "2.0")
stopifnot(as.character(packageVersion("TMB")) == "1.9.25")
objective <- function(p) (p$mu - 2)^2
ad <- MakeADFun(objective, list(mu = 0), silent = TRUE)
fit <- nlminb(ad$par, ad$fn, ad$gr)
stopifnot(fit$convergence == 0, abs(fit$par[[1]] - 2) < 1e-8)
'''], check=True)
    quarto = subprocess.check_output(['quarto', '--version'], text=True).strip()
    assert quarto == '1.9.37', quarto
    report = Path(directory, 'smoke.qmd')
    shutil.copyfile(ROOT / 'smoke.qmd', report)
    subprocess.run(['quarto', 'render', str(report), '--to', 'html', '--quiet'], check=True)
    rendered = report.with_suffix('.html').read_text()
    assert 'RTMB fit checked' in rendered and 'Container report checked' in rendered
    observed = json.loads(subprocess.check_output(['Rscript', '--vanilla', '-e', '''
cat(jsonlite::toJSON(list(r = as.character(getRversion()),
  packages = as.list(vapply(c("RTMB", "TMB", "jsonlite", "knitr", "rmarkdown", "Matrix", "MASS"),
    function(x) as.character(packageVersion(x)), ""))), auto_unbox = TRUE))
'''], text=True))
    observed.update(python=platform.python_version(), sqlite=sqlite3.sqlite_version,
                    quarto=quarto, platform=platform.platform())
    (ROOT / 'runtime.json').write_text(json.dumps(observed, indent=2) + '\n')
    print(json.dumps(observed, sort_keys=True))
