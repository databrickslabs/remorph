package com.databricks.labs.remorph.queries

import com.databricks.labs.remorph.{OkResult, TransformationConstructors}
import com.databricks.labs.remorph.parsers.PlanParser
import com.databricks.labs.remorph.intermediate.NoopNode
import org.antlr.v4.runtime.ParserRuleContext
import org.mockito.ArgumentMatchers.any
import org.mockito.Mockito.when
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec
import org.scalatestplus.mockito.MockitoSugar

class ExampleDebuggerTest extends AnyWordSpec with Matchers with MockitoSugar with TransformationConstructors {
  "ExampleDebugger" should {
    "work" in {
      val buf = new StringBuilder
      val parser = mock[PlanParser[_]]
      when(parser.parse(any())).thenReturn(lift(OkResult(ParserRuleContext.EMPTY)))
      when(parser.visit(any())).thenReturn(lift(OkResult(NoopNode)))

      val debugger = new ExampleDebugger(parser, x => buf.append(x), "snowflake")
      val name = s"${NestedFiles.projectRoot}/tests/resources/functional/snowflake/nested_query_with_json_1.sql"

      debugger.debugExample(name)

      buf.toString() should equal("NoopNode$\n")
    }
  }
}
