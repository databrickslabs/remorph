package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.FunctionDefinition
import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers
import org.scalatest.prop.TableDrivenPropertyChecks
import com.databricks.labs.remorph.parsers.{intermediate => ir}

class TSqlFunctionBuilderSpec extends AnyFlatSpec with Matchers with TableDrivenPropertyChecks {

  private val functionBuilder = new TSqlFunctionBuilder

  // While this appears to be somewhat redundant, it will catch any changes in the functionArity method
  // that happen through typos or other mistakes such as deletion.
  "TSqlFunctionBuilder" should "return correct arity for each function" in {

    val functions = Table(
      ("functionName", "expectedArity"), // Header

      // TSql specific
      ("@@CURSOR_ROWS", Some(FunctionDefinition.notConvertible(0))),
      ("@@DBTS", Some(FunctionDefinition.notConvertible(0))),
      ("@@FETCH_STATUS", Some(FunctionDefinition.notConvertible(0))),
      ("@@LANGID", Some(FunctionDefinition.notConvertible(0))),
      ("@@LANGUAGE", Some(FunctionDefinition.notConvertible(0))),
      ("@@LOCKTIMEOUT", Some(FunctionDefinition.notConvertible(0))),
      ("@@MAX_CONNECTIONS", Some(FunctionDefinition.notConvertible(0))),
      ("@@MAX_PRECISION", Some(FunctionDefinition.notConvertible(0))),
      ("@@NESTLEVEL", Some(FunctionDefinition.notConvertible(0))),
      ("@@OPTIONS", Some(FunctionDefinition.notConvertible(0))),
      ("@@REMSERVER", Some(FunctionDefinition.notConvertible(0))),
      ("@@SERVERNAME", Some(FunctionDefinition.notConvertible(0))),
      ("@@SERVICENAME", Some(FunctionDefinition.notConvertible(0))),
      ("@@SPID", Some(FunctionDefinition.notConvertible(0))),
      ("@@TEXTSIZE", Some(FunctionDefinition.notConvertible(0))),
      ("@@VERSION", Some(FunctionDefinition.notConvertible(0))),
      ("COLLATIONPROPERTY", Some(FunctionDefinition.notConvertible(2))),
      ("MODIFY", Some(FunctionDefinition.xml(1))))

    forAll(functions) { (functionName: String, expectedArity: Option[FunctionDefinition]) =>
      functionBuilder.functionDefinition(functionName) shouldEqual expectedArity
    }
  }

  "TSqlFunctionBuilder rename strategy" should "handle default case" in {

    val result = functionBuilder.rename("UNKNOWN_FUNCTION", List.empty)
    assert(result == ir.CallFunction("UNKNOWN_FUNCTION", List.empty))
  }
}
