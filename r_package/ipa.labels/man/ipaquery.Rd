% Generated manually; keep synchronized with R/lookup.R documentation.
\name{ipaquery}
\alias{ipaquery}
\title{Free-text IPA database query}
\description{
Searches all database fields case-insensitively for a free-text query.
When the query contains multiple words, every word must occur somewhere in
the same record.
}
\usage{
ipaquery(search_term, fields = NULL)
}
\arguments{
  \item{search_term}{A character string containing one or more search
  terms, such as \code{"voiced dental fricative"}.}
  \item{fields}{\code{NULL} to return all columns, one column name to
  return a vector, or multiple column names to return a data frame.}
}
\value{
A data frame containing matching records, a vector when one field is
requested, or a data frame containing only the requested columns.
}
\examples{
ipaquery("voiced implosive", fields = c("symbol", "description"))
ipaquery("schwa", fields = "symbol")
}
\seealso{\code{\link{ipalookup}}}
\keyword{database}
\keyword{documentation}
