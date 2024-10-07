-- snowflake sql:
SELECT
  d.col:display_position::NUMBER AS display_position,
  i.value:attributes::VARCHAR AS attributes,
  CAST(CURRENT_TIMESTAMP() AS TIMESTAMP_NTZ(9)) AS created_at,
  i.value:prop::FLOAT AS prop,
  d.col:candidates AS candidates
FROM
  (
    SELECT
      PARSE_JSON('{"display_position": 123, "impressions": [{"attributes": "some_attributes", "prop": 12.34}, {"attributes": "other_attributes", "prop": 56.78}], "candidates": "some_candidates"}') AS col,
      '2024-08-28' AS event_date,
      'store.replacements_view' AS event_name
  ) AS d,
  LATERAL FLATTEN(input => d.col:impressions, outer => true) AS i
WHERE
  d.event_date = '2024-08-28'
  AND d.event_name IN ('store.replacements_view');

-- databricks sql:
SELECT
  CAST(d.col:display_position AS DECIMAL(38, 0)) AS display_position,
  CAST(i.value:attributes AS STRING) AS attributes,
  CAST(CURRENT_TIMESTAMP() AS TIMESTAMP_NTZ) AS created_at,
  CAST(i.value:prop AS DOUBLE) AS prop,
  d.col:candidates AS candidates
FROM (
  SELECT
    PARSE_JSON('{"display_position": 123, "impressions": [{"attributes": "some_attributes", "prop": 12.34}, {"attributes": "other_attributes", "prop": 56.78}], "candidates": "some_candidates"}') AS col,
    '2024-08-28' AS event_date,
    'store.replacements_view' AS event_name
) AS d
, LATERAL VARIANT_EXPLODE_OUTER(d.col:impressions) AS i
WHERE
  d.event_date = '2024-08-28' AND d.event_name IN ('store.replacements_view');
