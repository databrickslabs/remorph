package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.IRHelpers
import org.scalatest.Assertion
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class TSqlErrorStategySpec extends AnyWordSpec with TSqlParserTestCommon with Matchers with IRHelpers {
  override protected def astBuilder: TSqlParserBaseVisitor[_] = new TSqlAstBuilder

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
      checkError(query = "SELECT * FROM FRED As X Y ", errContains = "missing")
    }
  }

}
