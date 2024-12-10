-- tsql sql:
CREATE PROCEDURE tpch.get_linked_resources
AS
BEGIN
    SELECT *
    FROM (
        VALUES ('resource1', 'link1'),
               ('resource2', 'link2')
    ) AS linked_resources (resource, link);
END;
EXEC tpch.get_linked_resources;
