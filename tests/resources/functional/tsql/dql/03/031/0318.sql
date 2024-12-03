--Query type: DQL
WITH CustomerCTE AS (SELECT c_name, c_birthdate FROM customer), ProspectiveBuyerCTE AS (SELECT c_name, c_birthdate FROM customer) SELECT a.c_name, a.c_birthdate FROM CustomerCTE AS a WHERE EXISTS (SELECT * FROM ProspectiveBuyerCTE AS b WHERE (a.c_name = b.c_name) AND (a.c_birthdate = b.c_birthdate))
