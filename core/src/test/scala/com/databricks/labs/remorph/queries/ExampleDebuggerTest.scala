package com.databricks.labs.remorph.queries

import com.databricks.labs.remorph.parsers.PlanParser
import com.databricks.labs.remorph.intermediate.NoopNode
import com.databricks.labs.remorph.Result
import org.antlr.v4.runtime.ParserRuleContext
import org.mockito.ArgumentMatchers.any
import org.mockito.Mockito.when
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec
import org.scalatestplus.mockito.MockitoSugar

class ExampleDebuggerTest extends AnyWordSpec with Matchers with MockitoSugar {
  "ExampleDebugger" should {
    "work" in {
      val buf = new StringBuilder
      val parser = mock[PlanParser[_]]
      when(parser.parse(any())).thenReturn(Result.Success(ParserRuleContext.EMPTY))
      when(parser.visit(any())).thenReturn(Result.Success(NoopNode))

      val debugger = new ExampleDebugger(_ => parser, x => buf.append(x))
      val name = s"${NestedFiles.projectRoot}/tests/resources/functional/snowflake/nested_query_with_json_1.sql"

      debugger.debugExample(name, None)

      buf.toString() should equal("NoopNode$\n")
    }
  }
}
