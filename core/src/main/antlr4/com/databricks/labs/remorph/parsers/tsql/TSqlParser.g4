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

options {
    tokenVocab = TSqlLexer;
}

tSqlFile: batch? EOF
    ;

// TODO: Simplify this
batch
    : goStatement
    | executeBodyBatch? (goStatement | sqlClauses+) goStatement*
    | batchLevelStatement goStatement*
    ;

batchLevelStatement
    : createOrAlterFunction
    | createOrAlterProcedure
    | createOrAlterTrigger
    | createView
    ;

sqlClauses
    : dmlClause SEMI?
    | cflStatement SEMI?
    | anotherStatement SEMI?
    | ddlClause SEMI?
    | dbccClause SEMI?
    | backupStatement SEMI?
    | SEMI
    ;

dmlClause
    : mergeStatement
    | deleteStatement
    | insertStatement
    | selectStatementStandalone
    | updateStatement
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
    | createDatabase
    | createDatabaseAuditSpecification
    | createDbRole
    | createEndpoint
    | createEventNotification
    | createExternalLibrary
    | createExternalResourcePool
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
    | disableTrigger
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
    | enableTrigger
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
    ;

blockStatement: BEGIN SEMI? sqlClauses* END SEMI?
    ;

breakStatement: BREAK SEMI?
    ;

continueStatement: CONTINUE SEMI?
    ;

gotoStatement: GOTO id SEMI? | id COLON SEMI?
    ;

returnStatement: RETURN expression? SEMI?
    ;

ifStatement: IF searchCondition sqlClauses (ELSE sqlClauses)? SEMI?
    ;

throwStatement: THROW ( throwErrorNumber COMMA throwMessage COMMA throwState)? SEMI?
    ;

throwErrorNumber: INT | LOCAL_ID
    ;

throwMessage: STRING | LOCAL_ID
    ;

throwState: INT | LOCAL_ID
    ;

tryCatchStatement
    : BEGIN TRY SEMI? tryClauses = sqlClauses+ END TRY SEMI? BEGIN CATCH SEMI? catchClauses = sqlClauses* END CATCH SEMI?
    ;

waitforStatement: WAITFOR receiveStatement? COMMA? (id t = expression)? expression? SEMI?
    ;

whileStatement: WHILE searchCondition ( sqlClauses | BREAK SEMI? | CONTINUE SEMI?)
    ;

printStatement: PRINT (expression | DOUBLE_QUOTE_ID) (COMMA LOCAL_ID)* SEMI?
    ;

raiseerrorStatement
    : RAISERROR LPAREN msg = (INT | STRING | LOCAL_ID) COMMA severity = constant_LOCAL_ID COMMA state = constant_LOCAL_ID (
        COMMA (constant_LOCAL_ID | NULL_)
    )* RPAREN (WITH genericOption)? SEMI?
    | RAISERROR INT formatstring = (STRING | LOCAL_ID | DOUBLE_QUOTE_ID) (
        COMMA argument += (INT | STRING | LOCAL_ID)
    )*
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
    : ALTER APPLICATION ROLE applictionRole = id WITH (COMMA? NAME EQ newApplicationRoleName = id)? (
        COMMA? PASSWORD EQ applicationRolePassword = STRING
    )? (COMMA? DEFAULT_SCHEMA EQ appRoleDefaultSchema = id)?
    ;

alterXmlSchemaCollection: ALTER XML SCHEMA COLLECTION id (DOT id)? ADD STRING
    ;

createApplicationRole: CREATE APPLICATION ROLE id WITH optionList
    ;

dropAggregate: DROP AGGREGATE (IF EXISTS)? id (DOT id)?
    ;

dropApplicationRole: DROP APPLICATION ROLE rolename = id
    ;

alterAssembly: ALTER ASSEMBLY id alterAssemblyClause
    ;

alterAssemblyClause
    : alterAssemblyFromClause? alterAssemblyWithClause? alterAssemblyDropClause? alterAssemblyAddClause?
    ;

alterAssemblyFromClause: FROM (STRING | AS id)
    ;

alterAssemblyDropClause: DROP optionList
    ;

alterAssemblyAddClause: ADD FILE FROM alterAssemblyClientFileClause
    ;

alterAssemblyClientFileClause: STRING (AS id)?
    ;

alterAssemblyWithClause: WITH optionList
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

alterAuthorization: ALTER AUTHORIZATION ON (classType DOUBLE_COLON)? entityName TO genericOption
    ;

classType: id id? id?
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
    | SQL LOGIN
    | SYMMETRIC KEY
    | TRIGGER ( DATABASE | SERVER)
    | TYPE
    | USER
    | XML SCHEMA COLLECTION
    ;

dropAvailabilityGroup: DROP AVAILABILITY GROUP groupName = id
    ;

alterAvailabilityGroup: alterAvailabilityGroupStart alterAvailabilityGroupOptions
    ;

alterAvailabilityGroupStart: ALTER AVAILABILITY GROUP groupName = id
    ;

alterAvailabilityGroupOptions
    : SET LPAREN (
        (
            AUTOMATED_BACKUP_PREFERENCE EQ (PRIMARY | SECONDARY_ONLY | SECONDARY | NONE)
            | FAILURE_CONDITION_LEVEL EQ INT
            | HEALTH_CHECK_TIMEOUT EQ milliseconds = INT
            | DB_FAILOVER EQ ( ON | OFF)
            | REQUIRED_SYNCHRONIZED_SECONDARIES_TO_COMMIT EQ INT
        ) RPAREN
    )
    | ADD DATABASE databaseName = id
    | REMOVE DATABASE databaseName = id
    | ADD REPLICA ON serverInstance = STRING (
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
        | SESSION_TIMEOUT EQ sessionTimeout = INT
    )
    | MODIFY REPLICA ON serverInstance = STRING (
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
            | SESSION_TIMEOUT EQ sessionTimeout = INT
        )
    ) RPAREN
    | REMOVE REPLICA ON STRING
    | JOIN
    | JOIN AVAILABILITY GROUP ON (
        COMMA? agName = STRING WITH LPAREN (
            LISTENER_URL EQ STRING COMMA AVAILABILITY_MODE EQ (
                SYNCHRONOUS_COMMIT
                | ASYNCHRONOUS_COMMIT
            ) COMMA FAILOVER_MODE EQ MANUAL COMMA SEEDING_MODE EQ (AUTOMATIC | MANUAL) RPAREN
        )
    )+
    | MODIFY AVAILABILITY GROUP ON (
        COMMA? agNameModified = STRING WITH LPAREN (
            LISTENER_URL EQ STRING (
                COMMA? AVAILABILITY_MODE EQ (SYNCHRONOUS_COMMIT | ASYNCHRONOUS_COMMIT)
            )? (COMMA? FAILOVER_MODE EQ MANUAL)? (COMMA? SEEDING_MODE EQ (AUTOMATIC | MANUAL))? RPAREN
        )
    )+
    | GRANT CREATE ANY DATABASE
    | DENY CREATE ANY DATABASE
    | FAILOVER
    | FORCE_FAILOVER_ALLOW_DATA_LOSS
    | ADD LISTENER listenerName = STRING LPAREN (
        WITH DHCP (ON LPAREN ipV4_failover ipV4_failover RPAREN)
        | WITH IP LPAREN (
            (COMMA? LPAREN ( ipV4_failover COMMA ipV4_failover | ipV6_failover) RPAREN)+ RPAREN (
                COMMA PORT EQ INT
            )?
        )
    ) RPAREN
    | MODIFY LISTENER (
        ADD IP LPAREN ( ipV4_failover ipV4_failover | ipV6_failover) RPAREN
        | PORT EQ INT
    )
    | RESTART LISTENER STRING
    | REMOVE LISTENER STRING
    | OFFLINE
    | WITH LPAREN DTC_SUPPORT EQ PER_DB RPAREN
    ;

ipV4_failover: STRING
    ;

ipV6_failover: STRING
    ;

createOrAlterBrokerPriority
    : (CREATE | ALTER) BROKER PRIORITY ConversationPriorityName = id FOR CONVERSATION SET LPAREN (
        CONTRACT_NAME EQ ( ( id) | ANY) COMMA?
    )? (LOCAL_SERVICE_NAME EQ (DOUBLE_FORWARD_SLASH? id | ANY) COMMA?)? (
        REMOTE_SERVICE_NAME EQ (RemoteServiceName = STRING | ANY) COMMA?
    )? (PRIORITY_LEVEL EQ ( PriorityValue = INT | DEFAULT))? RPAREN
    ;

dropBrokerPriority: DROP BROKER PRIORITY ConversationPriorityName = id
    ;

alterCertificate
    : ALTER CERTIFICATE certificateName = id (
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
    : ALTER COLUMN ENCRYPTION KEY columnEncryptionKey = id (ADD | DROP) VALUE LPAREN COLUMN_MASTER_KEY EQ columnMasterKeyName = id (
        COMMA ALGORITHM EQ algorithmName = STRING COMMA ENCRYPTED_VALUE EQ HEX
    )? RPAREN
    ;

createColumnEncryptionKey
    : CREATE COLUMN ENCRYPTION KEY columnEncryptionKey = id WITH VALUES (
        LPAREN COMMA? COLUMN_MASTER_KEY EQ columnMasterKeyName = id COMMA ALGORITHM EQ algorithmName = STRING COMMA ENCRYPTED_VALUE EQ encryptedValue
            = HEX RPAREN COMMA?
    )+
    ;

dropCertificate: DROP CERTIFICATE certificateName = id
    ;

dropColumnEncryptionKey: DROP COLUMN ENCRYPTION KEY keyName = id
    ;

dropColumnMasterKey: DROP COLUMN MASTER KEY keyName = id
    ;

dropContract: DROP CONTRACT droppedContractName = id
    ;

dropCredential: DROP CREDENTIAL credentialName = id
    ;

dropCryptograhicProvider: DROP CRYPTOGRAPHIC PROVIDER providerName = id
    ;

dropDatabase: DROP DATABASE (IF EXISTS)? ( COMMA? databaseNameOrDatabaseSnapshotName = id)+
    ;

dropDatabaseAuditSpecification: DROP DATABASE AUDIT SPECIFICATION auditSpecificationName = id
    ;

dropDatabaseEncryptionKey: DROP DATABASE ENCRYPTION KEY
    ;

dropDatabaseScopedCredential: DROP DATABASE SCOPED CREDENTIAL credentialName = id
    ;

dropDefault: DROP DEFAULT (IF EXISTS)? ( COMMA? (schemaName = id DOT)? defaultName = id)
    ;

dropEndpoint: DROP ENDPOINT endPointName = id
    ;

dropExternalDataSource: DROP EXTERNAL DATA SOURCE externalDataSourceName = id
    ;

dropExternalFileFormat: DROP EXTERNAL FILE FORMAT externalFileFormatName = id
    ;

dropExternalLibrary: DROP EXTERNAL LIBRARY libraryName = id ( AUTHORIZATION ownerName = id)?
    ;

dropExternalResourcePool: DROP EXTERNAL RESOURCE POOL poolName = id
    ;

dropExternalTable: DROP EXTERNAL TABLE (databaseName = id DOT)? ( schemaName = id DOT)? table = id
    ;

dropEventNotifications
    : DROP EVENT NOTIFICATION (COMMA? notificationName = id)+ ON (
        SERVER
        | DATABASE
        | QUEUE queueName = id
    )
    ;

dropEventSession: DROP EVENT SESSION eventSessionName = id ON SERVER
    ;

dropFulltextCatalog: DROP FULLTEXT CATALOG catalogName = id
    ;

dropFulltextIndex: DROP FULLTEXT INDEX ON (schema = id DOT)? table = id
    ;

dropFulltextStoplist: DROP FULLTEXT STOPLIST stoplistName = id
    ;

dropLogin: DROP LOGIN loginName = id
    ;

dropMasterKey: DROP MASTER KEY
    ;

dropMessageType: DROP MESSAGE TYPE messageTypeName = id
    ;

dropPartitionFunction: DROP PARTITION FUNCTION partitionFunctionName = id
    ;

dropPartitionScheme: DROP PARTITION SCHEME partitionSchemeName = id
    ;

dropQueue: DROP QUEUE (databaseName = id DOT)? (schemaName = id DOT)? queueName = id
    ;

dropRemoteServiceBinding: DROP REMOTE SERVICE BINDING bindingName = id
    ;

dropResourcePool: DROP RESOURCE POOL poolName = id
    ;

dropDbRole: DROP ROLE (IF EXISTS)? roleName = id
    ;

dropRoute: DROP ROUTE routeName = id
    ;

dropRule: DROP RULE (IF EXISTS)? ( COMMA? (schemaName = id DOT)? ruleName = id)?
    ;

dropSchema: DROP SCHEMA (IF EXISTS)? schemaName = id
    ;

dropSearchPropertyList: DROP SEARCH PROPERTY LIST propertyListName = id
    ;

dropSecurityPolicy
    : DROP SECURITY POLICY (IF EXISTS)? (schemaName = id DOT)? securityPolicyName = id
    ;

dropSequence
    : DROP SEQUENCE (IF EXISTS)? (
        COMMA? (databaseName = id DOT)? (schemaName = id DOT)? sequenceName = id
    )?
    ;

dropServerAudit: DROP SERVER AUDIT auditName = id
    ;

dropServerAuditSpecification: DROP SERVER AUDIT SPECIFICATION auditSpecificationName = id
    ;

dropServerRole: DROP SERVER ROLE roleName = id
    ;

dropService: DROP SERVICE droppedServiceName = id
    ;

dropSignature
    : DROP (COUNTER)? SIGNATURE FROM (schemaName = id DOT)? moduleName = id BY (
        COMMA? CERTIFICATE certName = id
        | COMMA? ASYMMETRIC KEY AsymKeyName = id
    )+
    ;

dropStatisticsNameAzureDwAndPdw
    : DROP STATISTICS (schemaName = id DOT)? objectName = id DOT statisticsName = id
    ;

dropSymmetricKey: DROP SYMMETRIC KEY symmetricKeyName = id ( REMOVE PROVIDER KEY)?
    ;

dropSynonym: DROP SYNONYM (IF EXISTS)? (schema = id DOT)? synonymName = id
    ;

dropUser: DROP USER (IF EXISTS)? userName = id
    ;

dropWorkloadGroup: DROP WORKLOAD GROUP groupName = id
    ;

disableTrigger
    : DISABLE TRIGGER ((COMMA? (schemaName = id DOT)? triggerName = id)+ | ALL) ON (
        (schemaId = id DOT)? objectName = id
        | DATABASE
        | ALL SERVER
    )
    ;

enableTrigger
    : ENABLE TRIGGER ((COMMA? (schemaName = id DOT)? triggerName = id)+ | ALL) ON (
        (schemaId = id DOT)? objectName = id
        | DATABASE
        | ALL SERVER
    )
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
    : CREATE COLUMN MASTER KEY keyName = id WITH LPAREN KEY_STORE_PROVIDER_NAME EQ keyStoreProviderName = STRING COMMA KEY_PATH EQ keyPath = STRING
        RPAREN
    ;

alterCredential
    : ALTER CREDENTIAL credentialName = id WITH IDENTITY EQ identityName = STRING (
        COMMA SECRET EQ secret = STRING
    )?
    ;

createCredential
    : CREATE CREDENTIAL credentialName = id WITH IDENTITY EQ identityName = STRING (
        COMMA SECRET EQ secret = STRING
    )? (FOR CRYPTOGRAPHIC PROVIDER cryptographicProviderName = id)?
    ;

alterCryptographicProvider
    : ALTER CRYPTOGRAPHIC PROVIDER providerName = id (FROM FILE EQ cryptoProviderDdlFile = STRING)? (
        ENABLE
        | DISABLE
    )?
    ;

createCryptographicProvider: CREATE CRYPTOGRAPHIC PROVIDER id FROM FILE EQ STRING
    ;

createEndpoint
    : CREATE ENDPOINT endpointname = id (AUTHORIZATION login = id)? (
        STATE EQ state = (STARTED | STOPPED | DISABLED)
    )? AS TCP LPAREN endpointListenerClause RPAREN (
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
        WINDOWS (NTLM | KERBEROS | NEGOTIATE)? ( CERTIFICATE certName = id)?
        | CERTIFICATE certName = id WINDOWS? ( NTLM | KERBEROS | NEGOTIATE)?
    )
    ;

endpointListenerClause
    : LISTENER_PORT EQ port = INT (
        COMMA LISTENER_IP EQ (ALL | LPAREN (ipv4 = IPV4_ADDR | ipv6 = STRING) RPAREN)
    )?
    ;

createEventNotification
    : CREATE EVENT NOTIFICATION eventNotificationName = id ON (
        SERVER
        | DATABASE
        | QUEUE queueName = id
    ) (WITH FAN_IN)? FOR (COMMA? eventTypeOrGroup = id)+ TO SERVICE brokerService = STRING COMMA brokerServiceSpecifierOrCurrentDatabase = STRING
    ;

createOrAlterEventSession
    : (CREATE | ALTER) EVENT SESSION eventSessionName = id ON SERVER (
        COMMA? ADD EVENT ((eventModuleGuid = id DOT)? eventPackageName = id DOT eventName = id) (
            LPAREN (SET ( COMMA? eventCustomizableAttributue = id EQ ( INT | STRING))*)? (
                ACTION LPAREN (
                    COMMA? (eventModuleGuid = id DOT)? eventPackageName = id DOT actionName = id
                )+ RPAREN
            )+ (WHERE eventSessionPredicateExpression)? RPAREN
        )*
    )* (COMMA? DROP EVENT (eventModuleGuid = id DOT)? eventPackageName = id DOT eventName = id)* (
        (ADD TARGET (eventModuleGuid = id DOT)? eventPackageName = id DOT targetName = id) (
            LPAREN SET (COMMA? targetParameterName = id EQ ( LPAREN? INT RPAREN? | STRING))+ RPAREN
        )*
    )* (DROP TARGET (eventModuleGuid = id DOT)? eventPackageName = id DOT targetName = id)* (
        WITH LPAREN (COMMA? MAX_MEMORY EQ maxMemory = INT (KB | MB))? (
            COMMA? EVENT_RETENTION_MODE EQ (
                ALLOW_SINGLE_EVENT_LOSS
                | ALLOW_MULTIPLE_EVENT_LOSS
                | NO_EVENT_LOSS
            )
        )? (COMMA? MAX_DISPATCH_LATENCY EQ ( maxDispatchLatencySeconds = INT SECONDS | INFINITE))? (
            COMMA? MAX_EVENT_SIZE EQ maxEventSize = INT (KB | MB)
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
    : (
        eventFieldName = id
        | (
            eventFieldName = id
            | ((eventModuleGuid = id DOT)? eventPackageName = id DOT predicateSourceName = id)
        ) (EQ | (LT GT) | (BANG EQ) | GT | (GT EQ) | LT | LT EQ) (INT | STRING)
    )
    | (eventModuleGuid = id DOT)? eventPackageName = id DOT predicateCompareName = id LPAREN (
        eventFieldName = id
        | ((eventModuleGuid = id DOT)? eventPackageName = id DOT predicateSourceName = id) COMMA (
            INT
            | STRING
        )
    ) RPAREN
    ;

alterExternalDataSource
    : ALTER EXTERNAL DATA SOURCE dataSourceName = id SET (
        LOCATION EQ location = STRING COMMA?
        | RESOURCE_MANAGER_LOCATION EQ resourceManagerLocation = STRING COMMA?
        | CREDENTIAL EQ credentialName = id
    )+
    | ALTER EXTERNAL DATA SOURCE dataSourceName = id WITH LPAREN TYPE EQ BLOB_STORAGE COMMA LOCATION EQ location = STRING (
        COMMA CREDENTIAL EQ credentialName = id
    )? RPAREN
    ;

alterExternalLibrary
    : ALTER EXTERNAL LIBRARY libraryName = id (AUTHORIZATION ownerName = id)? (SET | ADD) (
        LPAREN CONTENT EQ (clientLibrary = STRING | HEX | NONE) (
            COMMA PLATFORM EQ (WINDOWS | LINUX)? RPAREN
        ) WITH (COMMA? LANGUAGE EQ (R | PYTHON) | DATA_SOURCE EQ externalDataSourceName = id)+ RPAREN
    )
    ;

createExternalLibrary
    : CREATE EXTERNAL LIBRARY libraryName = id (AUTHORIZATION ownerName = id)? FROM (
        COMMA? LPAREN? (CONTENT EQ)? (clientLibrary = STRING | HEX | NONE) (
            COMMA PLATFORM EQ (WINDOWS | LINUX)? RPAREN
        )?
    ) (WITH ( COMMA? LANGUAGE EQ (R | PYTHON) | DATA_SOURCE EQ externalDataSourceName = id)+ RPAREN)?
    ;

alterExternalResourcePool
    : ALTER EXTERNAL RESOURCE POOL (poolName = id | DEFAULT_DOUBLE_QUOTE) WITH LPAREN MAX_CPU_PERCENT EQ maxCpuPercent = INT (
        COMMA? AFFINITY CPU EQ ( AUTO | (COMMA? INT TO INT | COMMA INT)+)
        | NUMANODE EQ (COMMA? INT TO INT | COMMA? INT)+
    ) (COMMA? MAX_MEMORY_PERCENT EQ maxMemoryPercent = INT)? (
        COMMA? MAX_PROCESSES EQ maxProcesses = INT
    )? RPAREN
    ;

createExternalResourcePool
    : CREATE EXTERNAL RESOURCE POOL poolName = id WITH LPAREN MAX_CPU_PERCENT EQ maxCpuPercent = INT (
        COMMA? AFFINITY CPU EQ ( AUTO | (COMMA? INT TO INT | COMMA INT)+)
        | NUMANODE EQ (COMMA? INT TO INT | COMMA? INT)+
    ) (COMMA? MAX_MEMORY_PERCENT EQ maxMemoryPercent = INT)? (
        COMMA? MAX_PROCESSES EQ maxProcesses = INT
    )? RPAREN
    ;

alterFulltextCatalog
    : ALTER FULLTEXT CATALOG catalogName = id (
        REBUILD (WITH ACCENT_SENSITIVITY EQ (ON | OFF))?
        | REORGANIZE
        | AS DEFAULT
    )
    ;

createFulltextCatalog
    : CREATE FULLTEXT CATALOG catalogName = id (ON FILEGROUP filegroup = id)? (
        IN PATH rootpath = STRING
    )? (WITH ACCENT_SENSITIVITY EQ (ON | OFF))? (AS DEFAULT)? (AUTHORIZATION ownerName = id)?
    ;

alterFulltextStoplist
    : ALTER FULLTEXT STOPLIST stoplistName = id (
        ADD stopword = STRING LANGUAGE (STRING | INT | HEX)
        | DROP (stopword = STRING LANGUAGE (STRING | INT | HEX) | ALL (STRING | INT | HEX) | ALL)
    )
    ;

createFulltextStoplist
    : CREATE FULLTEXT STOPLIST stoplistName = id (
        FROM ((databaseName = id DOT)? sourceStoplistName = id | SYSTEM STOPLIST)
    )? (AUTHORIZATION ownerName = id)?
    ;

alterLoginSqlServer
    : ALTER LOGIN loginName = id (
        (ENABLE | DISABLE)?
        | WITH (
            (PASSWORD EQ ( password = STRING | passwordHash = HEX HASHED)) (MUST_CHANGE | UNLOCK)*
        )? (OLD_PASSWORD EQ oldPassword = STRING ( MUST_CHANGE | UNLOCK)*)? (
            DEFAULT_DATABASE EQ defaultDatabase = id
        )? (DEFAULT_LANGUAGE EQ defaultLaguage = id)? (NAME EQ loginName = id)? (
            CHECK_POLICY EQ (ON | OFF)
        )? (CHECK_EXPIRATION EQ (ON | OFF))? (CREDENTIAL EQ credentialName = id)? (NO CREDENTIAL)?
        | (ADD | DROP) CREDENTIAL credentialName = id
    )
    ;

createLoginSqlServer
    : CREATE LOGIN loginName = id (
        WITH (
            (PASSWORD EQ ( password = STRING | passwordHash = HEX HASHED)) (MUST_CHANGE | UNLOCK)*
        )? (COMMA? SID EQ sid = HEX)? (COMMA? DEFAULT_DATABASE EQ defaultDatabase = id)? (
            COMMA? DEFAULT_LANGUAGE EQ defaultLaguage = id
        )? (COMMA? CHECK_EXPIRATION EQ (ON | OFF))? (COMMA? CHECK_POLICY EQ (ON | OFF))? (
            COMMA? CREDENTIAL EQ credentialName = id
        )?
        | (
            FROM (
                WINDOWS (
                    WITH (COMMA? DEFAULT_DATABASE EQ defaultDatabase = id)? (
                        COMMA? DEFAULT_LANGUAGE EQ defaultLanguage = STRING
                    )?
                )
                | CERTIFICATE certname = id
                | ASYMMETRIC KEY asymKeyName = id
            )
        )
    )
    ;

alterLoginAzureSql
    : ALTER LOGIN loginName = id (
        (ENABLE | DISABLE)?
        | WITH (
            PASSWORD EQ password = STRING (OLD_PASSWORD EQ oldPassword = STRING)?
            | NAME EQ loginName = id
        )
    )
    ;

createLoginAzureSql: CREATE LOGIN loginName = id WITH PASSWORD EQ STRING ( SID EQ sid = HEX)?
    ;

alterLoginAzureSqlDwAndPdw
    : ALTER LOGIN loginName = id (
        (ENABLE | DISABLE)?
        | WITH (
            PASSWORD EQ password = STRING (
                OLD_PASSWORD EQ oldPassword = STRING (MUST_CHANGE | UNLOCK)*
            )?
            | NAME EQ loginName = id
        )
    )
    ;

createLoginPdw
    : CREATE LOGIN loginName = id (
        WITH (PASSWORD EQ password = STRING (MUST_CHANGE)? ( CHECK_POLICY EQ (ON | OFF)?)?)
        | FROM WINDOWS
    )
    ;

alterMasterKeySqlServer
    : ALTER MASTER KEY (
        (FORCE)? REGENERATE WITH ENCRYPTION BY PASSWORD EQ password = STRING
        | (ADD | DROP) ENCRYPTION BY (SERVICE MASTER KEY | PASSWORD EQ encryptionPassword = STRING)
    )
    ;

createMasterKeySqlServer: CREATE MASTER KEY ENCRYPTION BY PASSWORD EQ password = STRING
    ;

alterMasterKeyAzureSql
    : ALTER MASTER KEY (
        (FORCE)? REGENERATE WITH ENCRYPTION BY PASSWORD EQ password = STRING
        | ADD ENCRYPTION BY (SERVICE MASTER KEY | PASSWORD EQ encryptionPassword = STRING)
        | DROP ENCRYPTION BY PASSWORD EQ encryptionPassword = STRING
    )
    ;

createMasterKeyAzureSql: CREATE MASTER KEY ( ENCRYPTION BY PASSWORD EQ password = STRING)?
    ;

alterMessageType
    : ALTER MESSAGE TYPE messageTypeName = id VALIDATION EQ (
        NONE
        | EMPTY
        | WELL_FORMED_XML
        | VALID_XML WITH SCHEMA COLLECTION schemaCollectionName = id
    )
    ;

alterPartitionFunction
    : ALTER PARTITION FUNCTION partitionFunctionName = id LPAREN RPAREN (SPLIT | MERGE) RANGE LPAREN INT RPAREN
    ;

alterPartitionScheme
    : ALTER PARTITION SCHEME partitionSchemeName = id NEXT USED (fileGroupName = id)?
    ;

alterRemoteServiceBinding
    : ALTER REMOTE SERVICE BINDING bindingName = id WITH (USER EQ userName = id)? (
        COMMA ANONYMOUS EQ (ON | OFF)
    )?
    ;

createRemoteServiceBinding
    : CREATE REMOTE SERVICE BINDING bindingName = id (AUTHORIZATION ownerName = id)? TO SERVICE remoteServiceName = STRING WITH (
        USER EQ userName = id
    )? (COMMA ANONYMOUS EQ (ON | OFF))?
    ;

createResourcePool
    : CREATE RESOURCE POOL poolName = id (
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
        | WITH LPAREN CLASSIFIER_FUNCTION EQ (schemaName = id DOT functionName = id | NULL_) RPAREN
        | RESET STATISTICS
        | WITH LPAREN MAX_OUTSTANDING_IO_PER_VOLUME EQ maxOutstandingIoPerVolume = INT RPAREN
    )
    ;

alterDatabaseAuditSpecification
    : ALTER DATABASE AUDIT SPECIFICATION auditSpecificationName = id (
        FOR SERVER AUDIT auditName = id
    )? (auditActionSpecGroup (COMMA auditActionSpecGroup)*)? (
        WITH LPAREN STATE EQ (ON | OFF) RPAREN
    )?
    ;

auditActionSpecGroup
    : (ADD | DROP) LPAREN (auditActionSpecification | auditActionGroupName = id) RPAREN
    ;

auditActionSpecification
    : actionSpecification (COMMA actionSpecification)* ON (auditClassName COLON COLON)? auditSecurable BY principalId (
        COMMA principalId
    )*
    ;

actionSpecification: SELECT | INSERT | UPDATE | DELETE | EXECUTE | RECEIVE | REFERENCES
    ;

auditClassName: OBJECT | SCHEMA | TABLE
    ;

auditSecurable: ((id DOT)? id DOT)? id
    ;

alterDbRole
    : ALTER ROLE roleName = id (
        (ADD | DROP) MEMBER databasePrincipal = id
        | WITH NAME EQ newRoleName = id
    )
    ;

createDatabaseAuditSpecification
    : CREATE DATABASE AUDIT SPECIFICATION auditSpecificationName = id (
        FOR SERVER AUDIT auditName = id
    )? (auditActionSpecGroup (COMMA auditActionSpecGroup)*)? (
        WITH LPAREN STATE EQ (ON | OFF) RPAREN
    )?
    ;

createDbRole: CREATE ROLE roleName = id (AUTHORIZATION ownerName = id)?
    ;

createRoute
    : CREATE ROUTE routeName = id (AUTHORIZATION ownerName = id)? WITH (
        COMMA? SERVICE_NAME EQ routeServiceName = STRING
    )? (COMMA? BROKER_INSTANCE EQ brokerInstanceIdentifier = STRING)? (COMMA? LIFETIME EQ INT)? COMMA? ADDRESS EQ STRING (
        COMMA MIRROR_ADDRESS EQ STRING
    )?
    ;

createRule: CREATE RULE (schemaName = id DOT)? ruleName = id AS searchCondition
    ;

alterSchemaSql
    : ALTER SCHEMA schemaName = id TRANSFER ((OBJECT | TYPE | XML SCHEMA COLLECTION) DOUBLE_COLON)? id (
        DOT id
    )?
    ;

createSchema
    : CREATE SCHEMA (
        schemaName = id
        | AUTHORIZATION ownerName = id
        | schemaName = id AUTHORIZATION ownerName = id
    ) (
        createTable
        | createView
        | (GRANT | DENY) (SELECT | INSERT | DELETE | UPDATE) ON (SCHEMA DOUBLE_COLON)? objectName = id TO ownerName = id
        | REVOKE (SELECT | INSERT | DELETE | UPDATE) ON (SCHEMA DOUBLE_COLON)? objectName = id FROM ownerName = id
    )*
    ;

createSchemaAzureSqlDwAndPdw: CREATE SCHEMA schemaName = id ( AUTHORIZATION ownerName = id)?
    ;

alterSchemaAzureSqlDwAndPdw
    : ALTER SCHEMA schemaName = id TRANSFER (OBJECT DOUBLE_COLON)? id (DOT ID)?
    ;

createSearchPropertyList
    : CREATE SEARCH PROPERTY LIST newListName = id (
        FROM (databaseName = id DOT)? sourceListName = id
    )? (AUTHORIZATION ownerName = id)?
    ;

createSecurityPolicy
    : CREATE SECURITY POLICY (schemaName = id DOT)? securityPolicyName = id (
        COMMA? ADD (FILTER | BLOCK)? PREDICATE tvfSchemaName = id DOT securityPredicateFunctionName = id LPAREN (
            COMMA? columnNameOrArguments = id
        )+ RPAREN ON tableSchemaName = id DOT name = id (
            COMMA? AFTER (INSERT | UPDATE)
            | COMMA? BEFORE (UPDATE | DELETE)
        )*
    )+ (WITH LPAREN STATE EQ (ON | OFF) ( SCHEMABINDING (ON | OFF))? RPAREN)? (NOT FOR REPLICATION)?
    ;

alterSequence
    : ALTER SEQUENCE (schemaName = id DOT)? sequenceName = id (RESTART (WITH INT)?)? (
        INCREMENT BY sequnceIncrement = INT
    )? (MINVALUE INT | NO MINVALUE)? (MAXVALUE INT | NO MAXVALUE)? (CYCLE | NO CYCLE)? (
        CACHE INT
        | NO CACHE
    )?
    ;

createSequence
    : CREATE SEQUENCE (schemaName = id DOT)? sequenceName = id (AS dataType)? (START WITH INT)? (
        INCREMENT BY MINUS? INT
    )? (MINVALUE (MINUS? INT)? | NO MINVALUE)? (MAXVALUE (MINUS? INT)? | NO MAXVALUE)? (
        CYCLE
        | NO CYCLE
    )? (CACHE INT? | NO CACHE)?
    ;

alterServerAudit
    : ALTER SERVER AUDIT auditName = id (
        (
            TO (
                FILE (
                    LPAREN (
                        COMMA? FILEPATH EQ filepath = STRING
                        | COMMA? MAXSIZE EQ ( INT (MB | GB | TB) | UNLIMITED)
                        | COMMA? MAX_ROLLOVER_FILES EQ maxRolloverFiles = ( INT | UNLIMITED)
                        | COMMA? MAX_FILES EQ maxFiles = INT
                        | COMMA? RESERVE_DISK_SPACE EQ (ON | OFF)
                    )* RPAREN
                )
                | APPLICATION_LOG
                | SECURITY_LOG
            )
        )? (
            WITH LPAREN (
                COMMA? QUEUE_DELAY EQ queueDelay = INT
                | COMMA? ON_FAILURE EQ ( CONTINUE | SHUTDOWN | FAIL_OPERATION)
                | COMMA? STATE EQ (ON | OFF)
            )* RPAREN
        )? (
            WHERE (
                COMMA? (NOT?) eventFieldName = id (
                    EQ
                    | (LT GT)
                    | (BANG EQ)
                    | GT
                    | (GT EQ)
                    | LT
                    | LT EQ
                ) (INT | STRING)
                | COMMA? (AND | OR) NOT? (EQ | (LT GT) | (BANG EQ) | GT | (GT EQ) | LT | LT EQ) (
                    INT
                    | STRING
                )
            )
        )?
        | REMOVE WHERE
        | MODIFY NAME EQ newAuditName = id
    )
    ;

createServerAudit
    : CREATE SERVER AUDIT auditName = id (
        (
            TO (
                FILE (
                    LPAREN (
                        COMMA? FILEPATH EQ filepath = STRING
                        | COMMA? MAXSIZE EQ ( INT (MB | GB | TB) | UNLIMITED)
                        | COMMA? MAX_ROLLOVER_FILES EQ maxRolloverFiles = ( INT | UNLIMITED)
                        | COMMA? MAX_FILES EQ maxFiles = INT
                        | COMMA? RESERVE_DISK_SPACE EQ (ON | OFF)
                    )* RPAREN
                )
                | APPLICATION_LOG
                | SECURITY_LOG
            )
        )? (
            WITH LPAREN (
                COMMA? QUEUE_DELAY EQ queueDelay = INT
                | COMMA? ON_FAILURE EQ ( CONTINUE | SHUTDOWN | FAIL_OPERATION)
                | COMMA? STATE EQ (ON | OFF)
                | COMMA? AUDIT_GUID EQ auditGuid = id
            )* RPAREN
        )? (
            WHERE (
                COMMA? (NOT?) eventFieldName = id (
                    EQ
                    | (LT GT)
                    | (BANG EQ)
                    | GT
                    | (GT EQ)
                    | LT
                    | LT EQ
                ) (INT | STRING)
                | COMMA? (AND | OR) NOT? (EQ | (LT GT) | (BANG EQ) | GT | (GT EQ) | LT | LT EQ) (
                    INT
                    | STRING
                )
            )
        )?
        | REMOVE WHERE
        | MODIFY NAME EQ newAuditName = id
    )
    ;

alterServerAuditSpecification
    : ALTER SERVER AUDIT SPECIFICATION auditSpecificationName = id (
        FOR SERVER AUDIT auditName = id
    )? ((ADD | DROP) LPAREN auditActionGroupName = id RPAREN)* (
        WITH LPAREN STATE EQ (ON | OFF) RPAREN
    )?
    ;

createServerAuditSpecification
    : CREATE SERVER AUDIT SPECIFICATION auditSpecificationName = id (
        FOR SERVER AUDIT auditName = id
    )? (ADD LPAREN auditActionGroupName = id RPAREN)* (WITH LPAREN STATE EQ (ON | OFF) RPAREN)?
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

createServerRole: CREATE SERVER ROLE serverRole = id ( AUTHORIZATION serverPrincipal = id)?
    ;

alterServerRolePdw: ALTER SERVER ROLE serverRoleName = id (ADD | DROP) MEMBER login = id
    ;

alterService
    : ALTER SERVICE modifiedServiceName = id (ON QUEUE (schemaName = id DOT)? queueName = id)? (
        LPAREN optArgClause (COMMA optArgClause)* RPAREN
    )?
    ;

optArgClause: (ADD | DROP) CONTRACT modifiedContractName = id
    ;

createService
    : CREATE SERVICE createServiceName = id (AUTHORIZATION ownerName = id)? ON QUEUE (
        schemaName = id DOT
    )? queueName = id (LPAREN (COMMA? (id | DEFAULT))+ RPAREN)?
    ;

alterServiceMasterKey
    : ALTER SERVICE MASTER KEY (
        FORCE? REGENERATE
        | (
            WITH (
                OLD_ACCOUNT EQ acoldAccountName = STRING COMMA OLD_PASSWORD EQ oldPassword = STRING
                | NEW_ACCOUNT EQ newAccountName = STRING COMMA NEW_PASSWORD EQ newPassword = STRING
            )?
        )
    )
    ;

alterSymmetricKey
    : ALTER SYMMETRIC KEY keyName = id (
        (ADD | DROP) ENCRYPTION BY (
            CERTIFICATE certificateName = id
            | PASSWORD EQ password = STRING
            | SYMMETRIC KEY symmetricKeyName = id
            | ASYMMETRIC KEY AsymKeyName = id
        )
    )
    ;

createSynonym
    : CREATE SYNONYM (schemaName_1 = id DOT)? synonymName = id FOR (
        (serverName = id DOT)? (databaseName = id DOT)? (schemaName_2 = id DOT)? objectName = id
        | (databaseOrSchema2 = id DOT)? ( schemaId2_orObjectName = id DOT)?
    )
    ;

alterUser
    : ALTER USER username = id WITH (
        COMMA? NAME EQ newusername = id
        | COMMA? DEFAULT_SCHEMA EQ ( schemaName = id | NULL_)
        | COMMA? LOGIN EQ loginame = id
        | COMMA? PASSWORD EQ STRING (OLD_PASSWORD EQ STRING)+
        | COMMA? DEFAULT_LANGUAGE EQ ( NONE | lcid = INT | languageNameOrAlias = id)
        | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ ( ON | OFF)
    )+
    ;

createUser
    : CREATE USER userName = id ((FOR | FROM) LOGIN loginName = id)? (
        WITH (
            COMMA? DEFAULT_SCHEMA EQ schemaName = id
            | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ ( ON | OFF)
        )*
    )?
    | CREATE USER (
        windowsPrincipal = id (
            WITH (
                COMMA? DEFAULT_SCHEMA EQ schemaName = id
                | COMMA? DEFAULT_LANGUAGE EQ ( NONE | INT | languageNameOrAlias = id)
                | COMMA? SID EQ HEX
                | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ ( ON | OFF)
            )*
        )?
        | userName = id WITH PASSWORD EQ password = STRING (
            COMMA? DEFAULT_SCHEMA EQ schemaName = id
            | COMMA? DEFAULT_LANGUAGE EQ ( NONE | INT | languageNameOrAlias = id)
            | COMMA? SID EQ HEX
            | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ ( ON | OFF)
        )*
        | Azure_Active_DirectoryPrincipal = id FROM EXTERNAL PROVIDER
    )
    | CREATE USER userName = id (
        WITHOUT LOGIN (
            COMMA? DEFAULT_SCHEMA EQ schemaName = id
            | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ ( ON | OFF)
        )*
        | (FOR | FROM) CERTIFICATE certName = id
        | (FOR | FROM) ASYMMETRIC KEY asymKeyName = id
    )
    | CREATE USER userName = id
    ;

createUserAzureSqlDw
    : CREATE USER userName = id ((FOR | FROM) LOGIN loginName = id | WITHOUT LOGIN)? (
        WITH DEFAULT_SCHEMA EQ schemaName = id
    )?
    | CREATE USER Azure_Active_DirectoryPrincipal = id FROM EXTERNAL PROVIDER (
        WITH DEFAULT_SCHEMA EQ schemaName = id
    )?
    ;

alterUserAzureSql
    : ALTER USER username = id WITH (
        COMMA? NAME EQ newusername = id
        | COMMA? DEFAULT_SCHEMA EQ schemaName = id
        | COMMA? LOGIN EQ loginame = id
        | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ ( ON | OFF)
    )+
    ;

alterWorkloadGroup
    : ALTER WORKLOAD GROUP (workloadGroupGroupName = id | DEFAULT_DOUBLE_QUOTE) (
        WITH LPAREN (
            IMPORTANCE EQ (LOW | MEDIUM | HIGH)
            | COMMA? REQUEST_MAX_MEMORY_GRANT_PERCENT EQ requestMaxMemoryGrant = INT
            | COMMA? REQUEST_MAX_CPU_TIME_SEC EQ requestMaxCpuTimeSec = INT
            | REQUEST_MEMORY_GRANT_TIMEOUT_SEC EQ requestMemoryGrantTimeoutSec = INT
            | MAX_DOP EQ maxDop = INT
            | GROUP_MAX_REQUESTS EQ groupMaxRequests = INT
        )+ RPAREN
    )? (USING (workloadGroupPoolName = id | DEFAULT_DOUBLE_QUOTE))?
    ;

createWorkloadGroup
    : CREATE WORKLOAD GROUP workloadGroupGroupName = id (
        WITH LPAREN (
            IMPORTANCE EQ (LOW | MEDIUM | HIGH)
            | COMMA? REQUEST_MAX_MEMORY_GRANT_PERCENT EQ requestMaxMemoryGrant = INT
            | COMMA? REQUEST_MAX_CPU_TIME_SEC EQ requestMaxCpuTimeSec = INT
            | REQUEST_MEMORY_GRANT_TIMEOUT_SEC EQ requestMemoryGrantTimeoutSec = INT
            | MAX_DOP EQ maxDop = INT
            | GROUP_MAX_REQUESTS EQ groupMaxRequests = INT
        )+ RPAREN
    )? (
        USING (workloadGroupPoolName = id | DEFAULT_DOUBLE_QUOTE)? (
            COMMA? EXTERNAL externalPoolName = id
            | DEFAULT_DOUBLE_QUOTE
        )?
    )?
    ;

createPartitionFunction
    : CREATE PARTITION FUNCTION partitionFunctionName = id LPAREN inputParameterType = dataType RPAREN AS RANGE (
        LEFT
        | RIGHT
    )? FOR VALUES LPAREN boundaryValues = expressionList RPAREN
    ;

createPartitionScheme
    : CREATE PARTITION SCHEME partitionSchemeName = id AS PARTITION partitionFunctionName = id ALL? TO LPAREN fileGroupNames += id (
        COMMA fileGroupNames += id
    )* RPAREN
    ;

createQueue
    : CREATE QUEUE (tableName | queueName = id) queueSettings? (ON filegroup = id | DEFAULT)?
    ;

queueSettings
    : WITH (STATUS EQ onOff COMMA?)? (RETENTION EQ onOff COMMA?)? (
        ACTIVATION LPAREN (
            (
                (STATUS EQ onOff COMMA?)? (PROCEDURE_NAME EQ funcProcNameDatabaseSchema COMMA?)? (
                    MAX_QUEUE_READERS EQ maxReaders = INT COMMA?
                )? (EXECUTE AS (SELF | userName = STRING | OWNER) COMMA?)?
            )
            | DROP
        ) RPAREN COMMA?
    )? (POISON_MESSAGE_HANDLING LPAREN (STATUS EQ onOff) RPAREN)?
    ;

alterQueue: ALTER QUEUE (tableName | queueName = id) ( queueSettings | queueAction)
    ;

queueAction
    : REBUILD (WITH LPAREN queueRebuildOptions RPAREN)?
    | REORGANIZE (WITH LOB_COMPACTION EQ onOff)?
    | MOVE TO (id | DEFAULT)
    ;

queueRebuildOptions: genericOption
    ;

createContract
    : CREATE CONTRACT contractName (AUTHORIZATION ownerName = id)? LPAREN (
        (messageTypeName = id | DEFAULT) SENT BY (INITIATOR | TARGET | ANY) COMMA?
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
    : CREATE MESSAGE TYPE messageTypeName = id (AUTHORIZATION ownerName = id)? (
        VALIDATION EQ (
            NONE
            | EMPTY
            | WELL_FORMED_XML
            | VALID_XML WITH SCHEMA COLLECTION schemaCollectionName = id
        )
    )
    ;

mergeStatement: withExpression? merge
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

deleteStatement: withExpression? delete
    ;

delete
    : DELETE topClause? FROM? ddlObject withTableHints? outputClause? (FROM tableSources)? updateWhereClause? optionClause? SEMI?
    ;

insertStatement: withExpression? insert
    ;

insert
    : INSERT topClause? INTO? ddlObject withTableHints? (LPAREN expressionList RPAREN)? outputClause? insertStatementValue optionClause? SEMI?
    ;

insertStatementValue: derivedTable | executeStatement | DEFAULT VALUES
    ;

receiveStatement
    : LPAREN? RECEIVE (ALL | DISTINCT | topClause | STAR) (LOCAL_ID EQ expression COMMA?)* FROM tableName (
        INTO tableVariable = id (WHERE where = searchCondition)
    )? RPAREN?
    ;

selectStatementStandalone: withExpression? selectStatement
    ;

selectStatement: queryExpression forClause? optionClause? SEMI?
    ;

updateStatement: withExpression? update
    ;

update
    : UPDATE topClause? ddlObject withTableHints? SET updateElem (COMMA updateElem)* outputClause? (
        FROM tableSources
    )? updateWhereClause? optionClause? SEMI?
    ;

updateWhereClause
    : WHERE (searchCondition | CURRENT OF ( GLOBAL? cursorName | cursorVar = LOCAL_ID))
    ;

outputClause
    : OUTPUT outputDmlListElem (COMMA outputDmlListElem)* (
        INTO ddlObject ( LPAREN columnNameList RPAREN)?
    )?
    ;

outputDmlListElem: (expression | asterisk) asColumnAlias?
    ;

createDatabase
    : CREATE DATABASE (database = id) (CONTAINMENT EQ ( NONE | PARTIAL))? (
        ON PRIMARY? databaseFileSpec ( COMMA databaseFileSpec)*
    )? (id /* LOG */ ON databaseFileSpec (COMMA databaseFileSpec)*)? (COLLATE collationName = id)? (
        WITH createDatabaseOption (COMMA createDatabaseOption)*
    )?
    ;

createIndex
    : CREATE UNIQUE? clustered? INDEX id ON tableName LPAREN columnNameListWithOrder RPAREN (
        INCLUDE LPAREN columnNameList RPAREN
    )? (WHERE where = searchCondition)? (createIndexOptions)? (ON id)? SEMI?
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

onPartitions
    : ON PARTITIONS LPAREN partitionNumber = INT (TO toPartitionNumber = INT)? (
        COMMA partitionNumber = INT (TO toPartitionNumber = INT)?
    )* RPAREN
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

createOrAlterProcedure
    : ((CREATE (OR (ALTER | REPLACE))?) | ALTER) proc = (PROC | PROCEDURE) procName = funcProcNameSchema (
        SEMI INT
    )? (LPAREN? procedureParam (COMMA procedureParam)* RPAREN?)? (
        WITH procedureOption (COMMA procedureOption)*
    )? (FOR REPLICATION)? AS (asExternalName | sqlClauses*)
    ;

asExternalName: EXTERNAL NAME assemblyName = id DOT className = id DOT methodName = id
    ;

createOrAlterTrigger: createOrAlterDmlTrigger | createOrAlterDdlTrigger
    ;

createOrAlterDmlTrigger
    : (CREATE (OR (ALTER | REPLACE))? | ALTER) TRIGGER simpleName ON tableName (
        WITH dmlTriggerOption (COMMA dmlTriggerOption)*
    )? (FOR | AFTER | INSTEAD OF) dmlTriggerOperation (COMMA dmlTriggerOperation)* (WITH APPEND)? (
        NOT FOR REPLICATION
    )? AS sqlClauses+
    ;

dmlTriggerOption: ENCRYPTION | executeClause
    ;

dmlTriggerOperation: (INSERT | UPDATE | DELETE)
    ;

createOrAlterDdlTrigger
    : (CREATE (OR (ALTER | REPLACE))? | ALTER) TRIGGER simpleName ON (ALL SERVER | DATABASE) (
        WITH dmlTriggerOption (COMMA dmlTriggerOption)*
    )? (FOR | AFTER) ddlTriggerOperation (COMMA ddlTriggerOperation)* AS sqlClauses+
    ;

ddlTriggerOperation: simpleId
    ;

createOrAlterFunction
    : ((CREATE (OR ALTER)?) | ALTER) FUNCTION funcName = funcProcNameSchema (
        (LPAREN procedureParam (COMMA procedureParam)* RPAREN)
        | LPAREN RPAREN
    ) //must have (), but can be empty
    (funcBodyReturnsSelect | funcBodyReturnsTable | funcBodyReturnsScalar) SEMI?
    ;

funcBodyReturnsSelect
    : RETURNS TABLE (WITH functionOption (COMMA functionOption)*)? AS? (
        asExternalName
        | RETURN (LPAREN selectStatementStandalone RPAREN | selectStatementStandalone)
    )
    ;

funcBodyReturnsTable
    : RETURNS LOCAL_ID tableTypeDefinition (WITH functionOption (COMMA functionOption)*)? AS? (
        asExternalName
        | BEGIN sqlClauses* RETURN SEMI? END SEMI?
    )
    ;

funcBodyReturnsScalar
    : RETURNS dataType (WITH functionOption (COMMA functionOption)*)? AS? (
        asExternalName
        | BEGIN sqlClauses* RETURN ret = expression SEMI? END
    )
    ;

procedureParamDefaultValue: NULL_ | DEFAULT | constant | LOCAL_ID
    ;

procedureParam
    : LOCAL_ID AS? (typeSchema = id DOT)? dataType VARYING? (
        EQ defaultVal = procedureParamDefaultValue
    )? (OUT | OUTPUT | READONLY)?
    ;

procedureOption: executeClause | genericOption
    ;

functionOption
    : ENCRYPTION
    | SCHEMABINDING
    | RETURNS NULL_ ON NULL_ INPUT
    | CALLED ON NULL_ INPUT
    | executeClause
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

createTableDefault
    : CREATE TABLE tableName LPAREN columnDefTableConstraints (COMMA? tableIndices)* COMMA? RPAREN (
        LOCK simpleId
    )? tableOptions* (ON id | DEFAULT | onPartitionOrFilegroup)? (TEXTIMAGE_ON id | DEFAULT)? SEMI?
    ;

createTableAs
    : CREATE TABLE tableName (LPAREN columnNameList RPAREN)? tableOptions? AS selectStatementStandalone SEMI?
    ;

createTable: createTableDefault | createTableAs
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
    : (simpleId | keyword) EQ (simpleId | keyword | onOff | INT)
    | CLUSTERED COLUMNSTORE INDEX
    | HEAP
    | FILLFACTOR EQ INT
    | DISTRIBUTION EQ distributionType
    | CLUSTERED INDEX LPAREN id (ASC | DESC)? ( COMMA id (ASC | DESC)?)* RPAREN
    | DATA_COMPRESSION EQ (NONE | ROW | PAGE) onPartitions?
    | XML_COMPRESSION EQ onOff onPartitions?
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
    : (CREATE (OR (ALTER | REPLACE))? | ALTER) VIEW simpleName (LPAREN columnNameList RPAREN)? (
        WITH viewAttribute (COMMA viewAttribute)*
    )? AS selectStatementStandalone (WITH CHECK OPTION)? SEMI?
    ;

viewAttribute: ENCRYPTION | SCHEMABINDING | VIEW_METADATA
    ;

alterTable
    : ALTER TABLE tableName (
        SET LPAREN LOCK_ESCALATION EQ (AUTO | TABLE | DISABLE) RPAREN
        | ADD columnDefTableConstraints
        | ALTER COLUMN (columnDefinition | columnModifier)
        | DROP COLUMN id (COMMA id)*
        | DROP CONSTRAINT constraint = id
        | WITH (CHECK | NOCHECK) ADD (CONSTRAINT constraint = id)? (
            FOREIGN KEY LPAREN fk = columnNameList RPAREN REFERENCES tableName (
                LPAREN pk = columnNameList RPAREN
            )? (onDelete | onUpdate)*
            | CHECK LPAREN searchCondition RPAREN
        )
        | (NOCHECK | CHECK) CONSTRAINT constraint = id
        | (ENABLE | DISABLE) TRIGGER id?
        | REBUILD tableOptions
        | SWITCH switchPartition
    ) SEMI?
    ;

switchPartition
    : (PARTITION? sourcePartitionNumberExpression = expression)? TO targetTable = tableName (
        PARTITION targetPartitionNumberExpression = expression
    )? (WITH lowPriorityLockWait)?
    ;

lowPriorityLockWait
    : WAIT_AT_LOW_PRIORITY LPAREN MAX_DURATION EQ expression MINUTES? COMMA ABORT_AFTER_WAIT EQ abortAfterWait = (
        NONE
        | SELF
        | BLOCKERS
    ) RPAREN
    ;

alterDatabase
    : ALTER DATABASE (database = id | CURRENT) (
        MODIFY NAME EQ newName = id
        | COLLATE collation = id
        | SET databaseOptionspec (WITH termination)?
        | addOrModifyFiles
        | addOrModifyFilegroups
    ) SEMI?
    ;

addOrModifyFiles
    : ADD id? /* LOG */ FILE fileSpec (COMMA fileSpec)* (TO FILEGROUP filegroupName = id)?
    | REMOVE FILE (id | fileSpec)
    ;

fileSpec
    : LPAREN NAME EQ name = idOrString (COMMA NEWNAME EQ newName = idOrString)? (
        COMMA FILENAME EQ fileName = STRING
    )? (COMMA SIZE EQ size = fileSize)? (COMMA MAXSIZE EQ (maxSize = fileSize) | UNLIMITED)? (
        COMMA FILEGROWTH EQ growthIncrement = fileSize
    )? (COMMA OFFLINE)? RPAREN
    ;

addOrModifyFilegroups
    : ADD FILEGROUP filegroupName = id (CONTAINS FILESTREAM | CONTAINS MEMORY_OPTIMIZED_DATA)?
    | REMOVE FILEGROUP filegrouName = id
    | MODIFY FILEGROUP filegrouName = id (
        filegroupUpdatabilityOption
        | DEFAULT
        | NAME EQ newFilegroupName = id
        | AUTOGROW_SINGLE_FILE
        | AUTOGROW_ALL_FILES
    )
    ;

filegroupUpdatabilityOption: READONLY | READWRITE | READ_ONLY | READ_WRITE
    ;

databaseOptionspec
    : autoOption
    | changeTrackingOption
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
    | genericOption
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
    : CHANGE_TRACKING EQ (
        OFF
        | ON LPAREN (changeTrackingOptionList ( COMMA changeTrackingOptionList)*)* RPAREN
    )
    ;

changeTrackingOptionList
    : AUTO_CLEANUP EQ onOff
    | CHANGE_RETENTION EQ INT ( DAYS | HOURS | MINUTES)
    ;

containmentOption: CONTAINMENT EQ (NONE | PARTIAL)
    ;

cursorOption: CURSOR_CLOSE_ON_COMMIT onOff | CURSOR_DEFAULT ( LOCAL | GLOBAL)
    ;

alterEndpoint
    : ALTER ENDPOINT endpointname = id (AUTHORIZATION login = id)? (
        STATE EQ state = (STARTED | STOPPED | DISABLED)
    )? AS TCP LPAREN endpointListenerClause RPAREN (
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

portNumber: port = INT
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

hadrOptions: HADR ( (AVAILABILITY GROUP EQ availabilityGroupName = id | OFF) | (SUSPEND | RESUME))
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

termination: ROLLBACK AFTER seconds = INT | ROLLBACK IMMEDIATE | NO_WAIT
    ;

dropIndex
    : DROP INDEX (IF EXISTS)? (
        dropRelationalOrXmlOrSpatialIndex (COMMA dropRelationalOrXmlOrSpatialIndex)*
        | dropBackwardCompatibleIndex ( COMMA dropBackwardCompatibleIndex)*
    ) SEMI?
    ;

dropRelationalOrXmlOrSpatialIndex: indexName = id ON tableName
    ;

dropBackwardCompatibleIndex: (ownerName = id DOT)? tableOrViewName = id DOT indexName = id
    ;

dropProcedure
    : DROP proc = (PROC | PROCEDURE) (IF EXISTS)? funcProcNameSchema (COMMA funcProcNameSchema)* SEMI?
    ;

dropTrigger: dropDmlTrigger | dropDdlTrigger
    ;

dropDmlTrigger: DROP TRIGGER (IF EXISTS)? simpleName (COMMA simpleName)* SEMI?
    ;

dropDdlTrigger
    : DROP TRIGGER (IF EXISTS)? simpleName (COMMA simpleName)* ON (DATABASE | ALL SERVER) SEMI?
    ;

dropFunction: DROP FUNCTION (IF EXISTS)? funcProcNameSchema ( COMMA funcProcNameSchema)* SEMI?
    ;

dropStatistics: DROP STATISTICS (COMMA? (tableName DOT)? name = id)+ SEMI
    ;

dropTable: DROP TABLE (IF EXISTS)? tableName (COMMA tableName)* SEMI?
    ;

dropView: DROP VIEW (IF EXISTS)? simpleName (COMMA simpleName)* SEMI?
    ;

createType
    : CREATE TYPE name = simpleName (FROM dataType nullNotnull?)? (
        AS TABLE LPAREN columnDefTableConstraints RPAREN
    )?
    ;

dropType: DROP TYPE (IF EXISTS)? name = simpleName
    ;

rowsetFunctionLimited: openquery | opendatasource
    ;

openquery: OPENQUERY LPAREN linkedServer = id COMMA query = STRING RPAREN
    ;

opendatasource
    : OPENDATASOURCE LPAREN provider = STRING COMMA init = STRING RPAREN DOT (database = id)? DOT (
        scheme = id
    )? DOT (table = id)
    ;

declareStatement
    : DECLARE LOCAL_ID AS? (dataType | tableTypeDefinition | tableName)
    | DECLARE loc += declareLocal (COMMA loc += declareLocal)*
    | DECLARE LOCAL_ID AS? xmlTypeDefinition
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
    : BACKUP DATABASE id (READ_WRITE_FILEGROUPS optionList)? (TO optionList)+ (
        MIRROR TO optionList
    )* WITH (
        optionList
        | ENCRYPTION LPAREN ALGORITHM EQ genericOption COMMA SERVER CERTIFICATE EQ genericOption RPAREN
    )?
    ;

backupLog: BACKUP id /* LOG */ id TO optionList (MIRROR TO optionList)? ( WITH optionList)?
    ;

backupCertificate
    : BACKUP CERTIFICATE certname = id TO FILE EQ certFile = STRING (
        WITH PRIVATE KEY LPAREN (
            COMMA? FILE EQ privateKeyFile = STRING
            | COMMA? ENCRYPTION BY PASSWORD EQ encryptionPassword = STRING
            | COMMA? DECRYPTION BY PASSWORD EQ decryptionPasword = STRING
        )+ RPAREN
    )?
    ;

backupMasterKey
    : BACKUP MASTER KEY TO FILE EQ masterKeyBackupFile = STRING ENCRYPTION BY PASSWORD EQ encryptionPassword = STRING
    ;

backupServiceMasterKey
    : BACKUP SERVICE MASTER KEY TO FILE EQ serviceMasterKeyBackupFile = STRING ENCRYPTION BY PASSWORD EQ encryptionPassword = STRING
    ;

killStatement: KILL (killProcess | killQueryNotification | killStatsJob)
    ;

killProcess: (sessionId = (INT | STRING) | UOW) (WITH STATUSONLY)?
    ;

killQueryNotification: QUERY NOTIFICATION SUBSCRIPTION ( ALL | subscriptionId = INT)
    ;

killStatsJob: STATS JOB jobId = INT
    ;

executeStatement: EXECUTE executeBody SEMI?
    ;

executeBodyBatch
    : funcProcNameServerDatabaseSchema (executeStatementArg (COMMA executeStatementArg)*)? SEMI?
    ;

executeBody
    : (returnStatus = LOCAL_ID EQ)? (funcProcNameServerDatabaseSchema | executeVarString) executeStatementArg?
    | LPAREN executeVarString (COMMA executeVarString)* RPAREN (AS (LOGIN | USER) EQ STRING)? (
        AT_KEYWORD linkedServer = id
    )?
    | AS ( (LOGIN | USER) EQ STRING | CALLER)
    ;

executeStatementArg
    : executeStatementArgUnnamed (COMMA executeStatementArg)*
    | executeStatementArgNamed (COMMA executeStatementArgNamed)*
    ;

executeStatementArgNamed: name = LOCAL_ID EQ value = executeParameter
    ;

executeStatementArgUnnamed: value = executeParameter
    ;

executeParameter: ( constant | LOCAL_ID (OUTPUT | OUT)? | id | DEFAULT | NULL_)
    ;

executeVarString
    : LOCAL_ID (OUTPUT | OUT)? (PLUS LOCAL_ID (PLUS executeVarString)?)?
    | STRING (PLUS LOCAL_ID (PLUS executeVarString)?)?
    ;

securityStatement
    : executeClause SEMI?
    | GRANT (ALL PRIVILEGES? | grantPermission (LPAREN columnNameList RPAREN)?) (
        ON (classTypeForGrant COLON COLON)? onId = tableName
    )? TO toPrincipal += principalId (COMMA toPrincipal += principalId)* (WITH GRANT OPTION)? (
        AS asPrincipal = principalId
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
    : CREATE CERTIFICATE certificateName = id (AUTHORIZATION userName = id)? (
        FROM existingKeys
        | generateNewKeys
    ) (ACTIVE FOR BEGIN DIALOG EQ onOff)?
    ;

existingKeys
    : ASSEMBLY assemblyName = id
    | EXECUTABLE? FILE EQ pathToFile = STRING (WITH PRIVATE KEY LPAREN privateKeyOptions RPAREN)?
    ;

privateKeyOptions
    : (FILE | HEX) EQ path = STRING (
        COMMA (DECRYPTION | ENCRYPTION) BY PASSWORD EQ password = STRING
    )?
    ;

generateNewKeys
    : (ENCRYPTION BY PASSWORD EQ password = STRING)? WITH SUBJECT EQ certificateSubjectName = STRING (
        COMMA dateOptions
    )*
    ;

dateOptions: (START_DATE | EXPIRY_DATE) EQ STRING
    ;

openKey
    : OPEN SYMMETRIC KEY keyName = id DECRYPTION BY decryptionMechanism
    | OPEN MASTER KEY DECRYPTION BY PASSWORD EQ password = STRING
    ;

closeKey: CLOSE SYMMETRIC KEY keyName = id | CLOSE ALL SYMMETRIC KEYS | CLOSE MASTER KEY
    ;

createKey
    : CREATE MASTER KEY ENCRYPTION BY PASSWORD EQ password = STRING
    | CREATE SYMMETRIC KEY keyName = id (AUTHORIZATION userName = id)? (
        FROM PROVIDER providerName = id
    )? WITH ((keyOptions | ENCRYPTION BY encryptionMechanism) COMMA?)+
    ;

keyOptions
    : KEY_SOURCE EQ passPhrase = STRING
    | ALGORITHM EQ algorithm
    | IDENTITY_VALUE EQ identityPhrase = STRING
    | PROVIDER_KEY_NAME EQ keyNameInProvider = STRING
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

encryptionMechanism
    : CERTIFICATE certificateName = id
    | ASYMMETRIC KEY asymKeyName = id
    | SYMMETRIC KEY decrypting_KeyName = id
    | PASSWORD EQ STRING
    ;

decryptionMechanism
    : CERTIFICATE certificateName = id (WITH PASSWORD EQ STRING)?
    | ASYMMETRIC KEY asymKeyName = id (WITH PASSWORD EQ STRING)?
    | SYMMETRIC KEY decrypting_KeyName = id
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

goStatement: GO INT?
    ;

useStatement: USE database = id
    ;

setuserStatement: SETUSER user = STRING?
    ;

reconfigureStatement: RECONFIGURE (WITH OVERRIDE)?
    ;

shutdownStatement: SHUTDOWN (WITH genericOption)?
    ;

checkpointStatement: CHECKPOINT (checkPointDuration = INT)?
    ;

dbccCheckallocOption: ALL_ERRORMSGS | NO_INFOMSGS | TABLOCK | ESTIMATEONLY
    ;

dbccCheckalloc
    : name = CHECKALLOC (
        LPAREN (database = id | databaseid = STRING | INT) (
            COMMA NOINDEX
            | COMMA ( REPAIR_ALLOW_DATA_LOSS | REPAIR_FAST | REPAIR_REBUILD)
        )? RPAREN (
            WITH dbccOption = dbccCheckallocOption (COMMA dbccOption = dbccCheckallocOption)*
        )?
    )?
    ;

dbccCheckcatalog
    : name = CHECKCATALOG (LPAREN (database = id | databasename = STRING | INT) RPAREN)? (
        WITH dbccOption = NO_INFOMSGS
    )?
    ;

dbccCheckconstraintsOption: ALL_CONSTRAINTS | ALL_ERRORMSGS | NO_INFOMSGS
    ;

dbccCheckconstraints
    : name = CHECKCONSTRAINTS (
        LPAREN (tableOrConstraint = id | tableOrConstraintName = STRING) RPAREN
    )? (
        WITH dbccOption = dbccCheckconstraintsOption (
            COMMA dbccOption = dbccCheckconstraintsOption
        )*
    )?
    ;

dbccCheckdbTableOption: genericOption
    ;

dbccCheckdb
    : name = CHECKDB (
        LPAREN (database = id | databasename = STRING | INT) (
            COMMA (NOINDEX | REPAIR_ALLOW_DATA_LOSS | REPAIR_FAST | REPAIR_REBUILD)
        )? RPAREN
    )? (WITH dbccOption = dbccCheckdbTableOption ( COMMA dbccOption = dbccCheckdbTableOption)*)?
    ;

dbccCheckfilegroupOption: genericOption
    ;

dbccCheckfilegroup
    : name = CHECKFILEGROUP (
        LPAREN (filegroupId = INT | filegroupName = STRING) (
            COMMA (NOINDEX | REPAIR_ALLOW_DATA_LOSS | REPAIR_FAST | REPAIR_REBUILD)
        )? RPAREN
    )? (WITH dbccOption = dbccCheckfilegroupOption ( COMMA dbccOption = dbccCheckfilegroupOption)*)?
    ;

dbccChecktable
    : name = CHECKTABLE LPAREN tableOrViewName = STRING (
        COMMA (
            NOINDEX
            | indexId = expression
            | REPAIR_ALLOW_DATA_LOSS
            | REPAIR_FAST
            | REPAIR_REBUILD
        )
    )? RPAREN (
        WITH dbccOption = dbccCheckdbTableOption (COMMA dbccOption = dbccCheckdbTableOption)*
    )?
    ;

dbccCleantable
    : name = CLEANTABLE LPAREN (database = id | databasename = STRING | INT) COMMA (
        tableOrView = id
        | tableOrViewName = STRING
    ) (COMMA batchSize = INT)? RPAREN (WITH dbccOption = NO_INFOMSGS)?
    ;

dbccClonedatabaseOption
    : NO_STATISTICS
    | NO_QUERYSTORE
    | SERVICEBROKER
    | VERIFY_CLONEDB
    | BACKUP_CLONEDB
    ;

dbccClonedatabase
    : name = CLONEDATABASE LPAREN sourceDatabase = id COMMA targetDatabase = id RPAREN (
        WITH dbccOption = dbccClonedatabaseOption (COMMA dbccOption = dbccClonedatabaseOption)*
    )?
    ;

dbccPdwShowspaceused
    : name = PDW_SHOWSPACEUSED (LPAREN tablename = id RPAREN)? (
        WITH dbccOption = IGNORE_REPLICATED_TABLE_CACHE
    )?
    ;

dbccProccache: name = PROCCACHE (WITH dbccOption = NO_INFOMSGS)?
    ;

dbccShowcontigOption: genericOption
    ;

dbccShowcontig
    : name = SHOWCONTIG (LPAREN tableOrView = expression ( COMMA index = expression)? RPAREN)? (
        WITH dbccOption = dbccShowcontigOption (COMMA dbccShowcontigOption)*
    )?
    ;

dbccShrinklog
    : name = SHRINKLOG (LPAREN SIZE EQ ((INT ( MB | GB | TB)) | DEFAULT) RPAREN)? (
        WITH dbccOption = NO_INFOMSGS
    )?
    ;

dbccDbreindex
    : name = DBREINDEX LPAREN table = idOrString (
        COMMA indexName = idOrString ( COMMA fillfactor = expression)?
    )? RPAREN (WITH dbccOption = NO_INFOMSGS)?
    ;

dbccDllFree: dllname = id LPAREN name = FREE RPAREN ( WITH dbccOption = NO_INFOMSGS)?
    ;

dbccDropcleanbuffers
    : name = DROPCLEANBUFFERS (LPAREN COMPUTE | ALL RPAREN)? (WITH dbccOption = NO_INFOMSGS)?
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

executeClause: EXECUTE AS clause = (CALLER | SELF | OWNER | STRING)
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

columnDefTableConstraint: columnDefinition | materializedColumnDefinition | tableConstraint
    ;

columnDefinition: id (dataType | AS expression PERSISTED?) columnDefinitionElement* columnIndex?
    ;

columnDefinitionElement
    : FILESTREAM
    | COLLATE collationName = id
    | SPARSE
    | MASKED WITH LPAREN FUNCTION EQ maskFunction = STRING RPAREN
    | (CONSTRAINT constraint = id)? DEFAULT constantExpr = expression
    | IDENTITY (LPAREN seed = INT COMMA increment = INT RPAREN)?
    | NOT FOR REPLICATION
    | GENERATED ALWAYS AS (ROW | TRANSACTION_ID | SEQUENCE_NUMBER) (START | END) HIDDEN_KEYWORD?
    | ROWGUIDCOL
    | ENCRYPTED WITH LPAREN COLUMN_ENCRYPTION_KEY EQ keyName = STRING COMMA ENCRYPTION_TYPE EQ (
        DETERMINISTIC
        | RANDOMIZED
    ) COMMA ALGORITHM EQ algo = STRING RPAREN
    | columnConstraint
    ;

columnModifier
    : id (ADD | DROP) (
        ROWGUIDCOL
        | PERSISTED
        | NOT FOR REPLICATION
        | SPARSE
        | HIDDEN_KEYWORD
        | MASKED ( WITH ( FUNCTION EQ STRING | LPAREN FUNCTION EQ STRING RPAREN))?
    )
    ;

materializedColumnDefinition: id (COMPUTE | AS) expression ( MATERIALIZED | NOT MATERIALIZED)?
    ;

columnConstraint
    : (CONSTRAINT constraint = id)? (
        nullNotnull
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

onPartitionOrFilegroup
    : ON (
        ( partitionSchemeName = id LPAREN partitionColumnName = id RPAREN)
        | filegroup = id
        | DEFAULT_DOUBLE_QUOTE
    )
    ;

tableConstraint
    : (CONSTRAINT constraint = id)? (
        ((PRIMARY KEY | UNIQUE) clustered? LPAREN columnNameListWithOrder RPAREN primaryKeyOptions)
        | ( FOREIGN KEY LPAREN fk = columnNameList RPAREN foreignKeyOptions)
        | ( CONNECTION LPAREN connectionNode ( COMMA connectionNode)* RPAREN)
        | ( DEFAULT constantExpr = expression FOR column = id ( WITH VALUES)?)
        | checkConstraint
    )
    ;

connectionNode: fromNodeTable = id TO toNodeTable = id
    ;

primaryKeyOptions: (WITH FILLFACTOR EQ INT)? alterTableIndexOptions? onPartitionOrFilegroup?
    ;

foreignKeyOptions
    : REFERENCES tableName LPAREN pk = columnNameList RPAREN (onDelete | onUpdate)* (
        NOT FOR REPLICATION
    )?
    ;

checkConstraint: CHECK (NOT FOR REPLICATION)? LPAREN searchCondition RPAREN
    ;

onDelete: ON DELETE (NO ACTION | CASCADE | SET NULL_ | SET DEFAULT)
    ;

onUpdate: ON UPDATE (NO ACTION | CASCADE | SET NULL_ | SET DEFAULT)
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
    | <assoc = right> op = BIT_NOT expression                 # exprBitNot
    | <assoc = right> op = (PLUS | MINUS) expression          # exprUnary
    | expression op = (STAR | DIV | MOD) expression           # exprOpPrec1
    | expression op = (PLUS | MINUS) expression               # exprOpPrec2
    | expression op = (BIT_AND | BIT_XOR | BIT_OR) expression # exprOpPrec3
    | expression op = DOUBLE_BAR expression                   # exprOpPrec4
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
    | LPAREN subquery RPAREN                                  # exprSubquery
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

primitiveExpression: op = (DEFAULT | NULL_ | LOCAL_ID) | constant
    ;

caseExpression: CASE caseExpr = expression? switchSection+ ( ELSE elseExpr = expression)? END
    ;

subquery: selectStatement
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
    : EXISTS LPAREN subquery RPAREN
    | freetextPredicate
    | expression comparisonOperator expression
    | expression ME expression
    | expression comparisonOperator (ALL | SOME | ANY) LPAREN subquery RPAREN
    | expression NOT* BETWEEN expression AND expression
    | expression NOT* IN LPAREN (subquery | expressionList) RPAREN
    | expression NOT* LIKE expression (ESCAPE expression)?
    | expression IS nullNotnull
    | expression
    ;

queryExpression
    : querySpecification unions += sqlUnion*
    | LPAREN queryExpression RPAREN (UNION ALL? queryExpression)?
    ;

sqlUnion
    : (UNION ALL? | EXCEPT | INTERSECT) (querySpecification | (LPAREN queryExpression RPAREN))
    ;

querySpecification
    : SELECT (ALL | DISTINCT)? topClause? selectListElem (COMMA selectListElem)* selectOptionalClauses
    ;

selectOptionalClauses
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

udtMethodArguments
    : LPAREN argument += executeVarString (COMMA argument += executeVarString)* RPAREN
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
    : tableName                  # tsiNamedTable
    | rowsetFunction             # tsiRowsetFunction
    | LPAREN derivedTable RPAREN # tsiDerivedTable
    | changeTable                # tsiChangeTable
    | nodesMethod                # tsiNodesMethod
    | functionCall               # tsiFunctionCall
    | LOCAL_ID                   # tsiLocalId
    | LOCAL_ID DOT functionCall  # tsiLocalIdFunctionCall
    | openXml                    # tsiOpenXml
    | openJson                   # tsiOpenJson
    | DOUBLE_COLON functionCall  # tsiDoubleColonFunctionCall
    | LPAREN tableSource RPAREN  # tsiParenTableSource
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
    : CHANGETABLE LPAREN CHANGES changetable = tableName COMMA changesid = (NULL_ | INT | LOCAL_ID) RPAREN
    ;

changeTableVersion
    : CHANGETABLE LPAREN VERSION versiontable = tableName COMMA pkColumns = fullColumnNameList COMMA pkValues = selectList RPAREN
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
        OPENROWSET LPAREN providerName = STRING COMMA connectionString = STRING COMMA sql = STRING RPAREN
    )
    | (OPENROWSET LPAREN BULK dataFile = STRING COMMA ( bulkOption (COMMA bulkOption)* | id) RPAREN)
    ;

bulkOption: id EQ bulkOptionValue = (INT | STRING)
    ;

derivedTable: subquery | tableValueConstructor | LPAREN tableValueConstructor RPAREN
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

jsonNullClause: (loseNulls = ABSENT | NULL_) ON NULL_
    ;

hierarchyidStaticMethod
    : HIERARCHYID DOUBLE_COLON (GETROOT LPAREN RPAREN | PARSE LPAREN input = expression RPAREN)
    ;

nodesMethod
    : (locId = LOCAL_ID | valueId = fullColumnName | LPAREN subquery RPAREN) DOT NODES LPAREN xquery = STRING RPAREN
    ;

switchSection: WHEN searchCondition THEN expression
    ;

asColumnAlias: AS? columnAlias
    ;

asTableAlias: AS? (id | DOUBLE_QUOTE_ID)
    ;

withTableHints: WITH LPAREN tableHint (COMMA? tableHint)* RPAREN
    ;

deprecatedTableHint: LPAREN tableHint RPAREN
    ;

sybaseLegacyHint: HOLDLOCK | NOHOLDLOCK | READPAST | SHARED
    ;

tableHint
    : INDEX EQ? LPAREN expressionList RPAREN
    | FORCESEEK ( LPAREN expression LPAREN columnNameList RPAREN RPAREN)?
    | genericOption
    ;

indexValue: id | INT
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

createDatabaseOption
    : FILESTREAM (databaseFilestreamOption (COMMA databaseFilestreamOption)*)
    | DEFAULT_LANGUAGE EQ ( id | STRING)
    | DEFAULT_FULLTEXT_LANGUAGE EQ ( id | STRING)
    | NESTED_TRIGGERS EQ ( OFF | ON)
    | TRANSFORM_NOISE_WORDS EQ ( OFF | ON)
    | TWO_DIGIT_YEAR_CUTOFF EQ INT
    | DB_CHAINING ( OFF | ON)
    | TRUSTWORTHY ( OFF | ON)
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

entityName
    : (
        server = id DOT database = id DOT schema = id DOT
        | database = id DOT (schema = id)? DOT
        | schema = id DOT
    )? table = id
    ;

entityNameForAzureDw: schema = id | schema = id DOT objectName = id
    ;

entityNameForParallelDw: schemaDatabase = id | schema = id DOT objectName = id
    ;

tableName: (linkedServer = id DOT DOT)? ids += id (DOT ids += id)*
    ;

simpleName: (schema = id DOT)? name = id
    ;

funcProcNameSchema: ((schema = id) DOT)? procedure = id
    ;

funcProcNameDatabaseSchema
    : database = id? DOT schema = id? DOT procedure = id
    | funcProcNameSchema
    ;

funcProcNameServerDatabaseSchema
    : server = id? DOT database = id? DOT schema = id? DOT procedure = id
    | funcProcNameDatabaseSchema
    ;

ddlObject: tableName | rowsetFunctionLimited | LOCAL_ID
    ;

fullColumnName: ((DELETED | INSERTED | tableName) DOT)? ( id | (DOLLAR (IDENTITY | ROWGUID)))
    ;

columnNameListWithOrder: id (ASC | DESC)? (COMMA id (ASC | DESC)?)*
    ;

insertColumnNameList: insertColumnId (COMMA insertColumnId)*
    ;

insertColumnId: (id? DOT)* id
    ;

columnNameList: id (COMMA id)*
    ;

cursorName: id | LOCAL_ID
    ;

onOff: ON | OFF
    ;

clustered: CLUSTERED | NONCLUSTERED
    ;

nullNotnull: NOT? NULL_
    ;

beginConversationTimer
    : BEGIN CONVERSATION TIMER LPAREN LOCAL_ID RPAREN TIMEOUT EQ expression SEMI?
    ;

beginConversationDialog
    : BEGIN DIALOG (CONVERSATION)? dialogHandle = LOCAL_ID FROM SERVICE initiatorServiceName = serviceName TO SERVICE targetServiceName = serviceName
        (
        COMMA serviceBrokerGuid = STRING
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
    : END CONVERSATION conversationHandle = LOCAL_ID SEMI? (
        WITH (
            ERROR EQ faliureCode = (LOCAL_ID | STRING) DESCRIPTION EQ failureText = (
                LOCAL_ID
                | STRING
            )
        )? CLEANUP?
    )?
    ;

waitforConversation
    : WAITFOR? LPAREN getConversation RPAREN (COMMA? TIMEOUT timeout = expression)? SEMI?
    ;

getConversation
    : GET CONVERSATION GROUP conversationGroupId = (STRING | LOCAL_ID) FROM queue = queueId SEMI?
    ;

queueId: (databaseName = id DOT schemaName = id DOT name = id) | id
    ;

sendConversation
    : SEND ON CONVERSATION conversationHandle = (STRING | LOCAL_ID) MESSAGE TYPE messageTypeName = expression (
        LPAREN messageBodyExpression = (STRING | LOCAL_ID) RPAREN
    )? SEMI?
    ;

dataType: dataTypeIdentity | id (LPAREN (INT | MAX) (COMMA INT)? RPAREN)?
    ;

dataTypeIdentity: id IDENTITY (LPAREN INT COMMA INT RPAREN)?
    ;

constant: con = (STRING | HEX | INT | REAL | FLOAT | MONEY) | parameter
    ;

keyword
    : ABORT
    | ABORT_AFTER_WAIT
    | ABSENT
    | ABSOLUTE
    | ACCENT_SENSITIVITY
    | ACCESS
    | ACTION
    | ACTIVATION
    | ACTIVE
    | ADD // ?
    | ADDRESS
    | ADMINISTER
    | AES
    | AES_128
    | AES_192
    | AES_256
    | AFFINITY
    | AFTER
    | AGGREGATE
    | ALGORITHM
    | ALL_CONSTRAINTS
    | ALL_ERRORMSGS
    | ALL_INDEXES
    | ALL_LEVELS
    | ALLOW_CONNECTIONS
    | ALLOW_ENCRYPTED_VALUE_MODIFICATIONS
    | ALLOW_MULTIPLE_EVENT_LOSS
    | ALLOW_PAGE_LOCKS
    | ALLOW_ROW_LOCKS
    | ALLOW_SINGLE_EVENT_LOSS
    | ALLOW_SNAPSHOT_ISOLATION
    | ALLOWED
    | ALWAYS
    | ANONYMOUS
    | ANSI_DEFAULTS
    | ANSI_NULL_DEFAULT
    | ANSI_NULL_DFLT_OFF
    | ANSI_NULL_DFLT_ON
    | ANSI_NULLS
    | ANSI_PADDING
    | ANSI_WARNINGS
    | APPEND
    | APPLICATION
    | APPLICATION_LOG
    | APPLY
    | ARITHABORT
    | ARITHIGNORE
    | ASSEMBLY
    | ASYMMETRIC
    | ASYNCHRONOUS_COMMIT
    | AT_KEYWORD
    | AUDIT
    | AUDIT_GUID
    | AUTHENTICATE
    | AUTHENTICATION
    | AUTO
    | AUTO_CLEANUP
    | AUTO_CLOSE
    | AUTO_CREATE_STATISTICS
    | AUTO_DROP
    | AUTO_SHRINK
    | AUTO_UPDATE_STATISTICS
    | AUTO_UPDATE_STATISTICS_ASYNC
    | AUTOGROW_ALL_FILES
    | AUTOGROW_SINGLE_FILE
    | AUTOMATED_BACKUP_PREFERENCE
    | AUTOMATIC
    | AVAILABILITY
    | AVAILABILITY_MODE
    | BACKUP_CLONEDB
    | BACKUP_PRIORITY
    | BASE64
    | BEFORE
    | BEGIN_DIALOG
    | BIGINT
    | BINARY_KEYWORD
    | BINDING
    | BLOB_STORAGE
    | BLOCK
    | BLOCKERS
    | BLOCKSIZE
    | BROKER
    | BROKER_INSTANCE
    | BUFFER
    | BUFFERCOUNT
    | BULK_LOGGED
    | CACHE
    | CALLED
    | CALLER
    | CAP_CPU_PERCENT
    | CAST
    | CATALOG
    | CATCH
    | CERTIFICATE
    | CHANGE
    | CHANGE_RETENTION
    | CHANGE_TRACKING
    | CHANGES
    | CHANGETABLE
    | CHECK_EXPIRATION
    | CHECK_POLICY
    | CHECKALLOC
    | CHECKCATALOG
    | CHECKCONSTRAINTS
    | CHECKDB
    | CHECKFILEGROUP
    | CHECKSUM
    | CHECKTABLE
    | CLASSIFIER_FUNCTION
    | CLEANTABLE
    | CLEANUP
    | CLONEDATABASE
    | CLUSTER
    | COLLECTION
    | COLUMN_ENCRYPTION_KEY
    | COLUMN_MASTER_KEY
    | COLUMNS
    | COLUMNSTORE
    | COLUMNSTORE_ARCHIVE
    | COMMITTED
    | COMPATIBILITY_LEVEL
    | COMPRESS_ALL_ROW_GROUPS
    | COMPRESSION
    | COMPRESSION_DELAY
    | CONCAT
    | CONCAT_NULL_YIELDS_NULL
    | CONFIGURATION
    | CONNECT
    | CONNECTION
    | CONTAINMENT
    | CONTENT
    | CONTEXT
    | CONTINUE_AFTER_ERROR
    | CONTRACT
    | CONTRACT_NAME
    | CONTROL
    | CONVERSATION
    | COOKIE
    | COPY_ONLY
    | COUNTER
    | CPU
    | CREATE_NEW
    | CREATION_DISPOSITION
    | CREDENTIAL
    | CRYPTOGRAPHIC
    | CURSOR_CLOSE_ON_COMMIT
    | CURSOR_DEFAULT
    | CYCLE
    | DATA
    | DATA_COMPRESSION
    | DATA_PURITY
    | DATA_SOURCE
    | DATABASE_MIRRORING
    | DATASPACE
    | DATE_CORRELATION_OPTIMIZATION
    | DAYS
    | DB_CHAINING
    | DB_FAILOVER
    | DBCC
    | DBREINDEX
    | DDL
    | DECRYPTION
    | DEFAULT
    | DEFAULT_DATABASE
    | DEFAULT_DOUBLE_QUOTE
    | DEFAULT_FULLTEXT_LANGUAGE
    | DEFAULT_LANGUAGE
    | DEFAULT_SCHEMA
    | DEFINITION
    | DELAY
    | DELAYED_DURABILITY
    | DELETED
    | DEPENDENTS
    | DES
    | DESCRIPTION
    | DESX
    | DETERMINISTIC
    | DHCP
    | DIAGNOSTICS
    | DIALOG
    | DIFFERENTIAL
    | DIRECTORY_NAME
    | DISABLE
    | DISABLE_BROKER
    | DISABLED
    | DISTRIBUTION
    | DOCUMENT
    | DROP_EXISTING
    | DROPCLEANBUFFERS
    | DTC_SUPPORT
    | DYNAMIC
    | ELEMENTS
    | EMERGENCY
    | EMPTY
    | ENABLE
    | ENABLE_BROKER
    | ENABLED
    | ENCRYPTED
    | ENCRYPTED_VALUE
    | ENCRYPTION
    | ENCRYPTION_TYPE
    | ENDPOINT
    | ENDPOINT_URL
    | ERROR
    | ERROR_BROKER_CONVERSATIONS
    | ESTIMATEONLY
    | EVENT
    | EVENT_RETENTION_MODE
    | EXCLUSIVE
    | EXECUTABLE
    | EXECUTABLE_FILE
    | EXPIREDATE
    | EXPIRY_DATE
    | EXPLICIT
    | EXTENDED_LOGICAL_CHECKS
    | EXTENSION
    | EXTERNAL_ACCESS
    | FAIL_OPERATION
    | FAILOVER
    | FAILOVER_MODE
    | FAILURE
    | FAILURE_CONDITION_LEVEL
    | FAILURECONDITIONLEVEL
    | FAN_IN
    | FAST_FORWARD
    | FILE_SNAPSHOT
    | FILEGROUP
    | FILEGROWTH
    | FILENAME
    | FILEPATH
    | FILESTREAM
    | FILESTREAM_ON
    | FILTER
    | FIRST
    | FMTONLY
    | FOLLOWING
    | FORCE
    | FORCE_FAILOVER_ALLOW_DATA_LOSS
    | FORCE_SERVICE_ALLOW_DATA_LOSS
    | FORCEPLAN
    | FORCESCAN
    | FORCESEEK
    | FORMAT
    | FORWARD_ONLY
    | FREE
    | FULLSCAN
    | FULLTEXT
    | GB
    | GENERATED
    | GET
    | GETROOT
    | GLOBAL
    | GO
    | GOVERNOR
    | GROUP_MAX_REQUESTS
    | GROUPING
    | HADR
    | HASH
    | HASHED
    | HEALTH_CHECK_TIMEOUT
    | HEALTHCHECKTIMEOUT
    | HEAP
    | HIDDEN_KEYWORD
    | HIERARCHYID
    | HIGH
    | HONOR_BROKER_PRIORITY
    | HOURS
    | IDENTITY_VALUE
    | IGNORE_CONSTRAINTS
    | IGNORE_DUP_KEY
    | IGNORE_REPLICATED_TABLE_CACHE
    | IGNORE_TRIGGERS
    | IIF
    | IMMEDIATE
    | IMPERSONATE
    | IMPLICIT_TRANSACTIONS
    | IMPORTANCE
    | INCLUDE
    | INCLUDE_NULL_VALUES
    | INCREMENT
    | INCREMENTAL
    | INFINITE
    | INIT
    | INITIATOR
    | INPUT
    | INSENSITIVE
    | INSERTED
    | INSTEAD
    | IO
    | IP
    | ISOLATION
    | JOB
    | JSON
    | JSON_ARRAY
    | JSON_OBJECT
    | KB
    | KEEPDEFAULTS
    | KEEPIDENTITY
    | KERBEROS
    | KEY_PATH
    | KEY_SOURCE
    | KEY_STORE_PROVIDER_NAME
    | KEYS
    | KEYSET
    | KWINT
    | LANGUAGE
    | LAST
    | LEVEL
    | LIBRARY
    | LIFETIME
    | LINKED
    | LINUX
    | LIST
    | LISTENER
    | LISTENER_IP
    | LISTENER_PORT
    | LISTENER_URL
    | LOB_COMPACTION
    | LOCAL
    | LOCAL_SERVICE_NAME
    | LOCATION
    | LOCK
    | LOCK_ESCALATION
    | LOGIN
    | LOOP
    | LOW
    | MANUAL
    | MARK
    | MASK
    | MASKED
    | MASTER
    | MATCHED
    | MATERIALIZED
    | MAX
    | MAX_CPU_PERCENT
    | MAX_DISPATCH_LATENCY
    | MAX_DOP
    | MAX_DURATION
    | MAX_EVENT_SIZE
    | MAX_FILES
    | MAX_IOPS_PER_VOLUME
    | MAX_MEMORY
    | MAX_MEMORY_PERCENT
    | MAX_OUTSTANDING_IO_PER_VOLUME
    | MAX_PROCESSES
    | MAX_QUEUE_READERS
    | MAX_ROLLOVER_FILES
    | MAX_SIZE
    | MAXSIZE
    | MAXTRANSFER
    | MAXVALUE
    | MB
    | MEDIADESCRIPTION
    | MEDIANAME
    | MEDIUM
    | MEMBER
    | MEMORY_OPTIMIZED_DATA
    | MEMORY_PARTITION_MODE
    | MESSAGE
    | MESSAGE_FORWARD_SIZE
    | MESSAGE_FORWARDING
    | MIN_CPU_PERCENT
    | MIN_IOPS_PER_VOLUME
    | MIN_MEMORY_PERCENT
    | MINUTES
    | MINVALUE
    | MIRROR
    | MIRROR_ADDRESS
    | MIXED_PAGE_ALLOCATION
    | MODE
    | MODIFY
    | MOVE
    | MULTI_USER
    | MUST_CHANGE
    | NAME
    | NESTED_TRIGGERS
    | NEW_ACCOUNT
    | NEW_BROKER
    | NEW_PASSWORD
    | NEWNAME
    | NEXT
    | NO
    | NO_CHECKSUM
    | NO_COMPRESSION
    | NO_EVENT_LOSS
    | NO_INFOMSGS
    | NO_QUERYSTORE
    | NO_STATISTICS
    | NO_TRUNCATE
    | NOCOUNT
    | NODES
    | NOEXEC
    | NOEXPAND
    | NOFORMAT
    | NOINDEX
    | NOINIT
    | NOLOCK
    | NON_TRANSACTED_ACCESS
    | NONE
    | NORECOMPUTE
    | NORECOVERY
    | NOREWIND
    | NOSKIP
    | NOTIFICATION
    | NOTIFICATIONS
    | NOUNLOAD
    | NTILE
    | NTLM
    | NUMANODE
    | NUMBER
    | NUMERIC_ROUNDABORT
    | OBJECT
    | OFFLINE
    | OFFSET
    | OLD_ACCOUNT
    | OLD_PASSWORD
    | ON_FAILURE
    | ON
    | OFF
    | ONLINE
    | ONLY
    | OPEN_EXISTING
    | OPENJSON
    | OPERATIONS
    | OPTIMISTIC
    | OUT
    | OUTPUT
    | OVERRIDE
    | OWNER
    | OWNERSHIP
    | PAD_INDEX
    | PAGE
    | PAGE_VERIFY
    | PAGECOUNT
    | PAGLOCK
    | PARAM_NODE
    | PARAMETERIZATION
    | PARSEONLY
    | PARTIAL
    | PARTITION
    | PARTITIONS
    | PARTNER
    | PASSWORD
    | PATH
    | PAUSE
    | PDW_SHOWSPACEUSED
    | PER_CPU
    | PER_DB
    | PER_NODE
    | PERMISSION_SET
    | PERSIST_SAMPLE_PERCENT
    | PERSISTED
    | PHYSICAL_ONLY
    | PLATFORM
    | POISON_MESSAGE_HANDLING
    | POLICY
    | POOL
    | PORT
    | PRECEDING
    | PRECISION
    | PREDICATE
    | PRIMARY_ROLE
    | PRIOR
    | PRIORITY
    | PRIORITY_LEVEL
    | PRIVATE
    | PRIVATE_KEY
    | PRIVILEGES
    | PROCCACHE
    | PROCEDURE_NAME
    | PROCESS
    | PROFILE
    | PROPERTY
    | PROVIDER
    | PROVIDER_KEY_NAME
    | PYTHON
    | QUERY
    | QUEUE
    | QUEUE_DELAY
    | QUOTED_IDENTIFIER
    | R
    | RANDOMIZED
    | RANGE
    | RC2
    | RC4
    | RC4_128
    | READ_COMMITTED_SNAPSHOT
    | READ_ONLY
    | READ_ONLY_ROUTING_LIST
    | READ_WRITE
    | READ_WRITE_FILEGROUPS
    | READCOMMITTED
    | READCOMMITTEDLOCK
    | READONLY
    | READPAST
    | READUNCOMMITTED
    | READWRITE
    | REBUILD
    | RECEIVE
    | RECOVERY
    | RECURSIVE_TRIGGERS
    | REGENERATE
    | RELATED_CONVERSATION
    | RELATED_CONVERSATION_GROUP
    | RELATIVE
    | REMOTE
    | REMOTE_PROC_TRANSACTIONS
    | REMOTE_SERVICE_NAME
    | REMOVE
    | REORGANIZE
    | REPAIR_ALLOW_DATA_LOSS
    | REPAIR_FAST
    | REPAIR_REBUILD
    | REPEATABLE
    | REPEATABLEREAD
    | REPLACE
    | REPLICA
    | REQUEST_MAX_CPU_TIME_SEC
    | REQUEST_MAX_MEMORY_GRANT_PERCENT
    | REQUEST_MEMORY_GRANT_TIMEOUT_SEC
    | REQUIRED
    | REQUIRED_SYNCHRONIZED_SECONDARIES_TO_COMMIT
    | RESAMPLE
    | RESERVE_DISK_SPACE
    | RESET
    | RESOURCE
    | RESOURCE_MANAGER_LOCATION
    | RESOURCES
    | RESTART
    | RESTRICTED_USER
    | RESUMABLE
    | RESUME
    | RETAINDAYS
    | RETENTION
    | RETURNS
    | REWIND
    | ROLE
    | ROOT
    | ROUND_ROBIN
    | ROUTE
    | ROW
    | ROWGUID
    | ROWLOCK
    | ROWS
    | RSA_512
    | RSA_1024
    | RSA_2048
    | RSA_3072
    | RSA_4096
    | SAFE
    | SAFETY
    | SAMPLE
    | SCHEDULER
    | SCHEMABINDING
    | SCHEME
    | SCOPED
    | SCRIPT
    | SCROLL
    | SCROLL_LOCKS
    | SEARCH
    | SECONDARY
    | SECONDARY_ONLY
    | SECONDARY_ROLE
    | SECONDS
    | SECRET
    | SECURABLES
    | SECURITY
    | SECURITY_LOG
    | SEEDING_MODE
    | SELF
    | SEMI_SENSITIVE
    | SEND
    | SENT
    | SEQUENCE
    | SEQUENCE_NUMBER
    | SERIALIZABLE
    | SERVER
    | SERVICE
    | SERVICE_BROKER
    | SERVICE_NAME
    | SERVICEBROKER
    | SESSION
    | SESSION_TIMEOUT
    | SETTINGS
    | SHARE
    | SHARED
    | SHOWCONTIG
    | SHOWPLAN
    | SHOWPLAN_ALL
    | SHOWPLAN_TEXT
    | SHOWPLAN_XML
    | SHRINKLOG
    | SID
    | SIGNATURE
    | SINGLE_USER
    | SIZE
    | SKIP_KEYWORD
    | SMALLINT
    | SNAPSHOT
    | SOFTNUMA
    | SORT_IN_TEMPDB
    | SOURCE
    | SP_EXECUTESQL
    | SPARSE
    | SPATIAL_WINDOW_MAX_CELLS
    | SPECIFICATION
    | SPLIT
    | SQL
    | SQLDUMPERFLAGS
    | SQLDUMPERPATH
    | SQLDUMPERTIMEOUT
    | STANDBY
    | START
    | START_DATE
    | STARTED
    | STARTUP_STATE
    | STATE
    | STATIC
    | STATISTICS_INCREMENTAL
    | STATISTICS_NORECOMPUTE
    | STATS
    | STATS_STREAM
    | STATUS
    | STATUSONLY
    | STOP
    | STOP_ON_ERROR
    | STOPLIST
    | STOPPED
    | SUBJECT
    | SUBSCRIBE
    | SUBSCRIPTION
    | SUPPORTED
    | SUSPEND
    | SWITCH
    | SYMMETRIC
    | SYNCHRONOUS_COMMIT
    | SYNONYM
    | SYSTEM
    | TABLE
    | TABLERESULTS
    | TABLOCK
    | TABLOCKX
    | TAKE
    | TAPE
    | TARGET
    | TARGET_RECOVERY_TIME
    | TB
    | TCP
    | TEXTIMAGE_ON
    | THROW
    | TIES
    | TIMEOUT
    | TIMER
    | TINYINT
    | TORN_PAGE_DETECTION
    | TOSTRING
    | TRACE
    | TRACK_CAUSALITY
    | TRACKING
    | TRANSACTION_ID
    | TRANSFER
    | TRANSFORM_NOISE_WORDS
    | TRIPLE_DES
    | TRIPLE_DES_3KEY
    | TRUSTWORTHY
    | TRY
    | TRY_CAST
    | TSQL
    | TWO_DIGIT_YEAR_CUTOFF
    | TYPE
    | TYPE_WARNING
    | UNBOUNDED
    | UNCHECKED
    | UNCOMMITTED
    | UNLIMITED
    | UNLOCK
    | UNMASK
    | UNSAFE
    | UOW
    | UPDLOCK
    | URL
    | USED
    | USING
    | VALID_XML
    | VALIDATION
    | VALUE
    | VAR
    | VERBOSELOGGING
    | VERIFY_CLONEDB
    | VERSION
    | VIEW_METADATA
    | VISIBILITY
    | WAIT
    | WAIT_AT_LOW_PRIORITY
    | WELL_FORMED_XML
    | WINDOWS
    | WITHOUT
    | WITHOUT_ARRAY_WRAPPER
    | WITNESS
    | WORK
    | WORKLOAD
    | XACT_ABORT
    | XLOCK
    | XML
    | XML_COMPRESSION
    | XMLDATA
    | XMLNAMESPACES
    | XMLSCHEMA
    | XSINIL
    | ZONE
    ;

id: ID | TEMP_ID | DOUBLE_QUOTE_ID | SQUARE_BRACKET_ID | keyword | RAW
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

xmlCommonDirectives: COMMA ( BINARY_KEYWORD BASE64 | TYPE | ROOT (LPAREN STRING RPAREN)?)
    ;