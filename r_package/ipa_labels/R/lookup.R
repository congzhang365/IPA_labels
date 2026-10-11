#' Load IPA Symbols Database
#' 
#' Dynamically reads the compressed JSON database from the package data directory.
#' 
#' @return A data frame containing the IPA database.
#' @importFrom utils read.csv
load_ipa_data <- function() {
  data_path <- system.file("extdata", "ipa_symbols.json.gz", package = "ipa_labels")
  if (data_path == "") {
    # Fallback to local workspace paths if package is not fully installed yet (for tests)
    possible_paths <- c(
      file.path(getwd(), "inst", "extdata", "ipa_symbols.json.gz"),
      file.path(getwd(), "ipa_symbols.json.gz"),
      file.path(getwd(), "r_package", "ipa_labels", "inst", "extdata", "ipa_symbols.json.gz"),
      file.path(getwd(), "inst", "extdata", "ipa_symbols.csv"),
      file.path(getwd(), "ipa_symbols.csv"),
      file.path(getwd(), "r_package", "ipa_labels", "inst", "extdata", "ipa_symbols.csv")
    )
    for (p in possible_paths) {
      if (file.exists(p)) {
        data_path <- p
        break
      }
    }
  }
  
  if (data_path == "" || !file.exists(data_path)) {
    stop("ipa_symbols.json.gz could not be located in the package directory.")
  }

  if (grepl("\\.json\\.gz$", data_path)) {
    connection <- gzfile(data_path, open = "rb")
    on.exit(close(connection), add = TRUE)
    json_text <- rawToChar(readBin(connection, what = "raw", n = 100000000L))
    return(jsonlite::fromJSON(json_text, simplifyDataFrame = TRUE))
  }

  # Backward-compatible fallback for an unbuilt development checkout.
  read.csv(data_path, fileEncoding = "UTF-8", stringsAsFactors = FALSE, check.names = FALSE)
}

load_ipa_json <- function(filename, default = list()) {
  data_path <- system.file("extdata", filename, package = "ipa_labels")
  if (data_path == "") {
    possible_paths <- c(
      file.path(getwd(), "inst", "extdata", filename),
      file.path(getwd(), "r_package", "ipa_labels", "inst", "extdata", filename)
    )
    for (p in possible_paths) if (file.exists(p)) { data_path <- p; break }
  }
  if (data_path == "" || !file.exists(data_path)) return(default)
  connection <- gzfile(data_path, open = "rb")
  on.exit(close(connection), add = TRUE)
  jsonlite::fromJSON(rawToChar(readBin(connection, what = "raw", n = 100000000L)), simplifyDataFrame = FALSE)
}

#' Structured IPA Database Lookup
#' 
#' Looks up phonetic records matching specified search criteria keys.
#' 
#' @param criteria A named list of query values (e.g., \code{list(voicing = "voiced", place = "bilabial")}).
#' @param fields A character vector of column names to return (e.g. \code{"symbol"} or \code{c("symbol", "tipa")}). If NULL, returns all columns.
#' @param ... Direct keyword arguments (e.g., \code{voicing = "voiced", place = "bilabial"}).
#' @return If fields is a single string, returns a vector of values. If fields is a vector, returns a filtered data frame.
#' @export
#' @examples
#' ipalookup(voicing = "voiceless", place = "velar", manner = "plosive", fields = "symbol")
#' ipalookup(list(type = "vowel", frontness = "front"), fields = c("symbol", "roundedness"))
ipalookup <- function(criteria = list(), fields = NULL, ...) {
  df <- load_ipa_data()
  
  # Merge criteria list and extra arguments
  dots <- list(...)
  search_dict <- criteria
  for (name in names(dots)) {
    search_dict[[name]] <- dots[[name]]
  }
  
  if (length(search_dict) == 0) {
    return(filter_fields(df, fields))
  }
  
  # Perform matching
  matches <- rep(TRUE, nrow(df))
  case_sensitive_fields <- c("symbol", "hex_code", "sampa", "arpabet")
  
  for (key in names(search_dict)) {
    if (!key %in% colnames(df)) {
      warning(paste("Field '", key, "' does not exist in the database.", sep = ""))
      matches <- rep(FALSE, nrow(df))
      break
    }
    
    row_vals <- trimws(as.character(df[[key]]))
    target_val <- trimws(as.character(search_dict[[key]]))
    
    if (key %in% case_sensitive_fields) {
      matches <- matches & (row_vals == target_val)
    } else {
      matches <- matches & (tolower(row_vals) == tolower(target_val))
    }
  }
  
  matched_df <- df[matches, , drop = FALSE]
  rownames(matched_df) <- NULL
  return(filter_fields(matched_df, fields))
}

#' Free-text IPA Database Query
#' 
#' Searches all text columns case-insensitively for the specified search term. If the term contains multiple words,
#' all words must match somewhere in the row.
#' 
#' @param search_term A character string containing search keywords (e.g., \code{"voiced dental fricative"}).
#' @param fields A character vector of column names to return. If NULL, returns all columns.
#' @return If fields is a single string, returns a vector of values. If fields is a vector, returns a filtered data frame.
#' @export
#' @examples
#' ipaquery("voiced implosive", fields = c("symbol", "description"))
#' ipaquery("schwa", fields = "symbol")
ipaquery <- function(search_term, fields = NULL) {
  df <- load_ipa_data()
  
  clean_term <- tolower(trimws(as.character(search_term)))
  search_words <- strsplit(clean_term, "\\s+")[[1]]
  
  if (length(search_words) == 0) {
    return(data.frame())
  }
  
  # Check if all search words match in any column of the row
  matches <- rep(TRUE, nrow(df))
  
  # Build a combined text representation for each row
  row_texts <- tolower(apply(df, 1, function(row) {
    paste(row, collapse = " ")
  }))
  
  for (word in search_words) {
    # Match the word inside the combined row text
    word_matches <- grepl(word, row_texts, fixed = TRUE)
    matches <- matches & word_matches
  }
  
  matched_df <- df[matches, , drop = FALSE]
  rownames(matched_df) <- NULL
  return(filter_fields(matched_df, fields))
}

#' Get one label for an IPA symbol
#'
#' @param symbol An exact IPA symbol.
#' @param field The database field to return.
#' @param default Value returned when no matching symbol is found.
#' @return A single field value.
#' @export
ipaget <- function(symbol, field = NULL, default = NA_character_) {
  matches <- ipalookup(symbol = symbol)
  if (nrow(matches) == 0) {
    return(default)
  }
  if (is.null(field)) {
    row <- matches[1, , drop = FALSE]
    features <- load_ipa_json("ipa_features.json.gz")[[as.character(symbol)]]
    if (is.null(features)) features <- list()
    height <- row$height[[1]]; frontness <- row$frontness[[1]]
    label_parts <- if (row$type[[1]] == "consonant") {
      c(row$voicing[[1]], row$place[[1]], row$manner[[1]])
    } else {
      c(height, frontness, row$roundedness[[1]], row$type[[1]])
    }
    full <- paste(na.omit(label_parts), collapse = " ")
    usv <- row$usv_code[[1]]
    return(list(
      symbol = list(ipa = row$symbol[[1]], sampa = na_or_null(row$sampa[[1]]), arpabet = na_or_null(row$arpabet[[1]]), default = row$symbol[[1]]),
      code = list(tipa = na_or_null(row$tipa[[1]]), ipa_number = na_or_null(row$ipa_number[[1]]), usv = na_or_null(usv), unicode = na_or_null(usv), unicode_range = na_or_null(row$unicode_range[[1]]), hex = na_or_null(row$hex_code[[1]]), decimal = na_or_null(row$decimal_code[[1]]), afii = na_or_null(row$af_ii[[1]]), default = na_or_null(row$tipa[[1]])),
      label = list(full = full, type = na_or_null(row$type[[1]]), voicing = na_or_null(row$voicing[[1]]), place = na_or_null(row$place[[1]]), manner = na_or_null(row$manner[[1]]), height = na_or_null(height), closeness = na_or_null(height), openness = na_or_null(height), frontness = na_or_null(frontness), backness = na_or_null(frontness), roundedness = na_or_null(row$roundedness[[1]]), default = full),
      features = c(features, list(default = features)),
      description = list(ipa_name = na_or_null(row$ipa_name[[1]]), unicode_name = na_or_null(row$unicode_name[[1]]), text = na_or_null(row$description[[1]]), default = na_or_null(row$ipa_name[[1]]))
    ))
  }
  if (!field %in% colnames(matches)) {
    stop(paste("Field '", field, "' does not exist in the database.", sep = ""))
  }
  matches[[field]][1]
}

na_or_null <- function(value) {
  if (is.null(value) || length(value) == 0 || is.na(value) || value %in% c("", "NA", "N/A")) NA else value
}

ipainventory <- function(language = NULL, iso639_3 = NULL, glottocode = NULL, inventory_id = NULL) {
  records <- load_ipa_json("phoible_inventories.json.gz")
  if (!is.null(language)) records <- Filter(function(x) tolower(x$language %||% "") == tolower(language), records)
  if (!is.null(iso639_3)) records <- Filter(function(x) identical(x$iso639_3, iso639_3), records)
  if (!is.null(glottocode)) records <- Filter(function(x) identical(x$glottocode, glottocode), records)
  if (!is.null(inventory_id)) records <- Filter(function(x) as.character(x$inventory_id) == as.character(inventory_id), records)
  records
}

`%||%` <- function(x, y) if (is.null(x)) y else x

#' Get values for a field across matching IPA records
#'
#' @param field The database field to return.
#' @param criteria A named list of query values.
#' @param unique Logical; if TRUE, remove duplicate values.
#' @param ... Direct keyword arguments for matching fields.
#' @return A character vector of non-empty field values.
#' @export
ipavalues <- function(field, criteria = list(), unique = FALSE, ...) {
  matches <- ipalookup(criteria = criteria, fields = field, ...)
  values <- matches[nzchar(matches)]
  if (unique) {
    values <- unique(values)
  }
  values
}

# Helper to filter fields based on fields argument
filter_fields <- function(df, fields) {
  if (is.null(fields)) {
    return(df)
  }
  
  if (length(fields) == 1) {
    # Return a flat vector of values
    if (!fields %in% colnames(df)) {
      stop(paste("Field '", fields, "' does not exist in the database.", sep = ""))
    }
    return(df[[fields]])
  }
  
  # Return data frame with only requested columns
  invalid_fields <- fields[!fields %in% colnames(df)]
  if (length(invalid_fields) > 0) {
    stop(paste("The following fields do not exist in the database: ", paste(invalid_fields, collapse = ", "), sep = ""))
  }
  
  return(df[, fields, drop = FALSE])
}
