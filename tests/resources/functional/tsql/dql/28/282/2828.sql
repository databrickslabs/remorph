--Query type: DQL
WITH xml_data AS ( SELECT TRY_CONVERT(xml, CONVERT(varchar(10), 4)) AS xml_result ) SELECT xml_result AS xml_output FROM xml_data