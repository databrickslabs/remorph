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
      val input2 = PreProcessing("""with base as (
                                   |
                                   |    select *
                                   |    from {{ ref('stg_twilio__address_tmp') }}
                                   |),
                                   |
                                   |fields as (
                                   |
                                   |    select
                                   |        {{
                                   |            fivetran_utils.fill_staging_columns(
                                   |                source_columns=adapter.get_columns_in_relation(ref('stg_twilio__address_tmp')),
                                   |                staging_columns=get_address_columns()
                                   |            )
                                   |        }}
                                   |    from base
                                   |),
                                   |
                                   |final as (
                                   |
                                   |    select
                                   |        _fivetran_synced,
                                   |        account_id,
                                   |        city,
                                   |        created_at,
                                   |        customer_name,
                                   |        emergency_enabled,
                                   |        friendly_name,
                                   |        cast(id as {{ dbt.type_string() }}) as address_id,
                                   |        iso_country,
                                   |        postal_code,
                                   |        region,
                                   |        street,
                                   |        updated_at,
                                   |        validated,
                                   |        verified
                                   |    from fields
                                   |)
                                   |
                                   |select *
                                   |from final""".stripMargin)
      val result = transpiler.transpile(input2).runAndDiscardState(input)

      // scalastyle:off
      val processed = result match {
        case OkResult(output) =>
          output
        case PartialResult(output, error) =>
          output
        case _ => ""
      }

      println(s"====\n$processed\n====")

      // Show that we cannot use this formatter on Jinja templated SQL
      println(s"${transpiler.format(processed)}")
      // scalastyle:on

      assert(input.source == processed)

    }

  }

}
