-- snowflake sql:
SELECT
  demo.level_key:"level_1_key":"level_2_key"['1'] AS col
FROM
    (
     SELECT
        PARSE_JSON('{
            "level_1_key": {
                "level_2_key": {
                    "1": "desired_value"
                }
            }
        }') AS level_key
    ) AS demo;

-- databricks sql:
SELECT
  demo.level_key:level_1_key:level_2_key['1'] AS col
FROM (
  SELECT
    PARSE_JSON(
      '{\n            "level_1_key": {\n                "level_2_key": {\n                    "1": "desired_value"\n                }\n            }\n        }'
    ) AS level_key
) AS demo
