options(warn = 1)

missing_token_status <- 42L
missing_library_status <- 43L
default_runtime_library <- "/home/rstudio/R/site-library"
default_state_dir <- "/home/rstudio/.cache/kflow-runtime-packages"
default_packages <- paste(
  "mfclrtmb=PacificCommunity/ofp-sam-mfclrtmb@main",
  "mfclkit=PacificCommunity/ofp-sam-mfclkit@main",
  "mfclshiny=PacificCommunity/mfclshiny@main",
  "KflowKit=kyuhank/KflowKit@main",
  sep = ","
)

log_message <- function(...) {
  message("[kflow-runtime-update] ", sprintf(...))
}

env_value <- function(name, default = "") {
  value <- Sys.getenv(name, unset = NA_character_)
  if (is.na(value) || !nzchar(value)) default else value
}

truthy <- function(value) {
  tolower(value) %in% c("1", "true", "yes", "y", "on", "always")
}

runtime_updates_enabled <- function() {
  value <- tolower(env_value("KFLOW_RUNTIME_UPDATE", "auto"))
  !value %in% c("0", "false", "no", "off", "never")
}

github_token <- function() {
  token <- env_value("GITHUB_PAT", "")
  if (!nzchar(token)) token <- env_value("GIT_PAT", "")
  token
}

resolve_runtime_library <- function() {
  configured <- env_value("KFLOW_RUNTIME_LIBRARY", "")
  if (!nzchar(configured)) configured <- env_value("R_LIBS_USER", "")
  if (!nzchar(configured)) configured <- default_runtime_library
  strsplit(configured, .Platform$path.sep, fixed = TRUE)[[1]][1]
}

ensure_runtime_library <- function(library_path) {
  dir.create(library_path, recursive = TRUE, showWarnings = FALSE)
  file.access(library_path, 2) == 0
}

package_installed <- function(package) {
  requireNamespace(package, quietly = TRUE)
}

installed_remote_sha <- function(package) {
  if (!package_installed(package)) return("")
  desc <- utils::packageDescription(package)
  value <- desc[["RemoteSha"]]
  if (is.null(value) || is.na(value)) "" else as.character(value)
}

parse_package_specs <- function(spec_text) {
  if (!nzchar(spec_text)) spec_text <- default_packages
  parts <- trimws(unlist(strsplit(spec_text, ",")))
  parts <- parts[nzchar(parts)]
  lapply(parts, function(part) {
    eq <- regexpr("=", part, fixed = TRUE)[1]
    if (eq < 2) {
      stop("Package spec must be package=owner/repo[@ref]: ", part, call. = FALSE)
    }
    package <- trimws(substr(part, 1, eq - 1))
    repo_ref <- trimws(substr(part, eq + 1, nchar(part)))
    ref <- "main"
    at <- regexpr("@", repo_ref, fixed = TRUE)[1]
    if (at > 0) {
      ref <- substr(repo_ref, at + 1, nchar(repo_ref))
      repo <- substr(repo_ref, 1, at - 1)
    } else {
      repo <- repo_ref
    }
    list(package = package, repo = repo, ref = ref)
  })
}

github_api <- function(path, token) {
  if (!requireNamespace("curl", quietly = TRUE)) {
    stop("curl is required for runtime package updates.", call. = FALSE)
  }
  handle <- curl::new_handle()
  curl::handle_setheaders(
    handle,
    Accept = "application/vnd.github+json",
    "X-GitHub-Api-Version" = "2022-11-28",
    "User-Agent" = "tuna-flow-runtime-updater"
  )
  if (nzchar(token)) {
    curl::handle_setheaders(handle, Authorization = paste("Bearer", token))
  }
  response <- tryCatch(
    curl::curl_fetch_memory(paste0("https://api.github.com", path), handle = handle),
    error = function(error) stop(conditionMessage(error), call. = FALSE)
  )
  status <- response$status_code
  if (status < 200 || status >= 300) {
    body <- rawToChar(response$content)
    stop(sprintf("GitHub API returned HTTP %s for %s\n%s", status, path, body), call. = FALSE)
  }
  rawToChar(response$content)
}

remote_sha <- function(repo, ref, token) {
  if (!requireNamespace("jsonlite", quietly = TRUE)) {
    stop("jsonlite is required for runtime package updates.", call. = FALSE)
  }
  path <- sprintf("/repos/%s/commits/%s", repo, utils::URLencode(ref, reserved = TRUE))
  json <- github_api(path, token)
  data <- jsonlite::fromJSON(json)
  as.character(data$sha)
}

state_path <- function(state_dir, package, repo, ref) {
  safe <- gsub("[^A-Za-z0-9_.-]+", "_", paste(package, repo, ref, sep = "__"))
  file.path(state_dir, paste0(safe, ".sha"))
}

should_check_remote <- function(state_file) {
  if (truthy(env_value("KFLOW_RUNTIME_FORCE_UPDATE", "false"))) return(TRUE)
  interval <- tolower(env_value("KFLOW_RUNTIME_UPDATE_INTERVAL_HOURS", "24"))
  if (interval %in% c("0", "always")) return(TRUE)
  if (interval %in% c("never", "off", "false", "no")) return(FALSE)
  if (!file.exists(state_file)) return(TRUE)
  hours <- suppressWarnings(as.numeric(interval))
  if (is.na(hours)) hours <- 24
  age <- as.numeric(difftime(Sys.time(), file.info(state_file)$mtime, units = "hours"))
  age >= hours
}

install_package <- function(spec, token, library_path, force = TRUE) {
  if (!requireNamespace("remotes", quietly = TRUE)) {
    stop("remotes is required to install GitHub packages.", call. = FALSE)
  }
  .libPaths(unique(c(library_path, .libPaths())))
  remotes::install_github(
    spec$repo,
    ref = spec$ref,
    auth_token = token,
    lib = library_path,
    upgrade = "never",
    force = force
  )
}

token <- github_token()
specs <- parse_package_specs(env_value("KFLOW_RUNTIME_PACKAGES", default_packages))
runtime_library <- resolve_runtime_library()
state_dir <- env_value("KFLOW_RUNTIME_STATE_DIR", default_state_dir)
.libPaths(unique(c(runtime_library, .libPaths())))

if (!runtime_updates_enabled()) {
  log_message("Runtime package updates are disabled.")
  quit(save = "no", status = 0)
}

missing_packages <- vapply(specs, function(spec) !package_installed(spec$package), logical(1))
if (!nzchar(token)) {
  if (!any(missing_packages)) {
    log_message("No GIT_PAT or GITHUB_PAT set; keeping installed private packages.")
    quit(save = "no", status = 0)
  }
  missing <- vapply(specs[missing_packages], function(spec) spec$package, character(1))
  if (truthy(env_value("KFLOW_RUNTIME_REQUIRE_PRIVATE_PACKAGES", "false"))) {
    log_message("No GIT_PAT or GITHUB_PAT set and required package(s) missing: %s.", paste(missing, collapse = ", "))
    quit(save = "no", status = missing_token_status)
  }
  log_message(
    "No GIT_PAT or GITHUB_PAT set; skipping optional private package(s): %s.",
    paste(missing, collapse = ", ")
  )
  quit(save = "no", status = 0)
}

if (!ensure_runtime_library(runtime_library)) {
  if (!any(missing_packages)) {
    log_message("Runtime library %s is not writable; keeping installed packages.", runtime_library)
    quit(save = "no", status = 0)
  }
  log_message("Runtime library %s is not writable and required packages are missing.", runtime_library)
  quit(save = "no", status = missing_library_status)
}

dir.create(state_dir, recursive = TRUE, showWarnings = FALSE)

for (spec in specs) {
  state_file <- state_path(state_dir, spec$package, spec$repo, spec$ref)
  installed <- package_installed(spec$package)

  if (installed && !should_check_remote(state_file)) {
    log_message("Skipping %s; checked recently.", spec$package)
    next
  }

  current_sha <- installed_remote_sha(spec$package)
  latest_sha <- remote_sha(spec$repo, spec$ref, token)
  force_update <- truthy(env_value("KFLOW_RUNTIME_FORCE_UPDATE", "false"))
  needs_install <- force_update || !installed || !nzchar(current_sha) || !identical(current_sha, latest_sha)

  if (needs_install) {
    log_message(
      "Installing %s from %s@%s (%s -> %s) into %s.",
      spec$package,
      spec$repo,
      spec$ref,
      if (nzchar(current_sha)) substr(current_sha, 1, 7) else "missing",
      substr(latest_sha, 1, 7),
      runtime_library
    )
    install_package(spec, token, runtime_library, force = TRUE)
  } else {
    log_message("%s is current at %s.", spec$package, substr(latest_sha, 1, 7))
  }

  writeLines(latest_sha, state_file)
}

quit(save = "no", status = 0)
