--Query type: DQL
SELECT Customer_Key = IDENTITY(int, 1, 1) INTO Customer_Dim FROM (VALUES ('Customer#0001', 'Smith'), ('Customer#0002', 'Johnson')) AS Customer_Source (Customer_ID, Customer_Name);