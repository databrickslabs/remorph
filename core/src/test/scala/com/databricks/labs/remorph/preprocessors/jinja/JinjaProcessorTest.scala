package com.databricks.labs.remorph.preprocessors.jinja

import com.databricks.labs.remorph.transpilers.TSqlToDatabricksTranspiler
import com.databricks.labs.remorph.{OkResult, PartialResult, PreProcessing}
import org.scalatest.wordspec.AnyWordSpec

class JinjaProcessorTest extends AnyWordSpec {

  "Preprocessor" should {
    "pre statement block" in {

      val transpiler = new TSqlToDatabricksTranspiler
      val input = PreProcessing("""{%- set payment_methods = dbt_utils.get_column_values(
                            |                              table=ref('raw_payments'),
                            |                              column='payment_method'
                            |) -%}
                            |
                            |select
                            |    order_id,
                            |    {%- for payment_method in payment_methods %}
                            |    sum(case when payment_method = '{{payment_method}}' then amount end) as {{payment_method}}_amount
                            |    {%- if not loop.last %},{% endif -%}
                            |    {% endfor %}
                            |    from {{ ref('raw_payments') }}
                            |    group by 1
                            |""".stripMargin)
      val result = transpiler.transpile(input).runAndDiscardState(input)

      // scalastyle:off
      val processed = result match {
        case OkResult(output) =>
          output
        case PartialResult(output, error) =>
          output
        case _ => ""
      }

      println(s"====\n$processed\n====")
      println(s"${transpiler.format(processed)}")
      // scalastyle:on

      assert(input.source == processed)

    }

  }

}
