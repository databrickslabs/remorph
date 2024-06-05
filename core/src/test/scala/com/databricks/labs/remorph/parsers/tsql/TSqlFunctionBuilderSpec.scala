package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.FunctionDefinition
import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers
import org.scalatest.prop.TableDrivenPropertyChecks

class TSqlFunctionBuilderSpec extends AnyFlatSpec with Matchers with TableDrivenPropertyChecks {

  // While this appears to be somewhat redundant, it will catch any changes in the functionArity method
  // that happen through typos or other mistakes such as deletion.
  "TSqlFunctionBuilder" should "return correct arity for each function" in {
    val functionBuilder = new TSqlFunctionBuilder

    val functions = Table(
      ("functionName", "expectedArity"), // Header

      // TSql specific
      ("@@CURSOR_STATUS", Some(FunctionDefinition.notConvertible(0))),
      ("@@FETCH_STATUS", Some(FunctionDefinition.notConvertible(0))),
      ("MODIFY", Some(FunctionDefinition.xml(1))))

    forAll(functions) { (functionName: String, expectedArity: Option[FunctionDefinition]) =>
      functionBuilder.functionDefinition(functionName) shouldEqual expectedArity
    }
  }

}
