options(warn = 1)

repo_owner <- "PacificCommunity"
repo_name <- "ofp-sam-mfclrtmb"
repo_slug <- sprintf("%s/%s", repo_owner, repo_name)
token <- Sys.getenv("GITHUB_PAT", "")

log_message <- function(...) {
  message("[mfclrtmb-update] ", sprintf(...))
}

if (!nzchar(token)) {
  log_message("GITHUB_PAT is not set; skipping %s update check.", repo_slug)
  quit(save = "no", status = 0)
}

github_get <- function(path) {
  url <- sprintf("https://api.github.com%s", path)
  response <- curl::curl_fetch_memory(
    url,
    handle = curl::new_handle(
      httpheader = c(
        Authorization = paste("Bearer", token),
        Accept = "application/vnd.github+json",
        `User-Agent` = "tester-mfclrtmb-updater"
      )
    )
  )

  if (response$status_code >= 300) {
    stop(sprintf("GitHub API request failed (%s): %s", response$status_code, url))
  }

  jsonlite::fromJSON(rawToChar(response$content))
}

find_installed_remote <- function() {
  db <- as.data.frame(installed.packages(fields = c(
    "Package", "LibPath", "RemoteType", "RemoteHost",
    "RemoteRepo", "RemoteUsername", "RemoteSha"
  )), stringsAsFactors = FALSE)

  matches <- db[
    db$RemoteType == "github" &
      db$RemoteUsername == repo_owner &
      db$RemoteRepo == repo_name,
    ,
    drop = FALSE
  ]

  if (nrow(matches) == 0) {
    return(NULL)
  }

  matches[1, , drop = FALSE]
}

repo_info <- github_get(sprintf("/repos/%s", repo_slug))
default_branch <- repo_info$default_branch
commit_info <- github_get(sprintf("/repos/%s/commits/%s", repo_slug, default_branch))
latest_sha <- commit_info$sha

installed_remote <- find_installed_remote()

if (is.null(installed_remote)) {
  log_message("Package from %s is not installed; installing latest from %s (%s).",
              repo_slug, default_branch, substr(latest_sha, 1, 7))
  remotes::install_github(repo_slug, auth_token = token, upgrade = "never")
  quit(save = "no", status = 0)
}

installed_sha <- installed_remote$RemoteSha[[1]]
installed_package <- installed_remote$Package[[1]]
installed_sha_label <- if (nzchar(installed_sha)) substr(installed_sha, 1, 7) else "unknown"

if (identical(installed_sha, latest_sha)) {
  log_message("%s is already up to date at %s.", installed_package, substr(latest_sha, 1, 7))
  quit(save = "no", status = 0)
}

log_message(
  "Updating %s from %s to %s.",
  installed_package,
  installed_sha_label,
  substr(latest_sha, 1, 7)
)

remotes::install_github(repo_slug, auth_token = token, upgrade = "never", force = TRUE)
