% Generated manually; keep synchronized with R/lookup.R documentation.
\name{ipalookup}
\alias{ipalookup}
\title{Structured IPA database lookup}
\description{
Looks up International Phonetic Alphabet records matching one or more
named fields. The package CSV is read at runtime, so edits to the database
are available without recompiling the package.
}
\usage{
ipalookup(criteria = list(), fields = NULL, ...)
}
\arguments{
  \item{criteria}{A named list of query values, such as
  \code{list(voicing = "voiced", place = "bilabial")}.}
  \item{fields}{\code{NULL} to return all columns, one column name to
  return a vector, or multiple column names to return a data frame.}
  \item{...}{Additional named field-value criteria. These override values
  with the same names in \code{criteria}.}
}
\value{
A data frame containing matching records, a vector when one field is
requested, or a data frame containing only the requested columns.
}
\examples{
ipalookup(voicing = "voiceless", place = "velar", manner = "plosive",
          fields = "symbol")
ipalookup(list(type = "vowel", frontness = "front"),
          fields = c("symbol", "roundedness"))
}
\seealso{\code{\link{ipaquery}}}
\keyword{database}
\keyword{documentation}
