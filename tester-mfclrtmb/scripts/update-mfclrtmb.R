options(warn = 1)

repo_owner <- "PacificCommunity"
repo_name <- "ofp-sam-mfclrtmb"
repo_slug <- sprintf("%s/%s", repo_owner, repo_name)
package_name <- "mfclrtmb"
missing_token_status <- 42L
missing_library_status <- 43L
default_runtime_library <- "/home/rstudio/R/site-library"
token <- Sys.getenv("GITHUB_PAT", "")

if (!nzchar(token)) {
  token <- Sys.getenv("GIT_PAT", "")
}

log_message <- function(...) {
  message("[mfclrtmb-update] ", sprintf(...))
}

is_package_installed <- function() {
  requireNamespace(package_name, quietly = TRUE)
}

installed_package_version <- function() {
  as.character(utils::packageVersion(package_name))
}

resolve_runtime_library <- function() {
  configured_library <- Sys.getenv("R_LIBS_USER", "")

  if (!nzchar(configured_library)) {
    configured_library <- default_runtime_library
  }

  strsplit(configured_library, .Platform$path.sep, fixed = TRUE)[[1]][1]
}

ensure_runtime_library <- function(library_path) {
  dir.create(library_path, recursive = TRUE, showWarnings = FALSE)
  file.access(library_path, 2) == 0
}

if (!nzchar(token)) {
  if (is_package_installed()) {
    log_message("GITHUB_PAT or GIT_PAT is not set; keeping bundled %s installation.", package_name)
    quit(save = "no", status = 0)
  }

  log_message(
    "GITHUB_PAT or GIT_PAT is not set and %s is not installed. Provide a token or use an image with %s preinstalled.",
    package_name,
    package_name
  )
  quit(save = "no", status = missing_token_status)
}

if (is_package_installed()) {
  log_message(
    "Checking installed %s %s against %s; runtime install will be skipped when already current.",
    package_name,
    installed_package_version(),
    repo_slug
  )
} else {
  log_message("%s is not installed; installing latest from %s.", package_name, repo_slug)
}

runtime_library <- resolve_runtime_library()

if (!ensure_runtime_library(runtime_library)) {
  if (is_package_installed()) {
    log_message(
      "Runtime library %s is not writable; keeping bundled %s installation.",
      runtime_library,
      package_name
    )
    quit(save = "no", status = 0)
  }

  log_message(
    "Runtime library %s is not writable and %s is not installed. Set R_LIBS_USER to a writable path or use an image with %s preinstalled.",
    runtime_library,
    package_name,
    package_name
  )
  quit(save = "no", status = missing_library_status)
}

.libPaths(unique(c(runtime_library, .libPaths())))
log_message("Installing runtime update into %s.", runtime_library)

remotes::install_github(
  repo_slug,
  auth_token = token,
  lib = runtime_library,
  upgrade = "never",
  force = FALSE
)
