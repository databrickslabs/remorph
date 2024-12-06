-- tsql sql:
CREATE XML SCHEMA COLLECTION MyNewSchemaCollection
AS N'<?xml version="1.0" encoding="utf-8"?><xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"><xs:element name="root"><xs:complexType><xs:sequence><xs:element name="person" maxOccurs="unbounded"><xs:complexType><xs:sequence><xs:element name="name" type="xs:string"/><xs:element name="age" type="xs:integer"/></xs:sequence></xs:complexType></xs:element></xs:sequence></xs:complexType></xs:element></xs:schema>';

SELECT *
FROM sys.xml_schema_collections
WHERE name = 'MyNewSchemaCollection';

-- REMORPH CLEANUP: DROP XML SCHEMA COLLECTION MyNewSchemaCollection;
