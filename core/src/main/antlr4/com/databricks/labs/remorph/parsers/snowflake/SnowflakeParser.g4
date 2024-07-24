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

options {
    tokenVocab = SnowflakeLexer;
}

snowflakeFile: batch? EOF
    ;

batch: sqlCommand (SEMI* sqlCommand)* SEMI*
    ;

sqlCommand: ddlCommand | dmlCommand | showCommand | useCommand | describeCommand | otherCommand
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
    : INSERT OVERWRITE? INTO objectName (L_PAREN ids += id (COMMA ids += id)* R_PAREN)? (
        valuesTableBody
        | queryStatement
    )
    ;

insertMultiTableStatement
    : INSERT OVERWRITE? ALL intoClause2
    | INSERT OVERWRITE? (FIRST | ALL) (WHEN predicate THEN intoClause2+)+ (ELSE intoClause2)? subquery
    ;

intoClause2: INTO objectName (L_PAREN columnList R_PAREN)? valuesList?
    ;

valuesList: VALUES L_PAREN valueItem (COMMA valueItem)* R_PAREN
    ;

valueItem: columnName | DEFAULT | NULL_
    ;

mergeStatement: MERGE INTO tableRef USING tableSource ON predicate mergeMatches
    ;

mergeMatches: mergeCond+
    ;

mergeCond
    : (WHEN MATCHED (AND predicate)? THEN mergeUpdateDelete)+
    | WHEN NOT MATCHED (AND predicate)? THEN mergeInsert
    ;

mergeUpdateDelete: UPDATE SET columnName EQ expr (COLON columnName EQ expr)* | DELETE
    ;

mergeInsert: INSERT (L_PAREN columnList R_PAREN)? VALUES L_PAREN exprList R_PAREN
    ;

updateStatement
    : UPDATE tableRef SET setColumnValue (COMMA setColumnValue)* (FROM tableSources)? (
        WHERE predicate
    )?
    ;

setColumnValue: id EQ expr
    ;

tableRef: objectName asAlias?
    ;

tableOrQuery: tableRef | L_PAREN subquery R_PAREN asAlias?
    ;

tablesOrQueries: tableOrQuery (COMMA tableOrQuery)*
    ;

deleteStatement: DELETE FROM tableRef (USING tablesOrQueries)? (WHERE predicate)?
    ;

valuesBuilder: VALUES L_PAREN exprList R_PAREN (COMMA L_PAREN exprList R_PAREN)?
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
    ;

beginTxn: BEGIN (WORK | TRANSACTION)? (NAME id)? | START TRANSACTION ( NAME id)?
    ;

copyIntoTable
    : COPY INTO objectName FROM (tableStage | userStage | namedStage | externalLocation) files? pattern? fileFormat? copyOptions* (
        VALIDATION_MODE EQ (RETURN_N_ROWS | RETURN_ERRORS | RETURN_ALL_ERRORS)
    )?
    //
    /* Data load with transformation */
    | COPY INTO objectName (L_PAREN columnList R_PAREN)? FROM L_PAREN SELECT selectList FROM (
        tableStage
        | userStage
        | namedStage
    ) R_PAREN files? pattern? fileFormat? copyOptions*
    ;

externalLocation
    : STRING
    //(for Amazon S3)
    //'s3://<bucket>[/<path>]'
    //        ( ( STORAGE_INTEGRATION EQ id_ )?
    //        | ( CREDENTIALS EQ L_PAREN ( AWS_KEY_ID EQ string AWS_SECRET_KEY EQ string ( AWS_TOKEN EQ string )? ) R_PAREN )?
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
    //            | ( CREDENTIALS EQ L_PAREN ( AZURE_SAS_TOKEN EQ string ) R_PAREN )
    //        )?
    //[ ENCRYPTION = ( [ TYPE = { 'AZURE_CSE' | 'NONE' } ] [ MASTER_KEY = '<string>' ] ) ]
    ;

files: FILES EQ L_PAREN string (COMMA string)* R_PAREN
    ;

fileFormat: FILE_FORMAT EQ L_PAREN (formatName | formatType) R_PAREN
    ;

formatName: FORMAT_NAME EQ string
    ;

formatType: TYPE EQ typeFileformat formatTypeOptions*
    ;

stageFileFormat
    : STAGE_FILE_FORMAT EQ L_PAREN FORMAT_NAME EQ string
    | TYPE EQ typeFileformat formatTypeOptions+ R_PAREN
    ;

copyIntoLocation
    : COPY INTO (tableStage | userStage | namedStage | externalLocation) FROM (
        objectName
        | L_PAREN queryStatement R_PAREN
    ) partitionBy? fileFormat? copyOptions? (VALIDATION_MODE EQ RETURN_ROWS)? HEADER?
    ;

comment
    : COMMENT ifExists? ON objectTypeName objectName functionSignature? IS string
    | COMMENT ifExists? ON COLUMN objectName IS string
    ;

functionSignature: L_PAREN dataTypeList? R_PAREN
    ;

commit: COMMIT WORK?
    ;

executeImmediate
    : EXECUTE IMMEDIATE (string | id | ID2) (USING L_PAREN id (COMMA id)* R_PAREN)?
    | EXECUTE IMMEDIATE DBL_DOLLAR
    ;

executeTask: EXECUTE TASK objectName
    ;

explain: EXPLAIN (USING (TABULAR | JSON | TEXT))? sqlCommand
    ;

parallel: PARALLEL EQ num
    ;

getDml: GET (namedStage | userStage | tableStage) STRING parallel? pattern?
    ;

grantOwnership
    : GRANT OWNERSHIP (
        ON (objectTypeName objectName | ALL objectTypePlural IN ( DATABASE id | SCHEMA schemaName))
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
        ) objectName
        | (schemaPrivileges | ALL PRIVILEGES?) ON (SCHEMA schemaName | ALL SCHEMAS IN DATABASE id)
        | ( schemaPrivileges | ALL PRIVILEGES?) ON FUTURE SCHEMAS IN DATABASE id
        | (schemaObjectPrivileges | ALL PRIVILEGES?) ON (
            objectType objectName
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
        | ( TABLE objectName | ALL TABLES IN SCHEMA schemaName)
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
namedStage: AT objectName stagePath?
    ;

stagePath: DIVIDE (ID (DIVIDE ID)* DIVIDE?)?
    ;

put
    : PUT STRING (tableStage | userStage | namedStage) (PARALLEL EQ num)? (
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
        ) objectName
        | (schemaPrivileges | ALL PRIVILEGES?) ON (SCHEMA schemaName | ALL SCHEMAS IN DATABASE id)
        | (schemaPrivileges | ALL PRIVILEGES?) ON (FUTURE SCHEMAS IN DATABASE <dbName>)
        | (schemaObjectPrivileges | ALL PRIVILEGES?) ON (
            objectType objectName
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
        | ( TABLE objectName | ALL TABLES IN SCHEMA schemaName)
        | ( VIEW objectName | ALL VIEWS IN SCHEMA schemaName)
    ) FROM SHARE id
    ;

revokeRole: REVOKE ROLE roleName FROM (ROLE roleName | USER id)
    ;

rollback: ROLLBACK WORK?
    ;

set: SET id EQ expr | SET L_PAREN id (COMMA id)* R_PAREN EQ L_PAREN expr (COMMA expr)* R_PAREN
    ;

truncateMaterializedView: TRUNCATE MATERIALIZED VIEW objectName
    ;

truncateTable: TRUNCATE TABLE? ifExists? objectName
    ;

unset: UNSET id | UNSET L_PAREN id (COMMA id)* R_PAREN
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
    | CLIENT_ENCRYPTION_KEY_SIZE EQ num
    | ENFORCE_SESSION_POLICY EQ trueFalse
    | EXTERNAL_OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST EQ trueFalse
    | INITIAL_REPLICATION_SIZE_LIMIT_IN_TB EQ num
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
    : DATA_RETENTION_TIME_IN_DAYS EQ num
    | MAX_DATA_EXTENSION_TIME_IN_DAYS EQ num
    | defaultDdlCollation
    | MAX_CONCURRENCY_LEVEL EQ num
    | NETWORK_POLICY EQ string
    | PIPE_EXECUTION_PAUSED EQ trueFalse
    | SESSION_POLICY EQ string
    | STATEMENT_QUEUED_TIMEOUT_IN_SECONDS EQ num
    | STATEMENT_TIMEOUT_IN_SECONDS EQ num
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
    | DAYS_TO_EXPIRY EQ num
    | MINS_TO_UNLOCK EQ num
    | DEFAULT_WAREHOUSE EQ string
    | DEFAULT_NAMESPACE EQ string
    | DEFAULT_ROLE EQ string
    //| DEFAULT_SECONDARY_ROLES EQ L_PAREN 'ALL' R_PAREN
    | MINS_TO_BYPASS_MFA EQ num
    | RSA_PUBLIC_KEY EQ string
    | RSA_PUBLIC_KEY_2 EQ string
    | commentClause
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
    | JSON_INDENT EQ num
    | LOCK_TIMEOUT EQ num
    | QUERY_TAG EQ string
    | ROWS_PER_RESULTSET EQ num
    | SIMULATED_DATA_SHARING_CONSUMER EQ string
    | STATEMENT_TIMEOUT_IN_SECONDS EQ num
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
    | TWO_DIGIT_CENTURY_START EQ num
    | UNSUPPORTED_DDL_ACTION EQ string
    | USE_CACHED_RESULT EQ trueFalse
    | WEEK_OF_YEAR_POLICY EQ num
    | WEEK_START EQ num
    ;

alterAccount: ALTER ACCOUNT alterAccountOpts
    ;

enabledTrueFalse: ENABLED EQ trueFalse
    ;

alterAlert
    : ALTER ALERT ifExists? id (
        resumeSuspend
        | SET alertSetClause+
        | UNSET alertUnsetClause+
        | MODIFY CONDITION EXISTS L_PAREN alertCondition R_PAREN
        | MODIFY ACTION alertAction
    )
    ;

resumeSuspend: RESUME | SUSPEND
    ;

alertSetClause: WAREHOUSE EQ id | SCHEDULE EQ string | commentClause
    ;

alertUnsetClause: WAREHOUSE | SCHEDULE | COMMENT
    ;

alterApiIntegration
    : ALTER API? INTEGRATION ifExists? id SET (API_AWS_ROLE_ARN EQ string)? (
        AZURE_AD_APPLICATION_ID EQ string
    )? (API_KEY EQ string)? enabledTrueFalse? (API_ALLOWED_PREFIXES EQ L_PAREN string R_PAREN)? (
        API_BLOCKED_PREFIXES EQ L_PAREN string R_PAREN
    )? commentClause?
    | ALTER API? INTEGRATION id setTags
    | ALTER API? INTEGRATION id unsetTags
    | ALTER API? INTEGRATION ifExists? id UNSET apiIntegrationProperty (
        COMMA apiIntegrationProperty
    )*
    ;

apiIntegrationProperty: API_KEY | ENABLED | API_BLOCKED_PREFIXES | COMMENT
    ;

alterConnection: ALTER CONNECTION alterConnectionOpts
    ;

alterDatabase
    : ALTER DATABASE ifExists? id RENAME TO id
    | ALTER DATABASE ifExists? id SWAP WITH id
    | ALTER DATABASE ifExists? id SET (DATA_RETENTION_TIME_IN_DAYS EQ num)? (
        MAX_DATA_EXTENSION_TIME_IN_DAYS EQ num
    )? defaultDdlCollation? commentClause?
    | ALTER DATABASE id setTags
    | ALTER DATABASE id unsetTags
    | ALTER DATABASE ifExists? id UNSET databaseProperty (COMMA databaseProperty)*
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

accountIdList: accountIdentifier (COMMA accountIdentifier)*
    ;

alterDynamicTable: ALTER DYNAMIC TABLE id (resumeSuspend | REFRESH | SET WAREHOUSE EQ id)
    ;

alterExternalTable
    : ALTER EXTERNAL TABLE ifExists? objectName REFRESH string?
    | ALTER EXTERNAL TABLE ifExists? objectName ADD FILES L_PAREN stringList R_PAREN
    | ALTER EXTERNAL TABLE ifExists? objectName REMOVE FILES L_PAREN stringList R_PAREN
    | ALTER EXTERNAL TABLE ifExists? objectName SET (AUTO_REFRESH EQ trueFalse)? tagDeclList?
    | ALTER EXTERNAL TABLE ifExists? objectName unsetTags
    //Partitions added and removed manually
    | ALTER EXTERNAL TABLE objectName ifExists? ADD PARTITION L_PAREN columnName EQ string (
        COMMA columnName EQ string
    )* R_PAREN LOCATION string
    | ALTER EXTERNAL TABLE objectName ifExists? DROP PARTITION LOCATION string
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
    : ALTER FAILOVER GROUP ifExists? id RENAME TO id
    | ALTER FAILOVER GROUP ifExists? id SET (OBJECT_TYPES EQ objectTypeList)? replicationSchedule?
    | ALTER FAILOVER GROUP ifExists? id SET OBJECT_TYPES EQ objectTypeList
    //        ALLOWED_INTEGRATION_TYPES EQ <integrationTypeName> [ , <integrationTypeName> ... ] ]
    replicationSchedule?
    | ALTER FAILOVER GROUP ifExists? id ADD dbNameList TO ALLOWED_DATABASES
    | ALTER FAILOVER GROUP ifExists? id MOVE DATABASES dbNameList TO FAILOVER GROUP id
    | ALTER FAILOVER GROUP ifExists? id REMOVE dbNameList FROM ALLOWED_DATABASES
    | ALTER FAILOVER GROUP ifExists? id ADD shareNameList TO ALLOWED_SHARES
    | ALTER FAILOVER GROUP ifExists? id MOVE SHARES shareNameList TO FAILOVER GROUP id
    | ALTER FAILOVER GROUP ifExists? id REMOVE shareNameList FROM ALLOWED_SHARES
    | ALTER FAILOVER GROUP ifExists? id ADD fullAcctList TO ALLOWED_ACCOUNTS ignoreEditionCheck?
    | ALTER FAILOVER GROUP ifExists? id REMOVE fullAcctList FROM ALLOWED_ACCOUNTS
    //Target Account
    | ALTER FAILOVER GROUP ifExists? id ( REFRESH | PRIMARY | SUSPEND | RESUME)
    ;

alterFileFormat
    : ALTER FILE FORMAT ifExists? id RENAME TO id
    | ALTER FILE FORMAT ifExists? id SET (formatTypeOptions* commentClause?)
    ;

alterFunction
    : alterFunctionSignature RENAME TO id
    | alterFunctionSignature SET commentClause
    | alterFunctionSignature SET SECURE
    | alterFunctionSignature UNSET (SECURE | COMMENT)
    // External Functions
    | alterFunctionSignature SET API_INTEGRATION EQ id
    | alterFunctionSignature SET HEADERS EQ L_PAREN headerDecl* R_PAREN
    | alterFunctionSignature SET CONTEXT_HEADERS EQ L_PAREN id* R_PAREN
    | alterFunctionSignature SET MAX_BATCH_ROWS EQ num
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

alterFunctionSignature: ALTER FUNCTION ifExists? id L_PAREN dataTypeList? R_PAREN
    ;

dataTypeList: dataType (COMMA dataType)*
    ;

alterMaskingPolicy
    : ALTER MASKING POLICY ifExists? id SET BODY ARROW expr
    | ALTER MASKING POLICY ifExists? id RENAME TO id
    | ALTER MASKING POLICY ifExists? id SET commentClause
    ;

alterMaterializedView
    : ALTER MATERIALIZED VIEW id (
        RENAME TO id
        | CLUSTER BY L_PAREN exprList R_PAREN
        | DROP CLUSTERING KEY
        | resumeSuspend RECLUSTER?
        | SET ( SECURE? commentClause?)
        | UNSET ( SECURE | COMMENT)
    )
    ;

alterNetworkPolicy: ALTER NETWORK POLICY alterNetworkPolicyOpts
    ;

alterNotificationIntegration
    : ALTER NOTIFICATION? INTEGRATION ifExists? id SET enabledTrueFalse? cloudProviderParamsAuto commentClause?
    // Push notifications
    | ALTER NOTIFICATION? INTEGRATION ifExists? id SET enabledTrueFalse? cloudProviderParamsPush commentClause?
    | ALTER NOTIFICATION? INTEGRATION id setTags
    | ALTER NOTIFICATION? INTEGRATION id unsetTags
    | ALTER NOTIFICATION? INTEGRATION ifExists id UNSET (ENABLED | COMMENT)
    ;

alterPipe
    : ALTER PIPE ifExists? id SET (objectProperties? commentClause?)
    | ALTER PIPE id setTags
    | ALTER PIPE id unsetTags
    | ALTER PIPE ifExists? id UNSET PIPE_EXECUTION_PAUSED EQ trueFalse
    | ALTER PIPE ifExists? id UNSET COMMENT
    | ALTER PIPE ifExists? id REFRESH (PREFIX EQ string)? (MODIFIED_AFTER EQ string)?
    ;

alterProcedure
    : ALTER PROCEDURE ifExists? id L_PAREN dataTypeList? R_PAREN RENAME TO id
    | ALTER PROCEDURE ifExists? id L_PAREN dataTypeList? R_PAREN SET commentClause
    | ALTER PROCEDURE ifExists? id L_PAREN dataTypeList? R_PAREN UNSET COMMENT
    | ALTER PROCEDURE ifExists? id L_PAREN dataTypeList? R_PAREN EXECUTE AS callerOwner
    ;

alterReplicationGroup
    //Source Account
    : ALTER REPLICATION GROUP ifExists? id RENAME TO id
    | ALTER REPLICATION GROUP ifExists? id SET (OBJECT_TYPES EQ objectTypeList)? (
        REPLICATION_SCHEDULE EQ string
    )?
    | ALTER REPLICATION GROUP ifExists? id SET OBJECT_TYPES EQ objectTypeList ALLOWED_INTEGRATION_TYPES EQ integrationTypeName (
        COMMA integrationTypeName
    )* (REPLICATION_SCHEDULE EQ string)?
    | ALTER REPLICATION GROUP ifExists? id ADD dbNameList TO ALLOWED_DATABASES
    | ALTER REPLICATION GROUP ifExists? id MOVE DATABASES dbNameList TO REPLICATION GROUP id
    | ALTER REPLICATION GROUP ifExists? id REMOVE dbNameList FROM ALLOWED_DATABASES
    | ALTER REPLICATION GROUP ifExists? id ADD shareNameList TO ALLOWED_SHARES
    | ALTER REPLICATION GROUP ifExists? id MOVE SHARES shareNameList TO REPLICATION GROUP id
    | ALTER REPLICATION GROUP ifExists? id REMOVE shareNameList FROM ALLOWED_SHARES
    | ALTER REPLICATION GROUP ifExists? id ADD accountIdList TO ALLOWED_ACCOUNTS ignoreEditionCheck?
    | ALTER REPLICATION GROUP ifExists? id REMOVE accountIdList FROM ALLOWED_ACCOUNTS
    //Target Account
    | ALTER REPLICATION GROUP ifExists? id REFRESH
    | ALTER REPLICATION GROUP ifExists? id SUSPEND
    | ALTER REPLICATION GROUP ifExists? id RESUME
    ;

creditQuota: CREDIT_QUOTA EQ num
    ;

frequency: FREQUENCY EQ (MONTHLY | DAILY | WEEKLY | YEARLY | NEVER)
    ;

notifyUsers: NOTIFY_USERS EQ L_PAREN id (COMMA id)* R_PAREN
    ;

triggerDefinition: ON num PERCENT DO (SUSPEND | SUSPEND_IMMEDIATE | NOTIFY)
    ;

alterResourceMonitor
    : ALTER RESOURCE MONITOR ifExists? id (
        SET creditQuota? frequency? (START_TIMESTAMP EQ L_PAREN string | IMMEDIATELY R_PAREN)? (
            END_TIMESTAMP EQ string
        )?
    )? (notifyUsers ( TRIGGERS triggerDefinition (COMMA triggerDefinition)*)?)?
    ;

alterRole
    : ALTER ROLE ifExists? id RENAME TO id
    | ALTER ROLE ifExists? id SET commentClause
    | ALTER ROLE ifExists? id UNSET COMMENT
    | ALTER ROLE ifExists? id setTags
    | ALTER ROLE ifExists? id unsetTags
    ;

alterRowAccessPolicy
    : ALTER ROW ACCESS POLICY ifExists? id SET BODY ARROW expr
    | ALTER ROW ACCESS POLICY ifExists? id RENAME TO id
    | ALTER ROW ACCESS POLICY ifExists? id SET commentClause
    ;

alterSchema
    : ALTER SCHEMA ifExists? schemaName RENAME TO schemaName
    | ALTER SCHEMA ifExists? schemaName SWAP WITH schemaName
    | ALTER SCHEMA ifExists? schemaName SET (
        (DATA_RETENTION_TIME_IN_DAYS EQ num)? (MAX_DATA_EXTENSION_TIME_IN_DAYS EQ num)? defaultDdlCollation? commentClause?
    )
    | ALTER SCHEMA ifExists? schemaName setTags
    | ALTER SCHEMA ifExists? schemaName unsetTags
    | ALTER SCHEMA ifExists? schemaName UNSET schemaProperty (COMMA schemaProperty)*
    | ALTER SCHEMA ifExists? schemaName ( ENABLE | DISABLE) MANAGED ACCESS
    ;

schemaProperty
    : DATA_RETENTION_TIME_IN_DAYS
    | MAX_DATA_EXTENSION_TIME_IN_DAYS
    | DEFAULT_DDL_COLLATION_
    | COMMENT
    ;

alterSequence
    : ALTER SEQUENCE ifExists? objectName RENAME TO objectName
    | ALTER SEQUENCE ifExists? objectName SET? ( INCREMENT BY? EQ? num)?
    | ALTER SEQUENCE ifExists? objectName SET (orderNoorder? commentClause | orderNoorder)
    | ALTER SEQUENCE ifExists? objectName UNSET COMMENT
    ;

alterSecurityIntegrationExternalOauth
    : ALTER SECURITY? INTEGRATION ifExists id SET (TYPE EQ EXTERNAL_OAUTH)? (ENABLED EQ trueFalse)? (
        EXTERNAL_OAUTH_TYPE EQ ( OKTA | AZURE | PING_FEDERATE | CUSTOM)
    )? (EXTERNAL_OAUTH_ISSUER EQ string)? (
        EXTERNAL_OAUTH_TOKEN_USER_MAPPING_CLAIM EQ (string | L_PAREN stringList R_PAREN)
    )? (EXTERNAL_OAUTH_SNOWFLAKE_USER_MAPPING_ATTRIBUTE EQ string)? (
        EXTERNAL_OAUTH_JWS_KEYS_URL EQ string
    )?                                                                      // For OKTA | PING_FEDERATE | CUSTOM
    (EXTERNAL_OAUTH_JWS_KEYS_URL EQ (string | L_PAREN stringList R_PAREN))? // For Azure
    (EXTERNAL_OAUTH_RSA_PUBLIC_KEY EQ string)? (EXTERNAL_OAUTH_RSA_PUBLIC_KEY_2 EQ string)? (
        EXTERNAL_OAUTH_BLOCKED_ROLES_LIST EQ L_PAREN stringList R_PAREN
    )? (EXTERNAL_OAUTH_ALLOWED_ROLES_LIST EQ L_PAREN stringList R_PAREN)? (
        EXTERNAL_OAUTH_AUDIENCE_LIST EQ L_PAREN string R_PAREN
    )? (EXTERNAL_OAUTH_ANY_ROLE_MODE EQ (DISABLE | ENABLE | ENABLE_FOR_PRIVILEGE))? (
        EXTERNAL_OAUTH_ANY_ROLE_MODE EQ string
    )? // Only for EXTERNAL_OAUTH_TYPE EQ CUSTOM
    | ALTER SECURITY? INTEGRATION ifExists? id UNSET securityIntegrationExternalOauthProperty (
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
    : ALTER SECURITY? INTEGRATION ifExists? id SET (TYPE EQ EXTERNAL_OAUTH)? enabledTrueFalse? (
        EXTERNAL_OAUTH_TYPE EQ ( OKTA | AZURE | PING_FEDERATE | CUSTOM)
    )? (EXTERNAL_OAUTH_ISSUER EQ string)? (
        EXTERNAL_OAUTH_TOKEN_USER_MAPPING_CLAIM EQ (string | L_PAREN stringList R_PAREN)
    )? (EXTERNAL_OAUTH_SNOWFLAKE_USER_MAPPING_ATTRIBUTE EQ string)? (
        EXTERNAL_OAUTH_JWS_KEYS_URL EQ string
    )?                                                                       // For OKTA | PING_FEDERATE | CUSTOM
    (EXTERNAL_OAUTH_JWS_KEYS_URL EQ ( string | L_PAREN stringList R_PAREN))? // For Azure
    (EXTERNAL_OAUTH_RSA_PUBLIC_KEY EQ string)? (EXTERNAL_OAUTH_RSA_PUBLIC_KEY_2 EQ string)? (
        EXTERNAL_OAUTH_BLOCKED_ROLES_LIST EQ L_PAREN stringList R_PAREN
    )? (EXTERNAL_OAUTH_ALLOWED_ROLES_LIST EQ L_PAREN stringList R_PAREN)? (
        EXTERNAL_OAUTH_AUDIENCE_LIST EQ L_PAREN string R_PAREN
    )? (EXTERNAL_OAUTH_ANY_ROLE_MODE EQ DISABLE | ENABLE | ENABLE_FOR_PRIVILEGE)? (
        EXTERNAL_OAUTH_SCOPE_DELIMITER EQ string
    ) // Only for EXTERNAL_OAUTH_TYPE EQ CUSTOM
    | ALTER SECURITY? INTEGRATION ifExists? id UNSET securityIntegrationSnowflakeOauthProperty (
        COMMA securityIntegrationSnowflakeOauthProperty
    )*
    | ALTER SECURITY? INTEGRATION id setTags
    | ALTER SECURITY? INTEGRATION id unsetTags
    ;

securityIntegrationSnowflakeOauthProperty: ENABLED | EXTERNAL_OAUTH_AUDIENCE_LIST
    ;

alterSecurityIntegrationSaml2
    : ALTER SECURITY? INTEGRATION ifExists? id SET (TYPE EQ SAML2)? enabledTrueFalse? (
        SAML2_ISSUER EQ string
    )? (SAML2_SSO_URL EQ string)? (SAML2_PROVIDER EQ string)? (SAML2_X509_CERT EQ string)? (
        SAML2_SP_INITIATED_LOGIN_PAGE_LABEL EQ string
    )? (SAML2_ENABLE_SP_INITIATED EQ trueFalse)? (SAML2_SNOWFLAKE_X509_CERT EQ string)? (
        SAML2_SIGN_REQUEST EQ trueFalse
    )? (SAML2_REQUESTED_NAMEID_FORMAT EQ string)? (SAML2_POST_LOGOUT_REDIRECT_URL EQ string)? (
        SAML2_FORCE_AUTHN EQ trueFalse
    )? (SAML2_SNOWFLAKE_ISSUER_URL EQ string)? (SAML2_SNOWFLAKE_ACS_URL EQ string)?
    | ALTER SECURITY? INTEGRATION ifExists? id UNSET ENABLED
    | ALTER SECURITY? INTEGRATION id setTags
    | ALTER SECURITY? INTEGRATION id unsetTags
    ;

alterSecurityIntegrationScim
    : ALTER SECURITY? INTEGRATION ifExists? id SET (NETWORK_POLICY EQ string)? (
        SYNC_PASSWORD EQ trueFalse
    )? commentClause?
    | ALTER SECURITY? INTEGRATION ifExists? id UNSET securityIntegrationScimProperty (
        COMMA securityIntegrationScimProperty
    )*
    | ALTER SECURITY? INTEGRATION id setTags
    | ALTER SECURITY? INTEGRATION id unsetTags
    ;

securityIntegrationScimProperty: NETWORK_POLICY | SYNC_PASSWORD | COMMENT
    ;

alterSession: ALTER SESSION SET sessionParams | ALTER SESSION UNSET paramName (COMMA paramName)*
    ;

alterSessionPolicy
    : ALTER SESSION POLICY ifExists? id (UNSET | SET) (SESSION_IDLE_TIMEOUT_MINS EQ num)? (
        SESSION_UI_IDLE_TIMEOUT_MINS EQ num
    )? commentClause?
    | ALTER SESSION POLICY ifExists? id RENAME TO id
    ;

alterShare
    : ALTER SHARE ifExists? id (ADD | REMOVE) ACCOUNTS EQ id (COMMA id)* (
        SHARE_RESTRICTIONS EQ trueFalse
    )?
    | ALTER SHARE ifExists? id ADD ACCOUNTS EQ id (COMMA id)* (SHARE_RESTRICTIONS EQ trueFalse)?
    | ALTER SHARE ifExists? id SET (ACCOUNTS EQ id (COMMA id)*)? commentClause?
    | ALTER SHARE ifExists? id setTags
    | ALTER SHARE id unsetTags
    | ALTER SHARE ifExists? id UNSET COMMENT
    ;

alterStorageIntegration
    : ALTER STORAGE? INTEGRATION ifExists? id SET cloudProviderParams2? enabledTrueFalse? (
        STORAGE_ALLOWED_LOCATIONS EQ L_PAREN stringList R_PAREN
    )? (STORAGE_BLOCKED_LOCATIONS EQ L_PAREN stringList R_PAREN)? commentClause?
    | ALTER STORAGE? INTEGRATION ifExists? id setTags
    | ALTER STORAGE? INTEGRATION id unsetTags
    | ALTER STORAGE? INTEGRATION ifExists? id UNSET (ENABLED | STORAGE_BLOCKED_LOCATIONS | COMMENT)
    //[ , ... ]
    ;

alterStream
    : ALTER STREAM ifExists? id SET tagDeclList? commentClause?
    | ALTER STREAM ifExists? id setTags
    | ALTER STREAM id unsetTags
    | ALTER STREAM ifExists? id UNSET COMMENT
    ;

alterTable
    : ALTER TABLE ifExists? objectName RENAME TO objectName
    | ALTER TABLE ifExists? objectName SWAP WITH objectName
    | ALTER TABLE ifExists? objectName (clusteringAction | tableColumnAction | constraintAction)
    | ALTER TABLE ifExists? objectName extTableColumnAction
    | ALTER TABLE ifExists? objectName searchOptimizationAction
    | ALTER TABLE ifExists? objectName SET stageFileFormat? (
        STAGE_COPY_OPTIONS EQ L_PAREN copyOptions R_PAREN
    )? (DATA_RETENTION_TIME_IN_DAYS EQ num)? (MAX_DATA_EXTENSION_TIME_IN_DAYS EQ num)? (
        CHANGE_TRACKING EQ trueFalse
    )? defaultDdlCollation? commentClause?
    | ALTER TABLE ifExists? objectName setTags
    | ALTER TABLE ifExists? objectName unsetTags
    | ALTER TABLE ifExists? objectName UNSET (
        DATA_RETENTION_TIME_IN_DAYS
        | MAX_DATA_EXTENSION_TIME_IN_DAYS
        | CHANGE_TRACKING
        | DEFAULT_DDL_COLLATION_
        | COMMENT
        |
    )
    //[ , ... ]
    | ALTER TABLE ifExists? objectName ADD ROW ACCESS POLICY id ON columnListInParentheses
    | ALTER TABLE ifExists? objectName DROP ROW ACCESS POLICY id
    | ALTER TABLE ifExists? objectName DROP ROW ACCESS POLICY id COMMA ADD ROW ACCESS POLICY id ON columnListInParentheses
    | ALTER TABLE ifExists? objectName DROP ALL ROW ACCESS POLICIES
    ;

clusteringAction
    : CLUSTER BY L_PAREN exprList R_PAREN
    | RECLUSTER ( MAX_SIZE EQ num)? ( WHERE expr)?
    | resumeSuspend RECLUSTER
    | DROP CLUSTERING KEY
    ;

tableColumnAction
    : ADD COLUMN? ifNotExists? fullColDecl (COMMA fullColDecl)*
    | RENAME COLUMN columnName TO columnName
    | alterModify (
        L_PAREN alterColumnClause (COLON alterColumnClause)* R_PAREN
        | alterColumnClause (COLON alterColumnClause)*
    )
    | alterModify COLUMN columnName SET MASKING POLICY id (
        USING L_PAREN columnName COMMA columnList R_PAREN
    )? FORCE?
    | alterModify COLUMN columnName UNSET MASKING POLICY
    | alterModify columnSetTags (COMMA columnSetTags)*
    | alterModify columnUnsetTags (COMMA columnUnsetTags)*
    | DROP COLUMN? ifExists? columnList
    //| DROP DEFAULT
    ;

alterColumnClause
    : COLUMN? columnName (
        DROP DEFAULT
        | SET DEFAULT objectName DOT NEXTVAL
        | ( SET? NOT NULL_ | DROP NOT NULL_)
        | ( (SET DATA)? TYPE)? dataType
        | COMMENT string
        | UNSET COMMENT
    )
    ;

inlineConstraint
    : (CONSTRAINT id)? (
        (UNIQUE | primaryKey) commonConstraintProperties*
        | foreignKey REFERENCES objectName (L_PAREN columnName R_PAREN)? constraintProperties
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

onAction: CASCADE | SET ( NULL_ | DEFAULT) | RESTRICT | NO ACTION
    ;

constraintProperties
    : commonConstraintProperties*
    | foreignKeyMatch
    | foreignKeyMatch? ( onUpdate onDelete? | onDelete onUpdate?)
    ;

extTableColumnAction
    : ADD COLUMN? columnName dataType AS L_PAREN expr R_PAREN
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

searchMethodWithTarget: (EQUALITY | SUBSTRING | GEO) L_PAREN (STAR | expr) R_PAREN
    ;

alterTableAlterColumn
    : ALTER TABLE objectName alterModify (
        L_PAREN alterColumnDeclList R_PAREN
        | alterColumnDeclList
    )
    | ALTER TABLE objectName alterModify COLUMN columnName SET MASKING POLICY id (
        USING L_PAREN columnName COMMA columnList R_PAREN
    )? FORCE?
    | ALTER TABLE objectName alterModify COLUMN columnName UNSET MASKING POLICY
    | ALTER TABLE objectName alterModify columnSetTags (COMMA columnSetTags)*
    | ALTER TABLE objectName alterModify columnUnsetTags (COMMA columnUnsetTags)*
    ;

alterColumnDeclList: alterColumnDecl (COMMA alterColumnDecl)*
    ;

alterColumnDecl: COLUMN? columnName alterColumnOpts
    ;

alterColumnOpts
    : DROP DEFAULT
    | SET DEFAULT objectName DOT NEXTVAL
    | ( SET? NOT NULL_ | DROP NOT NULL_)
    | ( (SET DATA)? TYPE)? dataType
    | commentClause
    | UNSET COMMENT
    ;

columnSetTags: COLUMN? columnName setTags
    ;

columnUnsetTags: COLUMN columnName unsetTags
    ;

alterTag: ALTER TAG ifExists? objectName alterTagOpts
    ;

alterTask
    : ALTER TASK ifExists? objectName resumeSuspend
    | ALTER TASK ifExists? objectName ( REMOVE | ADD) AFTER stringList
    | ALTER TASK ifExists? objectName SET
    // TODO : Check and review if element's order binded or not
    (WAREHOUSE EQ id)? taskSchedule? taskOverlap? taskTimeout? taskSuspendAfterFailureNumber? commentClause? sessionParamsList?
    | ALTER TASK ifExists? objectName UNSET
    // TODO : Check and review if element's order binded or not
    WAREHOUSE? SCHEDULE? ALLOW_OVERLAPPING_EXECUTION? USER_TASK_TIMEOUT_MS? SUSPEND_TASK_AFTER_NUM_FAILURES? COMMENT? sessionParameterList?
    //[ , ... ]
    | ALTER TASK ifExists? objectName setTags
    | ALTER TASK ifExists? objectName unsetTags
    | ALTER TASK ifExists? objectName MODIFY AS sql
    | ALTER TASK ifExists? objectName MODIFY WHEN expr
    ;

alterUser: ALTER USER ifExists? id alterUserOpts
    ;

alterView
    : ALTER VIEW ifExists? objectName RENAME TO objectName
    | ALTER VIEW ifExists? objectName SET commentClause
    | ALTER VIEW ifExists? objectName UNSET COMMENT
    | ALTER VIEW objectName SET SECURE
    | ALTER VIEW objectName UNSET SECURE
    | ALTER VIEW ifExists? objectName setTags
    | ALTER VIEW ifExists? objectName unsetTags
    | ALTER VIEW ifExists? objectName ADD ROW ACCESS POLICY id ON columnListInParentheses
    | ALTER VIEW ifExists? objectName DROP ROW ACCESS POLICY id
    | ALTER VIEW ifExists? objectName ADD ROW ACCESS POLICY id ON columnListInParentheses COMMA DROP ROW ACCESS POLICY id
    | ALTER VIEW ifExists? objectName DROP ALL ROW ACCESS POLICIES
    | ALTER VIEW objectName alterModify COLUMN? id SET MASKING POLICY id (
        USING L_PAREN columnName COMMA columnList R_PAREN
    )? FORCE?
    | ALTER VIEW objectName alterModify COLUMN? id UNSET MASKING POLICY
    | ALTER VIEW objectName alterModify COLUMN? id setTags
    | ALTER VIEW objectName alterModify COLUMN id unsetTags
    ;

alterModify: ALTER | MODIFY
    ;

alterWarehouse: ALTER WAREHOUSE ifExists? alterWarehouseOpts
    ;

alterConnectionOpts
    : id ENABLE FAILOVER TO ACCOUNTS id DOT id (COMMA id DOT id)* ignoreEditionCheck?
    | id DISABLE FAILOVER ( TO ACCOUNTS id DOT id (COMMA id DOT id))?
    | id PRIMARY
    | ifExists? id SET commentClause
    | ifExists? id UNSET COMMENT
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
    //    | UNSET (objectPropertyName | objectParamName | sessionParamName) //[ , ... ]
    ;

alterTagOpts
    : RENAME TO objectName
    | ( ADD | DROP) tagAllowedValues
    | UNSET ALLOWED_VALUES
    | SET MASKING POLICY id (COMMA MASKING POLICY id)*
    | UNSET MASKING POLICY id (COMMA MASKING POLICY id)*
    | SET commentClause
    | UNSET COMMENT
    ;

alterNetworkPolicyOpts
    : ifExists? id SET (ALLOWED_IP_LIST EQ L_PAREN stringList R_PAREN)? (
        BLOCKED_IP_LIST EQ L_PAREN stringList R_PAREN
    )? commentClause?
    | ifExists? id UNSET COMMENT
    | id RENAME TO id
    ;

alterWarehouseOpts
    : idFn? (SUSPEND | RESUME ifSuspended?)
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
    | UNSET paramName (COMMA paramName)?
    | SET RESOURCE_MONITOR EQ id
    | setTags
    | unsetTags
    | id RENAME TO id ( SAVE_OLD_URL EQ trueFalse)?
    | id DROP OLD URL
    ;

setTags: SET tagDeclList
    ;

tagDeclList: TAG objectName EQ tagValue (COMMA objectName EQ tagValue)*
    ;

unsetTags: UNSET TAG objectName (COMMA objectName)*
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
    ) (REGION_GROUP EQ regionGroupId)? (REGION EQ snowflakeRegionId)? commentClause?
    ;

createAlert
    : CREATE orReplace? ALERT ifNotExists? id WAREHOUSE EQ id SCHEDULE EQ string IF L_PAREN EXISTS L_PAREN alertCondition R_PAREN R_PAREN THEN
        alertAction
    ;

alertCondition: selectStatement | showCommand | call
    ;

alertAction: sqlCommand
    ;

createApiIntegration
    : CREATE orReplace? API INTEGRATION ifNotExists? id API_PROVIDER EQ (id) API_AWS_ROLE_ARN EQ string (
        API_KEY EQ string
    )? API_ALLOWED_PREFIXES EQ L_PAREN string R_PAREN (
        API_BLOCKED_PREFIXES EQ L_PAREN string R_PAREN
    )? ENABLED EQ trueFalse commentClause?
    | CREATE orReplace? API INTEGRATION ifNotExists? id API_PROVIDER EQ id AZURE_TENANT_ID EQ string AZURE_AD_APPLICATION_ID EQ string (
        API_KEY EQ string
    )? API_ALLOWED_PREFIXES EQ L_PAREN string R_PAREN (
        API_BLOCKED_PREFIXES EQ L_PAREN string R_PAREN
    )? ENABLED EQ trueFalse commentClause?
    | CREATE orReplace API INTEGRATION ifNotExists id API_PROVIDER EQ id GOOGLE_AUDIENCE EQ string API_ALLOWED_PREFIXES EQ L_PAREN string R_PAREN (
        API_BLOCKED_PREFIXES EQ L_PAREN string R_PAREN
    )? ENABLED EQ trueFalse commentClause?
    ;

createObjectClone
    : CREATE orReplace? (DATABASE | SCHEMA | TABLE) ifNotExists? id CLONE objectName (
        atBefore1 L_PAREN (TIMESTAMP ASSOC string | OFFSET ASSOC string | STATEMENT ASSOC id) R_PAREN
    )?
    | CREATE orReplace? (STAGE | FILE FORMAT | SEQUENCE | STREAM | TASK) ifNotExists? objectName CLONE objectName
    ;

createConnection
    : CREATE CONNECTION ifNotExists? id (
        commentClause?
        | (AS REPLICA OF id DOT id DOT id commentClause?)
    )
    ;

createDatabase
    : CREATE orReplace? TRANSIENT? DATABASE ifNotExists? id cloneAtBefore? (
        DATA_RETENTION_TIME_IN_DAYS EQ num
    )? (MAX_DATA_EXTENSION_TIME_IN_DAYS EQ num)? defaultDdlCollation? withTags? commentClause?
    ;

cloneAtBefore
    : CLONE id (
        atBefore1 L_PAREN (TIMESTAMP ASSOC string | OFFSET ASSOC string | STATEMENT ASSOC id) R_PAREN
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
    : CREATE orReplace? DYNAMIC TABLE id TARGET_LAG EQ (string | DOWNSTREAM) WAREHOUSE EQ wh = id AS queryStatement
    ;

createEventTable
    : CREATE orReplace? EVENT TABLE ifNotExists? id clusterBy? (DATA_RETENTION_TIME_IN_DAYS EQ num)? (
        MAX_DATA_EXTENSION_TIME_IN_DAYS EQ num
    )? changeTracking? (DEFAULT_DDL_COLLATION_ EQ string)? copyGrants? withRowAccessPolicy? withTags? (
        WITH? commentClause
    )?
    ;

createExternalFunction
    : CREATE orReplace? SECURE? EXTERNAL FUNCTION objectName L_PAREN (
        argName argDataType (COMMA argName argDataType)*
    )? R_PAREN RETURNS dataType nullNotNull? (
        ( CALLED ON NULL_ INPUT)
        | ((RETURNS NULL_ ON NULL_ INPUT) | STRICT)
    )? (VOLATILE | IMMUTABLE)? commentClause? API_INTEGRATION EQ id (
        HEADERS EQ L_PAREN headerDecl (COMMA headerDecl)* R_PAREN
    )? (CONTEXT_HEADERS EQ L_PAREN id (COMMA id)* R_PAREN)? (MAX_BATCH_ROWS EQ num)? compression? (
        REQUEST_TRANSLATOR EQ id
    )? (RESPONSE_TRANSLATOR EQ id)? AS string
    ;

createExternalTable
    // Partitions computed from expressions
    : CREATE orReplace? EXTERNAL TABLE ifNotExists? objectName L_PAREN externalTableColumnDeclList R_PAREN cloudProviderParams3? partitionBy? WITH?
        LOCATION EQ namedStage (REFRESH_ON_CREATE EQ trueFalse)? (AUTO_REFRESH EQ trueFalse)? pattern? fileFormat (
        AWS_SNS_TOPIC EQ string
    )? copyGrants? withRowAccessPolicy? withTags? commentClause?
    // Partitions added and removed manually
    | CREATE orReplace? EXTERNAL TABLE ifNotExists? objectName L_PAREN externalTableColumnDeclList R_PAREN cloudProviderParams3? partitionBy? WITH?
        LOCATION EQ namedStage PARTITION_TYPE EQ USER_SPECIFIED fileFormat copyGrants? withRowAccessPolicy? withTags? commentClause?
    // Delta Lake
    | CREATE orReplace? EXTERNAL TABLE ifNotExists? objectName L_PAREN externalTableColumnDeclList R_PAREN cloudProviderParams3? partitionBy? WITH?
        LOCATION EQ namedStage PARTITION_TYPE EQ USER_SPECIFIED fileFormat (TABLE_FORMAT EQ DELTA)? copyGrants? withRowAccessPolicy? withTags?
        commentClause?
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
    : CREATE FAILOVER GROUP ifNotExists? id OBJECT_TYPES EQ objectType (COMMA objectType)* (
        ALLOWED_DATABASES EQ id (COMMA id)*
    )? (ALLOWED_SHARES EQ id (COMMA id)*)? (
        ALLOWED_INTEGRATION_TYPES EQ integrationTypeName (COMMA integrationTypeName)*
    )? ALLOWED_ACCOUNTS EQ fullAcct (COMMA fullAcct)* (IGNORE EDITION CHECK)? (
        REPLICATION_SCHEDULE EQ string
    )?
    //      Secondary Replication Group
    | CREATE FAILOVER GROUP ifNotExists? id AS REPLICA OF id DOT id DOT id
    ;

typeFileformat
    : CSV
    | JSON
    | AVRO
    | ORC
    | PARQUET
    | XML
    | CSV_Q
    | JSON_Q
    | AVRO_Q
    | ORC_Q
    | PARQUET_Q
    | XML_Q
    ;

createFileFormat
    : CREATE orReplace? FILE FORMAT ifNotExists? objectName (TYPE EQ typeFileformat)? formatTypeOptions* commentClause?
    ;

argDecl: argName argDataType argDefaultValueClause?
    ;

argDefaultValueClause: DEFAULT expr
    ;

colDecl: columnName dataType virtualColumnDecl?
    ;

virtualColumnDecl: AS L_PAREN functionCall R_PAREN
    ;

functionDefinition: string | DBL_DOLLAR
    ;

createFunction
    : CREATE orReplace? SECURE? FUNCTION ifNotExists? objectName L_PAREN (argDecl (COMMA argDecl)*)? R_PAREN RETURNS (
        dataType
        | TABLE L_PAREN (colDecl (COMMA colDecl)*)? R_PAREN
    ) (LANGUAGE (JAVA | PYTHON | JAVASCRIPT | SCALA | SQL))? (
        CALLED ON NULL_ INPUT
        | RETURNS NULL_ ON NULL_ INPUT
        | STRICT
    )? (VOLATILE | IMMUTABLE)? (PACKAGES EQ L_PAREN stringList R_PAREN)? (
        RUNTIME_VERSION EQ (string | FLOAT)
    )? (IMPORTS EQ L_PAREN stringList R_PAREN)? (PACKAGES EQ L_PAREN stringList R_PAREN)? (
        HANDLER EQ string
    )? nullNotNull? commentClause? AS functionDefinition
    | CREATE orReplace? SECURE? FUNCTION objectName L_PAREN (argDecl (COMMA argDecl)*)? R_PAREN RETURNS (
        dataType
        | TABLE L_PAREN (colDecl (COMMA colDecl)*)? R_PAREN
    ) nullNotNull? (CALLED ON NULL_ INPUT | RETURNS NULL_ ON NULL_ INPUT | STRICT)? (
        VOLATILE
        | IMMUTABLE
    )? MEMOIZABLE? commentClause? AS functionDefinition
    ;

createManagedAccount
    : CREATE MANAGED ACCOUNT id ADMIN_NAME EQ id COMMA ADMIN_PASSWORD EQ string COMMA TYPE EQ READER (
        COMMA commentClause
    )?
    ;

createMaskingPolicy
    : CREATE orReplace? MASKING POLICY ifNotExists? objectName AS L_PAREN argName argDataType (
        COMMA argName argDataType
    )? R_PAREN RETURNS argDataType ARROW expr commentClause?
    ;

tagDecl: objectName EQ string
    ;

columnListInParentheses: L_PAREN columnList R_PAREN
    ;

createMaterializedView
    : CREATE orReplace? SECURE? MATERIALIZED VIEW ifNotExists? objectName (
        L_PAREN columnListWithComment R_PAREN
    )? viewCol* withRowAccessPolicy? withTags? copyGrants? commentClause? clusterBy? AS selectStatement
    //NOTA MATERIALIZED VIEW accept only simple select statement at this time
    ;

createNetworkPolicy
    : CREATE orReplace? NETWORK POLICY id ALLOWED_IP_LIST EQ L_PAREN stringList? R_PAREN (
        BLOCKED_IP_LIST EQ L_PAREN stringList? R_PAREN
    )? commentClause?
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
    : CREATE orReplace? NOTIFICATION INTEGRATION ifNotExists? id ENABLED EQ trueFalse TYPE EQ QUEUE cloudProviderParamsAuto commentClause?
    | CREATE orReplace? NOTIFICATION INTEGRATION ifNotExists? id ENABLED EQ trueFalse DIRECTION EQ OUTBOUND TYPE EQ QUEUE cloudProviderParamsPush
        commentClause?
    ;

createPipe
    : CREATE orReplace? PIPE ifNotExists? objectName (AUTO_INGEST EQ trueFalse)? (
        ERROR_INTEGRATION EQ id
    )? (AWS_SNS_TOPIC EQ string)? (INTEGRATION EQ string)? commentClause? AS copyIntoTable
    ;

callerOwner: CALLER | OWNER
    ;

executaAs: EXECUTE AS callerOwner
    ;

procedureDefinition: string | DBL_DOLLAR
    ;

notNull: NOT NULL_
    ;

createProcedure
    : CREATE orReplace? PROCEDURE objectName L_PAREN (argDecl (COMMA argDecl)*)? R_PAREN RETURNS (
        dataType
        | TABLE L_PAREN (colDecl (COMMA colDecl)*)? R_PAREN
    ) notNull? LANGUAGE SQL (CALLED ON NULL_ INPUT | RETURNS NULL_ ON NULL_ INPUT | STRICT)? (
        VOLATILE
        | IMMUTABLE
    )? // Note: VOLATILE and IMMUTABLE are deprecated.
    commentClause? executaAs? AS procedureDefinition
    | CREATE orReplace? SECURE? PROCEDURE objectName L_PAREN (argDecl (COMMA argDecl)*)? R_PAREN RETURNS dataType notNull? LANGUAGE JAVASCRIPT (
        CALLED ON NULL_ INPUT
        | RETURNS NULL_ ON NULL_ INPUT
        | STRICT
    )? (VOLATILE | IMMUTABLE)? // Note: VOLATILE and IMMUTABLE are deprecated.
    commentClause? executaAs? AS procedureDefinition
    | CREATE orReplace? SECURE? PROCEDURE objectName L_PAREN (argDecl (COMMA argDecl)*)? R_PAREN RETURNS (
        dataType notNull?
        | TABLE L_PAREN (colDecl (COMMA colDecl)*)? R_PAREN
    ) LANGUAGE PYTHON RUNTIME_VERSION EQ string (IMPORTS EQ L_PAREN stringList R_PAREN)? PACKAGES EQ L_PAREN stringList R_PAREN HANDLER EQ string
    //            ( CALLED ON NULL_ INPUT | RETURNS NULL_ ON NULL_ INPUT | STRICT )?
    //            ( VOLATILE | IMMUTABLE )? // Note: VOLATILE and IMMUTABLE are deprecated.
    commentClause? executaAs? AS procedureDefinition
    ;

createReplicationGroup
    : CREATE REPLICATION GROUP ifNotExists? id OBJECT_TYPES EQ objectType (COMMA objectType)* (
        ALLOWED_DATABASES EQ id (COMMA id)*
    )? (ALLOWED_SHARES EQ id (COMMA id)*)? (
        ALLOWED_INTEGRATION_TYPES EQ integrationTypeName (COMMA integrationTypeName)*
    )? ALLOWED_ACCOUNTS EQ fullAcct (COMMA fullAcct)* (IGNORE EDITION CHECK)? (
        REPLICATION_SCHEDULE EQ string
    )?
    //Secondary Replication Group
    | CREATE REPLICATION GROUP ifNotExists? id AS REPLICA OF id DOT id DOT id
    ;

createResourceMonitor
    : CREATE orReplace? RESOURCE MONITOR id WITH creditQuota? frequency? (
        START_TIMESTAMP EQ ( string | IMMEDIATELY)
    )? (END_TIMESTAMP EQ string)? notifyUsers? (TRIGGERS triggerDefinition+)?
    ;

createRole: CREATE orReplace? ROLE ifNotExists? id withTags? commentClause?
    ;

createRowAccessPolicy
    : CREATE orReplace? ROW ACCESS POLICY ifNotExists? id AS L_PAREN argDecl (COMMA argDecl)* R_PAREN RETURNS BOOLEAN ARROW expr commentClause?
    ;

createSchema
    : CREATE orReplace? TRANSIENT? SCHEMA ifNotExists? schemaName cloneAtBefore? (
        WITH MANAGED ACCESS
    )? (DATA_RETENTION_TIME_IN_DAYS EQ num)? (MAX_DATA_EXTENSION_TIME_IN_DAYS EQ num)? defaultDdlCollation? withTags? commentClause?
    ;

createSecurityIntegrationExternalOauth
    : CREATE orReplace? SECURITY INTEGRATION ifNotExists? id TYPE EQ EXTERNAL_OAUTH ENABLED EQ trueFalse EXTERNAL_OAUTH_TYPE EQ (
        OKTA
        | AZURE
        | PING_FEDERATE
        | CUSTOM
    ) EXTERNAL_OAUTH_ISSUER EQ string EXTERNAL_OAUTH_TOKEN_USER_MAPPING_CLAIM EQ (
        string
        | L_PAREN stringList R_PAREN
    ) EXTERNAL_OAUTH_SNOWFLAKE_USER_MAPPING_ATTRIBUTE EQ string (
        EXTERNAL_OAUTH_JWS_KEYS_URL EQ string
    )?                                                                      // For OKTA | PING_FEDERATE | CUSTOM
    (EXTERNAL_OAUTH_JWS_KEYS_URL EQ (string | L_PAREN stringList R_PAREN))? // For Azure
    (EXTERNAL_OAUTH_BLOCKED_ROLES_LIST EQ L_PAREN stringList R_PAREN)? (
        EXTERNAL_OAUTH_ALLOWED_ROLES_LIST EQ L_PAREN stringList R_PAREN
    )? (EXTERNAL_OAUTH_RSA_PUBLIC_KEY EQ string)? (EXTERNAL_OAUTH_RSA_PUBLIC_KEY_2 EQ string)? (
        EXTERNAL_OAUTH_AUDIENCE_LIST EQ L_PAREN string R_PAREN
    )? (EXTERNAL_OAUTH_ANY_ROLE_MODE EQ (DISABLE | ENABLE | ENABLE_FOR_PRIVILEGE))? (
        EXTERNAL_OAUTH_SCOPE_DELIMITER EQ string
    )? // Only for EXTERNAL_OAUTH_TYPE EQ CUSTOM
    ;

implicitNone: IMPLICIT | NONE
    ;

createSecurityIntegrationSnowflakeOauth
    : CREATE orReplace? SECURITY INTEGRATION ifNotExists? id TYPE EQ OAUTH OAUTH_CLIENT EQ partnerApplication OAUTH_REDIRECT_URI EQ string
    //Required when OAUTH_CLIENTEQLOOKER
    enabledTrueFalse? (OAUTH_ISSUE_REFRESH_TOKENS EQ trueFalse)? (
        OAUTH_REFRESH_TOKEN_VALIDITY EQ num
    )? (OAUTH_USE_SECONDARY_ROLES EQ implicitNone)? (
        BLOCKED_ROLES_LIST EQ L_PAREN stringList R_PAREN
    )? commentClause?
    // Snowflake OAuth for custom clients
    | CREATE orReplace? SECURITY INTEGRATION ifNotExists? id TYPE EQ OAUTH OAUTH_CLIENT EQ CUSTOM
    //OAUTH_CLIENT_TYPE EQ 'CONFIDENTIAL' | 'PUBLIC'
    OAUTH_REDIRECT_URI EQ string enabledTrueFalse? (OAUTH_ALLOW_NON_TLS_REDIRECT_URI EQ trueFalse)? (
        OAUTH_ENFORCE_PKCE EQ trueFalse
    )? (OAUTH_USE_SECONDARY_ROLES EQ implicitNone)? (
        PRE_AUTHORIZED_ROLES_LIST EQ L_PAREN stringList R_PAREN
    )? (BLOCKED_ROLES_LIST EQ L_PAREN stringList R_PAREN)? (
        OAUTH_ISSUE_REFRESH_TOKENS EQ trueFalse
    )? (OAUTH_REFRESH_TOKEN_VALIDITY EQ num)? networkPolicy? (
        OAUTH_CLIENT_RSA_PUBLIC_KEY EQ string
    )? (OAUTH_CLIENT_RSA_PUBLIC_KEY_2 EQ string)? commentClause?
    ;

createSecurityIntegrationSaml2
    : CREATE orReplace? SECURITY INTEGRATION ifNotExists? TYPE EQ SAML2 enabledTrueFalse SAML2_ISSUER EQ string SAML2_SSO_URL EQ string SAML2_PROVIDER
        EQ string SAML2_X509_CERT EQ string (SAML2_SP_INITIATED_LOGIN_PAGE_LABEL EQ string)? (
        SAML2_ENABLE_SP_INITIATED EQ trueFalse
    )? (SAML2_SNOWFLAKE_X509_CERT EQ string)? (SAML2_SIGN_REQUEST EQ trueFalse)? (
        SAML2_REQUESTED_NAMEID_FORMAT EQ string
    )? (SAML2_POST_LOGOUT_REDIRECT_URL EQ string)? (SAML2_FORCE_AUTHN EQ trueFalse)? (
        SAML2_SNOWFLAKE_ISSUER_URL EQ string
    )? (SAML2_SNOWFLAKE_ACS_URL EQ string)?
    ;

createSecurityIntegrationScim
    : CREATE orReplace? SECURITY INTEGRATION ifNotExists? id TYPE EQ SCIM SCIM_CLIENT EQ (
        OKTA_Q
        | AZURE_Q
        | GENERIC_Q
    ) RUN_AS_ROLE EQ (OKTA_PROVISIONER_Q | AAD_PROVISIONER_Q | GENERIC_SCIM_PROVISIONER_Q) networkPolicy? (
        SYNC_PASSWORD EQ trueFalse
    )? commentClause?
    ;

networkPolicy: NETWORK_POLICY EQ string
    ;

partnerApplication: TABLEAU_DESKTOP | TABLEAU_SERVER | LOOKER
    ;

startWith: START WITH? EQ? num
    ;

incrementBy: INCREMENT BY? EQ? num
    ;

createSequence
    : CREATE orReplace? SEQUENCE ifNotExists? objectName WITH? startWith? incrementBy? orderNoorder? commentClause?
    ;

createSessionPolicy
    : CREATE orReplace? SESSION POLICY ifExists? id (SESSION_IDLE_TIMEOUT_MINS EQ num)? (
        SESSION_UI_IDLE_TIMEOUT_MINS EQ num
    )? commentClause?
    ;

createShare: CREATE orReplace? SHARE id commentClause?
    ;

character
    : CHAR_LITERAL
    | AAD_PROVISIONER_Q
    | ARRAY_Q
    | AUTO_Q
    | AVRO_Q
    | AZURE_CSE_Q
    | AZURE_Q
    | BOTH_Q
    | CSV_Q
    | GCS_SSE_KMS_Q
    | GENERIC_Q
    | GENERIC_SCIM_PROVISIONER_Q
    | JSON_Q
    | NONE_Q
    | OBJECT_Q
    | OKTA_PROVISIONER_Q
    | OKTA_Q
    | ORC_Q
    | PARQUET_Q
    | S3
    | SNOWPARK_OPTIMIZED
    | XML_Q
    ;

formatTypeOptions
    //-- If TYPE EQ CSV
    : COMPRESSION EQ (AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE | AUTO_Q)
    | RECORD_DELIMITER EQ ( string | NONE)
    | FIELD_DELIMITER EQ ( string | NONE)
    | FILE_EXTENSION EQ string
    | SKIP_HEADER EQ num
    | SKIP_BLANK_LINES EQ trueFalse
    | DATE_FORMAT EQ (string | AUTO)
    | TIME_FORMAT EQ (string | AUTO)
    | TIMESTAMP_FORMAT EQ (string | AUTO)
    | BINARY_FORMAT EQ (HEX | BASE64 | UTF8)
    | ESCAPE EQ (character | NONE | NONE_Q)
    | ESCAPE_UNENCLOSED_FIELD EQ (string | NONE | NONE_Q)
    | TRIM_SPACE EQ trueFalse
    | FIELD_OPTIONALLY_ENCLOSED_BY EQ (string | NONE | NONE_Q)
    | NULL_IF EQ L_PAREN stringList R_PAREN
    | ERROR_ON_COLUMN_COUNT_MISMATCH EQ trueFalse
    | REPLACE_INVALID_CHARACTERS EQ trueFalse
    | EMPTY_FIELD_AS_NULL EQ trueFalse
    | SKIP_BYTE_ORDER_MARK EQ trueFalse
    | ENCODING EQ (string | UTF8) //by the way other encoding keyword are valid ie WINDOWS1252
    //-- If TYPE EQ JSON
    //| COMPRESSION EQ (AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE)
    //    | DATE_FORMAT EQ string | AUTO
    //    | TIME_FORMAT EQ string | AUTO
    //    | TIMESTAMP_FORMAT EQ string | AUTO
    //    | BINARY_FORMAT EQ HEX | BASE64 | UTF8
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
    | SIZE_LIMIT EQ num
    | PURGE EQ trueFalse
    | RETURN_FAILED_ONLY EQ trueFalse
    | MATCH_BY_COLUMN_NAME EQ CASE_SENSITIVE
    | CASE_INSENSITIVE
    | NONE
    | ENFORCE_LENGTH EQ trueFalse
    | TRUNCATECOLUMNS EQ trueFalse
    | FORCE EQ trueFalse
    ;

stageEncryptionOptsInternal
    : ENCRYPTION EQ L_PAREN TYPE EQ (SNOWFLAKE_FULL | SNOWFLAKE_SSE) R_PAREN
    ;

storageIntegrationEqId: STORAGE_INTEGRATION EQ id
    ;

storageCredentials: CREDENTIALS EQ parenStringOptions
    ;

storageEncryption: ENCRYPTION EQ parenStringOptions
    ;

parenStringOptions: L_PAREN stringOption* R_PAREN
    ;

stringOption: id EQ STRING
    ;

externalStageParams: URL EQ STRING storageIntegrationEqId? storageCredentials? storageEncryption?
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
    : DIRECTORY EQ L_PAREN (
        enable refreshOnCreate?
        | REFRESH_ON_CREATE EQ FALSE
        | refreshOnCreate enable
    ) R_PAREN
    ;

directoryTableExternalParams
    // (for Amazon S3)
    : DIRECTORY EQ L_PAREN enable refreshOnCreate? autoRefresh? R_PAREN
    // (for Google Cloud Storage)
    | DIRECTORY EQ L_PAREN enable autoRefresh? refreshOnCreate? notificationIntegration? R_PAREN
    // (for Microsoft Azure)
    | DIRECTORY EQ L_PAREN enable refreshOnCreate? autoRefresh? notificationIntegration? R_PAREN
    ;

/* ===========  Stage DDL section =========== */
createStage
    : CREATE orReplace? temporary? STAGE ifNotExists? objectNameOrIdentifier stageEncryptionOptsInternal? directoryTableInternalParams? (
        FILE_FORMAT EQ L_PAREN (FORMAT_NAME EQ string | TYPE EQ typeFileformat formatTypeOptions*) R_PAREN
    )? (COPY_OPTIONS_ EQ L_PAREN copyOptions R_PAREN)? withTags? commentClause?
    | CREATE orReplace? temporary? STAGE ifNotExists? objectNameOrIdentifier externalStageParams directoryTableExternalParams? (
        FILE_FORMAT EQ L_PAREN (FORMAT_NAME EQ string | TYPE EQ typeFileformat formatTypeOptions*) R_PAREN
    )? (COPY_OPTIONS_ EQ L_PAREN copyOptions R_PAREN)? withTags? commentClause?
    ;

alterStage
    : ALTER STAGE ifExists? objectNameOrIdentifier RENAME TO objectNameOrIdentifier
    | ALTER STAGE ifExists? objectNameOrIdentifier setTags
    | ALTER STAGE ifExists? objectNameOrIdentifier unsetTags
    | ALTER STAGE ifExists? objectNameOrIdentifier SET externalStageParams? fileFormat? (
        COPY_OPTIONS_ EQ L_PAREN copyOptions R_PAREN
    )? commentClause?
    ;

dropStage: DROP STAGE ifExists? objectNameOrIdentifier
    ;

describeStage: describe STAGE objectNameOrIdentifier
    ;

showStages: SHOW STAGES likePattern? inObj?
    ;

/* ===========  End of stage DDL section =========== */

cloudProviderParams
    //(for Amazon S3)
    : STORAGE_PROVIDER EQ S3 STORAGE_AWS_ROLE_ARN EQ string (STORAGE_AWS_OBJECT_ACL EQ string)?
    //(for Google Cloud Storage)
    | STORAGE_PROVIDER EQ GCS
    //(for Microsoft Azure)
    | STORAGE_PROVIDER EQ AZURE AZURE_TENANT_ID EQ string
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
    : CREATE orReplace? STORAGE INTEGRATION ifNotExists? id TYPE EQ EXTERNAL_STAGE cloudProviderParams ENABLED EQ trueFalse STORAGE_ALLOWED_LOCATIONS
        EQ L_PAREN stringList R_PAREN (STORAGE_BLOCKED_LOCATIONS EQ L_PAREN stringList R_PAREN)? commentClause?
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
    : atBefore1 L_PAREN (
        TIMESTAMP ASSOC string
        | OFFSET ASSOC string
        | STATEMENT ASSOC id
        | STREAM ASSOC string
    ) R_PAREN
    ;

createStream
    //-- table
    : CREATE orReplace? STREAM ifNotExists? objectName copyGrants? ON TABLE objectName streamTime? appendOnly? showInitialRows? commentClause?
    //-- External table
    | CREATE orReplace? STREAM ifNotExists? objectName copyGrants? ON EXTERNAL TABLE objectName streamTime? insertOnly? commentClause?
    //-- Directory table
    | CREATE orReplace? STREAM ifNotExists? objectName copyGrants? ON STAGE objectName commentClause?
    //-- View
    | CREATE orReplace? STREAM ifNotExists? objectName copyGrants? ON VIEW objectName streamTime? appendOnly? showInitialRows? commentClause?
    ;

temporary: TEMP | TEMPORARY
    ;

tableType: (( LOCAL | GLOBAL)? temporary | VOLATILE) | TRANSIENT
    ;

withTags: WITH? TAG L_PAREN tagDecl (COMMA tagDecl)* R_PAREN
    ;

withRowAccessPolicy: WITH? ROW ACCESS POLICY id ON L_PAREN columnName (COMMA columnName)* R_PAREN
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
        L_PAREN num COMMA num R_PAREN
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
        | foreignKey columnListInParentheses REFERENCES objectName columnListInParentheses constraintProperties
    )
    ;

fullColDecl
    : colDecl (collate | inlineConstraint | nullNotNull | (defaultValue | NULL_))* withMaskingPolicy? withTags? (
        COMMENT string
    )?
    ;

columnDeclItem: fullColDecl | outOfLineConstraint
    ;

columnDeclItemList: columnDeclItem (COMMA columnDeclItem)*
    ;

createTable
    : CREATE orReplace? tableType? TABLE (ifNotExists? objectName | objectName ifNotExists?) (
        (commentClause? createTableClause)
        | (createTableClause commentClause?)
    )
    ;

columnDeclItemListParen: L_PAREN columnDeclItemList R_PAREN
    ;

createTableClause
    : (columnDeclItemListParen clusterBy? | clusterBy? commentClause? columnDeclItemListParen) stageFileFormat? (
        STAGE_COPY_OPTIONS EQ L_PAREN copyOptions R_PAREN
    )? (DATA_RETENTION_TIME_IN_DAYS EQ num)? (MAX_DATA_EXTENSION_TIME_IN_DAYS EQ num)? changeTracking? defaultDdlCollation? copyGrants? commentClause?
        withRowAccessPolicy? withTags?
    ;

createTableAsSelect
    : CREATE orReplace? tableType? TABLE (ifNotExists? objectName | objectName ifNotExists?) (
        L_PAREN columnDeclItemList R_PAREN
    )? clusterBy? copyGrants? withRowAccessPolicy? withTags? commentClause? AS queryStatement
    ;

createTableLike
    : CREATE orReplace? TRANSIENT? TABLE ifNotExists? objectName LIKE objectName clusterBy? copyGrants?
    ;

createTag: CREATE orReplace? TAG ifNotExists? objectName tagAllowedValues? commentClause?
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
    : CREATE orReplace? TASK ifNotExists? objectName taskParameters* commentClause? copyGrants? (
        AFTER objectName (COMMA objectName)*
    )? (WHEN predicate)? AS sql
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

taskTimeout: USER_TASK_TIMEOUT_MS EQ num
    ;

taskSuspendAfterFailureNumber: SUSPEND_TASK_AFTER_NUM_FAILURES EQ num
    ;

taskErrorIntegration: ERROR_INTEGRATION EQ id
    ;

taskOverlap: ALLOW_OVERLAPPING_EXECUTION EQ trueFalse
    ;

sql: EXECUTE IMMEDIATE DBL_DOLLAR | sqlCommand | call
    ;

call: CALL objectName L_PAREN exprList? R_PAREN
    ;

createUser: CREATE orReplace? USER ifNotExists? id objectProperties? objectParams? sessionParams?
    ;

viewCol: columnName withMaskingPolicy withTags
    ;

createView
    : CREATE orReplace? SECURE? RECURSIVE? VIEW ifNotExists? objectName (
        L_PAREN columnListWithComment R_PAREN
    )? viewCol* withRowAccessPolicy? withTags? copyGrants? commentClause? AS queryStatement
    ;

createWarehouse: CREATE orReplace? WAREHOUSE ifNotExists? idFn (WITH? whProperties+)? whParams*
    ;

whCommonSize: XSMALL | SMALL | MEDIUM | LARGE | XLARGE | XXLARGE
    ;

whExtraSize: XXXLARGE | X4LARGE | X5LARGE | X6LARGE
    ;

whProperties
    : WAREHOUSE_SIZE EQ (whCommonSize | whExtraSize | ID2)
    | WAREHOUSE_TYPE EQ (STANDARD | SNOWPARK_OPTIMIZED)
    | MAX_CLUSTER_COUNT EQ num
    | MIN_CLUSTER_COUNT EQ num
    | SCALING_POLICY EQ (STANDARD | ECONOMY)
    | AUTO_SUSPEND (EQ num | NULL_)
    | AUTO_RESUME EQ trueFalse
    | INITIALLY_SUSPENDED EQ trueFalse
    | RESOURCE_MONITOR EQ id
    | commentClause
    | ENABLE_QUERY_ACCELERATION EQ trueFalse
    | QUERY_ACCELERATION_MAX_SCALE_FACTOR EQ num
    | MAX_CONCURRENCY_LEVEL EQ num
    ;

whParams
    : MAX_CONCURRENCY_LEVEL EQ num
    | STATEMENT_QUEUED_TIMEOUT_IN_SECONDS EQ num
    | STATEMENT_TIMEOUT_IN_SECONDS EQ num withTags?
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

dropObject: DROP objectType ifExists id cascadeRestrict?
    ;

dropAlert: DROP ALERT id
    ;

dropConnection: DROP CONNECTION ifExists? id
    ;

dropDatabase: DROP DATABASE ifExists? id cascadeRestrict?
    ;

dropDynamicTable: DROP DYNAMIC TABLE id
    ;

dropExternalTable: DROP EXTERNAL TABLE ifExists? objectName cascadeRestrict?
    ;

dropFailoverGroup: DROP FAILOVER GROUP ifExists? id
    ;

dropFileFormat: DROP FILE FORMAT ifExists? id
    ;

dropFunction: DROP FUNCTION ifExists? objectName argTypes
    ;

dropIntegration: DROP (API | NOTIFICATION | SECURITY | STORAGE)? INTEGRATION ifExists? id
    ;

dropManagedAccount: DROP MANAGED ACCOUNT id
    ;

dropMaskingPolicy: DROP MASKING POLICY id
    ;

dropMaterializedView: DROP MATERIALIZED VIEW ifExists? objectName
    ;

dropNetworkPolicy: DROP NETWORK POLICY ifExists? id
    ;

dropPipe: DROP PIPE ifExists? objectName
    ;

dropProcedure: DROP PROCEDURE ifExists? objectName argTypes
    ;

dropReplicationGroup: DROP REPLICATION GROUP ifExists? id
    ;

dropResourceMonitor: DROP RESOURCE MONITOR id
    ;

dropRole: DROP ROLE ifExists? id
    ;

dropRowAccessPolicy: DROP ROW ACCESS POLICY ifExists? id
    ;

dropSchema: DROP SCHEMA ifExists? schemaName cascadeRestrict?
    ;

dropSequence: DROP SEQUENCE ifExists? objectName cascadeRestrict?
    ;

dropSessionPolicy: DROP SESSION POLICY ifExists? id
    ;

dropShare: DROP SHARE id
    ;

dropStream: DROP STREAM ifExists? objectName
    ;

dropTable: DROP TABLE ifExists? objectName cascadeRestrict?
    ;

dropTag: DROP TAG ifExists? objectName
    ;

dropTask: DROP TASK ifExists? objectName
    ;

dropUser: DROP USER ifExists? id
    ;

dropView: DROP VIEW ifExists? objectName
    ;

dropWarehouse: DROP WAREHOUSE ifExists? idFn
    ;

cascadeRestrict: CASCADE | RESTRICT
    ;

argTypes: L_PAREN dataTypeList? R_PAREN
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

undropTable: UNDROP TABLE objectName
    ;

undropTag: UNDROP TAG objectName
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

/* */
commentClause: COMMENT EQ string
    ;

ifSuspended: IF SUSPENDED
    ;

ifExists: IF EXISTS
    ;

ifNotExists: IF NOT EXISTS
    ;

orReplace: OR REPLACE
    ;

describe: DESC | DESCRIBE
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

describeAlert: describe ALERT id
    ;

describeDatabase: describe DATABASE id
    ;

describeDynamicTable: describe DYNAMIC TABLE id
    ;

describeEventTable: describe EVENT TABLE id
    ;

describeExternalTable: describe EXTERNAL? TABLE objectName (TYPE EQ (COLUMNS | STAGE))?
    ;

describeFileFormat: describe FILE FORMAT id
    ;

describeFunction: describe FUNCTION objectName argTypes
    ;

describeIntegration: describe (API | NOTIFICATION | SECURITY | STORAGE)? INTEGRATION id
    ;

describeMaskingPolicy: describe MASKING POLICY id
    ;

describeMaterializedView: describe MATERIALIZED VIEW objectName
    ;

describeNetworkPolicy: describe NETWORK POLICY id
    ;

describePipe: describe PIPE objectName
    ;

describeProcedure: describe PROCEDURE objectName argTypes
    ;

describeResult: describe RESULT (STRING | LAST_QUERY_ID L_PAREN R_PAREN)
    ;

describeRowAccessPolicy: describe ROW ACCESS POLICY id
    ;

describeSchema: describe SCHEMA schemaName
    ;

describeSearchOptimization: describe SEARCH OPTIMIZATION ON objectName
    ;

describeSequence: describe SEQUENCE objectName
    ;

describeSessionPolicy: describe SESSION POLICY id
    ;

describeShare: describe SHARE id
    ;

describeStream: describe STREAM objectName
    ;

describeTable: describe TABLE objectName (TYPE EQ (COLUMNS | STAGE))?
    ;

describeTask: describe TASK objectName
    ;

describeTransaction: describe TRANSACTION num
    ;

describeUser: describe USER id
    ;

describeView: describe VIEW objectName
    ;

describeWarehouse: describe WAREHOUSE id
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
        IN (ACCOUNT | DATABASE id? | SCHEMA schemaName? | TABLE | TABLE? objectName)
    )?
    ;

showColumns
    : SHOW COLUMNS likePattern? (
        IN (
            ACCOUNT
            | DATABASE id?
            | SCHEMA schemaName?
            | TABLE
            | TABLE? objectName
            | VIEW
            | VIEW? objectName
        )
    )?
    ;

showConnections: SHOW CONNECTIONS likePattern?
    ;

startsWith: STARTS WITH string
    ;

limitRows: LIMIT num (FROM string)?
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
    | ON objectType objectName
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

inObj2: IN (ACCOUNT | DATABASE id? | SCHEMA schemaName? | TABLE | TABLE objectName)
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
            | TABLE objectName
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

showReplicationDatabases
    : SHOW REPLICATION DATABASES likePattern? (WITH PRIMARY accountIdentifier DOT id)?
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

showUsers: SHOW TERSE? USERS likePattern? (STARTS WITH string)? (LIMIT num)? (FROM string)?
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

//names
accountIdentifier: id
    ;

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

tagValue: string
    ;

argDataType: dataType
    ;

argName: id
    ;

paramName: id
    ;

regionGroupId: id
    ;

snowflakeRegionId: id
    ;

string: STRING
    ;

stringList: string (COMMA string)*
    ;

idFn: id | IDENTIFIER L_PAREN id R_PAREN
    ;

id
    : ID
    | ID2
    | DOUBLE_QUOTE_ID
    | DOUBLE_QUOTE_BLANK
    | nonReservedWords //id is used for object name. Snowflake is very permissive
    ;

nonReservedWords
    //List here lexer token referenced by rules which is not a keyword (SnowSQL Meaning) and allowed as object name
    : ACCOUNTADMIN
    | ACTION
    | ACTION
    | AES
    | ALERT
    | ARRAY
    | ARRAY_AGG
    | AT_KEYWORD
    | CHECKSUM
    | CLUSTER
    | COLLATE
    | COLLECTION
    | COMMENT
    | CONDITION
    | CONFIGURATION
    | COPY_OPTIONS_
    | DATA
    | DATE
    | DATE_FORMAT
    | DEFINITION
    | DELTA
    | DENSE_RANK
    | DIRECTION
    | DOWNSTREAM
    | DUMMY
    | DYNAMIC
    | EDITION
    | END
    | EMAIL
    | EVENT
    | EXCHANGE
    | EXPIRY_DATE
    | FIRST
    | FIRST_NAME
    | FLATTEN
    | FLOOR
    | FUNCTION
    | GET
    | GLOBAL
    | IDENTIFIER
    | IDENTITY
    | IF
    | INDEX
    | INPUT
    | INTERVAL
    | JAVASCRIPT
    | KEY
    | KEYS
    | LANGUAGE
    | LAST_NAME
    | LAST_QUERY_ID
    | LEAD
    | LENGTH
    | LOCAL
    | MAX_CONCURRENCY_LEVEL
    | MODE
    | NAME
    | NETWORK
    | NOORDER
    | OFFSET
    | OPTION
    | ORDER
    | ORGADMIN
    | OUTBOUND
    | OUTER
    | PARTITION
    | PATH_
    | PATTERN
    | PORT
    | PROCEDURE_NAME
    | PROPERTY
    | PROVIDER
    | PUBLIC
    | RANK
    | RECURSIVE
    | REGION
    | REPLACE
    | RESOURCE
    | RESOURCES
    | RESPECT
    | RESTRICT
    | RESULT
    | RLIKE
    | ROLE
    | ROLLUP
    | SECURITYADMIN
    | SHARES
    | SOURCE
    | STAGE
    | START
    | STATE
    | STATS
    | SYSADMIN
    | TABLE
    | TAG
    | TAGS
    | TARGET_LAG
    | TEMP
    | TIME
    | TIMESTAMP
    | TIMEZONE
    | TYPE
    | URL
    | USER
    | USERADMIN
    | VALUE
    | VALUES
    | VERSION
    | WAREHOUSE
    | WAREHOUSE_TYPE
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

objectName: id (DOT id)*
    ;

objectNameOrIdentifier: objectName | IDENTIFIER L_PAREN string R_PAREN
    ;

num: DECIMAL
    ;

/*** expressions ***/
exprList: expr (COMMA expr)*
    ;

expr
    : objectName DOT NEXTVAL                    # exprNextval
    | expr DOT expr                             # exprDot
    | expr COLON expr                           # exprColon
    | expr COLLATE string                       # exprCollate
    | caseExpression                            # exprCase
    | iffExpr                                   # exprIff
    | bracketExpression                         # exprBracket
    | sign expr                                 # exprSign
    | expr op = (STAR | DIVIDE | MODULE) expr   # exprPrecedence0
    | expr op = (PLUS | MINUS | PIPE_PIPE) expr # exprPrecedence1
    | expr comparisonOperator expr              # exprComparison
    | op = NOT+ expr                            # exprNot
    | expr AND expr                             # exprAnd
    | expr OR expr                              # exprOr
    | expr withinGroup                          # exprWithinGroup
    | expr overClause                           # exprOver
    | castExpr                                  # exprCast
    | expr COLON_COLON dataType                 # exprAscribe
    | functionCall                              # exprFuncCall
    | L_PAREN subquery R_PAREN                  # exprSubquery
    | expr predicatePartial                     # exprPredicate
    | DISTINCT expr                             # exprDistinct
    //Should be latest rule as it's nearly a catch all
    | primitiveExpression # exprPrimitive
    ;

withinGroup: WITHIN GROUP L_PAREN orderByClause R_PAREN
    ;

predicatePartial
    : IS nullNotNull
    | NOT? IN L_PAREN (subquery | exprList) R_PAREN
    | NOT? ( LIKE | ILIKE) expr (ESCAPE expr)?
    | NOT? RLIKE expr
    | NOT? (LIKE | ILIKE) ANY L_PAREN expr (COMMA expr)* R_PAREN (ESCAPE expr)?
    | NOT? BETWEEN expr AND expr
    ;

jsonPath: jsonPathElem (DOT jsonPathElem)*
    ;

jsonPathElem: ID | DOUBLE_QUOTE_ID (LSB (string | num) RSB)?
    ;

iffExpr: IFF L_PAREN predicate COMMA expr COMMA expr R_PAREN
    ;

castExpr: castOp = (TRY_CAST | CAST) L_PAREN expr AS dataType R_PAREN | INTERVAL expr
    ;

jsonLiteral: LCB kvPair (COMMA kvPair)* RCB | LCB RCB
    ;

kvPair: key = STRING COLON literal
    ;

arrayLiteral: LSB literal (COMMA literal)* RSB | LSB RSB
    ;

dataTypeSize: L_PAREN num R_PAREN
    ;

dataType
    : intAlias = (INT | INTEGER | SMALLINT | TINYINT | BYTEINT | BIGINT)
    | numberAlias = (NUMBER | NUMERIC | DECIMAL_) (L_PAREN num (COMMA num)? R_PAREN)?
    | floatAlias = (FLOAT_ | FLOAT4 | FLOAT8 | DOUBLE | DOUBLE_PRECISION | REAL_)
    | BOOLEAN
    | DATE
    | DATETIME dataTypeSize?
    | TIME dataTypeSize?
    | TIMESTAMP dataTypeSize?
    | TIMESTAMP_LTZ dataTypeSize?
    | TIMESTAMP_NTZ dataTypeSize?
    | TIMESTAMP_TZ dataTypeSize?
    | charAlias = ( CHAR | NCHAR | CHARACTER) dataTypeSize?
    | varcharAlias = (
        CHAR_VARYING
        | NCHAR_VARYING
        | NVARCHAR2
        | NVARCHAR
        | STRING_
        | TEXT
        | VARCHAR
    ) dataTypeSize?
    | binaryAlias = ( BINARY | VARBINARY) dataTypeSize?
    | VARIANT
    | OBJECT
    | ARRAY
    | GEOGRAPHY
    | GEOMETRY
    ;

primitiveExpression
    : DEFAULT           # primExprDefault //?
    | id LSB num RSB    # primArrayAccess
    | id LSB string RSB # primObjectAccess
    | id                # primExprColumn
    | literal           # primExprLiteral
    | BOTH_Q            # primExprBoth
    | ARRAY_Q           # primExprArray
    | OBJECT_Q          # primExprObject
    ;

overClause: OVER L_PAREN (PARTITION BY expr (COMMA expr)*)? windowOrderingAndFrame? R_PAREN
    ;

windowOrderingAndFrame: orderByClause rowOrRangeClause?
    ;

rowOrRangeClause: (ROWS | RANGE) windowFrameExtent
    ;

windowFrameExtent: BETWEEN windowFrameBound AND windowFrameBound
    ;

windowFrameBound: UNBOUNDED (PRECEDING | FOLLOWING) | num (PRECEDING | FOLLOWING) | CURRENT ROW
    ;

functionCall: builtinFunction | standardFunction | rankingWindowedFunction | aggregateFunction
    ;

builtinFunction: EXTRACT L_PAREN part = (STRING | ID) FROM expr R_PAREN # builtinExtract
    ;

standardFunction: functionName L_PAREN (exprList | paramAssocList)? R_PAREN
    ;

functionName: id | nonReservedFunctionName
    ;

nonReservedFunctionName
    : LEFT
    | RIGHT // keywords that cannot be used as id, but can be used as function names
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
    : op = (LISTAGG | ARRAY_AGG) L_PAREN DISTINCT? expr (COMMA string)? R_PAREN (
        WITHIN GROUP L_PAREN orderByClause R_PAREN
    )?                                      # aggFuncList
    | id L_PAREN DISTINCT? exprList R_PAREN # aggFuncExprList
    | id L_PAREN STAR R_PAREN               # aggFuncStar
    ;

literal
    : DATE_LIT
    | TIMESTAMP_LIT
    | STRING
    | sign? DECIMAL
    | sign? (REAL | FLOAT)
    | trueFalse
    | jsonLiteral
    | arrayLiteral
    | NULL_
    | AT_Q
    ;

sign: PLUS | MINUS
    ;

bracketExpression: L_PAREN exprList R_PAREN | L_PAREN subquery R_PAREN
    ;

caseExpression
    : CASE expr switchSection+ (ELSE expr)? END
    | CASE switchSearchConditionSection+ (ELSE expr)? END
    ;

switchSearchConditionSection: WHEN predicate THEN expr
    ;

switchSection: WHEN expr THEN expr
    ;

// select
queryStatement: withExpression? selectStatement setOperators*
    ;

withExpression: WITH commonTableExpression (COMMA commonTableExpression)*
    ;

commonTableExpression
    : id (L_PAREN columnList R_PAREN)? AS L_PAREN selectStatement setOperators* R_PAREN
    ;

selectStatement
    : selectClause selectOptionalClauses limitClause?
    | selectTopClause selectOptionalClauses //TOP and LIMIT are not allowed together
    ;

setOperators
    : (UNION ALL? | EXCEPT | MINUS_ | INTERSECT) selectStatement //EXCEPT and MINUS have same SQL meaning
    | L_PAREN selectStatement R_PAREN
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
    : columnElem asAlias?
    | columnElemStar
    //    | udtElem
    | expressionElem asAlias?
    ;

columnElemStar: (objectName DOT)? STAR
    ;

columnElem: (objectName DOT)? columnName | (objectName DOT)? DOLLAR columnPosition
    ;

asAlias: AS? alias
    ;

expressionElem: expr | predicate
    ;

columnPosition: num
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

tableSource
    : tableSourceItemJoined sample?
    //| L_PAREN tableSource R_PAREN
    ;

tableSourceItemJoined: objectRef joinClause* | L_PAREN tableSourceItemJoined R_PAREN joinClause*
    ;

objectRef
    : objectName atBefore? changes? matchRecognize? pivotUnpivot? tableAlias?        # objRefDefault
    | TABLE L_PAREN functionCall R_PAREN pivotUnpivot? tableAlias?                   # objRefTableFunc
    | LATERAL? (functionCall | (L_PAREN subquery R_PAREN)) pivotUnpivot? tableAlias? # objRefSubquery
    | valuesTable                                                                    # objRefValues
    | objectName START WITH predicate CONNECT BY priorList?                          # objRefStartWith
    ;

tableAlias: AS? alias (L_PAREN id (COMMA id)*)?
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
    : joinType? JOIN objectRef ((ON predicate)? | (USING L_PAREN columnList R_PAREN)?)
    //| joinType? JOIN objectRef (USING L_PAREN columnList R_PAREN)?
    | NATURAL outerJoin? JOIN objectRef
    | CROSS JOIN objectRef
    ;

atBefore
    : AT_KEYWORD L_PAREN (
        TIMESTAMP ASSOC expr
        | OFFSET ASSOC expr
        | STATEMENT ASSOC string
        | STREAM ASSOC string
    ) R_PAREN
    | BEFORE L_PAREN STATEMENT ASSOC string R_PAREN
    ;

end: END L_PAREN (TIMESTAMP ASSOC expr | OFFSET ASSOC expr | STATEMENT ASSOC string) R_PAREN
    ;

changes: CHANGES L_PAREN INFORMATION ASSOC defaultAppendOnly R_PAREN atBefore end?
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

matchOpts: SHOW EMPTY_ MATCHES | OMIT EMPTY_ MATCHES | WITH UNMATCHED ROWS
    ;

rowMatch: (ONE ROW PER MATCH | ALL ROWS PER MATCH) matchOpts?
    ;

firstLast: FIRST | LAST
    ;

// TODO: This syntax is unfinished and needs to be completed - DUMMY is just a placeholder from the original author
symbol: DUMMY
    ;

afterMatch: AFTER MATCH SKIP_ (PAST LAST ROW | TO NEXT ROW | TO firstLast? symbol)
    ;

symbolList: symbol AS expr (COMMA symbol AS expr)*
    ;

define: DEFINE symbolList
    ;

matchRecognize
    : MATCH_RECOGNIZE L_PAREN partitionBy? orderByClause? measures? rowMatch? afterMatch? pattern? define? R_PAREN
    ;

pivotUnpivot
    : PIVOT L_PAREN aggregateFunc = id L_PAREN pivotColumn = id R_PAREN FOR valueColumn = id IN L_PAREN values += literal (
        COMMA values += literal
    )* R_PAREN R_PAREN (asAlias columnAliasListInBrackets?)?
    | UNPIVOT L_PAREN valueColumn = id FOR nameColumn = id IN L_PAREN columnList R_PAREN R_PAREN
    ;

columnAliasListInBrackets: L_PAREN id (COMMA id)* R_PAREN
    ;

exprListInParentheses: L_PAREN exprList R_PAREN
    ;

valuesTable
    : L_PAREN valuesTableBody R_PAREN (asAlias columnAliasListInBrackets?)?
    | valuesTableBody (asAlias columnAliasListInBrackets?)?
    ;

valuesTableBody: VALUES exprListInParentheses (COMMA exprListInParentheses)*
    ;

sampleMethod
    : (SYSTEM | BLOCK) L_PAREN num R_PAREN        # sampleMethodBlock
    | (BERNOULLI | ROW)? L_PAREN num ROWS R_PAREN # sampleMethodRowFixed
    | (BERNOULLI | ROW)? L_PAREN num R_PAREN      # sampleMethodRowProba
    ;

sample: (SAMPLE | TABLESAMPLE) sampleMethod sampleSeed?
    ;

sampleSeed: (REPEATABLE | SEED) L_PAREN num R_PAREN
    ;

comparisonOperator: EQ | GT | LT | LE | GE | LTGT | NE
    ;

nullNotNull: NOT? NULL_
    ;

subquery: queryStatement
    ;

predicate
    : EXISTS L_PAREN subquery R_PAREN
    | expr comparisonOperator (ALL | SOME | ANY) L_PAREN subquery R_PAREN
    | expr predicatePartial
    | expr
    ;

whereClause: WHERE predicate
    ;

groupByElem: columnElem | num | expressionElem
    ;

groupByList: groupByElem (COMMA groupByElem)*
    ;

groupByClause
    : GROUP BY groupByList havingClause?
    | GROUP BY (CUBE | GROUPING SETS | ROLLUP) L_PAREN groupByList R_PAREN
    | GROUP BY ALL
    ;

havingClause: HAVING predicate
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