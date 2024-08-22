-- snowflake sql:
SELECT DISTINCT
  dst.CREATED_DATE
  , dst.task_id
  , dd.delivery_id::TEXT AS delivery_id
  , dst.ISSUE_CATEGORY
  , dst.issue
  , dd.store_id
  FROM proddb.public.dimension_salesforce_tasks dst
  JOIN edw.finance.dimension_deliveries dd
    ON dd.delivery_id = dst.delivery_id --this ensures delivery_id is associated
  WHERE dst.mto_flag = 1
      AND dst.customer_type IN ('Consumer')
      AND dd.STORE_ID IN (SELECT store_id FROM foo.bar.cng_stores_stage)
      AND dd.is_test = false
      AND dst.origin IN ('Chat')
      AND dd_agent_id IS NOT NULL
  AND dst.CREATED_DATE > current_date - 7
  ORDER BY 1 DESC, 3 DESC;
  ;

-- databricks sql:
SELECT DISTINCT
    dst.CREATED_DATE,
    dst.task_id,
    CAST(dd.delivery_id AS STRING) AS delivery_id,
    dst.ISSUE_CATEGORY,
    dst.issue,
    dd.store_id
  FROM proddb.public.dimension_salesforce_tasks AS dst
  JOIN edw.finance.dimension_deliveries AS dd
    ON dd.delivery_id = dst.delivery_id /* this ensures delivery_id is associated */
  WHERE
    dst.mto_flag = 1
    AND dst.customer_type IN ('Consumer')
    AND dd.STORE_ID IN (
      SELECT
        store_id
      FROM foo.bar.cng_stores_stage
    )
    AND dd.is_test = false
    AND dst.origin IN ('Chat')
    AND NOT dd_agent_id IS NULL
    AND dst.CREATED_DATE > CURRENT_DATE - 7
  ORDER BY
    1 DESC NULLS FIRST,
    3 DESC NULLS FIRST

