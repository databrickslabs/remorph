/*
T-SQL (Transact-SQL, MSSQL) grammar.
The MIT License (MIT).
Copyright (c) 2017, Mark Adams (madams51703@gmail.com)
Copyright (c) 2015-2017, Ivan Kochurkin (kvanttt@gmail.com), Positive Technologies.
Copyright (c) 2016, Scott Ure (scott@redstormsoftware.com).
Copyright (c) 2016, Rui Zhang (ruizhang.ccs@gmail.com).
Copyright (c) 2016, Marcus Henriksson (kuseman80@gmail.com).
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

parser grammar TSqlParser;

import procedure, commonparse;

options {
    tokenVocab = TSqlLexer;
}

// ============== Dialect compatibiltiy rules ==============
// The following rules provide substitutes for grammar rules referenced in the procedure.g4 grammar, that
// we do not have real equivalents for in this gramamr.
// Over time, as we homogonize more and more of the dialect grammars, these rules will be removed.
// Note that these rules will not be visited by the TSQL transpiler, as they are not part of
// TSQL and we are expecting syntacticly and semanticly sound input.

// string and stringList will eventually expand to composite token sequences for macro substitution, so they
// are not redundant here.
string: STRING
    ;
stringList: string (COMMA string)*
    ;

// expr is just an alias for expression, for Snowflake compatibility
// TODO: Change Snowflake to use the rule anme expression instead of expr as this is what the Spark parser uses
expr: expression
    ;
// ======================================================

// ================= TSQL Specific Rules ========================================

tSqlFile: SEMI* batch? EOF
    ;

batch: executeBodyBatch? SEMI* (sqlClauses SEMI*)+
    ;

// TODO: Properly sort out SEMI colons, which have been haphazzardly added in some
// places and not others.

sqlClauses
    : dmlClause SEMI*
    | cflStatement SEMI*
    | anotherStatement SEMI*
    | ddlClause SEMI*
    | dbccClause SEMI*
    | backupStatement SEMI*
    | createOrAlterFunction SEMI*
    | createOrAlterProcedure SEMI*
    | createOrAlterTrigger SEMI*
    | createView SEMI*
    | goStatement SEMI*
    ;

dmlClause: withExpression? ( selectStatement | merge | delete | insert | update | bulkStatement)
    ;

ddlClause
    : alterApplicationRole
    | alterAssembly
    | alterAsymmetricKey
    | alterAuthorization
    | alterAvailabilityGroup
    | alterCertificate
    | alterColumnEncryptionKey
    | alterCredential
    | alterCryptographicProvider
    | alterDatabase
    | alterDatabaseAuditSpecification
    | alterDbRole
    | alterEndpoint
    | alterExternalDataSource
    | alterExternalLibrary
    | alterExternalResourcePool
    | alterFulltextCatalog
    | alterFulltextStoplist
    | alterIndex
    | alterLoginAzureSql
    | alterLoginAzureSqlDwAndPdw
    | alterLoginSqlServer
    | alterMasterKeyAzureSql
    | alterMasterKeySqlServer
    | alterMessageType
    | alterPartitionFunction
    | alterPartitionScheme
    | alterRemoteServiceBinding
    | alterResourceGovernor
    | alterSchemaAzureSqlDwAndPdw
    | alterSchemaSql
    | alterSequence
    | alterServerAudit
    | alterServerAuditSpecification
    | alterServerConfiguration
    | alterServerRole
    | alterServerRolePdw
    | alterService
    | alterServiceMasterKey
    | alterSymmetricKey
    | alterTable
    | alterUser
    | alterUserAzureSql
    | alterWorkloadGroup
    | alterXmlSchemaCollection
    | createApplicationRole
    | createAssembly
    | createAsymmetricKey
    | createColumnEncryptionKey
    | createColumnMasterKey
    | createColumnstoreIndex
    | createCredential
    | createCryptographicProvider
    | createDatabaseScopedCredential
    | createDatabase
    | createDatabaseAuditSpecification
    | createDbRole
    | createEndpoint
    | createEventNotification
    | createExternalLibrary
    | createExternalResourcePool
    | createExternalDataSource
    | createFulltextCatalog
    | createFulltextStoplist
    | createIndex
    | createLoginAzureSql
    | createLoginPdw
    | createLoginSqlServer
    | createMasterKeyAzureSql
    | createMasterKeySqlServer
    | createNonclusteredColumnstoreIndex
    | createOrAlterBrokerPriority
    | createOrAlterEventSession
    | createPartitionFunction
    | createPartitionScheme
    | createRemoteServiceBinding
    | createResourcePool
    | createRoute
    | createRule
    | createSchema
    | createSchemaAzureSqlDwAndPdw
    | createSearchPropertyList
    | createSecurityPolicy
    | createSequence
    | createServerAudit
    | createServerAuditSpecification
    | createServerRole
    | createService
    | createStatistics
    | createSynonym
    | createTable
    | createType
    | createUser
    | createUserAzureSqlDw
    | createWorkloadGroup
    | createXmlIndex
    | createXmlSchemaCollection
    | triggerDisEn
    | dropAggregate
    | dropApplicationRole
    | dropAssembly
    | dropAsymmetricKey
    | dropAvailabilityGroup
    | dropBrokerPriority
    | dropCertificate
    | dropColumnEncryptionKey
    | dropColumnMasterKey
    | dropContract
    | dropCredential
    | dropCryptograhicProvider
    | dropDatabase
    | dropDatabaseAuditSpecification
    | dropDatabaseEncryptionKey
    | dropDatabaseScopedCredential
    | dropDbRole
    | dropDefault
    | dropEndpoint
    | dropEventNotifications
    | dropEventSession
    | dropExternalDataSource
    | dropExternalFileFormat
    | dropExternalLibrary
    | dropExternalResourcePool
    | dropExternalTable
    | dropFulltextCatalog
    | dropFulltextIndex
    | dropFulltextStoplist
    | dropFunction
    | dropIndex
    | dropLogin
    | dropMasterKey
    | dropMessageType
    | dropPartitionFunction
    | dropPartitionScheme
    | dropProcedure
    | dropQueue
    | dropRemoteServiceBinding
    | dropResourcePool
    | dropRoute
    | dropRule
    | dropSchema
    | dropSearchPropertyList
    | dropSecurityPolicy
    | dropSequence
    | dropServerAudit
    | dropServerAuditSpecification
    | dropServerRole
    | dropService
    | dropSignature
    | dropStatistics
    | dropStatisticsNameAzureDwAndPdw
    | dropSymmetricKey
    | dropSynonym
    | dropTable
    | dropTrigger
    | dropType
    | dropUser
    | dropView
    | dropWorkloadGroup
    | dropXmlSchemaCollection
    | triggerDisEn
    | lockTable
    | truncateTable
    | updateStatistics
    ;

backupStatement
    : backupDatabase
    | backupLog
    | backupCertificate
    | backupMasterKey
    | backupServiceMasterKey
    ;

cflStatement
    : blockStatement
    | breakStatement
    | continueStatement
    | gotoStatement
    | ifStatement
    | printStatement
    | raiseerrorStatement
    | returnStatement
    | throwStatement
    | tryCatchStatement
    | waitforStatement
    | whileStatement
    | receiveStatement
    ;

blockStatement: BEGIN SEMI? sqlClauses* END SEMI?
    ;

breakStatement: BREAK SEMI?
    ;

continueStatement: CONTINUE SEMI?
    ;

gotoStatement: GOTO id COLON? SEMI?
    ;

ifStatement: IF searchCondition sqlClauses (ELSE sqlClauses)? SEMI?
    ;

throwStatement: THROW ( intLocal COMMA stringLocal COMMA intLocal)? SEMI?
    ;

stringLocal: STRING | LOCAL_ID
    ;

intLocal: INT | LOCAL_ID
    ;

tryCatchStatement
    : BEGIN TRY SEMI? sqlClauses+ END TRY SEMI? BEGIN CATCH SEMI? sqlClauses* END CATCH SEMI?
    ;

waitforStatement
    : WAITFOR (
        DELAY STRING
        | id STRING // TIME
        | receiveStatement? COMMA? (id expression)? expression?
    ) SEMI?
    ;

whileStatement: WHILE searchCondition ( sqlClauses | BREAK SEMI? | CONTINUE SEMI?)
    ;

printStatement: PRINT (expression | DOUBLE_QUOTE_ID) (COMMA LOCAL_ID)* SEMI?
    ;

raiseerrorStatement
    : RAISERROR LPAREN (INT | STRING | LOCAL_ID) COMMA constant_LOCAL_ID COMMA constant_LOCAL_ID (
        COMMA (constant_LOCAL_ID | NULL)
    )* RPAREN (WITH genericOption)? SEMI?
    | RAISERROR INT formatstring = (STRING | LOCAL_ID | DOUBLE_QUOTE_ID) (
        COMMA args += (INT | STRING | LOCAL_ID)
    )* // Discontinued in SQL Server 2014 on
    ;

anotherStatement
    : alterQueue
    | checkpointStatement
    | conversationStatement
    | createContract
    | createQueue
    | cursorStatement
    | declareStatement
    | executeStatement
    | killStatement
    | messageStatement
    | reconfigureStatement
    | securityStatement
    | setStatement
    | setuserStatement
    | shutdownStatement
    | transactionStatement
    | useStatement
    ;

alterApplicationRole
    : ALTER APPLICATION ROLE id WITH (COMMA? NAME EQ id)? (COMMA? PASSWORD EQ STRING)? (
        COMMA? DEFAULT_SCHEMA EQ id
    )?
    ;

alterXmlSchemaCollection: ALTER XML SCHEMA COLLECTION dotIdentifier ADD STRING
    ;

createApplicationRole: CREATE APPLICATION ROLE id WITH optionList
    ;

dropAggregate: DROP AGGREGATE (IF EXISTS)? dotIdentifier?
    ;

dropApplicationRole: DROP APPLICATION ROLE id
    ;

alterAssembly: ALTER ASSEMBLY id alterAssemblyClause
    ;

alterAssemblyClause
    : (FROM (STRING | AS id))? (WITH optionList)? (DROP optionList)? (
        ADD FILE FROM STRING (AS id)?
    )?
    ;

createAssembly
    : CREATE ASSEMBLY id genericOption? FROM (COMMA? (STRING | HEX))+ (WITH genericOption)?
    ;

dropAssembly: DROP ASSEMBLY (IF EXISTS)? (COMMA? id)+ ( WITH genericOption)?
    ;

alterAsymmetricKey: ALTER ASYMMETRIC KEY id ( asymmetricKeyOption | REMOVE PRIVATE KEY)
    ;

asymmetricKeyOption
    : WITH PRIVATE KEY LPAREN asymmetricKeyPasswordChangeOption (
        COMMA asymmetricKeyPasswordChangeOption
    )? RPAREN
    ;

asymmetricKeyPasswordChangeOption: DECRYPTION BY genericOption | ENCRYPTION BY genericOption
    ;

createAsymmetricKey
    : CREATE ASYMMETRIC KEY id genericOption? (FROM genericOption)? (WITH genericOption)? (
        ENCRYPTION BY genericOption
    )?
    ;

dropAsymmetricKey: DROP ASYMMETRIC KEY id (REMOVE PROVIDER KEY)?
    ;

alterAuthorization
    : ALTER AUTHORIZATION ON (id id? id? DOUBLE_COLON)? dotIdentifier TO genericOption
    ;

classTypeForGrant
    : APPLICATION ROLE
    | ASSEMBLY
    | ASYMMETRIC KEY
    | AUDIT
    | AVAILABILITY GROUP
    | BROKER PRIORITY
    | CERTIFICATE
    | COLUMN ( ENCRYPTION | MASTER) KEY
    | CONTRACT
    | CREDENTIAL
    | CRYPTOGRAPHIC PROVIDER
    | DATABASE (
        AUDIT SPECIFICATION
        | ENCRYPTION KEY
        | EVENT SESSION
        | SCOPED (CONFIGURATION | CREDENTIAL | RESOURCE GOVERNOR)
    )?
    | ENDPOINT
    | EVENT SESSION
    | NOTIFICATION (DATABASE | OBJECT | SERVER)
    | EXTERNAL (DATA SOURCE | FILE FORMAT | LIBRARY | RESOURCE POOL | TABLE | CATALOG | STOPLIST)
    | LOGIN
    | MASTER KEY
    | MESSAGE TYPE
    | OBJECT
    | PARTITION ( FUNCTION | SCHEME)
    | REMOTE SERVICE BINDING
    | RESOURCE GOVERNOR
    | ROLE
    | ROUTE
    | SCHEMA
    | SEARCH PROPERTY LIST
    | SERVER ( ( AUDIT SPECIFICATION?) | ROLE)?
    | SERVICE
    | id LOGIN
    | SYMMETRIC KEY
    | TRIGGER ( DATABASE | SERVER)
    | TYPE
    | USER
    | XML SCHEMA COLLECTION
    ;

dropAvailabilityGroup: DROP AVAILABILITY GROUP id
    ;

alterAvailabilityGroup: alterAvailabilityGroupStart alterAvailabilityGroupOptions
    ;

alterAvailabilityGroupStart: ALTER AVAILABILITY GROUP id
    ;

// TODO: Consolodate all this junk and remove many lexer tokens!
alterAvailabilityGroupOptions
    : SET LPAREN (
        (
            AUTOMATED_BACKUP_PREFERENCE EQ (PRIMARY | SECONDARY_ONLY | SECONDARY | NONE)
            | FAILURE_CONDITION_LEVEL EQ INT
            | HEALTH_CHECK_TIMEOUT EQ INT
            | DB_FAILOVER EQ ( ON | OFF)
            | REQUIRED_SYNCHRONIZED_SECONDARIES_TO_COMMIT EQ INT
        ) RPAREN
    )
    | ADD DATABASE id
    | REMOVE DATABASE id
    | ADD REPLICA ON STRING (
        WITH LPAREN (
            (ENDPOINT_URL EQ STRING)? (
                COMMA? AVAILABILITY_MODE EQ (SYNCHRONOUS_COMMIT | ASYNCHRONOUS_COMMIT)
            )? (COMMA? FAILOVER_MODE EQ (AUTOMATIC | MANUAL))? (
                COMMA? SEEDING_MODE EQ (AUTOMATIC | MANUAL)
            )? (COMMA? BACKUP_PRIORITY EQ INT)? (
                COMMA? PRIMARY_ROLE LPAREN ALLOW_CONNECTIONS EQ (READ_WRITE | ALL) RPAREN
            )? (COMMA? SECONDARY_ROLE LPAREN ALLOW_CONNECTIONS EQ ( READ_ONLY) RPAREN)?
        )
    ) RPAREN
    | SECONDARY_ROLE LPAREN (
        ALLOW_CONNECTIONS EQ (NO | READ_ONLY | ALL)
        | READ_ONLY_ROUTING_LIST EQ (LPAREN ( ( STRING)) RPAREN)
    )
    | PRIMARY_ROLE LPAREN (
        ALLOW_CONNECTIONS EQ (NO | READ_ONLY | ALL)
        | READ_ONLY_ROUTING_LIST EQ ( LPAREN ((COMMA? STRING)* | NONE) RPAREN)
        | SESSION_TIMEOUT EQ INT
    )
    | MODIFY REPLICA ON STRING (
        WITH LPAREN (
            ENDPOINT_URL EQ STRING
            | AVAILABILITY_MODE EQ ( SYNCHRONOUS_COMMIT | ASYNCHRONOUS_COMMIT)
            | FAILOVER_MODE EQ (AUTOMATIC | MANUAL)
            | SEEDING_MODE EQ (AUTOMATIC | MANUAL)
            | BACKUP_PRIORITY EQ INT
        )
        | SECONDARY_ROLE LPAREN (
            ALLOW_CONNECTIONS EQ (NO | READ_ONLY | ALL)
            | READ_ONLY_ROUTING_LIST EQ ( LPAREN ( ( STRING)) RPAREN)
        )
        | PRIMARY_ROLE LPAREN (
            ALLOW_CONNECTIONS EQ (NO | READ_ONLY | ALL)
            | READ_ONLY_ROUTING_LIST EQ ( LPAREN ((COMMA? STRING)* | NONE) RPAREN)
            | SESSION_TIMEOUT EQ INT
        )
    ) RPAREN
    | REMOVE REPLICA ON STRING
    | JOIN
    | JOIN AVAILABILITY GROUP ON (
        COMMA? STRING WITH LPAREN (
            LISTENER_URL EQ STRING COMMA AVAILABILITY_MODE EQ (
                SYNCHRONOUS_COMMIT
                | ASYNCHRONOUS_COMMIT
            ) COMMA FAILOVER_MODE EQ MANUAL COMMA SEEDING_MODE EQ (AUTOMATIC | MANUAL) RPAREN
        )
    )+
    | MODIFY AVAILABILITY GROUP ON (
        COMMA? STRING WITH LPAREN (
            LISTENER_URL EQ STRING (
                COMMA? AVAILABILITY_MODE EQ (SYNCHRONOUS_COMMIT | ASYNCHRONOUS_COMMIT)
            )? (COMMA? FAILOVER_MODE EQ MANUAL)? (COMMA? SEEDING_MODE EQ (AUTOMATIC | MANUAL))? RPAREN
        )
    )+
    | GRANT CREATE ANY DATABASE
    | DENY CREATE ANY DATABASE
    | FAILOVER
    | FORCE_FAILOVER_ALLOW_DATA_LOSS
    | ADD LISTENER STRING LPAREN (
        WITH DHCP (ON LPAREN STRING STRING RPAREN)
        | WITH IP LPAREN (
            (COMMA? LPAREN ( STRING (COMMA STRING)?) RPAREN)+ RPAREN (COMMA PORT EQ INT)?
        )
    ) RPAREN
    | MODIFY LISTENER (ADD IP LPAREN ( STRING (COMMA STRING)?) RPAREN | PORT EQ INT)
    | RESTART LISTENER STRING
    | REMOVE LISTENER STRING
    | OFFLINE
    | WITH LPAREN DTC_SUPPORT EQ PER_DB RPAREN
    ;

createOrAlterBrokerPriority
    : (CREATE | ALTER) BROKER PRIORITY id FOR CONVERSATION SET LPAREN (
        CONTRACT_NAME EQ ( id | ANY) COMMA?
    )? (LOCAL_SERVICE_NAME EQ (DOUBLE_FORWARD_SLASH? id | ANY) COMMA?)? (
        REMOTE_SERVICE_NAME EQ (STRING | ANY) COMMA?
    )? (PRIORITY_LEVEL EQ ( INT | DEFAULT))? RPAREN
    ;

dropBrokerPriority: DROP BROKER PRIORITY id
    ;

alterCertificate
    : ALTER CERTIFICATE id (
        REMOVE PRIVATE_KEY
        | WITH PRIVATE KEY LPAREN (
            FILE EQ STRING COMMA?
            | DECRYPTION BY PASSWORD EQ STRING COMMA?
            | ENCRYPTION BY PASSWORD EQ STRING COMMA?
        )+ RPAREN
        | WITH ACTIVE FOR BEGIN_DIALOG EQ ( ON | OFF)
    )
    ;

alterColumnEncryptionKey
    : ALTER COLUMN ENCRYPTION KEY id (ADD | DROP) VALUE LPAREN COLUMN_MASTER_KEY EQ id (
        COMMA ALGORITHM EQ STRING COMMA ENCRYPTED_VALUE EQ HEX
    )? RPAREN
    ;

createColumnEncryptionKey
    : CREATE COLUMN ENCRYPTION KEY id WITH VALUES (
        LPAREN COMMA? COLUMN_MASTER_KEY EQ id COMMA ALGORITHM EQ STRING COMMA ENCRYPTED_VALUE EQ HEX RPAREN COMMA?
    )+
    ;

dropCertificate: DROP CERTIFICATE id
    ;

dropColumnEncryptionKey: DROP COLUMN ENCRYPTION KEY id
    ;

dropColumnMasterKey: DROP COLUMN MASTER KEY id
    ;

dropContract: DROP CONTRACT id
    ;

dropCredential: DROP CREDENTIAL id
    ;

dropCryptograhicProvider: DROP CRYPTOGRAPHIC PROVIDER id
    ;

dropDatabase: DROP DATABASE (IF EXISTS)? ( COMMA? id)+
    ;

dropDatabaseAuditSpecification: DROP DATABASE AUDIT SPECIFICATION id
    ;

dropDatabaseEncryptionKey: DROP DATABASE ENCRYPTION KEY
    ;

dropDatabaseScopedCredential: DROP DATABASE SCOPED CREDENTIAL id
    ;

dropDefault: DROP DEFAULT (IF EXISTS)? dotIdentifier (COMMA dotIdentifier)*
    ;

dropEndpoint: DROP ENDPOINT id
    ;

dropExternalDataSource: DROP EXTERNAL DATA SOURCE id
    ;

dropExternalFileFormat: DROP EXTERNAL FILE FORMAT id
    ;

dropExternalLibrary: DROP EXTERNAL LIBRARY id ( AUTHORIZATION id)?
    ;

dropExternalResourcePool: DROP EXTERNAL RESOURCE POOL id
    ;

dropExternalTable: DROP EXTERNAL TABLE dotIdentifier
    ;

dropEventNotifications: DROP EVENT NOTIFICATION id (COMMA id)* ON ( SERVER | DATABASE | QUEUE id)
    ;

dropEventSession: DROP EVENT SESSION id ON SERVER
    ;

dropFulltextCatalog: DROP FULLTEXT CATALOG id
    ;

dropFulltextIndex: DROP FULLTEXT INDEX ON dotIdentifier
    ;

dropFulltextStoplist: DROP FULLTEXT STOPLIST id
    ;

dropLogin: DROP LOGIN id
    ;

dropMasterKey: DROP MASTER KEY
    ;

dropMessageType: DROP MESSAGE TYPE id
    ;

dropPartitionFunction: DROP PARTITION FUNCTION id
    ;

dropPartitionScheme: DROP PARTITION SCHEME id
    ;

dropQueue: DROP QUEUE dotIdentifier
    ;

dropRemoteServiceBinding: DROP REMOTE SERVICE BINDING id
    ;

dropResourcePool: DROP RESOURCE POOL id
    ;

dropDbRole: DROP ROLE (IF EXISTS)? id
    ;

dropRoute: DROP ROUTE id
    ;

dropRule: DROP RULE (IF EXISTS)? dotIdentifier (COMMA dotIdentifier)*
    ;

dropSchema: DROP SCHEMA (IF EXISTS)? id
    ;

dropSearchPropertyList: DROP SEARCH PROPERTY LIST id
    ;

dropSecurityPolicy: DROP SECURITY POLICY (IF EXISTS)? dotIdentifier
    ;

dropSequence: DROP SEQUENCE (IF EXISTS)? dotIdentifier (COMMA dotIdentifier)*
    ;

dropServerAudit: DROP SERVER AUDIT id
    ;

dropServerAuditSpecification: DROP SERVER AUDIT SPECIFICATION id
    ;

dropServerRole: DROP SERVER ROLE id
    ;

dropService: DROP SERVICE id
    ;

dropSignature
    : DROP (COUNTER)? SIGNATURE FROM dotIdentifier BY (
        COMMA? CERTIFICATE cert += id
        | COMMA? ASYMMETRIC KEY id
    )+
    ;

dropStatisticsNameAzureDwAndPdw: DROP STATISTICS dotIdentifier
    ;

dropSymmetricKey: DROP SYMMETRIC KEY id ( REMOVE PROVIDER KEY)?
    ;

dropSynonym: DROP SYNONYM (IF EXISTS)? dotIdentifier
    ;

dropUser: DROP USER (IF EXISTS)? id
    ;

dropWorkloadGroup: DROP WORKLOAD GROUP id
    ;

triggerDisEn
    : (DISABLE | ENABLE) TRIGGER (
        triggers += dotIdentifier (COMMA triggers += dotIdentifier)*
        | ALL
    ) ON (dotIdentifier | DATABASE | ALL SERVER)
    ;

lockTable
    : LOCK TABLE tableName IN (SHARE | EXCLUSIVE) MODE (id /* WAIT INT | NOWAIT */ INT)? SEMI?
    ;

truncateTable
    : TRUNCATE TABLE tableName (
        WITH LPAREN PARTITIONS LPAREN (COMMA? (INT | INT TO INT))+ RPAREN RPAREN
    )?
    ;

createColumnMasterKey
    : CREATE COLUMN MASTER KEY id WITH LPAREN KEY_STORE_PROVIDER_NAME EQ STRING COMMA KEY_PATH EQ STRING RPAREN
    ;

alterCredential: ALTER CREDENTIAL id WITH IDENTITY EQ STRING ( COMMA SECRET EQ STRING)?
    ;

createCredential
    : CREATE CREDENTIAL id WITH IDENTITY EQ STRING (COMMA SECRET EQ STRING)? (
        FOR CRYPTOGRAPHIC PROVIDER id
    )?
    ;

alterCryptographicProvider
    : ALTER CRYPTOGRAPHIC PROVIDER id (FROM FILE EQ STRING)? (ENABLE | DISABLE)?
    ;

createCryptographicProvider: CREATE CRYPTOGRAPHIC PROVIDER id FROM FILE EQ STRING
    ;

createEndpoint
    : CREATE ENDPOINT id (AUTHORIZATION id)? (STATE EQ (STARTED | STOPPED | DISABLED))? AS TCP LPAREN endpointListenerClause RPAREN (
        FOR TSQL LPAREN RPAREN
        | FOR SERVICE_BROKER LPAREN endpointAuthenticationClause (
            COMMA? endpointEncryptionAlogorithmClause
        )? (COMMA? MESSAGE_FORWARDING EQ (ENABLED | DISABLED))? (
            COMMA? MESSAGE_FORWARD_SIZE EQ INT
        )? RPAREN
        | FOR DATABASE_MIRRORING LPAREN endpointAuthenticationClause (
            COMMA? endpointEncryptionAlogorithmClause
        )? COMMA? ROLE EQ (WITNESS | PARTNER | ALL) RPAREN
    )
    ;

endpointEncryptionAlogorithmClause
    : ENCRYPTION EQ (DISABLED | SUPPORTED | REQUIRED) (ALGORITHM (AES RC4? | RC4 AES?))?
    ;

endpointAuthenticationClause
    : AUTHENTICATION EQ (
        WINDOWS (NTLM | KERBEROS | NEGOTIATE)? ( CERTIFICATE id)?
        | CERTIFICATE id WINDOWS? ( NTLM | KERBEROS | NEGOTIATE)?
    )
    ;

endpointListenerClause
    : LISTENER_PORT EQ INT (
        COMMA LISTENER_IP EQ (ALL | LPAREN ( INT DOT INT DOT INT DOT INT | STRING) RPAREN)
    )?
    ;

createEventNotification
    : CREATE EVENT NOTIFICATION id ON (SERVER | DATABASE | QUEUE id) (WITH FAN_IN)? FOR (
        COMMA? etg += id
    )+ TO SERVICE STRING COMMA STRING
    ;

addDropEvent
    : ADD EVENT (
        dotIdentifier (
            LPAREN (SET ( COMMA? id EQ ( INT | STRING))*)? (
                ACTION LPAREN dotIdentifier (COMMA dotIdentifier)* RPAREN
            )+ (WHERE eventSessionPredicateExpression)? RPAREN
        )*
    )
    | DROP EVENT dotIdentifier
    ;

addDropEventTarget
    : ADD TARGET dotIdentifier (LPAREN SET (COMMA? id EQ ( LPAREN? INT RPAREN? | STRING))+ RPAREN)
    | DROP TARGET dotIdentifier
    ;

addDropEventOrTarget: addDropEvent | addDropEventTarget
    ;

createOrAlterEventSession
    : (CREATE | ALTER) EVENT SESSION id ON (SERVER | DATABASE) addDropEventOrTarget (
        COMMA addDropEventOrTarget
    )* (
        WITH LPAREN (COMMA? MAX_MEMORY EQ INT (KB | MB))? (
            COMMA? EVENT_RETENTION_MODE EQ (
                ALLOW_SINGLE_EVENT_LOSS
                | ALLOW_MULTIPLE_EVENT_LOSS
                | NO_EVENT_LOSS
            )
        )? (COMMA? MAX_DISPATCH_LATENCY EQ ( INT SECONDS | INFINITE))? (
            COMMA? MAX_EVENT_SIZE EQ INT (KB | MB)
        )? (COMMA? MEMORY_PARTITION_MODE EQ ( NONE | PER_NODE | PER_CPU))? (
            COMMA? TRACK_CAUSALITY EQ (ON | OFF)
        )? (COMMA? STARTUP_STATE EQ (ON | OFF))? RPAREN
    )? (STATE EQ (START | STOP))?
    ;

eventSessionPredicateExpression
    : (
        COMMA? (AND | OR)? NOT? (
            eventSessionPredicateFactor
            | LPAREN eventSessionPredicateExpression RPAREN
        )
    )+
    ;

eventSessionPredicateFactor
    : eventSessionPredicateLeaf
    | LPAREN eventSessionPredicateExpression RPAREN
    ;

eventSessionPredicateLeaf
    : dotIdentifier ((EQ | (LT GT) | (BANG EQ) | GT | (GT EQ) | LT | LT EQ) (INT | STRING))?
    | dotIdentifier LPAREN ( dotIdentifier COMMA (INT | STRING)) RPAREN
    ;

createExternalDataSource
    : CREATE EXTERNAL DATA SOURCE id WITH LPAREN (COMMA? ( genericOption | connectionOptions))* RPAREN SEMI?
    ;

connectionOptions: id EQ STRING (COMMA STRING)*
    ;

alterExternalDataSource
    : ALTER EXTERNAL DATA SOURCE id (
        SET (
            LOCATION EQ STRING COMMA?
            | RESOURCE_MANAGER_LOCATION EQ STRING COMMA?
            | CREDENTIAL EQ id
        )+
        | WITH LPAREN TYPE EQ BLOB_STORAGE COMMA LOCATION EQ STRING (COMMA CREDENTIAL EQ id)? RPAREN
    )
    ;

alterExternalLibrary
    : ALTER EXTERNAL LIBRARY id (AUTHORIZATION id)? (SET | ADD) (
        LPAREN CONTENT EQ (STRING | HEX | NONE) (COMMA PLATFORM EQ (WINDOWS | LINUX)? RPAREN) WITH (
            COMMA? LANGUAGE EQ id
            | DATA_SOURCE EQ id
        )+ RPAREN
    )
    ;

createExternalLibrary
    : CREATE EXTERNAL LIBRARY id (AUTHORIZATION id)? FROM (
        COMMA? LPAREN? (CONTENT EQ)? (STRING | HEX | NONE) (
            COMMA PLATFORM EQ (WINDOWS | LINUX)? RPAREN
        )?
    ) (WITH ( COMMA? LANGUAGE EQ id | DATA_SOURCE EQ id)+ RPAREN)?
    ;

alterExternalResourcePool
    : ALTER EXTERNAL RESOURCE POOL (id | DEFAULT_DOUBLE_QUOTE) WITH LPAREN MAX_CPU_PERCENT EQ INT (
        COMMA? AFFINITY CPU EQ ( AUTO | (COMMA? INT TO INT | COMMA INT)+)
        | NUMANODE EQ (COMMA? INT TO INT | COMMA? INT)+
    ) (COMMA? MAX_MEMORY_PERCENT EQ INT)? (COMMA? MAX_PROCESSES EQ INT)? RPAREN
    ;

createExternalResourcePool
    : CREATE EXTERNAL RESOURCE POOL id WITH LPAREN MAX_CPU_PERCENT EQ INT (
        COMMA? AFFINITY CPU EQ ( AUTO | (COMMA? INT TO INT | COMMA INT)+)
        | NUMANODE EQ (COMMA? INT TO INT | COMMA? INT)+
    ) (COMMA? MAX_MEMORY_PERCENT EQ INT)? (COMMA? MAX_PROCESSES EQ INT)? RPAREN
    ;

alterFulltextCatalog
    : ALTER FULLTEXT CATALOG id (
        REBUILD (WITH ACCENT_SENSITIVITY EQ (ON | OFF))?
        | REORGANIZE
        | AS DEFAULT
    )
    ;

createFulltextCatalog
    : CREATE FULLTEXT CATALOG id (ON FILEGROUP id)? (IN PATH STRING)? (
        WITH ACCENT_SENSITIVITY EQ (ON | OFF)
    )? (AS DEFAULT)? (AUTHORIZATION id)?
    ;

alterFulltextStoplist
    : ALTER FULLTEXT STOPLIST id (
        ADD STRING LANGUAGE (STRING | INT | HEX)
        | DROP (STRING LANGUAGE (STRING | INT | HEX) | ALL (STRING | INT | HEX) | ALL)
    )
    ;

createFulltextStoplist
    : CREATE FULLTEXT STOPLIST id (FROM (dotIdentifier | SYSTEM STOPLIST))? (AUTHORIZATION id)?
    ;

alterLoginSqlServer
    : ALTER LOGIN id (
        (ENABLE | DISABLE)?
        | WITH ((PASSWORD EQ ( STRING | HEX HASHED)) (MUST_CHANGE | UNLOCK)*)? (
            OLD_PASSWORD EQ STRING ( MUST_CHANGE | UNLOCK)*
        )? (DEFAULT_DATABASE EQ id)? (DEFAULT_LANGUAGE EQ id)? (NAME EQ id)? (
            CHECK_POLICY EQ (ON | OFF)
        )? (CHECK_EXPIRATION EQ (ON | OFF))? (CREDENTIAL EQ id)? (NO CREDENTIAL)?
        | (ADD | DROP) CREDENTIAL id
    )
    ;

createLoginSqlServer
    : CREATE LOGIN id (
        WITH ((PASSWORD EQ ( STRING | HEX HASHED)) (MUST_CHANGE | UNLOCK)*)? (COMMA? SID EQ HEX)? (
            COMMA? DEFAULT_DATABASE EQ id
        )? (COMMA? DEFAULT_LANGUAGE EQ id)? (COMMA? CHECK_EXPIRATION EQ (ON | OFF))? (
            COMMA? CHECK_POLICY EQ (ON | OFF)
        )? (COMMA? CREDENTIAL EQ id)?
        | (
            FROM (
                WINDOWS (
                    WITH (COMMA? DEFAULT_DATABASE EQ id)? (COMMA? DEFAULT_LANGUAGE EQ STRING)?
                )
                | CERTIFICATE id
                | ASYMMETRIC KEY id
            )
        )
    )
    ;

alterLoginAzureSql
    : ALTER LOGIN id (
        (ENABLE | DISABLE)?
        | WITH ( PASSWORD EQ STRING (OLD_PASSWORD EQ STRING)? | NAME EQ id)
    )
    ;

createLoginAzureSql: CREATE LOGIN id WITH PASSWORD EQ STRING ( SID EQ HEX)?
    ;

alterLoginAzureSqlDwAndPdw
    : ALTER LOGIN id (
        (ENABLE | DISABLE)?
        | WITH (PASSWORD EQ STRING ( OLD_PASSWORD EQ STRING (MUST_CHANGE | UNLOCK)*)? | NAME EQ id)
    )
    ;

createLoginPdw
    : CREATE LOGIN id (
        WITH (PASSWORD EQ STRING (MUST_CHANGE)? ( CHECK_POLICY EQ (ON | OFF)?)?)
        | FROM WINDOWS
    )
    ;

alterMasterKeySqlServer
    : ALTER MASTER KEY (
        (FORCE)? REGENERATE WITH ENCRYPTION BY PASSWORD EQ STRING
        | (ADD | DROP) ENCRYPTION BY (SERVICE MASTER KEY | PASSWORD EQ STRING)
    )
    ;

createMasterKeySqlServer: CREATE MASTER KEY ENCRYPTION BY PASSWORD EQ STRING
    ;

alterMasterKeyAzureSql
    : ALTER MASTER KEY (
        (FORCE)? REGENERATE WITH ENCRYPTION BY PASSWORD EQ STRING
        | ADD ENCRYPTION BY (SERVICE MASTER KEY | PASSWORD EQ STRING)
        | DROP ENCRYPTION BY PASSWORD EQ STRING
    )
    ;

createMasterKeyAzureSql: CREATE MASTER KEY ( ENCRYPTION BY PASSWORD EQ STRING)?
    ;

alterMessageType
    : ALTER MESSAGE TYPE id VALIDATION EQ (
        NONE
        | EMPTY
        | WELL_FORMED_XML
        | VALID_XML WITH SCHEMA COLLECTION id
    )
    ;

alterPartitionFunction
    : ALTER PARTITION FUNCTION id LPAREN RPAREN (SPLIT | MERGE) RANGE LPAREN INT RPAREN
    ;

alterPartitionScheme: ALTER PARTITION SCHEME id NEXT USED (id)?
    ;

alterRemoteServiceBinding
    : ALTER REMOTE SERVICE BINDING id WITH (USER EQ id)? (COMMA ANONYMOUS EQ (ON | OFF))?
    ;

createRemoteServiceBinding
    : CREATE REMOTE SERVICE BINDING id (AUTHORIZATION id)? TO SERVICE STRING WITH (USER EQ id)? (
        COMMA ANONYMOUS EQ (ON | OFF)
    )?
    ;

createResourcePool
    : CREATE RESOURCE POOL id (
        WITH LPAREN (COMMA? MIN_CPU_PERCENT EQ INT)? (COMMA? MAX_CPU_PERCENT EQ INT)? (
            COMMA? CAP_CPU_PERCENT EQ INT
        )? (
            COMMA? AFFINITY SCHEDULER EQ (
                AUTO
                | LPAREN (COMMA? (INT | INT TO INT))+ RPAREN
                | NUMANODE EQ LPAREN (COMMA? (INT | INT TO INT))+ RPAREN
            )
        )? (COMMA? MIN_MEMORY_PERCENT EQ INT)? (COMMA? MAX_MEMORY_PERCENT EQ INT)? (
            COMMA? MIN_IOPS_PER_VOLUME EQ INT
        )? (COMMA? MAX_IOPS_PER_VOLUME EQ INT)? RPAREN
    )?
    ;

alterResourceGovernor
    : ALTER RESOURCE GOVERNOR (
        (DISABLE | RECONFIGURE)
        | WITH LPAREN CLASSIFIER_FUNCTION EQ (dotIdentifier | NULL) RPAREN
        | RESET STATISTICS
        | WITH LPAREN MAX_OUTSTANDING_IO_PER_VOLUME EQ INT RPAREN
    )
    ;

alterDatabaseAuditSpecification
    : ALTER DATABASE AUDIT SPECIFICATION id (FOR SERVER AUDIT id)? (
        auditActionSpecGroup (COMMA auditActionSpecGroup)*
    )? (WITH LPAREN STATE EQ (ON | OFF) RPAREN)?
    ;

auditActionSpecGroup: (ADD | DROP) LPAREN (auditActionSpecification | id) RPAREN
    ;

auditActionSpecification
    : actionSpecification (COMMA actionSpecification)* ON (auditClassName COLON COLON)? dotIdentifier BY principalId (
        COMMA principalId
    )*
    ;

actionSpecification: SELECT | INSERT | UPDATE | DELETE | EXECUTE | RECEIVE | REFERENCES
    ;

auditClassName: OBJECT | SCHEMA | TABLE
    ;

alterDbRole: ALTER ROLE id ( (ADD | DROP) MEMBER id | WITH NAME EQ id)
    ;

createDatabaseAuditSpecification
    : CREATE DATABASE AUDIT SPECIFICATION id (FOR SERVER AUDIT id)? (
        auditActionSpecGroup (COMMA auditActionSpecGroup)*
    )? (WITH LPAREN STATE EQ (ON | OFF) RPAREN)?
    ;

createDbRole: CREATE ROLE id (AUTHORIZATION id)?
    ;

createRoute
    : CREATE ROUTE id (AUTHORIZATION id)? WITH (COMMA? SERVICE_NAME EQ STRING)? (
        COMMA? BROKER_INSTANCE EQ STRING
    )? (COMMA? LIFETIME EQ INT)? COMMA? ADDRESS EQ STRING (COMMA MIRROR_ADDRESS EQ STRING)?
    ;

createRule: CREATE RULE (id DOT)? id AS searchCondition
    ;

alterSchemaSql
    : ALTER SCHEMA id TRANSFER ((OBJECT | TYPE | XML SCHEMA COLLECTION) DOUBLE_COLON)? id (DOT id)?
    ;

createSchema
    : CREATE SCHEMA (id | AUTHORIZATION id | id AUTHORIZATION id) (
        createTable
        | createView
        | (GRANT | DENY) (SELECT | INSERT | DELETE | UPDATE) ON (SCHEMA DOUBLE_COLON)? id TO id
        | REVOKE (SELECT | INSERT | DELETE | UPDATE) ON (SCHEMA DOUBLE_COLON)? id FROM id
    )*
    ;

createSchemaAzureSqlDwAndPdw: CREATE SCHEMA id ( AUTHORIZATION id)?
    ;

alterSchemaAzureSqlDwAndPdw: ALTER SCHEMA id TRANSFER (OBJECT DOUBLE_COLON)? dotIdentifier?
    ;

createSearchPropertyList
    : CREATE SEARCH PROPERTY LIST id (FROM dotIdentifier)? (AUTHORIZATION id)?
    ;

createSecurityPolicy
    : CREATE SECURITY POLICY dotIdentifier (
        COMMA? ADD (FILTER | BLOCK)? PREDICATE dotIdentifier LPAREN (COMMA? id)+ RPAREN ON dotIdentifier (
            COMMA? AFTER (INSERT | UPDATE)
            | COMMA? BEFORE (UPDATE | DELETE)
        )*
    )+ (WITH LPAREN STATE EQ (ON | OFF) ( SCHEMABINDING (ON | OFF))? RPAREN)? (NOT FOR REPLICATION)?
    ;

alterSequence
    : ALTER SEQUENCE dotIdentifier (RESTART (WITH INT)?)? (INCREMENT BY INT)? (
        MINVALUE INT
        | NO MINVALUE
    )? (MAXVALUE INT | NO MAXVALUE)? (CYCLE | NO CYCLE)? (CACHE INT | NO CACHE)?
    ;

createSequence
    : CREATE SEQUENCE dotIdentifier (AS dataType)? (START WITH INT)? (INCREMENT BY MINUS? INT)? (
        MINVALUE (MINUS? INT)?
        | NO MINVALUE
    )? (MAXVALUE (MINUS? INT)? | NO MAXVALUE)? (CYCLE | NO CYCLE)? (CACHE INT? | NO CACHE)?
    ;

alterServerAudit
    : ALTER SERVER AUDIT id (
        (
            TO (
                FILE (
                    LPAREN (
                        COMMA? FILEPATH EQ STRING
                        | COMMA? MAXSIZE EQ ( INT (MB | GB | TB) | UNLIMITED)
                        | COMMA? MAX_ROLLOVER_FILES EQ ( INT | UNLIMITED)
                        | COMMA? MAX_FILES EQ INT
                        | COMMA? RESERVE_DISK_SPACE EQ (ON | OFF)
                    )* RPAREN
                )
                | APPLICATION_LOG
                | SECURITY_LOG
            )
        )? (
            WITH LPAREN (
                COMMA? QUEUE_DELAY EQ INT
                | COMMA? ON_FAILURE EQ ( CONTINUE | SHUTDOWN | FAIL_OPERATION)
                | COMMA? STATE EQ (ON | OFF)
            )* RPAREN
        )? (
            WHERE (
                COMMA? (NOT?) id (EQ | (LT GT) | (BANG EQ) | GT | (GT EQ) | LT | LT EQ) (
                    INT
                    | STRING
                )
                | COMMA? (AND | OR) NOT? (EQ | (LT GT) | (BANG EQ) | GT | (GT EQ) | LT | LT EQ) (
                    INT
                    | STRING
                )
            )
        )?
        | REMOVE WHERE
        | MODIFY NAME EQ id
    )
    ;

createServerAudit
    : CREATE SERVER AUDIT id (
        (
            TO (
                FILE (
                    LPAREN (
                        COMMA? FILEPATH EQ STRING
                        | COMMA? MAXSIZE EQ ( INT (MB | GB | TB) | UNLIMITED)
                        | COMMA? MAX_ROLLOVER_FILES EQ ( INT | UNLIMITED)
                        | COMMA? MAX_FILES EQ INT
                        | COMMA? RESERVE_DISK_SPACE EQ (ON | OFF)
                    )* RPAREN
                )
                | APPLICATION_LOG
                | SECURITY_LOG
            )
        )? (
            WITH LPAREN (
                COMMA? QUEUE_DELAY EQ INT
                | COMMA? ON_FAILURE EQ ( CONTINUE | SHUTDOWN | FAIL_OPERATION)
                | COMMA? STATE EQ (ON | OFF)
                | COMMA? AUDIT_GUID EQ id
            )* RPAREN
        )? (
            WHERE (
                COMMA? (NOT?) id (EQ | (LT GT) | (BANG EQ) | GT | (GT EQ) | LT | LT EQ) (
                    INT
                    | STRING
                )
                | COMMA? (AND | OR) NOT? (EQ | (LT GT) | (BANG EQ) | GT | (GT EQ) | LT | LT EQ) (
                    INT
                    | STRING
                )
            )
        )?
        | REMOVE WHERE
        | MODIFY NAME EQ id
    )
    ;

alterServerAuditSpecification
    : ALTER SERVER AUDIT SPECIFICATION id (FOR SERVER AUDIT id)? ((ADD | DROP) LPAREN id RPAREN)* (
        WITH LPAREN STATE EQ (ON | OFF) RPAREN
    )?
    ;

createServerAuditSpecification
    : CREATE SERVER AUDIT SPECIFICATION id (FOR SERVER AUDIT id)? (ADD LPAREN id RPAREN)* (
        WITH LPAREN STATE EQ (ON | OFF) RPAREN
    )?
    ;

alterServerConfiguration
    : ALTER SERVER CONFIGURATION SET (
        (
            PROCESS AFFINITY (
                CPU EQ (AUTO | (COMMA? INT | COMMA? INT TO INT)+)
                | NUMANODE EQ ( COMMA? INT | COMMA? INT TO INT)+
            )
            | DIAGNOSTICS id /* LOG */ (
                onOff
                | PATH EQ (STRING | DEFAULT)
                | MAX_SIZE EQ (INT MB | DEFAULT)
                | MAX_FILES EQ (INT | DEFAULT)
            )
            | FAILOVER CLUSTER PROPERTY (
                VERBOSELOGGING EQ (STRING | DEFAULT)
                | SQLDUMPERFLAGS EQ (STRING | DEFAULT)
                | SQLDUMPERPATH EQ (STRING | DEFAULT)
                | SQLDUMPERTIMEOUT (STRING | DEFAULT)
                | FAILURECONDITIONLEVEL EQ (STRING | DEFAULT)
                | HEALTHCHECKTIMEOUT EQ (INT | DEFAULT)
            )
            | HADR CLUSTER CONTEXT EQ (STRING | LOCAL)
            | BUFFER POOL EXTENSION (
                ON LPAREN FILENAME EQ STRING COMMA SIZE EQ INT (KB | MB | GB) RPAREN
                | OFF
            )
            | SET SOFTNUMA (ON | OFF)
        )
    )
    ;

alterServerRole: ALTER SERVER ROLE id ( (ADD | DROP) MEMBER id | WITH NAME EQ id)
    ;

createServerRole: CREATE SERVER ROLE id ( AUTHORIZATION id)?
    ;

alterServerRolePdw: ALTER SERVER ROLE id (ADD | DROP) MEMBER id
    ;

alterService
    : ALTER SERVICE id (ON QUEUE dotIdentifier)? (LPAREN optArgClause (COMMA optArgClause)* RPAREN)?
    ;

optArgClause: (ADD | DROP) CONTRACT id
    ;

createService
    : CREATE SERVICE id (AUTHORIZATION id)? ON QUEUE dotIdentifier (
        LPAREN (COMMA? (id | DEFAULT))+ RPAREN
    )?
    ;

alterServiceMasterKey
    : ALTER SERVICE MASTER KEY (
        FORCE? REGENERATE
        | (
            WITH (
                OLD_ACCOUNT EQ STRING COMMA OLD_PASSWORD EQ STRING
                | NEW_ACCOUNT EQ STRING COMMA NEW_PASSWORD EQ STRING
            )?
        )
    )
    ;

alterSymmetricKey
    : ALTER SYMMETRIC KEY id (
        (ADD | DROP) ENCRYPTION BY (
            CERTIFICATE id
            | PASSWORD EQ STRING
            | SYMMETRIC KEY id
            | ASYMMETRIC KEY id
        )
    )
    ;

createSynonym: CREATE SYNONYM dotIdentifier FOR dotIdentifier
    ;

alterUser
    : ALTER USER id WITH (
        COMMA? NAME EQ id
        | COMMA? DEFAULT_SCHEMA EQ ( id | NULL)
        | COMMA? LOGIN EQ id
        | COMMA? PASSWORD EQ STRING (OLD_PASSWORD EQ STRING)+
        | COMMA? DEFAULT_LANGUAGE EQ ( NONE | INT | id)
        | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ ( ON | OFF)
    )+
    ;

createUser
    : CREATE USER id ((FOR | FROM) LOGIN id)? (
        WITH (
            COMMA? DEFAULT_SCHEMA EQ id
            | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ ( ON | OFF)
        )*
    )?
    | CREATE USER (
        id (
            WITH (
                COMMA? DEFAULT_SCHEMA EQ id
                | COMMA? DEFAULT_LANGUAGE EQ ( NONE | INT | id)
                | COMMA? SID EQ HEX
                | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ ( ON | OFF)
            )*
        )?
        | id WITH PASSWORD EQ STRING (
            COMMA? DEFAULT_SCHEMA EQ id
            | COMMA? DEFAULT_LANGUAGE EQ ( NONE | INT | id)
            | COMMA? SID EQ HEX
            | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ ( ON | OFF)
        )*
        | id FROM EXTERNAL PROVIDER
    )
    | CREATE USER id (
        WITHOUT LOGIN (
            COMMA? DEFAULT_SCHEMA EQ id
            | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ ( ON | OFF)
        )*
        | (FOR | FROM) CERTIFICATE id
        | (FOR | FROM) ASYMMETRIC KEY id
    )
    | CREATE USER id
    ;

createUserAzureSqlDw
    : CREATE USER id ((FOR | FROM) LOGIN id | WITHOUT LOGIN)? (WITH DEFAULT_SCHEMA EQ id)?
    | CREATE USER id FROM EXTERNAL PROVIDER ( WITH DEFAULT_SCHEMA EQ id)?
    ;

alterUserAzureSql
    : ALTER USER id WITH (
        COMMA? NAME EQ id
        | COMMA? DEFAULT_SCHEMA EQ id
        | COMMA? LOGIN EQ id
        | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ ( ON | OFF)
    )+
    ;

alterWorkloadGroup
    : ALTER WORKLOAD GROUP (id | DEFAULT_DOUBLE_QUOTE) (
        WITH LPAREN (
            IMPORTANCE EQ (LOW | MEDIUM | HIGH)
            | COMMA? REQUEST_MAX_MEMORY_GRANT_PERCENT EQ INT
            | COMMA? REQUEST_MAX_CPU_TIME_SEC EQ INT
            | REQUEST_MEMORY_GRANT_TIMEOUT_SEC EQ INT
            | MAX_DOP EQ INT
            | GROUP_MAX_REQUESTS EQ INT
        )+ RPAREN
    )? (USING (id | DEFAULT_DOUBLE_QUOTE))?
    ;

createWorkloadGroup
    : CREATE WORKLOAD GROUP id (
        WITH LPAREN (
            IMPORTANCE EQ (LOW | MEDIUM | HIGH)
            | COMMA? REQUEST_MAX_MEMORY_GRANT_PERCENT EQ INT
            | COMMA? REQUEST_MAX_CPU_TIME_SEC EQ INT
            | REQUEST_MEMORY_GRANT_TIMEOUT_SEC EQ INT
            | MAX_DOP EQ INT
            | GROUP_MAX_REQUESTS EQ INT
        )+ RPAREN
    )? (USING (id | DEFAULT_DOUBLE_QUOTE)? ( COMMA? EXTERNAL id | DEFAULT_DOUBLE_QUOTE)?)?
    ;

createPartitionFunction
    : CREATE PARTITION FUNCTION id LPAREN dataType RPAREN AS RANGE (LEFT | RIGHT)? FOR VALUES LPAREN expressionList RPAREN
    ;

createPartitionScheme
    : CREATE PARTITION SCHEME id AS PARTITION id ALL? TO LPAREN fileGroupNames += id (
        COMMA fileGroupNames += id
    )* RPAREN
    ;

createQueue: CREATE QUEUE (tableName | id) queueSettings? (ON id | DEFAULT)?
    ;

queueSettings
    : WITH (STATUS EQ onOff COMMA?)? (RETENTION EQ onOff COMMA?)? (
        ACTIVATION LPAREN (
            (
                (STATUS EQ onOff COMMA?)? (PROCEDURE_NAME EQ dotIdentifier COMMA?)? (
                    MAX_QUEUE_READERS EQ INT COMMA?
                )? (EXECUTE AS (SELF | STRING | OWNER) COMMA?)?
            )
            | DROP
        ) RPAREN COMMA?
    )? (POISON_MESSAGE_HANDLING LPAREN (STATUS EQ onOff) RPAREN)?
    ;

alterQueue: ALTER QUEUE (tableName | id) ( queueSettings | queueAction)
    ;

queueAction
    : REBUILD (WITH LPAREN queueRebuildOptions RPAREN)?
    | REORGANIZE (WITH LOB_COMPACTION EQ onOff)?
    | MOVE TO (id | DEFAULT)
    ;

queueRebuildOptions: genericOption
    ;

createContract
    : CREATE CONTRACT contractName (AUTHORIZATION id)? LPAREN (
        (id | DEFAULT) SENT BY (INITIATOR | TARGET | ANY) COMMA?
    )+ RPAREN
    ;

conversationStatement
    : beginConversationTimer
    | beginConversationDialog
    | endConversation
    | getConversation
    | sendConversation
    | waitforConversation
    ;

messageStatement
    : CREATE MESSAGE TYPE id (AUTHORIZATION id)? (
        VALIDATION EQ (NONE | EMPTY | WELL_FORMED_XML | VALID_XML WITH SCHEMA COLLECTION id)
    )
    ;

merge
    : MERGE topClause? INTO? ddlObject withTableHints? asTableAlias? USING tableSources ON searchCondition whenMatch* outputClause? optionClause? SEMI
        ?
    ;

whenMatch: WHEN NOT? MATCHED (BY (TARGET | SOURCE))? (AND searchCondition)? THEN mergeAction
    ;

mergeAction
    : UPDATE SET updateElem (COMMA updateElem)*
    | DELETE
    | INSERT (LPAREN cols = expressionList RPAREN)? (
        VALUES LPAREN vals = expressionList RPAREN
        | DEFAULT VALUES
    )
    ;

delete
    : DELETE topClause? FROM? ddlObject withTableHints? outputClause? (FROM tableSources)? updateWhereClause? optionClause? SEMI?
    ;

bulkStatement
    : BULK INSERT dotIdentifier FROM STRING (
        WITH LPAREN bulkInsertOption (COMMA? bulkInsertOption)* RPAREN
    )?
    ;

bulkInsertOption: ORDER LPAREN bulkInsertCol (COMMA bulkInsertCol)* RPAREN | genericOption
    ;

bulkInsertCol: id (ASC | DESC)?
    ;

insert
    : INSERT topClause? INTO? ddlObject withTableHints? (LPAREN expressionList RPAREN)? outputClause? insertStatementValue optionClause? SEMI?
    ;

insertStatementValue: derivedTable | executeStatement | DEFAULT VALUES
    ;

receiveStatement
    : LPAREN? RECEIVE (ALL | DISTINCT | topClause | STAR | ((id | LOCAL_ID EQ expression) COMMA?)*) FROM tableName (
        INTO id (WHERE searchCondition)
    )? RPAREN?
    ;

selectStatementStandalone: withExpression? selectStatement
    ;

selectStatement: queryExpression forClause? optionClause? SEMI?
    ;

update
    : UPDATE topClause? ddlObject withTableHints? SET updateElem (COMMA updateElem)* outputClause? (
        FROM tableSources
    )? updateWhereClause? optionClause? SEMI?
    ;

updateWhereClause: WHERE (searchCondition | CURRENT OF ( GLOBAL? cursorName | LOCAL_ID))
    ;

outputClause
    : OUTPUT outputDmlListElem (COMMA outputDmlListElem)* (
        INTO ddlObject ( LPAREN columnNameList RPAREN)?
    )?
    ;

outputDmlListElem: (expression | asterisk) asColumnAlias?
    ;

createDatabase
    : CREATE DATABASE id (CONTAINMENT EQ ( NONE | PARTIAL))? (
        ON (PRIMARY? databaseFileSpec ( COMMA databaseFileSpec)*)? (
            id /* LOG */ ON databaseFileSpec (COMMA databaseFileSpec)*
        )?
    )? (COLLATE id)? (WITH createDatabaseOption (COMMA createDatabaseOption)*)? SEMI?
    ;

createDatabaseScopedCredential
    : CREATE DATABASE SCOPED CREDENTIAL id WITH IDENTITY EQ STRING (COMMA SECRET EQ STRING)? SEMI?
    ;

createDatabaseOption
    : FILESTREAM (databaseFilestreamOption (COMMA databaseFilestreamOption)*)
    | genericOption
    ;

createIndex
    : CREATE UNIQUE? clustered? INDEX id ON tableName LPAREN columnNameListWithOrder RPAREN (
        INCLUDE LPAREN columnNameList RPAREN
    )? (WHERE searchCondition)? (createIndexOptions)? (ON id)? SEMI?
    ;

createIndexOptions: WITH LPAREN relationalIndexOption ( COMMA relationalIndexOption)* RPAREN
    ;

relationalIndexOption: rebuildIndexOption | genericOption
    ;

alterIndex
    : ALTER INDEX (id | ALL) ON tableName (
        DISABLE
        | PAUSE
        | ABORT
        | RESUME resumableIndexOptions?
        | reorganizePartition
        | setIndexOptions
        | rebuildPartition
    )
    ;

resumableIndexOptions: WITH LPAREN ( resumableIndexOption (COMMA resumableIndexOption)*) RPAREN
    ;

resumableIndexOption: genericOption | lowPriorityLockWait
    ;

reorganizePartition: REORGANIZE (PARTITION EQ INT)? reorganizeOptions?
    ;

reorganizeOptions: WITH LPAREN (reorganizeOption (COMMA reorganizeOption)*) RPAREN
    ;

reorganizeOption: LOB_COMPACTION EQ onOff | COMPRESS_ALL_ROW_GROUPS EQ onOff
    ;

setIndexOptions: SET LPAREN setIndexOption (COMMA setIndexOption)* RPAREN
    ;

setIndexOption: genericOption
    ;

rebuildPartition
    : REBUILD (PARTITION EQ ALL)? rebuildIndexOptions?
    | REBUILD PARTITION EQ INT singlePartitionRebuildIndexOptions?
    ;

rebuildIndexOptions: WITH LPAREN rebuildIndexOption (COMMA rebuildIndexOption)* RPAREN
    ;

rebuildIndexOption
    : DATA_COMPRESSION EQ (NONE | ROW | PAGE | COLUMNSTORE | COLUMNSTORE_ARCHIVE) onPartitions?
    | XML_COMPRESSION EQ onOff onPartitions?
    | genericOption
    ;

singlePartitionRebuildIndexOptions
    : WITH LPAREN singlePartitionRebuildIndexOption (COMMA singlePartitionRebuildIndexOption)* RPAREN
    ;

singlePartitionRebuildIndexOption
    : genericOption
    | DATA_COMPRESSION EQ (NONE | ROW | PAGE | COLUMNSTORE | COLUMNSTORE_ARCHIVE) onPartitions?
    | XML_COMPRESSION EQ onOff onPartitions?
    | ONLINE EQ (ON (LPAREN lowPriorityLockWait RPAREN)? | OFF)
    ;

onPartitions: ON PARTITIONS LPAREN INT (TO INT)? ( COMMA INT (TO INT)?)* RPAREN
    ;

createColumnstoreIndex
    : CREATE CLUSTERED COLUMNSTORE INDEX id ON tableName createColumnstoreIndexOptions? (ON id)? SEMI?
    ;

createColumnstoreIndexOptions
    : WITH LPAREN columnstoreIndexOption (COMMA columnstoreIndexOption)* RPAREN
    ;

columnstoreIndexOption
    : genericOption
    | DATA_COMPRESSION EQ (COLUMNSTORE | COLUMNSTORE_ARCHIVE) onPartitions?
    ;

createNonclusteredColumnstoreIndex
    : CREATE NONCLUSTERED? COLUMNSTORE INDEX id ON tableName LPAREN columnNameListWithOrder RPAREN (
        WHERE searchCondition
    )? createColumnstoreIndexOptions? (ON id)? SEMI?
    ;

createOrAlterTrigger: createOrAlterDmlTrigger | createOrAlterDdlTrigger
    ;

createOrAlterDmlTrigger
    : (CREATE (OR (ALTER | REPLACE))? | ALTER) TRIGGER dotIdentifier ON tableName (
        WITH dmlTriggerOption (COMMA dmlTriggerOption)*
    )? (FOR | AFTER | INSTEAD OF) dmlTriggerOperation (COMMA dmlTriggerOperation)* (WITH APPEND)? (
        NOT FOR REPLICATION
    )? AS sqlClauses+
    ;

dmlTriggerOption: ENCRYPTION | executeAs
    ;

dmlTriggerOperation: (INSERT | UPDATE | DELETE)
    ;

createOrAlterDdlTrigger
    : (CREATE (OR (ALTER | REPLACE))? | ALTER) TRIGGER dotIdentifier ON (ALL SERVER | DATABASE) (
        WITH dmlTriggerOption (COMMA dmlTriggerOption)*
    )? (FOR | AFTER) ddlTriggerOperation (COMMA ddlTriggerOperation)* AS sqlClauses+
    ;

ddlTriggerOperation: simpleId
    ;

createOrAlterFunction
    : ((CREATE (OR ALTER)?) | ALTER) FUNCTION dotIdentifier (
        (LPAREN procedureParam (COMMA procedureParam)* RPAREN)
        | LPAREN RPAREN
    ) //must have (), but can be empty
    (funcBodyReturnsSelect | funcBodyReturnsTable | funcBodyReturnsScalar) SEMI?
    ;

funcBodyReturnsSelect
    : RETURNS TABLE (WITH functionOption (COMMA functionOption)*)? AS? (
        (EXTERNAL NAME dotIdentifier)
        | RETURN (LPAREN selectStatementStandalone RPAREN | selectStatementStandalone)
    )
    ;

funcBodyReturnsTable
    : RETURNS LOCAL_ID tableTypeDefinition (WITH functionOption (COMMA functionOption)*)? AS? (
        (EXTERNAL NAME dotIdentifier)
        | BEGIN sqlClauses* RETURN SEMI? END SEMI?
    )
    ;

funcBodyReturnsScalar
    : RETURNS dataType (WITH functionOption (COMMA functionOption)*)? AS? (
        (EXTERNAL NAME dotIdentifier)
        | BEGIN sqlClauses* RETURN expression SEMI? END
    )
    ;

functionOption
    : ENCRYPTION
    | SCHEMABINDING
    | RETURNS NULL ON NULL INPUT
    | CALLED ON NULL INPUT
    | executeAs
    ;

createStatistics
    : CREATE STATISTICS id ON tableName LPAREN columnNameList RPAREN (
        WITH (FULLSCAN | SAMPLE INT (PERCENT | ROWS) | STATS_STREAM) (COMMA NORECOMPUTE)? (
            COMMA INCREMENTAL EQ onOff
        )?
    )? SEMI?
    ;

updateStatistics
    : UPDATE STATISTICS tableName (id | LPAREN id ( COMMA id)* RPAREN)? updateStatisticsOptions?
    ;

updateStatisticsOptions: WITH updateStatisticsOption (COMMA updateStatisticsOption)*
    ;

updateStatisticsOption: RESAMPLE onPartitions? | optionList
    ;

createTable: CREATE (createExternal | createInternal)
    ;

createInternal
    : TABLE tableName (LPAREN columnDefTableConstraints COMMA? RPAREN)? tableOptions?
    // This sequence looks strange but alloes CTAS and normal CREATE TABLE to be parsed
    createTableAs? tableOptions? (ON id | DEFAULT | onPartitionOrFilegroup)? (
        TEXTIMAGE_ON id
        | DEFAULT
    )? SEMI?
    ;

createExternal
    : EXTERNAL TABLE tableName (LPAREN columnDefTableConstraints RPAREN)? WITH LPAREN optionList RPAREN (
        AS selectStatementStandalone
    ) SEMI?
    ;

table: TABLE tableName (LPAREN columnDefTableConstraints? COMMA? RPAREN)?
    ;

createTableAs
    : AS selectStatementStandalone
    | AS FILETABLE WITH lparenOptionList
    | AS (NODE | EDGE)
    | AS /* CLONE */ id OF dotIdentifier (AT_KEYWORD STRING)?
    ;

tableIndices
    : INDEX id UNIQUE? clustered? LPAREN columnNameListWithOrder RPAREN
    | INDEX id CLUSTERED COLUMNSTORE
    | INDEX id NONCLUSTERED? COLUMNSTORE LPAREN columnNameList RPAREN createTableIndexOptions? (
        ON id
    )?
    ;

tableOptions
    : WITH (LPAREN tableOption (COMMA tableOption)* RPAREN | tableOption (COMMA tableOption)*)
    ;

distributionType: HASH LPAREN id (COMMA id)* RPAREN | ROUND_ROBIN | REPLICATE
    ;

tableOption
    : DISTRIBUTION EQ distributionType
    | CLUSTERED INDEX LPAREN id (ASC | DESC)? ( COMMA id (ASC | DESC)?)* RPAREN
    | DATA_COMPRESSION EQ (NONE | ROW | PAGE) onPartitions?
    | XML_COMPRESSION EQ onOff onPartitions?
    | id EQ (
        OFF (LPAREN id RPAREN)?
        | ON (LPAREN tableOptionElement (COMMA tableOptionElement)* RPAREN)?
    )
    | genericOption
    ;

tableOptionElement: id EQ dotIdentifier LPAREN optionList RPAREN | genericOption
    ;

createTableIndexOptions
    : WITH LPAREN createTableIndexOption (COMMA createTableIndexOption)* RPAREN
    ;

createTableIndexOption
    : DATA_COMPRESSION EQ (NONE | ROW | PAGE | COLUMNSTORE | COLUMNSTORE_ARCHIVE) onPartitions?
    | XML_COMPRESSION EQ onOff onPartitions?
    | genericOption
    ;

createView
    : (CREATE (OR ALTER)? | ALTER) VIEW dotIdentifier (LPAREN columnNameList RPAREN)? (
        WITH optionList
    )? AS selectStatementStandalone (WITH genericOption)? SEMI?
    ;

alterTable
    : ALTER TABLE tableName (
        alterTableColumn
        | WITH genericOption // CHECK | NOCHECK
        | alterTableAdd
        | alterTableDrop
        | REBUILD tableOptions
        | SWITCH switchPartition
        | SET LPAREN id EQ ON LPAREN optionList RPAREN RPAREN
        | (SET LPAREN optionList RPAREN | genericOption)+
    ) SEMI?
    ;

alterTableDrop
    : DROP (
        dropSet (COMMA dropSet)*
        | WITH? (CHECK | NOCHECK) CONSTRAINT (ALL | id (COMMA id)*)
        | (ENABLE | DISABLE) TRIGGER (ALL | id (COMMA id)*)
        | (ENABLE | DISABLE) CHANGE_TRACKING (WITH LPAREN genericOption RPAREN)?
    ) SEMI?
    ;

dropSet
    : CONSTRAINT? (IF EXISTS)? dropId (COMMA dropId)*
    | COLUMN (IF EXISTS)? id (COMMA id)*
    | /* PERIOD */ id FOR /* SYSTEM_TIME */ id
    ;

dropId: id (WITH dropClusteredConstraintOption (COMMA dropClusteredConstraintOption)*?)
    ;

dropClusteredConstraintOption
    : genericOption
    | MOVE TO id (LPAREN dotIdentifier RPAREN | id | STRING)
    ;

alterTableAdd
    : ADD (
        ( computedColumnDefinition | tableConstraint | columnSetDefinition)+
        | (alterGenerated (COMMA alterGenerated)*)?
    )
    ;

alterGenerated
    : dotIdentifier id GENERATED ALWAYS AS (ROW | TRANSACTION_ID | SEQUENCE_NUMBER) (START | END) HIDDEN_KEYWORD? (
        NOT? NULL
    )? (CONSTRAINT id)? DEFAULT expression (WITH VALUES)?
    | /* PERIOD */ id FOR /* SYSTEM_TIME */ id LPAREN (dotIdentifier COMMA dotIdentifier) RPAREN
    ;

alterTableColumn
    : ALTER COLUMN dotIdentifier (
        (LPAREN INT (COMMA INT)? RPAREN | xmlSchemaCollection) (COLLATE id)? (NULL | NOT NULL)? SPARSE? (
            WITH LPAREN genericOption RPAREN
        )?
        | (ADD | DROP) genericOption (WITH LPAREN genericOption RPAREN)?
    )
    ;

switchPartition
    : (PARTITION? expression)? TO tableName (PARTITION expression)? (WITH lowPriorityLockWait)?
    ;

lowPriorityLockWait
    : WAIT_AT_LOW_PRIORITY LPAREN MAX_DURATION EQ expression MINUTES? COMMA ABORT_AFTER_WAIT EQ abortAfterWait = (
        NONE
        | SELF
        | BLOCKERS
    ) RPAREN
    ;

alterDatabase
    : ALTER DATABASE (id | CURRENT) (
        MODIFY NAME EQ id
        | COLLATE id
        | SET databaseOptionspec (WITH termination)?
        | addOrModifyFiles
        | addOrModifyFilegroups
    ) SEMI?
    ;

addOrModifyFiles
    : ADD id? /* LOG */ FILE fileSpec (COMMA fileSpec)* (TO FILEGROUP id)?
    | REMOVE FILE (id | fileSpec)
    ;

fileSpec
    : LPAREN NAME EQ idOrString (COMMA NEWNAME EQ idOrString)? (COMMA FILENAME EQ STRING)? (
        COMMA SIZE EQ fileSize
    )? (COMMA MAXSIZE EQ (fileSize) | UNLIMITED)? (COMMA FILEGROWTH EQ fileSize)? (COMMA OFFLINE)? RPAREN
    ;

addOrModifyFilegroups
    : ADD FILEGROUP id (CONTAINS FILESTREAM | CONTAINS MEMORY_OPTIMIZED_DATA)?
    | REMOVE FILEGROUP id
    | MODIFY FILEGROUP id (
        filegroupUpdatabilityOption
        | DEFAULT
        | NAME EQ id
        | AUTOGROW_SINGLE_FILE
        | AUTOGROW_ALL_FILES
    )
    ;

filegroupUpdatabilityOption: READONLY | READWRITE | READ_ONLY | READ_WRITE
    ;

databaseOptionspec
    : changeTrackingOption
    | autoOption
    | containmentOption
    | cursorOption
    | databaseMirroringOption
    | dateCorrelationOptimizationOption
    | dbEncryptionOption
    | dbStateOption
    | dbUpdateOption
    | dbUserAccessOption
    | delayedDurabilityOption
    | externalAccessOption
    | FILESTREAM databaseFilestreamOption
    | hadrOptions
    | mixedPageAllocationOption
    | recoveryOption
    | serviceBrokerOption
    | snapshotOption
    | sqlOption
    | targetRecoveryTimeOption
    | termination
    | queryStoreOption
    | genericOption
    ;

queryStoreOption
    : QUERY_STORE (
        EQ (
            OFF (LPAREN /* FORCED */ id RPAREN)?
            | ON (LPAREN queryStoreElementOpt (COMMA queryStoreElementOpt)* RPAREN)?
        )
        | LPAREN queryStoreElementOpt RPAREN
        | ALL
        | id
    )
    ;

queryStoreElementOpt: id EQ LPAREN optionList RPAREN | genericOption
    ;

autoOption
    : AUTO_CLOSE onOff
    | AUTO_CREATE_STATISTICS OFF
    | ON ( INCREMENTAL EQ ON | OFF)
    | AUTO_SHRINK onOff
    | AUTO_UPDATE_STATISTICS onOff
    | AUTO_UPDATE_STATISTICS_ASYNC (ON | OFF)
    ;

changeTrackingOption
    : CHANGE_TRACKING (
        EQ ( OFF | ON)
        | LPAREN (changeTrackingOpt ( COMMA changeTrackingOpt)*) RPAREN
    )
    ;

changeTrackingOpt: AUTO_CLEANUP EQ onOff | CHANGE_RETENTION EQ INT ( DAYS | HOURS | MINUTES)
    ;

containmentOption: CONTAINMENT EQ (NONE | PARTIAL)
    ;

cursorOption: CURSOR_CLOSE_ON_COMMIT onOff | CURSOR_DEFAULT ( LOCAL | GLOBAL)
    ;

alterEndpoint
    : ALTER ENDPOINT id (AUTHORIZATION id)? (STATE EQ state = (STARTED | STOPPED | DISABLED))? AS TCP LPAREN endpointListenerClause RPAREN (
        FOR TSQL LPAREN RPAREN
        | FOR SERVICE_BROKER LPAREN endpointAuthenticationClause (
            COMMA? endpointEncryptionAlogorithmClause
        )? (COMMA? MESSAGE_FORWARDING EQ (ENABLED | DISABLED))? (
            COMMA? MESSAGE_FORWARD_SIZE EQ INT
        )? RPAREN
        | FOR DATABASE_MIRRORING LPAREN endpointAuthenticationClause (
            COMMA? endpointEncryptionAlogorithmClause
        )? COMMA? ROLE EQ (WITNESS | PARTNER | ALL) RPAREN
    )
    ;

databaseMirroringOption: mirroringSetOption
    ;

mirroringSetOption: mirroringPartner partnerOption | mirroringWitness witnessOption
    ;

mirroringPartner: PARTNER
    ;

mirroringWitness: WITNESS
    ;

witnessPartnerEqual: EQ
    ;

partnerOption
    : witnessPartnerEqual partnerServer
    | FAILOVER
    | FORCE_SERVICE_ALLOW_DATA_LOSS
    | OFF
    | RESUME
    | SAFETY (FULL | OFF)
    | SUSPEND
    | TIMEOUT INT
    ;

witnessOption: witnessPartnerEqual witnessServer | OFF
    ;

witnessServer: partnerServer
    ;

partnerServer: partnerServerTcpPrefix host mirroringHostPortSeperator portNumber
    ;

mirroringHostPortSeperator: COLON
    ;

partnerServerTcpPrefix: TCP COLON DOUBLE_FORWARD_SLASH
    ;

portNumber: INT
    ;

host: id DOT host | (id DOT | id)
    ;

dateCorrelationOptimizationOption: DATE_CORRELATION_OPTIMIZATION onOff
    ;

dbEncryptionOption: ENCRYPTION onOff
    ;

dbStateOption: (ONLINE | OFFLINE | EMERGENCY)
    ;

dbUpdateOption: READ_ONLY | READ_WRITE
    ;

dbUserAccessOption: SINGLE_USER | RESTRICTED_USER | MULTI_USER
    ;

delayedDurabilityOption: genericOption
    ;

externalAccessOption
    : DB_CHAINING onOff
    | TRUSTWORTHY onOff
    | DEFAULT_LANGUAGE EQ ( id | STRING)
    | DEFAULT_FULLTEXT_LANGUAGE EQ ( id | STRING)
    | NESTED_TRIGGERS EQ ( OFF | ON)
    | TRANSFORM_NOISE_WORDS EQ ( OFF | ON)
    | TWO_DIGIT_YEAR_CUTOFF EQ INT
    ;

hadrOptions: HADR ( (AVAILABILITY GROUP EQ id | OFF) | (SUSPEND | RESUME))
    ;

mixedPageAllocationOption: MIXED_PAGE_ALLOCATION (OFF | ON)
    ;

recoveryOption: genericOption
    ;

serviceBrokerOption
    : ENABLE_BROKER
    | DISABLE_BROKER
    | NEW_BROKER
    | ERROR_BROKER_CONVERSATIONS
    | HONOR_BROKER_PRIORITY onOff
    ;

snapshotOption
    : ALLOW_SNAPSHOT_ISOLATION onOff
    | READ_COMMITTED_SNAPSHOT (ON | OFF)
    | MEMORY_OPTIMIZED_ELEVATE_TO_SNAPSHOT = (ON | OFF)
    ;

sqlOption
    : ANSI_NULL_DEFAULT onOff
    | ANSI_NULLS onOff
    | ANSI_PADDING onOff
    | ANSI_WARNINGS onOff
    | ARITHABORT onOff
    | COMPATIBILITY_LEVEL EQ INT
    | CONCAT_NULL_YIELDS_NULL onOff
    | NUMERIC_ROUNDABORT onOff
    | QUOTED_IDENTIFIER onOff
    | RECURSIVE_TRIGGERS onOff
    ;

targetRecoveryTimeOption: TARGET_RECOVERY_TIME EQ INT (SECONDS | MINUTES)
    ;

termination: ROLLBACK AFTER INT | ROLLBACK IMMEDIATE | NO_WAIT
    ;

dropIndex
    : DROP INDEX (IF EXISTS)? (
        dropRelationalOrXmlOrSpatialIndex (COMMA dropRelationalOrXmlOrSpatialIndex)*
        | dropBackwardCompatibleIndex ( COMMA dropBackwardCompatibleIndex)*
    ) SEMI?
    ;

dropRelationalOrXmlOrSpatialIndex: id ON tableName
    ;

dropBackwardCompatibleIndex: dotIdentifier
    ;

dropTrigger: dropDmlTrigger | dropDdlTrigger
    ;

dropDmlTrigger: DROP TRIGGER (IF EXISTS)? dotIdentifier (COMMA dotIdentifier)* SEMI?
    ;

dropDdlTrigger
    : DROP TRIGGER (IF EXISTS)? dotIdentifier (COMMA dotIdentifier)* ON (DATABASE | ALL SERVER) SEMI?
    ;

dropFunction: DROP FUNCTION (IF EXISTS)? dotIdentifier ( COMMA dotIdentifier)* SEMI?
    ;

dropStatistics: DROP STATISTICS (COMMA? dotIdentifier)+ SEMI
    ;

dropTable: DROP TABLE (IF EXISTS)? tableName (COMMA tableName)* SEMI?
    ;

dropView: DROP VIEW (IF EXISTS)? dotIdentifier (COMMA dotIdentifier)* SEMI?
    ;

createType
    : CREATE TYPE dotIdentifier (FROM dataType nullNotnull?)? (
        AS TABLE LPAREN columnDefTableConstraints RPAREN
    )?
    ;

dropType: DROP TYPE (IF EXISTS)? dotIdentifier
    ;

rowsetFunctionLimited: openquery | opendatasource
    ;

openquery: OPENQUERY LPAREN id COMMA STRING RPAREN
    ;

opendatasource: OPENDATASOURCE LPAREN STRING COMMA STRING RPAREN dotIdentifier
    ;

// TODO: JI - Simplify me
declareStatement
    : DECLARE LOCAL_ID AS? (dataType | tableTypeDefinition | tableName | xmlTypeDefinition)
    | DECLARE declareLocal (COMMA declareLocal)*
    | WITH xmlNamespaces
    ;

cursorStatement
    : CLOSE GLOBAL? cursorName SEMI?
    | DEALLOCATE GLOBAL? CURSOR? cursorName SEMI?
    | declareCursor
    | fetchCursor
    | OPEN GLOBAL? cursorName SEMI?
    ;

backupDatabase
    : BACKUP DATABASE id (READ_WRITE_FILEGROUPS (COMMA optionList)?)? optionList? (TO optionList) (
        MIRROR TO optionList
    )? (
        WITH (
            ENCRYPTION LPAREN ALGORITHM EQ genericOption COMMA SERVER CERTIFICATE EQ genericOption RPAREN
            | optionList
        )
    )? SEMI?
    ;

backupLog: BACKUP id /* LOG */ id TO optionList (MIRROR TO optionList)? ( WITH optionList)?
    ;

backupCertificate
    : BACKUP CERTIFICATE id TO FILE EQ STRING (
        WITH PRIVATE KEY LPAREN (
            COMMA? FILE EQ STRING
            | COMMA? ENCRYPTION BY PASSWORD EQ STRING
            | COMMA? DECRYPTION BY PASSWORD EQ STRING
        )+ RPAREN
    )?
    ;

backupMasterKey: BACKUP MASTER KEY TO FILE EQ STRING ENCRYPTION BY PASSWORD EQ STRING
    ;

backupServiceMasterKey
    : BACKUP SERVICE MASTER KEY TO FILE EQ STRING ENCRYPTION BY PASSWORD EQ STRING
    ;

killStatement: KILL (killProcess | killQueryNotification | killStatsJob)
    ;

killProcess: (sessionId = (INT | STRING) | UOW) (WITH STATUSONLY)?
    ;

killQueryNotification: QUERY NOTIFICATION SUBSCRIPTION ( ALL | INT)
    ;

killStatsJob: STATS JOB INT
    ;

executeStatement: EXECUTE executeBody SEMI?
    ;

executeBodyBatch: dotIdentifier (executeStatementArg (COMMA executeStatementArg)*)? SEMI?
    ;

executeBody
    : (LOCAL_ID EQ)? (dotIdentifier | executeVarString) (
        executeStatementArg (COMMA executeStatementArg)*
    )?
    | LPAREN executeVarString (COMMA executeVarString)* RPAREN (AS (LOGIN | USER) EQ STRING)? (
        AT_KEYWORD id
    )?
    | AS ( (LOGIN | USER) EQ STRING | CALLER)
    ;

// In practice unnamed arguments must precede named arguments, but we assume the input is syntactically valid
// and accept them in any order to simplitfy the grammar
executeStatementArg: (LOCAL_ID EQ)? executeParameter
    ;

executeParameter: ( constant | LOCAL_ID (OUTPUT | OUT)? | id | DEFAULT | NULL)
    ;

executeVarString
    : LOCAL_ID (OUTPUT | OUT)? (PLUS LOCAL_ID (PLUS executeVarString)?)?
    | STRING (PLUS LOCAL_ID (PLUS executeVarString)?)?
    ;

securityStatement
    : executeAs SEMI?
    | GRANT (ALL PRIVILEGES? | grantPermission (LPAREN columnNameList RPAREN)?) (
        ON (classTypeForGrant COLON COLON)? tableName
    )? TO toPrincipal += principalId (COMMA toPrincipal += principalId)* (WITH GRANT OPTION)? (
        AS principalId
    )? SEMI?
    | REVERT (WITH COOKIE EQ LOCAL_ID)? SEMI?
    | openKey
    | closeKey
    | createKey
    | createCertificate
    ;

principalId: id | PUBLIC
    ;

createCertificate
    : CREATE CERTIFICATE id (AUTHORIZATION id)? (FROM existingKeys | generateNewKeys) (
        ACTIVE FOR BEGIN DIALOG EQ onOff
    )?
    ;

existingKeys
    : ASSEMBLY id
    | EXECUTABLE? FILE EQ STRING (WITH PRIVATE KEY LPAREN privateKeyOptions RPAREN)?
    ;

privateKeyOptions
    : (FILE | HEX) EQ STRING (COMMA (DECRYPTION | ENCRYPTION) BY PASSWORD EQ STRING)?
    ;

generateNewKeys: (ENCRYPTION BY PASSWORD EQ STRING)? WITH SUBJECT EQ STRING ( COMMA dateOptions)*
    ;

dateOptions: (START_DATE | EXPIRY_DATE) EQ STRING
    ;

openKey
    : OPEN SYMMETRIC KEY id DECRYPTION BY decryptionMechanism
    | OPEN MASTER KEY DECRYPTION BY PASSWORD EQ STRING
    ;

closeKey: CLOSE SYMMETRIC KEY id | CLOSE ALL SYMMETRIC KEYS | CLOSE MASTER KEY
    ;

createKey
    : CREATE MASTER KEY ENCRYPTION BY PASSWORD EQ STRING
    | CREATE SYMMETRIC KEY id (AUTHORIZATION id)? (FROM PROVIDER id)? WITH (
        (keyOptions | ENCRYPTION BY encryptionMechanism) COMMA?
    )+
    ;

keyOptions
    : KEY_SOURCE EQ STRING
    | ALGORITHM EQ algorithm
    | IDENTITY_VALUE EQ STRING
    | PROVIDER_KEY_NAME EQ STRING
    | CREATION_DISPOSITION EQ (CREATE_NEW | OPEN_EXISTING)
    ;

algorithm
    : DES
    | TRIPLE_DES
    | TRIPLE_DES_3KEY
    | RC2
    | RC4
    | RC4_128
    | DESX
    | AES_128
    | AES_192
    | AES_256
    ;

encryptionMechanism: CERTIFICATE id | ASYMMETRIC KEY id | SYMMETRIC KEY id | PASSWORD EQ STRING
    ;

decryptionMechanism
    : CERTIFICATE id (WITH PASSWORD EQ STRING)?
    | ASYMMETRIC KEY id (WITH PASSWORD EQ STRING)?
    | SYMMETRIC KEY id
    | PASSWORD EQ STRING
    ;

grantPermission
    : ADMINISTER genericOption
    | ALTER ( ANY? genericOption)?
    | AUTHENTICATE SERVER?
    | BACKUP genericOption
    | CHECKPOINT
    | CONNECT genericOption?
    | CONTROL SERVER?
    | CREATE genericOption
    | DELETE
    | EXECUTE genericOption?
    | EXTERNAL genericOption
    | IMPERSONATE genericOption?
    | INSERT
    | KILL genericOption
    | RECEIVE
    | REFERENCES
    | SELECT genericOption?
    | SEND
    | SHOWPLAN
    | SHUTDOWN
    | SUBSCRIBE QUERY NOTIFICATIONS
    | TAKE OWNERSHIP
    | UNMASK
    | UNSAFE ASSEMBLY
    | UPDATE
    | VIEW ( ANY genericOption | genericOption)
    ;

setStatement
    : SET LOCAL_ID (DOT id)? EQ expression
    | SET LOCAL_ID assignmentOperator expression
    | SET LOCAL_ID EQ CURSOR declareSetCursorCommon (FOR (READ ONLY | UPDATE (OF columnNameList)?))?
    | setSpecial
    ;

transactionStatement
    : BEGIN DISTRIBUTED (TRAN | TRANSACTION) (id | LOCAL_ID)?
    | BEGIN (TRAN | TRANSACTION) ( (id | LOCAL_ID) (WITH MARK STRING)?)?
    | COMMIT (TRAN | TRANSACTION) (
        (id | LOCAL_ID) (WITH LPAREN DELAYED_DURABILITY EQ (OFF | ON) RPAREN)?
    )?
    | COMMIT WORK?
    | COMMIT id
    | ROLLBACK id
    | ROLLBACK (TRAN | TRANSACTION) (id | LOCAL_ID)?
    | ROLLBACK WORK?
    | SAVE (TRAN | TRANSACTION) (id | LOCAL_ID)?
    ;

goStatement: GO INT? SEMI?
    ;

useStatement: USE id
    ;

setuserStatement: SETUSER STRING?
    ;

reconfigureStatement: RECONFIGURE (WITH OVERRIDE)?
    ;

shutdownStatement: SHUTDOWN (WITH genericOption)?
    ;

checkpointStatement: CHECKPOINT (INT)?
    ;

dbccCheckallocOption: ALL_ERRORMSGS | NO_INFOMSGS | TABLOCK | ESTIMATEONLY
    ;

dbccCheckalloc
    : CHECKALLOC (
        LPAREN (id | STRING | INT) (
            COMMA NOINDEX
            | COMMA ( REPAIR_ALLOW_DATA_LOSS | REPAIR_FAST | REPAIR_REBUILD)
        )? RPAREN (WITH dbccCheckallocOption (COMMA dbccCheckallocOption)*)?
    )?
    ;

dbccCheckcatalog: CHECKCATALOG (LPAREN (id | STRING | INT) RPAREN)? ( WITH NO_INFOMSGS)?
    ;

dbccCheckconstraintsOption: ALL_CONSTRAINTS | ALL_ERRORMSGS | NO_INFOMSGS
    ;

dbccCheckconstraints
    : CHECKCONSTRAINTS (LPAREN (id | STRING) RPAREN)? (
        WITH dbccCheckconstraintsOption ( COMMA dbccCheckconstraintsOption)*
    )?
    ;

dbccCheckdbTableOption: genericOption
    ;

dbccCheckdb
    : CHECKDB (
        LPAREN (id | STRING | INT) (
            COMMA (NOINDEX | REPAIR_ALLOW_DATA_LOSS | REPAIR_FAST | REPAIR_REBUILD)
        )? RPAREN
    )? (WITH dbccCheckdbTableOption ( COMMA dbccCheckdbTableOption)*)?
    ;

dbccCheckfilegroupOption: genericOption
    ;

dbccCheckfilegroup
    : CHECKFILEGROUP (
        LPAREN (INT | STRING) (
            COMMA (NOINDEX | REPAIR_ALLOW_DATA_LOSS | REPAIR_FAST | REPAIR_REBUILD)
        )? RPAREN
    )? (WITH dbccCheckfilegroupOption ( COMMA dbccCheckfilegroupOption)*)?
    ;

dbccChecktable
    : CHECKTABLE LPAREN STRING (
        COMMA (NOINDEX | expression | REPAIR_ALLOW_DATA_LOSS | REPAIR_FAST | REPAIR_REBUILD)
    )? RPAREN (WITH dbccCheckdbTableOption (COMMA dbccCheckdbTableOption)*)?
    ;

dbccCleantable
    : CLEANTABLE LPAREN (id | STRING | INT) COMMA (id | STRING) (COMMA INT)? RPAREN (
        WITH NO_INFOMSGS
    )?
    ;

dbccClonedatabaseOption
    : NO_STATISTICS
    | NO_QUERYSTORE
    | SERVICEBROKER
    | VERIFY_CLONEDB
    | BACKUP_CLONEDB
    ;

dbccClonedatabase
    : CLONEDATABASE LPAREN id COMMA id RPAREN (
        WITH dbccClonedatabaseOption (COMMA dbccClonedatabaseOption)*
    )?
    ;

dbccPdwShowspaceused: PDW_SHOWSPACEUSED (LPAREN id RPAREN)? ( WITH IGNORE_REPLICATED_TABLE_CACHE)?
    ;

dbccProccache: PROCCACHE (WITH NO_INFOMSGS)?
    ;

dbccShowcontigOption: genericOption
    ;

dbccShowcontig
    : SHOWCONTIG (LPAREN expression ( COMMA expression)? RPAREN)? (
        WITH dbccShowcontigOption (COMMA dbccShowcontigOption)*
    )?
    ;

dbccShrinklog
    : SHRINKLOG (LPAREN SIZE EQ ((INT ( MB | GB | TB)) | DEFAULT) RPAREN)? (WITH NO_INFOMSGS)?
    ;

dbccDbreindex
    : DBREINDEX LPAREN idOrString (COMMA idOrString ( COMMA expression)?)? RPAREN (
        WITH NO_INFOMSGS
    )?
    ;

dbccDllFree: id LPAREN FREE RPAREN ( WITH NO_INFOMSGS)?
    ;

dbccDropcleanbuffers: DROPCLEANBUFFERS (LPAREN COMPUTE | ALL RPAREN)? (WITH NO_INFOMSGS)?
    ;

dbccClause
    : DBCC (
        dbccCheckalloc
        | dbccCheckcatalog
        | dbccCheckconstraints
        | dbccCheckdb
        | dbccCheckfilegroup
        | dbccChecktable
        | dbccCleantable
        | dbccClonedatabase
        | dbccDbreindex
        | dbccDllFree
        | dbccDropcleanbuffers
        | dbccPdwShowspaceused
        | dbccProccache
        | dbccShowcontig
        | dbccShrinklog
    )
    ;

executeAs: EXECUTE AS (CALLER | SELF | OWNER | STRING)
    ;

declareLocal: LOCAL_ID AS? dataType (EQ expression)?
    ;

tableTypeDefinition: TABLE LPAREN columnDefTableConstraints ( COMMA? tableTypeIndices)* RPAREN
    ;

tableTypeIndices
    : (((PRIMARY KEY | INDEX id) (CLUSTERED | NONCLUSTERED)?) | UNIQUE) LPAREN columnNameListWithOrder RPAREN
    | CHECK LPAREN searchCondition RPAREN
    ;

columnDefTableConstraints: columnDefTableConstraint (COMMA? columnDefTableConstraint)*
    ;

columnDefTableConstraint
    : columnDefinition
    | computedColumnDefinition
    | tableConstraint
    | tableIndices
    ;

computedColumnDefinition: id AS expression (PERSISTED (NOT NULL)?)? columnConstraint?
    ;

columnSetDefinition: id XML id FOR id
    ;

columnDefinition: id dataType columnDefinitionElement* columnIndex?
    ;

columnDefinitionElement
    : MASKED WITH LPAREN FUNCTION EQ STRING RPAREN
    | defaultValue
    | identityColumn
    | generatedAs
    | ROWGUIDCOL
    | ENCRYPTED WITH LPAREN COLUMN_ENCRYPTION_KEY EQ STRING COMMA ENCRYPTION_TYPE EQ (
        DETERMINISTIC
        | RANDOMIZED
    ) COMMA ALGORITHM EQ STRING RPAREN
    | columnConstraint
    | genericOption // TSQL column flags and options that we cannot support in Databricks
    ;

generatedAs
    : GENERATED ALWAYS AS (ROW | TRANSACTION_ID | SEQUENCE_NUMBER) (START | END) HIDDEN_KEYWORD?
    ;

identityColumn: IDENTITY (LPAREN INT COMMA INT RPAREN)?
    ;

defaultValue: (CONSTRAINT id)? DEFAULT expression
    ;

columnConstraint
    : (CONSTRAINT id)? (
        NOT? NULL
        | ((PRIMARY KEY | UNIQUE) clustered? primaryKeyOptions)
        | ( (FOREIGN KEY)? foreignKeyOptions)
        | checkConstraint
    )
    ;

columnIndex
    : INDEX id clustered? createTableIndexOptions? onPartitionOrFilegroup? (
        FILESTREAM_ON id // CHeck for quoted "NULL"
    )?
    ;

onPartitionOrFilegroup: ON ( ( id LPAREN id RPAREN) | id | DEFAULT_DOUBLE_QUOTE)
    ;

tableConstraint
    : (CONSTRAINT cid = id)? (
        ((PRIMARY KEY | UNIQUE) clustered? LPAREN columnNameListWithOrder RPAREN primaryKeyOptions)
        | ( FOREIGN KEY LPAREN columnNameList RPAREN foreignKeyOptions)
        | ( CONNECTION LPAREN connectionNode ( COMMA connectionNode)* RPAREN)
        | ( DEFAULT expression FOR defid = id ( WITH VALUES)?)
        | checkConstraint
    )
    ;

connectionNode: id TO id
    ;

primaryKeyOptions: (WITH FILLFACTOR EQ INT)? alterTableIndexOptions? onPartitionOrFilegroup?
    ;

foreignKeyOptions
    : REFERENCES tableName (LPAREN columnNameList RPAREN)? onDelete? onUpdate? (
        NOT FOR REPLICATION
    )?
    ;

checkConstraint: CHECK (NOT FOR REPLICATION)? LPAREN searchCondition RPAREN
    ;

onDelete: ON DELETE (NO ACTION | CASCADE | SET NULL | SET DEFAULT)
    ;

onUpdate: ON UPDATE (NO ACTION | CASCADE | SET NULL | SET DEFAULT)
    ;

alterTableIndexOptions: WITH LPAREN alterTableIndexOption ( COMMA alterTableIndexOption)* RPAREN
    ;

alterTableIndexOption
    : DATA_COMPRESSION EQ (NONE | ROW | PAGE | COLUMNSTORE | COLUMNSTORE_ARCHIVE) onPartitions?
    | XML_COMPRESSION EQ onOff onPartitions?
    | DISTRIBUTION EQ HASH LPAREN id RPAREN
    | CLUSTERED INDEX LPAREN id (ASC | DESC)? ( COMMA id (ASC | DESC)?)* RPAREN
    | ONLINE EQ (ON (LPAREN lowPriorityLockWait RPAREN)? | OFF)
    | genericOption
    ;

declareCursor
    : DECLARE cursorName (
        CURSOR ( declareSetCursorCommon ( FOR UPDATE (OF columnNameList)?)?)?
        | (SEMI_SENSITIVE | INSENSITIVE)? SCROLL? CURSOR FOR selectStatementStandalone (
            FOR (READ ONLY | UPDATE | (OF columnNameList))
        )?
    ) SEMI?
    ;

declareSetCursorCommon: declareSetCursorCommonPartial* FOR selectStatementStandalone
    ;

declareSetCursorCommonPartial
    : (LOCAL | GLOBAL)
    | (FORWARD_ONLY | SCROLL)
    | (STATIC | KEYSET | DYNAMIC | FAST_FORWARD)
    | (READ_ONLY | SCROLL_LOCKS | OPTIMISTIC)
    | TYPE_WARNING
    ;

fetchCursor
    : FETCH (( NEXT | PRIOR | FIRST | LAST | (ABSOLUTE | RELATIVE) expression)? FROM)? GLOBAL? cursorName (
        INTO LOCAL_ID (COMMA LOCAL_ID)*
    )? SEMI?
    ;

setSpecial
    : SET id (id | constant_LOCAL_ID | onOff) SEMI?
    | SET STATISTICS expression onOff
    // TODO: Extract these keywords (IO | TIME | XML | PROFILE) onOff SEMI?
    | SET ROWCOUNT (LOCAL_ID | INT) SEMI?
    | SET TEXTSIZE INT SEMI?
    | SET TRANSACTION ISOLATION LEVEL (
        READ UNCOMMITTED
        | READ COMMITTED
        | REPEATABLE READ
        | SNAPSHOT
        | SERIALIZABLE
        | INT
    ) SEMI?
    | SET IDENTITY_INSERT tableName onOff SEMI?
    | SET specialList (COMMA specialList)* onOff
    // TODO: Rework when it is time to implement SET modifyMethod
    ;

specialList
    : ANSI_NULLS
    | QUOTED_IDENTIFIER
    | ANSI_PADDING
    | ANSI_WARNINGS
    | ANSI_DEFAULTS
    | ANSI_NULL_DFLT_OFF
    | ANSI_NULL_DFLT_ON
    | ARITHABORT
    | ARITHIGNORE
    | CONCAT_NULL_YIELDS_NULL
    | CURSOR_CLOSE_ON_COMMIT
    | FMTONLY
    | FORCEPLAN
    | IMPLICIT_TRANSACTIONS
    | NOCOUNT
    | NOEXEC
    | NUMERIC_ROUNDABORT
    | PARSEONLY
    | REMOTE_PROC_TRANSACTIONS
    | SHOWPLAN_ALL
    | SHOWPLAN_TEXT
    | SHOWPLAN_XML
    | XACT_ABORT
    ;

constant_LOCAL_ID: constant | LOCAL_ID
    ;

expression
    : LPAREN expression RPAREN                                # exprPrecedence
    | <assoc = right> BIT_NOT expression                      # exprBitNot
    | <assoc = right> op = (PLUS | MINUS) expression          # exprUnary
    | expression op = (STAR | DIV | MOD) expression           # exprOpPrec1
    | expression op = (PLUS | MINUS) expression               # exprOpPrec2
    | expression op = (BIT_AND | BIT_XOR | BIT_OR) expression # exprOpPrec3
    | expression op = DOUBLE_BAR expression                   # exprOpPrec4
    | expression op = DOUBLE_COLON expression                 # exprOpPrec4
    | primitiveExpression                                     # exprPrimitive
    | functionCall                                            # exprFunc
    | functionValues                                          # exprFuncVal
    | expression COLLATE id                                   # exprCollate
    | caseExpression                                          # exprCase
    | expression timeZone                                     # exprTz
    | expression overClause                                   # exprOver
    | expression withinGroup                                  # exprWithinGroup
    | DOLLAR_ACTION                                           # exprDollar
    | <assoc = right> expression DOT expression               # exprDot
    | LPAREN selectStatement RPAREN                           # exprSubquery
    | ALL expression                                          # exprAll
    | DISTINCT expression                                     # exprDistinct
    | DOLLAR_ACTION                                           # exprDollar
    | STAR                                                    # exprStar
    | id                                                      # exprId
    ;

// TODO: Implement this ?
parameter: PLACEHOLDER
    ;

timeZone
    : AT_KEYWORD id ZONE expression // AT TIME ZONE
    ;

primitiveExpression: op = (DEFAULT | NULL | LOCAL_ID) | constant
    ;

caseExpression: CASE caseExpr = expression? switchSection+ ( ELSE elseExpr = expression)? END
    ;

withExpression: WITH xmlNamespaces? commonTableExpression ( COMMA commonTableExpression)*
    ;

commonTableExpression: id (LPAREN columnNameList RPAREN)? AS LPAREN selectStatement RPAREN
    ;

updateElem
    : (l1 = LOCAL_ID EQ)? (fullColumnName | l2 = LOCAL_ID) op = (
        EQ
        | PE
        | ME
        | SE
        | DE
        | MEA
        | AND_ASSIGN
        | XOR_ASSIGN
        | OR_ASSIGN
    ) expression                             # updateElemCol
    | id DOT id LPAREN expressionList RPAREN # updateElemUdt
    ;

searchCondition
    : LPAREN searchCondition RPAREN       # scPrec
    | NOT searchCondition                 # scNot
    | searchCondition AND searchCondition # scAnd
    | searchCondition OR searchCondition  # scOr
    | predicate                           # scPred
    ;

predicate
    : EXISTS LPAREN selectStatement RPAREN                                           # predExists
    | freetextPredicate                                                              # predFreetext
    | expression comparisonOperator expression                                       # predBinop
    | expression comparisonOperator (ALL | SOME | ANY) LPAREN selectStatement RPAREN # predASA
    | expression NOT? BETWEEN expression AND expression                              # predBetween
    | expression NOT? IN LPAREN (selectStatement | expressionList) RPAREN            # predIn
    | expression NOT? LIKE expression (ESCAPE expression)?                           # predLike
    | expression IS NOT? NULL                                                        # predIsNull
    | expression                                                                     # predExpression
    ;

queryExpression
    : querySpecification sqlUnion*
    | LPAREN queryExpression RPAREN (UNION ALL? queryExpression)?
    ;

sqlUnion
    // TODO: Handle INTERSECT precedence in the grammar; it has higher precedence than EXCEPT and UNION ALL.
    // Reference: https://learn.microsoft.com/en-us/sql/t-sql/language-elements/set-operators-except-and-intersect-transact-sql?view=sql-server-ver16#:~:text=following%20precedence
    : (UNION ALL? | EXCEPT | INTERSECT) (querySpecification | (LPAREN queryExpression RPAREN))
    ;

querySpecification
    : SELECT (ALL | DISTINCT)? topClause? selectListElem (COMMA selectListElem)* selectOptionalClauses
    ;

selectOptionalClauses
    // TODO: Fix ORDER BY; it needs to be outside the set operations instead of between.
    // Reference: https://learn.microsoft.com/en-us/sql/t-sql/language-elements/set-operators-union-transact-sql?view=sql-server-ver16#c-using-union-of-two-select-statements-with-order-by
    : intoClause? fromClause? whereClause? groupByClause? havingClause? selectOrderByClause?
    ;

groupByClause
    : GROUP BY (
        (ALL? expression (COMMA expression)*) (WITH id)?
        // Note that id should be checked for CUBE or ROLLUP
        | GROUPING SETS LPAREN groupingSetsItem ( COMMA groupingSetsItem)* RPAREN
    )
    ;

groupingSetsItem: LPAREN? expression (COMMA expression)* RPAREN? | LPAREN RPAREN
    ;

intoClause: INTO tableName
    ;

fromClause: FROM tableSources
    ;

whereClause: WHERE searchCondition
    ;

havingClause: HAVING searchCondition
    ;

topClause: TOP ( expression | LPAREN expression RPAREN) PERCENT? (WITH TIES)?
    ;

orderByClause: ORDER BY orderByExpression (COMMA orderByExpression)*
    ;

selectOrderByClause
    : orderByClause (
        OFFSET expression (ROW | ROWS) (FETCH (FIRST | NEXT) expression (ROW | ROWS) ONLY)?
    )?
    ;

// Unsupported in Databricks SQL
forClause
    : FOR BROWSE
    | FOR XML (RAW (LPAREN STRING RPAREN)? | AUTO) xmlCommonDirectives* (
        COMMA (XMLDATA | XMLSCHEMA (LPAREN STRING RPAREN)?)
    )? (COMMA ELEMENTS (XSINIL | ABSENT)?)?
    | FOR XML EXPLICIT xmlCommonDirectives* (COMMA XMLDATA)?
    | FOR XML PATH (LPAREN STRING RPAREN)? xmlCommonDirectives* (COMMA ELEMENTS (XSINIL | ABSENT)?)?
    | FOR JSON (AUTO | PATH) (
        COMMA (ROOT (LPAREN STRING RPAREN) | INCLUDE_NULL_VALUES | WITHOUT_ARRAY_WRAPPER)
    )*
    ;

orderByExpression: expression (COLLATE expression)? (ASC | DESC)?
    ;

optionClause: OPTION lparenOptionList
    ;

selectList: selectElement += selectListElem ( COMMA selectElement += selectListElem)*
    ;

asterisk: (INSERTED | DELETED) DOT STAR | (tableName DOT)? STAR
    ;

expressionElem: columnAlias EQ expression | expression asColumnAlias?
    ;

selectListElem
    : asterisk
    | LOCAL_ID op = (PE | ME | SE | DE | MEA | AND_ASSIGN | XOR_ASSIGN | OR_ASSIGN | EQ) expression
    | expressionElem
    ;

tableSources: source += tableSource (COMMA source += tableSource)*
    ;

tableSource: tableSourceItem joinPart*
    ;

// Almost all tableSource elements allow a table alias, and sone allow a list of column aliaes
// As this parser expects to see valid child anyway, we combine this into a single rule and
// then visit each possible table source individually, applying alias afterwards. This reduces
// rule complexity and parser complexity substantially.
tableSourceItem: tsiElement (asTableAlias columnAliasList?)? withTableHints?
    ;

tsiElement
    : tableName                                                   # tsiNamedTable
    | rowsetFunction                                              # tsiRowsetFunction
    | LPAREN derivedTable RPAREN                                  # tsiDerivedTable
    | changeTable                                                 # tsiChangeTable
    | nodesMethod                                                 # tsiNodesMethod
    | /* TODO (id DOT)? distinguish xml functions */ functionCall # tsiFunctionCall
    | LOCAL_ID                                                    # tsiLocalId
    | LOCAL_ID DOT functionCall                                   # tsiLocalIdFunctionCall
    | openXml                                                     # tsiOpenXml
    | openJson                                                    # tsiOpenJson
    | dotIdentifier? DOUBLE_COLON functionCall                    # tsiDoubleColonFunctionCall
    | LPAREN tableSource RPAREN                                   # tsiParenTableSource
    ;

openJson
    : OPENJSON LPAREN expression (COMMA expression)? RPAREN (WITH LPAREN jsonDeclaration RPAREN)? asTableAlias?
    ;

jsonDeclaration: jsonCol += jsonColumnDeclaration ( COMMA jsonCol += jsonColumnDeclaration)*
    ;

jsonColumnDeclaration: columnDeclaration (AS JSON)?
    ;

columnDeclaration: id dataType STRING?
    ;

changeTable: changeTableChanges | changeTableVersion
    ;

changeTableChanges
    : CHANGETABLE LPAREN CHANGES tableName COMMA changesid = (NULL | INT | LOCAL_ID) RPAREN
    ;

changeTableVersion
    : CHANGETABLE LPAREN VERSION tableName COMMA fullColumnNameList COMMA selectList RPAREN
    ;

joinPart: joinOn | crossJoin | apply | pivot | unpivot
    ;

outerJoin: (LEFT | RIGHT | FULL) OUTER?
    ;

joinType: INNER | outerJoin
    ;

joinOn
    : joinType? (joinHint = (LOOP | HASH | MERGE | REMOTE))? JOIN source = tableSource ON cond = searchCondition
    ;

crossJoin: CROSS JOIN tableSourceItem
    ;

apply: (CROSS | OUTER) APPLY tableSourceItem
    ;

pivot: PIVOT pivotClause asTableAlias
    ;

unpivot: UNPIVOT unpivotClause asTableAlias
    ;

pivotClause: LPAREN expression FOR fullColumnName IN columnAliasList RPAREN
    ;

unpivotClause: LPAREN id FOR id IN LPAREN fullColumnNameList RPAREN RPAREN
    ;

fullColumnNameList: column += fullColumnName (COMMA column += fullColumnName)*
    ;

rowsetFunction
    : (
        OPENROWSET LPAREN STRING COMMA ((STRING SEMI STRING SEMI STRING) | STRING) (
            COMMA (dotIdentifier | STRING)
        ) RPAREN
    )
    | (OPENROWSET LPAREN BULK STRING COMMA ( id EQ STRING COMMA optionList? | id) RPAREN)
    ;

derivedTable: selectStatement | tableValueConstructor | LPAREN tableValueConstructor RPAREN
    ;

functionCall
    : builtInFunctions
    | standardFunction
    | freetextFunction
    | partitionFunction
    | hierarchyidStaticMethod
    ;

// Things that are just special values and not really functions, but are documented as if they are functions
functionValues: f = ( AAPSEUDO | SESSION_USER | SYSTEM_USER | USER)
    ;

// Standard functions that are built in but take standard syntax, or are
// some user function etc
standardFunction: funcId LPAREN (expression (COMMA expression)*)? RPAREN
    ;

funcId: id | FORMAT | LEFT | RIGHT | REPLACE | CONCAT
    ;

partitionFunction: (id DOT)? DOLLAR_PARTITION DOT id LPAREN expression RPAREN
    ;

freetextFunction
    : f = (
        SEMANTICSIMILARITYDETAILSTABLE
        | SEMANTICSIMILARITYTABLE
        | SEMANTICKEYPHRASETABLE
        | CONTAINSTABLE
        | FREETEXTTABLE
    ) LPAREN expression COMMA (expression | LPAREN expressionList RPAREN | STAR) COMMA expression (
        COMMA LANGUAGE expression
    )? (COMMA expression)? RPAREN
    ;

freetextPredicate
    : CONTAINS LPAREN (
        fullColumnName
        | LPAREN fullColumnName (COMMA fullColumnName)* RPAREN
        | STAR
        | PROPERTY LPAREN fullColumnName COMMA expression RPAREN
    ) COMMA expression RPAREN
    | FREETEXT LPAREN tableName COMMA (
        fullColumnName
        | LPAREN fullColumnName (COMMA fullColumnName)* RPAREN
        | STAR
    ) COMMA expression (COMMA LANGUAGE expression)? RPAREN
    ;

builtInFunctions
    : NEXT VALUE FOR tableName                                                        # nextValueFor
    | (CAST | TRY_CAST) LPAREN expression AS dataType RPAREN                          # cast
    | JSON_ARRAY LPAREN expressionList? jsonNullClause? RPAREN                        # jsonArray
    | JSON_OBJECT LPAREN (jsonKeyValue (COMMA jsonKeyValue)*)? jsonNullClause? RPAREN # jsonObject
    ;

jsonKeyValue: expression COLON expression
    ;

jsonNullClause: (loseNulls = ABSENT | NULL) ON NULL
    ;

hierarchyidStaticMethod
    : HIERARCHYID DOUBLE_COLON (GETROOT LPAREN RPAREN | PARSE LPAREN input = expression RPAREN)
    ;

nodesMethod
    : (locId = LOCAL_ID | valueId = fullColumnName | LPAREN selectStatement RPAREN) DOT NODES LPAREN xquery = STRING RPAREN
    ;

switchSection: WHEN searchCondition THEN expression
    ;

asColumnAlias: AS? columnAlias
    ;

asTableAlias: AS? (id | DOUBLE_QUOTE_ID)
    ;

withTableHints: WITH LPAREN tableHint (COMMA? tableHint)* RPAREN
    ;

tableHint
    : INDEX EQ? LPAREN expressionList RPAREN
    | FORCESEEK ( LPAREN expression LPAREN columnNameList RPAREN RPAREN)?
    | genericOption
    ;

columnAliasList: LPAREN columnAlias (COMMA columnAlias)* RPAREN
    ;

columnAlias: id | STRING
    ;

tableValueConstructor: VALUES tableValueRow (COMMA tableValueRow)*
    ;

tableValueRow: LPAREN expressionList RPAREN
    ;

expressionList: exp += expression (COMMA exp += expression)*
    ;

withinGroup: WITHIN GROUP LPAREN orderByClause RPAREN
    ;

// The ((IGNORE | RESPECT) NULLS)? is strictly speaking, not part of the OVER clause
// but trails certain windowing functions such as LAG and LEAD. However, all such functions
// must use the OVER clause, so it is included here to make build the IR simpler.
overClause
    : ((IGNORE | RESPECT) NULLS)? OVER LPAREN (PARTITION BY expression (COMMA expression)*)? orderByClause? rowOrRangeClause? RPAREN
    ;

rowOrRangeClause: (ROWS | RANGE) windowFrameExtent
    ;

windowFrameExtent: windowFrameBound | BETWEEN windowFrameBound AND windowFrameBound
    ;

windowFrameBound: UNBOUNDED (PRECEDING | FOLLOWING) | INT (PRECEDING | FOLLOWING) | CURRENT ROW
    ;

databaseFilestreamOption
    : LPAREN ((NON_TRANSACTED_ACCESS EQ ( OFF | READ_ONLY | FULL)) | ( DIRECTORY_NAME EQ STRING)) RPAREN
    ;

databaseFileSpec: fileGroup | fileSpecification
    ;

fileGroup
    : FILEGROUP id (CONTAINS FILESTREAM)? (DEFAULT)? (CONTAINS MEMORY_OPTIMIZED_DATA)? fileSpecification (
        COMMA fileSpecification
    )*
    ;

fileSpecification
    : LPAREN NAME EQ (id | STRING) COMMA? FILENAME EQ file = STRING COMMA? (
        SIZE EQ fileSize COMMA?
    )? (MAXSIZE EQ (fileSize | UNLIMITED) COMMA?)? (FILEGROWTH EQ fileSize COMMA?)? RPAREN
    ;

tableName: (linkedServer = id DOT DOT)? ids += id (DOT ids += id)*
    ;

dotIdentifier: id (DOT id)*
    ;

ddlObject: tableName | rowsetFunctionLimited | LOCAL_ID
    ;

fullColumnName: ((DELETED | INSERTED | tableName) DOT)? ( id | (DOLLAR (IDENTITY | ROWGUID)))
    ;

columnNameListWithOrder: columnNameWithOrder (COMMA columnNameWithOrder)*
    ;

columnNameWithOrder: id (ASC | DESC)?
    ;

columnNameList: id (COMMA id)*
    ;

cursorName: id | LOCAL_ID
    ;

onOff: ON | OFF
    ;

clustered: CLUSTERED | NONCLUSTERED
    ;

nullNotnull: NOT? NULL
    ;

beginConversationTimer
    : BEGIN CONVERSATION TIMER LPAREN LOCAL_ID RPAREN TIMEOUT EQ expression SEMI?
    ;

beginConversationDialog
    : BEGIN DIALOG (CONVERSATION)? LOCAL_ID FROM SERVICE serviceName TO SERVICE serviceName (
        COMMA STRING
    )? ON CONTRACT contractName (
        WITH ((RELATED_CONVERSATION | RELATED_CONVERSATION_GROUP) EQ LOCAL_ID COMMA?)? (
            LIFETIME EQ (INT | LOCAL_ID) COMMA?
        )? (ENCRYPTION EQ onOff)?
    )? SEMI?
    ;

contractName: (id | expression)
    ;

serviceName: (id | expression)
    ;

endConversation
    : END CONVERSATION LOCAL_ID SEMI? (
        WITH (
            ERROR EQ faliureCode = (LOCAL_ID | STRING) DESCRIPTION EQ failureText = (
                LOCAL_ID
                | STRING
            )
        )? CLEANUP?
    )?
    ;

waitforConversation: WAITFOR? LPAREN getConversation RPAREN (COMMA? TIMEOUT expression)? SEMI?
    ;

getConversation
    : GET CONVERSATION GROUP conversationGroupId = (STRING | LOCAL_ID) FROM dotIdentifier SEMI?
    ;

sendConversation
    : SEND ON CONVERSATION conversationHandle = (STRING | LOCAL_ID) MESSAGE TYPE expression (
        LPAREN messageBodyExpression = (STRING | LOCAL_ID) RPAREN
    )? SEMI?
    ;

dataType: dataTypeIdentity | XML LPAREN id RPAREN | id (LPAREN (INT | MAX) (COMMA INT)? RPAREN)?
    ;

dataTypeList: dataType (COMMA dataType)*
    ;

dataTypeIdentity: id IDENTITY (LPAREN INT COMMA INT RPAREN)?
    ;

constant: con = (STRING | HEX | INT | REAL | FLOAT | MONEY) | parameter
    ;

id: ID | TEMP_ID | DOUBLE_QUOTE_ID | SQUARE_BRACKET_ID | NODEID | keyword | RAW
    ;

simpleId: ID
    ;

idOrString: id | STRING
    ;

// Spaces are allowed for comparison operators.
comparisonOperator
    : EQ
    | GT
    | LT
    | LT EQ
    | GT EQ
    | LT GT
    | EQ
    | BANG EQ
    | GT
    | BANG GT
    | LT
    | BANG LT
    ;

assignmentOperator: PE | ME | SE | DE | MEA | AND_ASSIGN | XOR_ASSIGN | OR_ASSIGN
    ;

fileSize: INT (KB | MB | GB | TB | MOD)?
    ;

/**
 * The parenthesised option list is used in many places, so it is defined here.
 */
lparenOptionList: LPAREN optionList RPAREN
    ;

/**
 * The generic option list is used in many places, so it is defined here.
 */
optionList: genericOption (COMMA genericOption)*
    ;

/**
 * Generic options have a few different formats, but otherwise they can almost all be
 * parsed generically rather than creating potentially hundreds of keywords and rules
 * that obfusctate the grammar and make maintenance difficult as TSQL evolves. SQL is,
 * or has become, a very verbose language with strange syntactical elements bolted in
 * becuase they could not fit otherwise. So, as many options as possible are parsed
 * here and the AST builders can decide what to do with them as they have context.
 *
 * Here are the various formats:
 *
 * KEYWORD                   - Just means the option is ON if it is present, OFF if NOT (but check semenatics)
 * KEYWORD ON|OFF            - The option is on or off (no consitency here)
 * KEYWORD = VALUE           - The option is set to a value - we accept any expression and assume
 *                             the AST builder will check the type and range, OR that we require valid
 *                             TSQL in the first place.
 * KEYWORD = VALUE KB        - Some sort of size value, where KB can be various things so is parsed as any id()
 * KEYWORD (=)? DEFAULT      - A fairly redundant option, but sometimes people want to be explicit
 * KEYWORD (=)? AUTO         - The option is set to AUTO, which occurs in a few places
 * something FOR something    - The option is a special case such as OPTIMIZE FOR UNKNOWN
 * DEFAULT                   - The option is set to the default value but is not named
 * ON                        - The option is on but is not named (will get just id)
 * OFF                       - The option is off but is not named (will get just id)
 * AUTO                      - The option is set to AUTO but is not named (will get just id)
 * ALL                       - The option is set to ALL but is not named (will get just id)
 */
genericOption
    : id EQ? (
        DEFAULT          // Default value  - don't resolve with expression
        | ON             // Simple ON      - don't resolve with expression
        | OFF            // Simple OFF     - don't resolve with expression
        | AUTO           // Simple AUTO    - don't resolve with expression
        | STRING         // String value   - don't resolve with expression
        | FOR id         // FOR id         - don't resolve with expression - special case
        | expression id? // Catch all for less explicit options, sometimes with extra keywords
    )?
    ;

// XML stuff

dropXmlSchemaCollection
    : DROP XML SCHEMA COLLECTION (relationalSchema = id DOT)? sqlIdentifier = id
    ;

schemaDeclaration: columnDeclaration (COMMA columnDeclaration)*
    ;

createXmlSchemaCollection
    : CREATE XML SCHEMA COLLECTION (relationalSchema = id DOT)? sqlIdentifier = id AS (
        STRING
        | id
        | LOCAL_ID
    )
    ;

openXml
    : OPENXML LPAREN expression COMMA expression (COMMA expression)? RPAREN (
        WITH LPAREN schemaDeclaration RPAREN
    )? asTableAlias?
    ;

xmlNamespaces: XMLNAMESPACES LPAREN xmlDeclaration (COMMA xmlDeclaration)* RPAREN
    ;

xmlDeclaration: STRING AS id | DEFAULT STRING
    ;

xmlTypeDefinition: XML LPAREN (CONTENT | DOCUMENT)? xmlSchemaCollection RPAREN
    ;

xmlSchemaCollection: ID DOT ID
    ;

createXmlIndex
    : CREATE PRIMARY? XML INDEX id ON tableName LPAREN id RPAREN (
        USING XML INDEX id (FOR (VALUE | PATH | PROPERTY)?)?
    )? xmlIndexOptions? SEMI?
    ;

xmlIndexOptions: WITH LPAREN xmlIndexOption (COMMA xmlIndexOption)* RPAREN
    ;

xmlIndexOption: ONLINE EQ (ON (LPAREN lowPriorityLockWait RPAREN)? | OFF) | genericOption
    ;

xmlCommonDirectives: COMMA ( BINARY id | TYPE | ROOT (LPAREN STRING RPAREN)?)
    ;
