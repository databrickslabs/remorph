-- snowflake sql:
SELECT
    p.info:id AS "ID",
    p.info:first AS "First",
    p.info:first.b AS C
FROM
    (SELECT PARSE_JSON('{"id": {"a":{"c":"102","d":"106"}}, "first": {"b":"105"}}')) AS p(info);

-- databricks sql:
SELECT
  p.info:id AS `ID`,
  p.info:first AS `First`,
  p.info:first.b AS C
FROM (
  SELECT
    PARSE_JSON('{"id": {"a":{"c":"102","d":"106"}}, "first": {"b":"105"}}')
) AS p(info);
