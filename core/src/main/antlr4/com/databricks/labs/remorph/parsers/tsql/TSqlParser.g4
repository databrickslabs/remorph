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

tSqlFile
    : batch? EOF
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
    : GOTO id SEMI?
    | id COLON SEMI?
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
    : ALTER APPLICATION ROLE applictionRole = id WITH (
        COMMA? NAME EQ newApplicationRoleName = id
    )? (COMMA? PASSWORD EQ applicationRolePassword = STRING)? (
        COMMA? DEFAULT_SCHEMA EQ appRoleDefaultSchema = id
    )?
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-xml-schema-collection-transact-sql?view=sql-server-ver16
alterXmlSchemaCollection
    : ALTER XML SCHEMA COLLECTION (id DOT)? id ADD STRING
    ;

createApplicationRole
    : CREATE APPLICATION ROLE applictionRole = id WITH (
        COMMA? PASSWORD EQ applicationRolePassword = STRING
    )? (COMMA? DEFAULT_SCHEMA EQ appRoleDefaultSchema = id)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-aggregate-transact-sql

dropAggregate
    : DROP AGGREGATE (IF EXISTS)? (schemaName = id DOT)? aggregateName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-application-role-transact-sql
dropApplicationRole
    : DROP APPLICATION ROLE rolename = id
    ;

alterAssembly
    : alterAssemblyStart assemblyName = id alterAssemblyClause
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
    : alterAssemblyFileName (alterAssemblyAs id)?
    ;

alterAssemblyFileName
    : STRING
    ;

//need to implement
alterAssemblyFileBits
    : alterAssemblyAs id
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
    : computerName = id
    ;

filePath
    : BACKSLASH filePath
    | id
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
    : CREATE ASSEMBLY assemblyName = id (AUTHORIZATION ownerName = id)? FROM (
        COMMA? (STRING | HEX)
    )+ (WITH PERMISSION_SET EQ (SAFE | EXTERNAL_ACCESS | UNSAFE))?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-assembly-transact-sql
dropAssembly
    : DROP ASSEMBLY (IF EXISTS)? (COMMA? assemblyName = id)+ (WITH NO DEPENDENTS)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-asymmetric-key-transact-sql

alterAsymmetricKey
    : alterAsymmetricKeyStart Asym_Key_Name = id (asymmetricKeyOption | REMOVE PRIVATE KEY)
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
    : CREATE ASYMMETRIC KEY Asym_Key_Nam = id (AUTHORIZATION databasePrincipalName = id)? (
        FROM (
            FILE EQ STRING
            | EXECUTABLE_FILE EQ STRING
            | ASSEMBLY Assembly_Name = id
            | PROVIDER Provider_Name = id
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
    : DROP ASYMMETRIC KEY keyName = id (REMOVE PROVIDER KEY)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-authorization-transact-sql

alterAuthorization
    : alterAuthorizationStart (classType colonColon)? entity = entityName entityTo authorizationGrantee
    ;

authorizationGrantee
    : principalName = id
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
    : DROP AVAILABILITY GROUP groupName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-availability-group-transact-sql
alterAvailabilityGroup
    : alterAvailabilityGroupStart alterAvailabilityGroupOptions
    ;

alterAvailabilityGroupStart
    : ALTER AVAILABILITY GROUP groupName = id
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
    : (CREATE | ALTER) BROKER PRIORITY ConversationPriorityName = id FOR CONVERSATION SET LPAREN (
        CONTRACT_NAME EQ ( ( id) | ANY) COMMA?
    )? (LOCAL_SERVICE_NAME EQ (DOUBLE_FORWARD_SLASH? id | ANY) COMMA?)? (
        REMOTE_SERVICE_NAME EQ (RemoteServiceName = STRING | ANY) COMMA?
    )? (PRIORITY_LEVEL EQ ( PriorityValue = INT | DEFAULT))? RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-broker-priority-transact-sql
dropBrokerPriority
    : DROP BROKER PRIORITY ConversationPriorityName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-certificate-transact-sql
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

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-column-encryption-key-transact-sql
alterColumnEncryptionKey
    : ALTER COLUMN ENCRYPTION KEY columnEncryptionKey = id (ADD | DROP) VALUE LPAREN COLUMN_MASTER_KEY EQ columnMasterKeyName = id (
        COMMA ALGORITHM EQ algorithmName = STRING COMMA ENCRYPTED_VALUE EQ HEX
    )? RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-column-encryption-key-transact-sql
createColumnEncryptionKey
    : CREATE COLUMN ENCRYPTION KEY columnEncryptionKey = id WITH VALUES (
        LPAREN COMMA? COLUMN_MASTER_KEY EQ columnMasterKeyName = id COMMA ALGORITHM EQ algorithmName = STRING COMMA ENCRYPTED_VALUE
            EQ encryptedValue = HEX RPAREN COMMA?
    )+
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-certificate-transact-sql
dropCertificate
    : DROP CERTIFICATE certificateName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-column-encryption-key-transact-sql
dropColumnEncryptionKey
    : DROP COLUMN ENCRYPTION KEY keyName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-column-master-key-transact-sql
dropColumnMasterKey
    : DROP COLUMN MASTER KEY keyName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-contract-transact-sql
dropContract
    : DROP CONTRACT droppedContractName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-credential-transact-sql
dropCredential
    : DROP CREDENTIAL credentialName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-cryptographic-provider-transact-sql
dropCryptograhicProvider
    : DROP CRYPTOGRAPHIC PROVIDER providerName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-database-transact-sql
dropDatabase
    : DROP DATABASE (IF EXISTS)? (COMMA? databaseNameOrDatabaseSnapshotName = id)+
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-database-audit-specification-transact-sql
dropDatabaseAuditSpecification
    : DROP DATABASE AUDIT SPECIFICATION auditSpecificationName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-database-encryption-key-transact-sql?view=sql-server-ver15
dropDatabaseEncryptionKey
    : DROP DATABASE ENCRYPTION KEY
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-database-scoped-credential-transact-sql
dropDatabaseScopedCredential
    : DROP DATABASE SCOPED CREDENTIAL credentialName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-default-transact-sql
dropDefault
    : DROP DEFAULT (IF EXISTS)? (COMMA? (schemaName = id DOT)? defaultName = id)
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-endpoint-transact-sql
dropEndpoint
    : DROP ENDPOINT endPointName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-external-data-source-transact-sql
dropExternalDataSource
    : DROP EXTERNAL DATA SOURCE externalDataSourceName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-external-file-format-transact-sql
dropExternalFileFormat
    : DROP EXTERNAL FILE FORMAT externalFileFormatName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-external-library-transact-sql
dropExternalLibrary
    : DROP EXTERNAL LIBRARY libraryName = id (AUTHORIZATION ownerName = id)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-external-resource-pool-transact-sql
dropExternalResourcePool
    : DROP EXTERNAL RESOURCE POOL poolName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-external-table-transact-sql
dropExternalTable
    : DROP EXTERNAL TABLE (databaseName = id DOT)? (schemaName = id DOT)? table = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-event-notification-transact-sql
dropEventNotifications
    : DROP EVENT NOTIFICATION (COMMA? notificationName = id)+ ON (
        SERVER
        | DATABASE
        | QUEUE queueName = id
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-event-session-transact-sql
dropEventSession
    : DROP EVENT SESSION eventSessionName = id ON SERVER
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-fulltext-catalog-transact-sql
dropFulltextCatalog
    : DROP FULLTEXT CATALOG catalogName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-fulltext-index-transact-sql
dropFulltextIndex
    : DROP FULLTEXT INDEX ON (schema = id DOT)? table = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-fulltext-stoplist-transact-sql
dropFulltextStoplist
    : DROP FULLTEXT STOPLIST stoplistName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-login-transact-sql
dropLogin
    : DROP LOGIN loginName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-master-key-transact-sql
dropMasterKey
    : DROP MASTER KEY
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-message-type-transact-sql
dropMessageType
    : DROP MESSAGE TYPE messageTypeName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-partition-function-transact-sql
dropPartitionFunction
    : DROP PARTITION FUNCTION partitionFunctionName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-partition-scheme-transact-sql
dropPartitionScheme
    : DROP PARTITION SCHEME partitionSchemeName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-queue-transact-sql
dropQueue
    : DROP QUEUE (databaseName = id DOT)? (schemaName = id DOT)? queueName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-remote-service-binding-transact-sql
dropRemoteServiceBinding
    : DROP REMOTE SERVICE BINDING bindingName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-resource-pool-transact-sql
dropResourcePool
    : DROP RESOURCE POOL poolName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-role-transact-sql
dropDbRole
    : DROP ROLE (IF EXISTS)? roleName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-route-transact-sql
dropRoute
    : DROP ROUTE routeName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-rule-transact-sql
dropRule
    : DROP RULE (IF EXISTS)? (COMMA? (schemaName = id DOT)? ruleName = id)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-schema-transact-sql
dropSchema
    : DROP SCHEMA (IF EXISTS)? schemaName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-search-property-list-transact-sql
dropSearchPropertyList
    : DROP SEARCH PROPERTY LIST propertyListName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-security-policy-transact-sql
dropSecurityPolicy
    : DROP SECURITY POLICY (IF EXISTS)? (schemaName = id DOT)? securityPolicyName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-sequence-transact-sql
dropSequence
    : DROP SEQUENCE (IF EXISTS)? (
        COMMA? (databaseName = id DOT)? (schemaName = id DOT)? sequenceName = id
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-server-audit-transact-sql
dropServerAudit
    : DROP SERVER AUDIT auditName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-server-audit-specification-transact-sql
dropServerAuditSpecification
    : DROP SERVER AUDIT SPECIFICATION auditSpecificationName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-server-role-transact-sql
dropServerRole
    : DROP SERVER ROLE roleName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-service-transact-sql
dropService
    : DROP SERVICE droppedServiceName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-signature-transact-sql
dropSignature
    : DROP (COUNTER)? SIGNATURE FROM (schemaName = id DOT)? moduleName = id BY (
        COMMA? CERTIFICATE certName = id
        | COMMA? ASYMMETRIC KEY AsymKeyName = id
    )+
    ;

dropStatisticsNameAzureDwAndPdw
    : DROP STATISTICS (schemaName = id DOT)? objectName = id DOT statisticsName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-symmetric-key-transact-sql
dropSymmetricKey
    : DROP SYMMETRIC KEY symmetricKeyName = id (REMOVE PROVIDER KEY)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-synonym-transact-sql
dropSynonym
    : DROP SYNONYM (IF EXISTS)? (schema = id DOT)? synonymName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-user-transact-sql
dropUser
    : DROP USER (IF EXISTS)? userName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-workload-group-transact-sql
dropWorkloadGroup
    : DROP WORKLOAD GROUP groupName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-xml-schema-collection-transact-sql
dropXmlSchemaCollection
    : DROP XML SCHEMA COLLECTION (relationalSchema = id DOT)? sqlIdentifier = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/disable-trigger-transact-sql
disableTrigger
    : DISABLE TRIGGER (( COMMA? (schemaName = id DOT)? triggerName = id)+ | ALL) ON (
        (schemaId = id DOT)? objectName = id
        | DATABASE
        | ALL SERVER
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/enable-trigger-transact-sql
enableTrigger
    : ENABLE TRIGGER (( COMMA? (schemaName = id DOT)? triggerName = id)+ | ALL) ON (
        (schemaId = id DOT)? objectName = id
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
    : CREATE COLUMN MASTER KEY keyName = id WITH LPAREN KEY_STORE_PROVIDER_NAME EQ keyStoreProviderName = STRING COMMA KEY_PATH EQ
        keyPath = STRING RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-credential-transact-sql
alterCredential
    : ALTER CREDENTIAL credentialName = id WITH IDENTITY EQ identityName = STRING (
        COMMA SECRET EQ secret = STRING
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-credential-transact-sql
createCredential
    : CREATE CREDENTIAL credentialName = id WITH IDENTITY EQ identityName = STRING (
        COMMA SECRET EQ secret = STRING
    )? (FOR CRYPTOGRAPHIC PROVIDER cryptographicProviderName = id)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-cryptographic-provider-transact-sql
alterCryptographicProvider
    : ALTER CRYPTOGRAPHIC PROVIDER providerName = id (
        FROM FILE EQ cryptoProviderDdlFile = STRING
    )? (ENABLE | DISABLE)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-cryptographic-provider-transact-sql
createCryptographicProvider
    : CREATE CRYPTOGRAPHIC PROVIDER providerName = id FROM FILE EQ pathOf_DLL = STRING
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/statements/create-endpoint-transact-sql?view=sql-server-ver16
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
        WINDOWS (NTLM | KERBEROS | NEGOTIATE)? (CERTIFICATE certName = id)?
        | CERTIFICATE certName = id WINDOWS? (NTLM | KERBEROS | NEGOTIATE)?
    )
    ;

endpointListenerClause
    : LISTENER_PORT EQ port = INT (
        COMMA LISTENER_IP EQ (ALL | LPAREN (ipv4 = IPV4_ADDR | ipv6 = STRING) RPAREN)
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-event-notification-transact-sql
createEventNotification
    : CREATE EVENT NOTIFICATION eventNotificationName = id ON (
        SERVER
        | DATABASE
        | QUEUE queueName = id
    ) (WITH FAN_IN)? FOR (COMMA? eventTypeOrGroup = id)+ TO SERVICE brokerService = STRING COMMA brokerServiceSpecifierOrCurrentDatabase =
        STRING
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-event-session-transact-sql
// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-event-session-transact-sql
// todo: not implemented
createOrAlterEventSession
    : (CREATE | ALTER) EVENT SESSION eventSessionName = id ON SERVER (
        COMMA? ADD EVENT (
            (eventModuleGuid = id DOT)? eventPackageName = id DOT eventName = id
        ) (
            LPAREN (SET ( COMMA? eventCustomizableAttributue = id EQ (INT | STRING))*)? (
                ACTION LPAREN (
                    COMMA? (eventModuleGuid = id DOT)? eventPackageName = id DOT actionName = id
                )+ RPAREN
            )+ (WHERE eventSessionPredicateExpression)? RPAREN
        )*
    )* (
        COMMA? DROP EVENT (eventModuleGuid = id DOT)? eventPackageName = id DOT eventName = id
    )* (
        (ADD TARGET (eventModuleGuid = id DOT)? eventPackageName = id DOT targetName = id) (
            LPAREN SET (
                COMMA? targetParameterName = id EQ (LPAREN? INT RPAREN? | STRING)
            )+ RPAREN
        )*
    )* (DROP TARGET (eventModuleGuid = id DOT)? eventPackageName = id DOT targetName = id)* (
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
        eventFieldName = id
        | (
            eventFieldName = id
            | (
                (eventModuleGuid = id DOT)? eventPackageName = id DOT predicateSourceName = id
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
    | (eventModuleGuid = id DOT)? eventPackageName = id DOT predicateCompareName = id LPAREN (
        eventFieldName = id
        | ((eventModuleGuid = id DOT)? eventPackageName = id DOT predicateSourceName = id) COMMA (
            INT
            | STRING
        )
    ) RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-external-data-source-transact-sql
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

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-external-library-transact-sql
alterExternalLibrary
    : ALTER EXTERNAL LIBRARY libraryName = id (AUTHORIZATION ownerName = id)? (SET | ADD) (
        LPAREN CONTENT EQ (clientLibrary = STRING | HEX | NONE) (
            COMMA PLATFORM EQ (WINDOWS | LINUX)? RPAREN
        ) WITH (
            COMMA? LANGUAGE EQ (R | PYTHON)
            | DATA_SOURCE EQ externalDataSourceName = id
        )+ RPAREN
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-external-library-transact-sql
createExternalLibrary
    : CREATE EXTERNAL LIBRARY libraryName = id (AUTHORIZATION ownerName = id)? FROM (
        COMMA? LPAREN? (CONTENT EQ)? (clientLibrary = STRING | HEX | NONE) (
            COMMA PLATFORM EQ (WINDOWS | LINUX)? RPAREN
        )?
    ) (
        WITH (
            COMMA? LANGUAGE EQ (R | PYTHON)
            | DATA_SOURCE EQ externalDataSourceName = id
        )+ RPAREN
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-external-resource-pool-transact-sql
alterExternalResourcePool
    : ALTER EXTERNAL RESOURCE POOL (poolName = id | DEFAULT_DOUBLE_QUOTE) WITH LPAREN MAX_CPU_PERCENT EQ maxCpuPercent = INT (
        COMMA? AFFINITY CPU EQ (AUTO | (COMMA? INT TO INT | COMMA INT)+)
        | NUMANODE EQ (COMMA? INT TO INT | COMMA? INT)+
    ) (COMMA? MAX_MEMORY_PERCENT EQ maxMemoryPercent = INT)? (
        COMMA? MAX_PROCESSES EQ maxProcesses = INT
    )? RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-external-resource-pool-transact-sql
createExternalResourcePool
    : CREATE EXTERNAL RESOURCE POOL poolName = id WITH LPAREN MAX_CPU_PERCENT EQ maxCpuPercent = INT (
        COMMA? AFFINITY CPU EQ (AUTO | (COMMA? INT TO INT | COMMA INT)+)
        | NUMANODE EQ (COMMA? INT TO INT | COMMA? INT)+
    ) (COMMA? MAX_MEMORY_PERCENT EQ maxMemoryPercent = INT)? (
        COMMA? MAX_PROCESSES EQ maxProcesses = INT
    )? RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-fulltext-catalog-transact-sql
alterFulltextCatalog
    : ALTER FULLTEXT CATALOG catalogName = id (
        REBUILD (WITH ACCENT_SENSITIVITY EQ (ON | OFF))?
        | REORGANIZE
        | AS DEFAULT
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-fulltext-catalog-transact-sql
createFulltextCatalog
    : CREATE FULLTEXT CATALOG catalogName = id (ON FILEGROUP filegroup = id)? (
        IN PATH rootpath = STRING
    )? (WITH ACCENT_SENSITIVITY EQ (ON | OFF))? (AS DEFAULT)? (AUTHORIZATION ownerName = id)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-fulltext-stoplist-transact-sql
alterFulltextStoplist
    : ALTER FULLTEXT STOPLIST stoplistName = id (
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
    : CREATE FULLTEXT STOPLIST stoplistName = id (
        FROM ((databaseName = id DOT)? sourceStoplistName = id | SYSTEM STOPLIST)
    )? (AUTHORIZATION ownerName = id)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-login-transact-sql
alterLoginSqlServer
    : ALTER LOGIN loginName = id (
        (ENABLE | DISABLE)?
        | WITH (
            (PASSWORD EQ ( password = STRING | passwordHash = HEX HASHED)) (
                MUST_CHANGE
                | UNLOCK
            )*
        )? (OLD_PASSWORD EQ oldPassword = STRING (MUST_CHANGE | UNLOCK)*)? (
            DEFAULT_DATABASE EQ defaultDatabase = id
        )? (DEFAULT_LANGUAGE EQ defaultLaguage = id)? (NAME EQ loginName = id)? (
            CHECK_POLICY EQ (ON | OFF)
        )? (CHECK_EXPIRATION EQ (ON | OFF))? (CREDENTIAL EQ credentialName = id)? (
            NO CREDENTIAL
        )?
        | (ADD | DROP) CREDENTIAL credentialName = id
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-login-transact-sql
createLoginSqlServer
    : CREATE LOGIN loginName = id (
        WITH (
            (PASSWORD EQ ( password = STRING | passwordHash = HEX HASHED)) (
                MUST_CHANGE
                | UNLOCK
            )*
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

createLoginAzureSql
    : CREATE LOGIN loginName = id WITH PASSWORD EQ STRING (SID EQ sid = HEX)?
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
    : ALTER MESSAGE TYPE messageTypeName = id VALIDATION EQ (
        NONE
        | EMPTY
        | WELL_FORMED_XML
        | VALID_XML WITH SCHEMA COLLECTION schemaCollectionName = id
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-partition-function-transact-sql
alterPartitionFunction
    : ALTER PARTITION FUNCTION partitionFunctionName = id LPAREN RPAREN (SPLIT | MERGE) RANGE LPAREN INT RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-partition-scheme-transact-sql
alterPartitionScheme
    : ALTER PARTITION SCHEME partitionSchemeName = id NEXT USED (fileGroupName = id)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-remote-service-binding-transact-sql
alterRemoteServiceBinding
    : ALTER REMOTE SERVICE BINDING bindingName = id WITH (USER EQ userName = id)? (
        COMMA ANONYMOUS EQ (ON | OFF)
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-remote-service-binding-transact-sql
createRemoteServiceBinding
    : CREATE REMOTE SERVICE BINDING bindingName = id (AUTHORIZATION ownerName = id)? TO SERVICE remoteServiceName = STRING WITH (
        USER EQ userName = id
    )? (COMMA ANONYMOUS EQ (ON | OFF))?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-resource-pool-transact-sql
createResourcePool
    : CREATE RESOURCE POOL poolName = id (
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
            schemaName = id DOT functionName = id
            | NULL_
        ) RPAREN
        | RESET STATISTICS
        | WITH LPAREN MAX_OUTSTANDING_IO_PER_VOLUME EQ maxOutstandingIoPerVolume = INT RPAREN
    )
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-database-audit-specification-transact-sql?view=sql-server-ver16
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
    : ((id DOT)? id DOT)? id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-role-transact-sql
alterDbRole
    : ALTER ROLE roleName = id (
        (ADD | DROP) MEMBER databasePrincipal = id
        | WITH NAME EQ newRoleName = id
    )
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/statements/create-database-audit-specification-transact-sql?view=sql-server-ver16
createDatabaseAuditSpecification
    : CREATE DATABASE AUDIT SPECIFICATION auditSpecificationName = id (
        FOR SERVER AUDIT auditName = id
    )? (auditActionSpecGroup (COMMA auditActionSpecGroup)*)? (
        WITH LPAREN STATE EQ (ON | OFF) RPAREN
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-role-transact-sql
createDbRole
    : CREATE ROLE roleName = id (AUTHORIZATION ownerName = id)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-route-transact-sql
createRoute
    : CREATE ROUTE routeName = id (AUTHORIZATION ownerName = id)? WITH (
        COMMA? SERVICE_NAME EQ routeServiceName = STRING
    )? (COMMA? BROKER_INSTANCE EQ brokerInstanceIdentifier = STRING)? (
        COMMA? LIFETIME EQ INT
    )? COMMA? ADDRESS EQ STRING (COMMA MIRROR_ADDRESS EQ STRING)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-rule-transact-sql
createRule
    : CREATE RULE (schemaName = id DOT)? ruleName = id AS searchCondition
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-schema-transact-sql
alterSchemaSql
    : ALTER SCHEMA schemaName = id TRANSFER (
        (OBJECT | TYPE | XML SCHEMA COLLECTION) DOUBLE_COLON
    )? id (DOT id)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-schema-transact-sql
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

createSchemaAzureSqlDwAndPdw
    : CREATE SCHEMA schemaName = id (AUTHORIZATION ownerName = id)?
    ;

alterSchemaAzureSqlDwAndPdw
    : ALTER SCHEMA schemaName = id TRANSFER (OBJECT DOUBLE_COLON)? id (DOT ID)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-search-property-list-transact-sql
createSearchPropertyList
    : CREATE SEARCH PROPERTY LIST newListName = id (
        FROM (databaseName = id DOT)? sourceListName = id
    )? (AUTHORIZATION ownerName = id)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-security-policy-transact-sql
createSecurityPolicy
    : CREATE SECURITY POLICY (schemaName = id DOT)? securityPolicyName = id (
        COMMA? ADD (FILTER | BLOCK)? PREDICATE tvfSchemaName = id DOT securityPredicateFunctionName = id LPAREN (
            COMMA? columnNameOrArguments = id
        )+ RPAREN ON tableSchemaName = id DOT name = id (
            COMMA? AFTER (INSERT | UPDATE)
            | COMMA? BEFORE (UPDATE | DELETE)
        )*
    )+ (WITH LPAREN STATE EQ (ON | OFF) (SCHEMABINDING (ON | OFF))? RPAREN)? (
        NOT FOR REPLICATION
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-sequence-transact-sql
alterSequence
    : ALTER SEQUENCE (schemaName = id DOT)? sequenceName = id (RESTART (WITH INT)?)? (
        INCREMENT BY sequnceIncrement = INT
    )? (MINVALUE INT | NO MINVALUE)? (MAXVALUE INT | NO MAXVALUE)? (CYCLE | NO CYCLE)? (
        CACHE INT
        | NO CACHE
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-sequence-transact-sql
createSequence
    : CREATE SEQUENCE (schemaName = id DOT)? sequenceName = id (AS dataType)? (
        START WITH INT
    )? (INCREMENT BY MINUS? INT)? (MINVALUE (MINUS? INT)? | NO MINVALUE)? (
        MAXVALUE (MINUS? INT)?
        | NO MAXVALUE
    )? (CYCLE | NO CYCLE)? (CACHE INT? | NO CACHE)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-server-audit-transact-sql
alterServerAudit
    : ALTER SERVER AUDIT auditName = id (
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
                COMMA? (NOT?) eventFieldName = id (
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
        | MODIFY NAME EQ newAuditName = id
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-server-audit-transact-sql
createServerAudit
    : CREATE SERVER AUDIT auditName = id (
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
        | MODIFY NAME EQ newAuditName = id
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-server-audit-specification-transact-sql

alterServerAuditSpecification
    : ALTER SERVER AUDIT SPECIFICATION auditSpecificationName = id (
        FOR SERVER AUDIT auditName = id
    )? ((ADD | DROP) LPAREN auditActionGroupName = id RPAREN)* (
        WITH LPAREN STATE EQ (ON | OFF) RPAREN
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-server-audit-specification-transact-sql
createServerAuditSpecification
    : CREATE SERVER AUDIT SPECIFICATION auditSpecificationName = id (
        FOR SERVER AUDIT auditName = id
    )? (ADD LPAREN auditActionGroupName = id RPAREN)* (
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
    : ALTER SERVER ROLE serverRoleName = id (
        (ADD | DROP) MEMBER serverPrincipal = id
        | WITH NAME EQ newServerRoleName = id
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-server-role-transact-sql
createServerRole
    : CREATE SERVER ROLE serverRole = id (AUTHORIZATION serverPrincipal = id)?
    ;

alterServerRolePdw
    : ALTER SERVER ROLE serverRoleName = id (ADD | DROP) MEMBER login = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-service-transact-sql
alterService
    : ALTER SERVICE modifiedServiceName = id (
        ON QUEUE (schemaName = id DOT)? queueName = id
    )? (LPAREN optArgClause (COMMA optArgClause)* RPAREN)?
    ;

optArgClause
    : (ADD | DROP) CONTRACT modifiedContractName = id
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-service-transact-sql
createService
    : CREATE SERVICE createServiceName = id (AUTHORIZATION ownerName = id)? ON QUEUE (
        schemaName = id DOT
    )? queueName = id (LPAREN (COMMA? (id | DEFAULT))+ RPAREN)?
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
    : ALTER SYMMETRIC KEY keyName = id (
        (ADD | DROP) ENCRYPTION BY (
            CERTIFICATE certificateName = id
            | PASSWORD EQ password = STRING
            | SYMMETRIC KEY symmetricKeyName = id
            | ASYMMETRIC KEY AsymKeyName = id
        )
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-synonym-transact-sql
createSynonym
    : CREATE SYNONYM (schemaName_1 = id DOT)? synonymName = id FOR (
        (serverName = id DOT)? (databaseName = id DOT)? (schemaName_2 = id DOT)? objectName = id
        | (databaseOrSchema2 = id DOT)? (schemaId2_orObjectName = id DOT)?
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-user-transact-sql
alterUser
    : ALTER USER username = id WITH (
        COMMA? NAME EQ newusername = id
        | COMMA? DEFAULT_SCHEMA EQ ( schemaName = id | NULL_)
        | COMMA? LOGIN EQ loginame = id
        | COMMA? PASSWORD EQ STRING (OLD_PASSWORD EQ STRING)+
        | COMMA? DEFAULT_LANGUAGE EQ (NONE | lcid = INT | languageNameOrAlias = id)
        | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ (ON | OFF)
    )+
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-user-transact-sql
createUser
    : CREATE USER userName = id ((FOR | FROM) LOGIN loginName = id)? (
        WITH (
            COMMA? DEFAULT_SCHEMA EQ schemaName = id
            | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ (ON | OFF)
        )*
    )?
    | CREATE USER (
        windowsPrincipal = id (
            WITH (
                COMMA? DEFAULT_SCHEMA EQ schemaName = id
                | COMMA? DEFAULT_LANGUAGE EQ (NONE | INT | languageNameOrAlias = id)
                | COMMA? SID EQ HEX
                | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ (ON | OFF)
            )*
        )?
        | userName = id WITH PASSWORD EQ password = STRING (
            COMMA? DEFAULT_SCHEMA EQ schemaName = id
            | COMMA? DEFAULT_LANGUAGE EQ (NONE | INT | languageNameOrAlias = id)
            | COMMA? SID EQ HEX
            | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ (ON | OFF)
        )*
        | Azure_Active_DirectoryPrincipal = id FROM EXTERNAL PROVIDER
    )
    | CREATE USER userName = id (
        WITHOUT LOGIN (
            COMMA? DEFAULT_SCHEMA EQ schemaName = id
            | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ (ON | OFF)
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
        | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ (ON | OFF)
    )+
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-workload-group-transact-sql

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

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-workload-group-transact-sql
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

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-xml-schema-collection-transact-sql
createXmlSchemaCollection
    : CREATE XML SCHEMA COLLECTION (relationalSchema = id DOT)? sqlIdentifier = id AS (
        STRING
        | id
        | LOCAL_ID
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-partition-function-transact-sql?view=sql-server-ver15
createPartitionFunction
    : CREATE PARTITION FUNCTION partitionFunctionName = id LPAREN inputParameterType = dataType RPAREN AS RANGE (
        LEFT
        | RIGHT
    )? FOR VALUES LPAREN boundaryValues = expressionList RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-partition-scheme-transact-sql?view=sql-server-ver15
createPartitionScheme
    : CREATE PARTITION SCHEME partitionSchemeName = id AS PARTITION partitionFunctionName = id ALL? TO LPAREN fileGroupNames += id (
        COMMA fileGroupNames += id
    )* RPAREN
    ;

createQueue
    : CREATE QUEUE (tableName | queueName = id) queueSettings? (
        ON filegroup = id
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
    : ALTER QUEUE (tableName | queueName = id) (queueSettings | queueAction)
    ;

queueAction
    : REBUILD (WITH LPAREN queueRebuildOptions RPAREN)?
    | REORGANIZE (WITH LOB_COMPACTION EQ onOff)?
    | MOVE TO (id | DEFAULT)
    ;

queueRebuildOptions
    : MAXDOP EQ INT
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
    : LPAREN? RECEIVE (ALL | DISTINCT | topClause | STAR) (LOCAL_ID EQ expression COMMA?)* FROM tableName (
        INTO tableVariable = id (WHERE where = searchCondition)
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
    : CREATE DATABASE (database = id) (CONTAINMENT EQ ( NONE | PARTIAL))? (
        ON PRIMARY? databaseFileSpec ( COMMA databaseFileSpec)*
    )? (LOG ON databaseFileSpec ( COMMA databaseFileSpec)*)? (COLLATE collationName = id)? (
        WITH createDatabaseOption ( COMMA createDatabaseOption)*
    )?
    ;

// https://msdn.microsoft.com/en-us/library/ms188783.aspx
createIndex
    : CREATE UNIQUE? clustered? INDEX id ON tableName LPAREN columnNameListWithOrder RPAREN (
        INCLUDE LPAREN columnNameList RPAREN
    )? (WHERE where = searchCondition)? (createIndexOptions)? (ON id)? SEMI?
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
    : CREATE CLUSTERED COLUMNSTORE INDEX id ON tableName createColumnstoreIndexOptions? (
        ON id
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
    : CREATE NONCLUSTERED? COLUMNSTORE INDEX id ON tableName LPAREN columnNameListWithOrder RPAREN (
        WHERE searchCondition
    )? createColumnstoreIndexOptions? (ON id)? SEMI?
    ;

createXmlIndex
    : CREATE PRIMARY? XML INDEX id ON tableName LPAREN id RPAREN (
        USING XML INDEX id (FOR (VALUE | PATH | PROPERTY)?)?
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
    : EXTERNAL NAME assemblyName = id DOT className = id DOT methodName = id
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
    : LOCAL_ID AS? (typeSchema = id DOT)? dataType VARYING? (
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
    : CREATE STATISTICS id ON tableName LPAREN columnNameList RPAREN (
        WITH (FULLSCAN | SAMPLE INT (PERCENT | ROWS) | STATS_STREAM) (COMMA NORECOMPUTE)? (
            COMMA INCREMENTAL EQ onOff
        )?
    )? SEMI?
    ;

updateStatistics
    : UPDATE STATISTICS tableName (id | LPAREN id ( COMMA id)* RPAREN)? updateStatisticsOptions?
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
    )? tableOptions* (ON id | DEFAULT | onPartitionOrFilegroup)? (TEXTIMAGE_ON id | DEFAULT)? SEMI?
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

tableOption
    : (simpleId | keyword) EQ (simpleId | keyword | onOff | INT)
    | CLUSTERED COLUMNSTORE INDEX
    | HEAP
    | FILLFACTOR EQ INT
    | DISTRIBUTION EQ HASH LPAREN id RPAREN
    | CLUSTERED INDEX LPAREN id (ASC | DESC)? (COMMA id (ASC | DESC)?)* RPAREN
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
    : WAIT_AT_LOW_PRIORITY LPAREN MAX_DURATION EQ maxDuration = time MINUTES? COMMA ABORT_AFTER_WAIT EQ abortAfterWait = (
        NONE
        | SELF
        | BLOCKERS
    ) RPAREN
    ;

// https://msdn.microsoft.com/en-us/library/ms174269.aspx
alterDatabase
    : ALTER DATABASE (database = id | CURRENT) (
        MODIFY NAME EQ newName = id
        | COLLATE collation = id
        | SET databaseOptionspec (WITH termination)?
        | addOrModifyFiles
        | addOrModifyFilegroups
    ) SEMI?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-database-transact-sql-file-and-filegroup-options?view=sql-server-ver15
addOrModifyFiles
    : ADD FILE fileSpec (COMMA fileSpec)* (TO FILEGROUP filegroupName = id)?
    | ADD LOG FILE fileSpec (COMMA fileSpec)*
    | REMOVE FILE logicalFileName = id
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
    : id DOT host
    | (id DOT | id)
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
    | DEFAULT_LANGUAGE EQ ( id | STRING)
    | DEFAULT_FULLTEXT_LANGUAGE EQ ( id | STRING)
    | NESTED_TRIGGERS EQ ( OFF | ON)
    | TRANSFORM_NOISE_WORDS EQ ( OFF | ON)
    | TWO_DIGIT_YEAR_CUTOFF EQ INT
    ;

hadrOptions
    : HADR (( AVAILABILITY GROUP EQ availabilityGroupName = id | OFF) | (SUSPEND | RESUME))
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
    : indexName = id ON tableName
    ;

dropBackwardCompatibleIndex
    : (ownerName = id DOT)? tableOrViewName = id DOT indexName = id
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
    : DROP STATISTICS (COMMA? (tableName DOT)? name = id)+ SEMI
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
    : OPENQUERY LPAREN linkedServer = id COMMA query = STRING RPAREN
    ;

// https://msdn.microsoft.com/en-us/library/ms179856.aspx
opendatasource
    : OPENDATASOURCE LPAREN provider = STRING COMMA init = STRING RPAREN DOT (database = id)? DOT (
        scheme = id
    )? DOT (table = id)
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
    : xmlNamespaceUri = STRING AS id
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
    : BACKUP DATABASE (databaseName = id) (
        READ_WRITE_FILEGROUPS (COMMA? (FILE | FILEGROUP) EQ fileOrFilegroup = STRING)*
    )? (COMMA? (FILE | FILEGROUP) EQ fileOrFilegroup = STRING)* (
        TO ( COMMA? logicalDeviceName = id)+
        | TO ( COMMA? (DISK | TAPE | URL) EQ (STRING | id))+
    ) (
        (MIRROR TO ( COMMA? logicalDeviceName = id)+)+
        | ( MIRROR TO ( COMMA? (DISK | TAPE | URL) EQ (STRING | id))+)+
    )? (
        WITH (
            COMMA? DIFFERENTIAL
            | COMMA? COPY_ONLY
            | COMMA? (COMPRESSION | NO_COMPRESSION)
            | COMMA? DESCRIPTION EQ (STRING | id)
            | COMMA? NAME EQ backupSetName = id
            | COMMA? CREDENTIAL
            | COMMA? FILE_SNAPSHOT
            | COMMA? (EXPIREDATE EQ (STRING | id) | RETAINDAYS EQ (INT | id))
            | COMMA? (NOINIT | INIT)
            | COMMA? (NOSKIP | SKIP_KEYWORD)
            | COMMA? (NOFORMAT | FORMAT)
            | COMMA? MEDIADESCRIPTION EQ (STRING | id)
            | COMMA? MEDIANAME EQ (medianame = STRING)
            | COMMA? BLOCKSIZE EQ (INT | id)
            | COMMA? BUFFERCOUNT EQ (INT | id)
            | COMMA? MAXTRANSFER EQ (INT | id)
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
                encryptorName = id
                | SERVER ASYMMETRIC KEY EQ encryptorName = id
            )
        )*
    )?
    ;

backupLog
    : BACKUP LOG (databaseName = id) (
        TO ( COMMA? logicalDeviceName = id)+
        | TO ( COMMA? (DISK | TAPE | URL) EQ (STRING | id))+
    ) (
        (MIRROR TO ( COMMA? logicalDeviceName = id)+)+
        | ( MIRROR TO ( COMMA? (DISK | TAPE | URL) EQ (STRING | id))+)+
    )? (
        WITH (
            COMMA? DIFFERENTIAL
            | COMMA? COPY_ONLY
            | COMMA? (COMPRESSION | NO_COMPRESSION)
            | COMMA? DESCRIPTION EQ (STRING | id)
            | COMMA? NAME EQ backupSetName = id
            | COMMA? CREDENTIAL
            | COMMA? FILE_SNAPSHOT
            | COMMA? (EXPIREDATE EQ (STRING | id) | RETAINDAYS EQ (INT | id))
            | COMMA? (NOINIT | INIT)
            | COMMA? (NOSKIP | SKIP_KEYWORD)
            | COMMA? (NOFORMAT | FORMAT)
            | COMMA? MEDIADESCRIPTION EQ (STRING | id)
            | COMMA? MEDIANAME EQ (medianame = STRING)
            | COMMA? BLOCKSIZE EQ (INT | id)
            | COMMA? BUFFERCOUNT EQ (INT | id)
            | COMMA? MAXTRANSFER EQ (INT | id)
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
                encryptorName = id
                | SERVER ASYMMETRIC KEY EQ encryptorName = id
            )
        )*
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/backup-certificate-transact-sql
backupCertificate
    : BACKUP CERTIFICATE certname = id TO FILE EQ certFile = STRING (
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
        AT_KEYWORD linkedServer = id
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
    : (constant | LOCAL_ID (OUTPUT | OUT)? | id | DEFAULT | NULL_)
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
    : id
    | PUBLIC
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

dateOptions
    : (START_DATE | EXPIRY_DATE) EQ STRING
    ;

openKey
    : OPEN SYMMETRIC KEY keyName = id DECRYPTION BY decryptionMechanism
    | OPEN MASTER KEY DECRYPTION BY PASSWORD EQ password = STRING
    ;

closeKey
    : CLOSE SYMMETRIC KEY keyName = id
    | CLOSE ALL SYMMETRIC KEYS
    | CLOSE MASTER KEY
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
    : SET LOCAL_ID (DOT memberName = id)? EQ expression
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
    : BEGIN DISTRIBUTED (TRAN | TRANSACTION) (id | LOCAL_ID)?
    // https://msdn.microsoft.com/en-us/library/ms188929.aspx
    | BEGIN (TRAN | TRANSACTION) ((id | LOCAL_ID) (WITH MARK STRING)?)?
    // https://msdn.microsoft.com/en-us/library/ms190295.aspx
    | COMMIT (TRAN | TRANSACTION) (
        (id | LOCAL_ID) (WITH LPAREN DELAYED_DURABILITY EQ (OFF | ON) RPAREN)?
    )?
    // https://msdn.microsoft.com/en-us/library/ms178628.aspx
    | COMMIT WORK?
    | COMMIT id
    | ROLLBACK id
    // https://msdn.microsoft.com/en-us/library/ms181299.aspx
    | ROLLBACK (TRAN | TRANSACTION) (id | LOCAL_ID)?
    // https://msdn.microsoft.com/en-us/library/ms174973.aspx
    | ROLLBACK WORK?
    // https://msdn.microsoft.com/en-us/library/ms188378.aspx
    | SAVE (TRAN | TRANSACTION) (id | LOCAL_ID)?
    ;

// https://msdn.microsoft.com/en-us/library/ms188037.aspx
goStatement
    : GO (count = INT)?
    ;

// https://msdn.microsoft.com/en-us/library/ms188366.aspx
useStatement
    : USE database = id
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
        LPAREN (database = id | databaseid = STRING | INT) (
            COMMA NOINDEX
            | COMMA ( REPAIR_ALLOW_DATA_LOSS | REPAIR_FAST | REPAIR_REBUILD)
        )? RPAREN (
            WITH dbccOption = dbccCheckallocOption (COMMA dbccOption = dbccCheckallocOption)*
        )?
    )?
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checkcatalog-transact-sql?view=sql-server-ver16
dbccCheckcatalog
    : name = CHECKCATALOG (LPAREN ( database = id | databasename = STRING | INT) RPAREN)? (
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
        LPAREN (tableOrConstraint = id | tableOrConstraintName = STRING) RPAREN
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
        LPAREN (database = id | databasename = STRING | INT) (
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

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-clonedatabase-transact-sql?view=sql-server-ver16
dbccClonedatabase
    : name = CLONEDATABASE LPAREN sourceDatabase = id COMMA targetDatabase = id RPAREN (
        WITH dbccOption = dbccClonedatabaseOption (COMMA dbccOption = dbccClonedatabaseOption)*
    )?
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-pdw-showspaceused-transact-sql?view=aps-pdw-2016-au7
dbccPdwShowspaceused
    : name = PDW_SHOWSPACEUSED (LPAREN tablename = id RPAREN)? (
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
    : dllname = id LPAREN name = FREE RPAREN (WITH dbccOption = NO_INFOMSGS)?
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
    : (((PRIMARY KEY | INDEX id) (CLUSTERED | NONCLUSTERED)?) | UNIQUE) LPAREN columnNameListWithOrder RPAREN
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
    : id (dataType | AS expression PERSISTED?) columnDefinitionElement* columnIndex?
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
    // NULL / NOT NULL is a constraint
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
        | MASKED (WITH (FUNCTION EQ STRING | LPAREN FUNCTION EQ STRING RPAREN))?
    )
    ;

materializedColumnDefinition
    : id (COMPUTE | AS) expression (MATERIALIZED | NOT MATERIALIZED)?
    ;

// https://msdn.microsoft.com/en-us/library/ms186712.aspx
// There is a documentation error: NOT NULL is a constraint
// and therefore can be given a name.
columnConstraint
    : (CONSTRAINT constraint = id)? (
        nullNotnull
        | ( (PRIMARY KEY | UNIQUE) clustered? primaryKeyOptions)
        | ( (FOREIGN KEY)? foreignKeyOptions)
        | checkConstraint
    )
    ;

columnIndex
    : INDEX indexName = id clustered? createTableIndexOptions? onPartitionOrFilegroup? (
        FILESTREAM_ON (filestreamFilegroupOrPartitionSchemaName = id | NULL_DOUBLE_QUOTE)
    )?
    ;

onPartitionOrFilegroup
    : ON (
        (partitionSchemeName = id LPAREN partitionColumnName = id RPAREN)
        | filegroup = id
        | DEFAULT_DOUBLE_QUOTE
    )
    ;

// https://msdn.microsoft.com/en-us/library/ms188066.aspx
tableConstraint
    : (CONSTRAINT constraint = id)? (
        ((PRIMARY KEY | UNIQUE) clustered? LPAREN columnNameListWithOrder RPAREN primaryKeyOptions)
        | ( FOREIGN KEY LPAREN fk = columnNameList RPAREN foreignKeyOptions)
        | ( CONNECTION LPAREN connectionNode ( COMMA connectionNode)* RPAREN)
        | ( DEFAULT constantExpr = expression FOR column = id (WITH VALUES)?)
        | checkConstraint
    )
    ;

connectionNode
    : fromNodeTable = id TO toNodeTable = id
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
    | DISTRIBUTION EQ HASH LPAREN id RPAREN
    | CLUSTERED INDEX LPAREN id (ASC | DESC)? (COMMA id (ASC | DESC)?)* RPAREN
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
    : SET id (id | constant_LOCAL_ID | onOff) SEMI?
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

constant_LOCAL_ID
    : constant
    | LOCAL_ID
    ;

// Expression.

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/expressions-transact-sql
// Operator precendence: https://docs.microsoft.com/en-us/sql/t-sql/language-elements/operator-precedence-transact-sql
expression
    : LPAREN expression RPAREN                                  #exprPrecedence
    | <assoc=right> op=BIT_NOT expression                       #exprBitNot
    | <assoc=right> op=(PLUS | MINUS) expression                #exprUnary
    | expression op=(STAR | DIV | MOD) expression               #exprOpPrec1
    | expression op=(PLUS | MINUS) expression                   #exprOpPrec2
    | expression op=(BIT_AND | BIT_XOR | BIT_OR) expression     #exprOpPrec3
    | expression op=DOUBLE_BAR expression                       #exprOpPrec4
    | primitiveExpression                                       #exprPrimitive
    | functionCall                                              #exprFunc
    | expression COLLATE id                                     #exprCollate
    | caseExpression                                            #exprCase
    | expression timeZone                                       #exprTz
    | expression overClause                                     #exprOver
    | id                                                        #exprId
    | DOLLAR_ACTION                                             #exprDollar
    | <assoc=right> expression DOT expression                   #exprDot
    | LPAREN subquery RPAREN                                    #exprSubquery
    | ALL expression                                            #exprAll
    | DISTINCT expression                                       #exprDistinct
    | STAR                                                      #exprStar
    ;

// TODO: Implement this
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
    | constant
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/case-transact-sql
caseExpression
    : CASE caseExpr=expression? switchSection+ (ELSE elseExpr = expression)? END
    ;

subquery
    : selectStatement
    ;

// https://msdn.microsoft.com/en-us/library/ms175972.aspx
withExpression
    : WITH ctes += commonTableExpression (COMMA ctes += commonTableExpression)*
    ;

commonTableExpression
    : expressionName = id (LPAREN columns = columnNameList RPAREN)? AS LPAREN cteQuery = selectStatement RPAREN
    ;

updateElem
    : LOCAL_ID EQ fullColumnName (EQ | assignmentOperator) expression //Combined variable and column update
    | (fullColumnName | LOCAL_ID) (EQ | assignmentOperator) expression
    | udtColumnName = id DOT methodName = id LPAREN expressionList RPAREN
    //| fullColumnName DOT WRITE (expression, )
    ;

updateElemMerge
    : (fullColumnName | LOCAL_ID) (EQ | assignmentOperator) expression
    | udtColumnName = id DOT methodName = id LPAREN expressionList RPAREN
    //| fullColumnName DOT WRITE (expression, )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/queries/search-condition-transact-sql
searchCondition
    : LPAREN searchCondition RPAREN         #scPrec
    | NOT searchCondition                   #scNot
    | searchCondition AND searchCondition   #scAnd
    | searchCondition OR searchCondition    #scOr
    | predicate                             #scPred
    ;

predicate
    : EXISTS LPAREN subquery RPAREN
    | freetextPredicate
    | expression comparisonOperator expression
    | expression ME expression ////SQL-82 syntax for left outer joins; PE. See https://stackoverflow.com/questions/40665/in-sybase-sql
    | expression comparisonOperator (ALL | SOME | ANY) LPAREN subquery RPAREN
    | expression NOT* BETWEEN expression AND expression
    | expression NOT* IN LPAREN (subquery | expressionList) RPAREN
    | expression NOT* LIKE expression (ESCAPE expression)?
    | expression IS nullNotnull
    | expression
    ;

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
// TODO: This is too much for one rule and it still misses things - rewrite
querySpecification
    : SELECT ad=(ALL | DISTINCT)? topClause? selectListElem (COMMA selectListElem)*
    // https://msdn.microsoft.com/en-us/library/ms188029.aspx
    (INTO into =tableName)? (FROM tableSources)? (WHERE where = searchCondition)?
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
    : ORDER BY orderByExpression (COMMA orderByExpression)*
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
    : expression (ASC | DESC)?
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
    : (INSERTED | DELETED) DOT STAR
    | (tableName DOT)? STAR
    ;

udtElem
    : udtColumnName = id DOT nonStaticAttr = id udtMethodArguments asColumnAlias?
    | udtColumnName = id DOUBLE_COLON staticAttr = id udtMethodArguments? asColumnAlias?
    ;

expressionElem
    : columnAlias EQ expression
    | expression asColumnAlias?
    ;

selectListElem
    : asterisk
    | LOCAL_ID op=(PE | ME | SE | DE | MEA | AND_ASSIGN | XOR_ASSIGN | OR_ASSIGN | EQ) expression
    | expressionElem
    | udtElem  // TODO: May not be needed as expressionElem can handle this?
    ;

tableSources
    : source += tableSource (COMMA source += tableSource)*
    ;

// https://sqlenlight.com/support/help/sa0006/
// TODO: This is exactly the same as tableSources alt 2 - investigate
nonAnsiJoin
    : source += tableSource (COMMA source += tableSource)+
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/queries/from-transact-sql
tableSource
    : tableSourceItem joinPart*
    ;

tableSourceItem
    : tableName deprecatedTableHint asTableAlias // this is currently allowed
    | tableName asTableAlias? (
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
    : id dataType STRING?
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
    : LPAREN expression FOR fullColumnName IN columnAliasList RPAREN
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
    | (OPENROWSET LPAREN BULK dataFile = STRING COMMA (bulkOption (COMMA bulkOption)* | id) RPAREN)
    ;

// runtime check.
bulkOption
    : id EQ bulkOptionValue = (INT | STRING)
    ;

derivedTable
    : subquery
    | LPAREN subquery (UNION ALL subquery)* RPAREN
    | tableValueConstructor
    | LPAREN tableValueConstructor RPAREN
    ;

functionCall
    : analyticWindowedFunction
    | builtInFunctions
    | standardFunction
    | freetextFunction
    | partitionFunction
    | hierarchyidStaticMethod
    // TODO: This is broken and highly ambiguous - will need to be reworked so the expression allows the primitives
    // | scalarFunctionName LPAREN expressionList? RPAREN
    ;

// Standard functions are built in but take standard syntax, or are
// some user function etc
standardFunction
    : funcId LPAREN (expression (COMMA expression)*)? RPAREN
    ;

funcId
    : id
    | LOG
    | FORMAT
    | LEFT
    | RIGHT
    | REPLACE
    | CONCAT
    ;

partitionFunction
    : (database = id DOT)? DOLLAR_PARTITION DOT funcName = id LPAREN expression RPAREN
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
    : NEXT VALUE FOR sequenceName = tableName (OVER LPAREN orderByClause RPAREN)? # NEXT_VALUE_FOR
      // https://msdn.microsoft.com/en-us/library/ms173784.aspx
    | BINARY_CHECKSUM LPAREN (star = STAR | expression (COMMA expression)*) RPAREN # BINARY_CHECKSUM
      // https://msdn.microsoft.com/en-us/library/ms189788.aspx
    | CHECKSUM LPAREN (star = STAR | expression (COMMA expression)*) RPAREN # CHECKSUM
      // https://docs.microsoft.com/en-us/sql/t-sql/functions/compress-transact-sql?view=sql-server-ver16
    | CAST LPAREN expression AS dataType RPAREN     # CAST
    | TRY_CAST LPAREN expression AS dataType RPAREN # TRY_CAST
      // https://learn.microsoft.com/en-us/sql/t-sql/functions/ident-seed-transact-sql?view=sql-server-ver16
    | IDENTITY LPAREN datatype = dataType (COMMA seed = INT COMMA increment = INT)? RPAREN # IDENTITY
    | CURSOR_ROWS # CURSOR_ROWS
      // https://learn.microsoft.com/en-us/sql/t-sql/functions/cursor-rows-transact-sql?view=sql-server-ver16
    | FETCH_STATUS # FETCH_STATUS
    | PARSE LPAREN str = expression AS dataType (USING culture = expression)? RPAREN # PARSE
    | JSON_ARRAY LPAREN expressionList? jsonNullClause? RPAREN # JSON_ARRAY
    | JSON_OBJECT LPAREN (keyValue = jsonKeyValue (COMMA keyValue = jsonKeyValue)*)? jsonNullClause? RPAREN # JSON_OBJECT
      // https://msdn.microsoft.com/en-us/library/ms177587.aspx
    | SESSION_USER # SESSION_USER
      // https://msdn.microsoft.com/en-us/library/ms179930.aspx
    | SYSTEM_USER # SYSTEM_USER
      // https://learn.microsoft.com/en-us/sql/t-sql/functions/user-transact-sql?view=sql-server-ver16
    | USER # USER
    ;

valueMethod
    : (
        locId = LOCAL_ID
        | valueId = fullColumnName
        | eventdata = EVENTDATA LPAREN RPAREN
        | LPAREN subquery RPAREN
    ) DOT standardFunction
    ;

hierarchyidStaticMethod
    : HIERARCHYID DOUBLE_COLON (GETROOT LPAREN RPAREN | PARSE LPAREN input = expression RPAREN)
    ;

nodesMethod
    : (locId = LOCAL_ID | valueId = fullColumnName | LPAREN subquery RPAREN) DOT NODES LPAREN xquery = STRING RPAREN
    ;

switchSection
    // Nore that searchCondition includes an expression only but allows too much for case expression.. on purpose
    : WHEN searchCondition THEN expression
    ;

asColumnAlias
    : AS? columnAlias
    ;

asTableAlias
    : AS? (id | DOUBLE_QUOTE_ID)
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
    : id
    | INT
    ;

columnAliasList
    : LPAREN columnAlias (COMMA columnAlias)* RPAREN
    ;

columnAlias
    : id
    | STRING
    ;

tableValueConstructor
    : VALUES LPAREN exps += expressionList RPAREN (COMMA LPAREN exps += expressionList RPAREN)*
    ;

expressionList
    : exp += expression (COMMA exp += expression)*
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/functions/analytic-functions-transact-sql
analyticWindowedFunction
    : (FIRST_VALUE | LAST_VALUE) LPAREN expression RPAREN
    | (LAG | LEAD) LPAREN expression (COMMA expression (COMMA expression)?)? RPAREN
    | (CUME_DIST | PERCENT_RANK) LPAREN RPAREN OVER LPAREN (PARTITION BY expressionList)? orderByClause RPAREN
    | (PERCENTILE_CONT | PERCENTILE_DISC) LPAREN expression RPAREN WITHIN GROUP LPAREN orderByClause RPAREN OVER LPAREN (
        PARTITION BY expressionList
    )? RPAREN
    ;

// https://msdn.microsoft.com/en-us/library/ms189461.aspx
overClause
    : OVER LPAREN (PARTITION BY expression (COMMA expression)*)? orderByClause? rowOrRangeClause? RPAREN
    ;

rowOrRangeClause
    : (ROWS | RANGE) windowFrameExtent
    ;

windowFrameExtent
    : windowFrameBound
    | BETWEEN windowFrameBound AND windowFrameBound
    ;

windowFrameBound
    : UNBOUNDED (PRECEDING | FOLLOWING)
    | INT (PRECEDING | FOLLOWING)
    | CURRENT ROW
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
    : FILEGROUP id (CONTAINS FILESTREAM)? (DEFAULT)? (CONTAINS MEMORY_OPTIMIZED_DATA)? fileSpecification (
        COMMA fileSpecification
    )*
    ;

fileSpecification
    : LPAREN NAME EQ (id | STRING) COMMA? FILENAME EQ file = STRING COMMA? (
        SIZE EQ fileSize COMMA?
    )? (MAXSIZE EQ (fileSize | UNLIMITED) COMMA?)? (FILEGROWTH EQ fileSize COMMA?)? RPAREN
    ;

// Primitive.
entityName
    : (
        server = id DOT database = id DOT schema = id DOT
        | database = id DOT (schema = id)? DOT
        | schema = id DOT
    )? table = id
    ;

entityNameForAzureDw
    : schema = id
    | schema = id DOT objectName = id
    ;

entityNameForParallelDw
    : schemaDatabase = id
    | schema = id DOT objectName = id
    ;

tableName
    : (linkedServer = id DOT DOT)? ids+=id (DOT ids +=id)*
    ;

simpleName
    : (schema = id DOT)? name = id
    ;

funcProcNameSchema
    : ((schema = id) DOT)? procedure = id
    ;

funcProcNameDatabaseSchema
    : database = id? DOT schema = id? DOT procedure = id
    | funcProcNameSchema
    ;

funcProcNameServerDatabaseSchema
    : server = id? DOT database = id? DOT schema = id? DOT procedure = id
    | funcProcNameDatabaseSchema
    ;

ddlObject
    : tableName
    | LOCAL_ID
    ;

fullColumnName
    : ((DELETED | INSERTED | tableName) DOT)? (
          id
        | (DOLLAR (IDENTITY | ROWGUID))
    )
    ;

columnNameListWithOrder
    : id (ASC | DESC)? (COMMA id (ASC | DESC)?)*
    ;

//For some reason, sql server allows any number of prefixes:  Here, h is the column: a.b.c.d.e.f.g.h
insertColumnNameList
    : col += insertColumnId (COMMA col += insertColumnId)*
    ;

insertColumnId
    : (ignore += id? DOT)* id
    ;

columnNameList
    : col += id (COMMA col += id)*
    ;

cursorName
    : id
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
    : (id | expression)
    ;

serviceName
    : (id | expression)
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
    : (databaseName = id DOT schemaName = id DOT name = id)
    | id
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
    | extType = id LPAREN scale = INT COMMA prec = INT RPAREN
    | extType = id LPAREN scale = INT RPAREN
    | extType = id IDENTITY (LPAREN seed = INT COMMA inc = INT RPAREN)?
    | doublePrec = DOUBLE PRECISION?
    | unscaledType = id
    ;

// https://msdn.microsoft.com/en-us/library/ms179899.aspx
constant
    : con = (
          STRING
        | HEX
        | INT
        | REAL
        | FLOAT
        | MONEY
        )
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
    | APPLICATION_LOG
    | APPLY
    | ARITHABORT
    | ARITHIGNORE
    | ASSEMBLY
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
    | CHANGE
    | CHANGE_RETENTION
    | CHANGE_TRACKING
    | CHECKALLOC
    | CHECKCATALOG
    | CHECKCONSTRAINTS
    | CHECKDB
    | CHECKFILEGROUP
    | CHECKSUM
    | CHECKTABLE
    | CLEANTABLE
    | CLEANUP
    | CLONEDATABASE
    | COLLECTION
    | COLUMN_ENCRYPTION_KEY
    | COLUMN_MASTER_KEY
    | COLUMNS
    | COLUMNSTORE
    | COLUMNSTORE_ARCHIVE
    | COMMITTED
    | COMPATIBILITY_LEVEL
    | COMPRESS_ALL_ROW_GROUPS
    | COMPRESSION_DELAY
    | CONCAT
    | CONCAT_NULL_YIELDS_NULL
    | CONTENT
    | CONTROL
    | COOKIE
    | COUNTER
    | CPU
    | CREATE_NEW
    | CREATION_DISPOSITION
    | CREDENTIAL
    | CRYPTOGRAPHIC
    | CUME_DIST
    | CURSOR_CLOSE_ON_COMMIT
    | CURSOR_DEFAULT
    | DATA
    | DATA_PURITY
    | DATE_CORRELATION_OPTIMIZATION
    | DAYS
    | DB_CHAINING
    | DB_FAILOVER
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
    | DEPENDENTS
    | DES
    | DESCRIPTION
    | DESX
    | DETERMINISTIC
    | DHCP
    | DIALOG
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
    | FILEGROUP
    | FILEGROWTH
    | FILENAME
    | FILEPATH
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
    | GB
    | GENERATED
    | GLOBAL
    | GO
    | GROUP_MAX_REQUESTS
    | GROUPING
    | HADR
    | HASH
    | HEALTH_CHECK_TIMEOUT
    | HIDDEN_KEYWORD
    | HIGH
    | HONOR_BROKER_PRIORITY
    | HOURS
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
    | INITIATOR
    | INPUT
    | INSENSITIVE
    | INSERTED
    | KWINT
    | IP
    | ISOLATION
    | JOB
    | JSON
    | JSON_OBJECT
    | JSON_ARRAY
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
    | LOOP
    | LOW
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
    | MIN_CPU_PERCENT
    | MIN_IOPS_PER_VOLUME
    | MIN_MEMORY_PERCENT
    | MINUTES
    | MIRROR_ADDRESS
    | MIXED_PAGE_ALLOCATION
    | MODE
    | MODIFY
    | MOVE
    | MULTI_USER
    | NAME
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
    | PARSEONLY
    | PARTITION
    | PARTITIONS
    | PARTNER
    | PATH
    | PAUSE
    | PDW_SHOWSPACEUSED
    | PERCENT_RANK
    | PERCENTILE_CONT
    | PERCENTILE_DISC
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
    | QUERY
    | QUEUE
    | QUEUE_DELAY
    | QUOTED_IDENTIFIER
    | RANDOMIZED
    | RANGE
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
    | ROBUST
    | ROOT
    | ROUTE
    | ROW
    | ROWGUID
    | ROWLOCK
    | ROWS
    | SAMPLE
    | SCHEMABINDING
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
    | SERVICEBROKER
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
    | SPARSE
    | SPATIAL_WINDOW_MAX_CELLS
    | STANDBY
    | START_DATE
    | STATIC
    | STATISTICS_INCREMENTAL
    | STATISTICS_NORECOMPUTE
    | STATS_STREAM
    | STATUS
    | STATUSONLY
    | STOPLIST
    | SUBJECT
    | SUBSCRIBE
    | SUBSCRIPTION
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
    | TRIPLE_DES
    | TRIPLE_DES_3KEY
    | TRUSTWORTHY
    | TRY
    | TSQL
    | TWO_DIGIT_YEAR_CUTOFF
    | TYPE
    | TYPE_WARNING
    | UNBOUNDED
    | UNCOMMITTED
    | UNKNOWN
    | UNLIMITED
    | UNMASK
    | UOW
    | UPDLOCK
    | USING
    | VALID_XML
    | VALIDATION
    | VALUE
    | VAR
    | VARBINARY_KEYWORD
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
    | COMPRESSION
    | CONNECT
    | CONNECTION
    | CONFIGURATION
    | CONTAINMENT
    | CONTEXT
    | CONTINUE_AFTER_ERROR
    | CONTRACT
    | CONTRACT_NAME
    | CONVERSATION
    | COPY_ONLY
    | CYCLE
    | DATA_COMPRESSION
    | DATA_SOURCE
    | DATABASE_MIRRORING
    | DATASPACE
    | DDL
    | DEFAULT_DATABASE
    | DEFAULT_SCHEMA
    | DIAGNOSTICS
    | DIFFERENTIAL
    | DISTRIBUTION
    | DTC_SUPPORT
    | ENABLED
    | ENDPOINT
    | ERROR
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
    | GET
    | GETROOT
    | GOVERNOR
    | HASHED
    | HEALTHCHECKTIMEOUT
    | HEAP
    | HIERARCHYID
    | IIF
    | IO
    | INCLUDE
    | INCREMENT
    | INFINITE
    | INIT
    | INSTEAD
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
    //
    | SP_EXECUTESQL
    //Built-ins:
    | VARCHAR
    | NVARCHAR
    | PRECISION //For some reason this is possible to use as ID
    | FILESTREAM_ON
    ;

// https://msdn.microsoft.com/en-us/library/ms175874.aspx
id
    : ID
    | TEMP_ID
    | DOUBLE_QUOTE_ID
    | DOUBLE_QUOTE_BLANK // TODO: This is unnecessary I think - remove
    | SQUARE_BRACKET_ID
    | keyword
    | RAW
    ;

simpleId
    : ID
    ;

idOrString
    : id
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
