--Query type: DQL
SELECT xCol.value('(//phone)[1]', 'NVARCHAR(50)') AS PhoneNumber FROM (VALUES (CONVERT(XML, '<customer><phone>123-456-7890</phone></customer>'))) AS T(xCol);
