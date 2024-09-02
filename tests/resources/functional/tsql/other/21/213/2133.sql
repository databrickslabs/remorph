--Query type: DCL
CREATE TABLE CustomerSeq (Id INT, Name VARCHAR(50));
INSERT INTO CustomerSeq (Id, Name)
VALUES (1, 'Customer'), (2, 'Order');
GRANT UPDATE ON CustomerSeq TO [TPC_H\User];
SELECT * FROM CustomerSeq;
-- REMORPH CLEANUP: DROP TABLE CustomerSeq;