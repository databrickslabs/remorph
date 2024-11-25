package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.intermediate.IRHelpers
import org.scalatest.Assertion
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class TSqlErrorStategySpec extends AnyWordSpec with TSqlParserTestCommon with Matchers with IRHelpers {
  override protected def astBuilder: TSqlParserBaseVisitor[_] = vc.astBuilder

  private def checkError(query: String, errContains: String): Assertion =
    checkError(query, _.tSqlFile(), errContains)

  "TSqlErrorStrategy" should {
    "process an invalid match parser exception" in {
      checkError(query = "SELECT * FROM", errContains = "was unexpected")
    }
    "process an extraneous input exception" in {
      checkError(query = "*", errContains = "unexpected extra input")
    }
    "process a missing input exception" in {
      checkError(query = "SELECT * FROM FRED As X Y ", errContains = "unexpected extra input")
    }
  }

  "TSqlErrorStrategy" should {
    "produce human readable messages" in {
      checkError(
        query = "SELECT * FROM FRED As X Y ",
        errContains = "unexpected extra input 'Y' while parsing a T-SQL batch")

      checkError(
        query = "*",
        errContains = "unexpected extra input '*' while parsing a T-SQL batch\n" +
          "expecting one of: End of batch, Identifier, Select Statement, Statement, ")

      checkError(
        query = "SELECT * FROM",
        errContains = "'<EOF>' was unexpected while parsing a table source in a FROM clause " +
          "in a SELECT statement\nexpecting one of:")
    }
  }
}
