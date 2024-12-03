--Query type: DDL
CREATE XML SCHEMA COLLECTION OrderDescriptionSchemaCollection
AS
'<xsd:schema targetNamespace="https://schemas.microsoft.com/sqlserver/2004/07/adventure-works/OrderModelDesc" xmlns="http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/OrderModelDesc" elementFormDefault="qualified" xmlns:xsd="http://www.w3.org/2001/XMLSchema" >
    <xsd:element name="OrderDescription" >
        <xsd:complexType>
            <xsd:sequence>
                <xsd:element name="OrderID" type="xsd:string" />
                <xsd:element name="OrderDate" type="xsd:string" />
            </xsd:sequence>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
<xs:schema targetNamespace="https://schemas.microsoft.com/sqlserver/2004/07/adventure-works/OrderModelWarrAndMain" xmlns="http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/OrderModelWarrAndMain" elementFormDefault="qualified" xmlns:mstns="https://tempuri.org/XMLSchema.xsd" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:wm="https://schemas.microsoft.com/sqlserver/2004/07/adventure-works/OrderModelDesc" >
    <xs:import namespace="https://schemas.microsoft.com/sqlserver/2004/07/adventure-works/OrderModelDesc" />
    <xs:element name="OrderWarranty" type="OrderWarranty" />
    <xs:complexType name="OrderWarranty">
        <xs:sequence>
            <xs:element name="WarrantyPeriod" type="xs:string" />
            <xs:element name="Description" type="xs:string" />
        </xs:sequence>
    </xs:complexType>
</xs:schema>';
-- REMORPH CLEANUP: DROP XML SCHEMA COLLECTION OrderDescriptionSchemaCollection;
