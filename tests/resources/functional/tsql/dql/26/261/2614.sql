--Query type: DQL
SELECT FirstName, LastName, BaseRate, BaseRate * 40 AS GrossPay FROM (VALUES ('John', 'Doe', 50000.0), ('Jane', 'Doe', 60000.0), ('Bob', 'Smith', 70000.0)) AS Employee(FirstName, LastName, BaseRate) ORDER BY LastName;
