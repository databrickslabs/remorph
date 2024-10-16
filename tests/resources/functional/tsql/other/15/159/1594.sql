--Query type: DML
DECLARE @conversation_group_id UNIQUEIDENTIFIER;
SET @conversation_group_id = NEWID();

WITH temp_result_set AS (
    SELECT @conversation_group_id AS conversation_group_id
)

SELECT *
FROM temp_result_set
WHERE conversation_group_id = @conversation_group_id;