#!/usr/bin/env Rscript

# Verify that the private and public workflow packages baked into the image are
# present at their requested immutable commits. This script runs during image
# construction, before the final runtime layers are written.
args <- commandArgs(trailingOnly = TRUE)
if (!length(args) || any(!grepl("^--[^=]+=.+$", args))) {
  stop("Expected --name=<commit> arguments.", call. = FALSE)
}

keys <- sub("^--([^=]+)=.*$", "\\1", args)
values <- sub("^--[^=]+=", "", args)
expected <- stats::setNames(values, keys)

package_for_key <- c(
  flcore = "FLCore",
  flr4mfcl = "FLR4MFCL",
  condorbox = "CondorBox",
  tandoori = "tandoori",
  kflowkit = "KflowKit",
  mfclrtmb = "mfclrtmb",
  mfclkit = "mfclkit",
  mfclshiny = "mfclshiny"
)

unknown <- setdiff(names(expected), names(package_for_key))
missing <- setdiff(names(package_for_key), names(expected))
if (length(unknown) || length(missing)) {
  stop(
    "Unexpected verification arguments. Unknown: ", paste(unknown, collapse = ", "),
    "; missing: ", paste(missing, collapse = ", "),
    call. = FALSE
  )
}

for (key in names(package_for_key)) {
  package <- package_for_key[[key]]
  if (!requireNamespace(package, quietly = TRUE)) {
    stop("Required package is missing: ", package, call. = FALSE)
  }

  description <- utils::packageDescription(package)
  actual <- description$RemoteSha
  if (is.null(actual)) actual <- ""
  actual <- tolower(trimws(actual))
  wanted <- tolower(trimws(expected[[key]]))
  if (!identical(actual, wanted)) {
    stop(
      "Pinned commit mismatch for ", package, ": expected ", wanted,
      ", found ", if (nzchar(actual)) actual else "<none>",
      call. = FALSE
    )
  }
}

message("Verified bundled workflow packages at requested commits.")
