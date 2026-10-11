# Sourcing package logic directly for verification
source("r_package/ipa.labels/R/lookup.R")

test_r_package <- function() {
  cat("=== Testing R Package ipa.labels ===\n")
  
  # Test 1: Lookup symbol 'p'
  cat("\nTest 1: Lookup symbol 'p' details...\n")
  p_details <- ipalookup(symbol = "p")
  if (nrow(p_details) > 0) {
    p_row <- p_details[1, ]
    cat("Success! Details for 'p':\n")
    print(p_row[, c("symbol", "tipa", "voicing", "place", "manner")])
    stopifnot(p_row$tipa == "p")
    stopifnot(p_row$voicing == "voiceless")
  } else {
    stop("Failed: No details found for 'p'")
  }
  
  # Test 2: Structured lookup
  cat("\nTest 2: Lookup voiceless velar plosive symbol...\n")
  symbols <- ipalookup(voicing = "voiceless", place = "velar", manner = "plosive", fields = "symbol")
  cat("Results: ", paste(symbols, collapse = ", "), "\n")
  stopifnot("k" %in% symbols)
  
  # Test 3: Free-text query
  cat("\nTest 3: Query for 'voiced bilabial plosive'...\n")
  b_matches <- ipaquery("voiced bilabial plosive", fields = "symbol")
  cat("Results: ", paste(b_matches, collapse = ", "), "\n")
  stopifnot("b" %in% b_matches)
  
  # Test 4: Query by IPA Name 'Esh'
  cat("\nTest 4: Query for 'Esh'...\n")
  esh_matches <- ipaquery("Esh", fields = "symbol")
  cat("Results: ", paste(esh_matches, collapse = ", "), "\n")
  stopifnot("\u0283" %in% esh_matches) # \u0283 is Esh (ʃ)
  
  # Test 5: Verify closeness/openness/height fields
  cat("\nTest 5: Checking closeness/openness/height vowel fields for 'i'...\n")
  i_details <- ipalookup(symbol = "i")
  i_row <- i_details[1, ]
  cat(sprintf("Symbol 'i': height=%s, closeness=%s, openness=%s\n", 
              i_row$height, i_row$closeness, i_row$openness))
  stopifnot(i_row$height == "close")
  stopifnot(i_row$closeness == "close")
  stopifnot(i_row$openness == "close")

  # Test 6: Convenience accessors
  cat("\nTest 6: Convenience accessors...\n")
  stopifnot(ipaget("p", "place") == "bilabial")
  places <- ipavalues("place", type = "consonant", unique = TRUE)
  stopifnot("bilabial" %in% places)
  stopifnot(!("" %in% places))

  p <- ipaget("p")
  stopifnot(p$symbol$ipa == "p")
  stopifnot(p$code$unicode == p$code$usv)
  stopifnot(p$label$place == "bilabial")
  stopifnot(identical(p$features$consonantal, TRUE))
  stopifnot(identical(p$features$labial, TRUE))
  stopifnot(!is.null(p$description$ipa_name))
  stopifnot(length(ipainventory(iso639_3 = "eng")) > 1)
  
  cat("\n=== All R tests passed successfully! ===\n")
}

test_r_package()
