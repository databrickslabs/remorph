-- snowflake sql:
SELECT
  d.value:display_position::NUMBER AS display_position,
  i.value:attributes::VARCHAR AS attributes,
  CAST(CURRENT_TIMESTAMP() AS TIMESTAMP_NTZ(9)) AS created_at,
  i.value:prop::FLOAT AS prop,
  d.value:candidates AS candidates
FROM
  (
    SELECT
      OBJECT_CONSTRUCT(
        'display_position', 123,
        'impressions', ARRAY_CONSTRUCT(
          OBJECT_CONSTRUCT('attributes', 'attr1', 'prop', 12.34),
          OBJECT_CONSTRUCT('attributes', 'attr2', 'prop', 56.78)
        ),
        'candidates', 'some_candidates'
      ) AS value,
      '2024-08-28' AS event_date,
      'store.replacements_view' AS event_name
  ) AS d,
  LATERAL FLATTEN(input => d.value:impressions) AS i
WHERE
  d.event_date = '2024-08-28'
  AND d.event_name IN ('store.replacements_view');

-- databricks sql:
SELECT
  CAST(d.value.display_position AS DECIMAL(38, 0)) AS display_position,
  CAST(i.attributes AS STRING) AS attributes,
  CAST(CURRENT_TIMESTAMP() AS TIMESTAMP_NTZ) AS created_at,
  CAST(i.prop AS DOUBLE) AS prop,
  d.value.candidates AS candidates
FROM (
  SELECT
    STRUCT(
      123 AS display_position,
      ARRAY(
        STRUCT('some attributes' AS attributes, 12.34 AS prop),
        STRUCT('other attributes' AS attributes, 56.78 AS prop)
      ) AS impressions,
      'some candidates' AS candidates
    ) AS value,
    '2024-08-28' AS event_date,
    'store.replacements_view' AS event_name
) AS d
LATERAL VIEW OUTER EXPLODE(d.value.impressions) AS i
WHERE
  d.event_date = '2024-08-28'
  AND d.event_name IN ('store.replacements_view');