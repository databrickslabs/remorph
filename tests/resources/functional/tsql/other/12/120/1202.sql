--Query type: DDL
CREATE XML SCHEMA COLLECTION HumanResources.HRResumeSchemaCollection
AS N'<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:ns="http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/Resume" targetNamespace="http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/Resume" elementFormDefault="qualified">
    <xs:element name="Skills">
        <xs:complexType>
            <xs:sequence>
                <xs:element name="Skill" minOccurs="0" maxOccurs="unbounded">
                    <xs:complexType>
                        <xs:attribute name="Level" type="xs:string" />
                    </xs:complexType>
                </xs:element>
            </xs:sequence>
        </xs:complexType>
    </xs:element>
</xs:schema>';

WITH EmployeeResumes AS (
    SELECT 'Doe' AS LName, 'John' AS FName, CONVERT(xml, '<ns:Skills xmlns:ns="http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/Resume"><ns:Skill ns:Level="Expert" /></ns:Skills>', 2) AS Resume
)
SELECT LName, FName, Resume FROM EmployeeResumes;

-- REMORPH CLEANUP: DROP XML SCHEMA COLLECTION HumanResources.HRResumeSchemaCollection;