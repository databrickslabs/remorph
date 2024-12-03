package com.databricks.labs.remorph.preprocessors.jinja

import com.databricks.labs.remorph.transpilers.TSqlToDatabricksTranspiler
import com.databricks.labs.remorph.{OkResult, PartialResult, PreProcessing, TranspilerState}
import org.scalatest.wordspec.AnyWordSpec

// Note that this test is as much for debugging purposes as anything else, but it does create the more complex
// cases of template use.
// Integration tests are really where it's at
class JinjaProcessorTest extends AnyWordSpec {

  "Preprocessor" should {
    "pre statement block" in {

      val transpiler = new TSqlToDatabricksTranspiler

      // Note that template replacement means that token lines and offsets will be out of sync with the start point
      // and we will need to insert positional tokens in a subsequent PR, so that the lexer can account for the missing
      // text. Another option may be to pas the replacement _!Jinja9999 with spaces and newlines to match the length
      // of the text they are replacing.
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

      // Note that we cannot format the output because the Scala based formatter we have does not handle DBT/Jinja
      // templates and therefore breaks the output
      val output = """{%- set payment_methods = dbt_utils.get_column_values(
                     |                              table=ref('raw_payments'),
                     |                              column='payment_method'
                     |) -%}
                     |
                     |SELECT order_id,
                     |    {%- for payment_method in payment_methods %}
                     |    SUM(CASE WHEN payment_method = '{{payment_method}}' THEN amount END) AS  {{payment_method}}_amount
                     |    {%- if not loop.last %},{% endif -%}
                     |    {% endfor %}
                     |    FROM  {{ ref('raw_payments') }}
                     |    GROUP BY 1;""".stripMargin

      val result = transpiler.transpile(input).runAndDiscardState(TranspilerState(input))

      val processed = result match {
        case OkResult(output) =>
          output
        case PartialResult(output, error) =>
          output
        case _ => ""
      }
      assert(output == processed)
    }
  }
}
