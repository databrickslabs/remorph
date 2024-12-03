--Query type: DQL
WITH temp_result AS (
    SELECT '/1/1/3/' AS StringValue, 0x5ADE AS hierarchyidValue
)
SELECT hierarchyid::Parse(StringValue) AS hierarchyidRepresentation, hierarchyidValue.ToString() AS StringRepresentation
FROM temp_result;
