--Query type: DML
DECLARE @myXML xml = '<root><processing-instruction>PI</processing-instruction></root>';
SET @myXML.modify('delete //processing-instruction()');
WITH xmlCTE AS (
    SELECT @myXML AS xml
)
SELECT xml FROM xmlCTE;