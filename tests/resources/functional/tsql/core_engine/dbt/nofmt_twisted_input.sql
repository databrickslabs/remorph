-- tsql sql:
{%- set payment_methods = dbt_utils.get_column_values(
                              table=ref('raw_payments'),
                              column='payment_method'
) -%}

select
    order_id,
    {%- for payment_method in payment_methods %}
    sum(case when payment_method = '{{payment_method}}' then amount end) as {{payment_method}}_amount
    {%- if not loop.last %},{% endif -%}
    {% endfor %}
    from {{ ref('raw_payments') }}
    group by 1
-- databricks sql:
{%- set payment_methods = dbt_utils.get_column_values(
                              table=ref('raw_payments'),
                              column='payment_method'
) -%}

SELECT order_id,
    {%- for payment_method in payment_methods %}
    SUM(CASE WHEN payment_method = '{{payment_method}}' THEN amount END) AS  {{payment_method}}_amount
    {%- if not loop.last %},{% endif -%}
    {% endfor %}
    FROM  {{ ref('raw_payments') }}
    GROUP BY 1;
