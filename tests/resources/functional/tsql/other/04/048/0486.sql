-- tsql sql:
CREATE TABLE #TPC_H_Messages
(
    MessageID INT,
    MessageName VARCHAR(100)
);

CREATE TABLE #TPC_H_Contracts
(
    ContractID INT,
    ContractName VARCHAR(100),
    MessageID INT
);

CREATE TABLE #TPC_H_Queues
(
    QueueID INT,
    QueueName VARCHAR(100)
);

CREATE TABLE #TPC_H_Services
(
    ServiceID INT,
    ServiceName VARCHAR(100),
    QueueID INT,
    ContractID INT
);

INSERT INTO #TPC_H_Messages (MessageID, MessageName)
VALUES
    (1, 'TPC_H_Message'),
    (2, 'TPC_H_Message_Sent');

INSERT INTO #TPC_H_Contracts (ContractID, ContractName, MessageID)
VALUES
    (1, 'TPC_H_Contract', 1);

INSERT INTO #TPC_H_Queues (QueueID, QueueName)
VALUES
    (1, 'dbo.TPC_H_Queue');

INSERT INTO #TPC_H_Services (ServiceID, ServiceName, QueueID, ContractID)
VALUES
    (1, 'TPC_H_Service', 1, 1);

SELECT *
FROM #TPC_H_Messages;

SELECT *
FROM #TPC_H_Contracts;

SELECT *
FROM #TPC_H_Queues;

SELECT *
FROM #TPC_H_Services;

DROP TABLE #TPC_H_Messages;

DROP TABLE #TPC_H_Contracts;

DROP TABLE #TPC_H_Queues;

DROP TABLE #TPC_H_Services;
