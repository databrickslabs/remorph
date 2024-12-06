-- tsql sql:
ALTER TABLE customer
ADD CONSTRAINT idx_customer_search UNIQUE NONCLUSTERED (c_acctbal, c_phone, c_address, c_comment)
WITH (ONLINE = ON);
