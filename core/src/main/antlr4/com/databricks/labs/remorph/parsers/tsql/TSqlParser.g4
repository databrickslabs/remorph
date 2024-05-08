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

// $antlr-format alignTrailingComments true, columnLimit 150, minEmptyLines 1, maxEmptyLinesToKeep 1, reflowComments false, useTab false
// $antlr-format allowShortRulesOnASingleLine false, allowShortBlocksOnASingleLine true, alignSemicolons hanging, alignColons hanging

parser grammar TSqlParser;

options {
    tokenVocab = TSqlLexer;
}

tsqlFile
    : batch* EOF
    | executeBodyBatch goStatement* EOF
    ;

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

// Data Manipulation Language: https://msdn.microsoft.com/en-us/library/ff848766(v=sql.120).aspx
dmlClause
    : mergeStatement
    | deleteStatement
    | insertStatement
    | selectStatementStandalone
    | updateStatement
    ;

// Data Definition Language: https://msdn.microsoft.com/en-us/library/ff848799.aspx)
ddlClause
    : alterApplicationRole
    | alterAssembly
    | alterAsymmetricKey
    | alterAuthorization
    | alterAuthorizationForAzureDw
    | alterAuthorizationForParallelDw
    | alterAuthorizationForSqlDatabase
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

// Control-of-Flow Language: https://docs.microsoft.com/en-us/sql/t-sql/language-elements/control-of-flow
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

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/begin-end-transact-sql
blockStatement
    : BEGIN SEMI? sqlClauses* END SEMI?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/break-transact-sql
breakStatement
    : BREAK SEMI?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/continue-transact-sql
continueStatement
    : CONTINUE SEMI?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/goto-transact-sql
gotoStatement
    : GOTO id_ SEMI?
    | id_ COLON SEMI?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/return-transact-sql
returnStatement
    : RETURN expression? SEMI?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/if-else-transact-sql
ifStatement
    : IF searchCondition sqlClauses (ELSE sqlClauses)? SEMI?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/throw-transact-sql
throwStatement
    : THROW (throwErrorNumber COMMA throwMessage COMMA throwState)? SEMI?
    ;

throwErrorNumber
    : INT
    | LOCAL_ID
    ;

throwMessage
    : STRING
    | LOCAL_ID
    ;

throwState
    : INT
    | LOCAL_ID
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/try-catch-transact-sql
tryCatchStatement
    : BEGIN TRY SEMI? tryClauses = sqlClauses+ END TRY SEMI? BEGIN CATCH SEMI? catchClauses = sqlClauses* END CATCH SEMI?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/waitfor-transact-sql
waitforStatement
    : WAITFOR receiveStatement? COMMA? ((DELAY | TIME | TIMEOUT) time)? expression? SEMI?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/while-transact-sql
whileStatement
    : WHILE searchCondition (sqlClauses | BREAK SEMI? | CONTINUE SEMI?)
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/print-transact-sql
printStatement
    : PRINT (expression | DOUBLE_QUOTE_ID) (COMMA LOCAL_ID)* SEMI?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/raiserror-transact-sql
raiseerrorStatement
    : RAISERROR LPAREN msg = (INT | STRING | LOCAL_ID) COMMA severity = constant_LOCAL_ID COMMA state = constant_LOCAL_ID (
        COMMA (constant_LOCAL_ID | NULL_)
    )* RPAREN (WITH (LOG | SETERROR | NOWAIT))? SEMI?
    | RAISERROR INT formatstring = (STRING | LOCAL_ID | DOUBLE_QUOTE_ID) (
        COMMA argument = (INT | STRING | LOCAL_ID)
    )*
    ;

emptyStatement
    : SEMI
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

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-application-role-transact-sql
alterApplicationRole
    : ALTER APPLICATION ROLE applictionRole = id_ WITH (
        COMMA? NAME EQ newApplicationRoleName = id_
    )? (COMMA? PASSWORD EQ applicationRolePassword = STRING)? (
        COMMA? DEFAULT_SCHEMA EQ appRoleDefaultSchema = id_
    )?
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-xml-schema-collection-transact-sql?view=sql-server-ver16
alterXmlSchemaCollection
    : ALTER XML SCHEMA COLLECTION (id_ DOT)? id_ ADD STRING
    ;

createApplicationRole
    : CREATE APPLICATION ROLE applictionRole = id_ WITH (
        COMMA? PASSWORD EQ applicationRolePassword = STRING
    )? (COMMA? DEFAULT_SCHEMA EQ appRoleDefaultSchema = id_)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-aggregate-transact-sql

dropAggregate
    : DROP AGGREGATE (IF EXISTS)? (schemaName = id_ DOT)? aggregateName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-application-role-transact-sql
dropApplicationRole
    : DROP APPLICATION ROLE rolename = id_
    ;

alterAssembly
    : alterAssemblyStart assemblyName = id_ alterAssemblyClause
    ;

alterAssemblyStart
    : ALTER ASSEMBLY
    ;

alterAssemblyClause
    : alterAssemblyFromClause? alterAssemblyWithClause? alterAssemblyDropClause? alterAssemblyAddClause?
    ;

alterAssemblyFromClause
    : alterAssemblyFromClauseStart (clientAssemblySpecifier | alterAssemblyFileBits)
    ;

alterAssemblyFromClauseStart
    : FROM
    ;

alterAssemblyDropClause
    : alterAssemblyDrop alterAssemblyDropMultipleFiles
    ;

alterAssemblyDropMultipleFiles
    : ALL
    | multipleLocalFiles
    ;

alterAssemblyDrop
    : DROP
    ;

alterAssemblyAddClause
    : alterAsssemblyAddClauseStart alterAssemblyClientFileClause
    ;

alterAsssemblyAddClauseStart
    : ADD FILE FROM
    ;

// need to implement
alterAssemblyClientFileClause
    : alterAssemblyFileName (alterAssemblyAs id_)?
    ;

alterAssemblyFileName
    : STRING
    ;

//need to implement
alterAssemblyFileBits
    : alterAssemblyAs id_
    ;

alterAssemblyAs
    : AS
    ;

alterAssemblyWithClause
    : alterAssemblyWith assemblyOption
    ;

alterAssemblyWith
    : WITH
    ;

clientAssemblySpecifier
    : networkFileShare
    | localFile
    | STRING
    ;

assemblyOption
    : PERMISSION_SET EQ (SAFE | EXTERNAL_ACCESS | UNSAFE)
    | VISIBILITY EQ onOff
    | UNCHECKED DATA
    | assemblyOption COMMA
    ;

networkFileShare
    : BACKSLASH BACKSLASH networkComputer filePath
    ;

networkComputer
    : computerName = id_
    ;

filePath
    : BACKSLASH filePath
    | id_
    ;

localFile
    : localDrive filePath
    ;

localDrive
    : DISK_DRIVE
    ;

multipleLocalFiles
    : multipleLocalFileStart localFile SINGLE_QUOTE COMMA
    | localFile
    ;

multipleLocalFileStart
    : SINGLE_QUOTE
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-assembly-transact-sql
createAssembly
    : CREATE ASSEMBLY assemblyName = id_ (AUTHORIZATION ownerName = id_)? FROM (
        COMMA? (STRING | HEX)
    )+ (WITH PERMISSION_SET EQ (SAFE | EXTERNAL_ACCESS | UNSAFE))?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-assembly-transact-sql
dropAssembly
    : DROP ASSEMBLY (IF EXISTS)? (COMMA? assemblyName = id_)+ (WITH NO DEPENDENTS)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-asymmetric-key-transact-sql

alterAsymmetricKey
    : alterAsymmetricKeyStart Asym_Key_Name = id_ (asymmetricKeyOption | REMOVE PRIVATE KEY)
    ;

alterAsymmetricKeyStart
    : ALTER ASYMMETRIC KEY
    ;

asymmetricKeyOption
    : asymmetricKeyOptionStart asymmetricKeyPasswordChangeOption (
        COMMA asymmetricKeyPasswordChangeOption
    )? RPAREN
    ;

asymmetricKeyOptionStart
    : WITH PRIVATE KEY LPAREN
    ;

asymmetricKeyPasswordChangeOption
    : DECRYPTION BY PASSWORD EQ STRING
    | ENCRYPTION BY PASSWORD EQ STRING
    ;

//https://docs.microsoft.com/en-us/sql/t-sql/statements/create-asymmetric-key-transact-sql

createAsymmetricKey
    : CREATE ASYMMETRIC KEY Asym_Key_Nam = id_ (AUTHORIZATION databasePrincipalName = id_)? (
        FROM (
            FILE EQ STRING
            | EXECUTABLE_FILE EQ STRING
            | ASSEMBLY Assembly_Name = id_
            | PROVIDER Provider_Name = id_
        )
    )? (
        WITH (
            ALGORITHM EQ (RSA_4096 | RSA_3072 | RSA_2048 | RSA_1024 | RSA_512)
            | PROVIDER_KEY_NAME EQ providerKeyName = STRING
            | CREATION_DISPOSITION EQ (CREATE_NEW | OPEN_EXISTING)
        )
    )? (ENCRYPTION BY PASSWORD EQ asymmetricKeyPassword = STRING)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-asymmetric-key-transact-sql
dropAsymmetricKey
    : DROP ASYMMETRIC KEY keyName = id_ (REMOVE PROVIDER KEY)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-authorization-transact-sql

alterAuthorization
    : alterAuthorizationStart (classType colonColon)? entity = entityName entityTo authorizationGrantee
    ;

authorizationGrantee
    : principalName = id_
    | SCHEMA OWNER
    ;

entityTo
    : TO
    ;

colonColon
    : DOUBLE_COLON
    ;

alterAuthorizationStart
    : ALTER AUTHORIZATION ON
    ;

alterAuthorizationForSqlDatabase
    : alterAuthorizationStart (classTypeForSqlDatabase colonColon)? entity = entityName entityTo authorizationGrantee
    ;

alterAuthorizationForAzureDw
    : alterAuthorizationStart (classTypeForAzureDw colonColon)? entity = entityNameForAzureDw entityTo authorizationGrantee
    ;

alterAuthorizationForParallelDw
    : alterAuthorizationStart (classTypeForParallelDw colonColon)? entity = entityNameForParallelDw entityTo authorizationGrantee
    ;

classType
    : OBJECT
    | ASSEMBLY
    | ASYMMETRIC KEY
    | AVAILABILITY GROUP
    | CERTIFICATE
    | CONTRACT
    | TYPE
    | DATABASE
    | ENDPOINT
    | FULLTEXT CATALOG
    | FULLTEXT STOPLIST
    | MESSAGE TYPE
    | REMOTE SERVICE BINDING
    | ROLE
    | ROUTE
    | SCHEMA
    | SEARCH PROPERTY LIST
    | SERVER ROLE
    | SERVICE
    | SYMMETRIC KEY
    | XML SCHEMA COLLECTION
    ;

classTypeForSqlDatabase
    : OBJECT
    | ASSEMBLY
    | ASYMMETRIC KEY
    | CERTIFICATE
    | TYPE
    | DATABASE
    | FULLTEXT CATALOG
    | FULLTEXT STOPLIST
    | ROLE
    | SCHEMA
    | SEARCH PROPERTY LIST
    | SYMMETRIC KEY
    | XML SCHEMA COLLECTION
    ;

classTypeForAzureDw
    : SCHEMA
    | OBJECT
    ;

classTypeForParallelDw
    : DATABASE
    | SCHEMA
    | OBJECT
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/grant-transact-sql?view=sql-server-ver15
// SELECT DISTINCT '| ' + CLASS_DESC
// FROM sys.dmAuditActions
// ORDER BY 1
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
        | SCOPED ( CONFIGURATION | CREDENTIAL | RESOURCE GOVERNOR)
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

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-availability-group-transact-sql
dropAvailabilityGroup
    : DROP AVAILABILITY GROUP groupName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-availability-group-transact-sql
alterAvailabilityGroup
    : alterAvailabilityGroupStart alterAvailabilityGroupOptions
    ;

alterAvailabilityGroupStart
    : ALTER AVAILABILITY GROUP groupName = id_
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
    | ADD DATABASE databaseName = id_
    | REMOVE DATABASE databaseName = id_
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
        | READ_ONLY_ROUTING_LIST EQ ( LPAREN ( ( STRING)) RPAREN)
    )
    | PRIMARY_ROLE LPAREN (
        ALLOW_CONNECTIONS EQ (NO | READ_ONLY | ALL)
        | READ_ONLY_ROUTING_LIST EQ (LPAREN ( (COMMA? STRING)* | NONE) RPAREN)
        | SESSION_TIMEOUT EQ sessionTimeout = INT
    )
    | MODIFY REPLICA ON serverInstance = STRING (
        WITH LPAREN (
            ENDPOINT_URL EQ STRING
            | AVAILABILITY_MODE EQ (SYNCHRONOUS_COMMIT | ASYNCHRONOUS_COMMIT)
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
            | READ_ONLY_ROUTING_LIST EQ (LPAREN ( (COMMA? STRING)* | NONE) RPAREN)
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
            )? (COMMA? FAILOVER_MODE EQ MANUAL)? (
                COMMA? SEEDING_MODE EQ (AUTOMATIC | MANUAL)
            )? RPAREN
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
        ADD IP LPAREN (ipV4_failover ipV4_failover | ipV6_failover) RPAREN
        | PORT EQ INT
    )
    | RESTART LISTENER STRING
    | REMOVE LISTENER STRING
    | OFFLINE
    | WITH LPAREN DTC_SUPPORT EQ PER_DB RPAREN
    ;

ipV4_failover
    : STRING
    ;

ipV6_failover
    : STRING
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-broker-priority-transact-sql
// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-broker-priority-transact-sql
createOrAlterBrokerPriority
    : (CREATE | ALTER) BROKER PRIORITY ConversationPriorityName = id_ FOR CONVERSATION SET LPAREN (
        CONTRACT_NAME EQ ( ( id_) | ANY) COMMA?
    )? (LOCAL_SERVICE_NAME EQ (DOUBLE_FORWARD_SLASH? id_ | ANY) COMMA?)? (
        REMOTE_SERVICE_NAME EQ (RemoteServiceName = STRING | ANY) COMMA?
    )? (PRIORITY_LEVEL EQ ( PriorityValue = INT | DEFAULT))? RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-broker-priority-transact-sql
dropBrokerPriority
    : DROP BROKER PRIORITY ConversationPriorityName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-certificate-transact-sql
alterCertificate
    : ALTER CERTIFICATE certificateName = id_ (
        REMOVE PRIVATE_KEY
        | WITH PRIVATE KEY LPAREN (
            FILE EQ STRING COMMA?
            | DECRYPTION BY PASSWORD EQ STRING COMMA?
            | ENCRYPTION BY PASSWORD EQ STRING COMMA?
        )+ RPAREN
        | WITH ACTIVE FOR BEGIN_DIALOG EQ ( ON | OFF)
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-column-encryption-key-transact-sql
alterColumnEncryptionKey
    : ALTER COLUMN ENCRYPTION KEY columnEncryptionKey = id_ (ADD | DROP) VALUE LPAREN COLUMN_MASTER_KEY EQ columnMasterKeyName = id_ (
        COMMA ALGORITHM EQ algorithmName = STRING COMMA ENCRYPTED_VALUE EQ HEX
    )? RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-column-encryption-key-transact-sql
createColumnEncryptionKey
    : CREATE COLUMN ENCRYPTION KEY columnEncryptionKey = id_ WITH VALUES (
        LPAREN COMMA? COLUMN_MASTER_KEY EQ columnMasterKeyName = id_ COMMA ALGORITHM EQ algorithmName = STRING COMMA ENCRYPTED_VALUE
            EQ encryptedValue = HEX RPAREN COMMA?
    )+
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-certificate-transact-sql
dropCertificate
    : DROP CERTIFICATE certificateName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-column-encryption-key-transact-sql
dropColumnEncryptionKey
    : DROP COLUMN ENCRYPTION KEY keyName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-column-master-key-transact-sql
dropColumnMasterKey
    : DROP COLUMN MASTER KEY keyName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-contract-transact-sql
dropContract
    : DROP CONTRACT droppedContractName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-credential-transact-sql
dropCredential
    : DROP CREDENTIAL credentialName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-cryptographic-provider-transact-sql
dropCryptograhicProvider
    : DROP CRYPTOGRAPHIC PROVIDER providerName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-database-transact-sql
dropDatabase
    : DROP DATABASE (IF EXISTS)? (COMMA? databaseNameOrDatabaseSnapshotName = id_)+
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-database-audit-specification-transact-sql
dropDatabaseAuditSpecification
    : DROP DATABASE AUDIT SPECIFICATION auditSpecificationName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-database-encryption-key-transact-sql?view=sql-server-ver15
dropDatabaseEncryptionKey
    : DROP DATABASE ENCRYPTION KEY
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-database-scoped-credential-transact-sql
dropDatabaseScopedCredential
    : DROP DATABASE SCOPED CREDENTIAL credentialName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-default-transact-sql
dropDefault
    : DROP DEFAULT (IF EXISTS)? (COMMA? (schemaName = id_ DOT)? defaultName = id_)
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-endpoint-transact-sql
dropEndpoint
    : DROP ENDPOINT endPointName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-external-data-source-transact-sql
dropExternalDataSource
    : DROP EXTERNAL DATA SOURCE externalDataSourceName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-external-file-format-transact-sql
dropExternalFileFormat
    : DROP EXTERNAL FILE FORMAT externalFileFormatName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-external-library-transact-sql
dropExternalLibrary
    : DROP EXTERNAL LIBRARY libraryName = id_ (AUTHORIZATION ownerName = id_)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-external-resource-pool-transact-sql
dropExternalResourcePool
    : DROP EXTERNAL RESOURCE POOL poolName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-external-table-transact-sql
dropExternalTable
    : DROP EXTERNAL TABLE (databaseName = id_ DOT)? (schemaName = id_ DOT)? table = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-event-notification-transact-sql
dropEventNotifications
    : DROP EVENT NOTIFICATION (COMMA? notificationName = id_)+ ON (
        SERVER
        | DATABASE
        | QUEUE queueName = id_
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-event-session-transact-sql
dropEventSession
    : DROP EVENT SESSION eventSessionName = id_ ON SERVER
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-fulltext-catalog-transact-sql
dropFulltextCatalog
    : DROP FULLTEXT CATALOG catalogName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-fulltext-index-transact-sql
dropFulltextIndex
    : DROP FULLTEXT INDEX ON (schema = id_ DOT)? table = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-fulltext-stoplist-transact-sql
dropFulltextStoplist
    : DROP FULLTEXT STOPLIST stoplistName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-login-transact-sql
dropLogin
    : DROP LOGIN loginName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-master-key-transact-sql
dropMasterKey
    : DROP MASTER KEY
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-message-type-transact-sql
dropMessageType
    : DROP MESSAGE TYPE messageTypeName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-partition-function-transact-sql
dropPartitionFunction
    : DROP PARTITION FUNCTION partitionFunctionName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-partition-scheme-transact-sql
dropPartitionScheme
    : DROP PARTITION SCHEME partitionSchemeName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-queue-transact-sql
dropQueue
    : DROP QUEUE (databaseName = id_ DOT)? (schemaName = id_ DOT)? queueName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-remote-service-binding-transact-sql
dropRemoteServiceBinding
    : DROP REMOTE SERVICE BINDING bindingName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-resource-pool-transact-sql
dropResourcePool
    : DROP RESOURCE POOL poolName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-role-transact-sql
dropDbRole
    : DROP ROLE (IF EXISTS)? roleName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-route-transact-sql
dropRoute
    : DROP ROUTE routeName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-rule-transact-sql
dropRule
    : DROP RULE (IF EXISTS)? (COMMA? (schemaName = id_ DOT)? ruleName = id_)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-schema-transact-sql
dropSchema
    : DROP SCHEMA (IF EXISTS)? schemaName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-search-property-list-transact-sql
dropSearchPropertyList
    : DROP SEARCH PROPERTY LIST propertyListName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-security-policy-transact-sql
dropSecurityPolicy
    : DROP SECURITY POLICY (IF EXISTS)? (schemaName = id_ DOT)? securityPolicyName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-sequence-transact-sql
dropSequence
    : DROP SEQUENCE (IF EXISTS)? (
        COMMA? (databaseName = id_ DOT)? (schemaName = id_ DOT)? sequenceName = id_
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-server-audit-transact-sql
dropServerAudit
    : DROP SERVER AUDIT auditName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-server-audit-specification-transact-sql
dropServerAuditSpecification
    : DROP SERVER AUDIT SPECIFICATION auditSpecificationName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-server-role-transact-sql
dropServerRole
    : DROP SERVER ROLE roleName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-service-transact-sql
dropService
    : DROP SERVICE droppedServiceName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-signature-transact-sql
dropSignature
    : DROP (COUNTER)? SIGNATURE FROM (schemaName = id_ DOT)? moduleName = id_ BY (
        COMMA? CERTIFICATE certName = id_
        | COMMA? ASYMMETRIC KEY AsymKeyName = id_
    )+
    ;

dropStatisticsNameAzureDwAndPdw
    : DROP STATISTICS (schemaName = id_ DOT)? objectName = id_ DOT statisticsName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-symmetric-key-transact-sql
dropSymmetricKey
    : DROP SYMMETRIC KEY symmetricKeyName = id_ (REMOVE PROVIDER KEY)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-synonym-transact-sql
dropSynonym
    : DROP SYNONYM (IF EXISTS)? (schema = id_ DOT)? synonymName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-user-transact-sql
dropUser
    : DROP USER (IF EXISTS)? userName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-workload-group-transact-sql
dropWorkloadGroup
    : DROP WORKLOAD GROUP groupName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-xml-schema-collection-transact-sql
dropXmlSchemaCollection
    : DROP XML SCHEMA COLLECTION (relationalSchema = id_ DOT)? sqlIdentifier = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/disable-trigger-transact-sql
disableTrigger
    : DISABLE TRIGGER (( COMMA? (schemaName = id_ DOT)? triggerName = id_)+ | ALL) ON (
        (schemaId = id_ DOT)? objectName = id_
        | DATABASE
        | ALL SERVER
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/enable-trigger-transact-sql
enableTrigger
    : ENABLE TRIGGER (( COMMA? (schemaName = id_ DOT)? triggerName = id_)+ | ALL) ON (
        (schemaId = id_ DOT)? objectName = id_
        | DATABASE
        | ALL SERVER
    )
    ;

lockTable
    : LOCK TABLE tableName IN (SHARE | EXCLUSIVE) MODE (WAIT seconds = INT | NOWAIT)? SEMI?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/truncate-table-transact-sql
truncateTable
    : TRUNCATE TABLE tableName (
        WITH LPAREN PARTITIONS LPAREN (COMMA? (INT | INT TO INT))+ RPAREN RPAREN
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-column-master-key-transact-sql
createColumnMasterKey
    : CREATE COLUMN MASTER KEY keyName = id_ WITH LPAREN KEY_STORE_PROVIDER_NAME EQ keyStoreProviderName = STRING COMMA KEY_PATH EQ
        keyPath = STRING RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-credential-transact-sql
alterCredential
    : ALTER CREDENTIAL credentialName = id_ WITH IDENTITY EQ identityName = STRING (
        COMMA SECRET EQ secret = STRING
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-credential-transact-sql
createCredential
    : CREATE CREDENTIAL credentialName = id_ WITH IDENTITY EQ identityName = STRING (
        COMMA SECRET EQ secret = STRING
    )? (FOR CRYPTOGRAPHIC PROVIDER cryptographicProviderName = id_)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-cryptographic-provider-transact-sql
alterCryptographicProvider
    : ALTER CRYPTOGRAPHIC PROVIDER providerName = id_ (
        FROM FILE EQ cryptoProviderDdlFile = STRING
    )? (ENABLE | DISABLE)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-cryptographic-provider-transact-sql
createCryptographicProvider
    : CREATE CRYPTOGRAPHIC PROVIDER providerName = id_ FROM FILE EQ pathOf_DLL = STRING
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/statements/create-endpoint-transact-sql?view=sql-server-ver16
createEndpoint
    : CREATE ENDPOINT endpointname = id_ (AUTHORIZATION login = id_)? (
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
        WINDOWS (NTLM | KERBEROS | NEGOTIATE)? (CERTIFICATE certName = id_)?
        | CERTIFICATE certName = id_ WINDOWS? (NTLM | KERBEROS | NEGOTIATE)?
    )
    ;

endpointListenerClause
    : LISTENER_PORT EQ port = INT (
        COMMA LISTENER_IP EQ (ALL | LPAREN (ipv4 = IPV4_ADDR | ipv6 = STRING) RPAREN)
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-event-notification-transact-sql
createEventNotification
    : CREATE EVENT NOTIFICATION eventNotificationName = id_ ON (
        SERVER
        | DATABASE
        | QUEUE queueName = id_
    ) (WITH FAN_IN)? FOR (COMMA? eventTypeOrGroup = id_)+ TO SERVICE brokerService = STRING COMMA brokerServiceSpecifierOrCurrentDatabase =
        STRING
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-event-session-transact-sql
// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-event-session-transact-sql
// todo: not implemented
createOrAlterEventSession
    : (CREATE | ALTER) EVENT SESSION eventSessionName = id_ ON SERVER (
        COMMA? ADD EVENT (
            (eventModuleGuid = id_ DOT)? eventPackageName = id_ DOT eventName = id_
        ) (
            LPAREN (SET ( COMMA? eventCustomizableAttributue = id_ EQ (INT | STRING))*)? (
                ACTION LPAREN (
                    COMMA? (eventModuleGuid = id_ DOT)? eventPackageName = id_ DOT actionName = id_
                )+ RPAREN
            )+ (WHERE eventSessionPredicateExpression)? RPAREN
        )*
    )* (
        COMMA? DROP EVENT (eventModuleGuid = id_ DOT)? eventPackageName = id_ DOT eventName = id_
    )* (
        (ADD TARGET (eventModuleGuid = id_ DOT)? eventPackageName = id_ DOT targetName = id_) (
            LPAREN SET (
                COMMA? targetParameterName = id_ EQ (LPAREN? INT RPAREN? | STRING)
            )+ RPAREN
        )*
    )* (DROP TARGET (eventModuleGuid = id_ DOT)? eventPackageName = id_ DOT targetName = id_)* (
        WITH LPAREN (COMMA? MAX_MEMORY EQ maxMemory = INT (KB | MB))? (
            COMMA? EVENT_RETENTION_MODE EQ (
                ALLOW_SINGLE_EVENT_LOSS
                | ALLOW_MULTIPLE_EVENT_LOSS
                | NO_EVENT_LOSS
            )
        )? (
            COMMA? MAX_DISPATCH_LATENCY EQ (
                maxDispatchLatencySeconds = INT SECONDS
                | INFINITE
            )
        )? (COMMA? MAX_EVENT_SIZE EQ maxEventSize = INT (KB | MB))? (
            COMMA? MEMORY_PARTITION_MODE EQ (NONE | PER_NODE | PER_CPU)
        )? (COMMA? TRACK_CAUSALITY EQ (ON | OFF))? (COMMA? STARTUP_STATE EQ (ON | OFF))? RPAREN
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
        eventFieldName = id_
        | (
            eventFieldName = id_
            | (
                (eventModuleGuid = id_ DOT)? eventPackageName = id_ DOT predicateSourceName = id_
            )
        ) (
            EQ
            | (LT GT)
            | (BANG EQ)
            | GT
            | (GT EQ)
            | LT
            | LT EQ
        ) (INT | STRING)
    )
    | (eventModuleGuid = id_ DOT)? eventPackageName = id_ DOT predicateCompareName = id_ LPAREN (
        eventFieldName = id_
        | ((eventModuleGuid = id_ DOT)? eventPackageName = id_ DOT predicateSourceName = id_) COMMA (
            INT
            | STRING
        )
    ) RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-external-data-source-transact-sql
alterExternalDataSource
    : ALTER EXTERNAL DATA SOURCE dataSourceName = id_ SET (
        LOCATION EQ location = STRING COMMA?
        | RESOURCE_MANAGER_LOCATION EQ resourceManagerLocation = STRING COMMA?
        | CREDENTIAL EQ credentialName = id_
    )+
    | ALTER EXTERNAL DATA SOURCE dataSourceName = id_ WITH LPAREN TYPE EQ BLOB_STORAGE COMMA LOCATION EQ location = STRING (
        COMMA CREDENTIAL EQ credentialName = id_
    )? RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-external-library-transact-sql
alterExternalLibrary
    : ALTER EXTERNAL LIBRARY libraryName = id_ (AUTHORIZATION ownerName = id_)? (SET | ADD) (
        LPAREN CONTENT EQ (clientLibrary = STRING | HEX | NONE) (
            COMMA PLATFORM EQ (WINDOWS | LINUX)? RPAREN
        ) WITH (
            COMMA? LANGUAGE EQ (R | PYTHON)
            | DATA_SOURCE EQ externalDataSourceName = id_
        )+ RPAREN
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-external-library-transact-sql
createExternalLibrary
    : CREATE EXTERNAL LIBRARY libraryName = id_ (AUTHORIZATION ownerName = id_)? FROM (
        COMMA? LPAREN? (CONTENT EQ)? (clientLibrary = STRING | HEX | NONE) (
            COMMA PLATFORM EQ (WINDOWS | LINUX)? RPAREN
        )?
    ) (
        WITH (
            COMMA? LANGUAGE EQ (R | PYTHON)
            | DATA_SOURCE EQ externalDataSourceName = id_
        )+ RPAREN
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-external-resource-pool-transact-sql
alterExternalResourcePool
    : ALTER EXTERNAL RESOURCE POOL (poolName = id_ | DEFAULT_DOUBLE_QUOTE) WITH LPAREN MAX_CPU_PERCENT EQ maxCpuPercent = INT (
        COMMA? AFFINITY CPU EQ (AUTO | (COMMA? INT TO INT | COMMA INT)+)
        | NUMANODE EQ (COMMA? INT TO INT | COMMA? INT)+
    ) (COMMA? MAX_MEMORY_PERCENT EQ maxMemoryPercent = INT)? (
        COMMA? MAX_PROCESSES EQ maxProcesses = INT
    )? RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-external-resource-pool-transact-sql
createExternalResourcePool
    : CREATE EXTERNAL RESOURCE POOL poolName = id_ WITH LPAREN MAX_CPU_PERCENT EQ maxCpuPercent = INT (
        COMMA? AFFINITY CPU EQ (AUTO | (COMMA? INT TO INT | COMMA INT)+)
        | NUMANODE EQ (COMMA? INT TO INT | COMMA? INT)+
    ) (COMMA? MAX_MEMORY_PERCENT EQ maxMemoryPercent = INT)? (
        COMMA? MAX_PROCESSES EQ maxProcesses = INT
    )? RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-fulltext-catalog-transact-sql
alterFulltextCatalog
    : ALTER FULLTEXT CATALOG catalogName = id_ (
        REBUILD (WITH ACCENT_SENSITIVITY EQ (ON | OFF))?
        | REORGANIZE
        | AS DEFAULT
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-fulltext-catalog-transact-sql
createFulltextCatalog
    : CREATE FULLTEXT CATALOG catalogName = id_ (ON FILEGROUP filegroup = id_)? (
        IN PATH rootpath = STRING
    )? (WITH ACCENT_SENSITIVITY EQ (ON | OFF))? (AS DEFAULT)? (AUTHORIZATION ownerName = id_)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-fulltext-stoplist-transact-sql
alterFulltextStoplist
    : ALTER FULLTEXT STOPLIST stoplistName = id_ (
        ADD stopword = STRING LANGUAGE (STRING | INT | HEX)
        | DROP (
            stopword = STRING LANGUAGE (STRING | INT | HEX)
            | ALL (STRING | INT | HEX)
            | ALL
        )
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-fulltext-stoplist-transact-sql
createFulltextStoplist
    : CREATE FULLTEXT STOPLIST stoplistName = id_ (
        FROM ((databaseName = id_ DOT)? sourceStoplistName = id_ | SYSTEM STOPLIST)
    )? (AUTHORIZATION ownerName = id_)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-login-transact-sql
alterLoginSqlServer
    : ALTER LOGIN loginName = id_ (
        (ENABLE | DISABLE)?
        | WITH (
            (PASSWORD EQ ( password = STRING | passwordHash = HEX HASHED)) (
                MUST_CHANGE
                | UNLOCK
            )*
        )? (OLD_PASSWORD EQ oldPassword = STRING (MUST_CHANGE | UNLOCK)*)? (
            DEFAULT_DATABASE EQ defaultDatabase = id_
        )? (DEFAULT_LANGUAGE EQ defaultLaguage = id_)? (NAME EQ loginName = id_)? (
            CHECK_POLICY EQ (ON | OFF)
        )? (CHECK_EXPIRATION EQ (ON | OFF))? (CREDENTIAL EQ credentialName = id_)? (
            NO CREDENTIAL
        )?
        | (ADD | DROP) CREDENTIAL credentialName = id_
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-login-transact-sql
createLoginSqlServer
    : CREATE LOGIN loginName = id_ (
        WITH (
            (PASSWORD EQ ( password = STRING | passwordHash = HEX HASHED)) (
                MUST_CHANGE
                | UNLOCK
            )*
        )? (COMMA? SID EQ sid = HEX)? (COMMA? DEFAULT_DATABASE EQ defaultDatabase = id_)? (
            COMMA? DEFAULT_LANGUAGE EQ defaultLaguage = id_
        )? (COMMA? CHECK_EXPIRATION EQ (ON | OFF))? (COMMA? CHECK_POLICY EQ (ON | OFF))? (
            COMMA? CREDENTIAL EQ credentialName = id_
        )?
        | (
            FROM (
                WINDOWS (
                    WITH (COMMA? DEFAULT_DATABASE EQ defaultDatabase = id_)? (
                        COMMA? DEFAULT_LANGUAGE EQ defaultLanguage = STRING
                    )?
                )
                | CERTIFICATE certname = id_
                | ASYMMETRIC KEY asymKeyName = id_
            )
        )
    )
    ;

alterLoginAzureSql
    : ALTER LOGIN loginName = id_ (
        (ENABLE | DISABLE)?
        | WITH (
            PASSWORD EQ password = STRING (OLD_PASSWORD EQ oldPassword = STRING)?
            | NAME EQ loginName = id_
        )
    )
    ;

createLoginAzureSql
    : CREATE LOGIN loginName = id_ WITH PASSWORD EQ STRING (SID EQ sid = HEX)?
    ;

alterLoginAzureSqlDwAndPdw
    : ALTER LOGIN loginName = id_ (
        (ENABLE | DISABLE)?
        | WITH (
            PASSWORD EQ password = STRING (
                OLD_PASSWORD EQ oldPassword = STRING (MUST_CHANGE | UNLOCK)*
            )?
            | NAME EQ loginName = id_
        )
    )
    ;

createLoginPdw
    : CREATE LOGIN loginName = id_ (
        WITH (PASSWORD EQ password = STRING (MUST_CHANGE)? (CHECK_POLICY EQ (ON | OFF)?)?)
        | FROM WINDOWS
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-master-key-transact-sql
alterMasterKeySqlServer
    : ALTER MASTER KEY (
        (FORCE)? REGENERATE WITH ENCRYPTION BY PASSWORD EQ password = STRING
        | (ADD | DROP) ENCRYPTION BY (
            SERVICE MASTER KEY
            | PASSWORD EQ encryptionPassword = STRING
        )
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-master-key-transact-sql
createMasterKeySqlServer
    : CREATE MASTER KEY ENCRYPTION BY PASSWORD EQ password = STRING
    ;

alterMasterKeyAzureSql
    : ALTER MASTER KEY (
        (FORCE)? REGENERATE WITH ENCRYPTION BY PASSWORD EQ password = STRING
        | ADD ENCRYPTION BY (SERVICE MASTER KEY | PASSWORD EQ encryptionPassword = STRING)
        | DROP ENCRYPTION BY PASSWORD EQ encryptionPassword = STRING
    )
    ;

createMasterKeyAzureSql
    : CREATE MASTER KEY (ENCRYPTION BY PASSWORD EQ password = STRING)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-message-type-transact-sql
alterMessageType
    : ALTER MESSAGE TYPE messageTypeName = id_ VALIDATION EQ (
        NONE
        | EMPTY
        | WELL_FORMED_XML
        | VALID_XML WITH SCHEMA COLLECTION schemaCollectionName = id_
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-partition-function-transact-sql
alterPartitionFunction
    : ALTER PARTITION FUNCTION partitionFunctionName = id_ LPAREN RPAREN (SPLIT | MERGE) RANGE LPAREN INT RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-partition-scheme-transact-sql
alterPartitionScheme
    : ALTER PARTITION SCHEME partitionSchemeName = id_ NEXT USED (fileGroupName = id_)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-remote-service-binding-transact-sql
alterRemoteServiceBinding
    : ALTER REMOTE SERVICE BINDING bindingName = id_ WITH (USER EQ userName = id_)? (
        COMMA ANONYMOUS EQ (ON | OFF)
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-remote-service-binding-transact-sql
createRemoteServiceBinding
    : CREATE REMOTE SERVICE BINDING bindingName = id_ (AUTHORIZATION ownerName = id_)? TO SERVICE remoteServiceName = STRING WITH (
        USER EQ userName = id_
    )? (COMMA ANONYMOUS EQ (ON | OFF))?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-resource-pool-transact-sql
createResourcePool
    : CREATE RESOURCE POOL poolName = id_ (
        WITH LPAREN (COMMA? MIN_CPU_PERCENT EQ INT)? (
            COMMA? MAX_CPU_PERCENT EQ INT
        )? (COMMA? CAP_CPU_PERCENT EQ INT)? (
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

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-resource-governor-transact-sql
alterResourceGovernor
    : ALTER RESOURCE GOVERNOR (
        (DISABLE | RECONFIGURE)
        | WITH LPAREN CLASSIFIER_FUNCTION EQ (
            schemaName = id_ DOT functionName = id_
            | NULL_
        ) RPAREN
        | RESET STATISTICS
        | WITH LPAREN MAX_OUTSTANDING_IO_PER_VOLUME EQ maxOutstandingIoPerVolume = INT RPAREN
    )
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-database-audit-specification-transact-sql?view=sql-server-ver16
alterDatabaseAuditSpecification
    : ALTER DATABASE AUDIT SPECIFICATION auditSpecificationName = id_ (
        FOR SERVER AUDIT auditName = id_
    )? (auditActionSpecGroup (COMMA auditActionSpecGroup)*)? (
        WITH LPAREN STATE EQ (ON | OFF) RPAREN
    )?
    ;

auditActionSpecGroup
    : (ADD | DROP) LPAREN (auditActionSpecification | auditActionGroupName = id_) RPAREN
    ;

auditActionSpecification
    : actionSpecification (COMMA actionSpecification)* ON (auditClassName COLON COLON)? auditSecurable BY principalId (
        COMMA principalId
    )*
    ;

actionSpecification
    : SELECT
    | INSERT
    | UPDATE
    | DELETE
    | EXECUTE
    | RECEIVE
    | REFERENCES
    ;

auditClassName
    : OBJECT
    | SCHEMA
    | TABLE
    ;

auditSecurable
    : ((id_ DOT)? id_ DOT)? id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-role-transact-sql
alterDbRole
    : ALTER ROLE roleName = id_ (
        (ADD | DROP) MEMBER databasePrincipal = id_
        | WITH NAME EQ newRoleName = id_
    )
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/statements/create-database-audit-specification-transact-sql?view=sql-server-ver16
createDatabaseAuditSpecification
    : CREATE DATABASE AUDIT SPECIFICATION auditSpecificationName = id_ (
        FOR SERVER AUDIT auditName = id_
    )? (auditActionSpecGroup (COMMA auditActionSpecGroup)*)? (
        WITH LPAREN STATE EQ (ON | OFF) RPAREN
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-role-transact-sql
createDbRole
    : CREATE ROLE roleName = id_ (AUTHORIZATION ownerName = id_)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-route-transact-sql
createRoute
    : CREATE ROUTE routeName = id_ (AUTHORIZATION ownerName = id_)? WITH (
        COMMA? SERVICE_NAME EQ routeServiceName = STRING
    )? (COMMA? BROKER_INSTANCE EQ brokerInstanceIdentifier = STRING)? (
        COMMA? LIFETIME EQ INT
    )? COMMA? ADDRESS EQ STRING (COMMA MIRROR_ADDRESS EQ STRING)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-rule-transact-sql
createRule
    : CREATE RULE (schemaName = id_ DOT)? ruleName = id_ AS searchCondition
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-schema-transact-sql
alterSchemaSql
    : ALTER SCHEMA schemaName = id_ TRANSFER (
        (OBJECT | TYPE | XML SCHEMA COLLECTION) DOUBLE_COLON
    )? id_ (DOT id_)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-schema-transact-sql
createSchema
    : CREATE SCHEMA (
        schemaName = id_
        | AUTHORIZATION ownerName = id_
        | schemaName = id_ AUTHORIZATION ownerName = id_
    ) (
        createTable
        | createView
        | (GRANT | DENY) (SELECT | INSERT | DELETE | UPDATE) ON (SCHEMA DOUBLE_COLON)? objectName = id_ TO ownerName = id_
        | REVOKE (SELECT | INSERT | DELETE | UPDATE) ON (SCHEMA DOUBLE_COLON)? objectName = id_ FROM ownerName = id_
    )*
    ;

createSchemaAzureSqlDwAndPdw
    : CREATE SCHEMA schemaName = id_ (AUTHORIZATION ownerName = id_)?
    ;

alterSchemaAzureSqlDwAndPdw
    : ALTER SCHEMA schemaName = id_ TRANSFER (OBJECT DOUBLE_COLON)? id_ (DOT ID)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-search-property-list-transact-sql
createSearchPropertyList
    : CREATE SEARCH PROPERTY LIST newListName = id_ (
        FROM (databaseName = id_ DOT)? sourceListName = id_
    )? (AUTHORIZATION ownerName = id_)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-security-policy-transact-sql
createSecurityPolicy
    : CREATE SECURITY POLICY (schemaName = id_ DOT)? securityPolicyName = id_ (
        COMMA? ADD (FILTER | BLOCK)? PREDICATE tvfSchemaName = id_ DOT securityPredicateFunctionName = id_ LPAREN (
            COMMA? columnNameOrArguments = id_
        )+ RPAREN ON tableSchemaName = id_ DOT name = id_ (
            COMMA? AFTER (INSERT | UPDATE)
            | COMMA? BEFORE (UPDATE | DELETE)
        )*
    )+ (WITH LPAREN STATE EQ (ON | OFF) (SCHEMABINDING (ON | OFF))? RPAREN)? (
        NOT FOR REPLICATION
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-sequence-transact-sql
alterSequence
    : ALTER SEQUENCE (schemaName = id_ DOT)? sequenceName = id_ (RESTART (WITH INT)?)? (
        INCREMENT BY sequnceIncrement = INT
    )? (MINVALUE INT | NO MINVALUE)? (MAXVALUE INT | NO MAXVALUE)? (CYCLE | NO CYCLE)? (
        CACHE INT
        | NO CACHE
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-sequence-transact-sql
createSequence
    : CREATE SEQUENCE (schemaName = id_ DOT)? sequenceName = id_ (AS dataType)? (
        START WITH INT
    )? (INCREMENT BY MINUS? INT)? (MINVALUE (MINUS? INT)? | NO MINVALUE)? (
        MAXVALUE (MINUS? INT)?
        | NO MAXVALUE
    )? (CYCLE | NO CYCLE)? (CACHE INT? | NO CACHE)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-server-audit-transact-sql
alterServerAudit
    : ALTER SERVER AUDIT auditName = id_ (
        (
            TO (
                FILE (
                    LPAREN (
                        COMMA? FILEPATH EQ filepath = STRING
                        | COMMA? MAXSIZE EQ ( INT (MB | GB | TB) | UNLIMITED)
                        | COMMA? MAX_ROLLOVER_FILES EQ maxRolloverFiles = (INT | UNLIMITED)
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
                | COMMA? ON_FAILURE EQ (CONTINUE | SHUTDOWN | FAIL_OPERATION)
                | COMMA? STATE EQ (ON | OFF)
            )* RPAREN
        )? (
            WHERE (
                COMMA? (NOT?) eventFieldName = id_ (
                    EQ
                    | (LT GT)
                    | (BANG EQ)
                    | GT
                    | (GT EQ)
                    | LT
                    | LT EQ
                ) (INT | STRING)
                | COMMA? (AND | OR) NOT? (
                    EQ
                    | (LT GT)
                    | (BANG EQ)
                    | GT
                    | (GT EQ)
                    | LT
                    | LT EQ
                ) (INT | STRING)
            )
        )?
        | REMOVE WHERE
        | MODIFY NAME EQ newAuditName = id_
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-server-audit-transact-sql
createServerAudit
    : CREATE SERVER AUDIT auditName = id_ (
        (
            TO (
                FILE (
                    LPAREN (
                        COMMA? FILEPATH EQ filepath = STRING
                        | COMMA? MAXSIZE EQ ( INT (MB | GB | TB) | UNLIMITED)
                        | COMMA? MAX_ROLLOVER_FILES EQ maxRolloverFiles = (INT | UNLIMITED)
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
                | COMMA? ON_FAILURE EQ (CONTINUE | SHUTDOWN | FAIL_OPERATION)
                | COMMA? STATE EQ (ON | OFF)
                | COMMA? AUDIT_GUID EQ auditGuid = id_
            )* RPAREN
        )? (
            WHERE (
                COMMA? (NOT?) eventFieldName = id_ (
                    EQ
                    | (LT GT)
                    | (BANG EQ)
                    | GT
                    | (GT EQ)
                    | LT
                    | LT EQ
                ) (INT | STRING)
                | COMMA? (AND | OR) NOT? (
                    EQ
                    | (LT GT)
                    | (BANG EQ)
                    | GT
                    | (GT EQ)
                    | LT
                    | LT EQ
                ) (INT | STRING)
            )
        )?
        | REMOVE WHERE
        | MODIFY NAME EQ newAuditName = id_
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-server-audit-specification-transact-sql

alterServerAuditSpecification
    : ALTER SERVER AUDIT SPECIFICATION auditSpecificationName = id_ (
        FOR SERVER AUDIT auditName = id_
    )? ((ADD | DROP) LPAREN auditActionGroupName = id_ RPAREN)* (
        WITH LPAREN STATE EQ (ON | OFF) RPAREN
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-server-audit-specification-transact-sql
createServerAuditSpecification
    : CREATE SERVER AUDIT SPECIFICATION auditSpecificationName = id_ (
        FOR SERVER AUDIT auditName = id_
    )? (ADD LPAREN auditActionGroupName = id_ RPAREN)* (
        WITH LPAREN STATE EQ (ON | OFF) RPAREN
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-server-configuration-transact-sql

alterServerConfiguration
    : ALTER SERVER CONFIGURATION SET (
        (
            PROCESS AFFINITY (
                CPU EQ (AUTO | (COMMA? INT | COMMA? INT TO INT)+)
                | NUMANODE EQ ( COMMA? INT | COMMA? INT TO INT)+
            )
            | DIAGNOSTICS LOG (
                ON
                | OFF
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

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-server-role-transact-sql
alterServerRole
    : ALTER SERVER ROLE serverRoleName = id_ (
        (ADD | DROP) MEMBER serverPrincipal = id_
        | WITH NAME EQ newServerRoleName = id_
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-server-role-transact-sql
createServerRole
    : CREATE SERVER ROLE serverRole = id_ (AUTHORIZATION serverPrincipal = id_)?
    ;

alterServerRolePdw
    : ALTER SERVER ROLE serverRoleName = id_ (ADD | DROP) MEMBER login = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-service-transact-sql
alterService
    : ALTER SERVICE modifiedServiceName = id_ (
        ON QUEUE (schemaName = id_ DOT)? queueName = id_
    )? (LPAREN optArgClause (COMMA optArgClause)* RPAREN)?
    ;

optArgClause
    : (ADD | DROP) CONTRACT modifiedContractName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-service-transact-sql
createService
    : CREATE SERVICE createServiceName = id_ (AUTHORIZATION ownerName = id_)? ON QUEUE (
        schemaName = id_ DOT
    )? queueName = id_ (LPAREN (COMMA? (id_ | DEFAULT))+ RPAREN)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-service-master-key-transact-sql

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

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-symmetric-key-transact-sql

alterSymmetricKey
    : ALTER SYMMETRIC KEY keyName = id_ (
        (ADD | DROP) ENCRYPTION BY (
            CERTIFICATE certificateName = id_
            | PASSWORD EQ password = STRING
            | SYMMETRIC KEY symmetricKeyName = id_
            | ASYMMETRIC KEY AsymKeyName = id_
        )
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-synonym-transact-sql
createSynonym
    : CREATE SYNONYM (schemaName_1 = id_ DOT)? synonymName = id_ FOR (
        (serverName = id_ DOT)? (databaseName = id_ DOT)? (schemaName_2 = id_ DOT)? objectName = id_
        | (databaseOrSchema2 = id_ DOT)? (schemaId_2_orObjectName = id_ DOT)?
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-user-transact-sql
alterUser
    : ALTER USER username = id_ WITH (
        COMMA? NAME EQ newusername = id_
        | COMMA? DEFAULT_SCHEMA EQ ( schemaName = id_ | NULL_)
        | COMMA? LOGIN EQ loginame = id_
        | COMMA? PASSWORD EQ STRING (OLD_PASSWORD EQ STRING)+
        | COMMA? DEFAULT_LANGUAGE EQ (NONE | lcid = INT | languageNameOrAlias = id_)
        | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ (ON | OFF)
    )+
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-user-transact-sql
createUser
    : CREATE USER userName = id_ ((FOR | FROM) LOGIN loginName = id_)? (
        WITH (
            COMMA? DEFAULT_SCHEMA EQ schemaName = id_
            | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ (ON | OFF)
        )*
    )?
    | CREATE USER (
        windowsPrincipal = id_ (
            WITH (
                COMMA? DEFAULT_SCHEMA EQ schemaName = id_
                | COMMA? DEFAULT_LANGUAGE EQ (NONE | INT | languageNameOrAlias = id_)
                | COMMA? SID EQ HEX
                | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ (ON | OFF)
            )*
        )?
        | userName = id_ WITH PASSWORD EQ password = STRING (
            COMMA? DEFAULT_SCHEMA EQ schemaName = id_
            | COMMA? DEFAULT_LANGUAGE EQ (NONE | INT | languageNameOrAlias = id_)
            | COMMA? SID EQ HEX
            | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ (ON | OFF)
        )*
        | Azure_Active_DirectoryPrincipal = id_ FROM EXTERNAL PROVIDER
    )
    | CREATE USER userName = id_ (
        WITHOUT LOGIN (
            COMMA? DEFAULT_SCHEMA EQ schemaName = id_
            | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ (ON | OFF)
        )*
        | (FOR | FROM) CERTIFICATE certName = id_
        | (FOR | FROM) ASYMMETRIC KEY asymKeyName = id_
    )
    | CREATE USER userName = id_
    ;

createUserAzureSqlDw
    : CREATE USER userName = id_ ((FOR | FROM) LOGIN loginName = id_ | WITHOUT LOGIN)? (
        WITH DEFAULT_SCHEMA EQ schemaName = id_
    )?
    | CREATE USER Azure_Active_DirectoryPrincipal = id_ FROM EXTERNAL PROVIDER (
        WITH DEFAULT_SCHEMA EQ schemaName = id_
    )?
    ;

alterUserAzureSql
    : ALTER USER username = id_ WITH (
        COMMA? NAME EQ newusername = id_
        | COMMA? DEFAULT_SCHEMA EQ schemaName = id_
        | COMMA? LOGIN EQ loginame = id_
        | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ (ON | OFF)
    )+
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-workload-group-transact-sql

alterWorkloadGroup
    : ALTER WORKLOAD GROUP (workloadGroupGroupName = id_ | DEFAULT_DOUBLE_QUOTE) (
        WITH LPAREN (
            IMPORTANCE EQ (LOW | MEDIUM | HIGH)
            | COMMA? REQUEST_MAX_MEMORY_GRANT_PERCENT EQ requestMaxMemoryGrant = INT
            | COMMA? REQUEST_MAX_CPU_TIME_SEC EQ requestMaxCpuTimeSec = INT
            | REQUEST_MEMORY_GRANT_TIMEOUT_SEC EQ requestMemoryGrantTimeoutSec = INT
            | MAX_DOP EQ maxDop = INT
            | GROUP_MAX_REQUESTS EQ groupMaxRequests = INT
        )+ RPAREN
    )? (USING (workloadGroupPoolName = id_ | DEFAULT_DOUBLE_QUOTE))?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-workload-group-transact-sql
createWorkloadGroup
    : CREATE WORKLOAD GROUP workloadGroupGroupName = id_ (
        WITH LPAREN (
            IMPORTANCE EQ (LOW | MEDIUM | HIGH)
            | COMMA? REQUEST_MAX_MEMORY_GRANT_PERCENT EQ requestMaxMemoryGrant = INT
            | COMMA? REQUEST_MAX_CPU_TIME_SEC EQ requestMaxCpuTimeSec = INT
            | REQUEST_MEMORY_GRANT_TIMEOUT_SEC EQ requestMemoryGrantTimeoutSec = INT
            | MAX_DOP EQ maxDop = INT
            | GROUP_MAX_REQUESTS EQ groupMaxRequests = INT
        )+ RPAREN
    )? (
        USING (workloadGroupPoolName = id_ | DEFAULT_DOUBLE_QUOTE)? (
            COMMA? EXTERNAL externalPoolName = id_
            | DEFAULT_DOUBLE_QUOTE
        )?
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-xml-schema-collection-transact-sql
createXmlSchemaCollection
    : CREATE XML SCHEMA COLLECTION (relationalSchema = id_ DOT)? sqlIdentifier = id_ AS (
        STRING
        | id_
        | LOCAL_ID
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-partition-function-transact-sql?view=sql-server-ver15
createPartitionFunction
    : CREATE PARTITION FUNCTION partitionFunctionName = id_ LPAREN inputParameterType = dataType RPAREN AS RANGE (
        LEFT
        | RIGHT
    )? FOR VALUES LPAREN boundaryValues = expressionList_ RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-partition-scheme-transact-sql?view=sql-server-ver15
createPartitionScheme
    : CREATE PARTITION SCHEME partitionSchemeName = id_ AS PARTITION partitionFunctionName = id_ ALL? TO LPAREN fileGroupNames += id_ (
        COMMA fileGroupNames += id_
    )* RPAREN
    ;

createQueue
    : CREATE QUEUE (fullTableName | queueName = id_) queueSettings? (
        ON filegroup = id_
        | DEFAULT
    )?
    ;

queueSettings
    : WITH (STATUS EQ onOff COMMA?)? (RETENTION EQ onOff COMMA?)? (
        ACTIVATION LPAREN (
            (
                (STATUS EQ onOff COMMA?)? (
                    PROCEDURE_NAME EQ funcProcNameDatabaseSchema COMMA?
                )? (MAX_QUEUE_READERS EQ maxReaders = INT COMMA?)? (
                    EXECUTE AS (SELF | userName = STRING | OWNER) COMMA?
                )?
            )
            | DROP
        ) RPAREN COMMA?
    )? (POISON_MESSAGE_HANDLING LPAREN (STATUS EQ onOff) RPAREN)?
    ;

alterQueue
    : ALTER QUEUE (fullTableName | queueName = id_) (queueSettings | queueAction)
    ;

queueAction
    : REBUILD (WITH LPAREN queueRebuildOptions RPAREN)?
    | REORGANIZE (WITH LOB_COMPACTION EQ onOff)?
    | MOVE TO (id_ | DEFAULT)
    ;

queueRebuildOptions
    : MAXDOP EQ INT
    ;

createContract
    : CREATE CONTRACT contractName (AUTHORIZATION ownerName = id_)? LPAREN (
        (messageTypeName = id_ | DEFAULT) SENT BY (INITIATOR | TARGET | ANY) COMMA?
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
    : CREATE MESSAGE TYPE messageTypeName = id_ (AUTHORIZATION ownerName = id_)? (
        VALIDATION EQ (
            NONE
            | EMPTY
            | WELL_FORMED_XML
            | VALID_XML WITH SCHEMA COLLECTION schemaCollectionName = id_
        )
    )
    ;

// DML

// https://docs.microsoft.com/en-us/sql/t-sql/statements/merge-transact-sql
// note that there's a limit on number of whenMatches but it has to be done runtime due to different ordering of statements allowed
mergeStatement
    : withExpression? MERGE (TOP LPAREN expression RPAREN PERCENT?)? INTO? ddlObject withTableHints? asTableAlias? USING tableSources ON
        searchCondition whenMatches+ outputClause? optionClause? SEMI
    ;

whenMatches
    : (WHEN MATCHED (AND searchCondition)? THEN mergeMatched)+
    | (WHEN NOT MATCHED (BY TARGET)? (AND searchCondition)? THEN mergeNotMatched)
    | (WHEN NOT MATCHED BY SOURCE (AND searchCondition)? THEN mergeMatched)+
    ;

mergeMatched
    : UPDATE SET updateElemMerge (COMMA updateElemMerge)*
    | DELETE
    ;

mergeNotMatched
    : INSERT (LPAREN columnNameList RPAREN)? (tableValueConstructor | DEFAULT VALUES)
    ;

// https://msdn.microsoft.com/en-us/library/ms189835.aspx
deleteStatement
    : withExpression? DELETE (TOP LPAREN expression RPAREN PERCENT? | TOP INT)? FROM? deleteStatementFrom withTableHints? outputClause? (
        FROM tableSources
    )? (WHERE (searchCondition | CURRENT OF (GLOBAL? cursorName | cursorVar = LOCAL_ID)))? forClause? optionClause? SEMI?
    ;

deleteStatementFrom
    : ddlObject
    | rowsetFunctionLimited
    | tableVar = LOCAL_ID
    ;

// https://msdn.microsoft.com/en-us/library/ms174335.aspx
insertStatement
    : withExpression? INSERT (TOP LPAREN expression RPAREN PERCENT?)? INTO? (
        ddlObject
        | rowsetFunctionLimited
    ) withTableHints? (LPAREN insertColumnNameList RPAREN)? outputClause? insertStatementValue forClause? optionClause? SEMI?
    ;

insertStatementValue
    : tableValueConstructor
    | derivedTable
    | executeStatement
    | DEFAULT VALUES
    ;

receiveStatement
    : LPAREN? RECEIVE (ALL | DISTINCT | topClause | STAR) (LOCAL_ID EQ expression COMMA?)* FROM fullTableName (
        INTO tableVariable = id_ (WHERE where = searchCondition)
    )? RPAREN?
    ;

// https://msdn.microsoft.com/en-us/library/ms189499.aspx
selectStatementStandalone
    : withExpression? selectStatement
    ;

selectStatement
    : queryExpression selectOrderByClause? forClause? optionClause? SEMI?
    ;

time
    : (LOCAL_ID | constant)
    ;

// https://msdn.microsoft.com/en-us/library/ms177523.aspx
updateStatement
    : withExpression? UPDATE (TOP LPAREN expression RPAREN PERCENT?)? (
        ddlObject
        | rowsetFunctionLimited
    ) withTableHints? SET updateElem (COMMA updateElem)* outputClause? (FROM tableSources)? (
        WHERE (searchCondition | CURRENT OF (GLOBAL? cursorName | cursorVar = LOCAL_ID))
    )? forClause? optionClause? SEMI?
    ;

// https://msdn.microsoft.com/en-us/library/ms177564.aspx
outputClause
    : OUTPUT outputDmlListElem (COMMA outputDmlListElem)* (
        INTO (LOCAL_ID | tableName) (LPAREN columnNameList RPAREN)?
    )?
    ;

outputDmlListElem
    : (expression | asterisk) asColumnAlias?
    ;

// DDL

// https://msdn.microsoft.com/en-ie/library/ms176061.aspx
createDatabase
    : CREATE DATABASE (database = id_) (CONTAINMENT EQ ( NONE | PARTIAL))? (
        ON PRIMARY? databaseFileSpec ( COMMA databaseFileSpec)*
    )? (LOG ON databaseFileSpec ( COMMA databaseFileSpec)*)? (COLLATE collationName = id_)? (
        WITH createDatabaseOption ( COMMA createDatabaseOption)*
    )?
    ;

// https://msdn.microsoft.com/en-us/library/ms188783.aspx
createIndex
    : CREATE UNIQUE? clustered? INDEX id_ ON tableName LPAREN columnNameListWithOrder RPAREN (
        INCLUDE LPAREN columnNameList RPAREN
    )? (WHERE where = searchCondition)? (createIndexOptions)? (ON id_)? SEMI?
    ;

createIndexOptions
    : WITH LPAREN relationalIndexOption (COMMA relationalIndexOption)* RPAREN
    ;

relationalIndexOption
    : rebuildIndexOption
    | DROP_EXISTING EQ onOff
    | OPTIMIZE_FOR_SEQUENTIAL_KEY EQ onOff
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-index-transact-sql
alterIndex
    : ALTER INDEX (id_ | ALL) ON tableName (
        DISABLE
        | PAUSE
        | ABORT
        | RESUME resumableIndexOptions?
        | reorganizePartition
        | setIndexOptions
        | rebuildPartition
    )
    ;

resumableIndexOptions
    : WITH LPAREN (resumableIndexOption (COMMA resumableIndexOption)*) RPAREN
    ;

resumableIndexOption
    : MAXDOP EQ maxDegreeOfParallelism = INT
    | MAX_DURATION EQ maxDuration = INT MINUTES?
    | lowPriorityLockWait
    ;

reorganizePartition
    : REORGANIZE (PARTITION EQ INT)? reorganizeOptions?
    ;

reorganizeOptions
    : WITH LPAREN (reorganizeOption (COMMA reorganizeOption)*) RPAREN
    ;

reorganizeOption
    : LOB_COMPACTION EQ onOff
    | COMPRESS_ALL_ROW_GROUPS EQ onOff
    ;

setIndexOptions
    : SET LPAREN setIndexOption (COMMA setIndexOption)* RPAREN
    ;

setIndexOption
    : ALLOW_ROW_LOCKS EQ onOff
    | ALLOW_PAGE_LOCKS EQ onOff
    | OPTIMIZE_FOR_SEQUENTIAL_KEY EQ onOff
    | IGNORE_DUP_KEY EQ onOff
    | STATISTICS_NORECOMPUTE EQ onOff
    | COMPRESSION_DELAY EQ delay = INT MINUTES?
    ;

rebuildPartition
    : REBUILD (PARTITION EQ ALL)? rebuildIndexOptions?
    | REBUILD PARTITION EQ INT singlePartitionRebuildIndexOptions?
    ;

rebuildIndexOptions
    : WITH LPAREN rebuildIndexOption (COMMA rebuildIndexOption)* RPAREN
    ;

rebuildIndexOption
    : PAD_INDEX EQ onOff
    | FILLFACTOR EQ INT
    | SORT_IN_TEMPDB EQ onOff
    | IGNORE_DUP_KEY EQ onOff
    | STATISTICS_NORECOMPUTE EQ onOff
    | STATISTICS_INCREMENTAL EQ onOff
    | ONLINE EQ (ON (LPAREN lowPriorityLockWait RPAREN)? | OFF)
    | RESUMABLE EQ onOff
    | MAX_DURATION EQ times = INT MINUTES?
    | ALLOW_ROW_LOCKS EQ onOff
    | ALLOW_PAGE_LOCKS EQ onOff
    | MAXDOP EQ maxDegreeOfParallelism = INT
    | DATA_COMPRESSION EQ (NONE | ROW | PAGE | COLUMNSTORE | COLUMNSTORE_ARCHIVE) onPartitions?
    | XML_COMPRESSION EQ onOff onPartitions?
    ;

singlePartitionRebuildIndexOptions
    : WITH LPAREN singlePartitionRebuildIndexOption (COMMA singlePartitionRebuildIndexOption)* RPAREN
    ;

singlePartitionRebuildIndexOption
    : SORT_IN_TEMPDB EQ onOff
    | MAXDOP EQ maxDegreeOfParallelism = INT
    | RESUMABLE EQ onOff
    | DATA_COMPRESSION EQ (NONE | ROW | PAGE | COLUMNSTORE | COLUMNSTORE_ARCHIVE) onPartitions?
    | XML_COMPRESSION EQ onOff onPartitions?
    | ONLINE EQ (ON (LPAREN lowPriorityLockWait RPAREN)? | OFF)
    ;

onPartitions
    : ON PARTITIONS LPAREN partitionNumber = INT (TO toPartitionNumber = INT)? (
        COMMA partitionNumber = INT (TO toPartitionNumber = INT)?
    )* RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-columnstore-index-transact-sql?view=sql-server-ver15
createColumnstoreIndex
    : CREATE CLUSTERED COLUMNSTORE INDEX id_ ON tableName createColumnstoreIndexOptions? (
        ON id_
    )? SEMI?
    ;

createColumnstoreIndexOptions
    : WITH LPAREN columnstoreIndexOption (COMMA columnstoreIndexOption)* RPAREN
    ;

columnstoreIndexOption
    : DROP_EXISTING EQ onOff
    | MAXDOP EQ maxDegreeOfParallelism = INT
    | ONLINE EQ onOff
    | COMPRESSION_DELAY EQ delay = INT MINUTES?
    | DATA_COMPRESSION EQ (COLUMNSTORE | COLUMNSTORE_ARCHIVE) onPartitions?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-columnstore-index-transact-sql?view=sql-server-ver15
createNonclusteredColumnstoreIndex
    : CREATE NONCLUSTERED? COLUMNSTORE INDEX id_ ON tableName LPAREN columnNameListWithOrder RPAREN (
        WHERE searchCondition
    )? createColumnstoreIndexOptions? (ON id_)? SEMI?
    ;

createXmlIndex
    : CREATE PRIMARY? XML INDEX id_ ON tableName LPAREN id_ RPAREN (
        USING XML INDEX id_ (FOR (VALUE | PATH | PROPERTY)?)?
    )? xmlIndexOptions? SEMI?
    ;

xmlIndexOptions
    : WITH LPAREN xmlIndexOption (COMMA xmlIndexOption)* RPAREN
    ;

xmlIndexOption
    : PAD_INDEX EQ onOff
    | FILLFACTOR EQ INT
    | SORT_IN_TEMPDB EQ onOff
    | IGNORE_DUP_KEY EQ onOff
    | DROP_EXISTING EQ onOff
    | ONLINE EQ (ON (LPAREN lowPriorityLockWait RPAREN)? | OFF)
    | ALLOW_ROW_LOCKS EQ onOff
    | ALLOW_PAGE_LOCKS EQ onOff
    | MAXDOP EQ maxDegreeOfParallelism = INT
    | XML_COMPRESSION EQ onOff
    ;

// https://msdn.microsoft.com/en-us/library/ms187926(v=sql.120).aspx
createOrAlterProcedure
    : ((CREATE (OR (ALTER | REPLACE))?) | ALTER) proc = (PROC | PROCEDURE) procName = funcProcNameSchema (
        SEMI INT
    )? (LPAREN? procedureParam (COMMA procedureParam)* RPAREN?)? (
        WITH procedureOption (COMMA procedureOption)*
    )? (FOR REPLICATION)? AS (asExternalName | sqlClauses*)
    ;

asExternalName
    : EXTERNAL NAME assemblyName = id_ DOT className = id_ DOT methodName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-trigger-transact-sql
createOrAlterTrigger
    : createOrAlterDmlTrigger
    | createOrAlterDdlTrigger
    ;

createOrAlterDmlTrigger
    : (CREATE (OR (ALTER | REPLACE))? | ALTER) TRIGGER simpleName ON tableName (
        WITH dmlTriggerOption (COMMA dmlTriggerOption)*
    )? (FOR | AFTER | INSTEAD OF) dmlTriggerOperation (COMMA dmlTriggerOperation)* (WITH APPEND)? (
        NOT FOR REPLICATION
    )? AS sqlClauses+
    ;

dmlTriggerOption
    : ENCRYPTION
    | executeClause
    ;

dmlTriggerOperation
    : (INSERT | UPDATE | DELETE)
    ;

createOrAlterDdlTrigger
    : (CREATE (OR (ALTER | REPLACE))? | ALTER) TRIGGER simpleName ON (ALL SERVER | DATABASE) (
        WITH dmlTriggerOption (COMMA dmlTriggerOption)*
    )? (FOR | AFTER) ddlTriggerOperation (COMMA ddlTriggerOperation)* AS sqlClauses+
    ;

ddlTriggerOperation
    : simpleId
    ;

// https://msdn.microsoft.com/en-us/library/ms186755.aspx
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

procedureParamDefaultValue
    : NULL_
    | DEFAULT
    | constant
    | LOCAL_ID
    ;

procedureParam
    : LOCAL_ID AS? (typeSchema = id_ DOT)? dataType VARYING? (
        EQ defaultVal = procedureParamDefaultValue
    )? (OUT | OUTPUT | READONLY)?
    ;

procedureOption
    : ENCRYPTION
    | RECOMPILE
    | executeClause
    ;

functionOption
    : ENCRYPTION
    | SCHEMABINDING
    | RETURNS NULL_ ON NULL_ INPUT
    | CALLED ON NULL_ INPUT
    | executeClause
    ;

// https://msdn.microsoft.com/en-us/library/ms188038.aspx
createStatistics
    : CREATE STATISTICS id_ ON tableName LPAREN columnNameList RPAREN (
        WITH (FULLSCAN | SAMPLE INT (PERCENT | ROWS) | STATS_STREAM) (COMMA NORECOMPUTE)? (
            COMMA INCREMENTAL EQ onOff
        )?
    )? SEMI?
    ;

updateStatistics
    : UPDATE STATISTICS fullTableName (id_ | LPAREN id_ ( COMMA id_)* RPAREN)? updateStatisticsOptions?
    ;

updateStatisticsOptions
    : WITH updateStatisticsOption (COMMA updateStatisticsOption)*
    ;

updateStatisticsOption
    : (FULLSCAN (COMMA? PERSIST_SAMPLE_PERCENT EQ onOff)?)
    | (SAMPLE number = INT (PERCENT | ROWS) (COMMA? PERSIST_SAMPLE_PERCENT EQ onOff)?)
    | RESAMPLE onPartitions?
    | STATS_STREAM EQ statsStream_ = expression
    | ROWCOUNT EQ INT
    | PAGECOUNT EQ INT
    | ALL
    | COLUMNS
    | INDEX
    | NORECOMPUTE
    | INCREMENTAL EQ onOff
    | MAXDOP EQ maxDregreeOfParallelism = INT
    | AUTO_DROP EQ onOff
    ;

// https://msdn.microsoft.com/en-us/library/ms174979.aspx
createTable
    : CREATE TABLE tableName LPAREN columnDefTableConstraints (COMMA? tableIndices)* COMMA? RPAREN (
        LOCK simpleId
    )? tableOptions* (ON id_ | DEFAULT | onPartitionOrFilegroup)? (TEXTIMAGE_ON id_ | DEFAULT)? SEMI?
    ;

tableIndices
    : INDEX id_ UNIQUE? clustered? LPAREN columnNameListWithOrder RPAREN
    | INDEX id_ CLUSTERED COLUMNSTORE
    | INDEX id_ NONCLUSTERED? COLUMNSTORE LPAREN columnNameList RPAREN createTableIndexOptions? (
        ON id_
    )?
    ;

tableOptions
    : WITH (LPAREN tableOption (COMMA tableOption)* RPAREN | tableOption (COMMA tableOption)*)
    ;

tableOption
    : (simpleId | keyword) EQ (simpleId | keyword | onOff | INT)
    | CLUSTERED COLUMNSTORE INDEX
    | HEAP
    | FILLFACTOR EQ INT
    | DISTRIBUTION EQ HASH LPAREN id_ RPAREN
    | CLUSTERED INDEX LPAREN id_ (ASC | DESC)? (COMMA id_ (ASC | DESC)?)* RPAREN
    | DATA_COMPRESSION EQ (NONE | ROW | PAGE) onPartitions?
    | XML_COMPRESSION EQ onOff onPartitions?
    ;

createTableIndexOptions
    : WITH LPAREN createTableIndexOption (COMMA createTableIndexOption)* RPAREN
    ;

createTableIndexOption
    : PAD_INDEX EQ onOff
    | FILLFACTOR EQ INT
    | IGNORE_DUP_KEY EQ onOff
    | STATISTICS_NORECOMPUTE EQ onOff
    | STATISTICS_INCREMENTAL EQ onOff
    | ALLOW_ROW_LOCKS EQ onOff
    | ALLOW_PAGE_LOCKS EQ onOff
    | OPTIMIZE_FOR_SEQUENTIAL_KEY EQ onOff
    | DATA_COMPRESSION EQ (NONE | ROW | PAGE | COLUMNSTORE | COLUMNSTORE_ARCHIVE) onPartitions?
    | XML_COMPRESSION EQ onOff onPartitions?
    ;

// https://msdn.microsoft.com/en-us/library/ms187956.aspx
createView
    : (CREATE (OR (ALTER | REPLACE))? | ALTER) VIEW simpleName (LPAREN columnNameList RPAREN)? (
        WITH viewAttribute (COMMA viewAttribute)*
    )? AS selectStatementStandalone (WITH CHECK OPTION)? SEMI?
    ;

viewAttribute
    : ENCRYPTION
    | SCHEMABINDING
    | VIEW_METADATA
    ;

// https://msdn.microsoft.com/en-us/library/ms190273.aspx
alterTable
    : ALTER TABLE tableName (
        SET LPAREN LOCK_ESCALATION EQ (AUTO | TABLE | DISABLE) RPAREN
        | ADD columnDefTableConstraints
        | ALTER COLUMN (columnDefinition | columnModifier)
        | DROP COLUMN id_ (COMMA id_)*
        | DROP CONSTRAINT constraint = id_
        | WITH (CHECK | NOCHECK) ADD (CONSTRAINT constraint = id_)? (
            FOREIGN KEY LPAREN fk = columnNameList RPAREN REFERENCES tableName (
                LPAREN pk = columnNameList RPAREN
            )? (onDelete | onUpdate)*
            | CHECK LPAREN searchCondition RPAREN
        )
        | (NOCHECK | CHECK) CONSTRAINT constraint = id_
        | (ENABLE | DISABLE) TRIGGER id_?
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
    : WAIT_AT_LOW_PRIORITY LPAREN MAX_DURATION EQ maxDuration = time MINUTES? COMMA ABORT_AFTER_WAIT EQ abortAfterWait = (
        NONE
        | SELF
        | BLOCKERS
    ) RPAREN
    ;

// https://msdn.microsoft.com/en-us/library/ms174269.aspx
alterDatabase
    : ALTER DATABASE (database = id_ | CURRENT) (
        MODIFY NAME EQ newName = id_
        | COLLATE collation = id_
        | SET databaseOptionspec (WITH termination)?
        | addOrModifyFiles
        | addOrModifyFilegroups
    ) SEMI?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-database-transact-sql-file-and-filegroup-options?view=sql-server-ver15
addOrModifyFiles
    : ADD FILE fileSpec (COMMA fileSpec)* (TO FILEGROUP filegroupName = id_)?
    | ADD LOG FILE fileSpec (COMMA fileSpec)*
    | REMOVE FILE logicalFileName = id_
    | MODIFY FILE fileSpec
    ;

fileSpec
    : LPAREN NAME EQ name = idOrString (COMMA NEWNAME EQ newName = idOrString)? (
        COMMA FILENAME EQ fileName = STRING
    )? (COMMA SIZE EQ size = fileSize)? (COMMA MAXSIZE EQ (maxSize = fileSize) | UNLIMITED)? (
        COMMA FILEGROWTH EQ growthIncrement = fileSize
    )? (COMMA OFFLINE)? RPAREN
    ;

addOrModifyFilegroups
    : ADD FILEGROUP filegroupName = id_ (CONTAINS FILESTREAM | CONTAINS MEMORY_OPTIMIZED_DATA)?
    | REMOVE FILEGROUP filegrouName = id_
    | MODIFY FILEGROUP filegrouName = id_ (
        filegroupUpdatabilityOption
        | DEFAULT
        | NAME EQ newFilegroupName = id_
        | AUTOGROW_SINGLE_FILE
        | AUTOGROW_ALL_FILES
    )
    ;

filegroupUpdatabilityOption
    : READONLY
    | READWRITE
    | READ_ONLY
    | READ_WRITE
    ;

// https://msdn.microsoft.com/en-us/library/bb522682.aspx
// Runtime check.
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
    | parameterizationOption
    //  | queryStoreOptions
    | recoveryOption
    //  | remoteDataArchiveOption
    | serviceBrokerOption
    | snapshotOption
    | sqlOption
    | targetRecoveryTimeOption
    | termination
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
        | ON LPAREN (changeTrackingOptionList (COMMA changeTrackingOptionList)*)* RPAREN
    )
    ;

changeTrackingOptionList
    : AUTO_CLEANUP EQ onOff
    | CHANGE_RETENTION EQ INT ( DAYS | HOURS | MINUTES)
    ;

containmentOption
    : CONTAINMENT EQ (NONE | PARTIAL)
    ;

cursorOption
    : CURSOR_CLOSE_ON_COMMIT onOff
    | CURSOR_DEFAULT ( LOCAL | GLOBAL)
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-endpoint-transact-sql
alterEndpoint
    : ALTER ENDPOINT endpointname = id_ (AUTHORIZATION login = id_)? (
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

/* Will visit later
*/
databaseMirroringOption
    : mirroringSetOption
    ;

mirroringSetOption
    : mirroringPartner partnerOption
    | mirroringWitness witnessOption
    ;

mirroringPartner
    : PARTNER
    ;

mirroringWitness
    : WITNESS
    ;

witnessPartnerEqual
    : EQ
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

witnessOption
    : witnessPartnerEqual witnessServer
    | OFF
    ;

witnessServer
    : partnerServer
    ;

partnerServer
    : partnerServerTcpPrefix host mirroringHostPortSeperator portNumber
    ;

mirroringHostPortSeperator
    : COLON
    ;

partnerServerTcpPrefix
    : TCP COLON DOUBLE_FORWARD_SLASH
    ;

portNumber
    : port = INT
    ;

host
    : id_ DOT host
    | (id_ DOT | id_)
    ;

dateCorrelationOptimizationOption
    : DATE_CORRELATION_OPTIMIZATION onOff
    ;

dbEncryptionOption
    : ENCRYPTION onOff
    ;

dbStateOption
    : (ONLINE | OFFLINE | EMERGENCY)
    ;

dbUpdateOption
    : READ_ONLY
    | READ_WRITE
    ;

dbUserAccessOption
    : SINGLE_USER
    | RESTRICTED_USER
    | MULTI_USER
    ;

delayedDurabilityOption
    : DELAYED_DURABILITY EQ (DISABLED | ALLOWED | FORCED)
    ;

externalAccessOption
    : DB_CHAINING onOff
    | TRUSTWORTHY onOff
    | DEFAULT_LANGUAGE EQ ( id_ | STRING)
    | DEFAULT_FULLTEXT_LANGUAGE EQ ( id_ | STRING)
    | NESTED_TRIGGERS EQ ( OFF | ON)
    | TRANSFORM_NOISE_WORDS EQ ( OFF | ON)
    | TWO_DIGIT_YEAR_CUTOFF EQ INT
    ;

hadrOptions
    : HADR (( AVAILABILITY GROUP EQ availabilityGroupName = id_ | OFF) | (SUSPEND | RESUME))
    ;

mixedPageAllocationOption
    : MIXED_PAGE_ALLOCATION (OFF | ON)
    ;

parameterizationOption
    : PARAMETERIZATION (SIMPLE | FORCED)
    ;

recoveryOption
    : RECOVERY (FULL | BULK_LOGGED | SIMPLE)
    | TORN_PAGE_DETECTION onOff
    | ACCELERATED_DATABASE_RECOVERY EQ onOff
    | PAGE_VERIFY ( CHECKSUM | TORN_PAGE_DETECTION | NONE)
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

targetRecoveryTimeOption
    : TARGET_RECOVERY_TIME EQ INT (SECONDS | MINUTES)
    ;

termination
    : ROLLBACK AFTER seconds = INT
    | ROLLBACK IMMEDIATE
    | NO_WAIT
    ;

// https://msdn.microsoft.com/en-us/library/ms176118.aspx
dropIndex
    : DROP INDEX (IF EXISTS)? (
        dropRelationalOrXmlOrSpatialIndex (COMMA dropRelationalOrXmlOrSpatialIndex)*
        | dropBackwardCompatibleIndex (COMMA dropBackwardCompatibleIndex)*
    ) SEMI?
    ;

dropRelationalOrXmlOrSpatialIndex
    : indexName = id_ ON fullTableName
    ;

dropBackwardCompatibleIndex
    : (ownerName = id_ DOT)? tableOrViewName = id_ DOT indexName = id_
    ;

// https://msdn.microsoft.com/en-us/library/ms174969.aspx
dropProcedure
    : DROP proc = (PROC | PROCEDURE) (IF EXISTS)? funcProcNameSchema (COMMA funcProcNameSchema)* SEMI?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-trigger-transact-sql
dropTrigger
    : dropDmlTrigger
    | dropDdlTrigger
    ;

dropDmlTrigger
    : DROP TRIGGER (IF EXISTS)? simpleName (COMMA simpleName)* SEMI?
    ;

dropDdlTrigger
    : DROP TRIGGER (IF EXISTS)? simpleName (COMMA simpleName)* ON (DATABASE | ALL SERVER) SEMI?
    ;

// https://msdn.microsoft.com/en-us/library/ms190290.aspx
dropFunction
    : DROP FUNCTION (IF EXISTS)? funcProcNameSchema (COMMA funcProcNameSchema)* SEMI?
    ;

// https://msdn.microsoft.com/en-us/library/ms175075.aspx
dropStatistics
    : DROP STATISTICS (COMMA? (tableName DOT)? name = id_)+ SEMI
    ;

// https://msdn.microsoft.com/en-us/library/ms173790.aspx
dropTable
    : DROP TABLE (IF EXISTS)? tableName (COMMA tableName)* SEMI?
    ;

// https://msdn.microsoft.com/en-us/library/ms173492.aspx
dropView
    : DROP VIEW (IF EXISTS)? simpleName (COMMA simpleName)* SEMI?
    ;

createType
    : CREATE TYPE name = simpleName (FROM dataType nullNotnull?)? (
        AS TABLE LPAREN columnDefTableConstraints RPAREN
    )?
    ;

dropType
    : DROP TYPE (IF EXISTS)? name = simpleName
    ;

rowsetFunctionLimited
    : openquery
    | opendatasource
    ;

// https://msdn.microsoft.com/en-us/library/ms188427(v=sql.120).aspx
openquery
    : OPENQUERY LPAREN linkedServer = id_ COMMA query = STRING RPAREN
    ;

// https://msdn.microsoft.com/en-us/library/ms179856.aspx
opendatasource
    : OPENDATASOURCE LPAREN provider = STRING COMMA init = STRING RPAREN DOT (database = id_)? DOT (
        scheme = id_
    )? DOT (table = id_)
    ;

// Other statements.

// https://msdn.microsoft.com/en-us/library/ms188927.aspx
declareStatement
    : DECLARE LOCAL_ID AS? (dataType | tableTypeDefinition | tableName)
    | DECLARE loc += declareLocal (COMMA loc += declareLocal)*
    | DECLARE LOCAL_ID AS? xmlTypeDefinition
    | WITH XMLNAMESPACES LPAREN xmlDec += xmlDeclaration (COMMA xmlDec += xmlDeclaration)* RPAREN
    ;

xmlDeclaration
    : xmlNamespaceUri = STRING AS id_
    | DEFAULT STRING
    ;

// https://msdn.microsoft.com/en-us/library/ms181441(v=sql.120).aspx
cursorStatement
    // https://msdn.microsoft.com/en-us/library/ms175035(v=sql.120).aspx
    : CLOSE GLOBAL? cursorName SEMI?
    // https://msdn.microsoft.com/en-us/library/ms188782(v=sql.120).aspx
    | DEALLOCATE GLOBAL? CURSOR? cursorName SEMI?
    // https://msdn.microsoft.com/en-us/library/ms180169(v=sql.120).aspx
    | declareCursor
    // https://msdn.microsoft.com/en-us/library/ms180152(v=sql.120).aspx
    | fetchCursor
    // https://msdn.microsoft.com/en-us/library/ms190500(v=sql.120).aspx
    | OPEN GLOBAL? cursorName SEMI?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/backup-transact-sql
backupDatabase
    : BACKUP DATABASE (databaseName = id_) (
        READ_WRITE_FILEGROUPS (COMMA? (FILE | FILEGROUP) EQ fileOrFilegroup = STRING)*
    )? (COMMA? (FILE | FILEGROUP) EQ fileOrFilegroup = STRING)* (
        TO ( COMMA? logicalDeviceName = id_)+
        | TO ( COMMA? (DISK | TAPE | URL) EQ (STRING | id_))+
    ) (
        (MIRROR TO ( COMMA? logicalDeviceName = id_)+)+
        | ( MIRROR TO ( COMMA? (DISK | TAPE | URL) EQ (STRING | id_))+)+
    )? (
        WITH (
            COMMA? DIFFERENTIAL
            | COMMA? COPY_ONLY
            | COMMA? (COMPRESSION | NO_COMPRESSION)
            | COMMA? DESCRIPTION EQ (STRING | id_)
            | COMMA? NAME EQ backupSetName = id_
            | COMMA? CREDENTIAL
            | COMMA? FILE_SNAPSHOT
            | COMMA? (EXPIREDATE EQ (STRING | id_) | RETAINDAYS EQ (INT | id_))
            | COMMA? (NOINIT | INIT)
            | COMMA? (NOSKIP | SKIP_KEYWORD)
            | COMMA? (NOFORMAT | FORMAT)
            | COMMA? MEDIADESCRIPTION EQ (STRING | id_)
            | COMMA? MEDIANAME EQ (medianame = STRING)
            | COMMA? BLOCKSIZE EQ (INT | id_)
            | COMMA? BUFFERCOUNT EQ (INT | id_)
            | COMMA? MAXTRANSFER EQ (INT | id_)
            | COMMA? (NO_CHECKSUM | CHECKSUM)
            | COMMA? (STOP_ON_ERROR | CONTINUE_AFTER_ERROR)
            | COMMA? RESTART
            | COMMA? STATS (EQ statsPercent = INT)?
            | COMMA? (REWIND | NOREWIND)
            | COMMA? (LOAD | NOUNLOAD)
            | COMMA? ENCRYPTION LPAREN ALGORITHM EQ (
                AES_128
                | AES_192
                | AES_256
                | TRIPLE_DES_3KEY
            ) COMMA SERVER CERTIFICATE EQ (
                encryptorName = id_
                | SERVER ASYMMETRIC KEY EQ encryptorName = id_
            )
        )*
    )?
    ;

backupLog
    : BACKUP LOG (databaseName = id_) (
        TO ( COMMA? logicalDeviceName = id_)+
        | TO ( COMMA? (DISK | TAPE | URL) EQ (STRING | id_))+
    ) (
        (MIRROR TO ( COMMA? logicalDeviceName = id_)+)+
        | ( MIRROR TO ( COMMA? (DISK | TAPE | URL) EQ (STRING | id_))+)+
    )? (
        WITH (
            COMMA? DIFFERENTIAL
            | COMMA? COPY_ONLY
            | COMMA? (COMPRESSION | NO_COMPRESSION)
            | COMMA? DESCRIPTION EQ (STRING | id_)
            | COMMA? NAME EQ backupSetName = id_
            | COMMA? CREDENTIAL
            | COMMA? FILE_SNAPSHOT
            | COMMA? (EXPIREDATE EQ (STRING | id_) | RETAINDAYS EQ (INT | id_))
            | COMMA? (NOINIT | INIT)
            | COMMA? (NOSKIP | SKIP_KEYWORD)
            | COMMA? (NOFORMAT | FORMAT)
            | COMMA? MEDIADESCRIPTION EQ (STRING | id_)
            | COMMA? MEDIANAME EQ (medianame = STRING)
            | COMMA? BLOCKSIZE EQ (INT | id_)
            | COMMA? BUFFERCOUNT EQ (INT | id_)
            | COMMA? MAXTRANSFER EQ (INT | id_)
            | COMMA? (NO_CHECKSUM | CHECKSUM)
            | COMMA? (STOP_ON_ERROR | CONTINUE_AFTER_ERROR)
            | COMMA? RESTART
            | COMMA? STATS (EQ statsPercent = INT)?
            | COMMA? (REWIND | NOREWIND)
            | COMMA? (LOAD | NOUNLOAD)
            | COMMA? (NORECOVERY | STANDBY EQ undoFileName = STRING)
            | COMMA? NO_TRUNCATE
            | COMMA? ENCRYPTION LPAREN ALGORITHM EQ (
                AES_128
                | AES_192
                | AES_256
                | TRIPLE_DES_3KEY
            ) COMMA SERVER CERTIFICATE EQ (
                encryptorName = id_
                | SERVER ASYMMETRIC KEY EQ encryptorName = id_
            )
        )*
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/backup-certificate-transact-sql
backupCertificate
    : BACKUP CERTIFICATE certname = id_ TO FILE EQ certFile = STRING (
        WITH PRIVATE KEY LPAREN (
            COMMA? FILE EQ privateKeyFile = STRING
            | COMMA? ENCRYPTION BY PASSWORD EQ encryptionPassword = STRING
            | COMMA? DECRYPTION BY PASSWORD EQ decryptionPasword = STRING
        )+ RPAREN
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/backup-master-key-transact-sql
backupMasterKey
    : BACKUP MASTER KEY TO FILE EQ masterKeyBackupFile = STRING ENCRYPTION BY PASSWORD EQ encryptionPassword = STRING
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/backup-service-master-key-transact-sql
backupServiceMasterKey
    : BACKUP SERVICE MASTER KEY TO FILE EQ serviceMasterKeyBackupFile = STRING ENCRYPTION BY PASSWORD EQ encryptionPassword = STRING
    ;

killStatement
    : KILL (killProcess | killQueryNotification | killStatsJob)
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/kill-transact-sql
killProcess
    : (sessionId = (INT | STRING) | UOW) (WITH STATUSONLY)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/kill-query-notification-subscription-transact-sql
killQueryNotification
    : QUERY NOTIFICATION SUBSCRIPTION (ALL | subscriptionId = INT)
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/kill-stats-job-transact-sql
killStatsJob
    : STATS JOB jobId = INT
    ;

// https://msdn.microsoft.com/en-us/library/ms188332.aspx
executeStatement
    : EXECUTE executeBody SEMI?
    ;

executeBodyBatch
    : funcProcNameServerDatabaseSchema (executeStatementArg (COMMA executeStatementArg)*)? SEMI?
    ;

//https://docs.microsoft.com/it-it/sql/t-sql/language-elements/execute-transact-sql?view=sql-server-ver15
executeBody
    : (returnStatus = LOCAL_ID EQ)? (funcProcNameServerDatabaseSchema | executeVarString) executeStatementArg?
    | LPAREN executeVarString (COMMA executeVarString)* RPAREN (AS (LOGIN | USER) EQ STRING)? (
        AT_KEYWORD linkedServer = id_
    )?
    | AS ( (LOGIN | USER) EQ STRING | CALLER)
    ;

executeStatementArg
    : executeStatementArgUnnamed (COMMA executeStatementArg)*     //Unnamed params can continue unnamed
    | executeStatementArgNamed (COMMA executeStatementArgNamed)* //Named can only be continued by unnamed
    ;

executeStatementArgNamed
    : name = LOCAL_ID EQ value = executeParameter
    ;

executeStatementArgUnnamed
    : value = executeParameter
    ;

executeParameter
    : (constant | LOCAL_ID (OUTPUT | OUT)? | id_ | DEFAULT | NULL_)
    ;

executeVarString
    : LOCAL_ID (OUTPUT | OUT)? (PLUS LOCAL_ID (PLUS executeVarString)?)?
    | STRING (PLUS LOCAL_ID (PLUS executeVarString)?)?
    ;

// https://msdn.microsoft.com/en-us/library/ff848791.aspx
securityStatement
    // https://msdn.microsoft.com/en-us/library/ms188354.aspx
    : executeClause SEMI?
    // https://msdn.microsoft.com/en-us/library/ms187965.aspx
    | GRANT (ALL PRIVILEGES? | grantPermission (LPAREN columnNameList RPAREN)?) (
        ON (classTypeForGrant COLON COLON)? onId = tableName
    )? TO toPrincipal += principalId (COMMA toPrincipal += principalId)* (WITH GRANT OPTION)? (
        AS asPrincipal = principalId
    )? SEMI?
    // https://msdn.microsoft.com/en-us/library/ms178632.aspx
    | REVERT (WITH COOKIE EQ LOCAL_ID)? SEMI?
    | openKey
    | closeKey
    | createKey
    | createCertificate
    ;

principalId
    : id_
    | PUBLIC
    ;

createCertificate
    : CREATE CERTIFICATE certificateName = id_ (AUTHORIZATION userName = id_)? (
        FROM existingKeys
        | generateNewKeys
    ) (ACTIVE FOR BEGIN DIALOG EQ onOff)?
    ;

existingKeys
    : ASSEMBLY assemblyName = id_
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

dateOptions
    : (START_DATE | EXPIRY_DATE) EQ STRING
    ;

openKey
    : OPEN SYMMETRIC KEY keyName = id_ DECRYPTION BY decryptionMechanism
    | OPEN MASTER KEY DECRYPTION BY PASSWORD EQ password = STRING
    ;

closeKey
    : CLOSE SYMMETRIC KEY keyName = id_
    | CLOSE ALL SYMMETRIC KEYS
    | CLOSE MASTER KEY
    ;

createKey
    : CREATE MASTER KEY ENCRYPTION BY PASSWORD EQ password = STRING
    | CREATE SYMMETRIC KEY keyName = id_ (AUTHORIZATION userName = id_)? (
        FROM PROVIDER providerName = id_
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
    : CERTIFICATE certificateName = id_
    | ASYMMETRIC KEY asymKeyName = id_
    | SYMMETRIC KEY decrypting_KeyName = id_
    | PASSWORD EQ STRING
    ;

decryptionMechanism
    : CERTIFICATE certificateName = id_ (WITH PASSWORD EQ STRING)?
    | ASYMMETRIC KEY asymKeyName = id_ (WITH PASSWORD EQ STRING)?
    | SYMMETRIC KEY decrypting_KeyName = id_
    | PASSWORD EQ STRING
    ;

// https://docs.microsoft.com/en-us/sql/relational-databases/system-functions/sys-fn-builtin-permissions-transact-sql?view=sql-server-ver15
// SELECT DISTINCT '| ' + permissionName
// FROM sys.fnBuiltinPermissions (DEFAULT)
// ORDER BY 1
grantPermission
    : ADMINISTER (BULK OPERATIONS | DATABASE BULK OPERATIONS)
    | ALTER (
        ANY (
            APPLICATION ROLE
            | ASSEMBLY
            | ASYMMETRIC KEY
            | AVAILABILITY GROUP
            | CERTIFICATE
            | COLUMN ( ENCRYPTION KEY | MASTER KEY)
            | CONNECTION
            | CONTRACT
            | CREDENTIAL
            | DATABASE (
                AUDIT
                | DDL TRIGGER
                | EVENT ( NOTIFICATION | SESSION)
                | SCOPED CONFIGURATION
            )?
            | DATASPACE
            | ENDPOINT
            | EVENT ( NOTIFICATION | SESSION)
            | EXTERNAL ( DATA SOURCE | FILE FORMAT | LIBRARY)
            | FULLTEXT CATALOG
            | LINKED SERVER
            | LOGIN
            | MASK
            | MESSAGE TYPE
            | REMOTE SERVICE BINDING
            | ROLE
            | ROUTE
            | SCHEMA
            | SECURITY POLICY
            | SERVER ( AUDIT | ROLE)
            | SERVICE
            | SYMMETRIC KEY
            | USER
        )
        | RESOURCES
        | SERVER STATE
        | SETTINGS
        | TRACE
    )?
    | AUTHENTICATE SERVER?
    | BACKUP ( DATABASE | LOG)
    | CHECKPOINT
    | CONNECT ( ANY DATABASE | REPLICATION | SQL)?
    | CONTROL SERVER?
    | CREATE (
        AGGREGATE
        | ANY DATABASE
        | ASSEMBLY
        | ASYMMETRIC KEY
        | AVAILABILITY GROUP
        | CERTIFICATE
        | CONTRACT
        | DATABASE (DDL EVENT NOTIFICATION)?
        | DDL EVENT NOTIFICATION
        | DEFAULT
        | ENDPOINT
        | EXTERNAL LIBRARY
        | FULLTEXT CATALOG
        | FUNCTION
        | MESSAGE TYPE
        | PROCEDURE
        | QUEUE
        | REMOTE SERVICE BINDING
        | ROLE
        | ROUTE
        | RULE
        | SCHEMA
        | SEQUENCE
        | SERVER ROLE
        | SERVICE
        | SYMMETRIC KEY
        | SYNONYM
        | TABLE
        | TRACE EVENT NOTIFICATION
        | TYPE
        | VIEW
        | XML SCHEMA COLLECTION
    )
    | DELETE
    | EXECUTE ( ANY EXTERNAL SCRIPT)?
    | EXTERNAL ACCESS ASSEMBLY
    | IMPERSONATE ( ANY LOGIN)?
    | INSERT
    | KILL DATABASE CONNECTION
    | RECEIVE
    | REFERENCES
    | SELECT ( ALL USER SECURABLES)?
    | SEND
    | SHOWPLAN
    | SHUTDOWN
    | SUBSCRIBE QUERY NOTIFICATIONS
    | TAKE OWNERSHIP
    | UNMASK
    | UNSAFE ASSEMBLY
    | UPDATE
    | VIEW (
        ANY (DATABASE | DEFINITION | COLUMN ( ENCRYPTION | MASTER) KEY DEFINITION)
        | CHANGE TRACKING
        | DATABASE STATE
        | DEFINITION
        | SERVER STATE
    )
    ;

// https://msdn.microsoft.com/en-us/library/ms190356.aspx
// https://msdn.microsoft.com/en-us/library/ms189484.aspx
setStatement
    : SET LOCAL_ID (DOT memberName = id_)? EQ expression
    | SET LOCAL_ID assignmentOperator expression
    | SET LOCAL_ID EQ CURSOR declareSetCursorCommon (
        FOR (READ ONLY | UPDATE (OF columnNameList)?)
    )?
    // https://msdn.microsoft.com/en-us/library/ms189837.aspx
    | setSpecial
    ;

// https://msdn.microsoft.com/en-us/library/ms174377.aspx
transactionStatement
    // https://msdn.microsoft.com/en-us/library/ms188386.aspx
    : BEGIN DISTRIBUTED (TRAN | TRANSACTION) (id_ | LOCAL_ID)?
    // https://msdn.microsoft.com/en-us/library/ms188929.aspx
    | BEGIN (TRAN | TRANSACTION) ((id_ | LOCAL_ID) (WITH MARK STRING)?)?
    // https://msdn.microsoft.com/en-us/library/ms190295.aspx
    | COMMIT (TRAN | TRANSACTION) (
        (id_ | LOCAL_ID) (WITH LPAREN DELAYED_DURABILITY EQ (OFF | ON) RPAREN)?
    )?
    // https://msdn.microsoft.com/en-us/library/ms178628.aspx
    | COMMIT WORK?
    | COMMIT id_
    | ROLLBACK id_
    // https://msdn.microsoft.com/en-us/library/ms181299.aspx
    | ROLLBACK (TRAN | TRANSACTION) (id_ | LOCAL_ID)?
    // https://msdn.microsoft.com/en-us/library/ms174973.aspx
    | ROLLBACK WORK?
    // https://msdn.microsoft.com/en-us/library/ms188378.aspx
    | SAVE (TRAN | TRANSACTION) (id_ | LOCAL_ID)?
    ;

// https://msdn.microsoft.com/en-us/library/ms188037.aspx
goStatement
    : GO (count = INT)?
    ;

// https://msdn.microsoft.com/en-us/library/ms188366.aspx
useStatement
    : USE database = id_
    ;

setuserStatement
    : SETUSER user = STRING?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/reconfigure-transact-sql
reconfigureStatement
    : RECONFIGURE (WITH OVERRIDE)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/shutdown-transact-sql
shutdownStatement
    : SHUTDOWN (WITH NOWAIT)?
    ;

checkpointStatement
    : CHECKPOINT (checkPointDuration = INT)?
    ;

dbccCheckallocOption
    : ALL_ERRORMSGS
    | NO_INFOMSGS
    | TABLOCK
    | ESTIMATEONLY
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checkalloc-transact-sql?view=sql-server-ver16
dbccCheckalloc
    : name = CHECKALLOC (
        LPAREN (database = id_ | databaseid = STRING | INT) (
            COMMA NOINDEX
            | COMMA ( REPAIR_ALLOW_DATA_LOSS | REPAIR_FAST | REPAIR_REBUILD)
        )? RPAREN (
            WITH dbccOption = dbccCheckallocOption (COMMA dbccOption = dbccCheckallocOption)*
        )?
    )?
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checkcatalog-transact-sql?view=sql-server-ver16
dbccCheckcatalog
    : name = CHECKCATALOG (LPAREN ( database = id_ | databasename = STRING | INT) RPAREN)? (
        WITH dbccOption = NO_INFOMSGS
    )?
    ;

dbccCheckconstraintsOption
    : ALL_CONSTRAINTS
    | ALL_ERRORMSGS
    | NO_INFOMSGS
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checkconstraints-transact-sql?view=sql-server-ver16
dbccCheckconstraints
    : name = CHECKCONSTRAINTS (
        LPAREN (tableOrConstraint = id_ | tableOrConstraintName = STRING) RPAREN
    )? (
        WITH dbccOption = dbccCheckconstraintsOption (
            COMMA dbccOption = dbccCheckconstraintsOption
        )*
    )?
    ;

dbccCheckdbTableOption
    : ALL_ERRORMSGS
    | EXTENDED_LOGICAL_CHECKS
    | NO_INFOMSGS
    | TABLOCK
    | ESTIMATEONLY
    | PHYSICAL_ONLY
    | DATA_PURITY
    | MAXDOP EQ maxDregreeOfParallelism = INT
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checkdb-transact-sql?view=sql-server-ver16
dbccCheckdb
    : name = CHECKDB (
        LPAREN (database = id_ | databasename = STRING | INT) (
            COMMA (NOINDEX | REPAIR_ALLOW_DATA_LOSS | REPAIR_FAST | REPAIR_REBUILD)
        )? RPAREN
    )? (
        WITH dbccOption = dbccCheckdbTableOption (COMMA dbccOption = dbccCheckdbTableOption)*
    )?
    ;

dbccCheckfilegroupOption
    : ALL_ERRORMSGS
    | NO_INFOMSGS
    | TABLOCK
    | ESTIMATEONLY
    | PHYSICAL_ONLY
    | MAXDOP EQ maxDregreeOfParallelism = INT
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checkfilegroup-transact-sql?view=sql-server-ver16
// Additional parameters: https://dbtut.com/index.php/2019/01/01/dbcc-checkfilegroup-command-on-sql-server/
dbccCheckfilegroup
    : name = CHECKFILEGROUP (
        LPAREN (filegroupId = INT | filegroupName = STRING) (
            COMMA (NOINDEX | REPAIR_ALLOW_DATA_LOSS | REPAIR_FAST | REPAIR_REBUILD)
        )? RPAREN
    )? (
        WITH dbccOption = dbccCheckfilegroupOption (
            COMMA dbccOption = dbccCheckfilegroupOption
        )*
    )?
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checktable-transact-sql?view=sql-server-ver16
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

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-cleantable-transact-sql?view=sql-server-ver16
dbccCleantable
    : name = CLEANTABLE LPAREN (database = id_ | databasename = STRING | INT) COMMA (
        tableOrView = id_
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

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-clonedatabase-transact-sql?view=sql-server-ver16
dbccClonedatabase
    : name = CLONEDATABASE LPAREN sourceDatabase = id_ COMMA targetDatabase = id_ RPAREN (
        WITH dbccOption = dbccClonedatabaseOption (COMMA dbccOption = dbccClonedatabaseOption)*
    )?
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-pdw-showspaceused-transact-sql?view=aps-pdw-2016-au7
dbccPdwShowspaceused
    : name = PDW_SHOWSPACEUSED (LPAREN tablename = id_ RPAREN)? (
        WITH dbccOption = IGNORE_REPLICATED_TABLE_CACHE
    )?
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-proccache-transact-sql?view=sql-server-ver16
dbccProccache
    : name = PROCCACHE (WITH dbccOption = NO_INFOMSGS)?
    ;

dbccShowcontigOption
    : ALL_INDEXES
    | TABLERESULTS
    | FAST
    | ALL_LEVELS
    | NO_INFOMSGS
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-showcontig-transact-sql?view=sql-server-ver16
dbccShowcontig
    : name = SHOWCONTIG (LPAREN tableOrView = expression ( COMMA index = expression)? RPAREN)? (
        WITH dbccOption = dbccShowcontigOption (COMMA dbccShowcontigOption)*
    )?
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-shrinklog-azure-sql-data-warehouse?view=aps-pdw-2016-au7
dbccShrinklog
    : name = SHRINKLOG (LPAREN SIZE EQ ( (INT ( MB | GB | TB)) | DEFAULT) RPAREN)? (
        WITH dbccOption = NO_INFOMSGS
    )?
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-dbreindex-transact-sql?view=sql-server-ver16
dbccDbreindex
    : name = DBREINDEX LPAREN table = idOrString (
        COMMA indexName = idOrString ( COMMA fillfactor = expression)?
    )? RPAREN (WITH dbccOption = NO_INFOMSGS)?
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-dllname-free-transact-sql?view=sql-server-ver16
dbccDllFree
    : dllname = id_ LPAREN name = FREE RPAREN (WITH dbccOption = NO_INFOMSGS)?
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-dropcleanbuffers-transact-sql?view=sql-server-ver16
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

executeClause
    : EXECUTE AS clause = (CALLER | SELF | OWNER | STRING)
    ;

declareLocal
    : LOCAL_ID AS? dataType (EQ expression)?
    ;

tableTypeDefinition
    : TABLE LPAREN columnDefTableConstraints (COMMA? tableTypeIndices)* RPAREN
    ;

tableTypeIndices
    : (((PRIMARY KEY | INDEX id_) (CLUSTERED | NONCLUSTERED)?) | UNIQUE) LPAREN columnNameListWithOrder RPAREN
    | CHECK LPAREN searchCondition RPAREN
    ;

xmlTypeDefinition
    : XML LPAREN (CONTENT | DOCUMENT)? xmlSchemaCollection RPAREN
    ;

xmlSchemaCollection
    : ID DOT ID
    ;

columnDefTableConstraints
    : columnDefTableConstraint (COMMA? columnDefTableConstraint)*
    ;

columnDefTableConstraint
    : columnDefinition
    | materializedColumnDefinition
    | tableConstraint
    ;

// https://msdn.microsoft.com/en-us/library/ms187742.aspx
// There is a documentation error: column definition elements can be given in
// any order
columnDefinition
    : id_ (dataType | AS expression PERSISTED?) columnDefinitionElement* columnIndex?
    ;

columnDefinitionElement
    : FILESTREAM
    | COLLATE collationName = id_
    | SPARSE
    | MASKED WITH LPAREN FUNCTION EQ maskFunction = STRING RPAREN
    | (CONSTRAINT constraint = id_)? DEFAULT constantExpr = expression
    | IDENTITY (LPAREN seed = INT COMMA increment = INT RPAREN)?
    | NOT FOR REPLICATION
    | GENERATED ALWAYS AS (ROW | TRANSACTION_ID | SEQUENCE_NUMBER) (START | END) HIDDEN_KEYWORD?
    // NULL / NOT NULL is a constraint
    | ROWGUIDCOL
    | ENCRYPTED WITH LPAREN COLUMN_ENCRYPTION_KEY EQ keyName = STRING COMMA ENCRYPTION_TYPE EQ (
        DETERMINISTIC
        | RANDOMIZED
    ) COMMA ALGORITHM EQ algo = STRING RPAREN
    | columnConstraint
    ;

columnModifier
    : id_ (ADD | DROP) (
        ROWGUIDCOL
        | PERSISTED
        | NOT FOR REPLICATION
        | SPARSE
        | HIDDEN_KEYWORD
        | MASKED (WITH (FUNCTION EQ STRING | LPAREN FUNCTION EQ STRING RPAREN))?
    )
    ;

materializedColumnDefinition
    : id_ (COMPUTE | AS) expression (MATERIALIZED | NOT MATERIALIZED)?
    ;

// https://msdn.microsoft.com/en-us/library/ms186712.aspx
// There is a documentation error: NOT NULL is a constraint
// and therefore can be given a name.
columnConstraint
    : (CONSTRAINT constraint = id_)? (
        nullNotnull
        | ( (PRIMARY KEY | UNIQUE) clustered? primaryKeyOptions)
        | ( (FOREIGN KEY)? foreignKeyOptions)
        | checkConstraint
    )
    ;

columnIndex
    : INDEX indexName = id_ clustered? createTableIndexOptions? onPartitionOrFilegroup? (
        FILESTREAM_ON (filestreamFilegroupOrPartitionSchemaName = id_ | NULL_DOUBLE_QUOTE)
    )?
    ;

onPartitionOrFilegroup
    : ON (
        (partitionSchemeName = id_ LPAREN partitionColumnName = id_ RPAREN)
        | filegroup = id_
        | DEFAULT_DOUBLE_QUOTE
    )
    ;

// https://msdn.microsoft.com/en-us/library/ms188066.aspx
tableConstraint
    : (CONSTRAINT constraint = id_)? (
        ((PRIMARY KEY | UNIQUE) clustered? LPAREN columnNameListWithOrder RPAREN primaryKeyOptions)
        | ( FOREIGN KEY LPAREN fk = columnNameList RPAREN foreignKeyOptions)
        | ( CONNECTION LPAREN connectionNode ( COMMA connectionNode)* RPAREN)
        | ( DEFAULT constantExpr = expression FOR column = id_ (WITH VALUES)?)
        | checkConstraint
    )
    ;

connectionNode
    : fromNodeTable = id_ TO toNodeTable = id_
    ;

primaryKeyOptions
    : (WITH FILLFACTOR EQ INT)? alterTableIndexOptions? onPartitionOrFilegroup?
    ;

foreignKeyOptions
    : REFERENCES tableName LPAREN pk = columnNameList RPAREN (onDelete | onUpdate)* (
        NOT FOR REPLICATION
    )?
    ;

checkConstraint
    : CHECK (NOT FOR REPLICATION)? LPAREN searchCondition RPAREN
    ;

onDelete
    : ON DELETE (NO ACTION | CASCADE | SET NULL_ | SET DEFAULT)
    ;

onUpdate
    : ON UPDATE (NO ACTION | CASCADE | SET NULL_ | SET DEFAULT)
    ;

alterTableIndexOptions
    : WITH LPAREN alterTableIndexOption (COMMA alterTableIndexOption)* RPAREN
    ;

// https://msdn.microsoft.com/en-us/library/ms186869.aspx
alterTableIndexOption
    : PAD_INDEX EQ onOff
    | FILLFACTOR EQ INT
    | IGNORE_DUP_KEY EQ onOff
    | STATISTICS_NORECOMPUTE EQ onOff
    | ALLOW_ROW_LOCKS EQ onOff
    | ALLOW_PAGE_LOCKS EQ onOff
    | OPTIMIZE_FOR_SEQUENTIAL_KEY EQ onOff
    | SORT_IN_TEMPDB EQ onOff
    | MAXDOP EQ maxDegreeOfParallelism = INT
    | DATA_COMPRESSION EQ (NONE | ROW | PAGE | COLUMNSTORE | COLUMNSTORE_ARCHIVE) onPartitions?
    | XML_COMPRESSION EQ onOff onPartitions?
    | DISTRIBUTION EQ HASH LPAREN id_ RPAREN
    | CLUSTERED INDEX LPAREN id_ (ASC | DESC)? (COMMA id_ (ASC | DESC)?)* RPAREN
    | ONLINE EQ (ON (LPAREN lowPriorityLockWait RPAREN)? | OFF)
    | RESUMABLE EQ onOff
    | MAX_DURATION EQ times = INT MINUTES?
    ;

// https://msdn.microsoft.com/en-us/library/ms180169.aspx
declareCursor
    : DECLARE cursorName (
        CURSOR (declareSetCursorCommon (FOR UPDATE (OF columnNameList)?)?)?
        | (SEMI_SENSITIVE | INSENSITIVE)? SCROLL? CURSOR FOR selectStatementStandalone (
            FOR (READ ONLY | UPDATE | (OF columnNameList))
        )?
    ) SEMI?
    ;

declareSetCursorCommon
    : declareSetCursorCommonPartial* FOR selectStatementStandalone
    ;

declareSetCursorCommonPartial
    : (LOCAL | GLOBAL)
    | (FORWARD_ONLY | SCROLL)
    | (STATIC | KEYSET | DYNAMIC | FAST_FORWARD)
    | (READ_ONLY | SCROLL_LOCKS | OPTIMISTIC)
    | TYPE_WARNING
    ;

fetchCursor
    : FETCH ((NEXT | PRIOR | FIRST | LAST | (ABSOLUTE | RELATIVE) expression)? FROM)? GLOBAL? cursorName (
        INTO LOCAL_ID (COMMA LOCAL_ID)*
    )? SEMI?
    ;

// https://msdn.microsoft.com/en-us/library/ms190356.aspx
// Runtime check.
setSpecial
    : SET id_ (id_ | constant_LOCAL_ID | onOff) SEMI?
    | SET STATISTICS (IO | TIME | XML | PROFILE) onOff SEMI?
    | SET ROWCOUNT (LOCAL_ID | INT) SEMI?
    | SET TEXTSIZE INT SEMI?
    // https://msdn.microsoft.com/en-us/library/ms173763.aspx
    | SET TRANSACTION ISOLATION LEVEL (
        READ UNCOMMITTED
        | READ COMMITTED
        | REPEATABLE READ
        | SNAPSHOT
        | SERIALIZABLE
        | INT
    ) SEMI?
    // https://msdn.microsoft.com/en-us/library/ms188059.aspx
    | SET IDENTITY_INSERT tableName onOff SEMI?
    | SET specialList (COMMA specialList)* onOff
    | SET modifyMethod
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

constant_LOCAL_ID
    : constant
    | LOCAL_ID
    ;

// Expression.

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/expressions-transact-sql
// Operator precendence: https://docs.microsoft.com/en-us/sql/t-sql/language-elements/operator-precedence-transact-sql
expression
    : LPAREN expression RPAREN                                  #expr_precedence
    | <assoc=right> op=BIT_NOT expression                       #expr_bit_not
    | <assoc=right> op=(PLUS | MINUS) expression                #expr_unary
    | expression op=(STAR | DIV | MOD) expression               #expr_op_prec_1
    | expression op=(PLUS | MINUS) expression                   #expr_op_prec_2
    | expression op=(BIT_AND | BIT_XOR | BIT_OR) expression     #expr_op_prec_3
    | expression op=DOUBLE_BAR expression                       #expr_op_prec_4
    | primitive_expression                                      #expr_primitive
    | function_call                                             #expr_func
    | expression COLLATE id_                                    #expr_collate
    | case_expression                                           #expr_case
    | expression time_zone                                      #expr_tz
    | over_clause                                               #expr_over
    | hierarchyid_call                                          #exprHierarchyId
    | value_call                                                #exprValue
    | query_call                                                #expryQuery
    | exist_call                                                #exprExist
    | modify_call                                               #exprModiy
    | id_                                                       #expr_id
    | DOLLAR_ACTION                                             #expr_dollar
    | <assoc=right> expression DOT expression                   #exprDot
    | LPAREN subquery RPAREN                                    #expr_subquery
    | over_clause                                               #expr_over
    ;

parameter
    : PLACEHOLDER
    ;

timeZone
    : AT_KEYWORD TIME ZONE expression
    ;

primitiveExpression
    : DEFAULT
    | NULL_
    | LOCAL_ID
    | primitiveConstant
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/case-transact-sql
caseExpression
    : CASE caseExpr = expression switchSection+ (ELSE elseExpr = expression)? END
    | CASE switchSearchConditionSection+ (ELSE elseExpr = expression)? END
    ;

subquery
    : selectStatement
    ;

// https://msdn.microsoft.com/en-us/library/ms175972.aspx
withExpression
    : WITH ctes += commonTableExpression (COMMA ctes += commonTableExpression)*
    ;

commonTableExpression
    : expressionName = id_ (LPAREN columns = columnNameList RPAREN)? AS LPAREN cteQuery = selectStatement RPAREN
    ;

updateElem
    : LOCAL_ID EQ fullColumnName (EQ | assignmentOperator) expression //Combined variable and column update
    | (fullColumnName | LOCAL_ID) (EQ | assignmentOperator) expression
    | udtColumnName = id_ DOT methodName = id_ LPAREN expressionList_ RPAREN
    //| fullColumnName DOT WRITE (expression, )
    ;

updateElemMerge
    : (fullColumnName | LOCAL_ID) (EQ | assignmentOperator) expression
    | udtColumnName = id_ DOT methodName = id_ LPAREN expressionList_ RPAREN
    //| fullColumnName DOT WRITE (expression, )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/queries/search-condition-transact-sql
searchCondition
    : NOT* (predicate | LPAREN searchCondition RPAREN)
    | searchCondition AND searchCondition // AND takes precedence over OR
    | searchCondition OR searchCondition
    ;

predicate
    : EXISTS LPAREN subquery RPAREN
    | freetextPredicate
    | expression comparisonOperator expression
    | expression ME expression ////SQL-82 syntax for left outer joins; PE. See https://stackoverflow.com/questions/40665/in-sybase-sql
    | expression comparisonOperator (ALL | SOME | ANY) LPAREN subquery RPAREN
    | expression NOT* BETWEEN expression AND expression
    | expression NOT* IN LPAREN (subquery | expressionList_) RPAREN
    | expression NOT* LIKE expression (ESCAPE expression)?
    | expression IS nullNotnull
    ;

// Changed union rule to sqlUnion to avoid union construct with C++ target.  Issue reported by person who generates into C++.  This individual reports change causes generated code to work

queryExpression
    : querySpecification selectOrderByClause? unions += sqlUnion* //if using top, order by can be on the "top" side of union :/
    | LPAREN queryExpression RPAREN (UNION ALL? queryExpression)?
    ;

sqlUnion
    : (UNION ALL? | EXCEPT | INTERSECT) (
        spec = querySpecification
        | (LPAREN op = queryExpression RPAREN)
    )
    ;

// https://msdn.microsoft.com/en-us/library/ms176104.aspx
querySpecification
    : SELECT allOrDistinct = (ALL | DISTINCT)? top = topClause? columns = selectList
    // https://msdn.microsoft.com/en-us/library/ms188029.aspx
    (INTO into = tableName)? (FROM from = tableSources)? (WHERE where = searchCondition)?
    // https://msdn.microsoft.com/en-us/library/ms177673.aspx
    (
        GROUP BY (
            (groupByAll = ALL? groupBys += groupByItem (COMMA groupBys += groupByItem)*)
            | GROUPING SETS LPAREN groupSets += groupingSetsItem (
                COMMA groupSets += groupingSetsItem
            )* RPAREN
        )
    )? (HAVING having = searchCondition)?
    ;

// https://msdn.microsoft.com/en-us/library/ms189463.aspx
topClause
    : TOP (topPercent | topCount) (WITH TIES)?
    ;

topPercent
    : percentConstant = (REAL | FLOAT | INT) PERCENT
    | LPAREN topperExpression = expression RPAREN PERCENT
    ;

topCount
    : countConstant = INT
    | LPAREN topcountExpression = expression RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/queries/select-over-clause-transact-sql?view=sql-server-ver16
orderByClause
    : ORDER BY orderBys += orderByExpression (COMMA orderBys += orderByExpression)*
    ;

// https://msdn.microsoft.com/en-us/library/ms188385.aspx
selectOrderByClause
    : orderByClause (
        OFFSET offsetExp = expression offsetRows = (ROW | ROWS) (
            FETCH fetchOffset = (FIRST | NEXT) fetchExp = expression fetchRows = (ROW | ROWS) ONLY
        )?
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/queries/select-for-clause-transact-sql
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

xmlCommonDirectives
    : COMMA (BINARY_KEYWORD BASE64 | TYPE | ROOT (LPAREN STRING RPAREN)?)
    ;

orderByExpression
    : orderBy = expression (ascending = ASC | descending = DESC)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/queries/select-group-by-transact-sql?view=sql-server-ver15
groupingSetsItem
    : LPAREN? groupSetItems += groupByItem (COMMA groupSetItems += groupByItem)* RPAREN?
    | LPAREN RPAREN
    ;

groupByItem
    : expression
    /*| rollupSpec
    | cubeSpec
    | groupingSetsSpec
    | grandTotal*/
    ;

optionClause
    // https://msdn.microsoft.com/en-us/library/ms181714.aspx
    : OPTION LPAREN options_ += option (COMMA options_ += option)* RPAREN
    ;

option
    : FAST numberRows = INT
    | (HASH | ORDER) GROUP
    | (MERGE | HASH | CONCAT) UNION
    | (LOOP | MERGE | HASH) JOIN
    | EXPAND VIEWS
    | FORCE ORDER
    | IGNORE_NONCLUSTERED_COLUMNSTORE_INDEX
    | KEEP PLAN
    | KEEPFIXED PLAN
    | MAXDOP numberOfProcessors = INT
    | MAXRECURSION numberRecursion = INT
    | OPTIMIZE FOR LPAREN optimizeForArg (COMMA optimizeForArg)* RPAREN
    | OPTIMIZE FOR UNKNOWN
    | PARAMETERIZATION (SIMPLE | FORCED)
    | RECOMPILE
    | ROBUST PLAN
    | USE PLAN STRING
    ;

optimizeForArg
    : LOCAL_ID (UNKNOWN | EQ (constant | NULL_))
    ;

// https://msdn.microsoft.com/en-us/library/ms176104.aspx
selectList
    : selectElement += selectListElem (COMMA selectElement += selectListElem)*
    ;

udtMethodArguments
    : LPAREN argument += executeVarString (COMMA argument += executeVarString)* RPAREN
    ;

// https://docs.microsoft.com/ru-ru/sql/t-sql/queries/select-clause-transact-sql
asterisk
    : (tableName DOT)? STAR
    | (INSERTED | DELETED) DOT STAR
    ;

udtElem
    : udtColumnName = id_ DOT nonStaticAttr = id_ udtMethodArguments asColumnAlias?
    | udtColumnName = id_ DOUBLE_COLON staticAttr = id_ udtMethodArguments? asColumnAlias?
    ;

expressionElem
    : leftAlias = columnAlias eq = EQ leftAssignment = expression
    | expressionAs = expression asColumnAlias?
    ;

selectListElem
    : asterisk
    | udtElem
    | LOCAL_ID (assignmentOperator | EQ) expression
    | expressionElem
    ;

tableSources
    : nonAnsiJoin
    | source += tableSource (COMMA source += tableSource)*
    ;

// https://sqlenlight.com/support/help/sa0006/
nonAnsiJoin
    : source += tableSource (COMMA source += tableSource)+
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/queries/from-transact-sql
tableSource
    : tableSourceItem joins += joinPart*
    ;

tableSourceItem
    : fullTableName deprecatedTableHint asTableAlias // this is currently allowed
    | fullTableName asTableAlias? (
        withTableHints
        | deprecatedTableHint
        | sybaseLegacyHints
    )?
    | rowsetFunction asTableAlias?
    | LPAREN derivedTable RPAREN (asTableAlias columnAliasList?)?
    | changeTable asTableAlias?
    | nodesMethod (asTableAlias columnAliasList?)?
    | functionCall (asTableAlias columnAliasList?)?
    | locId = LOCAL_ID asTableAlias?
    | locIdCall = LOCAL_ID DOT locFcall = functionCall (asTableAlias columnAliasList?)?
    | openXml
    | openJson
    | DOUBLE_COLON oldstyleFcall = functionCall asTableAlias? // Build-in function (old syntax)
    | LPAREN tableSource RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/functions/openxml-transact-sql
openXml
    : OPENXML LPAREN expression COMMA expression (COMMA expression)? RPAREN (WITH LPAREN schemaDeclaration RPAREN)? asTableAlias?
    ;

openJson
    : OPENJSON LPAREN expression (COMMA expression)? RPAREN (WITH LPAREN jsonDeclaration RPAREN)? asTableAlias?
    ;

jsonDeclaration
    : jsonCol += jsonColumnDeclaration (COMMA jsonCol += jsonColumnDeclaration)*
    ;

jsonColumnDeclaration
    : columnDeclaration (AS JSON)?
    ;

schemaDeclaration
    : xmlCol += columnDeclaration (COMMA xmlCol += columnDeclaration)*
    ;

columnDeclaration
    : id_ dataType STRING?
    ;

changeTable
    : changeTableChanges
    | changeTableVersion
    ;

changeTableChanges
    : CHANGETABLE LPAREN CHANGES changetable = tableName COMMA changesid = (NULL_ | INT | LOCAL_ID) RPAREN
    ;

changeTableVersion
    : CHANGETABLE LPAREN VERSION versiontable = tableName COMMA pkColumns = fullColumnNameList COMMA pkValues = selectList RPAREN
    ;

// https://msdn.microsoft.com/en-us/library/ms191472.aspx
joinPart
    // https://msdn.microsoft.com/en-us/library/ms173815(v=sql.120).aspx
    : joinOn
    | crossJoin
    | apply_
    | pivot
    | unpivot
    ;

outerJoin
    : (LEFT | RIGHT | FULL) OUTER?
    ;

joinType
    : INNER
    | outerJoin
    ;

joinOn
    : joinType? (
        joinHint = (LOOP | HASH | MERGE | REMOTE)
    )? JOIN source = tableSource ON cond = searchCondition
    ;

crossJoin
    : CROSS JOIN tableSourceItem
    ;

apply_
    : applyStyle = (CROSS | OUTER) APPLY source = tableSourceItem
    ;

pivot
    : PIVOT pivotClause asTableAlias
    ;

unpivot
    : UNPIVOT unpivotClause asTableAlias
    ;

pivotClause
    : LPAREN aggregateWindowedFunction FOR fullColumnName IN columnAliasList RPAREN
    ;

unpivotClause
    : LPAREN unpivotExp = expression FOR fullColumnName IN LPAREN fullColumnNameList RPAREN RPAREN
    ;

fullColumnNameList
    : column += fullColumnName (COMMA column += fullColumnName)*
    ;

// https://msdn.microsoft.com/en-us/library/ms190312.aspx
rowsetFunction
    : (
        OPENROWSET LPAREN providerName = STRING COMMA connectionString = STRING COMMA sql = STRING RPAREN
    )
    | (OPENROWSET LPAREN BULK dataFile = STRING COMMA (bulkOption (COMMA bulkOption)* | id_) RPAREN)
    ;

// runtime check.
bulkOption
    : id_ EQ bulkOptionValue = (INT | STRING)
    ;

derivedTable
    : subquery
    | LPAREN subquery (UNION ALL subquery)* RPAREN
    | tableValueConstructor
    | LPAREN tableValueConstructor RPAREN
    ;

functionCall
    : rankingWindowedFunction                      # RANKING_WINDOWED_FUNC
    | aggregateWindowedFunction                    # AGGREGATE_WINDOWED_FUNC
    | analyticWindowedFunction                     # ANALYTIC_WINDOWED_FUNC
    | builtInFunctions                             # BUILT_IN_FUNC
    | scalarFunctionName LPAREN expressionList_? RPAREN # SCALAR_FUNCTION
    | freetextFunction                              # FREE_TEXT
    | partitionFunction                             # PARTITION_FUNC
    | hierarchyidStaticMethod                      # HIERARCHYID_METHOD
    ;

partitionFunction
    : (database = id_ DOT)? DOLLAR_PARTITION DOT funcName = id_ LPAREN expression RPAREN
    ;

freetextFunction
    : (CONTAINSTABLE | FREETEXTTABLE) LPAREN tableName COMMA (
        fullColumnName
        | LPAREN fullColumnName (COMMA fullColumnName)* RPAREN
        | STAR
    ) COMMA expression (COMMA LANGUAGE expression)? (COMMA expression)? RPAREN
    | (SEMANTICSIMILARITYTABLE | SEMANTICKEYPHRASETABLE) LPAREN tableName COMMA (
        fullColumnName
        | LPAREN fullColumnName (COMMA fullColumnName)* RPAREN
        | STAR
    ) COMMA expression RPAREN
    | SEMANTICSIMILARITYDETAILSTABLE LPAREN tableName COMMA fullColumnName COMMA expression COMMA fullColumnName COMMA expression RPAREN
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

jsonKeyValue
    : jsonKeyName = expression COLON valueExpression = expression
    ;

jsonNullClause
    : (ABSENT | NULL_) ON NULL_
    ;

builtInFunctions
    // Metadata functions
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/app-name-transact-sql?view=sql-server-ver16
    : APP_NAME LPAREN RPAREN # APP_NAME
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/applock-mode-transact-sql?view=sql-server-ver16
    | APPLOCK_MODE LPAREN databasePrincipal = expression COMMA resourceName = expression COMMA lockOwner = expression RPAREN # APPLOCK_MODE
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/applock-test-transact-sql?view=sql-server-ver16
    | APPLOCK_TEST LPAREN databasePrincipal = expression COMMA resourceName = expression COMMA lockMode = expression COMMA lockOwner = expression RPAREN #
        APPLOCK_TEST
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/assemblyproperty-transact-sql?view=sql-server-ver16
    | ASSEMBLYPROPERTY LPAREN assemblyName = expression COMMA propertyName = expression RPAREN # ASSEMBLYPROPERTY
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/col-length-transact-sql?view=sql-server-ver16
    | COL_LENGTH LPAREN table = expression COMMA column = expression RPAREN # COL_LENGTH
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/col-name-transact-sql?view=sql-server-ver16
    | COL_NAME LPAREN tableId = expression COMMA columnId = expression RPAREN # COL_NAME
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/columnproperty-transact-sql?view=sql-server-ver16
    | COLUMNPROPERTY LPAREN id = expression COMMA column = expression COMMA property = expression RPAREN # COLUMNPROPERTY
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/databasepropertyex-transact-sql?view=sql-server-ver16
    | DATABASEPROPERTYEX LPAREN database = expression COMMA property = expression RPAREN # DATABASEPROPERTYEX
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/db-id-transact-sql?view=sql-server-ver16
    | DB_ID LPAREN databaseName = expression? RPAREN # DB_ID
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/db-name-transact-sql?view=sql-server-ver16
    | DB_NAME LPAREN databaseId = expression? RPAREN # DB_NAME
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/file-id-transact-sql?view=sql-server-ver16
    | FILE_ID LPAREN fileName = expression RPAREN # FILE_ID
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/file-idex-transact-sql?view=sql-server-ver16
    | FILE_IDEX LPAREN fileName = expression RPAREN # FILE_IDEX
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/file-name-transact-sql?view=sql-server-ver16
    | FILE_NAME LPAREN fileId = expression RPAREN # FILE_NAME
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/filegroup-id-transact-sql?view=sql-server-ver16
    | FILEGROUP_ID LPAREN filegroupName = expression RPAREN # FILEGROUP_ID
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/filegroup-name-transact-sql?view=sql-server-ver16
    | FILEGROUP_NAME LPAREN filegroupId = expression RPAREN # FILEGROUP_NAME
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/filegroupproperty-transact-sql?view=sql-server-ver16
    | FILEGROUPPROPERTY LPAREN filegroupName = expression COMMA property = expression RPAREN # FILEGROUPPROPERTY
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/fileproperty-transact-sql?view=sql-server-ver16
    | FILEPROPERTY LPAREN fileName = expression COMMA property = expression RPAREN # FILEPROPERTY
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/filepropertyex-transact-sql?view=sql-server-ver16
    | FILEPROPERTYEX LPAREN name = expression COMMA property = expression RPAREN # FILEPROPERTYEX
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/fulltextcatalogproperty-transact-sql?view=sql-server-ver16
    | FULLTEXTCATALOGPROPERTY LPAREN catalogName = expression COMMA property = expression RPAREN # FULLTEXTCATALOGPROPERTY
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/fulltextserviceproperty-transact-sql?view=sql-server-ver16
    | FULLTEXTSERVICEPROPERTY LPAREN property = expression RPAREN # FULLTEXTSERVICEPROPERTY
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/index-col-transact-sql?view=sql-server-ver16
    | INDEX_COL LPAREN tableOrViewName = expression COMMA indexId = expression COMMA keyId = expression RPAREN # INDEX_COL
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/indexkey-property-transact-sql?view=sql-server-ver16
    | INDEXKEY_PROPERTY LPAREN objectId = expression COMMA indexId = expression COMMA keyId = expression COMMA property = expression RPAREN # INDEXKEY_PROPERTY
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/indexproperty-transact-sql?view=sql-server-ver16
    | INDEXPROPERTY LPAREN objectId = expression COMMA indexOrStatisticsName = expression COMMA property = expression RPAREN # INDEXPROPERTY
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/next-value-for-transact-sql?view=sql-server-ver16
    | NEXT VALUE FOR sequenceName = tableName (OVER LPAREN orderByClause RPAREN)? # NEXT_VALUE_FOR
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/object-definition-transact-sql?view=sql-server-ver16
    | OBJECT_DEFINITION LPAREN objectId = expression RPAREN # OBJECT_DEFINITION
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/object-id-transact-sql?view=sql-server-ver16
    | OBJECT_ID LPAREN objectName = expression (COMMA objectType = expression)? RPAREN # OBJECT_ID
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/object-name-transact-sql?view=sql-server-ver16
    | OBJECT_NAME LPAREN objectId = expression (COMMA databaseId = expression)? RPAREN # OBJECT_NAME
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/object-schema-name-transact-sql?view=sql-server-ver16
    | OBJECT_SCHEMA_NAME LPAREN objectId = expression (COMMA databaseId = expression)? RPAREN # OBJECT_SCHEMA_NAME
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/objectproperty-transact-sql?view=sql-server-ver16
    | OBJECTPROPERTY LPAREN id = expression COMMA property = expression RPAREN # OBJECTPROPERTY
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/objectpropertyex-transact-sql?view=sql-server-ver16
    | OBJECTPROPERTYEX LPAREN id = expression COMMA property = expression RPAREN # OBJECTPROPERTYEX
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/original-db-name-transact-sql?view=sql-server-ver16
    | ORIGINAL_DB_NAME LPAREN RPAREN # ORIGINAL_DB_NAME
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/parsename-transact-sql?view=sql-server-ver16
    | PARSENAME LPAREN objectName = expression COMMA objectPiece = expression RPAREN # PARSENAME
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/schema-id-transact-sql?view=sql-server-ver16
    | SCHEMA_ID LPAREN schemaName = expression? RPAREN # SCHEMA_ID
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/schema-name-transact-sql?view=sql-server-ver16
    | SCHEMA_NAME LPAREN schemaId = expression? RPAREN # SCHEMA_NAME
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/scope-identity-transact-sql?view=sql-server-ver16
    | SCOPE_IDENTITY LPAREN RPAREN # SCOPE_IDENTITY
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/serverproperty-transact-sql?view=sql-server-ver16
    | SERVERPROPERTY LPAREN property = expression RPAREN # SERVERPROPERTY
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/stats-date-transact-sql?view=sql-server-ver16
    | STATS_DATE LPAREN objectId = expression COMMA statsId = expression RPAREN # STATS_DATE
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/type-id-transact-sql?view=sql-server-ver16
    | TYPE_ID LPAREN typeName = expression RPAREN # TYPE_ID
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/type-name-transact-sql?view=sql-server-ver16
    | TYPE_NAME LPAREN typeId = expression RPAREN # TYPE_NAME
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/typeproperty-transact-sql?view=sql-server-ver16
    | TYPEPROPERTY LPAREN type = expression COMMA property = expression RPAREN # TYPEPROPERTY
    // String functions
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/ascii-transact-sql?view=sql-server-ver16
    | ASCII LPAREN characterExpression = expression RPAREN # ASCII
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/char-transact-sql?view=sql-server-ver16
    | CHAR LPAREN integerExpression = expression RPAREN # CHAR
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/charindex-transact-sql?view=sql-server-ver16
    | CHARINDEX LPAREN expressionToFind = expression COMMA expressionToSearch = expression (
        COMMA startLocation = expression
    )? RPAREN # CHARINDEX
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/concat-transact-sql?view=sql-server-ver16
    | CONCAT LPAREN stringValue_1 = expression COMMA stringValue_2 = expression (
        COMMA stringValueN += expression
    )* RPAREN # CONCAT
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/concat-ws-transact-sql?view=sql-server-ver16
    | CONCAT_WS LPAREN separator = expression COMMA argument_1 = expression COMMA argument_2 = expression (
        COMMA argumentN += expression
    )* RPAREN # CONCAT_WS
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/difference-transact-sql?view=sql-server-ver16
    | DIFFERENCE LPAREN characterExpression_1 = expression COMMA characterExpression_2 = expression RPAREN # DIFFERENCE
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/format-transact-sql?view=sql-server-ver16
    | FORMAT LPAREN value = expression COMMA format = expression (COMMA culture = expression)? RPAREN # FORMAT
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/left-transact-sql?view=sql-server-ver16
    | LEFT LPAREN characterExpression = expression COMMA integerExpression = expression RPAREN # LEFT
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/len-transact-sql?view=sql-server-ver16
    | LEN LPAREN stringExpression = expression RPAREN # LEN
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/lower-transact-sql?view=sql-server-ver16
    | LOWER LPAREN characterExpression = expression RPAREN # LOWER
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/ltrim-transact-sql?view=sql-server-ver16
    | LTRIM LPAREN characterExpression = expression RPAREN # LTRIM
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/nchar-transact-sql?view=sql-server-ver16
    | NCHAR LPAREN integerExpression = expression RPAREN # NCHAR
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/patindex-transact-sql?view=sql-server-ver16
    | PATINDEX LPAREN pattern = expression COMMA stringExpression = expression RPAREN # PATINDEX
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/quotename-transact-sql?view=sql-server-ver16
    | QUOTENAME LPAREN characterString = expression (COMMA quoteCharacter = expression)? RPAREN # QUOTENAME
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/replace-transact-sql?view=sql-server-ver16
    | REPLACE LPAREN input = expression COMMA replacing = expression COMMA with = expression RPAREN # REPLACE
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/replicate-transact-sql?view=sql-server-ver16
    | REPLICATE LPAREN stringExpression = expression COMMA integerExpression = expression RPAREN # REPLICATE
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/reverse-transact-sql?view=sql-server-ver16
    | REVERSE LPAREN stringExpression = expression RPAREN # REVERSE
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/right-transact-sql?view=sql-server-ver16
    | RIGHT LPAREN characterExpression = expression COMMA integerExpression = expression RPAREN # RIGHT
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/rtrim-transact-sql?view=sql-server-ver16
    | RTRIM LPAREN characterExpression = expression RPAREN # RTRIM
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/soundex-transact-sql?view=sql-server-ver16
    | SOUNDEX LPAREN characterExpression = expression RPAREN # SOUNDEX
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/space-transact-sql?view=sql-server-ver16
    | SPACE_KEYWORD LPAREN integerExpression = expression RPAREN # SPACE
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/str-transact-sql?view=sql-server-ver16
    | STR LPAREN floatExpression = expression (
        COMMA lengthExpression = expression ( COMMA decimal = expression)?
    )? RPAREN # STR
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/string-agg-transact-sql?view=sql-server-ver16
    | STRING_AGG LPAREN expr = expression COMMA separator = expression RPAREN (
        WITHIN GROUP LPAREN orderByClause RPAREN
    )? # STRINGAGG
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/string-escape-transact-sql?view=sql-server-ver16
    | STRING_ESCAPE LPAREN text_ = expression COMMA type_ = expression RPAREN # STRING_ESCAPE
    // https://msdn.microsoft.com/fr-fr/library/ms188043.aspx
    | STUFF LPAREN str = expression COMMA from = expression COMMA to = expression COMMA strWith = expression RPAREN # STUFF
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/substring-transact-sql?view=sql-server-ver16
    | SUBSTRING LPAREN stringExpression = expression COMMA start_ = expression COMMA length = expression RPAREN # SUBSTRING
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/translate-transact-sql?view=sql-server-ver16
    | TRANSLATE LPAREN inputString = expression COMMA characters = expression COMMA translations = expression RPAREN # TRANSLATE
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/trim-transact-sql?view=sql-server-ver16
    | TRIM LPAREN (characters = expression FROM)? string_ = expression RPAREN # TRIM
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/unicode-transact-sql?view=sql-server-ver16
    | UNICODE LPAREN ncharacterExpression = expression RPAREN # UNICODE
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/upper-transact-sql?view=sql-server-ver16
    | UPPER LPAREN characterExpression = expression RPAREN # UPPER
    // System functions
    // https://msdn.microsoft.com/en-us/library/ms173784.aspx
    | BINARY_CHECKSUM LPAREN (star = STAR | expression (COMMA expression)*) RPAREN # BINARY_CHECKSUM
    // https://msdn.microsoft.com/en-us/library/ms189788.aspx
    | CHECKSUM LPAREN (star = STAR | expression (COMMA expression)*) RPAREN # CHECKSUM
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/compress-transact-sql?view=sql-server-ver16
    | COMPRESS LPAREN expr = expression RPAREN # COMPRESS
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/connectionproperty-transact-sql?view=sql-server-ver16
    | CONNECTIONPROPERTY LPAREN property = STRING RPAREN # CONNECTIONPROPERTY
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/context-info-transact-sql?view=sql-server-ver16
    | CONTEXT_INFO LPAREN RPAREN # CONTEXT_INFO
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/current-request-id-transact-sql?view=sql-server-ver16
    | CURRENT_REQUEST_ID LPAREN RPAREN # CURRENT_REQUEST_ID
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/current-transaction-id-transact-sql?view=sql-server-ver16
    | CURRENT_TRANSACTION_ID LPAREN RPAREN # CURRENT_TRANSACTION_ID
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/decompress-transact-sql?view=sql-server-ver16
    | DECOMPRESS LPAREN expr = expression RPAREN # DECOMPRESS
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/error-line-transact-sql?view=sql-server-ver16
    | ERROR_LINE LPAREN RPAREN # ERROR_LINE
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/error-message-transact-sql?view=sql-server-ver16
    | ERROR_MESSAGE LPAREN RPAREN # ERROR_MESSAGE
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/error-number-transact-sql?view=sql-server-ver16
    | ERROR_NUMBER LPAREN RPAREN # ERROR_NUMBER
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/error-procedure-transact-sql?view=sql-server-ver16
    | ERROR_PROCEDURE LPAREN RPAREN # ERROR_PROCEDURE
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/error-severity-transact-sql?view=sql-server-ver16
    | ERROR_SEVERITY LPAREN RPAREN # ERROR_SEVERITY
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/error-state-transact-sql?view=sql-server-ver16
    | ERROR_STATE LPAREN RPAREN # ERROR_STATE
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/formatmessage-transact-sql?view=sql-server-ver16
    | FORMATMESSAGE LPAREN (msgNumber = INT | msgString = STRING | msgVariable = LOCAL_ID) COMMA expression (
        COMMA expression
    )* RPAREN # FORMATMESSAGE
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/get-filestream-transaction-context-transact-sql?view=sql-server-ver16
    | GET_FILESTREAM_TRANSACTION_CONTEXT LPAREN RPAREN # GET_FILESTREAM_TRANSACTION_CONTEXT
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/getansinull-transact-sql?view=sql-server-ver16
    | GETANSINULL LPAREN (database = STRING)? RPAREN # GETANSINULL
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/host-id-transact-sql?view=sql-server-ver16
    | HOST_ID LPAREN RPAREN # HOST_ID
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/host-name-transact-sql?view=sql-server-ver16
    | HOST_NAME LPAREN RPAREN # HOST_NAME
    // https://msdn.microsoft.com/en-us/library/ms184325.aspx
    | ISNULL LPAREN left = expression COMMA right = expression RPAREN # ISNULL
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/isnumeric-transact-sql?view=sql-server-ver16
    | ISNUMERIC LPAREN expression RPAREN # ISNUMERIC
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/min-active-rowversion-transact-sql?view=sql-server-ver16
    | MIN_ACTIVE_ROWVERSION LPAREN RPAREN # MIN_ACTIVE_ROWVERSION
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/newid-transact-sql?view=sql-server-ver16
    | NEWID LPAREN RPAREN # NEWID
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/newsequentialid-transact-sql?view=sql-server-ver16
    | NEWSEQUENTIALID LPAREN RPAREN # NEWSEQUENTIALID
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/rowcount-big-transact-sql?view=sql-server-ver16
    | ROWCOUNT_BIG LPAREN RPAREN # ROWCOUNT_BIG
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/session-context-transact-sql?view=sql-server-ver16
    | SESSION_CONTEXT LPAREN key = STRING RPAREN # SESSION_CONTEXT
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/xact-state-transact-sql?view=sql-server-ver16
    | XACT_STATE LPAREN RPAREN # XACT_STATE
    // https://msdn.microsoft.com/en-us/library/hh231076.aspx
    // https://msdn.microsoft.com/en-us/library/ms187928.aspx
    | CAST LPAREN expression AS dataType RPAREN     # CAST
    | TRY_CAST LPAREN expression AS dataType RPAREN # TRY_CAST
    | CONVERT LPAREN convertDataType = dataType COMMA convertExpression = expression (
        COMMA style = expression
    )? RPAREN # CONVERT
    // https://msdn.microsoft.com/en-us/library/ms190349.aspx
    | COALESCE LPAREN expressionList_ RPAREN # COALESCE
    // Cursor functions
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/cursor-rows-transact-sql?view=sql-server-ver16
    | CURSOR_ROWS # CURSOR_ROWS
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/cursor-rows-transact-sql?view=sql-server-ver16
    | FETCH_STATUS # FETCH_STATUS
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/cursor-status-transact-sql?view=sql-server-ver16
    | CURSOR_STATUS LPAREN scope = STRING COMMA cursor = expression RPAREN # CURSOR_STATUS
    // Cryptographic functions
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/cert-id-transact-sql?view=sql-server-ver16
    | CERT_ID LPAREN certName = expression RPAREN # CERT_ID
    // Data type functions
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/datalength-transact-sql?view=sql-server-ver16
    | DATALENGTH LPAREN expression RPAREN # DATALENGTH
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/ident-current-transact-sql?view=sql-server-ver16
    | IDENT_CURRENT LPAREN tableOrView = expression RPAREN # IDENT_CURRENT
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/ident-incr-transact-sql?view=sql-server-ver16
    | IDENT_INCR LPAREN tableOrView = expression RPAREN # IDENT_INCR
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/ident-seed-transact-sql?view=sql-server-ver16
    | IDENT_SEED LPAREN tableOrView = expression RPAREN # IDENT_SEED
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/ident-seed-transact-sql?view=sql-server-ver16
    | IDENTITY LPAREN datatype = dataType (COMMA seed = INT COMMA increment = INT)? RPAREN # IDENTITY
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/ident-seed-transact-sql?view=sql-server-ver16
    | SQL_VARIANT_PROPERTY LPAREN expr = expression COMMA property = STRING RPAREN # SQL_VARIANT_PROPERTY
    // Date functions
    //https://infocenter.sybase.com/help/index.jsp?topic=/com.sybase.infocenter.dc36271.1572/html/blocks/CJADIDHD.htm
    | CURRENT_DATE LPAREN RPAREN # CURRENT_DATE
    // https://msdn.microsoft.com/en-us/library/ms188751.aspx
    | CURRENT_TIMESTAMP # CURRENT_TIMESTAMP
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/current-timezone-transact-sql?view=sql-server-ver16
    | CURRENT_TIMEZONE LPAREN RPAREN # CURRENT_TIMEZONE
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/current-timezone-id-transact-sql?view=sql-server-ver16
    | CURRENT_TIMEZONE_ID LPAREN RPAREN # CURRENT_TIMEZONE_ID
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/date-bucket-transact-sql?view=sql-server-ver16
    | DATE_BUCKET LPAREN datepart = dateparts_9 COMMA number = expression COMMA date = expression (
        COMMA origin = expression
    )? RPAREN # DATE_BUCKET
    // https://msdn.microsoft.com/en-us/library/ms186819.aspx
    | DATEADD LPAREN datepart = dateparts_12 COMMA number = expression COMMA date = expression RPAREN # DATEADD
    // https://msdn.microsoft.com/en-us/library/ms189794.aspx
    | DATEDIFF LPAREN datepart = dateparts_12 COMMA dateFirst = expression COMMA dateSecond = expression RPAREN # DATEDIFF
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/datediff-big-transact-sql?view=sql-server-ver16
    | DATEDIFF_BIG LPAREN datepart = dateparts_12 COMMA startdate = expression COMMA enddate = expression RPAREN # DATEDIFF_BIG
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/datefromparts-transact-sql?view=sql-server-ver16
    | DATEFROMPARTS LPAREN year = expression COMMA month = expression COMMA day = expression RPAREN # DATEFROMPARTS
    // https://msdn.microsoft.com/en-us/library/ms174395.aspx
    | DATENAME LPAREN datepart = dateparts_15 COMMA date = expression RPAREN # DATENAME
    // https://msdn.microsoft.com/en-us/library/ms174420.aspx
    | DATEPART LPAREN datepart = dateparts_15 COMMA date = expression RPAREN # DATEPART
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/datetime2fromparts-transact-sql?view=sql-server-ver16
    | DATETIME2FROMPARTS LPAREN year = expression COMMA month = expression COMMA day = expression COMMA hour = expression COMMA minute = expression COMMA seconds =
        expression COMMA fractions = expression COMMA precision = expression RPAREN # DATETIME2FROMPARTS
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/datetimefromparts-transact-sql?view=sql-server-ver16
    | DATETIMEFROMPARTS LPAREN year = expression COMMA month = expression COMMA day = expression COMMA hour = expression COMMA minute = expression COMMA seconds =
        expression COMMA milliseconds = expression RPAREN # DATETIMEFROMPARTS
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/datetimeoffsetfromparts-transact-sql?view=sql-server-ver16
    | DATETIMEOFFSETFROMPARTS LPAREN year = expression COMMA month = expression COMMA day = expression COMMA hour = expression COMMA minute = expression COMMA
        seconds = expression COMMA fractions = expression COMMA hourOffset = expression COMMA minuteOffset = expression COMMA precision = INT RPAREN #
        DATETIMEOFFSETFROMPARTS
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/datetrunc-transact-sql?view=sql-server-ver16
    | DATETRUNC LPAREN datepart = datepartsDatetrunc COMMA date = expression RPAREN # DATETRUNC
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/day-transact-sql?view=sql-server-ver16
    | DAY LPAREN date = expression RPAREN # DAY
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/eomonth-transact-sql?view=sql-server-ver16
    | EOMONTH LPAREN startDate = expression (COMMA monthToAdd = expression)? RPAREN # EOMONTH
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/getdate-transact-sql
    | GETDATE LPAREN RPAREN # GETDATE
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/getdate-transact-sql
    | GETUTCDATE LPAREN RPAREN # GETUTCDATE
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/isdate-transact-sql?view=sql-server-ver16
    | ISDATE LPAREN expression RPAREN # ISDATE
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/month-transact-sql?view=sql-server-ver16
    | MONTH LPAREN date = expression RPAREN # MONTH
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/smalldatetimefromparts-transact-sql?view=sql-server-ver16
    | SMALLDATETIMEFROMPARTS LPAREN year = expression COMMA month = expression COMMA day = expression COMMA hour = expression COMMA minute = expression RPAREN #
        SMALLDATETIMEFROMPARTS
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/switchoffset-transact-sql?view=sql-server-ver16
    | SWITCHOFFSET LPAREN datetimeoffsetExpression = expression COMMA timezoneoffsetExpression = expression RPAREN # SWITCHOFFSET
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/sysdatetime-transact-sql?view=sql-server-ver16
    | SYSDATETIME LPAREN RPAREN # SYSDATETIME
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/sysdatetimeoffset-transact-sql?view=sql-server-ver16
    | SYSDATETIMEOFFSET LPAREN RPAREN # SYSDATETIMEOFFSET
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/sysutcdatetime-transact-sql?view=sql-server-ver16
    | SYSUTCDATETIME LPAREN RPAREN # SYSUTCDATETIME
    //https://learn.microsoft.com/en-us/sql/t-sql/functions/timefromparts-transact-sql?view=sql-server-ver16
    | TIMEFROMPARTS LPAREN hour = expression COMMA minute = expression COMMA seconds = expression COMMA fractions = expression COMMA precision = INT RPAREN #
        TIMEFROMPARTS
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/todatetimeoffset-transact-sql?view=sql-server-ver16
    | TODATETIMEOFFSET LPAREN datetimeExpression = expression COMMA timezoneoffsetExpression = expression RPAREN # TODATETIMEOFFSET
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/year-transact-sql?view=sql-server-ver16
    | YEAR LPAREN date = expression RPAREN # YEAR
    // https://msdn.microsoft.com/en-us/library/ms189838.aspx
    | IDENTITY LPAREN dataType (COMMA seed = INT)? (COMMA increment = INT)? RPAREN # IDENTITY
    // https://msdn.microsoft.com/en-us/library/bb839514.aspx
    | MIN_ACTIVE_ROWVERSION LPAREN RPAREN # MIN_ACTIVE_ROWVERSION
    // https://msdn.microsoft.com/en-us/library/ms177562.aspx
    | NULLIF LPAREN left = expression COMMA right = expression RPAREN # NULLIF
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/parse-transact-sql
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/try-parse-transact-sql
    | PARSE LPAREN str = expression AS dataType (USING culture = expression)? RPAREN # PARSE
    // https://docs.microsoft.com/en-us/sql/t-sql/xml/xml-data-type-methods
    | xmlDataTypeMethods # XML_DATA_TYPE_FUNC
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/logical-functions-iif-transact-sql
    | IIF LPAREN cond = searchCondition COMMA left = expression COMMA right = expression RPAREN # IIF
    // JSON functions
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/isjson-transact-sql?view=azure-sqldw-latest
    | ISJSON LPAREN jsonExpr = expression (COMMA jsonTypeConstraint = expression)? RPAREN # ISJSON
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/json-object-transact-sql?view=azure-sqldw-latest
    | JSON_OBJECT LPAREN (keyValue = jsonKeyValue (COMMA keyValue = jsonKeyValue)*)? jsonNullClause? RPAREN # JSON_OBJECT
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/json-array-transact-sql?view=azure-sqldw-latest
    | JSON_ARRAY LPAREN expressionList_? jsonNullClause? RPAREN # JSON_ARRAY
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/json-value-transact-sql?view=azure-sqldw-latest
    | JSON_VALUE LPAREN expr = expression COMMA path = expression RPAREN # JSON_VALUE
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/json-query-transact-sql?view=azure-sqldw-latest
    | JSON_QUERY LPAREN expr = expression (COMMA path = expression)? RPAREN # JSON_QUERY
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/json-modify-transact-sql?view=azure-sqldw-latest
    | JSON_MODIFY LPAREN expr = expression COMMA path = expression COMMA newValue = expression RPAREN # JSON_MODIFY
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/json-path-exists-transact-sql?view=azure-sqldw-latest
    | JSON_PATH_EXISTS LPAREN valueExpression = expression COMMA sqlJsonPath = expression RPAREN # JSON_PATH_EXISTS
    // Math functions
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/abs-transact-sql?view=sql-server-ver16
    | ABS LPAREN numericExpression = expression RPAREN # ABS
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/acos-transact-sql?view=sql-server-ver16
    | ACOS LPAREN floatExpression = expression RPAREN # ACOS
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/asin-transact-sql?view=sql-server-ver16
    | ASIN LPAREN floatExpression = expression RPAREN # ASIN
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/atan-transact-sql?view=sql-server-ver16
    | ATAN LPAREN floatExpression = expression RPAREN # ATAN
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/atn2-transact-sql?view=sql-server-ver16
    | ATN2 LPAREN floatExpression = expression COMMA floatExpression = expression RPAREN # ATN2
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/ceiling-transact-sql?view=sql-server-ver16
    | CEILING LPAREN numericExpression = expression RPAREN # CEILING
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/cos-transact-sql?view=sql-server-ver16
    | COS LPAREN floatExpression = expression RPAREN # COS
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/cot-transact-sql?view=sql-server-ver16
    | COT LPAREN floatExpression = expression RPAREN # COT
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/degrees-transact-sql?view=sql-server-ver16
    | DEGREES LPAREN numericExpression = expression RPAREN # DEGREES
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/exp-transact-sql?view=sql-server-ver16
    | EXP LPAREN floatExpression = expression RPAREN # EXP
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/floor-transact-sql?view=sql-server-ver16
    | FLOOR LPAREN numericExpression = expression RPAREN # FLOOR
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/log-transact-sql?view=sql-server-ver16
    | LOG LPAREN floatExpression = expression (COMMA base = expression)? RPAREN # LOG
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/log10-transact-sql?view=sql-server-ver16
    | LOG10 LPAREN floatExpression = expression RPAREN # LOG10
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/pi-transact-sql?view=sql-server-ver16
    | PI LPAREN RPAREN # PI
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/power-transact-sql?view=sql-server-ver16
    | POWER LPAREN floatExpression = expression COMMA y = expression RPAREN # POWER
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/radians-transact-sql?view=sql-server-ver16
    | RADIANS LPAREN numericExpression = expression RPAREN # RADIANS
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/rand-transact-sql?view=sql-server-ver16
    | RAND LPAREN (seed = expression)? RPAREN # RAND
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/round-transact-sql?view=sql-server-ver16
    | ROUND LPAREN numericExpression = expression COMMA length = expression (COMMA function = expression)? RPAREN # ROUND
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/sign-transact-sql?view=sql-server-ver16
    | SIGN LPAREN numericExpression = expression RPAREN # MATH_SIGN
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/sin-transact-sql?view=sql-server-ver16
    | SIN LPAREN floatExpression = expression RPAREN # SIN
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/sqrt-transact-sql?view=sql-server-ver16
    | SQRT LPAREN floatExpression = expression RPAREN # SQRT
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/square-transact-sql?view=sql-server-ver16
    | SQUARE LPAREN floatExpression = expression RPAREN # SQUARE
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/tan-transact-sql?view=sql-server-ver16
    | TAN LPAREN floatExpression = expression RPAREN # TAN
    // Logical functions
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/logical-functions-greatest-transact-sql?view=azure-sqldw-latest
    | GREATEST LPAREN expressionList_ RPAREN # GREATEST
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/logical-functions-least-transact-sql?view=azure-sqldw-latest
    | LEAST LPAREN expressionList_ RPAREN # LEAST
    // Security functions
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/certencoded-transact-sql?view=sql-server-ver16
    | CERTENCODED LPAREN certid = expression RPAREN # CERTENCODED
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/certprivatekey-transact-sql?view=sql-server-ver16
    | CERTPRIVATEKEY LPAREN certid = expression COMMA encryptionPassword = expression (
        COMMA decryptionPasword = expression
    )? RPAREN # CERTPRIVATEKEY
    // https://msdn.microsoft.com/en-us/library/ms176050.aspx
    | CURRENT_USER # CURRENT_USER
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/database-principal-id-transact-sql?view=sql-server-ver16
    | DATABASE_PRINCIPAL_ID LPAREN (principalName = expression)? RPAREN # DATABASE_PRINCIPAL_ID
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/has-dbaccess-transact-sql?view=sql-server-ver16
    | HAS_DBACCESS LPAREN databaseName = expression RPAREN # HAS_DBACCESS
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/has-perms-by-name-transact-sql?view=sql-server-ver16
    | HAS_PERMS_BY_NAME LPAREN securable = expression COMMA securableClass = expression COMMA permission = expression (
        COMMA subSecurable = expression (COMMA subSecurableClass = expression)?
    )? RPAREN # HAS_PERMS_BY_NAME
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/is-member-transact-sql?view=sql-server-ver16
    | IS_MEMBER LPAREN groupOrRole = expression RPAREN # IS_MEMBER
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/is-rolemember-transact-sql?view=sql-server-ver16
    | IS_ROLEMEMBER LPAREN role = expression (COMMA databasePrincipal = expression)? RPAREN # IS_ROLEMEMBER
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/is-srvrolemember-transact-sql?view=sql-server-ver16
    | IS_SRVROLEMEMBER LPAREN role = expression (COMMA login = expression)? RPAREN # IS_SRVROLEMEMBER
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/loginproperty-transact-sql?view=sql-server-ver16
    | LOGINPROPERTY LPAREN loginName = expression COMMA propertyName = expression RPAREN # LOGINPROPERTY
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/original-login-transact-sql?view=sql-server-ver16
    | ORIGINAL_LOGIN LPAREN RPAREN # ORIGINAL_LOGIN
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/permissions-transact-sql?view=sql-server-ver16
    | PERMISSIONS LPAREN (objectId = expression (COMMA column = expression)?)? RPAREN # PERMISSIONS
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/pwdencrypt-transact-sql?view=sql-server-ver16
    | PWDENCRYPT LPAREN password = expression RPAREN # PWDENCRYPT
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/pwdcompare-transact-sql?view=sql-server-ver16
    | PWDCOMPARE LPAREN clearTextPassword = expression COMMA passwordHash = expression (
        COMMA version = expression
    )? RPAREN # PWDCOMPARE
    // https://msdn.microsoft.com/en-us/library/ms177587.aspx
    | SESSION_USER # SESSION_USER
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/sessionproperty-transact-sql?view=sql-server-ver16
    | SESSIONPROPERTY LPAREN optionName = expression RPAREN # SESSIONPROPERTY
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/suser-id-transact-sql?view=sql-server-ver16
    | SUSER_ID LPAREN (login = expression)? RPAREN # SUSER_ID
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/suser-name-transact-sql?view=sql-server-ver16
    | SUSER_NAME LPAREN (serverUserSid = expression)? RPAREN # SUSER_SNAME
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/suser-sid-transact-sql?view=sql-server-ver16
    | SUSER_SID LPAREN (login = expression (COMMA param2 = expression)?)? RPAREN # SUSER_SID
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/suser-sname-transact-sql?view=sql-server-ver16
    | SUSER_SNAME LPAREN (serverUserSid = expression)? RPAREN # SUSER_SNAME
    // https://msdn.microsoft.com/en-us/library/ms179930.aspx
    | SYSTEM_USER # SYSTEM_USER
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/user-transact-sql?view=sql-server-ver16
    | USER # USER
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/user-id-transact-sql?view=sql-server-ver16
    | USER_ID LPAREN (user = expression)? RPAREN # USER_ID
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/user-name-transact-sql?view=sql-server-ver16
    | USER_NAME LPAREN (id = expression)? RPAREN # USER_NAME
    ;

xmlDataTypeMethods
    : valueMethod
    | queryMethod
    | existMethod
    | modifyMethod
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/functions/date-bucket-transact-sql?view=sql-server-ver16
dateparts_9
    : YEAR
    | YEAR_ABBR
    | QUARTER
    | QUARTER_ABBR
    | MONTH
    | MONTH_ABBR
    | DAY
    | DAY_ABBR
    | WEEK
    | WEEK_ABBR
    | HOUR
    | HOUR_ABBR
    | MINUTE
    | MINUTE_ABBR
    | SECOND
    | SECOND_ABBR
    | MILLISECOND
    | MILLISECOND_ABBR
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/functions/dateadd-transact-sql?view=sql-server-ver16
dateparts_12
    : dateparts_9
    | DAYOFYEAR
    | DAYOFYEAR_ABBR
    | MICROSECOND
    | MICROSECOND_ABBR
    | NANOSECOND
    | NANOSECOND_ABBR
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/functions/datename-transact-sql?view=sql-server-ver16
dateparts_15
    : dateparts_12
    | WEEKDAY
    | WEEKDAY_ABBR
    | TZOFFSET
    | TZOFFSET_ABBR
    | ISO_WEEK
    | ISO_WEEK_ABBR
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/functions/datetrunc-transact-sql?view=sql-server-ver16
datepartsDatetrunc
    : dateparts_9
    | DAYOFYEAR
    | DAYOFYEAR_ABBR
    | MICROSECOND
    | MICROSECOND_ABBR
    | ISO_WEEK
    | ISO_WEEK_ABBR
    ;

valueMethod
    : (
        locId = LOCAL_ID
        | valueId = fullColumnName
        | eventdata = EVENTDATA LPAREN RPAREN
        | query = queryMethod
        | LPAREN subquery RPAREN
    ) DOT call = valueCall
    ;

valueCall
    : (VALUE | VALUE_SQUARE_BRACKET) LPAREN xquery = STRING COMMA sqltype = STRING RPAREN
    ;

queryMethod
    : (locId = LOCAL_ID | valueId = fullColumnName | LPAREN subquery RPAREN) DOT call = queryCall
    ;

queryCall
    : (QUERY | QUERY_SQUARE_BRACKET) LPAREN xquery = STRING RPAREN
    ;

existMethod
    : (locId = LOCAL_ID | valueId = fullColumnName | LPAREN subquery RPAREN) DOT call = existCall
    ;

existCall
    : (EXIST | EXIST_SQUARE_BRACKET) LPAREN xquery = STRING RPAREN
    ;

modifyMethod
    : (locId = LOCAL_ID | valueId = fullColumnName | LPAREN subquery RPAREN) DOT call = modifyCall
    ;

modifyCall
    : (MODIFY | MODIFY_SQUARE_BRACKET) LPAREN xmlDml = STRING RPAREN
    ;

hierarchyidCall
    : GETANCESTOR LPAREN n = expression RPAREN
    | GETDESCENDANT LPAREN child1 = expression COMMA child2 = expression RPAREN
    | GETLEVEL LPAREN RPAREN
    | ISDESCENDANTOF LPAREN parent_ = expression RPAREN
    | GETREPARENTEDVALUE LPAREN oldroot = expression COMMA newroot = expression RPAREN
    | TOSTRING LPAREN RPAREN
    ;

hierarchyidStaticMethod
    : HIERARCHYID DOUBLE_COLON (GETROOT LPAREN RPAREN | PARSE LPAREN input = expression RPAREN)
    ;

nodesMethod
    : (locId = LOCAL_ID | valueId = fullColumnName | LPAREN subquery RPAREN) DOT NODES LPAREN xquery = STRING RPAREN
    ;

switchSection
    : WHEN expression THEN expression
    ;

switchSearchConditionSection
    : WHEN searchCondition THEN expression
    ;

asColumnAlias
    : AS? columnAlias
    ;

asTableAlias
    : AS? tableAlias
    ;

tableAlias
    : id_
    ;

// https://msdn.microsoft.com/en-us/library/ms187373.aspx
withTableHints
    : WITH LPAREN hint += tableHint (COMMA? hint += tableHint)* RPAREN
    ;

deprecatedTableHint
    : LPAREN tableHint RPAREN
    ;

// https://infocenter-archive.sybase.com/help/index.jsp?topic=/com.sybase.infocenter.dc00938.1502/html/locking/locking103.htm
// https://infocenter-archive.sybase.com/help/index.jsp?topic=/com.sybase.dc32300_1250/html/sqlug/sqlug792.htm
// https://infocenter-archive.sybase.com/help/index.jsp?topic=/com.sybase.dc36271_36272_36273_36274_1250/html/refman/X35229.htm
// Legacy hint with no parenthesis and no WITH keyword. Actually conflicts with table alias name except for holdlock which is
// a reserved keyword in this grammar. We might want a separate sybase grammar variant.
sybaseLegacyHints
    : sybaseLegacyHint+
    ;

sybaseLegacyHint
    : HOLDLOCK
    | NOHOLDLOCK
    | READPAST
    | SHARED
    ;

// For simplicity, we don't build subsets for INSERT/UPDATE/DELETE/SELECT/MERGE
// which means the grammar accept slightly more than the what the specification (documentation) says.
tableHint
    : NOEXPAND
    | INDEX (
        LPAREN indexValue (COMMA indexValue)* RPAREN
        | EQ LPAREN indexValue RPAREN
        | EQ indexValue // examples in the doc include this syntax
    )
    | FORCESEEK ( LPAREN indexValue LPAREN columnNameList RPAREN RPAREN)?
    | FORCESCAN
    | HOLDLOCK
    | NOLOCK
    | NOWAIT
    | PAGLOCK
    | READCOMMITTED
    | READCOMMITTEDLOCK
    | READPAST
    | READUNCOMMITTED
    | REPEATABLEREAD
    | ROWLOCK
    | SERIALIZABLE
    | SNAPSHOT
    | SPATIAL_WINDOW_MAX_CELLS EQ INT
    | TABLOCK
    | TABLOCKX
    | UPDLOCK
    | XLOCK
    | KEEPIDENTITY
    | KEEPDEFAULTS
    | IGNORE_CONSTRAINTS
    | IGNORE_TRIGGERS
    ;

indexValue
    : id_
    | INT
    ;

columnAliasList
    : LPAREN alias += columnAlias (COMMA alias += columnAlias)* RPAREN
    ;

columnAlias
    : id_
    | STRING
    ;

tableValueConstructor
    : VALUES LPAREN exps += expressionList_ RPAREN (COMMA LPAREN exps += expressionList_ RPAREN)*
    ;

expressionList_
    : exp += expression (COMMA exp += expression)*
    ;

// https://msdn.microsoft.com/en-us/library/ms189798.aspx
rankingWindowedFunction
    : (RANK | DENSE_RANK | ROW_NUMBER) LPAREN RPAREN overClause
    | NTILE LPAREN expression RPAREN overClause
    ;

// https://msdn.microsoft.com/en-us/library/ms173454.aspx
aggregateWindowedFunction
    : aggFunc = (AVG | MAX | MIN | SUM | STDEV | STDEVP | VAR | VARP) LPAREN allDistinctExpression RPAREN overClause?
    | cnt = (COUNT | COUNT_BIG) LPAREN (STAR | allDistinctExpression) RPAREN overClause?
    | CHECKSUM_AGG LPAREN allDistinctExpression RPAREN
    | GROUPING LPAREN expression RPAREN
    | GROUPING_ID LPAREN expressionList_ RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/functions/analytic-functions-transact-sql
analyticWindowedFunction
    : (FIRST_VALUE | LAST_VALUE) LPAREN expression RPAREN overClause
    | (LAG | LEAD) LPAREN expression (COMMA expression (COMMA expression)?)? RPAREN overClause
    | (CUME_DIST | PERCENT_RANK) LPAREN RPAREN OVER LPAREN (PARTITION BY expressionList_)? orderByClause RPAREN
    | (PERCENTILE_CONT | PERCENTILE_DISC) LPAREN expression RPAREN WITHIN GROUP LPAREN orderByClause RPAREN OVER LPAREN (
        PARTITION BY expressionList_
    )? RPAREN
    ;

allDistinctExpression
    : (ALL | DISTINCT)? expression
    ;

// https://msdn.microsoft.com/en-us/library/ms189461.aspx
overClause
    : OVER LPAREN (PARTITION BY expressionList_)? orderByClause? rowOrRangeClause? RPAREN
    ;

rowOrRangeClause
    : (ROWS | RANGE) windowFrameExtent
    ;

windowFrameExtent
    : windowFramePreceding
    | BETWEEN windowFrameBound AND windowFrameBound
    ;

windowFrameBound
    : windowFramePreceding
    | windowFrameFollowing
    ;

windowFramePreceding
    : UNBOUNDED PRECEDING
    | INT PRECEDING
    | CURRENT ROW
    ;

windowFrameFollowing
    : UNBOUNDED FOLLOWING
    | INT FOLLOWING
    ;

createDatabaseOption
    : FILESTREAM (databaseFilestreamOption (COMMA databaseFilestreamOption)*)
    | DEFAULT_LANGUAGE EQ ( id_ | STRING)
    | DEFAULT_FULLTEXT_LANGUAGE EQ ( id_ | STRING)
    | NESTED_TRIGGERS EQ ( OFF | ON)
    | TRANSFORM_NOISE_WORDS EQ ( OFF | ON)
    | TWO_DIGIT_YEAR_CUTOFF EQ INT
    | DB_CHAINING ( OFF | ON)
    | TRUSTWORTHY ( OFF | ON)
    ;

databaseFilestreamOption
    : LPAREN (
        ( NON_TRANSACTED_ACCESS EQ ( OFF | READ_ONLY | FULL))
        | ( DIRECTORY_NAME EQ STRING)
    ) RPAREN
    ;

databaseFileSpec
    : fileGroup
    | fileSpecification
    ;

fileGroup
    : FILEGROUP id_ (CONTAINS FILESTREAM)? (DEFAULT)? (CONTAINS MEMORY_OPTIMIZED_DATA)? fileSpecification (
        COMMA fileSpecification
    )*
    ;

fileSpecification
    : LPAREN NAME EQ (id_ | STRING) COMMA? FILENAME EQ file = STRING COMMA? (
        SIZE EQ fileSize COMMA?
    )? (MAXSIZE EQ (fileSize | UNLIMITED) COMMA?)? (FILEGROWTH EQ fileSize COMMA?)? RPAREN
    ;

// Primitive.
entityName
    : (
        server = id_ DOT database = id_ DOT schema = id_ DOT
        | database = id_ DOT (schema = id_)? DOT
        | schema = id_ DOT
    )? table = id_
    ;

entityNameForAzureDw
    : schema = id_
    | schema = id_ DOT objectName = id_
    ;

entityNameForParallelDw
    : schemaDatabase = id_
    | schema = id_ DOT objectName = id_
    ;

fullTableName
    : (
        linkedServer = id_ DOT DOT schema = id_ DOT
        | server = id_ DOT database = id_ DOT schema = id_ DOT
        | database = id_ DOT schema = id_? DOT
        | schema = id_ DOT
    )? table = id_
    ;

tableName
    : (database = id_ DOT schema = id_? DOT | schema = id_ DOT)? (
        table = id_
        | blockingHierarchy = BLOCKING_HIERARCHY
    )
    ;

simpleName
    : (schema = id_ DOT)? name = id_
    ;

funcProcNameSchema
    : ((schema = id_) DOT)? procedure = id_
    ;

funcProcNameDatabaseSchema
    : database = id_? DOT schema = id_? DOT procedure = id_
    | funcProcNameSchema
    ;

funcProcNameServerDatabaseSchema
    : server = id_? DOT database = id_? DOT schema = id_? DOT procedure = id_
    | funcProcNameDatabaseSchema
    ;

ddlObject
    : fullTableName
    | LOCAL_ID
    ;

fullColumnName
    : ((DELETED | INSERTED | fullTableName) DOT)? (
        columnName = id_
        | (DOLLAR (IDENTITY | ROWGUID))
    )
    ;

columnNameListWithOrder
    : id_ (ASC | DESC)? (COMMA id_ (ASC | DESC)?)*
    ;

//For some reason, sql server allows any number of prefixes:  Here, h is the column: a.b.c.d.e.f.g.h
insertColumnNameList
    : col += insertColumnId (COMMA col += insertColumnId)*
    ;

insertColumnId
    : (ignore += id_? DOT)* id_
    ;

columnNameList
    : col += id_ (COMMA col += id_)*
    ;

cursorName
    : id_
    | LOCAL_ID
    ;

onOff
    : ON
    | OFF
    ;

clustered
    : CLUSTERED
    | NONCLUSTERED
    ;

nullNotnull
    : NOT? NULL_
    ;

scalarFunctionName
    : funcProcNameServerDatabaseSchema
    | RIGHT
    | LEFT
    | BINARY_CHECKSUM
    | CHECKSUM
    ;

beginConversationTimer
    : BEGIN CONVERSATION TIMER LPAREN LOCAL_ID RPAREN TIMEOUT EQ time SEMI?
    ;

beginConversationDialog
    : BEGIN DIALOG (CONVERSATION)? dialogHandle = LOCAL_ID FROM SERVICE initiatorServiceName = serviceName TO SERVICE targetServiceName =
        serviceName (COMMA serviceBrokerGuid = STRING)? ON CONTRACT contractName (
        WITH ((RELATED_CONVERSATION | RELATED_CONVERSATION_GROUP) EQ LOCAL_ID COMMA?)? (
            LIFETIME EQ (INT | LOCAL_ID) COMMA?
        )? (ENCRYPTION EQ onOff)?
    )? SEMI?
    ;

contractName
    : (id_ | expression)
    ;

serviceName
    : (id_ | expression)
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
    : WAITFOR? LPAREN getConversation RPAREN (COMMA? TIMEOUT timeout = time)? SEMI?
    ;

getConversation
    : GET CONVERSATION GROUP conversationGroupId = (STRING | LOCAL_ID) FROM queue = queueId SEMI?
    ;

queueId
    : (databaseName = id_ DOT schemaName = id_ DOT name = id_)
    | id_
    ;

sendConversation
    : SEND ON CONVERSATION conversationHandle = (STRING | LOCAL_ID) MESSAGE TYPE messageTypeName = expression (
        LPAREN messageBodyExpression = (STRING | LOCAL_ID) RPAREN
    )? SEMI?
    ;

// https://msdn.microsoft.com/en-us/library/ms187752.aspx
// TODO: implement runtime check or add new tokens.

dataType
    : scaled = (VARCHAR | NVARCHAR | BINARY_KEYWORD | VARBINARY_KEYWORD | SQUARE_BRACKET_ID) LPAREN MAX RPAREN
    | extType = id_ LPAREN scale = INT COMMA prec = INT RPAREN
    | extType = id_ LPAREN scale = INT RPAREN
    | extType = id_ IDENTITY (LPAREN seed = INT COMMA inc = INT RPAREN)?
    | doublePrec = DOUBLE PRECISION?
    | unscaledType = id_
    ;

// https://msdn.microsoft.com/en-us/library/ms179899.aspx
constant
    : STRING // string, datetime or uniqueidentifier
    | HEX
    | MINUS? (INT | REAL | FLOAT)                    // float or decimal
    | MINUS? DOLLAR (MINUS | PLUS)? (INT | FLOAT) // money
    | parameter
    ;

// To reduce ambiguity, -X is considered as an application of unary operator
primitiveConstant
    : STRING // string, datetime or uniqueidentifier
    | HEX
    | INT
    | REAL
    | FLOAT
    | DOLLAR (MINUS | PLUS)? (INT | FLOAT) // money
    | parameter
    ;

keyword
    : ABORT
    | ABSOLUTE
    | ACCENT_SENSITIVITY
    | ACCESS
    | ACTION
    | ACTIVATION
    | ACTIVE
    | ADD // ?
    | ADDRESS
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
    | ALLOW_ENCRYPTED_VALUE_MODIFICATIONS
    | ALLOW_PAGE_LOCKS
    | ALLOW_ROW_LOCKS
    | ALLOW_SNAPSHOT_ISOLATION
    | ALLOWED
    | ALWAYS
    | ANSI_DEFAULTS
    | ANSI_NULL_DEFAULT
    | ANSI_NULL_DFLT_OFF
    | ANSI_NULL_DFLT_ON
    | ANSI_NULLS
    | ANSI_PADDING
    | ANSI_WARNINGS
    | APP_NAME
    | APPLICATION_LOG
    | APPLOCK_MODE
    | APPLOCK_TEST
    | APPLY
    | ARITHABORT
    | ARITHIGNORE
    | ASCII
    | ASSEMBLY
    | ASSEMBLYPROPERTY
    | AT_KEYWORD
    | AUDIT
    | AUDIT_GUID
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
    | AVAILABILITY
    | AVG
    | BACKUP_CLONEDB
    | BACKUP_PRIORITY
    | BASE64
    | BEGIN_DIALOG
    | BIGINT
    | BINARY_KEYWORD
    | BINARY_CHECKSUM
    | BINDING
    | BLOB_STORAGE
    | BROKER
    | BROKER_INSTANCE
    | BULK_LOGGED
    | CALLER
    | CAP_CPU_PERCENT
    | CAST
    | TRY_CAST
    | CATALOG
    | CATCH
    | CERT_ID
    | CERTENCODED
    | CERTPRIVATEKEY
    | CHANGE
    | CHANGE_RETENTION
    | CHANGE_TRACKING
    | CHAR
    | CHARINDEX
    | CHECKALLOC
    | CHECKCATALOG
    | CHECKCONSTRAINTS
    | CHECKDB
    | CHECKFILEGROUP
    | CHECKSUM
    | CHECKSUM_AGG
    | CHECKTABLE
    | CLEANTABLE
    | CLEANUP
    | CLONEDATABASE
    | COL_LENGTH
    | COL_NAME
    | COLLECTION
    | COLUMN_ENCRYPTION_KEY
    | COLUMN_MASTER_KEY
    | COLUMNPROPERTY
    | COLUMNS
    | COLUMNSTORE
    | COLUMNSTORE_ARCHIVE
    | COMMITTED
    | COMPATIBILITY_LEVEL
    | COMPRESS_ALL_ROW_GROUPS
    | COMPRESSION_DELAY
    | CONCAT
    | CONCAT_WS
    | CONCAT_NULL_YIELDS_NULL
    | CONTENT
    | CONTROL
    | COOKIE
    | COUNT
    | COUNT_BIG
    | COUNTER
    | CPU
    | CREATE_NEW
    | CREATION_DISPOSITION
    | CREDENTIAL
    | CRYPTOGRAPHIC
    | CUME_DIST
    | CURSOR_CLOSE_ON_COMMIT
    | CURSOR_DEFAULT
    | CURSOR_STATUS
    | DATA
    | DATA_PURITY
    | DATABASE_PRINCIPAL_ID
    | DATABASEPROPERTYEX
    | DATALENGTH
    | DATE_CORRELATION_OPTIMIZATION
    | DATEADD
    | DATEDIFF
    | DATENAME
    | DATEPART
    | DAYS
    | DB_CHAINING
    | DB_FAILOVER
    | DB_ID
    | DB_NAME
    | DBCC
    | DBREINDEX
    | DECRYPTION
    | DEFAULT_DOUBLE_QUOTE
    | DEFAULT_FULLTEXT_LANGUAGE
    | DEFAULT_LANGUAGE
    | DEFINITION
    | DELAY
    | DELAYED_DURABILITY
    | DELETED
    | DENSE_RANK
    | DEPENDENTS
    | DES
    | DESCRIPTION
    | DESX
    | DETERMINISTIC
    | DHCP
    | DIALOG
    | DIFFERENCE
    | DIRECTORY_NAME
    | DISABLE
    | DISABLE_BROKER
    | DISABLED
    | DOCUMENT
    | DROP_EXISTING
    | DROPCLEANBUFFERS
    | DYNAMIC
    | ELEMENTS
    | EMERGENCY
    | EMPTY
    | ENABLE
    | ENABLE_BROKER
    | ENCRYPTED
    | ENCRYPTED_VALUE
    | ENCRYPTION
    | ENCRYPTION_TYPE
    | ENDPOINT_URL
    | ERROR_BROKER_CONVERSATIONS
    | ESTIMATEONLY
    | EXCLUSIVE
    | EXECUTABLE
    | EXIST
    | EXIST_SQUARE_BRACKET
    | EXPAND
    | EXPIRY_DATE
    | EXPLICIT
    | EXTENDED_LOGICAL_CHECKS
    | FAIL_OPERATION
    | FAILOVER_MODE
    | FAILURE
    | FAILURE_CONDITION_LEVEL
    | FAST
    | FAST_FORWARD
    | FILE_ID
    | FILE_IDEX
    | FILE_NAME
    | FILEGROUP
    | FILEGROUP_ID
    | FILEGROUP_NAME
    | FILEGROUPPROPERTY
    | FILEGROWTH
    | FILENAME
    | FILEPATH
    | FILEPROPERTY
    | FILEPROPERTYEX
    | FILESTREAM
    | FILTER
    | FIRST
    | FIRST_VALUE
    | FMTONLY
    | FOLLOWING
    | FORCE
    | FORCE_FAILOVER_ALLOW_DATA_LOSS
    | FORCED
    | FORCEPLAN
    | FORCESCAN
    | FORMAT
    | FORWARD_ONLY
    | FREE
    | FULLSCAN
    | FULLTEXT
    | FULLTEXTCATALOGPROPERTY
    | FULLTEXTSERVICEPROPERTY
    | GB
    | GENERATED
    | GETDATE
    | GETUTCDATE
    | GLOBAL
    | GO
    | GREATEST
    | GROUP_MAX_REQUESTS
    | GROUPING
    | GROUPING_ID
    | HADR
    | HAS_DBACCESS
    | HAS_PERMS_BY_NAME
    | HASH
    | HEALTH_CHECK_TIMEOUT
    | HIDDEN_KEYWORD
    | HIGH
    | HONOR_BROKER_PRIORITY
    | HOURS
    | IDENT_CURRENT
    | IDENT_INCR
    | IDENT_SEED
    | IDENTITY_VALUE
    | IGNORE_CONSTRAINTS
    | IGNORE_DUP_KEY
    | IGNORE_NONCLUSTERED_COLUMNSTORE_INDEX
    | IGNORE_REPLICATED_TABLE_CACHE
    | IGNORE_TRIGGERS
    | IMMEDIATE
    | IMPERSONATE
    | IMPLICIT_TRANSACTIONS
    | IMPORTANCE
    | INCLUDE_NULL_VALUES
    | INCREMENTAL
    | INDEX_COL
    | INDEXKEY_PROPERTY
    | INDEXPROPERTY
    | INITIATOR
    | INPUT
    | INSENSITIVE
    | INSERTED
    | KWINT
    | IP
    | IS_MEMBER
    | IS_ROLEMEMBER
    | IS_SRVROLEMEMBER
    | ISJSON
    | ISOLATION
    | JOB
    | JSON
    | JSON_OBJECT
    | JSON_ARRAY
    | JSON_VALUE
    | JSON_QUERY
    | JSON_MODIFY
    | JSON_PATH_EXISTS
    | KB
    | KEEP
    | KEEPDEFAULTS
    | KEEPFIXED
    | KEEPIDENTITY
    | KEY_SOURCE
    | KEYS
    | KEYSET
    | LAG
    | LAST
    | LAST_VALUE
    | LEAD
    | LEAST
    | LEN
    | LEVEL
    | LIST
    | LISTENER
    | LISTENER_URL
    | LOB_COMPACTION
    | LOCAL
    | LOCATION
    | LOCK
    | LOCK_ESCALATION
    | LOGIN
    | LOGINPROPERTY
    | LOOP
    | LOW
    | LOWER
    | LTRIM
    | MANUAL
    | MARK
    | MASKED
    | MATERIALIZED
    | MAX
    | MAX_CPU_PERCENT
    | MAX_DOP
    | MAX_FILES
    | MAX_IOPS_PER_VOLUME
    | MAX_MEMORY_PERCENT
    | MAX_PROCESSES
    | MAX_QUEUE_READERS
    | MAX_ROLLOVER_FILES
    | MAXDOP
    | MAXRECURSION
    | MAXSIZE
    | MB
    | MEDIUM
    | MEMORY_OPTIMIZED_DATA
    | MESSAGE
    | MIN
    | MIN_ACTIVE_ROWVERSION
    | MIN_CPU_PERCENT
    | MIN_IOPS_PER_VOLUME
    | MIN_MEMORY_PERCENT
    | MINUTES
    | MIRROR_ADDRESS
    | MIXED_PAGE_ALLOCATION
    | MODE
    | MODIFY
    | MODIFY_SQUARE_BRACKET
    | MOVE
    | MULTI_USER
    | NAME
    | NCHAR
    | NESTED_TRIGGERS
    | NEW_ACCOUNT
    | NEW_BROKER
    | NEW_PASSWORD
    | NEWNAME
    | NEXT
    | NO
    | NO_INFOMSGS
    | NO_QUERYSTORE
    | NO_STATISTICS
    | NO_TRUNCATE
    | NO_WAIT
    | NOCOUNT
    | NODES
    | NOEXEC
    | NOEXPAND
    | NOINDEX
    | NOLOCK
    | NON_TRANSACTED_ACCESS
    | NORECOMPUTE
    | NORECOVERY
    | NOTIFICATIONS
    | NOWAIT
    | NTILE
    | NULL_DOUBLE_QUOTE
    | NUMANODE
    | NUMBER
    | NUMERIC_ROUNDABORT
    | OBJECT
    | OBJECT_DEFINITION
    | OBJECT_ID
    | OBJECT_NAME
    | OBJECT_SCHEMA_NAME
    | OBJECTPROPERTY
    | OBJECTPROPERTYEX
    | OFFLINE
    | OFFSET
    | OLD_ACCOUNT
    | ONLINE
    | ONLY
    | OPEN_EXISTING
    | OPENJSON
    | OPTIMISTIC
    | OPTIMIZE
    | OPTIMIZE_FOR_SEQUENTIAL_KEY
    | ORIGINAL_DB_NAME
    | ORIGINAL_LOGIN
    | OUT
    | OUTPUT
    | OVERRIDE
    | OWNER
    | OWNERSHIP
    | PAD_INDEX
    | PAGE_VERIFY
    | PAGECOUNT
    | PAGLOCK
    | PARAMETERIZATION
    | PARSENAME
    | PARSEONLY
    | PARTITION
    | PARTITIONS
    | PARTNER
    | PATH
    | PATINDEX
    | PAUSE
    | PDW_SHOWSPACEUSED
    | PERCENT_RANK
    | PERCENTILE_CONT
    | PERCENTILE_DISC
    | PERMISSIONS
    | PERSIST_SAMPLE_PERCENT
    | PHYSICAL_ONLY
    | POISON_MESSAGE_HANDLING
    | POOL
    | PORT
    | PRECEDING
    | PRIMARY_ROLE
    | PRIOR
    | PRIORITY
    | PRIORITY_LEVEL
    | PRIVATE
    | PRIVATE_KEY
    | PRIVILEGES
    | PROCCACHE
    | PROCEDURE_NAME
    | PROPERTY
    | PROVIDER
    | PROVIDER_KEY_NAME
    | PWDCOMPARE
    | PWDENCRYPT
    | QUERY
    | QUERY_SQUARE_BRACKET
    | QUEUE
    | QUEUE_DELAY
    | QUOTED_IDENTIFIER
    | QUOTENAME
    | RANDOMIZED
    | RANGE
    | RANK
    | RC2
    | RC4
    | RC4_128
    | READ_COMMITTED_SNAPSHOT
    | READ_ONLY
    | READ_ONLY_ROUTING_LIST
    | READ_WRITE
    | READCOMMITTED
    | READCOMMITTEDLOCK
    | READONLY
    | READPAST
    | READUNCOMMITTED
    | READWRITE
    | REBUILD
    | RECEIVE
    | RECOMPILE
    | RECOVERY
    | RECURSIVE_TRIGGERS
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
    | REPLICATE
    | REQUEST_MAX_CPU_TIME_SEC
    | REQUEST_MAX_MEMORY_GRANT_PERCENT
    | REQUEST_MEMORY_GRANT_TIMEOUT_SEC
    | REQUIRED_SYNCHRONIZED_SECONDARIES_TO_COMMIT
    | RESAMPLE
    | RESERVE_DISK_SPACE
    | RESOURCE
    | RESOURCE_MANAGER_LOCATION
    | RESTRICTED_USER
    | RESUMABLE
    | RETENTION
    | REVERSE
    | ROBUST
    | ROOT
    | ROUTE
    | ROW
    | ROW_NUMBER
    | ROWGUID
    | ROWLOCK
    | ROWS
    | RTRIM
    | SAMPLE
    | SCHEMA_ID
    | SCHEMA_NAME
    | SCHEMABINDING
    | SCOPE_IDENTITY
    | SCOPED
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
    | SERVERPROPERTY
    | SERVICEBROKER
    | SESSIONPROPERTY
    | SESSION_TIMEOUT
    | SETERROR
    | SHARE
    | SHARED
    | SHOWCONTIG
    | SHOWPLAN
    | SHOWPLAN_ALL
    | SHOWPLAN_TEXT
    | SHOWPLAN_XML
    | SIGNATURE
    | SIMPLE
    | SINGLE_USER
    | SIZE
    | SMALLINT
    | SNAPSHOT
    | SORT_IN_TEMPDB
    | SOUNDEX
    | SPACE_KEYWORD
    | SPARSE
    | SPATIAL_WINDOW_MAX_CELLS
    | SQL_VARIANT_PROPERTY
    | STANDBY
    | START_DATE
    | STATIC
    | STATISTICS_INCREMENTAL
    | STATISTICS_NORECOMPUTE
    | STATS_DATE
    | STATS_STREAM
    | STATUS
    | STATUSONLY
    | STDEV
    | STDEVP
    | STOPLIST
    | STR
    | STRING_AGG
    | STRING_ESCAPE
    | STUFF
    | SUBJECT
    | SUBSCRIBE
    | SUBSCRIPTION
    | SUBSTRING
    | SUM
    | SUSER_ID
    | SUSER_NAME
    | SUSER_SID
    | SUSER_SNAME
    | SUSPEND
    | SYMMETRIC
    | SYNCHRONOUS_COMMIT
    | SYNONYM
    | SYSTEM
    | TABLERESULTS
    | TABLOCK
    | TABLOCKX
    | TAKE
    | TARGET_RECOVERY_TIME
    | TB
    | TEXTIMAGE_ON
    | THROW
    | TIES
    | TIME
    | TIMEOUT
    | TIMER
    | TINYINT
    | TORN_PAGE_DETECTION
    | TRACKING
    | TRANSACTION_ID
    | TRANSFORM_NOISE_WORDS
    | TRANSLATE
    | TRIM
    | TRIPLE_DES
    | TRIPLE_DES_3KEY
    | TRUSTWORTHY
    | TRY
    | TSQL
    | TWO_DIGIT_YEAR_CUTOFF
    | TYPE
    | TYPE_ID
    | TYPE_NAME
    | TYPE_WARNING
    | TYPEPROPERTY
    | UNBOUNDED
    | UNCOMMITTED
    | UNICODE
    | UNKNOWN
    | UNLIMITED
    | UNMASK
    | UOW
    | UPDLOCK
    | UPPER
    | USER_ID
    | USER_NAME
    | USING
    | VALID_XML
    | VALIDATION
    | VALUE
    | VALUE_SQUARE_BRACKET
    | VAR
    | VARBINARY_KEYWORD
    | VARP
    | VERIFY_CLONEDB
    | VERSION
    | VIEW_METADATA
    | VIEWS
    | WAIT
    | WELL_FORMED_XML
    | WITHOUT_ARRAY_WRAPPER
    | WORK
    | WORKLOAD
    | XLOCK
    | XML
    | XML_COMPRESSION
    | XMLDATA
    | XMLNAMESPACES
    | XMLSCHEMA
    | XSINIL
    | ZONE
    //More keywords that can also be used as IDs
    | ABORT_AFTER_WAIT
    | ABSENT
    | ADMINISTER
    | AES
    | ALLOW_CONNECTIONS
    | ALLOW_MULTIPLE_EVENT_LOSS
    | ALLOW_SINGLE_EVENT_LOSS
    | ANONYMOUS
    | APPEND
    | APPLICATION
    | ASYMMETRIC
    | ASYNCHRONOUS_COMMIT
    | AUTHENTICATE
    | AUTHENTICATION
    | AUTOMATED_BACKUP_PREFERENCE
    | AUTOMATIC
    | AVAILABILITY_MODE
    | BEFORE
    | BLOCK
    | BLOCKERS
    | BLOCKSIZE
    | BLOCKING_HIERARCHY
    | BUFFER
    | BUFFERCOUNT
    | CACHE
    | CALLED
    | CERTIFICATE
    | CHANGETABLE
    | CHANGES
    | CHECK_POLICY
    | CHECK_EXPIRATION
    | CLASSIFIER_FUNCTION
    | CLUSTER
    | COMPRESS
    | COMPRESSION
    | CONNECT
    | CONNECTION
    | CONFIGURATION
    | CONNECTIONPROPERTY
    | CONTAINMENT
    | CONTEXT
    | CONTEXT_INFO
    | CONTINUE_AFTER_ERROR
    | CONTRACT
    | CONTRACT_NAME
    | CONVERSATION
    | COPY_ONLY
    | CURRENT_REQUEST_ID
    | CURRENT_TRANSACTION_ID
    | CYCLE
    | DATA_COMPRESSION
    | DATA_SOURCE
    | DATABASE_MIRRORING
    | DATASPACE
    | DDL
    | DECOMPRESS
    | DEFAULT_DATABASE
    | DEFAULT_SCHEMA
    | DIAGNOSTICS
    | DIFFERENTIAL
    | DISTRIBUTION
    | DTC_SUPPORT
    | ENABLED
    | ENDPOINT
    | ERROR
    | ERROR_LINE
    | ERROR_MESSAGE
    | ERROR_NUMBER
    | ERROR_PROCEDURE
    | ERROR_SEVERITY
    | ERROR_STATE
    | EVENT
    | EVENTDATA
    | EVENT_RETENTION_MODE
    | EXECUTABLE_FILE
    | EXPIREDATE
    | EXTENSION
    | EXTERNAL_ACCESS
    | FAILOVER
    | FAILURECONDITIONLEVEL
    | FAN_IN
    | FILE_SNAPSHOT
    | FORCESEEK
    | FORCE_SERVICE_ALLOW_DATA_LOSS
    | FORMATMESSAGE
    | GET
    | GET_FILESTREAM_TRANSACTION_CONTEXT
    | GETANCESTOR
    | GETANSINULL
    | GETDESCENDANT
    | GETLEVEL
    | GETREPARENTEDVALUE
    | GETROOT
    | GOVERNOR
    | HASHED
    | HEALTHCHECKTIMEOUT
    | HEAP
    | HIERARCHYID
    | HOST_ID
    | HOST_NAME
    | IIF
    | IO
    | INCLUDE
    | INCREMENT
    | INFINITE
    | INIT
    | INSTEAD
    | ISDESCENDANTOF
    | ISNULL
    | ISNUMERIC
    | KERBEROS
    | KEY_PATH
    | KEY_STORE_PROVIDER_NAME
    | LANGUAGE
    | LIBRARY
    | LIFETIME
    | LINKED
    | LINUX
    | LISTENER_IP
    | LISTENER_PORT
    | LOCAL_SERVICE_NAME
    | LOG
    | MASK
    | MATCHED
    | MASTER
    | MAX_MEMORY
    | MAXTRANSFER
    | MAXVALUE
    | MAX_DISPATCH_LATENCY
    | MAX_DURATION
    | MAX_EVENT_SIZE
    | MAX_SIZE
    | MAX_OUTSTANDING_IO_PER_VOLUME
    | MEDIADESCRIPTION
    | MEDIANAME
    | MEMBER
    | MEMORY_PARTITION_MODE
    | MESSAGE_FORWARDING
    | MESSAGE_FORWARD_SIZE
    | MINVALUE
    | MIRROR
    | MUST_CHANGE
    | NEWID
    | NEWSEQUENTIALID
    | NOFORMAT
    | NOINIT
    | NONE
    | NOREWIND
    | NOSKIP
    | NOUNLOAD
    | NO_CHECKSUM
    | NO_COMPRESSION
    | NO_EVENT_LOSS
    | NOTIFICATION
    | NTLM
    | OLD_PASSWORD
    | ON_FAILURE
    | OPERATIONS
    | PAGE
    | PARAM_NODE
    | PARTIAL
    | PASSWORD
    | PERMISSION_SET
    | PER_CPU
    | PER_DB
    | PER_NODE
    | PERSISTED
    | PLATFORM
    | POLICY
    | PREDICATE
    | PROCESS
    | PROFILE
    | PYTHON
    | R
    | READ_WRITE_FILEGROUPS
    | REGENERATE
    | RELATED_CONVERSATION
    | RELATED_CONVERSATION_GROUP
    | REQUIRED
    | RESET
    | RESOURCES
    | RESTART
    | RESUME
    | RETAINDAYS
    | RETURNS
    | REWIND
    | ROLE
    | ROUND_ROBIN
    | ROWCOUNT_BIG
    | RSA_512
    | RSA_1024
    | RSA_2048
    | RSA_3072
    | RSA_4096
    | SAFETY
    | SAFE
    | SCHEDULER
    | SCHEME
    | SCRIPT
    | SERVER
    | SERVICE
    | SERVICE_BROKER
    | SERVICE_NAME
    | SESSION
    | SESSION_CONTEXT
    | SETTINGS
    | SHRINKLOG
    | SID
    | SKIP_KEYWORD
    | SOFTNUMA
    | SOURCE
    | SPECIFICATION
    | SPLIT
    | SQL
    | SQLDUMPERFLAGS
    | SQLDUMPERPATH
    | SQLDUMPERTIMEOUT
    | STATE
    | STATS
    | START
    | STARTED
    | STARTUP_STATE
    | STOP
    | STOPPED
    | STOP_ON_ERROR
    | SUPPORTED
    | SWITCH
    | TAPE
    | TARGET
    | TCP
    | TOSTRING
    | TRACE
    | TRACK_CAUSALITY
    | TRANSFER
    | UNCHECKED
    | UNLOCK
    | UNSAFE
    | URL
    | USED
    | VERBOSELOGGING
    | VISIBILITY
    | WAIT_AT_LOW_PRIORITY
    | WINDOWS
    | WITHOUT
    | WITNESS
    | XACT_ABORT
    | XACT_STATE
    //
    | ABS
    | ACOS
    | ASIN
    | ATAN
    | ATN2
    | CEILING
    | COS
    | COT
    | DEGREES
    | EXP
    | FLOOR
    | LOG10
    | PI
    | POWER
    | RADIANS
    | RAND
    | ROUND
    | SIGN
    | SIN
    | SQRT
    | SQUARE
    | TAN
    //
    | CURRENT_TIMEZONE
    | CURRENT_TIMEZONE_ID
    | DATE_BUCKET
    | DATEDIFF_BIG
    | DATEFROMPARTS
    | DATETIME2FROMPARTS
    | DATETIMEFROMPARTS
    | DATETIMEOFFSETFROMPARTS
    | DATETRUNC
    | DAY
    | EOMONTH
    | ISDATE
    | MONTH
    | SMALLDATETIMEFROMPARTS
    | SWITCHOFFSET
    | SYSDATETIME
    | SYSDATETIMEOFFSET
    | SYSUTCDATETIME
    | TIMEFROMPARTS
    | TODATETIMEOFFSET
    | YEAR
    //
    | QUARTER
    | DAYOFYEAR
    | WEEK
    | HOUR
    | MINUTE
    | SECOND
    | MILLISECOND
    | MICROSECOND
    | NANOSECOND
    | TZOFFSET
    | ISO_WEEK
    | WEEKDAY
    //
    | YEAR_ABBR
    | QUARTER_ABBR
    | MONTH_ABBR
    | DAYOFYEAR_ABBR
    | DAY_ABBR
    | WEEK_ABBR
    | HOUR_ABBR
    | MINUTE_ABBR
    | SECOND_ABBR
    | MILLISECOND_ABBR
    | MICROSECOND_ABBR
    | NANOSECOND_ABBR
    | TZOFFSET_ABBR
    | ISO_WEEK_ABBR
    | WEEKDAY_ABBR
    //
    | SP_EXECUTESQL
    //Build-ins:
    | VARCHAR
    | NVARCHAR
    | PRECISION //For some reason this is possible to use as ID
    | FILESTREAM_ON
    ;

// https://msdn.microsoft.com/en-us/library/ms175874.aspx
id_
    : ID
    | TEMP_ID
    | DOUBLE_QUOTE_ID
    | DOUBLE_QUOTE_BLANK // TODO: This is silly I think - remove
    | SQUARE_BRACKET_ID
    | keyword
    | RAW
    ;

simpleId
    : ID
    ;

idOrString
    : id_
    | STRING
    ;

// https://msdn.microsoft.com/en-us/library/ms188074.aspx
// Spaces are allowed for comparison operators.
comparisonOperator
    : EQ
    | GT
    | LT
    | LT EQ
    | GT EQ
    | LT GT
    | EQ
    | GT
    | LT
    ;

assignmentOperator
    : PE
    | ME
    | SE
    | DE
    | MEA
    | AND_ASSIGN
    | XOR_ASSIGN
    | OR_ASSIGN
    ;

fileSize
    : INT (KB | MB | GB | TB | MOD)?
    ;