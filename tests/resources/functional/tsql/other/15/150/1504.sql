--Query type: DML
DECLARE @SubjectCustomer HIERARCHYID, @OldParent HIERARCHYID, @NewParent HIERARCHYID;

DECLARE @CustomerDemo TABLE (
    CustID HIERARCHYID,
    CustNode HIERARCHYID
);

INSERT INTO @CustomerDemo (CustID, CustNode)
VALUES ('/1/1/', '/1/1/'), ('/1/2/', '/1/2/'), ('/1/3/', '/1/3/');

SELECT @SubjectCustomer = CustNode FROM @CustomerDemo WHERE CustID = '/1/1/';
SELECT @OldParent = CustNode FROM @CustomerDemo WHERE CustID = '/1/2/';
SELECT @NewParent = CustNode FROM @CustomerDemo WHERE CustID = '/1/3/';

UPDATE @CustomerDemo
SET CustNode = @SubjectCustomer.GetReparentedValue(@OldParent, @NewParent)
WHERE CustNode = @SubjectCustomer;

SELECT CustNode.ToString() AS Current_CustNode_AS_Text, CustID, CustNode
FROM @CustomerDemo
WHERE CustID = '/1/1/';

-- REMORPH CLEANUP: DROP TABLE @CustomerDemo;