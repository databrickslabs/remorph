-- snowflake sql:
SELECT
  d.value:display_position::NUMBER as display_position,
  i.value:attributes::VARCHAR as attributes,
  cast(current_timestamp() as timestamp_ntz(9)) as created_at,
  i.value:prop::FLOAT as prop,
  candidates
FROM dwh.vw  d,
LATERAL FLATTEN (INPUT => d.impressions, OUTER => true) i
WHERE event_date = '{start_date}' and event_name in ('store.replacements_view');

-- databricks sql:
SELECT
  CAST(d.value.display_position AS DECIMAL(38, 0)) AS display_position,
  CAST(i.attributes AS STRING) AS attributes,
  CAST(CURRENT_TIMESTAMP() AS TIMESTAMP_NTZ) AS created_at,
  CAST(i.prop AS DOUBLE) AS prop, candidates
FROM dwh.vw AS d LATERAL VIEW OUTER EXPLODE(d.impressions) AS i
WHERE event_date = '{start_date}' AND event_name IN ('store.replacements_view');
