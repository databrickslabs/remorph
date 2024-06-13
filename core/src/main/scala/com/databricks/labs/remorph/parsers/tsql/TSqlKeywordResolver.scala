package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers._

class TSqlKeywordResolver extends KeywordResolver {

  private val tSqlKeywordsPf: PartialFunction[String, Keyword] = {
    // etc...
    case "DELAY" => Keyword(NonReserved, OptionKeyword, ExpressionOption, IntegerOption) // PLaceholer
  }
  override def resolveKeyword(keyword: String): Option[Keyword] = {
    tSqlKeywordsPf.lift(keyword.toUpperCase()).orElse(super.resolveKeyword(keyword))
  }
}
