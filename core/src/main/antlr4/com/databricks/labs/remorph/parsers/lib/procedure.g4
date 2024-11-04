/*
Universal grammar for SQL stored procedure declarations
 */
parser grammar procedure;


// Snowflake

alterProcedure
    : ALTER PROCEDURE (IF EXISTS)? id L_PAREN dataTypeList? R_PAREN RENAME TO id
    | ALTER PROCEDURE (IF EXISTS)? id L_PAREN dataTypeList? R_PAREN SET (COMMENT EQ string)
    | ALTER PROCEDURE (IF EXISTS)? id L_PAREN dataTypeList? R_PAREN UNSET COMMENT
    | ALTER PROCEDURE (IF EXISTS)? id L_PAREN dataTypeList? R_PAREN EXECUTE AS (CALLER | OWNER)
    ;

createProcedure
    : CREATE (OR REPLACE)? PROCEDURE dotIdentifier L_PAREN (argDecl (COMMA argDecl)*)? R_PAREN RETURNS (
        dataType
        | table_
    ) notNull? LANGUAGE SQL (CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT)? (
        VOLATILE
        | IMMUTABLE
    )? // Note: VOLATILE and IMMUTABLE are deprecated.
    (COMMENT EQ string)? executaAs? AS procedureDefinition
    | CREATE (OR REPLACE)? SECURE? PROCEDURE dotIdentifier L_PAREN (argDecl (COMMA argDecl)*)? R_PAREN RETURNS dataType notNull? LANGUAGE JAVASCRIPT (
        CALLED ON NULL INPUT
        | RETURNS NULL ON NULL INPUT
        | STRICT
    )? (VOLATILE | IMMUTABLE)? // Note: VOLATILE and IMMUTABLE are deprecated.
    (COMMENT EQ string)? executaAs? AS procedureDefinition
    | CREATE (OR REPLACE)? SECURE? PROCEDURE dotIdentifier L_PAREN (argDecl (COMMA argDecl)*)? R_PAREN RETURNS (
        dataType notNull?
        | TABLE L_PAREN (colDecl (COMMA colDecl)*)? R_PAREN
    ) LANGUAGE PYTHON RUNTIME_VERSION EQ string (IMPORTS EQ L_PAREN stringList R_PAREN)? PACKAGES EQ L_PAREN stringList R_PAREN HANDLER EQ string
    //            ( CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT )?
    //            ( VOLATILE | IMMUTABLE )? // Note: VOLATILE and IMMUTABLE are deprecated.
    (COMMENT EQ string)? executaAs? AS procedureDefinition
    ;

dropProcedure: DROP PROCEDURE (IF EXISTS)? dotIdentifier argTypes
    ;

procedureDefinition: DOLLAR_STRING | declareCommand? BEGIN procStatement+ END SEMI
    ;


// TSQL

createOrAlterProcedure
    : ((CREATE (OR (ALTER | REPLACE))?) | ALTER) proc = (PROC | PROCEDURE) dotIdentifier (SEMI INT)? (
        LPAREN? procedureParam (COMMA procedureParam)* RPAREN?
    )? (WITH procedureOption (COMMA procedureOption)*)? (FOR REPLICATION)? AS (
          EXTERNAL NAME dotIdentifier
        | sqlClauses*
    )
    ;


procedureParamDefaultValue: NULL | DEFAULT | constant | LOCAL_ID
    ;

procedureParam
    : LOCAL_ID AS? (id DOT)? dataType VARYING? (EQ procedureParamDefaultValue)? (
        OUT
        | OUTPUT
        | READONLY
    )?
    ;

procedureOption: executeClause | genericOption
    ;

dropProcedure
    : DROP proc = (PROC | PROCEDURE) (IF EXISTS)? dotIdentifier (COMMA dotIdentifier)* SEMI?
    ;
