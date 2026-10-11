\name{ipavalues}
\alias{ipavalues}
\title{Get values for a field across matching IPA records}
\description{Returns non-empty values for one field across records matching the supplied criteria.}
\usage{ipavalues(field, criteria = list(), unique = FALSE, ...)}
\arguments{
  \item{field}{The database field to return.}
  \item{criteria}{A named list of query values.}
  \item{unique}{Logical; if TRUE, duplicate values are removed.}
  \item{...}{Direct keyword arguments for matching fields.}
}
\value{A character vector of non-empty field values.}
\examples{
ipavalues("height", type = "vowel", unique = TRUE)
ipavalues("place", type = "consonant", unique = TRUE)
}
\seealso{\code{\link{ipaget}}}
\keyword{database}
