-- Because of the let command allows LET? it means that error recovery can't happen easily in Snowflake
-- because teh parser sees everything as valid.
-- TODO: TRy to rejig the parser so that error recovery can work athe top level batch
-- snowflake sql:
* ;
SELECT 1 ;
SELECT A B FROM C ;

-- databricks sql:
/* The following issues were detected:

   Unparsed input - ErrorNode encountered
    Unparsable text: '*' was unexpected while parsing a Snowflake batch
    expecting one of: $Identifier, End of batch, Identifier, Select Statement, Statement, '""', '(', 'BODY', 'CALL', 'CHARACTER', 'CURRENT_TIME', 'DECLARE'...
    Unparsable text: *
    Unparsable text: ;
    Unparsable text: SELECT
    Unparsable text: 1
    Unparsable text: ;
    Unparsable text: SELECT
    Unparsable text: A
    Unparsable text: B
    Unparsable text: FROM
    Unparsable text: C
    Unparsable text: ;
    Unparsable text: parser recovered by ignoring: * ;
    SELECT 1 ;
    SELECT A B FROM C ;
 */
