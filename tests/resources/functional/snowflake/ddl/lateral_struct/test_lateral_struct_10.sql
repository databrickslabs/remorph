-- snowflake sql:
SELECT
    tt.id,
    lit.value: details AS details
FROM VALUES
    (1, '{"order": {"id": 101,"items": [{"item_id": "A1","quantity": 2,"details": {"color": "red"}},{"item_id": "B2","quantity": 5,"details": {"color": "blue"}}]}}'),
    (2, '{"order": {"id": 202,"items": [{"item_id": "C3","quantity": 4,"details": {"color": "green", "size": "L"}},{"item_id": "D4","quantity": 3,"details": {"color": "yellow", "size": "M"}}]}}')
AS tt(id, resp)
, LATERAL FLATTEN(input => PARSE_JSON(tt.resp):order.items) AS lit

-- databricks sql:
SELECT
tt.id,
lit.value:details AS details
FROM VALUES
    (1, '{"order": {"id": 101,"items": [{"item_id": "A1","quantity": 2,"details": {"color": "red"}},{"item_id": "B2","quantity": 5,"details": {"color": "blue"}}]}}'),
    (2, '{"order": {"id": 202,"items": [{"item_id": "C3","quantity": 4,"details": {"color": "green", "size": "L"}},{"item_id": "D4","quantity": 3,"details": {"color": "yellow", "size": "M"}}]}}')
AS tt(id, resp)
, LATERAL VARIANT_EXPLODE(PARSE_JSON(tt.resp):order.items) AS lit;
