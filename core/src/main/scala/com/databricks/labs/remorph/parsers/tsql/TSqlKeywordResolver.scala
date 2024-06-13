package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers._

class TSqlKeywordResolver extends KeywordResolver {

  private val tSqlKeywordsPf: PartialFunction[String, Keyword] = {
    case "DELAY" => Keyword(NonReserved, OptionKeyword, ExpressionOption)
    case "TIME" => Keyword(NonReserved, OptionKeyword, BooleanOption)
    case "TIMEOUT" => Keyword(NonReserved, OptionKeyword, BooleanOption)
    // etc...

  }
  override def resolveKeyword(keyword: String): Option[Keyword] = {
    tSqlKeywordsPf.lift(keyword.toUpperCase()).orElse(super.resolveKeyword(keyword))
  }
}
