\name{ipaget}
\alias{ipaget}
\title{Get one label for an IPA symbol}
\description{Returns one field from the first record matching an exact IPA symbol.}
\usage{ipaget(symbol, field, default = NA_character_)}
\arguments{
  \item{symbol}{An exact IPA symbol.}
  \item{field}{The database field to return.}
  \item{default}{The value returned when no matching symbol is found.}
}
\value{A single field value.}
\examples{ipaget("p", "place")}
\seealso{\code{\link{ipavalues}}}
\keyword{database}
