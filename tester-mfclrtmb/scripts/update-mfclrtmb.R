options(warn = 1)

repo_owner <- "PacificCommunity"
repo_name <- "ofp-sam-mfclrtmb"
repo_slug <- sprintf("%s/%s", repo_owner, repo_name)
package_name <- "mfclrtmb"
missing_token_status <- 42L
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
  log_message("Refreshing bundled %s from %s.", package_name, repo_slug)
} else {
  log_message("%s is not installed; installing latest from %s.", package_name, repo_slug)
}

remotes::install_github(repo_slug, auth_token = token, upgrade = "never", force = TRUE)
