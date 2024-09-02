--Query type: DQL
SELECT BIT_COUNT(0x123456) AS BitCount FROM (VALUES (0x123456)) AS BitCountTable(BitString);