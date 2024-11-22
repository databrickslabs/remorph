package com.databricks.labs.remorph.preprocessors.jinja

import com.databricks.labs.remorph.{OkResult, PreProcessing}
import org.scalatest.wordspec.AnyWordSpec

class JinjaProcessorTest extends AnyWordSpec {

  "Preprocessor" should {
    "pre statement block" in {

      // NB: These will be moved to a PreProcessorTestCommon trait
      val dbtPreProc = new JinjaProcessor()
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
      val result = dbtPreProc.pre(input).run(input)

      // scalastyle:off
      val processed = result match {
        case OkResult(output) =>
          dbtPreProc.post(output._2.source).run(output._2) match {
            case OkResult(output) => output._2
            case _ => ""
          }
        case _ => ""
      }

      println(processed)
      // scalastyle:on

      assert(input.source == processed)

    }

  }

}
