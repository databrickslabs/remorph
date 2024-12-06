-- presto sql:
SELECT
  *,
  any_keys_match(
    metadata,
    k -> (
      k LIKE 'config_%'
      OR k = 'active'
    )
  ) AS has_config_or_active
FROM
  your_table;

-- databricks sql:
SELECT
  *,
  EXISTS(
    MAP_KEYS(metadata),
    k -> (
      k LIKE 'config_%'
      OR k = 'active'
    )
  ) AS has_config_or_active
FROM
  your_table;
