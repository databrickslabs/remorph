/*
Snowflake Database grammar.
The MIT License (MIT).

Copyright (c) 2022, Michał Lorek.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
*/

// =================================================================================
// Please reformat the grammr file before a change commit. See remorph/core/README.md
// For formatting, see: https://github.com/mike-lischke/antlr-format/blob/main/doc/formatting.md
// $antlr-format alignColons hanging
// $antlr-format columnLimit 150
// $antlr-format alignSemicolons hanging
// $antlr-format alignTrailingComments true
// =================================================================================
parser grammar SnowflakeParser;

import procedure, commonparse;

options {
    tokenVocab = SnowflakeLexer;
}

// ============== Dialect compatibiltiy rules ==============
// The following rules provide substitutes for grammar rules referenced in the procedure.g4 grammar, that
// we do not have real equivalents for in this gramamr.
// Over time, as we homogonize more and more of the dialect grammars, these rules will be removed.

// TODO: We will move genericOption into a parsercommon.g4 and reference it in all dialects for common option processing
// For now, this rule is not used within the Snowflake rules, but it will be
genericOption: ID EQ (string | INT | trueFalse | jsonLiteral)
    ;

// ======================================================

snowflakeFile: SEMI* batch? EOF
    ;

batch: (sqlClauses SEMI*)+
    ;

sqlClauses
    : ddlCommand
    | dmlCommand
    | showCommand
    | useCommand
    | describeCommand
    | otherCommand
    | snowSqlCommand
    ;

ddlCommand: alterCommand | createCommand | dropCommand | undropCommand
    ;

dmlCommand
    : queryStatement
    | insertStatement
    | insertMultiTableStatement
    | updateStatement
    | deleteStatement
    | mergeStatement
    ;

insertStatement
    : INSERT OVERWRITE? INTO dotIdentifier (LPAREN ids += id (COMMA ids += id)* RPAREN)? (
        valuesTableBody
        | queryStatement
    )
    ;

insertMultiTableStatement
    : INSERT OVERWRITE? ALL intoClause2
    | INSERT OVERWRITE? (FIRST | ALL) (WHEN searchCondition THEN intoClause2+)+ (ELSE intoClause2)? subquery
    ;

intoClause2: INTO dotIdentifier (LPAREN columnList RPAREN)? valuesList?
    ;

valuesList: VALUES LPAREN valueItem (COMMA valueItem)* RPAREN
    ;

valueItem: columnName | DEFAULT | NULL
    ;

mergeStatement: MERGE INTO tableRef USING tableSource ON searchCondition mergeCond
    ;

mergeCond: (mergeCondMatch | mergeCondNotMatch)+
    ;

mergeCondMatch: (WHEN MATCHED (AND searchCondition)? THEN mergeUpdateDelete)
    ;

mergeCondNotMatch: WHEN NOT MATCHED (AND searchCondition)? THEN mergeInsert
    ;

mergeUpdateDelete: UPDATE SET setColumnValue (COMMA setColumnValue)* | DELETE
    ;

mergeInsert: INSERT ((LPAREN columnList RPAREN)? VALUES LPAREN exprList RPAREN)?
    ;

updateStatement
    : UPDATE tableRef SET setColumnValue (COMMA setColumnValue)* (FROM tableSources)? (
        WHERE searchCondition
    )?
    ;

setColumnValue: columnName EQ expr
    ;

tableRef: dotIdentifier asAlias?
    ;

tableOrQuery: tableRef | LPAREN subquery RPAREN asAlias?
    ;

tablesOrQueries: tableOrQuery (COMMA tableOrQuery)*
    ;

deleteStatement: DELETE FROM tableRef (USING tablesOrQueries)? (WHERE searchCondition)?
    ;

otherCommand
    : copyIntoTable
    | copyIntoLocation
    | comment
    | commit
    | executeImmediate
    | executeTask
    | explain
    | getDml
    | grantOwnership
    | grantToRole
    | grantToShare
    | grantRole
    | list
    | put
    | remove
    | revokeFromRole
    | revokeFromShare
    | revokeRole
    | rollback
    | set
    | truncateMaterializedView
    | truncateTable
    | unset
    | call
    | beginTxn
    | declareCommand
    | let
    ;

snowSqlCommand: SQLCOMMAND
    ;

beginTxn: BEGIN (WORK | TRANSACTION)? (NAME id)? | START TRANSACTION ( NAME id)?
    ;

copyIntoTable
    : COPY INTO dotIdentifier FROM (tableStage | userStage | namedStage | externalLocation) files? pattern? fileFormat? copyOptions* (
        VALIDATION_MODE EQ (RETURN_N_ROWS | RETURN_ERRORS | RETURN_ALL_ERRORS)
    )?
    //
    /* Data load with transformation */
    | COPY INTO dotIdentifier (LPAREN columnList RPAREN)? FROM LPAREN SELECT selectList FROM (
        tableStage
        | userStage
        | namedStage
    ) RPAREN files? pattern? fileFormat? copyOptions*
    ;

externalLocation
    : string
    //(for Amazon S3)
    //'s3://<bucket>[/<path>]'
    //        ( ( STORAGE_INTEGRATION EQ id_ )?
    //        | ( CREDENTIALS EQ LPAREN ( AWS_KEY_ID EQ string AWS_SECRET_KEY EQ string ( AWS_TOKEN EQ string )? ) RPAREN )?
    //        )?
    //        [ ENCRYPTION = ( [ TYPE = 'AWS_CSE' ] [ MASTER_KEY = '<string>' ] |
    //                   [ TYPE = 'AWS_SSE_S3' ] |
    //                   [ TYPE = 'AWS_SSE_KMS' [ KMS_KEY_ID = '<string>' ] ] |
    //                   [ TYPE = 'NONE' ] ) ]
    //
    // (for Google Cloud Storage)
    //'gcs://<bucket>[/<path>]'
    //        ( STORAGE_INTEGRATION EQ id_ )?
    //[ ENCRYPTION = ( [ TYPE = 'GCS_SSE_KMS' ] [ KMS_KEY_ID = '<string>' ] | [ TYPE = 'NONE' ] ) ]
    //
    // (for Microsoft Azure)
    //'azure://<account>.blob.core.windows.net/<container>[/<path>]'
    //        (   ( STORAGE_INTEGRATION EQ id_ )?
    //            | ( CREDENTIALS EQ LPAREN ( AZURE_SAS_TOKEN EQ string ) RPAREN )
    //        )?
    //[ ENCRYPTION = ( [ TYPE = { 'AZURE_CSE' | 'NONE' } ] [ MASTER_KEY = '<string>' ] ) ]
    ;

files: FILES EQ LPAREN string (COMMA string)* RPAREN
    ;

fileFormat: FILE_FORMAT EQ LPAREN (formatName | formatType) RPAREN
    ;

formatName: FORMAT_NAME EQ string
    ;

formatType: TYPE EQ typeFileformat formatTypeOptions*
    ;

let
    // variable and resultset are covered under the same visitor since expr is common
    : LET id (dataType | RESULTSET)? (ASSIGN | DEFAULT) expr SEMI # letVariableAssignment
    | LET id CURSOR FOR (selectStatement | id) SEMI               # letCursor
    ;

stageFileFormat
    : STAGE_FILE_FORMAT EQ LPAREN FORMAT_NAME EQ string
    | TYPE EQ typeFileformat formatTypeOptions+ RPAREN
    ;

copyIntoLocation
    : COPY INTO (tableStage | userStage | namedStage | externalLocation) FROM (
        dotIdentifier
        | LPAREN queryStatement RPAREN
    ) partitionBy? fileFormat? copyOptions? (VALIDATION_MODE EQ RETURN_ROWS)? HEADER?
    ;

comment
    : COMMENT (IF EXISTS)? ON objectTypeName dotIdentifier functionSignature? IS string
    | COMMENT (IF EXISTS)? ON COLUMN dotIdentifier IS string
    ;

functionSignature: LPAREN dataTypeList? RPAREN
    ;

commit: COMMIT WORK?
    ;

executeImmediate
    : EXECUTE IMMEDIATE (string | id | LOCAL_ID) (USING LPAREN id (COMMA id)* RPAREN)?
    ;

executeTask: EXECUTE TASK dotIdentifier
    ;

explain: EXPLAIN (USING (TABULAR | JSON | id))? sqlClauses
    ;

parallel: PARALLEL EQ INT
    ;

getDml: GET (namedStage | userStage | tableStage) string parallel? pattern?
    ;

grantOwnership
    : GRANT OWNERSHIP (
        ON (
            objectTypeName dotIdentifier
            | ALL objectTypePlural IN ( DATABASE id | SCHEMA schemaName)
        )
        | ON FUTURE objectTypePlural IN ( DATABASE id | SCHEMA schemaName)
    ) TO ROLE id (( REVOKE | COPY) CURRENT GRANTS)?
    ;

grantToRole
    : GRANT (
        ( globalPrivileges | ALL PRIVILEGES?) ON ACCOUNT
        | (accountObjectPrivileges | ALL PRIVILEGES?) ON (
            USER
            | RESOURCE MONITOR
            | WAREHOUSE
            | DATABASE
            | INTEGRATION
        ) dotIdentifier
        | (schemaPrivileges | ALL PRIVILEGES?) ON (SCHEMA schemaName | ALL SCHEMAS IN DATABASE id)
        | ( schemaPrivileges | ALL PRIVILEGES?) ON FUTURE SCHEMAS IN DATABASE id
        | (schemaObjectPrivileges | ALL PRIVILEGES?) ON (
            objectType dotIdentifier
            | ALL objectTypePlural IN ( DATABASE id | SCHEMA schemaName)
        )
        | (schemaObjectPrivileges | ALL PRIVILEGES?) ON FUTURE objectTypePlural IN (
            DATABASE id
            | SCHEMA schemaName
        )
    ) TO ROLE? id (WITH GRANT OPTION)?
    ;

globalPrivileges: globalPrivilege (COMMA globalPrivilege)*
    ;

globalPrivilege
    : CREATE (
        ACCOUNT
        | DATA EXCHANGE LISTING
        | DATABASE
        | INTEGRATION
        | NETWORK POLICY
        | ROLE
        | SHARE
        | USER
        | WAREHOUSE
    )
    | (
        APPLY MASKING POLICY
        | APPLY ROW ACCESS POLICY
        | APPLY SESSION POLICY
        | APPLY TAG
        | ATTACH POLICY
    )
    | (
        EXECUTE TASK
        | IMPORT SHARE
        | MANAGE GRANTS
        | MONITOR ( EXECUTION | USAGE)
        | OVERRIDE SHARE RESTRICTIONS
    )
    ;

accountObjectPrivileges: accountObjectPrivilege (COMMA accountObjectPrivilege)*
    ;

accountObjectPrivilege
    : MONITOR
    | MODIFY
    | USAGE
    | OPERATE
    | CREATE SCHEMA
    | IMPORTED PRIVILEGES
    | USE_ANY_ROLE
    ;

schemaPrivileges: schemaPrivilege (COMMA schemaPrivilege)*
    ;

schemaPrivilege
    : MODIFY
    | MONITOR
    | USAGE
    | CREATE (
        TABLE
        | EXTERNAL TABLE
        | VIEW
        | MATERIALIZED VIEW
        | MASKING POLICY
        | ROW ACCESS POLICY
        | SESSION POLICY
        | TAG
        | SEQUENCE
        | FUNCTION
        | PROCEDURE
        | FILE FORMAT
        | STAGE
        | PIPE
        | STREAM
        | TASK
    )
    | ADD SEARCH OPTIMIZATION
    ;

schemaObjectPrivileges: schemaObjectPrivilege (COMMA schemaObjectPrivilege)*
    ;

schemaObjectPrivilege
    : SELECT
    | INSERT
    | UPDATE
    | DELETE
    | TRUNCATE
    | REFERENCES
    | USAGE
    | READ (COMMA WRITE)?
    | MONITOR
    | OPERATE
    | APPLY
    ;

grantToShare
    : GRANT objectPrivilege ON (
        DATABASE id
        | SCHEMA id
        | FUNCTION id
        | ( TABLE dotIdentifier | ALL TABLES IN SCHEMA schemaName)
        | VIEW id
    ) TO SHARE id
    ;

objectPrivilege: USAGE | SELECT | REFERENCE_USAGE
    ;

grantRole: GRANT ROLE roleName TO (ROLE roleName | USER id)
    ;

roleName: systemDefinedRole | id
    ;

systemDefinedRole: ORGADMIN | ACCOUNTADMIN | SECURITYADMIN | USERADMIN | SYSADMIN | PUBLIC
    ;

list: LIST (userStage | tableStage | namedStage) pattern?
    ;

//  @~[/<path>]
userStage: AT TILDA stagePath?
    ;

//  @[<namespace>.]%<tableName>[/<path>]
tableStage: AT schemaName? MODULE id stagePath?
    ;

//  @[<namespace>.]<extStageName>[/<path>]
namedStage: AT dotIdentifier stagePath?
    ;

stagePath: DIVIDE (ID (DIVIDE ID)* DIVIDE?)?
    ;

put
    : PUT string (tableStage | userStage | namedStage) (PARALLEL EQ INT)? (
        AUTO_COMPRESS EQ trueFalse
    )? (
        SOURCE_COMPRESSION EQ (
            AUTO_DETECT
            | GZIP
            | BZ2
            | BROTLI
            | ZSTD
            | DEFLATE
            | RAW_DEFLATE
            | NONE
        )
    )? (OVERWRITE EQ trueFalse)?
    ;

remove: REMOVE (tableStage | userStage | namedStage) pattern?
    ;

revokeFromRole
    : REVOKE (GRANT OPTION FOR)? (
        ( globalPrivilege | ALL PRIVILEGES?) ON ACCOUNT
        | (accountObjectPrivileges | ALL PRIVILEGES?) ON (
            RESOURCE MONITOR
            | WAREHOUSE
            | DATABASE
            | INTEGRATION
        ) dotIdentifier
        | (schemaPrivileges | ALL PRIVILEGES?) ON (SCHEMA schemaName | ALL SCHEMAS IN DATABASE id)
        | (schemaPrivileges | ALL PRIVILEGES?) ON (FUTURE SCHEMAS IN DATABASE <dbName>)
        | (schemaObjectPrivileges | ALL PRIVILEGES?) ON (
            objectType dotIdentifier
            | ALL objectTypePlural IN SCHEMA schemaName
        )
        | (schemaObjectPrivileges | ALL PRIVILEGES?) ON FUTURE objectTypePlural IN (
            DATABASE id
            | SCHEMA schemaName
        )
    ) FROM ROLE? id cascadeRestrict?
    ;

revokeFromShare
    : REVOKE objectPrivilege ON (
        DATABASE id
        | SCHEMA schemaName
        | ( TABLE dotIdentifier | ALL TABLES IN SCHEMA schemaName)
        | ( VIEW dotIdentifier | ALL VIEWS IN SCHEMA schemaName)
    ) FROM SHARE id
    ;

revokeRole: REVOKE ROLE roleName FROM (ROLE roleName | USER id)
    ;

rollback: ROLLBACK WORK?
    ;

set: SET id EQ expr | SET LPAREN id (COMMA id)* RPAREN EQ LPAREN expr (COMMA expr)* RPAREN
    ;

truncateMaterializedView: TRUNCATE MATERIALIZED VIEW dotIdentifier
    ;

truncateTable: TRUNCATE TABLE? (IF EXISTS)? dotIdentifier
    ;

unset: UNSET id | UNSET LPAREN id (COMMA id)* RPAREN
    ;

// alter commands
alterCommand
    : alterAccount
    | alterAlert
    | alterApiIntegration
    | alterConnection
    | alterDatabase
    | alterDynamicTable
    //| alterEventTable // uses ALTER TABLE stmt
    | alterExternalTable
    | alterFailoverGroup
    | alterFileFormat
    | alterFunction
    | alterMaskingPolicy
    | alterMaterializedView
    | alterNetworkPolicy
    | alterNotificationIntegration
    | alterPipe
    | alterProcedure
    | alterReplicationGroup
    | alterResourceMonitor
    | alterRole
    | alterRowAccessPolicy
    | alterSchema
    | alterSecurityIntegrationExternalOauth
    | alterSecurityIntegrationSnowflakeOauth
    | alterSecurityIntegrationSaml2
    | alterSecurityIntegrationScim
    | alterSequence
    | alterSession
    | alterSessionPolicy
    | alterShare
    | alterStage
    | alterStorageIntegration
    | alterStream
    | alterTable
    | alterTableAlterColumn
    | alterTag
    | alterTask
    | alterUser
    | alterView
    | alterWarehouse
    ;

accountParams
    : ALLOW_ID_TOKEN EQ trueFalse
    | CLIENT_ENCRYPTION_KEY_SIZE EQ INT
    | ENFORCE_SESSION_POLICY EQ trueFalse
    | EXTERNAL_OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST EQ trueFalse
    | INITIAL_REPLICATION_SIZE_LIMIT_IN_TB EQ INT
    | NETWORK_POLICY EQ string
    | PERIODIC_DATA_REKEYING EQ trueFalse
    | PREVENT_UNLOAD_TO_INLINE_URL EQ trueFalse
    | PREVENT_UNLOAD_TO_INTERNAL_STAGES EQ trueFalse
    | REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_CREATION EQ trueFalse
    | REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_OPERATION EQ trueFalse
    | SAML_IDENTITY_PROVIDER EQ jsonLiteral
    | SESSION_POLICY EQ string
    | SSO_LOGIN_PAGE EQ trueFalse
    ;

objectParams
    : DATA_RETENTION_TIME_IN_DAYS EQ INT
    | MAX_DATA_EXTENSION_TIME_IN_DAYS EQ INT
    | defaultDdlCollation
    | MAX_CONCURRENCY_LEVEL EQ INT
    | NETWORK_POLICY EQ string
    | PIPE_EXECUTION_PAUSED EQ trueFalse
    | SESSION_POLICY EQ string
    | STATEMENT_QUEUED_TIMEOUT_IN_SECONDS EQ INT
    | STATEMENT_TIMEOUT_IN_SECONDS EQ INT
    ;

defaultDdlCollation: DEFAULT_DDL_COLLATION_ EQ string
    ;

objectProperties
    : PASSWORD EQ string
    | LOGIN_NAME EQ string
    | DISPLAY_NAME EQ string
    | FIRST_NAME EQ string
    | MIDDLE_NAME EQ string
    | LAST_NAME EQ string
    | EMAIL EQ string
    | MUST_CHANGE_PASSWORD EQ trueFalse
    | DISABLED EQ trueFalse
    | DAYS_TO_EXPIRY EQ INT
    | MINS_TO_UNLOCK EQ INT
    | DEFAULT_WAREHOUSE EQ string
    | DEFAULT_NAMESPACE EQ string
    | DEFAULT_ROLE EQ string
    //| DEFAULT_SECONDARY_ROLES EQ LPAREN 'ALL' RPAREN
    | MINS_TO_BYPASS_MFA EQ INT
    | RSA_PUBLIC_KEY EQ string
    | RSA_PUBLIC_KEY_2 EQ string
    | (COMMENT EQ string)
    ;

sessionParams
    : ABORT_DETACHED_QUERY EQ trueFalse
    | AUTOCOMMIT EQ trueFalse
    | BINARY_INPUT_FORMAT EQ string
    | BINARY_OUTPUT_FORMAT EQ string
    | DATE_INPUT_FORMAT EQ string
    | DATE_OUTPUT_FORMAT EQ string
    | ERROR_ON_NONDETERMINISTIC_MERGE EQ trueFalse
    | ERROR_ON_NONDETERMINISTIC_UPDATE EQ trueFalse
    | JSON_INDENT EQ INT
    | LOCK_TIMEOUT EQ INT
    | QUERY_TAG EQ string
    | ROWS_PER_RESULTSET EQ INT
    | SIMULATED_DATA_SHARING_CONSUMER EQ string
    | STATEMENT_TIMEOUT_IN_SECONDS EQ INT
    | STRICT_JSON_OUTPUT EQ trueFalse
    | TIMESTAMP_DAY_IS_ALWAYS_24H EQ trueFalse
    | TIMESTAMP_INPUT_FORMAT EQ string
    | TIMESTAMP_LTZ_OUTPUT_FORMAT EQ string
    | TIMESTAMP_NTZ_OUTPUT_FORMAT EQ string
    | TIMESTAMP_OUTPUT_FORMAT EQ string
    | TIMESTAMP_TYPE_MAPPING EQ string
    | TIMESTAMP_TZ_OUTPUT_FORMAT EQ string
    | TIMEZONE EQ string
    | TIME_INPUT_FORMAT EQ string
    | TIME_OUTPUT_FORMAT EQ string
    | TRANSACTION_DEFAULT_ISOLATION_LEVEL EQ string
    | TWO_DIGIT_CENTURY_START EQ INT
    | UNSUPPORTED_DDL_ACTION EQ string
    | USE_CACHED_RESULT EQ trueFalse
    | WEEK_OF_YEAR_POLICY EQ INT
    | WEEK_START EQ INT
    ;

alterAccount: ALTER ACCOUNT alterAccountOpts
    ;

enabledTrueFalse: ENABLED EQ trueFalse
    ;

alterAlert
    : ALTER ALERT (IF EXISTS)? id (
        resumeSuspend
        | SET alertSetClause+
        | UNSET alertUnsetClause+
        | MODIFY CONDITION EXISTS LPAREN alertCondition RPAREN
        | MODIFY ACTION alertAction
    )
    ;

resumeSuspend: RESUME | SUSPEND
    ;

alertSetClause: WAREHOUSE EQ id | SCHEDULE EQ string | (COMMENT EQ string)
    ;

alertUnsetClause: WAREHOUSE | SCHEDULE | COMMENT
    ;

alterApiIntegration
    : ALTER API? INTEGRATION (IF EXISTS)? id SET (API_AWS_ROLE_ARN EQ string)? (
        AZURE_AD_APPLICATION_ID EQ string
    )? (API_KEY EQ string)? enabledTrueFalse? (API_ALLOWED_PREFIXES EQ LPAREN string RPAREN)? (
        API_BLOCKED_PREFIXES EQ LPAREN string RPAREN
    )? (COMMENT EQ string)?
    | ALTER API? INTEGRATION id setTags
    | ALTER API? INTEGRATION id unsetTags
    | ALTER API? INTEGRATION (IF EXISTS)? id UNSET apiIntegrationProperty (
        COMMA apiIntegrationProperty
    )*
    ;

apiIntegrationProperty: API_KEY | ENABLED | API_BLOCKED_PREFIXES | COMMENT
    ;

alterConnection: ALTER CONNECTION alterConnectionOpts
    ;

alterDatabase
    : ALTER DATABASE (IF EXISTS)? id RENAME TO id
    | ALTER DATABASE (IF EXISTS)? id SWAP WITH id
    | ALTER DATABASE (IF EXISTS)? id SET (DATA_RETENTION_TIME_IN_DAYS EQ INT)? (
        MAX_DATA_EXTENSION_TIME_IN_DAYS EQ INT
    )? defaultDdlCollation? (COMMENT EQ string)?
    | ALTER DATABASE id setTags
    | ALTER DATABASE id unsetTags
    | ALTER DATABASE (IF EXISTS)? id UNSET databaseProperty (COMMA databaseProperty)*
    | ALTER DATABASE id ENABLE REPLICATION TO ACCOUNTS accountIdList (IGNORE EDITION CHECK)?
    | ALTER DATABASE id DISABLE REPLICATION ( TO ACCOUNTS accountIdList)?
    | ALTER DATABASE id REFRESH
    // Database Failover
    | ALTER DATABASE id ENABLE FAILOVER TO ACCOUNTS accountIdList
    | ALTER DATABASE id DISABLE FAILOVER ( TO ACCOUNTS accountIdList)?
    | ALTER DATABASE id PRIMARY
    ;

databaseProperty
    : DATA_RETENTION_TIME_IN_DAYS
    | MAX_DATA_EXTENSION_TIME_IN_DAYS
    | DEFAULT_DDL_COLLATION_
    | COMMENT
    ;

accountIdList: id (COMMA id)*
    ;

alterDynamicTable: ALTER DYNAMIC TABLE id (resumeSuspend | REFRESH | SET WAREHOUSE EQ id)
    ;

alterExternalTable
    : ALTER EXTERNAL TABLE (IF EXISTS)? dotIdentifier REFRESH string?
    | ALTER EXTERNAL TABLE (IF EXISTS)? dotIdentifier ADD FILES LPAREN stringList RPAREN
    | ALTER EXTERNAL TABLE (IF EXISTS)? dotIdentifier REMOVE FILES LPAREN stringList RPAREN
    | ALTER EXTERNAL TABLE (IF EXISTS)? dotIdentifier SET (AUTO_REFRESH EQ trueFalse)? tagDeclList?
    | ALTER EXTERNAL TABLE (IF EXISTS)? dotIdentifier unsetTags
    //Partitions added and removed manually
    | ALTER EXTERNAL TABLE dotIdentifier (IF EXISTS)? ADD PARTITION LPAREN columnName EQ string (
        COMMA columnName EQ string
    )* RPAREN LOCATION string
    | ALTER EXTERNAL TABLE dotIdentifier (IF EXISTS)? DROP PARTITION LOCATION string
    ;

ignoreEditionCheck: IGNORE EDITION CHECK
    ;

replicationSchedule: REPLICATION_SCHEDULE EQ string
    ;

dbNameList: id (COMMA id)*
    ;

shareNameList: id (COMMA id)*
    ;

fullAcctList: fullAcct (COMMA fullAcct)*
    ;

alterFailoverGroup
    //Source Account
    : ALTER FAILOVER GROUP (IF EXISTS)? id RENAME TO id
    | ALTER FAILOVER GROUP (IF EXISTS)? id SET (OBJECT_TYPES EQ objectTypeList)? replicationSchedule?
    | ALTER FAILOVER GROUP (IF EXISTS)? id SET OBJECT_TYPES EQ objectTypeList
    //        ALLOWED_INTEGRATION_TYPES EQ <integrationTypeName> [ , <integrationTypeName> ... ] ]
    replicationSchedule?
    | ALTER FAILOVER GROUP (IF EXISTS)? id ADD dbNameList TO ALLOWED_DATABASES
    | ALTER FAILOVER GROUP (IF EXISTS)? id MOVE DATABASES dbNameList TO FAILOVER GROUP id
    | ALTER FAILOVER GROUP (IF EXISTS)? id REMOVE dbNameList FROM ALLOWED_DATABASES
    | ALTER FAILOVER GROUP (IF EXISTS)? id ADD shareNameList TO ALLOWED_SHARES
    | ALTER FAILOVER GROUP (IF EXISTS)? id MOVE SHARES shareNameList TO FAILOVER GROUP id
    | ALTER FAILOVER GROUP (IF EXISTS)? id REMOVE shareNameList FROM ALLOWED_SHARES
    | ALTER FAILOVER GROUP (IF EXISTS)? id ADD fullAcctList TO ALLOWED_ACCOUNTS ignoreEditionCheck?
    | ALTER FAILOVER GROUP (IF EXISTS)? id REMOVE fullAcctList FROM ALLOWED_ACCOUNTS
    //Target Account
    | ALTER FAILOVER GROUP (IF EXISTS)? id (REFRESH | PRIMARY | SUSPEND | RESUME)
    ;

alterFileFormat
    : ALTER FILE FORMAT (IF EXISTS)? id RENAME TO id
    | ALTER FILE FORMAT (IF EXISTS)? id SET (formatTypeOptions* (COMMENT EQ string)?)
    ;

alterFunction
    : alterFunctionSignature RENAME TO id
    | alterFunctionSignature SET (COMMENT EQ string)
    | alterFunctionSignature SET SECURE
    | alterFunctionSignature UNSET (SECURE | COMMENT)
    // External Functions
    | alterFunctionSignature SET API_INTEGRATION EQ id
    | alterFunctionSignature SET HEADERS EQ LPAREN headerDecl* RPAREN
    | alterFunctionSignature SET CONTEXT_HEADERS EQ LPAREN id* RPAREN
    | alterFunctionSignature SET MAX_BATCH_ROWS EQ INT
    | alterFunctionSignature SET COMPRESSION EQ compressionType
    | alterFunctionSignature SET (REQUEST_TRANSLATOR | RESPONSE_TRANSLATOR) EQ id
    | alterFunctionSignature UNSET (
        COMMENT
        | HEADERS
        | CONTEXT_HEADERS
        | MAX_BATCH_ROWS
        | COMPRESSION
        | SECURE
        | REQUEST_TRANSLATOR
        | RESPONSE_TRANSLATOR
    )
    ;

alterFunctionSignature: ALTER FUNCTION (IF EXISTS)? id LPAREN dataTypeList? RPAREN
    ;

dataTypeList: dataType (COMMA dataType)*
    ;

alterMaskingPolicy
    : ALTER MASKING POLICY (IF EXISTS)? id SET BODY ARROW expr
    | ALTER MASKING POLICY (IF EXISTS)? id RENAME TO id
    | ALTER MASKING POLICY (IF EXISTS)? id SET (COMMENT EQ string)
    ;

alterMaterializedView
    : ALTER MATERIALIZED VIEW id (
        RENAME TO id
        | CLUSTER BY LPAREN exprList RPAREN
        | DROP CLUSTERING KEY
        | resumeSuspend RECLUSTER?
        | SET ( SECURE? (COMMENT EQ string)?)
        | UNSET ( SECURE | COMMENT)
    )
    ;

alterNetworkPolicy: ALTER NETWORK POLICY alterNetworkPolicyOpts
    ;

alterNotificationIntegration
    : ALTER NOTIFICATION? INTEGRATION (IF EXISTS)? id SET enabledTrueFalse? cloudProviderParamsAuto (
        COMMENT EQ string
    )?
    // Push notifications
    | ALTER NOTIFICATION? INTEGRATION (IF EXISTS)? id SET enabledTrueFalse? cloudProviderParamsPush (
        COMMENT EQ string
    )?
    | ALTER NOTIFICATION? INTEGRATION id setTags
    | ALTER NOTIFICATION? INTEGRATION id unsetTags
    | ALTER NOTIFICATION? INTEGRATION (IF EXISTS) id UNSET (ENABLED | COMMENT)
    ;

alterPipe
    : ALTER PIPE (IF EXISTS)? id SET (objectProperties? (COMMENT EQ string)?)
    | ALTER PIPE id setTags
    | ALTER PIPE id unsetTags
    | ALTER PIPE (IF EXISTS)? id UNSET PIPE_EXECUTION_PAUSED EQ trueFalse
    | ALTER PIPE (IF EXISTS)? id UNSET COMMENT
    | ALTER PIPE (IF EXISTS)? id REFRESH (PREFIX EQ string)? (MODIFIED_AFTER EQ string)?
    ;

alterReplicationGroup
    //Source Account
    : ALTER REPLICATION GROUP (IF EXISTS)? id RENAME TO id
    | ALTER REPLICATION GROUP (IF EXISTS)? id SET (OBJECT_TYPES EQ objectTypeList)? (
        REPLICATION_SCHEDULE EQ string
    )?
    | ALTER REPLICATION GROUP (IF EXISTS)? id SET OBJECT_TYPES EQ objectTypeList ALLOWED_INTEGRATION_TYPES EQ integrationTypeName (
        COMMA integrationTypeName
    )* (REPLICATION_SCHEDULE EQ string)?
    | ALTER REPLICATION GROUP (IF EXISTS)? id ADD dbNameList TO ALLOWED_DATABASES
    | ALTER REPLICATION GROUP (IF EXISTS)? id MOVE DATABASES dbNameList TO REPLICATION GROUP id
    | ALTER REPLICATION GROUP (IF EXISTS)? id REMOVE dbNameList FROM ALLOWED_DATABASES
    | ALTER REPLICATION GROUP (IF EXISTS)? id ADD shareNameList TO ALLOWED_SHARES
    | ALTER REPLICATION GROUP (IF EXISTS)? id MOVE SHARES shareNameList TO REPLICATION GROUP id
    | ALTER REPLICATION GROUP (IF EXISTS)? id REMOVE shareNameList FROM ALLOWED_SHARES
    | ALTER REPLICATION GROUP (IF EXISTS)? id ADD accountIdList TO ALLOWED_ACCOUNTS ignoreEditionCheck?
    | ALTER REPLICATION GROUP (IF EXISTS)? id REMOVE accountIdList FROM ALLOWED_ACCOUNTS
    //Target Account
    | ALTER REPLICATION GROUP (IF EXISTS)? id REFRESH
    | ALTER REPLICATION GROUP (IF EXISTS)? id SUSPEND
    | ALTER REPLICATION GROUP (IF EXISTS)? id RESUME
    ;

creditQuota: CREDIT_QUOTA EQ INT
    ;

frequency: FREQUENCY EQ (MONTHLY | DAILY | WEEKLY | YEARLY | NEVER)
    ;

notifyUsers: NOTIFY_USERS EQ LPAREN id (COMMA id)* RPAREN
    ;

triggerDefinition: ON INT PERCENT DO (SUSPEND | SUSPEND_IMMEDIATE | NOTIFY)
    ;

alterResourceMonitor
    : ALTER RESOURCE MONITOR (IF EXISTS)? id (
        SET creditQuota? frequency? (START_TIMESTAMP EQ LPAREN string | IMMEDIATELY RPAREN)? (
            END_TIMESTAMP EQ string
        )?
    )? (notifyUsers ( TRIGGERS triggerDefinition (COMMA triggerDefinition)*)?)?
    ;

alterRole
    : ALTER ROLE (IF EXISTS)? id RENAME TO id
    | ALTER ROLE (IF EXISTS)? id SET (COMMENT EQ string)
    | ALTER ROLE (IF EXISTS)? id UNSET COMMENT
    | ALTER ROLE (IF EXISTS)? id setTags
    | ALTER ROLE (IF EXISTS)? id unsetTags
    ;

alterRowAccessPolicy
    : ALTER ROW ACCESS POLICY (IF EXISTS)? id SET BODY ARROW expr
    | ALTER ROW ACCESS POLICY (IF EXISTS)? id RENAME TO id
    | ALTER ROW ACCESS POLICY (IF EXISTS)? id SET (COMMENT EQ string)
    ;

alterSchema
    : ALTER SCHEMA (IF EXISTS)? schemaName RENAME TO schemaName
    | ALTER SCHEMA (IF EXISTS)? schemaName SWAP WITH schemaName
    | ALTER SCHEMA (IF EXISTS)? schemaName SET (
        (DATA_RETENTION_TIME_IN_DAYS EQ INT)? (MAX_DATA_EXTENSION_TIME_IN_DAYS EQ INT)? defaultDdlCollation? (
            COMMENT EQ string
        )?
    )
    | ALTER SCHEMA (IF EXISTS)? schemaName setTags
    | ALTER SCHEMA (IF EXISTS)? schemaName unsetTags
    | ALTER SCHEMA (IF EXISTS)? schemaName UNSET schemaProperty (COMMA schemaProperty)*
    | ALTER SCHEMA (IF EXISTS)? schemaName ( ENABLE | DISABLE) MANAGED ACCESS
    ;

schemaProperty
    : DATA_RETENTION_TIME_IN_DAYS
    | MAX_DATA_EXTENSION_TIME_IN_DAYS
    | DEFAULT_DDL_COLLATION_
    | COMMENT
    ;

alterSequence
    : ALTER SEQUENCE (IF EXISTS)? dotIdentifier RENAME TO dotIdentifier
    | ALTER SEQUENCE (IF EXISTS)? dotIdentifier SET? ( INCREMENT BY? EQ? INT)?
    | ALTER SEQUENCE (IF EXISTS)? dotIdentifier SET (
        orderNoorder? (COMMENT EQ string)
        | orderNoorder
    )
    | ALTER SEQUENCE (IF EXISTS)? dotIdentifier UNSET COMMENT
    ;

alterSecurityIntegrationExternalOauth
    : ALTER SECURITY? INTEGRATION (IF EXISTS) id SET (TYPE EQ EXTERNAL_OAUTH)? (
        ENABLED EQ trueFalse
    )? (EXTERNAL_OAUTH_TYPE EQ ( OKTA | id | PING_FEDERATE | CUSTOM))? (
        EXTERNAL_OAUTH_ISSUER EQ string
    )? (EXTERNAL_OAUTH_TOKEN_USER_MAPPING_CLAIM EQ (string | LPAREN stringList RPAREN))? (
        EXTERNAL_OAUTH_SNOWFLAKE_USER_MAPPING_ATTRIBUTE EQ string
    )? (EXTERNAL_OAUTH_JWS_KEYS_URL EQ string)?                           // For OKTA | PING_FEDERATE | CUSTOM
    (EXTERNAL_OAUTH_JWS_KEYS_URL EQ (string | LPAREN stringList RPAREN))? // For Azure
    (EXTERNAL_OAUTH_RSA_PUBLIC_KEY EQ string)? (EXTERNAL_OAUTH_RSA_PUBLIC_KEY_2 EQ string)? (
        EXTERNAL_OAUTH_BLOCKED_ROLES_LIST EQ LPAREN stringList RPAREN
    )? (EXTERNAL_OAUTH_ALLOWED_ROLES_LIST EQ LPAREN stringList RPAREN)? (
        EXTERNAL_OAUTH_AUDIENCE_LIST EQ LPAREN string RPAREN
    )? (EXTERNAL_OAUTH_ANY_ROLE_MODE EQ (DISABLE | ENABLE | ENABLE_FOR_PRIVILEGE))? (
        EXTERNAL_OAUTH_ANY_ROLE_MODE EQ string
    )? // Only for EXTERNAL_OAUTH_TYPE EQ CUSTOM
    | ALTER SECURITY? INTEGRATION (IF EXISTS)? id UNSET securityIntegrationExternalOauthProperty (
        COMMA securityIntegrationExternalOauthProperty
    )*
    | ALTER SECURITY? INTEGRATION id setTags
    | ALTER SECURITY? INTEGRATION id unsetTags
    ;

securityIntegrationExternalOauthProperty
    : ENABLED
    | NETWORK_POLICY
    | OAUTH_CLIENT_RSA_PUBLIC_KEY
    | OAUTH_CLIENT_RSA_PUBLIC_KEY_2
    | OAUTH_USE_SECONDARY_ROLES EQ (IMPLICIT | NONE)
    | COMMENT
    ;

alterSecurityIntegrationSnowflakeOauth
    : ALTER SECURITY? INTEGRATION (IF EXISTS)? id SET (TYPE EQ EXTERNAL_OAUTH)? enabledTrueFalse? (
        EXTERNAL_OAUTH_TYPE EQ ( OKTA | id | PING_FEDERATE | CUSTOM)
    )? (EXTERNAL_OAUTH_ISSUER EQ string)? (
        EXTERNAL_OAUTH_TOKEN_USER_MAPPING_CLAIM EQ (string | LPAREN stringList RPAREN)
    )? (EXTERNAL_OAUTH_SNOWFLAKE_USER_MAPPING_ATTRIBUTE EQ string)? (
        EXTERNAL_OAUTH_JWS_KEYS_URL EQ string
    )?                                                                     // For OKTA | PING_FEDERATE | CUSTOM
    (EXTERNAL_OAUTH_JWS_KEYS_URL EQ ( string | LPAREN stringList RPAREN))? // For Azure
    (EXTERNAL_OAUTH_RSA_PUBLIC_KEY EQ string)? (EXTERNAL_OAUTH_RSA_PUBLIC_KEY_2 EQ string)? (
        EXTERNAL_OAUTH_BLOCKED_ROLES_LIST EQ LPAREN stringList RPAREN
    )? (EXTERNAL_OAUTH_ALLOWED_ROLES_LIST EQ LPAREN stringList RPAREN)? (
        EXTERNAL_OAUTH_AUDIENCE_LIST EQ LPAREN string RPAREN
    )? (EXTERNAL_OAUTH_ANY_ROLE_MODE EQ DISABLE | ENABLE | ENABLE_FOR_PRIVILEGE)? (
        EXTERNAL_OAUTH_SCOPE_DELIMITER EQ string
    ) // Only for EXTERNAL_OAUTH_TYPE EQ CUSTOM
    | ALTER SECURITY? INTEGRATION (IF EXISTS)? id UNSET securityIntegrationSnowflakeOauthProperty (
        COMMA securityIntegrationSnowflakeOauthProperty
    )*
    | ALTER SECURITY? INTEGRATION id setTags
    | ALTER SECURITY? INTEGRATION id unsetTags
    ;

securityIntegrationSnowflakeOauthProperty: ENABLED | EXTERNAL_OAUTH_AUDIENCE_LIST
    ;

alterSecurityIntegrationSaml2
    : ALTER SECURITY? INTEGRATION (IF EXISTS)? id SET (TYPE EQ SAML2)? enabledTrueFalse? (
        SAML2_ISSUER EQ string
    )? (SAML2_SSO_URL EQ string)? (SAML2_PROVIDER EQ string)? (SAML2_X509_CERT EQ string)? (
        SAML2_SP_INITIATED_LOGIN_PAGE_LABEL EQ string
    )? (SAML2_ENABLE_SP_INITIATED EQ trueFalse)? (SAML2_SNOWFLAKE_X509_CERT EQ string)? (
        SAML2_SIGN_REQUEST EQ trueFalse
    )? (SAML2_REQUESTED_NAMEID_FORMAT EQ string)? (SAML2_POST_LOGOUT_REDIRECT_URL EQ string)? (
        SAML2_FORCE_AUTHN EQ trueFalse
    )? (SAML2_SNOWFLAKE_ISSUER_URL EQ string)? (SAML2_SNOWFLAKE_ACS_URL EQ string)?
    | ALTER SECURITY? INTEGRATION (IF EXISTS)? id UNSET ENABLED
    | ALTER SECURITY? INTEGRATION id setTags
    | ALTER SECURITY? INTEGRATION id unsetTags
    ;

alterSecurityIntegrationScim
    : ALTER SECURITY? INTEGRATION (IF EXISTS)? id SET (NETWORK_POLICY EQ string)? (
        SYNC_PASSWORD EQ trueFalse
    )? (COMMENT EQ string)?
    | ALTER SECURITY? INTEGRATION (IF EXISTS)? id UNSET securityIntegrationScimProperty (
        COMMA securityIntegrationScimProperty
    )*
    | ALTER SECURITY? INTEGRATION id setTags
    | ALTER SECURITY? INTEGRATION id unsetTags
    ;

securityIntegrationScimProperty: NETWORK_POLICY | SYNC_PASSWORD | COMMENT
    ;

alterSession: ALTER SESSION SET sessionParams | ALTER SESSION UNSET id (COMMA id)*
    ;

alterSessionPolicy
    : ALTER SESSION POLICY (IF EXISTS)? id (UNSET | SET) (SESSION_IDLE_TIMEOUT_MINS EQ INT)? (
        SESSION_UI_IDLE_TIMEOUT_MINS EQ INT
    )? (COMMENT EQ string)?
    | ALTER SESSION POLICY (IF EXISTS)? id RENAME TO id
    ;

alterShare
    : ALTER SHARE (IF EXISTS)? id (ADD | REMOVE) ACCOUNTS EQ id (COMMA id)* (
        SHARE_RESTRICTIONS EQ trueFalse
    )?
    | ALTER SHARE (IF EXISTS)? id ADD ACCOUNTS EQ id (COMMA id)* (SHARE_RESTRICTIONS EQ trueFalse)?
    | ALTER SHARE (IF EXISTS)? id SET (ACCOUNTS EQ id (COMMA id)*)? (COMMENT EQ string)?
    | ALTER SHARE (IF EXISTS)? id setTags
    | ALTER SHARE id unsetTags
    | ALTER SHARE (IF EXISTS)? id UNSET COMMENT
    ;

alterStorageIntegration
    : ALTER STORAGE? INTEGRATION (IF EXISTS)? id SET cloudProviderParams2? enabledTrueFalse? (
        STORAGE_ALLOWED_LOCATIONS EQ LPAREN stringList RPAREN
    )? (STORAGE_BLOCKED_LOCATIONS EQ LPAREN stringList RPAREN)? (COMMENT EQ string)?
    | ALTER STORAGE? INTEGRATION (IF EXISTS)? id setTags
    | ALTER STORAGE? INTEGRATION id unsetTags
    | ALTER STORAGE? INTEGRATION (IF EXISTS)? id UNSET (
        ENABLED
        | STORAGE_BLOCKED_LOCATIONS
        | COMMENT
    )
    //[ , ... ]
    ;

alterStream
    : ALTER STREAM (IF EXISTS)? id SET tagDeclList? (COMMENT EQ string)?
    | ALTER STREAM (IF EXISTS)? id setTags
    | ALTER STREAM id unsetTags
    | ALTER STREAM (IF EXISTS)? id UNSET COMMENT
    ;

alterTable
    : ALTER TABLE (IF EXISTS)? dotIdentifier RENAME TO dotIdentifier
    | ALTER TABLE (IF EXISTS)? dotIdentifier SWAP WITH dotIdentifier
    | ALTER TABLE (IF EXISTS)? dotIdentifier (
        clusteringAction
        | tableColumnAction
        | constraintAction
    )
    | ALTER TABLE (IF EXISTS)? dotIdentifier extTableColumnAction
    | ALTER TABLE (IF EXISTS)? dotIdentifier searchOptimizationAction
    | ALTER TABLE (IF EXISTS)? dotIdentifier SET stageFileFormat? (
        STAGE_COPY_OPTIONS EQ LPAREN copyOptions RPAREN
    )? (DATA_RETENTION_TIME_IN_DAYS EQ INT)? (MAX_DATA_EXTENSION_TIME_IN_DAYS EQ INT)? (
        CHANGE_TRACKING EQ trueFalse
    )? defaultDdlCollation? (COMMENT EQ string)?
    | ALTER TABLE (IF EXISTS)? dotIdentifier setTags
    | ALTER TABLE (IF EXISTS)? dotIdentifier unsetTags
    | ALTER TABLE (IF EXISTS)? dotIdentifier UNSET (
        DATA_RETENTION_TIME_IN_DAYS
        | MAX_DATA_EXTENSION_TIME_IN_DAYS
        | CHANGE_TRACKING
        | DEFAULT_DDL_COLLATION_
        | COMMENT
        |
    )
    //[ , ... ]
    | ALTER TABLE (IF EXISTS)? dotIdentifier ADD ROW ACCESS POLICY id ON columnListInParentheses
    | ALTER TABLE (IF EXISTS)? dotIdentifier DROP ROW ACCESS POLICY id
    | ALTER TABLE (IF EXISTS)? dotIdentifier DROP ROW ACCESS POLICY id COMMA ADD ROW ACCESS POLICY id ON columnListInParentheses
    | ALTER TABLE (IF EXISTS)? dotIdentifier DROP ALL ROW ACCESS POLICIES
    ;

clusteringAction
    : CLUSTER BY LPAREN exprList RPAREN
    | RECLUSTER ( MAX_SIZE EQ INT)? ( WHERE expr)?
    | resumeSuspend RECLUSTER
    | DROP CLUSTERING KEY
    ;

tableColumnAction
    : ADD COLUMN? (IF NOT EXISTS)? fullColDecl (COMMA fullColDecl)*
    | RENAME COLUMN columnName TO columnName
    | alterModify (
        LPAREN alterColumnClause (COLON alterColumnClause)* RPAREN
        | alterColumnClause (COLON alterColumnClause)*
    )
    | alterModify COLUMN columnName SET MASKING POLICY id (
        USING LPAREN columnName COMMA columnList RPAREN
    )? FORCE?
    | alterModify COLUMN columnName UNSET MASKING POLICY
    | alterModify columnSetTags (COMMA columnSetTags)*
    | alterModify columnUnsetTags (COMMA columnUnsetTags)*
    | DROP COLUMN? (IF EXISTS)? columnList
    //| DROP DEFAULT
    ;

alterColumnClause
    : COLUMN? columnName (
        DROP DEFAULT
        | SET DEFAULT dotIdentifier DOT NEXTVAL
        | ( SET? NOT NULL | DROP NOT NULL)
        | ( (SET DATA)? TYPE)? dataType
        | COMMENT string
        | UNSET COMMENT
    )
    ;

inlineConstraint
    : (CONSTRAINT id)? (
        (UNIQUE | primaryKey) commonConstraintProperties*
        | foreignKey REFERENCES dotIdentifier (LPAREN columnName RPAREN)? constraintProperties
    )
    ;

enforcedNotEnforced: NOT? ENFORCED
    ;

deferrableNotDeferrable: NOT? DEFERRABLE
    ;

initiallyDeferredOrImmediate: INITIALLY (DEFERRED | IMMEDIATE)
    ;

//TODO : Some properties are mutualy exclusive ie INITIALLY DEFERRED is not compatible with NOT DEFERRABLE
// also VALIDATE | NOVALIDATE need to be after ENABLE or ENFORCED. Lot of case to handle :)
commonConstraintProperties
    : enforcedNotEnforced (VALIDATE | NOVALIDATE)?
    | deferrableNotDeferrable
    | initiallyDeferredOrImmediate
    | ( ENABLE | DISABLE) ( VALIDATE | NOVALIDATE)?
    | RELY
    | NORELY
    ;

onUpdate: ON UPDATE onAction
    ;

onDelete: ON DELETE onAction
    ;

foreignKeyMatch: MATCH matchType = (FULL | PARTIAL | SIMPLE)
    ;

onAction: CASCADE | SET ( NULL | DEFAULT) | RESTRICT | NO ACTION
    ;

constraintProperties
    : commonConstraintProperties*
    | foreignKeyMatch
    | foreignKeyMatch? ( onUpdate onDelete? | onDelete onUpdate?)
    ;

extTableColumnAction
    : ADD COLUMN? columnName dataType AS LPAREN expr RPAREN
    | RENAME COLUMN columnName TO columnName
    | DROP COLUMN? columnList
    ;

constraintAction
    : ADD outOfLineConstraint
    | RENAME CONSTRAINT id TO id
    | alterModify (CONSTRAINT id | primaryKey | UNIQUE | foreignKey) columnListInParentheses enforcedNotEnforced? (
        VALIDATE
        | NOVALIDATE
    ) (RELY | NORELY)
    | DROP (CONSTRAINT id | primaryKey | UNIQUE | foreignKey) columnListInParentheses? cascadeRestrict?
    | DROP PRIMARY KEY
    ;

searchOptimizationAction
    : ADD SEARCH OPTIMIZATION (ON searchMethodWithTarget (COMMA searchMethodWithTarget)*)?
    | DROP SEARCH OPTIMIZATION (ON searchMethodWithTarget (COMMA searchMethodWithTarget)*)?
    ;

searchMethodWithTarget: (EQUALITY | SUBSTRING | GEO) LPAREN (STAR | expr) RPAREN
    ;

alterTableAlterColumn
    : ALTER TABLE dotIdentifier alterModify (
        LPAREN alterColumnDeclList RPAREN
        | alterColumnDeclList
    )
    | ALTER TABLE dotIdentifier alterModify COLUMN columnName SET MASKING POLICY id (
        USING LPAREN columnName COMMA columnList RPAREN
    )? FORCE?
    | ALTER TABLE dotIdentifier alterModify COLUMN columnName UNSET MASKING POLICY
    | ALTER TABLE dotIdentifier alterModify columnSetTags (COMMA columnSetTags)*
    | ALTER TABLE dotIdentifier alterModify columnUnsetTags (COMMA columnUnsetTags)*
    ;

alterColumnDeclList: alterColumnDecl (COMMA alterColumnDecl)*
    ;

alterColumnDecl: COLUMN? columnName alterColumnOpts
    ;

alterColumnOpts
    : DROP DEFAULT
    | SET DEFAULT dotIdentifier DOT NEXTVAL
    | ( SET? NOT NULL | DROP NOT NULL)
    | ( (SET DATA)? TYPE)? dataType
    | (COMMENT EQ string)
    | UNSET COMMENT
    ;

columnSetTags: COLUMN? columnName setTags
    ;

columnUnsetTags: COLUMN columnName unsetTags
    ;

alterTag: ALTER TAG (IF EXISTS)? dotIdentifier alterTagOpts
    ;

alterTask
    : ALTER TASK (IF EXISTS)? dotIdentifier resumeSuspend
    | ALTER TASK (IF EXISTS)? dotIdentifier ( REMOVE | ADD) AFTER stringList
    | ALTER TASK (IF EXISTS)? dotIdentifier SET
    // TODO : Check and review if element's order binded or not
    (WAREHOUSE EQ id)? taskSchedule? taskOverlap? taskTimeout? taskSuspendAfterFailureNumber? (
        COMMENT EQ string
    )? sessionParamsList?
    | ALTER TASK (IF EXISTS)? dotIdentifier UNSET
    // TODO : Check and review if element's order binded or not
    WAREHOUSE? SCHEDULE? ALLOW_OVERLAPPING_EXECUTION? USER_TASK_TIMEOUT_MS? SUSPEND_TASK_AFTER_NUM_FAILURES? COMMENT? sessionParameterList?
    //[ , ... ]
    | ALTER TASK (IF EXISTS)? dotIdentifier setTags
    | ALTER TASK (IF EXISTS)? dotIdentifier unsetTags
    | ALTER TASK (IF EXISTS)? dotIdentifier MODIFY AS sql
    | ALTER TASK (IF EXISTS)? dotIdentifier MODIFY WHEN expr
    ;

alterUser: ALTER USER (IF EXISTS)? id alterUserOpts
    ;

alterView
    : ALTER VIEW (IF EXISTS)? dotIdentifier RENAME TO dotIdentifier
    | ALTER VIEW (IF EXISTS)? dotIdentifier SET (COMMENT EQ string)
    | ALTER VIEW (IF EXISTS)? dotIdentifier UNSET COMMENT
    | ALTER VIEW dotIdentifier SET SECURE
    | ALTER VIEW dotIdentifier UNSET SECURE
    | ALTER VIEW (IF EXISTS)? dotIdentifier setTags
    | ALTER VIEW (IF EXISTS)? dotIdentifier unsetTags
    | ALTER VIEW (IF EXISTS)? dotIdentifier ADD ROW ACCESS POLICY id ON columnListInParentheses
    | ALTER VIEW (IF EXISTS)? dotIdentifier DROP ROW ACCESS POLICY id
    | ALTER VIEW (IF EXISTS)? dotIdentifier ADD ROW ACCESS POLICY id ON columnListInParentheses COMMA DROP ROW ACCESS POLICY id
    | ALTER VIEW (IF EXISTS)? dotIdentifier DROP ALL ROW ACCESS POLICIES
    | ALTER VIEW dotIdentifier alterModify COLUMN? id SET MASKING POLICY id (
        USING LPAREN columnName COMMA columnList RPAREN
    )? FORCE?
    | ALTER VIEW dotIdentifier alterModify COLUMN? id UNSET MASKING POLICY
    | ALTER VIEW dotIdentifier alterModify COLUMN? id setTags
    | ALTER VIEW dotIdentifier alterModify COLUMN id unsetTags
    ;

alterModify: ALTER | MODIFY
    ;

alterWarehouse: ALTER WAREHOUSE (IF EXISTS)? alterWarehouseOpts
    ;

alterConnectionOpts
    : id ENABLE FAILOVER TO ACCOUNTS id DOT id (COMMA id DOT id)* ignoreEditionCheck?
    | id DISABLE FAILOVER ( TO ACCOUNTS id DOT id (COMMA id DOT id))?
    | id PRIMARY
    | (IF EXISTS)? id SET (COMMENT EQ string)
    | (IF EXISTS)? id UNSET COMMENT
    ;

alterUserOpts
    : RENAME TO id
    | RESET PASSWORD
    | ABORT ALL QUERIES
    | ADD DELEGATED AUTHORIZATION OF ROLE id TO SECURITY INTEGRATION id
    | REMOVE DELEGATED (AUTHORIZATION OF ROLE id | AUTHORIZATIONS) FROM SECURITY INTEGRATION id
    | setTags
    | unsetTags
    //    | SET objectProperties? objectParams? sessionParams?
    //    | UNSET (objectPropertyName | objectid | sessionid) //[ , ... ]
    ;

alterTagOpts
    : RENAME TO dotIdentifier
    | ( ADD | DROP) tagAllowedValues
    | UNSET ALLOWED_VALUES
    | SET MASKING POLICY id (COMMA MASKING POLICY id)*
    | UNSET MASKING POLICY id (COMMA MASKING POLICY id)*
    | SET (COMMENT EQ string)
    | UNSET COMMENT
    ;

alterNetworkPolicyOpts
    : (IF EXISTS)? id SET (ALLOWED_IP_LIST EQ LPAREN stringList RPAREN)? (
        BLOCKED_IP_LIST EQ LPAREN stringList RPAREN
    )? (COMMENT EQ string)?
    | (IF EXISTS)? id UNSET COMMENT
    | id RENAME TO id
    ;

alterWarehouseOpts
    : idFn? (SUSPEND | RESUME (IF SUSPENDED)?)
    | idFn? ABORT ALL QUERIES
    | idFn RENAME TO id
    //    | id SET [ objectProperties ]
    | idFn setTags
    | idFn unsetTags
    | idFn UNSET id (COMMA id)*
    | id SET whProperties (COLON whProperties)*
    ;

alterAccountOpts
    : SET accountParams? objectParams? sessionParams?
    | UNSET id (COMMA id)?
    | SET RESOURCE_MONITOR EQ id
    | setTags
    | unsetTags
    | id RENAME TO id ( SAVE_OLD_URL EQ trueFalse)?
    | id DROP OLD URL
    ;

setTags: SET tagDeclList
    ;

tagDeclList: TAG dotIdentifier EQ string (COMMA dotIdentifier EQ string)*
    ;

unsetTags: UNSET TAG dotIdentifier (COMMA dotIdentifier)*
    ;

// create commands
createCommand
    : createAccount
    | createAlert
    | createApiIntegration
    | createObjectClone
    | createConnection
    | createDatabase
    | createDynamicTable
    | createEventTable
    | createExternalFunction
    | createExternalTable
    | createFailoverGroup
    | createFileFormat
    | createFunction
    //| createIntegration
    | createManagedAccount
    | createMaskingPolicy
    | createMaterializedView
    | createNetworkPolicy
    | createNotificationIntegration
    | createPipe
    | createProcedure
    | createReplicationGroup
    | createResourceMonitor
    | createRole
    | createRowAccessPolicy
    | createSchema
    | createSecurityIntegrationExternalOauth
    | createSecurityIntegrationSnowflakeOauth
    | createSecurityIntegrationSaml2
    | createSecurityIntegrationScim
    | createSequence
    | createSessionPolicy
    | createShare
    | createStage
    | createStorageIntegration
    | createStream
    | createTable
    | createTableAsSelect
    | createTableLike
    //    | create_|AlterTable_…Constraint
    | createTag
    | createTask
    | createUser
    | createView
    | createWarehouse
    ;

createAccount
    : CREATE ACCOUNT id ADMIN_NAME EQ id ADMIN_PASSWORD EQ string (FIRST_NAME EQ id)? (
        LAST_NAME EQ id
    )? EMAIL EQ string (MUST_CHANGE_PASSWORD EQ trueFalse)? EDITION EQ (
        STANDARD
        | ENTERPRISE
        | BUSINESS_CRITICAL
    ) (REGION_GROUP EQ id)? (REGION EQ id)? (COMMENT EQ string)?
    ;

createAlert
    : CREATE (OR REPLACE)? ALERT (IF NOT EXISTS)? id WAREHOUSE EQ id SCHEDULE EQ string IF LPAREN EXISTS LPAREN alertCondition RPAREN RPAREN THEN
        alertAction
    ;

alertCondition: selectStatement | showCommand | call
    ;

alertAction: sqlClauses
    ;

createApiIntegration
    : CREATE (OR REPLACE)? API INTEGRATION (IF NOT EXISTS)? id API_PROVIDER EQ (id) API_AWS_ROLE_ARN EQ string (
        API_KEY EQ string
    )? API_ALLOWED_PREFIXES EQ LPAREN string RPAREN (API_BLOCKED_PREFIXES EQ LPAREN string RPAREN)? ENABLED EQ trueFalse (
        COMMENT EQ string
    )?
    | CREATE (OR REPLACE)? API INTEGRATION (IF NOT EXISTS)? id API_PROVIDER EQ id AZURE_TENANT_ID EQ string AZURE_AD_APPLICATION_ID EQ string (
        API_KEY EQ string
    )? API_ALLOWED_PREFIXES EQ LPAREN string RPAREN (API_BLOCKED_PREFIXES EQ LPAREN string RPAREN)? ENABLED EQ trueFalse (
        COMMENT EQ string
    )?
    | CREATE (OR REPLACE) API INTEGRATION (IF NOT EXISTS) id API_PROVIDER EQ id GOOGLE_AUDIENCE EQ string API_ALLOWED_PREFIXES EQ LPAREN string RPAREN
        (
        API_BLOCKED_PREFIXES EQ LPAREN string RPAREN
    )? ENABLED EQ trueFalse (COMMENT EQ string)?
    ;

createObjectClone
    : CREATE (OR REPLACE)? (DATABASE | SCHEMA | TABLE) (IF NOT EXISTS)? id CLONE dotIdentifier (
        atBefore1 LPAREN (TIMESTAMP ASSOC string | OFFSET ASSOC string | STATEMENT ASSOC id) RPAREN
    )?
    | CREATE (OR REPLACE)? (STAGE | FILE FORMAT | SEQUENCE | STREAM | TASK) (IF NOT EXISTS)? dotIdentifier CLONE dotIdentifier
    ;

createConnection
    : CREATE CONNECTION (IF NOT EXISTS)? id (
        (COMMENT EQ string)?
        | (AS REPLICA OF id DOT id DOT id (COMMENT EQ string)?)
    )
    ;

createDatabase
    : CREATE (OR REPLACE)? TRANSIENT? DATABASE (IF NOT EXISTS)? id cloneAtBefore? (
        DATA_RETENTION_TIME_IN_DAYS EQ INT
    )? (MAX_DATA_EXTENSION_TIME_IN_DAYS EQ INT)? defaultDdlCollation? withTags? (COMMENT EQ string)?
    ;

cloneAtBefore
    : CLONE id (
        atBefore1 LPAREN (TIMESTAMP ASSOC string | OFFSET ASSOC string | STATEMENT ASSOC id) RPAREN
    )?
    ;

atBefore1: AT_KEYWORD | BEFORE
    ;

headerDecl: string EQ string
    ;

compressionType: NONE | GZIP | DEFLATE | AUTO
    ;

compression: COMPRESSION EQ compressionType
    ;

createDynamicTable
    : CREATE (OR REPLACE)? DYNAMIC TABLE id TARGET_LAG EQ (string | DOWNSTREAM) WAREHOUSE EQ wh = id AS queryStatement
    ;

createEventTable
    : CREATE (OR REPLACE)? EVENT TABLE (IF NOT EXISTS)? id clusterBy? (
        DATA_RETENTION_TIME_IN_DAYS EQ INT
    )? (MAX_DATA_EXTENSION_TIME_IN_DAYS EQ INT)? changeTracking? (DEFAULT_DDL_COLLATION_ EQ string)? copyGrants? withRowAccessPolicy? withTags? (
        WITH? (COMMENT EQ string)
    )?
    ;

createExternalFunction
    : CREATE (OR REPLACE)? SECURE? EXTERNAL FUNCTION dotIdentifier LPAREN (
        id dataType (COMMA id dataType)*
    )? RPAREN RETURNS dataType (NOT? NULL)? (
        ( CALLED ON NULL INPUT)
        | ((RETURNS NULL ON NULL INPUT) | STRICT)
    )? (VOLATILE | IMMUTABLE)? (COMMENT EQ string)? API_INTEGRATION EQ id (
        HEADERS EQ LPAREN headerDecl (COMMA headerDecl)* RPAREN
    )? (CONTEXT_HEADERS EQ LPAREN id (COMMA id)* RPAREN)? (MAX_BATCH_ROWS EQ INT)? compression? (
        REQUEST_TRANSLATOR EQ id
    )? (RESPONSE_TRANSLATOR EQ id)? AS string
    ;

createExternalTable
    // Partitions computed from expressions
    : CREATE (OR REPLACE)? EXTERNAL TABLE (IF NOT EXISTS)? dotIdentifier LPAREN externalTableColumnDeclList RPAREN cloudProviderParams3? partitionBy?
        WITH? LOCATION EQ namedStage (REFRESH_ON_CREATE EQ trueFalse)? (AUTO_REFRESH EQ trueFalse)? pattern? fileFormat (
        AWS_SNS_TOPIC EQ string
    )? copyGrants? withRowAccessPolicy? withTags? (COMMENT EQ string)?
    // Partitions added and removed manually
    | CREATE (OR REPLACE)? EXTERNAL TABLE (IF NOT EXISTS)? dotIdentifier LPAREN externalTableColumnDeclList RPAREN cloudProviderParams3? partitionBy?
        WITH? LOCATION EQ namedStage PARTITION_TYPE EQ USER_SPECIFIED fileFormat copyGrants? withRowAccessPolicy? withTags? (
        COMMENT EQ string
    )?
    // Delta Lake
    | CREATE (OR REPLACE)? EXTERNAL TABLE (IF NOT EXISTS)? dotIdentifier LPAREN externalTableColumnDeclList RPAREN cloudProviderParams3? partitionBy?
        WITH? LOCATION EQ namedStage PARTITION_TYPE EQ USER_SPECIFIED fileFormat (
        TABLE_FORMAT EQ DELTA
    )? copyGrants? withRowAccessPolicy? withTags? (COMMENT EQ string)?
    ;

externalTableColumnDecl: columnName dataType AS (expr | id) inlineConstraint?
    ;

externalTableColumnDeclList: externalTableColumnDecl (COMMA externalTableColumnDecl)*
    ;

fullAcct: id DOT id
    ;

integrationTypeName: SECURITY INTEGRATIONS | API INTEGRATIONS
    ;

createFailoverGroup
    : CREATE FAILOVER GROUP (IF NOT EXISTS)? id OBJECT_TYPES EQ objectType (COMMA objectType)* (
        ALLOWED_DATABASES EQ id (COMMA id)*
    )? (ALLOWED_SHARES EQ id (COMMA id)*)? (
        ALLOWED_INTEGRATION_TYPES EQ integrationTypeName (COMMA integrationTypeName)*
    )? ALLOWED_ACCOUNTS EQ fullAcct (COMMA fullAcct)* (IGNORE EDITION CHECK)? (
        REPLICATION_SCHEDULE EQ string
    )?
    //      Secondary Replication Group
    | CREATE FAILOVER GROUP (IF NOT EXISTS)? id AS REPLICA OF id DOT id DOT id
    ;

typeFileformat: CSV | JSON | AVRO | ORC | PARQUET | XML | string
    ;

createFileFormat
    : CREATE (OR REPLACE)? FILE FORMAT (IF NOT EXISTS)? dotIdentifier (TYPE EQ typeFileformat)? formatTypeOptions* (
        COMMENT EQ string
    )?
    ;

argDecl: id dataType (DEFAULT expr)?
    ;

colDecl: columnName dataType? virtualColumnDecl?
    ;

virtualColumnDecl: AS LPAREN functionCall RPAREN
    ;

functionDefinition: string
    ;

// TODO: merge these rules to avoid massive lookahead
createFunction
    : CREATE (OR REPLACE)? SECURE? FUNCTION (IF NOT EXISTS)? dotIdentifier LPAREN (
        argDecl (COMMA argDecl)*
    )? RPAREN RETURNS (dataType | TABLE LPAREN (colDecl (COMMA colDecl)*)? RPAREN) (LANGUAGE id)? (
        CALLED ON NULL INPUT
        | RETURNS NULL ON NULL INPUT
        | STRICT
    )? (VOLATILE | IMMUTABLE)? (PACKAGES EQ LPAREN stringList RPAREN)? (
        RUNTIME_VERSION EQ (string | FLOAT)
    )? (IMPORTS EQ LPAREN stringList RPAREN)? (PACKAGES EQ LPAREN stringList RPAREN)? (
        HANDLER EQ string
    )? (NOT? NULL)? (COMMENT EQ com = string)? AS functionDefinition
    | CREATE (OR REPLACE)? SECURE? FUNCTION dotIdentifier LPAREN (argDecl (COMMA argDecl)*)? RPAREN RETURNS (
        dataType
        | TABLE LPAREN (colDecl (COMMA colDecl)*)? RPAREN
    ) (NOT? NULL)? (CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT)? (
        VOLATILE
        | IMMUTABLE
    )? MEMOIZABLE? (COMMENT EQ com = string)? AS functionDefinition
    ;

createManagedAccount
    : CREATE MANAGED ACCOUNT id ADMIN_NAME EQ id COMMA ADMIN_PASSWORD EQ string COMMA TYPE EQ READER (
        COMMA (COMMENT EQ string)
    )?
    ;

createMaskingPolicy
    : CREATE (OR REPLACE)? MASKING POLICY (IF NOT EXISTS)? dotIdentifier AS LPAREN id dataType (
        COMMA id dataType
    )? RPAREN RETURNS dataType ARROW expr (COMMENT EQ string)?
    ;

tagDecl: dotIdentifier EQ string
    ;

columnListInParentheses: LPAREN columnList RPAREN
    ;

createMaterializedView
    : CREATE (OR REPLACE)? SECURE? MATERIALIZED VIEW (IF NOT EXISTS)? dotIdentifier (
        LPAREN columnListWithComment RPAREN
    )? viewCol* withRowAccessPolicy? withTags? copyGrants? (COMMENT EQ string)? clusterBy? AS selectStatement
    //NOTA MATERIALIZED VIEW accept only simple select statement at this time
    ;

createNetworkPolicy
    : CREATE (OR REPLACE)? NETWORK POLICY id ALLOWED_IP_LIST EQ LPAREN stringList? RPAREN (
        BLOCKED_IP_LIST EQ LPAREN stringList? RPAREN
    )? (COMMENT EQ string)?
    ;

cloudProviderParamsAuto
    //(for Google Cloud Storage)
    : NOTIFICATION_PROVIDER EQ GCP_PUBSUB GCP_PUBSUB_SUBSCRIPTION_NAME EQ string
    //(for Microsoft Azure Storage)
    | NOTIFICATION_PROVIDER EQ AZURE_EVENT_GRID AZURE_STORAGE_QUEUE_PRIMARY_URI EQ string AZURE_TENANT_ID EQ string
    ;

cloudProviderParamsPush
    //(for Amazon SNS)
    : NOTIFICATION_PROVIDER EQ AWS_SNS AWS_SNS_TOPIC_ARN EQ string AWS_SNS_ROLE_ARN EQ string
    //(for Google Pub/Sub)
    | NOTIFICATION_PROVIDER EQ GCP_PUBSUB GCP_PUBSUB_TOPIC_NAME EQ string
    //(for Microsoft Azure Event Grid)
    | NOTIFICATION_PROVIDER EQ AZURE_EVENT_GRID AZURE_EVENT_GRID_TOPIC_ENDPOINT EQ string AZURE_TENANT_ID EQ string
    ;

createNotificationIntegration
    : CREATE (OR REPLACE)? NOTIFICATION INTEGRATION (IF NOT EXISTS)? id ENABLED EQ trueFalse TYPE EQ QUEUE cloudProviderParamsAuto (
        COMMENT EQ string
    )?
    | CREATE (OR REPLACE)? NOTIFICATION INTEGRATION (IF NOT EXISTS)? id ENABLED EQ trueFalse DIRECTION EQ OUTBOUND TYPE EQ QUEUE
        cloudProviderParamsPush (COMMENT EQ string)?
    ;

createPipe
    : CREATE (OR REPLACE)? PIPE (IF NOT EXISTS)? dotIdentifier (AUTO_INGEST EQ trueFalse)? (
        ERROR_INTEGRATION EQ id
    )? (AWS_SNS_TOPIC EQ string)? (INTEGRATION EQ string)? (COMMENT EQ string)? AS copyIntoTable
    ;

executeAs: EXECUTE AS (CALLER | OWNER)
    ;

table: TABLE (LPAREN (colDecl (COMMA colDecl)*)? RPAREN) | (functionCall)
    ;

createReplicationGroup
    : CREATE REPLICATION GROUP (IF NOT EXISTS)? id OBJECT_TYPES EQ objectType (COMMA objectType)* (
        ALLOWED_DATABASES EQ id (COMMA id)*
    )? (ALLOWED_SHARES EQ id (COMMA id)*)? (
        ALLOWED_INTEGRATION_TYPES EQ integrationTypeName (COMMA integrationTypeName)*
    )? ALLOWED_ACCOUNTS EQ fullAcct (COMMA fullAcct)* (IGNORE EDITION CHECK)? (
        REPLICATION_SCHEDULE EQ string
    )?
    //Secondary Replication Group
    | CREATE REPLICATION GROUP (IF NOT EXISTS)? id AS REPLICA OF id DOT id DOT id
    ;

createResourceMonitor
    : CREATE (OR REPLACE)? RESOURCE MONITOR id WITH creditQuota? frequency? (
        START_TIMESTAMP EQ ( string | IMMEDIATELY)
    )? (END_TIMESTAMP EQ string)? notifyUsers? (TRIGGERS triggerDefinition+)?
    ;

createRole: CREATE (OR REPLACE)? ROLE (IF NOT EXISTS)? id withTags? (COMMENT EQ string)?
    ;

createRowAccessPolicy
    : CREATE (OR REPLACE)? ROW ACCESS POLICY (IF NOT EXISTS)? id AS LPAREN argDecl (COMMA argDecl)* RPAREN RETURNS id /* BOOLEAN */ ARROW expr (
        COMMENT EQ string
    )?
    ;

createSchema
    : CREATE (OR REPLACE)? TRANSIENT? SCHEMA (IF NOT EXISTS)? schemaName cloneAtBefore? (
        WITH MANAGED ACCESS
    )? (DATA_RETENTION_TIME_IN_DAYS EQ INT)? (MAX_DATA_EXTENSION_TIME_IN_DAYS EQ INT)? defaultDdlCollation? withTags? (
        COMMENT EQ string
    )?
    ;

createSecurityIntegrationExternalOauth
    : CREATE (OR REPLACE)? SECURITY INTEGRATION (IF NOT EXISTS)? id TYPE EQ EXTERNAL_OAUTH ENABLED EQ trueFalse EXTERNAL_OAUTH_TYPE EQ (
        OKTA
        | id
        | PING_FEDERATE
        | CUSTOM
    ) EXTERNAL_OAUTH_ISSUER EQ string EXTERNAL_OAUTH_TOKEN_USER_MAPPING_CLAIM EQ (
        string
        | LPAREN stringList RPAREN
    ) EXTERNAL_OAUTH_SNOWFLAKE_USER_MAPPING_ATTRIBUTE EQ string (
        EXTERNAL_OAUTH_JWS_KEYS_URL EQ string
    )?                                                                    // For OKTA | PING_FEDERATE | CUSTOM
    (EXTERNAL_OAUTH_JWS_KEYS_URL EQ (string | LPAREN stringList RPAREN))? // For Azure
    (EXTERNAL_OAUTH_BLOCKED_ROLES_LIST EQ LPAREN stringList RPAREN)? (
        EXTERNAL_OAUTH_ALLOWED_ROLES_LIST EQ LPAREN stringList RPAREN
    )? (EXTERNAL_OAUTH_RSA_PUBLIC_KEY EQ string)? (EXTERNAL_OAUTH_RSA_PUBLIC_KEY_2 EQ string)? (
        EXTERNAL_OAUTH_AUDIENCE_LIST EQ LPAREN string RPAREN
    )? (EXTERNAL_OAUTH_ANY_ROLE_MODE EQ (DISABLE | ENABLE | ENABLE_FOR_PRIVILEGE))? (
        EXTERNAL_OAUTH_SCOPE_DELIMITER EQ string
    )? // Only for EXTERNAL_OAUTH_TYPE EQ CUSTOM
    ;

implicitNone: IMPLICIT | NONE
    ;

createSecurityIntegrationSnowflakeOauth
    : CREATE (OR REPLACE)? SECURITY INTEGRATION (IF NOT EXISTS)? id TYPE EQ OAUTH OAUTH_CLIENT EQ partnerApplication OAUTH_REDIRECT_URI EQ string
    //Required when OAUTH_CLIENTEQLOOKER
    enabledTrueFalse? (OAUTH_ISSUE_REFRESH_TOKENS EQ trueFalse)? (
        OAUTH_REFRESH_TOKEN_VALIDITY EQ INT
    )? (OAUTH_USE_SECONDARY_ROLES EQ implicitNone)? (
        BLOCKED_ROLES_LIST EQ LPAREN stringList RPAREN
    )? (COMMENT EQ string)?
    // Snowflake OAuth for custom clients
    | CREATE (OR REPLACE)? SECURITY INTEGRATION (IF NOT EXISTS)? id TYPE EQ OAUTH OAUTH_CLIENT EQ CUSTOM
    //OAUTH_CLIENT_TYPE EQ 'CONFIDENTIAL' | 'PUBLIC'
    OAUTH_REDIRECT_URI EQ string enabledTrueFalse? (OAUTH_ALLOW_NON_TLS_REDIRECT_URI EQ trueFalse)? (
        OAUTH_ENFORCE_PKCE EQ trueFalse
    )? (OAUTH_USE_SECONDARY_ROLES EQ implicitNone)? (
        PRE_AUTHORIZED_ROLES_LIST EQ LPAREN stringList RPAREN
    )? (BLOCKED_ROLES_LIST EQ LPAREN stringList RPAREN)? (OAUTH_ISSUE_REFRESH_TOKENS EQ trueFalse)? (
        OAUTH_REFRESH_TOKEN_VALIDITY EQ INT
    )? networkPolicy? (OAUTH_CLIENT_RSA_PUBLIC_KEY EQ string)? (
        OAUTH_CLIENT_RSA_PUBLIC_KEY_2 EQ string
    )? (COMMENT EQ string)?
    ;

createSecurityIntegrationSaml2
    : CREATE (OR REPLACE)? SECURITY INTEGRATION (IF NOT EXISTS)? TYPE EQ SAML2 enabledTrueFalse SAML2_ISSUER EQ string SAML2_SSO_URL EQ string
        SAML2_PROVIDER EQ string SAML2_X509_CERT EQ string (
        SAML2_SP_INITIATED_LOGIN_PAGE_LABEL EQ string
    )? (SAML2_ENABLE_SP_INITIATED EQ trueFalse)? (SAML2_SNOWFLAKE_X509_CERT EQ string)? (
        SAML2_SIGN_REQUEST EQ trueFalse
    )? (SAML2_REQUESTED_NAMEID_FORMAT EQ string)? (SAML2_POST_LOGOUT_REDIRECT_URL EQ string)? (
        SAML2_FORCE_AUTHN EQ trueFalse
    )? (SAML2_SNOWFLAKE_ISSUER_URL EQ string)? (SAML2_SNOWFLAKE_ACS_URL EQ string)?
    ;

createSecurityIntegrationScim
    : CREATE (OR REPLACE)? SECURITY INTEGRATION (IF NOT EXISTS)? id TYPE EQ SCIM SCIM_CLIENT EQ string RUN_AS_ROLE EQ string networkPolicy? (
        SYNC_PASSWORD EQ trueFalse
    )? (COMMENT EQ string)?
    ;

networkPolicy: NETWORK_POLICY EQ string
    ;

partnerApplication: TABLEAU_DESKTOP | TABLEAU_SERVER | LOOKER
    ;

startWith: START WITH? EQ? INT
    ;

incrementBy: INCREMENT BY? EQ? INT
    ;

createSequence
    : CREATE (OR REPLACE)? SEQUENCE (IF NOT EXISTS)? dotIdentifier WITH? startWith? incrementBy? orderNoorder? (
        COMMENT EQ string
    )?
    ;

createSessionPolicy
    : CREATE (OR REPLACE)? SESSION POLICY (IF EXISTS)? id (SESSION_IDLE_TIMEOUT_MINS EQ INT)? (
        SESSION_UI_IDLE_TIMEOUT_MINS EQ INT
    )? (COMMENT EQ string)?
    ;

createShare: CREATE (OR REPLACE)? SHARE id (COMMENT EQ string)?
    ;

formatTypeOptions
    //-- If TYPE EQ CSV
    : COMPRESSION EQ (AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE | string)
    | RECORD_DELIMITER EQ ( string | NONE)
    | FIELD_DELIMITER EQ ( string | NONE)
    | FILE_EXTENSION EQ string
    | SKIP_HEADER EQ INT
    | SKIP_BLANK_LINES EQ trueFalse
    | DATE_FORMAT EQ (string | AUTO)
    | TIME_FORMAT EQ (string | AUTO)
    | TIMESTAMP_FORMAT EQ (string | AUTO)
    | BINARY_FORMAT EQ id
    | ESCAPE EQ (string | NONE)
    | ESCAPE_UNENCLOSED_FIELD EQ (string | NONE)
    | TRIM_SPACE EQ trueFalse
    | FIELD_OPTIONALLY_ENCLOSED_BY EQ (string | NONE)
    | NULL_IF EQ LPAREN stringList RPAREN
    | ERROR_ON_COLUMN_COUNT_MISMATCH EQ trueFalse
    | REPLACE_INVALID_CHARACTERS EQ trueFalse
    | EMPTY_FIELD_AS_NULL EQ trueFalse
    | SKIP_BYTE_ORDER_MARK EQ trueFalse
    | ENCODING EQ (string | id) //by the way other encoding keyword are valid ie WINDOWS1252
    //-- If TYPE EQ JSON
    //| COMPRESSION EQ (AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE)
    //    | DATE_FORMAT EQ string | AUTO
    //    | TIME_FORMAT EQ string | AUTO
    //    | TIMESTAMP_FORMAT EQ string | AUTO
    //    | BINARY_FORMAT id
    //    | TRIM_SPACE EQ trueFalse
    //    | NULL_IF EQ LR_BRACKET stringList RR_BRACKET
    //    | FILE_EXTENSION EQ string
    | ENABLE_OCTAL EQ trueFalse
    | ALLOW_DUPLICATE EQ trueFalse
    | STRIP_OUTER_ARRAY EQ trueFalse
    | STRIP_NULL_VALUES EQ trueFalse
    //    | REPLACE_INVALID_CHARACTERS EQ trueFalse
    | IGNORE_UTF8_ERRORS EQ trueFalse
    //    | SKIP_BYTE_ORDER_MARK EQ trueFalse
    //-- If TYPE EQ AVRO
    //    | COMPRESSION EQ AUTO | GZIP | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE
    //    | TRIM_SPACE EQ trueFalse
    //    | NULL_IF EQ LR_BRACKET stringList RR_BRACKET
    //-- If TYPE EQ ORC
    //    | TRIM_SPACE EQ trueFalse
    //    | NULL_IF EQ LR_BRACKET stringList RR_BRACKET
    //-- If TYPE EQ PARQUET
    | COMPRESSION EQ AUTO
    | LZO
    | SNAPPY
    | NONE
    | SNAPPY_COMPRESSION EQ trueFalse
    | BINARY_AS_TEXT EQ trueFalse
    //    | TRIM_SPACE EQ trueFalse
    //    | NULL_IF EQ LR_BRACKET stringList RR_BRACKET
    //-- If TYPE EQ XML
    | COMPRESSION EQ AUTO
    | GZIP
    | BZ2
    | BROTLI
    | ZSTD
    | DEFLATE
    | RAW_DEFLATE
    | NONE
    //    | IGNORE_UTF8_ERRORS EQ trueFalse
    | PRESERVE_SPACE EQ trueFalse
    | STRIP_OUTER_ELEMENT EQ trueFalse
    | DISABLE_SNOWFLAKE_DATA EQ trueFalse
    | DISABLE_AUTO_CONVERT EQ trueFalse
    //    | SKIP_BYTE_ORDER_MARK EQ trueFalse
    ;

copyOptions
    : ON_ERROR EQ (CONTINUE | SKIP_FILE | SKIP_FILE_N | SKIP_FILE_N ABORT_STATEMENT)
    | SIZE_LIMIT EQ INT
    | PURGE EQ trueFalse
    | RETURN_FAILED_ONLY EQ trueFalse
    | MATCH_BY_COLUMN_NAME EQ CASE_SENSITIVE
    | CASE_INSENSITIVE
    | NONE
    | ENFORCE_LENGTH EQ trueFalse
    | TRUNCATECOLUMNS EQ trueFalse
    | FORCE EQ trueFalse
    ;

stageEncryptionOptsInternal: ENCRYPTION EQ LPAREN TYPE EQ (SNOWFLAKE_FULL | SNOWFLAKE_SSE) RPAREN
    ;

storageIntegrationEqId: STORAGE_INTEGRATION EQ id
    ;

storageCredentials: CREDENTIALS EQ parenStringOptions
    ;

storageEncryption: ENCRYPTION EQ parenStringOptions
    ;

parenStringOptions: LPAREN stringOption* RPAREN
    ;

stringOption: id EQ string
    ;

externalStageParams: URL EQ string storageIntegrationEqId? storageCredentials? storageEncryption?
    ;

trueFalse: TRUE | FALSE
    ;

enable: ENABLE EQ trueFalse
    ;

refreshOnCreate: REFRESH_ON_CREATE EQ trueFalse
    ;

autoRefresh: AUTO_REFRESH EQ trueFalse
    ;

notificationIntegration: NOTIFICATION_INTEGRATION EQ string
    ;

directoryTableInternalParams
    : DIRECTORY EQ LPAREN (
        enable refreshOnCreate?
        | REFRESH_ON_CREATE EQ FALSE
        | refreshOnCreate enable
    ) RPAREN
    ;

directoryTableExternalParams
    // (for Amazon S3)
    : DIRECTORY EQ LPAREN enable refreshOnCreate? autoRefresh? RPAREN
    // (for Google Cloud Storage)
    | DIRECTORY EQ LPAREN enable autoRefresh? refreshOnCreate? notificationIntegration? RPAREN
    // (for Microsoft Azure)
    | DIRECTORY EQ LPAREN enable refreshOnCreate? autoRefresh? notificationIntegration? RPAREN
    ;

/* ===========  Stage DDL section =========== */
createStage
    : CREATE (OR REPLACE)? temporary? STAGE (IF NOT EXISTS)? dotIdentifierOrIdent stageEncryptionOptsInternal? directoryTableInternalParams? (
        FILE_FORMAT EQ LPAREN (FORMAT_NAME EQ string | TYPE EQ typeFileformat formatTypeOptions*) RPAREN
    )? (COPY_OPTIONS_ EQ LPAREN copyOptions RPAREN)? withTags? (COMMENT EQ string)?
    | CREATE (OR REPLACE)? temporary? STAGE (IF NOT EXISTS)? dotIdentifierOrIdent externalStageParams directoryTableExternalParams? (
        FILE_FORMAT EQ LPAREN (FORMAT_NAME EQ string | TYPE EQ typeFileformat formatTypeOptions*) RPAREN
    )? (COPY_OPTIONS_ EQ LPAREN copyOptions RPAREN)? withTags? (COMMENT EQ string)?
    ;

alterStage
    : ALTER STAGE (IF EXISTS)? dotIdentifierOrIdent RENAME TO dotIdentifierOrIdent
    | ALTER STAGE (IF EXISTS)? dotIdentifierOrIdent setTags
    | ALTER STAGE (IF EXISTS)? dotIdentifierOrIdent unsetTags
    | ALTER STAGE (IF EXISTS)? dotIdentifierOrIdent SET externalStageParams? fileFormat? (
        COPY_OPTIONS_ EQ LPAREN copyOptions RPAREN
    )? (COMMENT EQ string)?
    ;

dropStage: DROP STAGE (IF EXISTS)? dotIdentifierOrIdent
    ;

describeStage: DESCRIBE STAGE dotIdentifierOrIdent
    ;

showStages: SHOW STAGES likePattern? inObj?
    ;

/* ===========  End of stage DDL section =========== */

cloudProviderParams
    : STORAGE_PROVIDER EQ string (
        AZURE_TENANT_ID EQ (string | ID)
        | STORAGE_AWS_ROLE_ARN EQ string (STORAGE_AWS_OBJECT_ACL EQ string)?
    )?
    ;

cloudProviderParams2
    //(for Amazon S3)
    : STORAGE_AWS_ROLE_ARN EQ string (STORAGE_AWS_OBJECT_ACL EQ string)?
    //(for Microsoft Azure)
    | AZURE_TENANT_ID EQ string
    ;

cloudProviderParams3: INTEGRATION EQ string
    ;

createStorageIntegration
    : CREATE (OR REPLACE)? STORAGE INTEGRATION (IF NOT EXISTS)? id TYPE EQ EXTERNAL_STAGE cloudProviderParams ENABLED EQ trueFalse
        STORAGE_ALLOWED_LOCATIONS EQ LPAREN stringList RPAREN (
        STORAGE_BLOCKED_LOCATIONS EQ LPAREN stringList RPAREN
    )? (COMMENT EQ string)?
    ;

copyGrants: COPY GRANTS
    ;

appendOnly: APPEND_ONLY EQ trueFalse
    ;

insertOnly: INSERT_ONLY EQ TRUE
    ;

showInitialRows: SHOW_INITIAL_ROWS EQ trueFalse
    ;

streamTime
    : atBefore1 LPAREN (
        TIMESTAMP ASSOC string
        | OFFSET ASSOC string
        | STATEMENT ASSOC id
        | STREAM ASSOC string
    ) RPAREN
    ;

createStream
    //-- table
    : CREATE (OR REPLACE)? STREAM (IF NOT EXISTS)? dotIdentifier copyGrants? ON TABLE dotIdentifier streamTime? appendOnly? showInitialRows? (
        COMMENT EQ string
    )?
    //-- External table
    | CREATE (OR REPLACE)? STREAM (IF NOT EXISTS)? dotIdentifier copyGrants? ON EXTERNAL TABLE dotIdentifier streamTime? insertOnly? (
        COMMENT EQ string
    )?
    //-- Directory table
    | CREATE (OR REPLACE)? STREAM (IF NOT EXISTS)? dotIdentifier copyGrants? ON STAGE dotIdentifier (
        COMMENT EQ string
    )?
    //-- View
    | CREATE (OR REPLACE)? STREAM (IF NOT EXISTS)? dotIdentifier copyGrants? ON VIEW dotIdentifier streamTime? appendOnly? showInitialRows? (
        COMMENT EQ string
    )?
    ;

temporary: TEMP | TEMPORARY
    ;

tableType: (( LOCAL | GLOBAL)? temporary | VOLATILE) | TRANSIENT
    ;

withTags: WITH? TAG LPAREN tagDecl (COMMA tagDecl)* RPAREN
    ;

withRowAccessPolicy: WITH? ROW ACCESS POLICY id ON LPAREN columnName (COMMA columnName)* RPAREN
    ;

clusterBy: CLUSTER BY LINEAR? exprListInParentheses
    ;

changeTracking: CHANGE_TRACKING EQ trueFalse
    ;

withMaskingPolicy: WITH? MASKING POLICY id (USING columnListInParentheses)?
    ;

collate: COLLATE string
    ;

orderNoorder: ORDER | NOORDER
    ;

defaultValue
    : DEFAULT expr
    | (AUTOINCREMENT | IDENTITY) (
        LPAREN INT COMMA INT RPAREN
        | startWith
        | incrementBy
        | startWith incrementBy
    )? orderNoorder?
    ;

foreignKey: FOREIGN KEY
    ;

primaryKey: PRIMARY KEY
    ;

outOfLineConstraint
    : (CONSTRAINT id)? (
        (UNIQUE | primaryKey) columnListInParentheses commonConstraintProperties*
        | foreignKey columnListInParentheses REFERENCES dotIdentifier columnListInParentheses constraintProperties
    )
    ;

// TODO: Fix fullColDecl as defaultvalue being NULL and nullable are ambiguous - works with current visitor thoguh for now
fullColDecl
    : colDecl (collate | inlineConstraint | (NOT? NULL) | (defaultValue | NULL))* withMaskingPolicy? withTags? (
        COMMENT string
    )?
    ;

columnDeclItem: fullColDecl | outOfLineConstraint
    ;

columnDeclItemList: columnDeclItem (COMMA columnDeclItem)*
    ;

createTable
    : CREATE (OR REPLACE)? tableType? TABLE (
        (IF NOT EXISTS)? dotIdentifier
        | dotIdentifier (IF NOT EXISTS)?
    ) (((COMMENT EQ string)? createTableClause) | (createTableClause (COMMENT EQ string)?))
    ;

columnDeclItemListParen: LPAREN columnDeclItemList RPAREN
    ;

createTableClause
    : (
        columnDeclItemListParen clusterBy?
        | clusterBy? (COMMENT EQ string)? columnDeclItemListParen
    ) stageFileFormat? (STAGE_COPY_OPTIONS EQ LPAREN copyOptions RPAREN)? (
        DATA_RETENTION_TIME_IN_DAYS EQ INT
    )? (MAX_DATA_EXTENSION_TIME_IN_DAYS EQ INT)? changeTracking? defaultDdlCollation? copyGrants? (
        COMMENT EQ string
    )? withRowAccessPolicy? withTags?
    ;

createTableAsSelect
    : CREATE (OR REPLACE)? tableType? TABLE (
        (IF NOT EXISTS)? dotIdentifier
        | dotIdentifier (IF NOT EXISTS)?
    ) (LPAREN columnDeclItemList RPAREN)? clusterBy? copyGrants? withRowAccessPolicy? withTags? (
        COMMENT EQ string
    )? AS LPAREN? queryStatement RPAREN?
    ;

createTableLike
    : CREATE (OR REPLACE)? TRANSIENT? TABLE (IF NOT EXISTS)? dotIdentifier LIKE dotIdentifier clusterBy? copyGrants?
    ;

createTag
    : CREATE (OR REPLACE)? TAG (IF NOT EXISTS)? dotIdentifier tagAllowedValues? (COMMENT EQ string)?
    ;

tagAllowedValues: ALLOWED_VALUES stringList
    ;

sessionParameter
    : ABORT_DETACHED_QUERY
    | ALLOW_CLIENT_MFA_CACHING
    | ALLOW_ID_TOKEN
    | AUTOCOMMIT
    | AUTOCOMMIT_API_SUPPORTED
    | BINARY_INPUT_FORMAT
    | BINARY_OUTPUT_FORMAT
    | CLIENT_ENABLE_LOG_INFO_STATEMENT_PARAMETERS
    | CLIENT_ENCRYPTION_KEY_SIZE
    | CLIENT_MEMORY_LIMIT
    | CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX
    | CLIENT_METADATA_USE_SESSION_DATABASE
    | CLIENT_PREFETCH_THREADS
    | CLIENT_RESULT_CHUNK_SIZE
    | CLIENT_RESULT_COLUMN_CASE_INSENSITIVE
    | CLIENT_SESSION_KEEP_ALIVE
    | CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY
    | CLIENT_TIMESTAMP_TYPE_MAPPING
    | DATA_RETENTION_TIME_IN_DAYS
    | DATE_INPUT_FORMAT
    | DATE_OUTPUT_FORMAT
    | DEFAULT_DDL_COLLATION_
    | ENABLE_INTERNAL_STAGES_PRIVATELINK
    | ENABLE_UNLOAD_PHYSICAL_TYPE_OPTIMIZATION
    | ENFORCE_SESSION_POLICY
    | ERROR_ON_NONDETERMINISTIC_MERGE
    | ERROR_ON_NONDETERMINISTIC_UPDATE
    | EXTERNAL_OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST
    | GEOGRAPHY_OUTPUT_FORMAT
    | GEOMETRY_OUTPUT_FORMAT
    | INITIAL_REPLICATION_SIZE_LIMIT_IN_TB
    | JDBC_TREAT_DECIMAL_AS_INT
    | JDBC_TREAT_TIMESTAMP_NTZ_AS_UTC
    | JDBC_USE_SESSION_TIMEZONE
    | JSON_INDENT
    | JS_TREAT_INTEGER_AS_BIGINT
    | LOCK_TIMEOUT
    | MAX_CONCURRENCY_LEVEL
    | MAX_DATA_EXTENSION_TIME_IN_DAYS
    | MULTI_STATEMENT_COUNT
    | MIN_DATA_RETENTION_TIME_IN_DAYS
    | NETWORK_POLICY
    | SHARE_RESTRICTIONS
    | PERIODIC_DATA_REKEYING
    | PIPE_EXECUTION_PAUSED
    | PREVENT_UNLOAD_TO_INLINE_URL
    | PREVENT_UNLOAD_TO_INTERNAL_STAGES
    | QUERY_TAG
    | QUOTED_IDENTIFIERS_IGNORE_CASE
    | REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_CREATION
    | REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_OPERATION
    | ROWS_PER_RESULTSET
    | SAML_IDENTITY_PROVIDER
    | SIMULATED_DATA_SHARING_CONSUMER
    | SSO_LOGIN_PAGE
    | STATEMENT_QUEUED_TIMEOUT_IN_SECONDS
    | STATEMENT_TIMEOUT_IN_SECONDS
    | STRICT_JSON_OUTPUT
    | SUSPEND_TASK_AFTER_NUM_FAILURES
    | TIMESTAMP_DAY_IS_ALWAYS_24H
    | TIMESTAMP_INPUT_FORMAT
    | TIMESTAMP_LTZ_OUTPUT_FORMAT
    | TIMESTAMP_NTZ_OUTPUT_FORMAT
    | TIMESTAMP_OUTPUT_FORMAT
    | TIMESTAMP_TYPE_MAPPING
    | TIMESTAMP_TZ_OUTPUT_FORMAT
    | TIMEZONE
    | TIME_INPUT_FORMAT
    | TIME_OUTPUT_FORMAT
    | TRANSACTION_ABORT_ON_ERROR
    | TRANSACTION_DEFAULT_ISOLATION_LEVEL
    | TWO_DIGIT_CENTURY_START
    | UNSUPPORTED_DDL_ACTION
    | USE_CACHED_RESULT
    | USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE
    | USER_TASK_TIMEOUT_MS
    | WEEK_OF_YEAR_POLICY
    | WEEK_START
    ;

sessionParameterList: sessionParameter (COMMA sessionParameter)*
    ;

sessionParamsList: sessionParams (COMMA sessionParams)*
    ;

createTask
    : CREATE (OR REPLACE)? TASK (IF NOT EXISTS)? dotIdentifier taskParameters* (COMMENT EQ string)? copyGrants? (
        AFTER dotIdentifier (COMMA dotIdentifier)*
    )? (WHEN searchCondition)? AS sql
    ;

taskParameters
    : taskCompute
    | taskSchedule
    | taskOverlap
    | sessionParamsList
    | taskTimeout
    | taskSuspendAfterFailureNumber
    | taskErrorIntegration
    ;

taskCompute
    : WAREHOUSE EQ id
    | USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE EQ (
        whCommonSize
        | string
    ) //Snowflake allow quoted warehouse size but must be without quote.
    ;

taskSchedule: SCHEDULE EQ string
    ;

taskTimeout: USER_TASK_TIMEOUT_MS EQ INT
    ;

taskSuspendAfterFailureNumber: SUSPEND_TASK_AFTER_NUM_FAILURES EQ INT
    ;

taskErrorIntegration: ERROR_INTEGRATION EQ id
    ;

taskOverlap: ALLOW_OVERLAPPING_EXECUTION EQ trueFalse
    ;

sql: EXECUTE IMMEDIATE DOLLAR_STRING | sqlClauses | call
    ;

// Snowfllake allows calls to special internal stored procedures, named x.y!entrypoint
call: CALL dotIdentifier (BANG id)? LPAREN exprList? RPAREN
    ;

createUser
    : CREATE (OR REPLACE)? USER (IF NOT EXISTS)? id objectProperties? objectParams? sessionParams?
    ;

viewCol: columnName withMaskingPolicy withTags
    ;

createView
    : CREATE (OR REPLACE)? SECURE? RECURSIVE? VIEW (IF NOT EXISTS)? dotIdentifier (
        LPAREN columnListWithComment RPAREN
    )? viewCol* withRowAccessPolicy? withTags? copyGrants? (COMMENT EQ string)? AS queryStatement
    ;

createWarehouse
    : CREATE (OR REPLACE)? WAREHOUSE (IF NOT EXISTS)? idFn (WITH? whProperties+)? whParams*
    ;

whCommonSize: XSMALL | SMALL | MEDIUM | LARGE | XLARGE | XXLARGE
    ;

whExtraSize: XXXLARGE | X4LARGE | X5LARGE | X6LARGE
    ;

whProperties
    : WAREHOUSE_SIZE EQ (whCommonSize | whExtraSize | LOCAL_ID)
    | WAREHOUSE_TYPE EQ (STANDARD | string)
    | MAX_CLUSTER_COUNT EQ INT
    | MIN_CLUSTER_COUNT EQ INT
    | SCALING_POLICY EQ (STANDARD | ECONOMY)
    | AUTO_SUSPEND (EQ INT | NULL)
    | AUTO_RESUME EQ trueFalse
    | INITIALLY_SUSPENDED EQ trueFalse
    | RESOURCE_MONITOR EQ id
    | (COMMENT EQ string)
    | ENABLE_QUERY_ACCELERATION EQ trueFalse
    | QUERY_ACCELERATION_MAX_SCALE_FACTOR EQ INT
    | MAX_CONCURRENCY_LEVEL EQ INT
    ;

whParams
    : MAX_CONCURRENCY_LEVEL EQ INT
    | STATEMENT_QUEUED_TIMEOUT_IN_SECONDS EQ INT
    | STATEMENT_TIMEOUT_IN_SECONDS EQ INT withTags?
    ;

objectTypeName
    : ROLE
    | USER
    | WAREHOUSE
    | INTEGRATION
    | NETWORK POLICY
    | SESSION POLICY
    | DATABASE
    | SCHEMA
    | TABLE
    | VIEW
    | STAGE
    | FILE FORMAT
    | STREAM
    | TASK
    | MASKING POLICY
    | ROW ACCESS POLICY
    | TAG
    | PIPE
    | FUNCTION
    | PROCEDURE
    | SEQUENCE
    ;

objectTypePlural
    : ROLES
    | USERS
    | WAREHOUSES
    | INTEGRATIONS
    | DATABASES
    | SCHEMAS
    | TABLES
    | VIEWS
    | STAGES
    | STREAMS
    | TASKS
    | ALERTS
    ;

// drop commands
dropCommand
    : dropObject
    | dropAlert
    | dropConnection
    | dropDatabase
    | dropDynamicTable
    //| dropEventTable //uses DROP TABLE stmt
    | dropExternalTable
    | dropFailoverGroup
    | dropFileFormat
    | dropFunction
    | dropIntegration
    | dropManagedAccount
    | dropMaskingPolicy
    | dropMaterializedView
    | dropNetworkPolicy
    | dropPipe
    | dropProcedure
    | dropReplicationGroup
    | dropResourceMonitor
    | dropRole
    | dropRowAccessPolicy
    | dropSchema
    | dropSequence
    | dropSessionPolicy
    | dropShare
    | dropStage
    | dropStream
    | dropTable
    | dropTag
    | dropTask
    | dropUser
    | dropView
    | dropWarehouse
    ;

dropObject: DROP objectType (IF EXISTS)? id cascadeRestrict?
    ;

dropAlert: DROP ALERT id
    ;

dropConnection: DROP CONNECTION (IF EXISTS)? id
    ;

dropDatabase: DROP DATABASE (IF EXISTS)? id cascadeRestrict?
    ;

dropDynamicTable: DROP DYNAMIC TABLE id
    ;

dropExternalTable: DROP EXTERNAL TABLE (IF EXISTS)? dotIdentifier cascadeRestrict?
    ;

dropFailoverGroup: DROP FAILOVER GROUP (IF EXISTS)? id
    ;

dropFileFormat: DROP FILE FORMAT (IF EXISTS)? id
    ;

dropFunction: DROP FUNCTION (IF EXISTS)? dotIdentifier argTypes
    ;

dropIntegration: DROP (API | NOTIFICATION | SECURITY | STORAGE)? INTEGRATION (IF EXISTS)? id
    ;

dropManagedAccount: DROP MANAGED ACCOUNT id
    ;

dropMaskingPolicy: DROP MASKING POLICY id
    ;

dropMaterializedView: DROP MATERIALIZED VIEW (IF EXISTS)? dotIdentifier
    ;

dropNetworkPolicy: DROP NETWORK POLICY (IF EXISTS)? id
    ;

dropPipe: DROP PIPE (IF EXISTS)? dotIdentifier
    ;

dropReplicationGroup: DROP REPLICATION GROUP (IF EXISTS)? id
    ;

dropResourceMonitor: DROP RESOURCE MONITOR id
    ;

dropRole: DROP ROLE (IF EXISTS)? id
    ;

dropRowAccessPolicy: DROP ROW ACCESS POLICY (IF EXISTS)? id
    ;

dropSchema: DROP SCHEMA (IF EXISTS)? schemaName cascadeRestrict?
    ;

dropSequence: DROP SEQUENCE (IF EXISTS)? dotIdentifier cascadeRestrict?
    ;

dropSessionPolicy: DROP SESSION POLICY (IF EXISTS)? id
    ;

dropShare: DROP SHARE id
    ;

dropStream: DROP STREAM (IF EXISTS)? dotIdentifier
    ;

dropTable: DROP TABLE (IF EXISTS)? dotIdentifier cascadeRestrict?
    ;

dropTag: DROP TAG (IF EXISTS)? dotIdentifier
    ;

dropTask: DROP TASK (IF EXISTS)? dotIdentifier
    ;

dropUser: DROP USER (IF EXISTS)? id
    ;

dropView: DROP VIEW (IF EXISTS)? dotIdentifier
    ;

dropWarehouse: DROP WAREHOUSE (IF EXISTS)? idFn
    ;

cascadeRestrict: CASCADE | RESTRICT
    ;

argTypes: LPAREN dataTypeList? RPAREN
    ;

// undrop commands
undropCommand
    : undropDatabase
    | undropSchema
    | undropTable
    | undropTag //: undropObject
    ;

undropDatabase: UNDROP DATABASE id
    ;

undropSchema: UNDROP SCHEMA schemaName
    ;

undropTable: UNDROP TABLE dotIdentifier
    ;

undropTag: UNDROP TAG dotIdentifier
    ;

// use commands
useCommand: useDatabase | useRole | useSchema | useSecondaryRoles | useWarehouse
    ;

useDatabase: USE DATABASE id
    ;

useRole: USE ROLE id
    ;

useSchema: USE SCHEMA? (id DOT)? id
    ;

useSecondaryRoles: USE SECONDARY ROLES (ALL | NONE)
    ;

useWarehouse: USE WAREHOUSE idFn
    ;

// describe command
describeCommand
    : describeAlert
    | describeDatabase
    | describeDynamicTable
    | describeEventTable
    | describeExternalTable
    | describeFileFormat
    | describeFunction
    | describeIntegration
    | describeMaskingPolicy
    | describeMaterializedView
    | describeNetworkPolicy
    | describePipe
    | describeProcedure
    | describeResult
    | describeRowAccessPolicy
    | describeSchema
    | describeSearchOptimization
    | describeSequence
    | describeSessionPolicy
    | describeShare
    | describeStage
    | describeStream
    | describeTable
    | describeTask
    | describeTransaction
    | describeUser
    | describeView
    | describeWarehouse
    ;

describeAlert: DESCRIBE ALERT id
    ;

describeDatabase: DESCRIBE DATABASE id
    ;

describeDynamicTable: DESCRIBE DYNAMIC TABLE id
    ;

describeEventTable: DESCRIBE EVENT TABLE id
    ;

describeExternalTable: DESCRIBE EXTERNAL? TABLE dotIdentifier (TYPE EQ (COLUMNS | STAGE))?
    ;

describeFileFormat: DESCRIBE FILE FORMAT id
    ;

describeFunction: DESCRIBE FUNCTION dotIdentifier argTypes
    ;

describeIntegration: DESCRIBE (API | NOTIFICATION | SECURITY | STORAGE)? INTEGRATION id
    ;

describeMaskingPolicy: DESCRIBE MASKING POLICY id
    ;

describeMaterializedView: DESCRIBE MATERIALIZED VIEW dotIdentifier
    ;

describeNetworkPolicy: DESCRIBE NETWORK POLICY id
    ;

describePipe: DESCRIBE PIPE dotIdentifier
    ;

describeProcedure: DESCRIBE PROCEDURE dotIdentifier argTypes
    ;

describeResult: DESCRIBE RESULT (string | LAST_QUERY_ID LPAREN RPAREN)
    ;

describeRowAccessPolicy: DESCRIBE ROW ACCESS POLICY id
    ;

describeSchema: DESCRIBE SCHEMA schemaName
    ;

describeSearchOptimization: DESCRIBE SEARCH OPTIMIZATION ON dotIdentifier
    ;

describeSequence: DESCRIBE SEQUENCE dotIdentifier
    ;

describeSessionPolicy: DESCRIBE SESSION POLICY id
    ;

describeShare: DESCRIBE SHARE id
    ;

describeStream: DESCRIBE STREAM dotIdentifier
    ;

describeTable: DESCRIBE TABLE dotIdentifier (TYPE EQ (COLUMNS | STAGE))?
    ;

describeTask: DESCRIBE TASK dotIdentifier
    ;

describeTransaction: DESCRIBE TRANSACTION INT
    ;

describeUser: DESCRIBE USER id
    ;

describeView: DESCRIBE VIEW dotIdentifier
    ;

describeWarehouse: DESCRIBE WAREHOUSE id
    ;

// show commands
showCommand
    : showAlerts
    | showChannels
    | showColumns
    | showConnections
    | showDatabases
    | showDatabasesInFailoverGroup
    | showDatabasesInReplicationGroup
    | showDelegatedAuthorizations
    | showDynamicTables
    | showEventTables
    | showExternalFunctions
    | showExternalTables
    | showFailoverGroups
    | showFileFormats
    | showFunctions
    | showGlobalAccounts
    | showGrants
    | showIntegrations
    | showLocks
    | showManagedAccounts
    | showMaskingPolicies
    | showMaterializedViews
    | showNetworkPolicies
    | showObjects
    | showOrganizationAccounts
    | showParameters
    | showPipes
    | showPrimaryKeys
    | showProcedures
    | showRegions
    | showReplicationAccounts
    | showReplicationDatabases
    | showReplicationGroups
    | showResourceMonitors
    | showRoles
    | showRowAccessPolicies
    | showSchemas
    | showSequences
    | showSessionPolicies
    | showShares
    | showSharesInFailoverGroup
    | showSharesInReplicationGroup
    | showStages
    | showStreams
    | showTables
    | showTags
    | showTasks
    | showTransactions
    | showUserFunctions
    | showUsers
    | showVariables
    | showViews
    | showWarehouses
    ;

showAlerts
    : SHOW TERSE? ALERTS likePattern? (IN ( ACCOUNT | DATABASE id? | SCHEMA schemaName?))? startsWith? limitRows?
    ;

showChannels
    : SHOW CHANNELS likePattern? (
        IN (ACCOUNT | DATABASE id? | SCHEMA schemaName? | TABLE | TABLE? dotIdentifier)
    )?
    ;

showColumns
    : SHOW COLUMNS likePattern? (
        IN (
            ACCOUNT
            | DATABASE id?
            | SCHEMA schemaName?
            | TABLE
            | TABLE? dotIdentifier
            | VIEW
            | VIEW? dotIdentifier
        )
    )?
    ;

showConnections: SHOW CONNECTIONS likePattern?
    ;

startsWith: STARTS WITH string
    ;

limitRows: LIMIT INT (FROM string)?
    ;

showDatabases: SHOW TERSE? DATABASES HISTORY? likePattern? startsWith? limitRows?
    ;

showDatabasesInFailoverGroup: SHOW DATABASES IN FAILOVER GROUP id
    ;

showDatabasesInReplicationGroup: SHOW DATABASES IN REPLICATION GROUP id
    ;

showDelegatedAuthorizations
    : SHOW DELEGATED AUTHORIZATIONS
    | SHOW DELEGATED AUTHORIZATIONS BY USER id
    | SHOW DELEGATED AUTHORIZATIONS TO SECURITY INTEGRATION id
    ;

showDynamicTables
    : SHOW DYNAMIC TABLES likePattern? (IN ( ACCOUNT | DATABASE id? | SCHEMA? schemaName?))? startsWith? limitRows?
    ;

showEventTables
    : SHOW TERSE? EVENT TABLES likePattern? (IN ( ACCOUNT | DATABASE id? | SCHEMA? schemaName?))? startsWith? limitRows?
    ;

showExternalFunctions: SHOW EXTERNAL FUNCTIONS likePattern?
    ;

showExternalTables
    : SHOW TERSE? EXTERNAL TABLES likePattern? (IN ( ACCOUNT | DATABASE id? | SCHEMA? schemaName?))? startsWith? limitRows?
    ;

showFailoverGroups: SHOW FAILOVER GROUPS (IN ACCOUNT id)?
    ;

showFileFormats
    : SHOW FILE FORMATS likePattern? (
        IN (ACCOUNT | DATABASE | DATABASE id | SCHEMA | SCHEMA schemaName | schemaName)
    )?
    ;

showFunctions
    : SHOW FUNCTIONS likePattern? (IN ( ACCOUNT | DATABASE | DATABASE id | SCHEMA | SCHEMA id | id))?
    ;

showGlobalAccounts: SHOW GLOBAL ACCOUNTS likePattern?
    ;

showGrants
    : SHOW GRANTS showGrantsOpts?
    | SHOW FUTURE GRANTS IN SCHEMA schemaName
    | SHOW FUTURE GRANTS IN DATABASE id
    ;

showGrantsOpts
    : ON ACCOUNT
    | ON objectType dotIdentifier
    | TO (ROLE id | USER id | SHARE id)
    | OF ROLE id
    | OF SHARE id
    ;

showIntegrations: SHOW (API | NOTIFICATION | SECURITY | STORAGE)? INTEGRATIONS likePattern?
    ;

showLocks: SHOW LOCKS (IN ACCOUNT)?
    ;

showManagedAccounts: SHOW MANAGED ACCOUNTS likePattern?
    ;

showMaskingPolicies: SHOW MASKING POLICIES likePattern? inObj?
    ;

inObj: IN (ACCOUNT | DATABASE | DATABASE id | SCHEMA | SCHEMA schemaName | schemaName)
    ;

inObj2: IN (ACCOUNT | DATABASE id? | SCHEMA schemaName? | TABLE | TABLE dotIdentifier)
    ;

showMaterializedViews: SHOW MATERIALIZED VIEWS likePattern? inObj?
    ;

showNetworkPolicies: SHOW NETWORK POLICIES
    ;

showObjects: SHOW OBJECTS likePattern? inObj?
    ;

showOrganizationAccounts: SHOW ORGANIZATION ACCOUNTS likePattern?
    ;

inFor: IN | FOR
    ;

showParameters
    : SHOW PARAMETERS likePattern? (
        inFor (
            SESSION
            | ACCOUNT
            | USER id?
            | ( WAREHOUSE | DATABASE | SCHEMA | TASK) id?
            | TABLE dotIdentifier
        )
    )?
    ;

showPipes: SHOW PIPES likePattern? inObj?
    ;

showPrimaryKeys: SHOW TERSE? PRIMARY KEYS inObj2?
    ;

showProcedures: SHOW PROCEDURES likePattern? inObj?
    ;

showRegions: SHOW REGIONS likePattern?
    ;

showReplicationAccounts: SHOW REPLICATION ACCOUNTS likePattern?
    ;

showReplicationDatabases: SHOW REPLICATION DATABASES likePattern? (WITH PRIMARY id DOT id)?
    ;

showReplicationGroups: SHOW REPLICATION GROUPS (IN ACCOUNT id)?
    ;

showResourceMonitors: SHOW RESOURCE MONITORS likePattern?
    ;

showRoles: SHOW ROLES likePattern?
    ;

showRowAccessPolicies: SHOW ROW ACCESS POLICIES likePattern? inObj?
    ;

showSchemas
    : SHOW TERSE? SCHEMAS HISTORY? likePattern? (IN ( ACCOUNT | DATABASE id?))? startsWith? limitRows?
    ;

showSequences: SHOW SEQUENCES likePattern? inObj?
    ;

showSessionPolicies: SHOW SESSION POLICIES
    ;

showShares: SHOW SHARES likePattern?
    ;

showSharesInFailoverGroup: SHOW SHARES IN FAILOVER GROUP id
    ;

showSharesInReplicationGroup: SHOW SHARES IN REPLICATION GROUP id
    ;

showStreams: SHOW STREAMS likePattern? inObj?
    ;

showTables: SHOW TABLES likePattern? inObj?
    ;

showTags
    : SHOW TAGS likePattern? (
        IN ACCOUNT
        | DATABASE
        | DATABASE id
        | SCHEMA
        | SCHEMA schemaName
        | schemaName
    )?
    ;

showTasks
    : SHOW TERSE? TASKS likePattern? (IN ( ACCOUNT | DATABASE id? | SCHEMA? schemaName?))? startsWith? limitRows?
    ;

showTransactions: SHOW TRANSACTIONS (IN ACCOUNT)?
    ;

showUserFunctions: SHOW USER FUNCTIONS likePattern? inObj?
    ;

showUsers: SHOW TERSE? USERS likePattern? (STARTS WITH string)? (LIMIT INT)? (FROM string)?
    ;

showVariables: SHOW VARIABLES likePattern?
    ;

showViews
    : SHOW TERSE? VIEWS likePattern? (IN ( ACCOUNT | DATABASE id? | SCHEMA? schemaName?))? startsWith? limitRows?
    ;

showWarehouses: SHOW WAREHOUSES likePattern?
    ;

likePattern: LIKE string
    ;

// TODO: Fix this - it is jsut a dotIdentifer - if ther are too many dots, its not the parser's problem
schemaName: d = id DOT s = id | s = id
    ;

objectType
    : ACCOUNT PARAMETERS
    | DATABASES
    | INTEGRATIONS
    | NETWORK POLICIES
    | RESOURCE MONITORS
    | ROLES
    | SHARES
    | USERS
    | WAREHOUSES
    ;

objectTypeList: objectType (COMMA objectType)*
    ;

// Strings are not a single token match but a stream of parts which may consist
// of variable references as well as plain text.
string: STRING_START stringPart* STRING_END | DOLLAR_STRING
    ;

stringPart
    : (
        VAR_SIMPLE
        | VAR_COMPLEX
        | STRING_CONTENT
        | STRING_UNICODE
        | STRING_ESCAPE
        | STRING_SQUOTE
        | STRING_AMPAMP
    )
    ;

stringList: string (COMMA string)*
    ;

idFn: id | IDENTIFIER LPAREN id RPAREN
    ;

id
    : ID
    | LOCAL_ID
    | DOUBLE_QUOTE_ID
    | AMP LCB? ID RCB? // Snowflake variables from CLI or injection - we rely on valid input
    | keyword          // almost any ketword can be used as an id :(
    ;

pattern: PATTERN EQ string
    ;

//patternAssoc
//    : PATTERN ASSOC string
//    ;

columnName: (id DOT)? id
    ;

columnList: columnName (COMMA columnName)*
    ;

columnListWithComment: columnName (COMMENT string)? (COMMA columnName (COMMENT string)?)*
    ;

dotIdentifier: id (DOT id)*
    ;

dotIdentifierOrIdent: dotIdentifier | IDENTIFIER LPAREN string RPAREN
    ;

/*** expressions ***/
exprList: expr (COMMA expr)*
    ;

// Snowflake stupidly allows AND and OR in any expression that results in a purely logical
// TRUE/FALSE result and is not involved in, say, a predicate. So we must also allow that,
// even though it messes with precedence somewhat. However,  as we only see queries that
// parse/work in Snowflake, there is no practical effect on correct parsing. It is a PITA
// that we have had to rename rules to make it make sense though.
expr
    : op = NOT+ expr # exprNot
    | expr AND expr  # exprAnd
    | expr OR expr   # exprOr
    | expression     # nonLogicalExpression
    ;

// Use this entry point into epxression when allowing AND and OR would be ambiguous, such as in
// searchConditions.
expression
    : LPAREN expression RPAREN                              # exprPrecedence
    | dotIdentifier DOT NEXTVAL                             # exprNextval
    | expression DOT expression                             # exprDot
    | expression COLON expression                           # exprColon
    | expression COLLATE string                             # exprCollate
    | caseExpression                                        # exprCase
    | iffExpr                                               # exprIff
    | sign expression                                       # exprSign
    | expression op = (STAR | DIVIDE | MODULE) expression   # exprPrecedence0
    | expression op = (PLUS | MINUS | PIPE_PIPE) expression # exprPrecedence1
    | expression comparisonOperator expression              # exprComparison
    | expression COLON_COLON dataType                       # exprAscribe
    | expression withinGroup                                # exprWithinGroup
    | expression overClause                                 # exprOver
    | castExpr                                              # exprCast
    | functionCall                                          # exprFuncCall
    | DISTINCT expression                                   # exprDistinct
    | LPAREN subquery RPAREN                                # exprSubquery
    | primitiveExpression                                   # exprPrimitive
    ;

withinGroup: WITHIN GROUP LPAREN orderByClause RPAREN
    ;

iffExpr: IFF LPAREN searchCondition COMMA expr COMMA expr RPAREN
    ;

castExpr: castOp = (TRY_CAST | CAST) LPAREN expr AS dataType RPAREN | INTERVAL expr
    ;

jsonLiteral: LCB kvPair (COMMA kvPair)* RCB | LCB RCB
    ;

kvPair: key = string COLON literal
    ;

arrayLiteral: LSB expr (COMMA expr)* RSB | LSB RSB
    ;

dataType
    : OBJECT (LPAREN objectField (COMMA objectField)* RPAREN)?
    | ARRAY (LPAREN dataType RPAREN)?
    | id discard? (LPAREN INT (COMMA INT)? RPAREN)?
    ;

// Caters for things like DOUBLE PRECISION where the PRECISION isn't needed
// and hrow awaya keywords that are also verbose for no good reason
discard: VARYING | id
    ;

objectField: id dataType
    ;

primitiveExpression
    : DEFAULT           # primExprDefault //?
    | id LSB INT RSB    # primArrayAccess
    | id LSB string RSB # primObjectAccess
    | id                # primExprColumn
    | literal           # primExprLiteral
    | COLON id          # primVariable // TODO: This needs to move to main expression as expression COLON expression  when JSON is implemented
    ;

overClause: OVER LPAREN (PARTITION BY expr (COMMA expr)*)? windowOrderingAndFrame? RPAREN
    ;

windowOrderingAndFrame: orderByClause rowOrRangeClause?
    ;

rowOrRangeClause: (ROWS | RANGE) windowFrameExtent
    ;

windowFrameExtent: BETWEEN windowFrameBound AND windowFrameBound
    ;

windowFrameBound: UNBOUNDED (PRECEDING | FOLLOWING) | INT (PRECEDING | FOLLOWING) | CURRENT ROW
    ;

functionCall: builtinFunction | standardFunction | rankingWindowedFunction | aggregateFunction
    ;

builtinFunction: EXTRACT LPAREN (string | ID) FROM expr RPAREN # builtinExtract
    ;

standardFunction
    : functionOptionalBrackets (LPAREN exprList? RPAREN)?
    | functionName LPAREN (exprList | paramAssocList)? RPAREN
    ;

functionName: id | nonReservedFunctionName
    ;

nonReservedFunctionName
    : LEFT
    | RIGHT // keywords that cannot be used as id, but can be used as function names
    ;

functionOptionalBrackets
    : CURRENT_DATE      // https://docs.snowflake.com/en/sql-reference/functions/current_date
    | CURRENT_TIMESTAMP // https://docs.snowflake.com/en/sql-reference/functions/current_timestamp
    | CURRENT_TIME      // https://docs.snowflake.com/en/sql-reference/functions/current_time
    | LOCALTIME         // https://docs.snowflake.com/en/sql-reference/functions/localtime
    | LOCALTIMESTAMP    // https://docs.snowflake.com/en/sql-reference/functions/localtimestamp
    ;

paramAssocList: paramAssoc (COMMA paramAssoc)*
    ;

paramAssoc: id ASSOC expr
    ;

ignoreOrRepectNulls: (IGNORE | RESPECT) NULLS
    ;

rankingWindowedFunction: standardFunction ignoreOrRepectNulls? overClause
    ;

aggregateFunction
    : op = (LISTAGG | ARRAY_AGG) LPAREN DISTINCT? expr (COMMA string)? RPAREN (
        WITHIN GROUP LPAREN orderByClause RPAREN
    )?                                    # aggFuncList
    | id LPAREN DISTINCT? exprList RPAREN # aggFuncExprList
    | id LPAREN STAR RPAREN               # aggFuncStar
    ;

literal
    : TIMESTAMP string
    | string
    | sign? INT
    | sign? (REAL | FLOAT)
    | trueFalse
    | jsonLiteral
    | arrayLiteral
    | NULL
    | PARAM     // A question mark can be used as a placeholder for a prepared statement that will use binding.
    | id string // DATE and any other additions
    ;

constant: string | INT | REAL | FLOAT
    ;

sign: PLUS | MINUS
    ;

caseExpression
    : CASE expr switchSection+ (ELSE expr)? END
    | CASE switchSearchConditionSection+ (ELSE expr)? END
    ;

switchSearchConditionSection: WHEN searchCondition THEN expr
    ;

switchSection: WHEN expr THEN expr
    ;

// select
queryStatement: withExpression? selectStatement setOperators*
    ;

withExpression: WITH RECURSIVE? commonTableExpression (COMMA commonTableExpression)*
    ;

commonTableExpression
    : tableName = id (LPAREN columnList RPAREN)? AS LPAREN (selectStatement setOperators*) RPAREN # CTETable
    | id AS LPAREN expr RPAREN																	  # CTEColumn
    ;

selectStatement
    : selectClause selectOptionalClauses limitClause?
    | selectTopClause selectOptionalClauses //TOP and LIMIT are not allowed together
    | LPAREN selectStatement RPAREN
    ;

setOperators
    // TODO: Handle INTERSECT precedence in the grammar; it has higher precedence than EXCEPT and UNION ALL.
    // Reference: https://docs.snowflake.com/en/sql-reference/operators-query#:~:text=precedence
    : (UNION ALL? | EXCEPT | MINUS_ | INTERSECT) selectStatement //EXCEPT and MINUS have same SQL meaning
    ;

selectOptionalClauses
    : intoClause? fromClause? whereClause? (groupByClause | havingClause)? qualifyClause? orderByClause?
    ;

selectClause: SELECT selectListNoTop
    ;

selectTopClause: SELECT selectListTop
    ;

selectListNoTop: allDistinct? selectList
    ;

selectListTop: allDistinct? topClause? selectList
    ;

selectList: selectListElem (COMMA selectListElem)*
    ;

selectListElem
    : expressionElem asAlias?
    | columnElem asAlias?
    | columnElemStar
    //    | udtElem
    ;

columnElemStar: (dotIdentifier DOT)? STAR
    ;

columnElem: (dotIdentifier DOT)? columnName | (dotIdentifier DOT)? DOLLAR columnPosition
    ;

asAlias: AS? alias
    ;

expressionElem: searchCondition | expr
    ;

columnPosition: INT
    ;

allDistinct: ALL | DISTINCT
    ;

topClause: TOP expr
    ;

intoClause: INTO varList
    ;

varList: var (COMMA var)*
    ;

var: COLON id
    ;

fromClause
    : FROM tableSources // objectRef joinClause*
    ;

tableSources: tableSource (COMMA tableSource)*
    ;

tableSource: tableSourceItemJoined sample? | LPAREN tableSource RPAREN
    ;

tableSourceItemJoined: objectRef joinClause* | LPAREN tableSourceItemJoined RPAREN joinClause*
    ;

objectRef
    : dotIdentifier atBefore? changes? matchRecognize? pivotUnpivot? tableAlias?   # objRefDefault
    | TABLE LPAREN functionCall RPAREN pivotUnpivot? tableAlias?                   # objRefTableFunc
    | valuesTable tableAlias?                                                      # objRefValues
    | LATERAL? (functionCall | (LPAREN subquery RPAREN)) pivotUnpivot? tableAlias? # objRefSubquery
    | dotIdentifier START WITH searchCondition CONNECT BY priorList?               # objRefStartWith
    ;

tableAlias: AS? alias (LPAREN id (COMMA id)* RPAREN)?
    ;

priorList: priorItem (COMMA priorItem)*
    ;

priorItem: PRIOR? id EQ PRIOR? id
    ;

outerJoin: (LEFT | RIGHT | FULL) OUTER?
    ;

joinType: INNER | outerJoin
    ;

joinClause
    : joinType? JOIN objectRef ((ON searchCondition) | (USING LPAREN columnList RPAREN))?
    | NATURAL outerJoin? JOIN objectRef
    | CROSS JOIN objectRef
    ;

atBefore
    : AT_KEYWORD LPAREN (
        TIMESTAMP ASSOC expr
        | OFFSET ASSOC expr
        | STATEMENT ASSOC string
        | STREAM ASSOC string
    ) RPAREN
    | BEFORE LPAREN STATEMENT ASSOC string RPAREN
    ;

end: END LPAREN ( TIMESTAMP ASSOC expr | OFFSET ASSOC expr | STATEMENT ASSOC string) RPAREN
    ;

changes: CHANGES LPAREN INFORMATION ASSOC defaultAppendOnly RPAREN atBefore end?
    ;

defaultAppendOnly: DEFAULT | APPEND_ONLY
    ;

partitionBy: PARTITION BY exprList
    ;

alias: id
    ;

exprAliasList: expr AS? alias (COMMA expr AS? alias)*
    ;

measures: MEASURES exprAliasList
    ;

matchOpts: SHOW EMPTY MATCHES | OMIT EMPTY MATCHES | WITH UNMATCHED ROWS
    ;

rowMatch: (ONE ROW PER MATCH | ALL ROWS PER MATCH) matchOpts?
    ;

firstLast: FIRST | LAST
    ;

// TODO: This syntax is unfinished and needs to be completed - DUMMY is just a placeholder from the original author
symbol: DUMMY
    ;

afterMatch: AFTER MATCH KWSKIP (PAST LAST ROW | TO NEXT ROW | TO firstLast? symbol)
    ;

symbolList: symbol AS expr (COMMA symbol AS expr)*
    ;

define: DEFINE symbolList
    ;

matchRecognize
    : MATCH_RECOGNIZE LPAREN partitionBy? orderByClause? measures? rowMatch? afterMatch? pattern? define? RPAREN
    ;

pivotUnpivot
    : PIVOT LPAREN aggregateFunc = id LPAREN pivotColumn = id RPAREN FOR valueColumn = id IN LPAREN values += literal (
        COMMA values += literal
    )* RPAREN RPAREN (asAlias columnAliasListInBrackets?)?
    | UNPIVOT LPAREN valueColumn = id FOR nameColumn = id IN LPAREN columnList RPAREN RPAREN
    ;

columnAliasListInBrackets: LPAREN id (COMMA id)* RPAREN
    ;

exprListInParentheses: LPAREN exprList RPAREN
    ;

valuesTable: LPAREN valuesTableBody RPAREN | valuesTableBody
    ;

valuesTableBody: VALUES exprListInParentheses (COMMA exprListInParentheses)*
    ;

sampleMethod
    : (SYSTEM | BLOCK) LPAREN INT RPAREN        # sampleMethodBlock
    | (BERNOULLI | ROW)? LPAREN INT ROWS RPAREN # sampleMethodRowFixed
    | (BERNOULLI | ROW)? LPAREN INT RPAREN      # sampleMethodRowProba
    ;

sample: (SAMPLE | TABLESAMPLE) sampleMethod sampleSeed?
    ;

sampleSeed: (REPEATABLE | SEED) LPAREN INT RPAREN
    ;

comparisonOperator: EQ | GT | LT | LE | GE | LTGT | NE
    ;

subquery: queryStatement
    ;

searchCondition
    : LPAREN searchCondition RPAREN       # scPrec
    | NOT searchCondition                 # scNot
    | searchCondition AND searchCondition # scAnd
    | searchCondition OR searchCondition  # scOr
    | predicate                           # scPred
    ;

predicate
    : EXISTS LPAREN subquery RPAREN                                                              # predExists
    | expression comparisonOperator expression                                                   # predBinop
    | expression comparisonOperator (ALL | SOME | ANY) LPAREN subquery RPAREN                    # predASA
    | expression IS NOT? NULL                                                                    # predIsNull
    | expression NOT? IN LPAREN (subquery | exprList) RPAREN                                     # predIn
    | expression NOT? BETWEEN expression AND expression                                          # predBetween
    | expression NOT? op = (LIKE | ILIKE) expression (ESCAPE expression)?                        # predLikeSinglePattern
    | expression NOT? op = (LIKE | ILIKE) (ANY | ALL) exprListInParentheses (ESCAPE expression)? # predLikeMultiplePatterns
    | expression NOT? RLIKE expression                                                           # predRLike
    | expression                                                                                 # predExpr
    ;

whereClause: WHERE searchCondition
    ;

groupByElem: columnElem | INT | expressionElem
    ;

groupByList: groupByElem (COMMA groupByElem)*
    ;

groupByClause
    : GROUP BY groupByList havingClause?
    | GROUP BY (GROUPING SETS | id) LPAREN groupByList RPAREN
    | GROUP BY ALL
    ;

havingClause: HAVING searchCondition
    ;

qualifyClause: QUALIFY expr
    ;

orderItem: expr (ASC | DESC)? (NULLS ( FIRST | LAST))?
    ;

orderByClause: ORDER BY orderItem (COMMA orderItem)*
    ;

limitClause
    : LIMIT expr (OFFSET expr)?
    | (OFFSET expr)? (ROW | ROWS)? FETCH (FIRST | NEXT)? expr (ROW | ROWS)? ONLY?
    ;
