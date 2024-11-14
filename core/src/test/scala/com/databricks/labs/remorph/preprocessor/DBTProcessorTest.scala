package com.databricks.labs.remorph.preprocessor

import com.databricks.labs.remorph.{OkResult, Parsing}
import com.databricks.labs.remorph.preprocessor.dbt.DBTPreprocessor
import org.scalatest.wordspec.AnyWordSpec

class DBTProcessorTest extends AnyWordSpec {

  "Preprocessor" should {
    "process statement block" in {

      // NB: These will be moved to a PreProcessorTestCommon trait
      val dbtPreProc = new DBTPreprocessor()
      val input = Parsing("""{%- set payment_methods = dbt_utils.get_column_values(
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
      val result = dbtPreProc.process(input).run(input)

      // scalastyle:off
      result match {
        case OkResult(output) => println(output._2)
        case _ => assert(false)
      }
      // scalastyle:on

      assert(true)

    }

  }

}
