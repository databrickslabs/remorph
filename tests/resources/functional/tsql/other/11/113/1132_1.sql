-- tsql sql:
DECLARE @RevokeStatement nvarchar(max);
SELECT @RevokeStatement = 'REVOKE SELECT ON SCHEMA :: ' + SchemaName + ' TO ' + UserName + ';
FROM (
    VALUES ('Marketing', 'MarketingTeam')
) AS Permissions(SchemaName, UserName);
EXEC sp_executesql @RevokeStatement;
