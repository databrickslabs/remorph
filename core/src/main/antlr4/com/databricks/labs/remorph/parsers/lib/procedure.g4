/*
Universal grammar for SQL stored procedure declarations
 */




parser grammar procedure;

// Snowflake specific
// TODO: Reconcile with TSQL and SQL/PSM

alterProcedure:
    ALTER PROCEDURE (IF EXISTS)? id LPAREN dataTypeList? RPAREN RENAME TO id
    | ALTER PROCEDURE (IF EXISTS)? id LPAREN dataTypeList? RPAREN SET (
        COMMENT EQ string
    )
    | ALTER PROCEDURE (IF EXISTS)? id LPAREN dataTypeList? RPAREN UNSET COMMENT
    | ALTER PROCEDURE (IF EXISTS)? id LPAREN dataTypeList? RPAREN EXECUTE AS (
        CALLER
        | OWNER
    )
;

createProcedure:
    CREATE (OR REPLACE)? PROCEDURE dotIdentifier LPAREN (
        procArgDecl (COMMA procArgDecl)*
    )? RPAREN RETURNS (dataType | table) (NOT? NULL)? LANGUAGE id (
        CALLED ON NULL INPUT
        | RETURNS NULL ON NULL INPUT
        | STRICT
    )? (VOLATILE | IMMUTABLE)? // Note: VOLATILE and IMMUTABLE are deprecated.
    (COMMENT EQ string)? executeAs? AS procedureDefinition
    | CREATE (OR REPLACE)? SECURE? PROCEDURE dotIdentifier LPAREN (
        procArgDecl (COMMA procArgDecl)*
    )? RPAREN RETURNS dataType (NOT? NULL)? LANGUAGE id (
        CALLED ON NULL INPUT
        | RETURNS NULL ON NULL INPUT
        | STRICT
    )? (VOLATILE | IMMUTABLE)? // Note: VOLATILE and IMMUTABLE are deprecated.
    (COMMENT EQ string)? executeAs? AS procedureDefinition
    | CREATE (OR REPLACE)? SECURE? PROCEDURE dotIdentifier LPAREN (
        procArgDecl (COMMA procArgDecl)*
    )? RPAREN RETURNS (dataType (NOT? NULL)? | table) LANGUAGE id RUNTIME_VERSION EQ string (
        IMPORTS EQ LPAREN stringList RPAREN
    )? PACKAGES EQ LPAREN stringList RPAREN HANDLER EQ string
    //            ( CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT )?
    //            ( VOLATILE | IMMUTABLE )? // Note: VOLATILE and IMMUTABLE are deprecated.
    (COMMENT EQ string)? executeAs? AS procedureDefinition
;

procArgDecl: id dataType (DEFAULT expr)?;

dropProcedure:
    DROP PROCEDURE (IF EXISTS)? dotIdentifier (
        COMMA dotIdentifier
    )* (LPAREN ( dataType (COMMA dataType)*)? RPAREN)? SEMI?
;

procedureDefinition:
    DOLLAR_STRING
    | declareCommand? BEGIN procStatement* END SEMI?
;

assign:
    LET? id (dataType | RESULTSET)? (ASSIGN | DEFAULT) expr SEMI # assignVariable
    | LET? id CURSOR FOR (selectStatement | id) SEMI             # assignCursor
;

// TSQL

createOrAlterProcedure: (
        (CREATE (OR (ALTER | REPLACE))?)
        | ALTER
    ) PROCEDURE dotIdentifier (SEMI INT)? (
        LPAREN? procedureParam (COMMA procedureParam)* RPAREN?
    )? (WITH procedureOption (COMMA procedureOption)*)? (
        FOR REPLICATION
    )? AS (EXTERNAL NAME dotIdentifier | sqlClauses*)
;

procedureParamDefaultValue:
    NULL
    | DEFAULT
    | constant
    | LOCAL_ID
;

procedureParam:
    LOCAL_ID AS? (id DOT)? dataType VARYING? (
        EQ procedureParamDefaultValue
    )? (OUT | OUTPUT | READONLY)?
;

procedureOption: executeAs | genericOption;

procStatement:
    declareCommand
    | assign
    | returnStatement
    | sqlClauses
;

// -----------------------------------------------------------
// SQL/PSM is for Spark, GoogleSQL, mySQL, Teradata, DB2
// The SQL/PSM standard is extended here to cover TSQL, Snowflake and other dialects in the future

returnStatement: RETURN expr SEMI;

// see https://docs.snowflake.com/en/sql-reference/snowflake-scripting/declare
declareCommand: DECLARE declareElement+;

declareElement:
    id dataType SEMI                                   # declareSimple
    | id dataType (DEFAULT | EQ) expr SEMI             # declareWithDefault
    | id CURSOR FOR expr SEMI                          # declareCursorElement
    | id RESULTSET ((ASSIGN | DEFAULT) expr)? SEMI     # declareResultSet
    | id EXCEPTION LPAREN INT COMMA string RPAREN SEMI # declareException
;

// TODO: Complete definition of SQL/PSM rules