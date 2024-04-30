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

tsql_file
    : batch* EOF
    | execute_body_batch go_statement* EOF
    ;

batch
    : go_statement
    | execute_body_batch? (go_statement | sql_clauses+) go_statement*
    | batch_level_statement go_statement*
    ;

batch_level_statement
    : create_or_alter_function
    | create_or_alter_procedure
    | create_or_alter_trigger
    | create_view
    ;

sql_clauses
    : dml_clause SEMI?
    | cfl_statement SEMI?
    | another_statement SEMI?
    | ddl_clause SEMI?
    | dbcc_clause SEMI?
    | backup_statement SEMI?
    | SEMI
    ;

// Data Manipulation Language: https://msdn.microsoft.com/en-us/library/ff848766(v=sql.120).aspx
dml_clause
    : merge_statement
    | delete_statement
    | insert_statement
    | select_statement_standalone
    | update_statement
    ;

// Data Definition Language: https://msdn.microsoft.com/en-us/library/ff848799.aspx)
ddl_clause
    : alter_application_role
    | alter_assembly
    | alter_asymmetric_key
    | alter_authorization
    | alter_authorization_for_azure_dw
    | alter_authorization_for_parallel_dw
    | alter_authorization_for_sql_database
    | alter_availability_group
    | alter_certificate
    | alter_column_encryption_key
    | alter_credential
    | alter_cryptographic_provider
    | alter_database
    | alter_database_audit_specification
    | alter_db_role
    | alter_endpoint
    | alter_external_data_source
    | alter_external_library
    | alter_external_resource_pool
    | alter_fulltext_catalog
    | alter_fulltext_stoplist
    | alter_index
    | alter_login_azure_sql
    | alter_login_azure_sql_dw_and_pdw
    | alter_login_sql_server
    | alter_master_key_azure_sql
    | alter_master_key_sql_server
    | alter_message_type
    | alter_partition_function
    | alter_partition_scheme
    | alter_remote_service_binding
    | alter_resource_governor
    | alter_schema_azure_sql_dw_and_pdw
    | alter_schema_sql
    | alter_sequence
    | alter_server_audit
    | alter_server_audit_specification
    | alter_server_configuration
    | alter_server_role
    | alter_server_role_pdw
    | alter_service
    | alter_service_master_key
    | alter_symmetric_key
    | alter_table
    | alter_user
    | alter_user_azure_sql
    | alter_workload_group
    | alter_xml_schema_collection
    | create_application_role
    | create_assembly
    | create_asymmetric_key
    | create_column_encryption_key
    | create_column_master_key
    | create_columnstore_index
    | create_credential
    | create_cryptographic_provider
    | create_database
    | create_database_audit_specification
    | create_db_role
    | create_endpoint
    | create_event_notification
    | create_external_library
    | create_external_resource_pool
    | create_fulltext_catalog
    | create_fulltext_stoplist
    | create_index
    | create_login_azure_sql
    | create_login_pdw
    | create_login_sql_server
    | create_master_key_azure_sql
    | create_master_key_sql_server
    | create_nonclustered_columnstore_index
    | create_or_alter_broker_priority
    | create_or_alter_event_session
    | create_partition_function
    | create_partition_scheme
    | create_remote_service_binding
    | create_resource_pool
    | create_route
    | create_rule
    | create_schema
    | create_schema_azure_sql_dw_and_pdw
    | create_search_property_list
    | create_security_policy
    | create_sequence
    | create_server_audit
    | create_server_audit_specification
    | create_server_role
    | create_service
    | create_statistics
    | create_synonym
    | create_table
    | create_type
    | create_user
    | create_user_azure_sql_dw
    | create_workload_group
    | create_xml_index
    | create_xml_schema_collection
    | disable_trigger
    | drop_aggregate
    | drop_application_role
    | drop_assembly
    | drop_asymmetric_key
    | drop_availability_group
    | drop_broker_priority
    | drop_certificate
    | drop_column_encryption_key
    | drop_column_master_key
    | drop_contract
    | drop_credential
    | drop_cryptograhic_provider
    | drop_database
    | drop_database_audit_specification
    | drop_database_encryption_key
    | drop_database_scoped_credential
    | drop_db_role
    | drop_default
    | drop_endpoint
    | drop_event_notifications
    | drop_event_session
    | drop_external_data_source
    | drop_external_file_format
    | drop_external_library
    | drop_external_resource_pool
    | drop_external_table
    | drop_fulltext_catalog
    | drop_fulltext_index
    | drop_fulltext_stoplist
    | drop_function
    | drop_index
    | drop_login
    | drop_master_key
    | drop_message_type
    | drop_partition_function
    | drop_partition_scheme
    | drop_procedure
    | drop_queue
    | drop_remote_service_binding
    | drop_resource_pool
    | drop_route
    | drop_rule
    | drop_schema
    | drop_search_property_list
    | drop_security_policy
    | drop_sequence
    | drop_server_audit
    | drop_server_audit_specification
    | drop_server_role
    | drop_service
    | drop_signature
    | drop_statistics
    | drop_statistics_name_azure_dw_and_pdw
    | drop_symmetric_key
    | drop_synonym
    | drop_table
    | drop_trigger
    | drop_type
    | drop_user
    | drop_view
    | drop_workload_group
    | drop_xml_schema_collection
    | enable_trigger
    | lock_table
    | truncate_table
    | update_statistics
    ;

backup_statement
    : backup_database
    | backup_log
    | backup_certificate
    | backup_master_key
    | backup_service_master_key
    ;

// Control-of-Flow Language: https://docs.microsoft.com/en-us/sql/t-sql/language-elements/control-of-flow
cfl_statement
    : block_statement
    | break_statement
    | continue_statement
    | goto_statement
    | if_statement
    | print_statement
    | raiseerror_statement
    | return_statement
    | throw_statement
    | try_catch_statement
    | waitfor_statement
    | while_statement
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/begin-end-transact-sql
block_statement
    : BEGIN SEMI? sql_clauses* END SEMI?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/break-transact-sql
break_statement
    : BREAK SEMI?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/continue-transact-sql
continue_statement
    : CONTINUE SEMI?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/goto-transact-sql
goto_statement
    : GOTO id_ SEMI?
    | id_ COLON SEMI?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/return-transact-sql
return_statement
    : RETURN expression? SEMI?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/if-else-transact-sql
if_statement
    : IF search_condition sql_clauses (ELSE sql_clauses)? SEMI?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/throw-transact-sql
throw_statement
    : THROW (throw_error_number COMMA throw_message COMMA throw_state)? SEMI?
    ;

throw_error_number
    : INT
    | LOCAL_ID
    ;

throw_message
    : STRING
    | LOCAL_ID
    ;

throw_state
    : INT
    | LOCAL_ID
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/try-catch-transact-sql
try_catch_statement
    : BEGIN TRY SEMI? try_clauses = sql_clauses+ END TRY SEMI? BEGIN CATCH SEMI? catch_clauses = sql_clauses* END CATCH SEMI?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/waitfor-transact-sql
waitfor_statement
    : WAITFOR receive_statement? COMMA? ((DELAY | TIME | TIMEOUT) time)? expression? SEMI?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/while-transact-sql
while_statement
    : WHILE search_condition (sql_clauses | BREAK SEMI? | CONTINUE SEMI?)
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/print-transact-sql
print_statement
    : PRINT (expression | DOUBLE_QUOTE_ID) (COMMA LOCAL_ID)* SEMI?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/raiserror-transact-sql
raiseerror_statement
    : RAISERROR LPAREN msg = (INT | STRING | LOCAL_ID) COMMA severity = constant_LOCAL_ID COMMA state = constant_LOCAL_ID (
        COMMA (constant_LOCAL_ID | NULL_)
    )* RPAREN (WITH (LOG | SETERROR | NOWAIT))? SEMI?
    | RAISERROR INT formatstring = (STRING | LOCAL_ID | DOUBLE_QUOTE_ID) (
        COMMA argument = (INT | STRING | LOCAL_ID)
    )*
    ;

empty_statement
    : SEMI
    ;

another_statement
    : alter_queue
    | checkpoint_statement
    | conversation_statement
    | create_contract
    | create_queue
    | cursor_statement
    | declare_statement
    | execute_statement
    | kill_statement
    | message_statement
    | reconfigure_statement
    | security_statement
    | set_statement
    | setuser_statement
    | shutdown_statement
    | transaction_statement
    | use_statement
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-application-role-transact-sql
alter_application_role
    : ALTER APPLICATION ROLE appliction_role = id_ WITH (
        COMMA? NAME EQ new_application_role_name = id_
    )? (COMMA? PASSWORD EQ application_role_password = STRING)? (
        COMMA? DEFAULT_SCHEMA EQ app_role_default_schema = id_
    )?
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-xml-schema-collection-transact-sql?view=sql-server-ver16
alter_xml_schema_collection
    : ALTER XML SCHEMA COLLECTION (id_ DOT)? id_ ADD STRING
    ;

create_application_role
    : CREATE APPLICATION ROLE appliction_role = id_ WITH (
        COMMA? PASSWORD EQ application_role_password = STRING
    )? (COMMA? DEFAULT_SCHEMA EQ app_role_default_schema = id_)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-aggregate-transact-sql

drop_aggregate
    : DROP AGGREGATE (IF EXISTS)? (schema_name = id_ DOT)? aggregate_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-application-role-transact-sql
drop_application_role
    : DROP APPLICATION ROLE rolename = id_
    ;

alter_assembly
    : alter_assembly_start assembly_name = id_ alter_assembly_clause
    ;

alter_assembly_start
    : ALTER ASSEMBLY
    ;

alter_assembly_clause
    : alter_assembly_from_clause? alter_assembly_with_clause? alter_assembly_drop_clause? alter_assembly_add_clause?
    ;

alter_assembly_from_clause
    : alter_assembly_from_clause_start (client_assembly_specifier | alter_assembly_file_bits)
    ;

alter_assembly_from_clause_start
    : FROM
    ;

alter_assembly_drop_clause
    : alter_assembly_drop alter_assembly_drop_multiple_files
    ;

alter_assembly_drop_multiple_files
    : ALL
    | multiple_local_files
    ;

alter_assembly_drop
    : DROP
    ;

alter_assembly_add_clause
    : alter_asssembly_add_clause_start alter_assembly_client_file_clause
    ;

alter_asssembly_add_clause_start
    : ADD FILE FROM
    ;

// need to implement
alter_assembly_client_file_clause
    : alter_assembly_file_name (alter_assembly_as id_)?
    ;

alter_assembly_file_name
    : STRING
    ;

//need to implement
alter_assembly_file_bits
    : alter_assembly_as id_
    ;

alter_assembly_as
    : AS
    ;

alter_assembly_with_clause
    : alter_assembly_with assembly_option
    ;

alter_assembly_with
    : WITH
    ;

client_assembly_specifier
    : network_file_share
    | local_file
    | STRING
    ;

assembly_option
    : PERMISSION_SET EQ (SAFE | EXTERNAL_ACCESS | UNSAFE)
    | VISIBILITY EQ on_off
    | UNCHECKED DATA
    | assembly_option COMMA
    ;

network_file_share
    : BACKSLASH BACKSLASH network_computer file_path
    ;

network_computer
    : computer_name = id_
    ;

file_path
    : BACKSLASH file_path
    | id_
    ;

local_file
    : local_drive file_path
    ;

local_drive
    : DISK_DRIVE
    ;

multiple_local_files
    : multiple_local_file_start local_file SINGLE_QUOTE COMMA
    | local_file
    ;

multiple_local_file_start
    : SINGLE_QUOTE
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-assembly-transact-sql
create_assembly
    : CREATE ASSEMBLY assembly_name = id_ (AUTHORIZATION owner_name = id_)? FROM (
        COMMA? (STRING | HEX)
    )+ (WITH PERMISSION_SET EQ (SAFE | EXTERNAL_ACCESS | UNSAFE))?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-assembly-transact-sql
drop_assembly
    : DROP ASSEMBLY (IF EXISTS)? (COMMA? assembly_name = id_)+ (WITH NO DEPENDENTS)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-asymmetric-key-transact-sql

alter_asymmetric_key
    : alter_asymmetric_key_start Asym_Key_Name = id_ (asymmetric_key_option | REMOVE PRIVATE KEY)
    ;

alter_asymmetric_key_start
    : ALTER ASYMMETRIC KEY
    ;

asymmetric_key_option
    : asymmetric_key_option_start asymmetric_key_password_change_option (
        COMMA asymmetric_key_password_change_option
    )? RPAREN
    ;

asymmetric_key_option_start
    : WITH PRIVATE KEY LPAREN
    ;

asymmetric_key_password_change_option
    : DECRYPTION BY PASSWORD EQ STRING
    | ENCRYPTION BY PASSWORD EQ STRING
    ;

//https://docs.microsoft.com/en-us/sql/t-sql/statements/create-asymmetric-key-transact-sql

create_asymmetric_key
    : CREATE ASYMMETRIC KEY Asym_Key_Nam = id_ (AUTHORIZATION database_principal_name = id_)? (
        FROM (
            FILE EQ STRING
            | EXECUTABLE_FILE EQ STRING
            | ASSEMBLY Assembly_Name = id_
            | PROVIDER Provider_Name = id_
        )
    )? (
        WITH (
            ALGORITHM EQ (RSA_4096 | RSA_3072 | RSA_2048 | RSA_1024 | RSA_512)
            | PROVIDER_KEY_NAME EQ provider_key_name = STRING
            | CREATION_DISPOSITION EQ (CREATE_NEW | OPEN_EXISTING)
        )
    )? (ENCRYPTION BY PASSWORD EQ asymmetric_key_password = STRING)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-asymmetric-key-transact-sql
drop_asymmetric_key
    : DROP ASYMMETRIC KEY key_name = id_ (REMOVE PROVIDER KEY)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-authorization-transact-sql

alter_authorization
    : alter_authorization_start (class_type colon_colon)? entity = entity_name entity_to authorization_grantee
    ;

authorization_grantee
    : principal_name = id_
    | SCHEMA OWNER
    ;

entity_to
    : TO
    ;

colon_colon
    : DOUBLE_COLON
    ;

alter_authorization_start
    : ALTER AUTHORIZATION ON
    ;

alter_authorization_for_sql_database
    : alter_authorization_start (class_type_for_sql_database colon_colon)? entity = entity_name entity_to authorization_grantee
    ;

alter_authorization_for_azure_dw
    : alter_authorization_start (class_type_for_azure_dw colon_colon)? entity = entity_name_for_azure_dw entity_to authorization_grantee
    ;

alter_authorization_for_parallel_dw
    : alter_authorization_start (class_type_for_parallel_dw colon_colon)? entity = entity_name_for_parallel_dw entity_to authorization_grantee
    ;

class_type
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

class_type_for_sql_database
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

class_type_for_azure_dw
    : SCHEMA
    | OBJECT
    ;

class_type_for_parallel_dw
    : DATABASE
    | SCHEMA
    | OBJECT
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/grant-transact-sql?view=sql-server-ver15
// SELECT DISTINCT '| ' + CLASS_DESC
// FROM sys.dm_audit_actions
// ORDER BY 1
class_type_for_grant
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
drop_availability_group
    : DROP AVAILABILITY GROUP group_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-availability-group-transact-sql
alter_availability_group
    : alter_availability_group_start alter_availability_group_options
    ;

alter_availability_group_start
    : ALTER AVAILABILITY GROUP group_name = id_
    ;

alter_availability_group_options
    : SET LPAREN (
        (
            AUTOMATED_BACKUP_PREFERENCE EQ (PRIMARY | SECONDARY_ONLY | SECONDARY | NONE)
            | FAILURE_CONDITION_LEVEL EQ INT
            | HEALTH_CHECK_TIMEOUT EQ milliseconds = INT
            | DB_FAILOVER EQ ( ON | OFF)
            | REQUIRED_SYNCHRONIZED_SECONDARIES_TO_COMMIT EQ INT
        ) RPAREN
    )
    | ADD DATABASE database_name = id_
    | REMOVE DATABASE database_name = id_
    | ADD REPLICA ON server_instance = STRING (
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
        | SESSION_TIMEOUT EQ session_timeout = INT
    )
    | MODIFY REPLICA ON server_instance = STRING (
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
            | SESSION_TIMEOUT EQ session_timeout = INT
        )
    ) RPAREN
    | REMOVE REPLICA ON STRING
    | JOIN
    | JOIN AVAILABILITY GROUP ON (
        COMMA? ag_name = STRING WITH LPAREN (
            LISTENER_URL EQ STRING COMMA AVAILABILITY_MODE EQ (
                SYNCHRONOUS_COMMIT
                | ASYNCHRONOUS_COMMIT
            ) COMMA FAILOVER_MODE EQ MANUAL COMMA SEEDING_MODE EQ (AUTOMATIC | MANUAL) RPAREN
        )
    )+
    | MODIFY AVAILABILITY GROUP ON (
        COMMA? ag_name_modified = STRING WITH LPAREN (
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
    | ADD LISTENER listener_name = STRING LPAREN (
        WITH DHCP (ON LPAREN ip_v4_failover ip_v4_failover RPAREN)
        | WITH IP LPAREN (
            (COMMA? LPAREN ( ip_v4_failover COMMA ip_v4_failover | ip_v6_failover) RPAREN)+ RPAREN (
                COMMA PORT EQ INT
            )?
        )
    ) RPAREN
    | MODIFY LISTENER (
        ADD IP LPAREN (ip_v4_failover ip_v4_failover | ip_v6_failover) RPAREN
        | PORT EQ INT
    )
    | RESTART LISTENER STRING
    | REMOVE LISTENER STRING
    | OFFLINE
    | WITH LPAREN DTC_SUPPORT EQ PER_DB RPAREN
    ;

ip_v4_failover
    : STRING
    ;

ip_v6_failover
    : STRING
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-broker-priority-transact-sql
// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-broker-priority-transact-sql
create_or_alter_broker_priority
    : (CREATE | ALTER) BROKER PRIORITY ConversationPriorityName = id_ FOR CONVERSATION SET LPAREN (
        CONTRACT_NAME EQ ( ( id_) | ANY) COMMA?
    )? (LOCAL_SERVICE_NAME EQ (DOUBLE_FORWARD_SLASH? id_ | ANY) COMMA?)? (
        REMOTE_SERVICE_NAME EQ (RemoteServiceName = STRING | ANY) COMMA?
    )? (PRIORITY_LEVEL EQ ( PriorityValue = INT | DEFAULT))? RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-broker-priority-transact-sql
drop_broker_priority
    : DROP BROKER PRIORITY ConversationPriorityName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-certificate-transact-sql
alter_certificate
    : ALTER CERTIFICATE certificate_name = id_ (
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
alter_column_encryption_key
    : ALTER COLUMN ENCRYPTION KEY column_encryption_key = id_ (ADD | DROP) VALUE LPAREN COLUMN_MASTER_KEY EQ column_master_key_name = id_ (
        COMMA ALGORITHM EQ algorithm_name = STRING COMMA ENCRYPTED_VALUE EQ HEX
    )? RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-column-encryption-key-transact-sql
create_column_encryption_key
    : CREATE COLUMN ENCRYPTION KEY column_encryption_key = id_ WITH VALUES (
        LPAREN COMMA? COLUMN_MASTER_KEY EQ column_master_key_name = id_ COMMA ALGORITHM EQ algorithm_name = STRING COMMA ENCRYPTED_VALUE
            EQ encrypted_value = HEX RPAREN COMMA?
    )+
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-certificate-transact-sql
drop_certificate
    : DROP CERTIFICATE certificate_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-column-encryption-key-transact-sql
drop_column_encryption_key
    : DROP COLUMN ENCRYPTION KEY key_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-column-master-key-transact-sql
drop_column_master_key
    : DROP COLUMN MASTER KEY key_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-contract-transact-sql
drop_contract
    : DROP CONTRACT dropped_contract_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-credential-transact-sql
drop_credential
    : DROP CREDENTIAL credential_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-cryptographic-provider-transact-sql
drop_cryptograhic_provider
    : DROP CRYPTOGRAPHIC PROVIDER provider_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-database-transact-sql
drop_database
    : DROP DATABASE (IF EXISTS)? (COMMA? database_name_or_database_snapshot_name = id_)+
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-database-audit-specification-transact-sql
drop_database_audit_specification
    : DROP DATABASE AUDIT SPECIFICATION audit_specification_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-database-encryption-key-transact-sql?view=sql-server-ver15
drop_database_encryption_key
    : DROP DATABASE ENCRYPTION KEY
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-database-scoped-credential-transact-sql
drop_database_scoped_credential
    : DROP DATABASE SCOPED CREDENTIAL credential_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-default-transact-sql
drop_default
    : DROP DEFAULT (IF EXISTS)? (COMMA? (schema_name = id_ DOT)? default_name = id_)
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-endpoint-transact-sql
drop_endpoint
    : DROP ENDPOINT endPointName = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-external-data-source-transact-sql
drop_external_data_source
    : DROP EXTERNAL DATA SOURCE external_data_source_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-external-file-format-transact-sql
drop_external_file_format
    : DROP EXTERNAL FILE FORMAT external_file_format_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-external-library-transact-sql
drop_external_library
    : DROP EXTERNAL LIBRARY library_name = id_ (AUTHORIZATION owner_name = id_)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-external-resource-pool-transact-sql
drop_external_resource_pool
    : DROP EXTERNAL RESOURCE POOL pool_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-external-table-transact-sql
drop_external_table
    : DROP EXTERNAL TABLE (database_name = id_ DOT)? (schema_name = id_ DOT)? table = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-event-notification-transact-sql
drop_event_notifications
    : DROP EVENT NOTIFICATION (COMMA? notification_name = id_)+ ON (
        SERVER
        | DATABASE
        | QUEUE queue_name = id_
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-event-session-transact-sql
drop_event_session
    : DROP EVENT SESSION event_session_name = id_ ON SERVER
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-fulltext-catalog-transact-sql
drop_fulltext_catalog
    : DROP FULLTEXT CATALOG catalog_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-fulltext-index-transact-sql
drop_fulltext_index
    : DROP FULLTEXT INDEX ON (schema = id_ DOT)? table = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-fulltext-stoplist-transact-sql
drop_fulltext_stoplist
    : DROP FULLTEXT STOPLIST stoplist_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-login-transact-sql
drop_login
    : DROP LOGIN login_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-master-key-transact-sql
drop_master_key
    : DROP MASTER KEY
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-message-type-transact-sql
drop_message_type
    : DROP MESSAGE TYPE message_type_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-partition-function-transact-sql
drop_partition_function
    : DROP PARTITION FUNCTION partition_function_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-partition-scheme-transact-sql
drop_partition_scheme
    : DROP PARTITION SCHEME partition_scheme_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-queue-transact-sql
drop_queue
    : DROP QUEUE (database_name = id_ DOT)? (schema_name = id_ DOT)? queue_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-remote-service-binding-transact-sql
drop_remote_service_binding
    : DROP REMOTE SERVICE BINDING binding_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-resource-pool-transact-sql
drop_resource_pool
    : DROP RESOURCE POOL pool_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-role-transact-sql
drop_db_role
    : DROP ROLE (IF EXISTS)? role_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-route-transact-sql
drop_route
    : DROP ROUTE route_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-rule-transact-sql
drop_rule
    : DROP RULE (IF EXISTS)? (COMMA? (schema_name = id_ DOT)? rule_name = id_)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-schema-transact-sql
drop_schema
    : DROP SCHEMA (IF EXISTS)? schema_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-search-property-list-transact-sql
drop_search_property_list
    : DROP SEARCH PROPERTY LIST property_list_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-security-policy-transact-sql
drop_security_policy
    : DROP SECURITY POLICY (IF EXISTS)? (schema_name = id_ DOT)? security_policy_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-sequence-transact-sql
drop_sequence
    : DROP SEQUENCE (IF EXISTS)? (
        COMMA? (database_name = id_ DOT)? (schema_name = id_ DOT)? sequence_name = id_
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-server-audit-transact-sql
drop_server_audit
    : DROP SERVER AUDIT audit_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-server-audit-specification-transact-sql
drop_server_audit_specification
    : DROP SERVER AUDIT SPECIFICATION audit_specification_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-server-role-transact-sql
drop_server_role
    : DROP SERVER ROLE role_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-service-transact-sql
drop_service
    : DROP SERVICE dropped_service_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-signature-transact-sql
drop_signature
    : DROP (COUNTER)? SIGNATURE FROM (schema_name = id_ DOT)? module_name = id_ BY (
        COMMA? CERTIFICATE cert_name = id_
        | COMMA? ASYMMETRIC KEY Asym_key_name = id_
    )+
    ;

drop_statistics_name_azure_dw_and_pdw
    : DROP STATISTICS (schema_name = id_ DOT)? object_name = id_ DOT statistics_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-symmetric-key-transact-sql
drop_symmetric_key
    : DROP SYMMETRIC KEY symmetric_key_name = id_ (REMOVE PROVIDER KEY)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-synonym-transact-sql
drop_synonym
    : DROP SYNONYM (IF EXISTS)? (schema = id_ DOT)? synonym_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-user-transact-sql
drop_user
    : DROP USER (IF EXISTS)? user_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-workload-group-transact-sql
drop_workload_group
    : DROP WORKLOAD GROUP group_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-xml-schema-collection-transact-sql
drop_xml_schema_collection
    : DROP XML SCHEMA COLLECTION (relational_schema = id_ DOT)? sql_identifier = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/disable-trigger-transact-sql
disable_trigger
    : DISABLE TRIGGER (( COMMA? (schema_name = id_ DOT)? trigger_name = id_)+ | ALL) ON (
        (schema_id = id_ DOT)? object_name = id_
        | DATABASE
        | ALL SERVER
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/enable-trigger-transact-sql
enable_trigger
    : ENABLE TRIGGER (( COMMA? (schema_name = id_ DOT)? trigger_name = id_)+ | ALL) ON (
        (schema_id = id_ DOT)? object_name = id_
        | DATABASE
        | ALL SERVER
    )
    ;

lock_table
    : LOCK TABLE table_name IN (SHARE | EXCLUSIVE) MODE (WAIT seconds = INT | NOWAIT)? SEMI?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/truncate-table-transact-sql
truncate_table
    : TRUNCATE TABLE table_name (
        WITH LPAREN PARTITIONS LPAREN (COMMA? (INT | INT TO INT))+ RPAREN RPAREN
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-column-master-key-transact-sql
create_column_master_key
    : CREATE COLUMN MASTER KEY key_name = id_ WITH LPAREN KEY_STORE_PROVIDER_NAME EQ key_store_provider_name = STRING COMMA KEY_PATH EQ
        key_path = STRING RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-credential-transact-sql
alter_credential
    : ALTER CREDENTIAL credential_name = id_ WITH IDENTITY EQ identity_name = STRING (
        COMMA SECRET EQ secret = STRING
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-credential-transact-sql
create_credential
    : CREATE CREDENTIAL credential_name = id_ WITH IDENTITY EQ identity_name = STRING (
        COMMA SECRET EQ secret = STRING
    )? (FOR CRYPTOGRAPHIC PROVIDER cryptographic_provider_name = id_)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-cryptographic-provider-transact-sql
alter_cryptographic_provider
    : ALTER CRYPTOGRAPHIC PROVIDER provider_name = id_ (
        FROM FILE EQ crypto_provider_ddl_file = STRING
    )? (ENABLE | DISABLE)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-cryptographic-provider-transact-sql
create_cryptographic_provider
    : CREATE CRYPTOGRAPHIC PROVIDER provider_name = id_ FROM FILE EQ path_of_DLL = STRING
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/statements/create-endpoint-transact-sql?view=sql-server-ver16
create_endpoint
    : CREATE ENDPOINT endpointname = id_ (AUTHORIZATION login = id_)? (
        STATE EQ state = (STARTED | STOPPED | DISABLED)
    )? AS TCP LPAREN endpoint_listener_clause RPAREN (
        FOR TSQL LPAREN RPAREN
        | FOR SERVICE_BROKER LPAREN endpoint_authentication_clause (
            COMMA? endpoint_encryption_alogorithm_clause
        )? (COMMA? MESSAGE_FORWARDING EQ (ENABLED | DISABLED))? (
            COMMA? MESSAGE_FORWARD_SIZE EQ INT
        )? RPAREN
        | FOR DATABASE_MIRRORING LPAREN endpoint_authentication_clause (
            COMMA? endpoint_encryption_alogorithm_clause
        )? COMMA? ROLE EQ (WITNESS | PARTNER | ALL) RPAREN
    )
    ;

endpoint_encryption_alogorithm_clause
    : ENCRYPTION EQ (DISABLED | SUPPORTED | REQUIRED) (ALGORITHM (AES RC4? | RC4 AES?))?
    ;

endpoint_authentication_clause
    : AUTHENTICATION EQ (
        WINDOWS (NTLM | KERBEROS | NEGOTIATE)? (CERTIFICATE cert_name = id_)?
        | CERTIFICATE cert_name = id_ WINDOWS? (NTLM | KERBEROS | NEGOTIATE)?
    )
    ;

endpoint_listener_clause
    : LISTENER_PORT EQ port = INT (
        COMMA LISTENER_IP EQ (ALL | LPAREN (ipv4 = IPV4_ADDR | ipv6 = STRING) RPAREN)
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-event-notification-transact-sql
create_event_notification
    : CREATE EVENT NOTIFICATION event_notification_name = id_ ON (
        SERVER
        | DATABASE
        | QUEUE queue_name = id_
    ) (WITH FAN_IN)? FOR (COMMA? event_type_or_group = id_)+ TO SERVICE broker_service = STRING COMMA broker_service_specifier_or_current_database =
        STRING
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-event-session-transact-sql
// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-event-session-transact-sql
// todo: not implemented
create_or_alter_event_session
    : (CREATE | ALTER) EVENT SESSION event_session_name = id_ ON SERVER (
        COMMA? ADD EVENT (
            (event_module_guid = id_ DOT)? event_package_name = id_ DOT event_name = id_
        ) (
            LPAREN (SET ( COMMA? event_customizable_attributue = id_ EQ (INT | STRING))*)? (
                ACTION LPAREN (
                    COMMA? (event_module_guid = id_ DOT)? event_package_name = id_ DOT action_name = id_
                )+ RPAREN
            )+ (WHERE event_session_predicate_expression)? RPAREN
        )*
    )* (
        COMMA? DROP EVENT (event_module_guid = id_ DOT)? event_package_name = id_ DOT event_name = id_
    )* (
        (ADD TARGET (event_module_guid = id_ DOT)? event_package_name = id_ DOT target_name = id_) (
            LPAREN SET (
                COMMA? target_parameter_name = id_ EQ (LPAREN? INT RPAREN? | STRING)
            )+ RPAREN
        )*
    )* (DROP TARGET (event_module_guid = id_ DOT)? event_package_name = id_ DOT target_name = id_)* (
        WITH LPAREN (COMMA? MAX_MEMORY EQ max_memory = INT (KB | MB))? (
            COMMA? EVENT_RETENTION_MODE EQ (
                ALLOW_SINGLE_EVENT_LOSS
                | ALLOW_MULTIPLE_EVENT_LOSS
                | NO_EVENT_LOSS
            )
        )? (
            COMMA? MAX_DISPATCH_LATENCY EQ (
                max_dispatch_latency_seconds = INT SECONDS
                | INFINITE
            )
        )? (COMMA? MAX_EVENT_SIZE EQ max_event_size = INT (KB | MB))? (
            COMMA? MEMORY_PARTITION_MODE EQ (NONE | PER_NODE | PER_CPU)
        )? (COMMA? TRACK_CAUSALITY EQ (ON | OFF))? (COMMA? STARTUP_STATE EQ (ON | OFF))? RPAREN
    )? (STATE EQ (START | STOP))?
    ;

event_session_predicate_expression
    : (
        COMMA? (AND | OR)? NOT? (
            event_session_predicate_factor
            | LPAREN event_session_predicate_expression RPAREN
        )
    )+
    ;

event_session_predicate_factor
    : event_session_predicate_leaf
    | LPAREN event_session_predicate_expression RPAREN
    ;

event_session_predicate_leaf
    : (
        event_field_name = id_
        | (
            event_field_name = id_
            | (
                (event_module_guid = id_ DOT)? event_package_name = id_ DOT predicate_source_name = id_
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
    | (event_module_guid = id_ DOT)? event_package_name = id_ DOT predicate_compare_name = id_ LPAREN (
        event_field_name = id_
        | ((event_module_guid = id_ DOT)? event_package_name = id_ DOT predicate_source_name = id_) COMMA (
            INT
            | STRING
        )
    ) RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-external-data-source-transact-sql
alter_external_data_source
    : ALTER EXTERNAL DATA SOURCE data_source_name = id_ SET (
        LOCATION EQ location = STRING COMMA?
        | RESOURCE_MANAGER_LOCATION EQ resource_manager_location = STRING COMMA?
        | CREDENTIAL EQ credential_name = id_
    )+
    | ALTER EXTERNAL DATA SOURCE data_source_name = id_ WITH LPAREN TYPE EQ BLOB_STORAGE COMMA LOCATION EQ location = STRING (
        COMMA CREDENTIAL EQ credential_name = id_
    )? RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-external-library-transact-sql
alter_external_library
    : ALTER EXTERNAL LIBRARY library_name = id_ (AUTHORIZATION owner_name = id_)? (SET | ADD) (
        LPAREN CONTENT EQ (client_library = STRING | HEX | NONE) (
            COMMA PLATFORM EQ (WINDOWS | LINUX)? RPAREN
        ) WITH (
            COMMA? LANGUAGE EQ (R | PYTHON)
            | DATA_SOURCE EQ external_data_source_name = id_
        )+ RPAREN
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-external-library-transact-sql
create_external_library
    : CREATE EXTERNAL LIBRARY library_name = id_ (AUTHORIZATION owner_name = id_)? FROM (
        COMMA? LPAREN? (CONTENT EQ)? (client_library = STRING | HEX | NONE) (
            COMMA PLATFORM EQ (WINDOWS | LINUX)? RPAREN
        )?
    ) (
        WITH (
            COMMA? LANGUAGE EQ (R | PYTHON)
            | DATA_SOURCE EQ external_data_source_name = id_
        )+ RPAREN
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-external-resource-pool-transact-sql
alter_external_resource_pool
    : ALTER EXTERNAL RESOURCE POOL (pool_name = id_ | DEFAULT_DOUBLE_QUOTE) WITH LPAREN MAX_CPU_PERCENT EQ max_cpu_percent = INT (
        COMMA? AFFINITY CPU EQ (AUTO | (COMMA? INT TO INT | COMMA INT)+)
        | NUMANODE EQ (COMMA? INT TO INT | COMMA? INT)+
    ) (COMMA? MAX_MEMORY_PERCENT EQ max_memory_percent = INT)? (
        COMMA? MAX_PROCESSES EQ max_processes = INT
    )? RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-external-resource-pool-transact-sql
create_external_resource_pool
    : CREATE EXTERNAL RESOURCE POOL pool_name = id_ WITH LPAREN MAX_CPU_PERCENT EQ max_cpu_percent = INT (
        COMMA? AFFINITY CPU EQ (AUTO | (COMMA? INT TO INT | COMMA INT)+)
        | NUMANODE EQ (COMMA? INT TO INT | COMMA? INT)+
    ) (COMMA? MAX_MEMORY_PERCENT EQ max_memory_percent = INT)? (
        COMMA? MAX_PROCESSES EQ max_processes = INT
    )? RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-fulltext-catalog-transact-sql
alter_fulltext_catalog
    : ALTER FULLTEXT CATALOG catalog_name = id_ (
        REBUILD (WITH ACCENT_SENSITIVITY EQ (ON | OFF))?
        | REORGANIZE
        | AS DEFAULT
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-fulltext-catalog-transact-sql
create_fulltext_catalog
    : CREATE FULLTEXT CATALOG catalog_name = id_ (ON FILEGROUP filegroup = id_)? (
        IN PATH rootpath = STRING
    )? (WITH ACCENT_SENSITIVITY EQ (ON | OFF))? (AS DEFAULT)? (AUTHORIZATION owner_name = id_)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-fulltext-stoplist-transact-sql
alter_fulltext_stoplist
    : ALTER FULLTEXT STOPLIST stoplist_name = id_ (
        ADD stopword = STRING LANGUAGE (STRING | INT | HEX)
        | DROP (
            stopword = STRING LANGUAGE (STRING | INT | HEX)
            | ALL (STRING | INT | HEX)
            | ALL
        )
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-fulltext-stoplist-transact-sql
create_fulltext_stoplist
    : CREATE FULLTEXT STOPLIST stoplist_name = id_ (
        FROM ((database_name = id_ DOT)? source_stoplist_name = id_ | SYSTEM STOPLIST)
    )? (AUTHORIZATION owner_name = id_)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-login-transact-sql
alter_login_sql_server
    : ALTER LOGIN login_name = id_ (
        (ENABLE | DISABLE)?
        | WITH (
            (PASSWORD EQ ( password = STRING | password_hash = HEX HASHED)) (
                MUST_CHANGE
                | UNLOCK
            )*
        )? (OLD_PASSWORD EQ old_password = STRING (MUST_CHANGE | UNLOCK)*)? (
            DEFAULT_DATABASE EQ default_database = id_
        )? (DEFAULT_LANGUAGE EQ default_laguage = id_)? (NAME EQ login_name = id_)? (
            CHECK_POLICY EQ (ON | OFF)
        )? (CHECK_EXPIRATION EQ (ON | OFF))? (CREDENTIAL EQ credential_name = id_)? (
            NO CREDENTIAL
        )?
        | (ADD | DROP) CREDENTIAL credential_name = id_
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-login-transact-sql
create_login_sql_server
    : CREATE LOGIN login_name = id_ (
        WITH (
            (PASSWORD EQ ( password = STRING | password_hash = HEX HASHED)) (
                MUST_CHANGE
                | UNLOCK
            )*
        )? (COMMA? SID EQ sid = HEX)? (COMMA? DEFAULT_DATABASE EQ default_database = id_)? (
            COMMA? DEFAULT_LANGUAGE EQ default_laguage = id_
        )? (COMMA? CHECK_EXPIRATION EQ (ON | OFF))? (COMMA? CHECK_POLICY EQ (ON | OFF))? (
            COMMA? CREDENTIAL EQ credential_name = id_
        )?
        | (
            FROM (
                WINDOWS (
                    WITH (COMMA? DEFAULT_DATABASE EQ default_database = id_)? (
                        COMMA? DEFAULT_LANGUAGE EQ default_language = STRING
                    )?
                )
                | CERTIFICATE certname = id_
                | ASYMMETRIC KEY asym_key_name = id_
            )
        )
    )
    ;

alter_login_azure_sql
    : ALTER LOGIN login_name = id_ (
        (ENABLE | DISABLE)?
        | WITH (
            PASSWORD EQ password = STRING (OLD_PASSWORD EQ old_password = STRING)?
            | NAME EQ login_name = id_
        )
    )
    ;

create_login_azure_sql
    : CREATE LOGIN login_name = id_ WITH PASSWORD EQ STRING (SID EQ sid = HEX)?
    ;

alter_login_azure_sql_dw_and_pdw
    : ALTER LOGIN login_name = id_ (
        (ENABLE | DISABLE)?
        | WITH (
            PASSWORD EQ password = STRING (
                OLD_PASSWORD EQ old_password = STRING (MUST_CHANGE | UNLOCK)*
            )?
            | NAME EQ login_name = id_
        )
    )
    ;

create_login_pdw
    : CREATE LOGIN loginName = id_ (
        WITH (PASSWORD EQ password = STRING (MUST_CHANGE)? (CHECK_POLICY EQ (ON | OFF)?)?)
        | FROM WINDOWS
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-master-key-transact-sql
alter_master_key_sql_server
    : ALTER MASTER KEY (
        (FORCE)? REGENERATE WITH ENCRYPTION BY PASSWORD EQ password = STRING
        | (ADD | DROP) ENCRYPTION BY (
            SERVICE MASTER KEY
            | PASSWORD EQ encryption_password = STRING
        )
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-master-key-transact-sql
create_master_key_sql_server
    : CREATE MASTER KEY ENCRYPTION BY PASSWORD EQ password = STRING
    ;

alter_master_key_azure_sql
    : ALTER MASTER KEY (
        (FORCE)? REGENERATE WITH ENCRYPTION BY PASSWORD EQ password = STRING
        | ADD ENCRYPTION BY (SERVICE MASTER KEY | PASSWORD EQ encryption_password = STRING)
        | DROP ENCRYPTION BY PASSWORD EQ encryption_password = STRING
    )
    ;

create_master_key_azure_sql
    : CREATE MASTER KEY (ENCRYPTION BY PASSWORD EQ password = STRING)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-message-type-transact-sql
alter_message_type
    : ALTER MESSAGE TYPE message_type_name = id_ VALIDATION EQ (
        NONE
        | EMPTY
        | WELL_FORMED_XML
        | VALID_XML WITH SCHEMA COLLECTION schema_collection_name = id_
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-partition-function-transact-sql
alter_partition_function
    : ALTER PARTITION FUNCTION partition_function_name = id_ LPAREN RPAREN (SPLIT | MERGE) RANGE LPAREN INT RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-partition-scheme-transact-sql
alter_partition_scheme
    : ALTER PARTITION SCHEME partition_scheme_name = id_ NEXT USED (file_group_name = id_)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-remote-service-binding-transact-sql
alter_remote_service_binding
    : ALTER REMOTE SERVICE BINDING binding_name = id_ WITH (USER EQ user_name = id_)? (
        COMMA ANONYMOUS EQ (ON | OFF)
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-remote-service-binding-transact-sql
create_remote_service_binding
    : CREATE REMOTE SERVICE BINDING binding_name = id_ (AUTHORIZATION owner_name = id_)? TO SERVICE remote_service_name = STRING WITH (
        USER EQ user_name = id_
    )? (COMMA ANONYMOUS EQ (ON | OFF))?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-resource-pool-transact-sql
create_resource_pool
    : CREATE RESOURCE POOL pool_name = id_ (
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
alter_resource_governor
    : ALTER RESOURCE GOVERNOR (
        (DISABLE | RECONFIGURE)
        | WITH LPAREN CLASSIFIER_FUNCTION EQ (
            schema_name = id_ DOT function_name = id_
            | NULL_
        ) RPAREN
        | RESET STATISTICS
        | WITH LPAREN MAX_OUTSTANDING_IO_PER_VOLUME EQ max_outstanding_io_per_volume = INT RPAREN
    )
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-database-audit-specification-transact-sql?view=sql-server-ver16
alter_database_audit_specification
    : ALTER DATABASE AUDIT SPECIFICATION audit_specification_name = id_ (
        FOR SERVER AUDIT audit_name = id_
    )? (audit_action_spec_group (COMMA audit_action_spec_group)*)? (
        WITH LPAREN STATE EQ (ON | OFF) RPAREN
    )?
    ;

audit_action_spec_group
    : (ADD | DROP) LPAREN (audit_action_specification | audit_action_group_name = id_) RPAREN
    ;

audit_action_specification
    : action_specification (COMMA action_specification)* ON (audit_class_name COLON COLON)? audit_securable BY principal_id (
        COMMA principal_id
    )*
    ;

action_specification
    : SELECT
    | INSERT
    | UPDATE
    | DELETE
    | EXECUTE
    | RECEIVE
    | REFERENCES
    ;

audit_class_name
    : OBJECT
    | SCHEMA
    | TABLE
    ;

audit_securable
    : ((id_ DOT)? id_ DOT)? id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-role-transact-sql
alter_db_role
    : ALTER ROLE role_name = id_ (
        (ADD | DROP) MEMBER database_principal = id_
        | WITH NAME EQ new_role_name = id_
    )
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/statements/create-database-audit-specification-transact-sql?view=sql-server-ver16
create_database_audit_specification
    : CREATE DATABASE AUDIT SPECIFICATION audit_specification_name = id_ (
        FOR SERVER AUDIT audit_name = id_
    )? (audit_action_spec_group (COMMA audit_action_spec_group)*)? (
        WITH LPAREN STATE EQ (ON | OFF) RPAREN
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-role-transact-sql
create_db_role
    : CREATE ROLE role_name = id_ (AUTHORIZATION owner_name = id_)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-route-transact-sql
create_route
    : CREATE ROUTE route_name = id_ (AUTHORIZATION owner_name = id_)? WITH (
        COMMA? SERVICE_NAME EQ route_service_name = STRING
    )? (COMMA? BROKER_INSTANCE EQ broker_instance_identifier = STRING)? (
        COMMA? LIFETIME EQ INT
    )? COMMA? ADDRESS EQ STRING (COMMA MIRROR_ADDRESS EQ STRING)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-rule-transact-sql
create_rule
    : CREATE RULE (schema_name = id_ DOT)? rule_name = id_ AS search_condition
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-schema-transact-sql
alter_schema_sql
    : ALTER SCHEMA schema_name = id_ TRANSFER (
        (OBJECT | TYPE | XML SCHEMA COLLECTION) DOUBLE_COLON
    )? id_ (DOT id_)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-schema-transact-sql
create_schema
    : CREATE SCHEMA (
        schema_name = id_
        | AUTHORIZATION owner_name = id_
        | schema_name = id_ AUTHORIZATION owner_name = id_
    ) (
        create_table
        | create_view
        | (GRANT | DENY) (SELECT | INSERT | DELETE | UPDATE) ON (SCHEMA DOUBLE_COLON)? object_name = id_ TO owner_name = id_
        | REVOKE (SELECT | INSERT | DELETE | UPDATE) ON (SCHEMA DOUBLE_COLON)? object_name = id_ FROM owner_name = id_
    )*
    ;

create_schema_azure_sql_dw_and_pdw
    : CREATE SCHEMA schema_name = id_ (AUTHORIZATION owner_name = id_)?
    ;

alter_schema_azure_sql_dw_and_pdw
    : ALTER SCHEMA schema_name = id_ TRANSFER (OBJECT DOUBLE_COLON)? id_ (DOT ID)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-search-property-list-transact-sql
create_search_property_list
    : CREATE SEARCH PROPERTY LIST new_list_name = id_ (
        FROM (database_name = id_ DOT)? source_list_name = id_
    )? (AUTHORIZATION owner_name = id_)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-security-policy-transact-sql
create_security_policy
    : CREATE SECURITY POLICY (schema_name = id_ DOT)? security_policy_name = id_ (
        COMMA? ADD (FILTER | BLOCK)? PREDICATE tvf_schema_name = id_ DOT security_predicate_function_name = id_ LPAREN (
            COMMA? column_name_or_arguments = id_
        )+ RPAREN ON table_schema_name = id_ DOT name = id_ (
            COMMA? AFTER (INSERT | UPDATE)
            | COMMA? BEFORE (UPDATE | DELETE)
        )*
    )+ (WITH LPAREN STATE EQ (ON | OFF) (SCHEMABINDING (ON | OFF))? RPAREN)? (
        NOT FOR REPLICATION
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-sequence-transact-sql
alter_sequence
    : ALTER SEQUENCE (schema_name = id_ DOT)? sequence_name = id_ (RESTART (WITH INT)?)? (
        INCREMENT BY sequnce_increment = INT
    )? (MINVALUE INT | NO MINVALUE)? (MAXVALUE INT | NO MAXVALUE)? (CYCLE | NO CYCLE)? (
        CACHE INT
        | NO CACHE
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-sequence-transact-sql
create_sequence
    : CREATE SEQUENCE (schema_name = id_ DOT)? sequence_name = id_ (AS data_type)? (
        START WITH INT
    )? (INCREMENT BY MINUS? INT)? (MINVALUE (MINUS? INT)? | NO MINVALUE)? (
        MAXVALUE (MINUS? INT)?
        | NO MAXVALUE
    )? (CYCLE | NO CYCLE)? (CACHE INT? | NO CACHE)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-server-audit-transact-sql
alter_server_audit
    : ALTER SERVER AUDIT audit_name = id_ (
        (
            TO (
                FILE (
                    LPAREN (
                        COMMA? FILEPATH EQ filepath = STRING
                        | COMMA? MAXSIZE EQ ( INT (MB | GB | TB) | UNLIMITED)
                        | COMMA? MAX_ROLLOVER_FILES EQ max_rollover_files = (INT | UNLIMITED)
                        | COMMA? MAX_FILES EQ max_files = INT
                        | COMMA? RESERVE_DISK_SPACE EQ (ON | OFF)
                    )* RPAREN
                )
                | APPLICATION_LOG
                | SECURITY_LOG
            )
        )? (
            WITH LPAREN (
                COMMA? QUEUE_DELAY EQ queue_delay = INT
                | COMMA? ON_FAILURE EQ (CONTINUE | SHUTDOWN | FAIL_OPERATION)
                | COMMA? STATE EQ (ON | OFF)
            )* RPAREN
        )? (
            WHERE (
                COMMA? (NOT?) event_field_name = id_ (
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
        | MODIFY NAME EQ new_audit_name = id_
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-server-audit-transact-sql
create_server_audit
    : CREATE SERVER AUDIT audit_name = id_ (
        (
            TO (
                FILE (
                    LPAREN (
                        COMMA? FILEPATH EQ filepath = STRING
                        | COMMA? MAXSIZE EQ ( INT (MB | GB | TB) | UNLIMITED)
                        | COMMA? MAX_ROLLOVER_FILES EQ max_rollover_files = (INT | UNLIMITED)
                        | COMMA? MAX_FILES EQ max_files = INT
                        | COMMA? RESERVE_DISK_SPACE EQ (ON | OFF)
                    )* RPAREN
                )
                | APPLICATION_LOG
                | SECURITY_LOG
            )
        )? (
            WITH LPAREN (
                COMMA? QUEUE_DELAY EQ queue_delay = INT
                | COMMA? ON_FAILURE EQ (CONTINUE | SHUTDOWN | FAIL_OPERATION)
                | COMMA? STATE EQ (ON | OFF)
                | COMMA? AUDIT_GUID EQ audit_guid = id_
            )* RPAREN
        )? (
            WHERE (
                COMMA? (NOT?) event_field_name = id_ (
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
        | MODIFY NAME EQ new_audit_name = id_
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-server-audit-specification-transact-sql

alter_server_audit_specification
    : ALTER SERVER AUDIT SPECIFICATION audit_specification_name = id_ (
        FOR SERVER AUDIT audit_name = id_
    )? ((ADD | DROP) LPAREN audit_action_group_name = id_ RPAREN)* (
        WITH LPAREN STATE EQ (ON | OFF) RPAREN
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-server-audit-specification-transact-sql
create_server_audit_specification
    : CREATE SERVER AUDIT SPECIFICATION audit_specification_name = id_ (
        FOR SERVER AUDIT audit_name = id_
    )? (ADD LPAREN audit_action_group_name = id_ RPAREN)* (
        WITH LPAREN STATE EQ (ON | OFF) RPAREN
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-server-configuration-transact-sql

alter_server_configuration
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
alter_server_role
    : ALTER SERVER ROLE server_role_name = id_ (
        (ADD | DROP) MEMBER server_principal = id_
        | WITH NAME EQ new_server_role_name = id_
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-server-role-transact-sql
create_server_role
    : CREATE SERVER ROLE server_role = id_ (AUTHORIZATION server_principal = id_)?
    ;

alter_server_role_pdw
    : ALTER SERVER ROLE server_role_name = id_ (ADD | DROP) MEMBER login = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-service-transact-sql
alter_service
    : ALTER SERVICE modified_service_name = id_ (
        ON QUEUE (schema_name = id_ DOT)? queue_name = id_
    )? (LPAREN opt_arg_clause (COMMA opt_arg_clause)* RPAREN)?
    ;

opt_arg_clause
    : (ADD | DROP) CONTRACT modified_contract_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-service-transact-sql
create_service
    : CREATE SERVICE create_service_name = id_ (AUTHORIZATION owner_name = id_)? ON QUEUE (
        schema_name = id_ DOT
    )? queue_name = id_ (LPAREN (COMMA? (id_ | DEFAULT))+ RPAREN)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-service-master-key-transact-sql

alter_service_master_key
    : ALTER SERVICE MASTER KEY (
        FORCE? REGENERATE
        | (
            WITH (
                OLD_ACCOUNT EQ acold_account_name = STRING COMMA OLD_PASSWORD EQ old_password = STRING
                | NEW_ACCOUNT EQ new_account_name = STRING COMMA NEW_PASSWORD EQ new_password = STRING
            )?
        )
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-symmetric-key-transact-sql

alter_symmetric_key
    : ALTER SYMMETRIC KEY key_name = id_ (
        (ADD | DROP) ENCRYPTION BY (
            CERTIFICATE certificate_name = id_
            | PASSWORD EQ password = STRING
            | SYMMETRIC KEY symmetric_key_name = id_
            | ASYMMETRIC KEY Asym_key_name = id_
        )
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-synonym-transact-sql
create_synonym
    : CREATE SYNONYM (schema_name_1 = id_ DOT)? synonym_name = id_ FOR (
        (server_name = id_ DOT)? (database_name = id_ DOT)? (schema_name_2 = id_ DOT)? object_name = id_
        | (database_or_schema2 = id_ DOT)? (schema_id_2_or_object_name = id_ DOT)?
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-user-transact-sql
alter_user
    : ALTER USER username = id_ WITH (
        COMMA? NAME EQ newusername = id_
        | COMMA? DEFAULT_SCHEMA EQ ( schema_name = id_ | NULL_)
        | COMMA? LOGIN EQ loginame = id_
        | COMMA? PASSWORD EQ STRING (OLD_PASSWORD EQ STRING)+
        | COMMA? DEFAULT_LANGUAGE EQ (NONE | lcid = INT | language_name_or_alias = id_)
        | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ (ON | OFF)
    )+
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-user-transact-sql
create_user
    : CREATE USER user_name = id_ ((FOR | FROM) LOGIN login_name = id_)? (
        WITH (
            COMMA? DEFAULT_SCHEMA EQ schema_name = id_
            | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ (ON | OFF)
        )*
    )?
    | CREATE USER (
        windows_principal = id_ (
            WITH (
                COMMA? DEFAULT_SCHEMA EQ schema_name = id_
                | COMMA? DEFAULT_LANGUAGE EQ (NONE | INT | language_name_or_alias = id_)
                | COMMA? SID EQ HEX
                | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ (ON | OFF)
            )*
        )?
        | user_name = id_ WITH PASSWORD EQ password = STRING (
            COMMA? DEFAULT_SCHEMA EQ schema_name = id_
            | COMMA? DEFAULT_LANGUAGE EQ (NONE | INT | language_name_or_alias = id_)
            | COMMA? SID EQ HEX
            | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ (ON | OFF)
        )*
        | Azure_Active_Directory_principal = id_ FROM EXTERNAL PROVIDER
    )
    | CREATE USER user_name = id_ (
        WITHOUT LOGIN (
            COMMA? DEFAULT_SCHEMA EQ schema_name = id_
            | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ (ON | OFF)
        )*
        | (FOR | FROM) CERTIFICATE cert_name = id_
        | (FOR | FROM) ASYMMETRIC KEY asym_key_name = id_
    )
    | CREATE USER user_name = id_
    ;

create_user_azure_sql_dw
    : CREATE USER user_name = id_ ((FOR | FROM) LOGIN login_name = id_ | WITHOUT LOGIN)? (
        WITH DEFAULT_SCHEMA EQ schema_name = id_
    )?
    | CREATE USER Azure_Active_Directory_principal = id_ FROM EXTERNAL PROVIDER (
        WITH DEFAULT_SCHEMA EQ schema_name = id_
    )?
    ;

alter_user_azure_sql
    : ALTER USER username = id_ WITH (
        COMMA? NAME EQ newusername = id_
        | COMMA? DEFAULT_SCHEMA EQ schema_name = id_
        | COMMA? LOGIN EQ loginame = id_
        | COMMA? ALLOW_ENCRYPTED_VALUE_MODIFICATIONS EQ (ON | OFF)
    )+
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-workload-group-transact-sql

alter_workload_group
    : ALTER WORKLOAD GROUP (workload_group_group_name = id_ | DEFAULT_DOUBLE_QUOTE) (
        WITH LPAREN (
            IMPORTANCE EQ (LOW | MEDIUM | HIGH)
            | COMMA? REQUEST_MAX_MEMORY_GRANT_PERCENT EQ request_max_memory_grant = INT
            | COMMA? REQUEST_MAX_CPU_TIME_SEC EQ request_max_cpu_time_sec = INT
            | REQUEST_MEMORY_GRANT_TIMEOUT_SEC EQ request_memory_grant_timeout_sec = INT
            | MAX_DOP EQ max_dop = INT
            | GROUP_MAX_REQUESTS EQ group_max_requests = INT
        )+ RPAREN
    )? (USING (workload_group_pool_name = id_ | DEFAULT_DOUBLE_QUOTE))?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-workload-group-transact-sql
create_workload_group
    : CREATE WORKLOAD GROUP workload_group_group_name = id_ (
        WITH LPAREN (
            IMPORTANCE EQ (LOW | MEDIUM | HIGH)
            | COMMA? REQUEST_MAX_MEMORY_GRANT_PERCENT EQ request_max_memory_grant = INT
            | COMMA? REQUEST_MAX_CPU_TIME_SEC EQ request_max_cpu_time_sec = INT
            | REQUEST_MEMORY_GRANT_TIMEOUT_SEC EQ request_memory_grant_timeout_sec = INT
            | MAX_DOP EQ max_dop = INT
            | GROUP_MAX_REQUESTS EQ group_max_requests = INT
        )+ RPAREN
    )? (
        USING (workload_group_pool_name = id_ | DEFAULT_DOUBLE_QUOTE)? (
            COMMA? EXTERNAL external_pool_name = id_
            | DEFAULT_DOUBLE_QUOTE
        )?
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-xml-schema-collection-transact-sql
create_xml_schema_collection
    : CREATE XML SCHEMA COLLECTION (relational_schema = id_ DOT)? sql_identifier = id_ AS (
        STRING
        | id_
        | LOCAL_ID
    )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-partition-function-transact-sql?view=sql-server-ver15
create_partition_function
    : CREATE PARTITION FUNCTION partition_function_name = id_ LPAREN input_parameter_type = data_type RPAREN AS RANGE (
        LEFT
        | RIGHT
    )? FOR VALUES LPAREN boundary_values = expression_list_ RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-partition-scheme-transact-sql?view=sql-server-ver15
create_partition_scheme
    : CREATE PARTITION SCHEME partition_scheme_name = id_ AS PARTITION partition_function_name = id_ ALL? TO LPAREN file_group_names += id_ (
        COMMA file_group_names += id_
    )* RPAREN
    ;

create_queue
    : CREATE QUEUE (full_table_name | queue_name = id_) queue_settings? (
        ON filegroup = id_
        | DEFAULT
    )?
    ;

queue_settings
    : WITH (STATUS EQ on_off COMMA?)? (RETENTION EQ on_off COMMA?)? (
        ACTIVATION LPAREN (
            (
                (STATUS EQ on_off COMMA?)? (
                    PROCEDURE_NAME EQ func_proc_name_database_schema COMMA?
                )? (MAX_QUEUE_READERS EQ max_readers = INT COMMA?)? (
                    EXECUTE AS (SELF | user_name = STRING | OWNER) COMMA?
                )?
            )
            | DROP
        ) RPAREN COMMA?
    )? (POISON_MESSAGE_HANDLING LPAREN (STATUS EQ on_off) RPAREN)?
    ;

alter_queue
    : ALTER QUEUE (full_table_name | queue_name = id_) (queue_settings | queue_action)
    ;

queue_action
    : REBUILD (WITH LPAREN queue_rebuild_options RPAREN)?
    | REORGANIZE (WITH LOB_COMPACTION EQ on_off)?
    | MOVE TO (id_ | DEFAULT)
    ;

queue_rebuild_options
    : MAXDOP EQ INT
    ;

create_contract
    : CREATE CONTRACT contract_name (AUTHORIZATION owner_name = id_)? LPAREN (
        (message_type_name = id_ | DEFAULT) SENT BY (INITIATOR | TARGET | ANY) COMMA?
    )+ RPAREN
    ;

conversation_statement
    : begin_conversation_timer
    | begin_conversation_dialog
    | end_conversation
    | get_conversation
    | send_conversation
    | waitfor_conversation
    ;

message_statement
    : CREATE MESSAGE TYPE message_type_name = id_ (AUTHORIZATION owner_name = id_)? (
        VALIDATION EQ (
            NONE
            | EMPTY
            | WELL_FORMED_XML
            | VALID_XML WITH SCHEMA COLLECTION schema_collection_name = id_
        )
    )
    ;

// DML

// https://docs.microsoft.com/en-us/sql/t-sql/statements/merge-transact-sql
// note that there's a limit on number of when_matches but it has to be done runtime due to different ordering of statements allowed
merge_statement
    : with_expression? MERGE (TOP LPAREN expression RPAREN PERCENT?)? INTO? ddl_object with_table_hints? as_table_alias? USING table_sources ON
        search_condition when_matches+ output_clause? option_clause? SEMI
    ;

when_matches
    : (WHEN MATCHED (AND search_condition)? THEN merge_matched)+
    | (WHEN NOT MATCHED (BY TARGET)? (AND search_condition)? THEN merge_not_matched)
    | (WHEN NOT MATCHED BY SOURCE (AND search_condition)? THEN merge_matched)+
    ;

merge_matched
    : UPDATE SET update_elem_merge (COMMA update_elem_merge)*
    | DELETE
    ;

merge_not_matched
    : INSERT (LPAREN column_name_list RPAREN)? (table_value_constructor | DEFAULT VALUES)
    ;

// https://msdn.microsoft.com/en-us/library/ms189835.aspx
delete_statement
    : with_expression? DELETE (TOP LPAREN expression RPAREN PERCENT? | TOP INT)? FROM? delete_statement_from with_table_hints? output_clause? (
        FROM table_sources
    )? (WHERE (search_condition | CURRENT OF (GLOBAL? cursor_name | cursor_var = LOCAL_ID)))? for_clause? option_clause? SEMI?
    ;

delete_statement_from
    : ddl_object
    | rowset_function_limited
    | table_var = LOCAL_ID
    ;

// https://msdn.microsoft.com/en-us/library/ms174335.aspx
insert_statement
    : with_expression? INSERT (TOP LPAREN expression RPAREN PERCENT?)? INTO? (
        ddl_object
        | rowset_function_limited
    ) with_table_hints? (LPAREN insert_column_name_list RPAREN)? output_clause? insert_statement_value for_clause? option_clause? SEMI?
    ;

insert_statement_value
    : table_value_constructor
    | derived_table
    | execute_statement
    | DEFAULT VALUES
    ;

receive_statement
    : LPAREN? RECEIVE (ALL | DISTINCT | top_clause | STAR) (LOCAL_ID EQ expression COMMA?)* FROM full_table_name (
        INTO table_variable = id_ (WHERE where = search_condition)
    )? RPAREN?
    ;

// https://msdn.microsoft.com/en-us/library/ms189499.aspx
select_statement_standalone
    : with_expression? select_statement
    ;

select_statement
    : query_expression select_order_by_clause? for_clause? option_clause? SEMI?
    ;

time
    : (LOCAL_ID | constant)
    ;

// https://msdn.microsoft.com/en-us/library/ms177523.aspx
update_statement
    : with_expression? UPDATE (TOP LPAREN expression RPAREN PERCENT?)? (
        ddl_object
        | rowset_function_limited
    ) with_table_hints? SET update_elem (COMMA update_elem)* output_clause? (FROM table_sources)? (
        WHERE (search_condition | CURRENT OF (GLOBAL? cursor_name | cursor_var = LOCAL_ID))
    )? for_clause? option_clause? SEMI?
    ;

// https://msdn.microsoft.com/en-us/library/ms177564.aspx
output_clause
    : OUTPUT output_dml_list_elem (COMMA output_dml_list_elem)* (
        INTO (LOCAL_ID | table_name) (LPAREN column_name_list RPAREN)?
    )?
    ;

output_dml_list_elem
    : (expression | asterisk) as_column_alias?
    ;

// DDL

// https://msdn.microsoft.com/en-ie/library/ms176061.aspx
create_database
    : CREATE DATABASE (database = id_) (CONTAINMENT EQ ( NONE | PARTIAL))? (
        ON PRIMARY? database_file_spec ( COMMA database_file_spec)*
    )? (LOG ON database_file_spec ( COMMA database_file_spec)*)? (COLLATE collation_name = id_)? (
        WITH create_database_option ( COMMA create_database_option)*
    )?
    ;

// https://msdn.microsoft.com/en-us/library/ms188783.aspx
create_index
    : CREATE UNIQUE? clustered? INDEX id_ ON table_name LPAREN column_name_list_with_order RPAREN (
        INCLUDE LPAREN column_name_list RPAREN
    )? (WHERE where = search_condition)? (create_index_options)? (ON id_)? SEMI?
    ;

create_index_options
    : WITH LPAREN relational_index_option (COMMA relational_index_option)* RPAREN
    ;

relational_index_option
    : rebuild_index_option
    | DROP_EXISTING EQ on_off
    | OPTIMIZE_FOR_SEQUENTIAL_KEY EQ on_off
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-index-transact-sql
alter_index
    : ALTER INDEX (id_ | ALL) ON table_name (
        DISABLE
        | PAUSE
        | ABORT
        | RESUME resumable_index_options?
        | reorganize_partition
        | set_index_options
        | rebuild_partition
    )
    ;

resumable_index_options
    : WITH LPAREN (resumable_index_option (COMMA resumable_index_option)*) RPAREN
    ;

resumable_index_option
    : MAXDOP EQ max_degree_of_parallelism = INT
    | MAX_DURATION EQ max_duration = INT MINUTES?
    | low_priority_lock_wait
    ;

reorganize_partition
    : REORGANIZE (PARTITION EQ INT)? reorganize_options?
    ;

reorganize_options
    : WITH LPAREN (reorganize_option (COMMA reorganize_option)*) RPAREN
    ;

reorganize_option
    : LOB_COMPACTION EQ on_off
    | COMPRESS_ALL_ROW_GROUPS EQ on_off
    ;

set_index_options
    : SET LPAREN set_index_option (COMMA set_index_option)* RPAREN
    ;

set_index_option
    : ALLOW_ROW_LOCKS EQ on_off
    | ALLOW_PAGE_LOCKS EQ on_off
    | OPTIMIZE_FOR_SEQUENTIAL_KEY EQ on_off
    | IGNORE_DUP_KEY EQ on_off
    | STATISTICS_NORECOMPUTE EQ on_off
    | COMPRESSION_DELAY EQ delay = INT MINUTES?
    ;

rebuild_partition
    : REBUILD (PARTITION EQ ALL)? rebuild_index_options?
    | REBUILD PARTITION EQ INT single_partition_rebuild_index_options?
    ;

rebuild_index_options
    : WITH LPAREN rebuild_index_option (COMMA rebuild_index_option)* RPAREN
    ;

rebuild_index_option
    : PAD_INDEX EQ on_off
    | FILLFACTOR EQ INT
    | SORT_IN_TEMPDB EQ on_off
    | IGNORE_DUP_KEY EQ on_off
    | STATISTICS_NORECOMPUTE EQ on_off
    | STATISTICS_INCREMENTAL EQ on_off
    | ONLINE EQ (ON (LPAREN low_priority_lock_wait RPAREN)? | OFF)
    | RESUMABLE EQ on_off
    | MAX_DURATION EQ times = INT MINUTES?
    | ALLOW_ROW_LOCKS EQ on_off
    | ALLOW_PAGE_LOCKS EQ on_off
    | MAXDOP EQ max_degree_of_parallelism = INT
    | DATA_COMPRESSION EQ (NONE | ROW | PAGE | COLUMNSTORE | COLUMNSTORE_ARCHIVE) on_partitions?
    | XML_COMPRESSION EQ on_off on_partitions?
    ;

single_partition_rebuild_index_options
    : WITH LPAREN single_partition_rebuild_index_option (COMMA single_partition_rebuild_index_option)* RPAREN
    ;

single_partition_rebuild_index_option
    : SORT_IN_TEMPDB EQ on_off
    | MAXDOP EQ max_degree_of_parallelism = INT
    | RESUMABLE EQ on_off
    | DATA_COMPRESSION EQ (NONE | ROW | PAGE | COLUMNSTORE | COLUMNSTORE_ARCHIVE) on_partitions?
    | XML_COMPRESSION EQ on_off on_partitions?
    | ONLINE EQ (ON (LPAREN low_priority_lock_wait RPAREN)? | OFF)
    ;

on_partitions
    : ON PARTITIONS LPAREN partition_number = INT (TO to_partition_number = INT)? (
        COMMA partition_number = INT (TO to_partition_number = INT)?
    )* RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-columnstore-index-transact-sql?view=sql-server-ver15
create_columnstore_index
    : CREATE CLUSTERED COLUMNSTORE INDEX id_ ON table_name create_columnstore_index_options? (
        ON id_
    )? SEMI?
    ;

create_columnstore_index_options
    : WITH LPAREN columnstore_index_option (COMMA columnstore_index_option)* RPAREN
    ;

columnstore_index_option
    : DROP_EXISTING EQ on_off
    | MAXDOP EQ max_degree_of_parallelism = INT
    | ONLINE EQ on_off
    | COMPRESSION_DELAY EQ delay = INT MINUTES?
    | DATA_COMPRESSION EQ (COLUMNSTORE | COLUMNSTORE_ARCHIVE) on_partitions?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-columnstore-index-transact-sql?view=sql-server-ver15
create_nonclustered_columnstore_index
    : CREATE NONCLUSTERED? COLUMNSTORE INDEX id_ ON table_name LPAREN column_name_list_with_order RPAREN (
        WHERE search_condition
    )? create_columnstore_index_options? (ON id_)? SEMI?
    ;

create_xml_index
    : CREATE PRIMARY? XML INDEX id_ ON table_name LPAREN id_ RPAREN (
        USING XML INDEX id_ (FOR (VALUE | PATH | PROPERTY)?)?
    )? xml_index_options? SEMI?
    ;

xml_index_options
    : WITH LPAREN xml_index_option (COMMA xml_index_option)* RPAREN
    ;

xml_index_option
    : PAD_INDEX EQ on_off
    | FILLFACTOR EQ INT
    | SORT_IN_TEMPDB EQ on_off
    | IGNORE_DUP_KEY EQ on_off
    | DROP_EXISTING EQ on_off
    | ONLINE EQ (ON (LPAREN low_priority_lock_wait RPAREN)? | OFF)
    | ALLOW_ROW_LOCKS EQ on_off
    | ALLOW_PAGE_LOCKS EQ on_off
    | MAXDOP EQ max_degree_of_parallelism = INT
    | XML_COMPRESSION EQ on_off
    ;

// https://msdn.microsoft.com/en-us/library/ms187926(v=sql.120).aspx
create_or_alter_procedure
    : ((CREATE (OR (ALTER | REPLACE))?) | ALTER) proc = (PROC | PROCEDURE) procName = func_proc_name_schema (
        SEMI INT
    )? (LPAREN? procedure_param (COMMA procedure_param)* RPAREN?)? (
        WITH procedure_option (COMMA procedure_option)*
    )? (FOR REPLICATION)? AS (as_external_name | sql_clauses*)
    ;

as_external_name
    : EXTERNAL NAME assembly_name = id_ DOT class_name = id_ DOT method_name = id_
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/create-trigger-transact-sql
create_or_alter_trigger
    : create_or_alter_dml_trigger
    | create_or_alter_ddl_trigger
    ;

create_or_alter_dml_trigger
    : (CREATE (OR (ALTER | REPLACE))? | ALTER) TRIGGER simple_name ON table_name (
        WITH dml_trigger_option (COMMA dml_trigger_option)*
    )? (FOR | AFTER | INSTEAD OF) dml_trigger_operation (COMMA dml_trigger_operation)* (WITH APPEND)? (
        NOT FOR REPLICATION
    )? AS sql_clauses+
    ;

dml_trigger_option
    : ENCRYPTION
    | execute_clause
    ;

dml_trigger_operation
    : (INSERT | UPDATE | DELETE)
    ;

create_or_alter_ddl_trigger
    : (CREATE (OR (ALTER | REPLACE))? | ALTER) TRIGGER simple_name ON (ALL SERVER | DATABASE) (
        WITH dml_trigger_option (COMMA dml_trigger_option)*
    )? (FOR | AFTER) ddl_trigger_operation (COMMA ddl_trigger_operation)* AS sql_clauses+
    ;

ddl_trigger_operation
    : simple_id
    ;

// https://msdn.microsoft.com/en-us/library/ms186755.aspx
create_or_alter_function
    : ((CREATE (OR ALTER)?) | ALTER) FUNCTION funcName = func_proc_name_schema (
        (LPAREN procedure_param (COMMA procedure_param)* RPAREN)
        | LPAREN RPAREN
    ) //must have (), but can be empty
    (func_body_returns_select | func_body_returns_table | func_body_returns_scalar) SEMI?
    ;

func_body_returns_select
    : RETURNS TABLE (WITH function_option (COMMA function_option)*)? AS? (
        as_external_name
        | RETURN (LPAREN select_statement_standalone RPAREN | select_statement_standalone)
    )
    ;

func_body_returns_table
    : RETURNS LOCAL_ID table_type_definition (WITH function_option (COMMA function_option)*)? AS? (
        as_external_name
        | BEGIN sql_clauses* RETURN SEMI? END SEMI?
    )
    ;

func_body_returns_scalar
    : RETURNS data_type (WITH function_option (COMMA function_option)*)? AS? (
        as_external_name
        | BEGIN sql_clauses* RETURN ret = expression SEMI? END
    )
    ;

procedure_param_default_value
    : NULL_
    | DEFAULT
    | constant
    | LOCAL_ID
    ;

procedure_param
    : LOCAL_ID AS? (type_schema = id_ DOT)? data_type VARYING? (
        EQ default_val = procedure_param_default_value
    )? (OUT | OUTPUT | READONLY)?
    ;

procedure_option
    : ENCRYPTION
    | RECOMPILE
    | execute_clause
    ;

function_option
    : ENCRYPTION
    | SCHEMABINDING
    | RETURNS NULL_ ON NULL_ INPUT
    | CALLED ON NULL_ INPUT
    | execute_clause
    ;

// https://msdn.microsoft.com/en-us/library/ms188038.aspx
create_statistics
    : CREATE STATISTICS id_ ON table_name LPAREN column_name_list RPAREN (
        WITH (FULLSCAN | SAMPLE INT (PERCENT | ROWS) | STATS_STREAM) (COMMA NORECOMPUTE)? (
            COMMA INCREMENTAL EQ on_off
        )?
    )? SEMI?
    ;

update_statistics
    : UPDATE STATISTICS full_table_name (id_ | LPAREN id_ ( COMMA id_)* RPAREN)? update_statistics_options?
    ;

update_statistics_options
    : WITH update_statistics_option (COMMA update_statistics_option)*
    ;

update_statistics_option
    : (FULLSCAN (COMMA? PERSIST_SAMPLE_PERCENT EQ on_off)?)
    | (SAMPLE number = INT (PERCENT | ROWS) (COMMA? PERSIST_SAMPLE_PERCENT EQ on_off)?)
    | RESAMPLE on_partitions?
    | STATS_STREAM EQ stats_stream_ = expression
    | ROWCOUNT EQ INT
    | PAGECOUNT EQ INT
    | ALL
    | COLUMNS
    | INDEX
    | NORECOMPUTE
    | INCREMENTAL EQ on_off
    | MAXDOP EQ max_dregree_of_parallelism = INT
    | AUTO_DROP EQ on_off
    ;

// https://msdn.microsoft.com/en-us/library/ms174979.aspx
create_table
    : CREATE TABLE table_name LPAREN column_def_table_constraints (COMMA? table_indices)* COMMA? RPAREN (
        LOCK simple_id
    )? table_options* (ON id_ | DEFAULT | on_partition_or_filegroup)? (TEXTIMAGE_ON id_ | DEFAULT)? SEMI?
    ;

table_indices
    : INDEX id_ UNIQUE? clustered? LPAREN column_name_list_with_order RPAREN
    | INDEX id_ CLUSTERED COLUMNSTORE
    | INDEX id_ NONCLUSTERED? COLUMNSTORE LPAREN column_name_list RPAREN create_table_index_options? (
        ON id_
    )?
    ;

table_options
    : WITH (LPAREN table_option (COMMA table_option)* RPAREN | table_option (COMMA table_option)*)
    ;

table_option
    : (simple_id | keyword) EQ (simple_id | keyword | on_off | INT)
    | CLUSTERED COLUMNSTORE INDEX
    | HEAP
    | FILLFACTOR EQ INT
    | DISTRIBUTION EQ HASH LPAREN id_ RPAREN
    | CLUSTERED INDEX LPAREN id_ (ASC | DESC)? (COMMA id_ (ASC | DESC)?)* RPAREN
    | DATA_COMPRESSION EQ (NONE | ROW | PAGE) on_partitions?
    | XML_COMPRESSION EQ on_off on_partitions?
    ;

create_table_index_options
    : WITH LPAREN create_table_index_option (COMMA create_table_index_option)* RPAREN
    ;

create_table_index_option
    : PAD_INDEX EQ on_off
    | FILLFACTOR EQ INT
    | IGNORE_DUP_KEY EQ on_off
    | STATISTICS_NORECOMPUTE EQ on_off
    | STATISTICS_INCREMENTAL EQ on_off
    | ALLOW_ROW_LOCKS EQ on_off
    | ALLOW_PAGE_LOCKS EQ on_off
    | OPTIMIZE_FOR_SEQUENTIAL_KEY EQ on_off
    | DATA_COMPRESSION EQ (NONE | ROW | PAGE | COLUMNSTORE | COLUMNSTORE_ARCHIVE) on_partitions?
    | XML_COMPRESSION EQ on_off on_partitions?
    ;

// https://msdn.microsoft.com/en-us/library/ms187956.aspx
create_view
    : (CREATE (OR (ALTER | REPLACE))? | ALTER) VIEW simple_name (LPAREN column_name_list RPAREN)? (
        WITH view_attribute (COMMA view_attribute)*
    )? AS select_statement_standalone (WITH CHECK OPTION)? SEMI?
    ;

view_attribute
    : ENCRYPTION
    | SCHEMABINDING
    | VIEW_METADATA
    ;

// https://msdn.microsoft.com/en-us/library/ms190273.aspx
alter_table
    : ALTER TABLE table_name (
        SET LPAREN LOCK_ESCALATION EQ (AUTO | TABLE | DISABLE) RPAREN
        | ADD column_def_table_constraints
        | ALTER COLUMN (column_definition | column_modifier)
        | DROP COLUMN id_ (COMMA id_)*
        | DROP CONSTRAINT constraint = id_
        | WITH (CHECK | NOCHECK) ADD (CONSTRAINT constraint = id_)? (
            FOREIGN KEY LPAREN fk = column_name_list RPAREN REFERENCES table_name (
                LPAREN pk = column_name_list RPAREN
            )? (on_delete | on_update)*
            | CHECK LPAREN search_condition RPAREN
        )
        | (NOCHECK | CHECK) CONSTRAINT constraint = id_
        | (ENABLE | DISABLE) TRIGGER id_?
        | REBUILD table_options
        | SWITCH switch_partition
    ) SEMI?
    ;

switch_partition
    : (PARTITION? source_partition_number_expression = expression)? TO target_table = table_name (
        PARTITION target_partition_number_expression = expression
    )? (WITH low_priority_lock_wait)?
    ;

low_priority_lock_wait
    : WAIT_AT_LOW_PRIORITY LPAREN MAX_DURATION EQ max_duration = time MINUTES? COMMA ABORT_AFTER_WAIT EQ abort_after_wait = (
        NONE
        | SELF
        | BLOCKERS
    ) RPAREN
    ;

// https://msdn.microsoft.com/en-us/library/ms174269.aspx
alter_database
    : ALTER DATABASE (database = id_ | CURRENT) (
        MODIFY NAME EQ new_name = id_
        | COLLATE collation = id_
        | SET database_optionspec (WITH termination)?
        | add_or_modify_files
        | add_or_modify_filegroups
    ) SEMI?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-database-transact-sql-file-and-filegroup-options?view=sql-server-ver15
add_or_modify_files
    : ADD FILE filespec (COMMA filespec)* (TO FILEGROUP filegroup_name = id_)?
    | ADD LOG FILE filespec (COMMA filespec)*
    | REMOVE FILE logical_file_name = id_
    | MODIFY FILE filespec
    ;

filespec
    : LPAREN NAME EQ name = id_or_string (COMMA NEWNAME EQ new_name = id_or_string)? (
        COMMA FILENAME EQ file_name = STRING
    )? (COMMA SIZE EQ size = file_size)? (COMMA MAXSIZE EQ (max_size = file_size) | UNLIMITED)? (
        COMMA FILEGROWTH EQ growth_increment = file_size
    )? (COMMA OFFLINE)? RPAREN
    ;

add_or_modify_filegroups
    : ADD FILEGROUP filegroup_name = id_ (CONTAINS FILESTREAM | CONTAINS MEMORY_OPTIMIZED_DATA)?
    | REMOVE FILEGROUP filegrou_name = id_
    | MODIFY FILEGROUP filegrou_name = id_ (
        filegroup_updatability_option
        | DEFAULT
        | NAME EQ new_filegroup_name = id_
        | AUTOGROW_SINGLE_FILE
        | AUTOGROW_ALL_FILES
    )
    ;

filegroup_updatability_option
    : READONLY
    | READWRITE
    | READ_ONLY
    | READ_WRITE
    ;

// https://msdn.microsoft.com/en-us/library/bb522682.aspx
// Runtime check.
database_optionspec
    : auto_option
    | change_tracking_option
    | containment_option
    | cursor_option
    | database_mirroring_option
    | date_correlation_optimization_option
    | db_encryption_option
    | db_state_option
    | db_update_option
    | db_user_access_option
    | delayed_durability_option
    | external_access_option
    | FILESTREAM database_filestream_option
    | hadr_options
    | mixed_page_allocation_option
    | parameterization_option
    //  | query_store_options
    | recovery_option
    //  | remote_data_archive_option
    | service_broker_option
    | snapshot_option
    | sql_option
    | target_recovery_time_option
    | termination
    ;

auto_option
    : AUTO_CLOSE on_off
    | AUTO_CREATE_STATISTICS OFF
    | ON ( INCREMENTAL EQ ON | OFF)
    | AUTO_SHRINK on_off
    | AUTO_UPDATE_STATISTICS on_off
    | AUTO_UPDATE_STATISTICS_ASYNC (ON | OFF)
    ;

change_tracking_option
    : CHANGE_TRACKING EQ (
        OFF
        | ON LPAREN (change_tracking_option_list (COMMA change_tracking_option_list)*)* RPAREN
    )
    ;

change_tracking_option_list
    : AUTO_CLEANUP EQ on_off
    | CHANGE_RETENTION EQ INT ( DAYS | HOURS | MINUTES)
    ;

containment_option
    : CONTAINMENT EQ (NONE | PARTIAL)
    ;

cursor_option
    : CURSOR_CLOSE_ON_COMMIT on_off
    | CURSOR_DEFAULT ( LOCAL | GLOBAL)
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/alter-endpoint-transact-sql
alter_endpoint
    : ALTER ENDPOINT endpointname = id_ (AUTHORIZATION login = id_)? (
        STATE EQ state = (STARTED | STOPPED | DISABLED)
    )? AS TCP LPAREN endpoint_listener_clause RPAREN (
        FOR TSQL LPAREN RPAREN
        | FOR SERVICE_BROKER LPAREN endpoint_authentication_clause (
            COMMA? endpoint_encryption_alogorithm_clause
        )? (COMMA? MESSAGE_FORWARDING EQ (ENABLED | DISABLED))? (
            COMMA? MESSAGE_FORWARD_SIZE EQ INT
        )? RPAREN
        | FOR DATABASE_MIRRORING LPAREN endpoint_authentication_clause (
            COMMA? endpoint_encryption_alogorithm_clause
        )? COMMA? ROLE EQ (WITNESS | PARTNER | ALL) RPAREN
    )
    ;

/* Will visit later
*/
database_mirroring_option
    : mirroring_set_option
    ;

mirroring_set_option
    : mirroring_partner partner_option
    | mirroring_witness witness_option
    ;

mirroring_partner
    : PARTNER
    ;

mirroring_witness
    : WITNESS
    ;

witness_partner_equal
    : EQ
    ;

partner_option
    : witness_partner_equal partner_server
    | FAILOVER
    | FORCE_SERVICE_ALLOW_DATA_LOSS
    | OFF
    | RESUME
    | SAFETY (FULL | OFF)
    | SUSPEND
    | TIMEOUT INT
    ;

witness_option
    : witness_partner_equal witness_server
    | OFF
    ;

witness_server
    : partner_server
    ;

partner_server
    : partner_server_tcp_prefix host mirroring_host_port_seperator port_number
    ;

mirroring_host_port_seperator
    : COLON
    ;

partner_server_tcp_prefix
    : TCP COLON DOUBLE_FORWARD_SLASH
    ;

port_number
    : port = INT
    ;

host
    : id_ DOT host
    | (id_ DOT | id_)
    ;

date_correlation_optimization_option
    : DATE_CORRELATION_OPTIMIZATION on_off
    ;

db_encryption_option
    : ENCRYPTION on_off
    ;

db_state_option
    : (ONLINE | OFFLINE | EMERGENCY)
    ;

db_update_option
    : READ_ONLY
    | READ_WRITE
    ;

db_user_access_option
    : SINGLE_USER
    | RESTRICTED_USER
    | MULTI_USER
    ;

delayed_durability_option
    : DELAYED_DURABILITY EQ (DISABLED | ALLOWED | FORCED)
    ;

external_access_option
    : DB_CHAINING on_off
    | TRUSTWORTHY on_off
    | DEFAULT_LANGUAGE EQ ( id_ | STRING)
    | DEFAULT_FULLTEXT_LANGUAGE EQ ( id_ | STRING)
    | NESTED_TRIGGERS EQ ( OFF | ON)
    | TRANSFORM_NOISE_WORDS EQ ( OFF | ON)
    | TWO_DIGIT_YEAR_CUTOFF EQ INT
    ;

hadr_options
    : HADR (( AVAILABILITY GROUP EQ availability_group_name = id_ | OFF) | (SUSPEND | RESUME))
    ;

mixed_page_allocation_option
    : MIXED_PAGE_ALLOCATION (OFF | ON)
    ;

parameterization_option
    : PARAMETERIZATION (SIMPLE | FORCED)
    ;

recovery_option
    : RECOVERY (FULL | BULK_LOGGED | SIMPLE)
    | TORN_PAGE_DETECTION on_off
    | ACCELERATED_DATABASE_RECOVERY EQ on_off
    | PAGE_VERIFY ( CHECKSUM | TORN_PAGE_DETECTION | NONE)
    ;

service_broker_option
    : ENABLE_BROKER
    | DISABLE_BROKER
    | NEW_BROKER
    | ERROR_BROKER_CONVERSATIONS
    | HONOR_BROKER_PRIORITY on_off
    ;

snapshot_option
    : ALLOW_SNAPSHOT_ISOLATION on_off
    | READ_COMMITTED_SNAPSHOT (ON | OFF)
    | MEMORY_OPTIMIZED_ELEVATE_TO_SNAPSHOT = (ON | OFF)
    ;

sql_option
    : ANSI_NULL_DEFAULT on_off
    | ANSI_NULLS on_off
    | ANSI_PADDING on_off
    | ANSI_WARNINGS on_off
    | ARITHABORT on_off
    | COMPATIBILITY_LEVEL EQ INT
    | CONCAT_NULL_YIELDS_NULL on_off
    | NUMERIC_ROUNDABORT on_off
    | QUOTED_IDENTIFIER on_off
    | RECURSIVE_TRIGGERS on_off
    ;

target_recovery_time_option
    : TARGET_RECOVERY_TIME EQ INT (SECONDS | MINUTES)
    ;

termination
    : ROLLBACK AFTER seconds = INT
    | ROLLBACK IMMEDIATE
    | NO_WAIT
    ;

// https://msdn.microsoft.com/en-us/library/ms176118.aspx
drop_index
    : DROP INDEX (IF EXISTS)? (
        drop_relational_or_xml_or_spatial_index (COMMA drop_relational_or_xml_or_spatial_index)*
        | drop_backward_compatible_index (COMMA drop_backward_compatible_index)*
    ) SEMI?
    ;

drop_relational_or_xml_or_spatial_index
    : index_name = id_ ON full_table_name
    ;

drop_backward_compatible_index
    : (owner_name = id_ DOT)? table_or_view_name = id_ DOT index_name = id_
    ;

// https://msdn.microsoft.com/en-us/library/ms174969.aspx
drop_procedure
    : DROP proc = (PROC | PROCEDURE) (IF EXISTS)? func_proc_name_schema (COMMA func_proc_name_schema)* SEMI?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-trigger-transact-sql
drop_trigger
    : drop_dml_trigger
    | drop_ddl_trigger
    ;

drop_dml_trigger
    : DROP TRIGGER (IF EXISTS)? simple_name (COMMA simple_name)* SEMI?
    ;

drop_ddl_trigger
    : DROP TRIGGER (IF EXISTS)? simple_name (COMMA simple_name)* ON (DATABASE | ALL SERVER) SEMI?
    ;

// https://msdn.microsoft.com/en-us/library/ms190290.aspx
drop_function
    : DROP FUNCTION (IF EXISTS)? func_proc_name_schema (COMMA func_proc_name_schema)* SEMI?
    ;

// https://msdn.microsoft.com/en-us/library/ms175075.aspx
drop_statistics
    : DROP STATISTICS (COMMA? (table_name DOT)? name = id_)+ SEMI
    ;

// https://msdn.microsoft.com/en-us/library/ms173790.aspx
drop_table
    : DROP TABLE (IF EXISTS)? table_name (COMMA table_name)* SEMI?
    ;

// https://msdn.microsoft.com/en-us/library/ms173492.aspx
drop_view
    : DROP VIEW (IF EXISTS)? simple_name (COMMA simple_name)* SEMI?
    ;

create_type
    : CREATE TYPE name = simple_name (FROM data_type null_notnull?)? (
        AS TABLE LPAREN column_def_table_constraints RPAREN
    )?
    ;

drop_type
    : DROP TYPE (IF EXISTS)? name = simple_name
    ;

rowset_function_limited
    : openquery
    | opendatasource
    ;

// https://msdn.microsoft.com/en-us/library/ms188427(v=sql.120).aspx
openquery
    : OPENQUERY LPAREN linked_server = id_ COMMA query = STRING RPAREN
    ;

// https://msdn.microsoft.com/en-us/library/ms179856.aspx
opendatasource
    : OPENDATASOURCE LPAREN provider = STRING COMMA init = STRING RPAREN DOT (database = id_)? DOT (
        scheme = id_
    )? DOT (table = id_)
    ;

// Other statements.

// https://msdn.microsoft.com/en-us/library/ms188927.aspx
declare_statement
    : DECLARE LOCAL_ID AS? (data_type | table_type_definition | table_name)
    | DECLARE loc += declare_local (COMMA loc += declare_local)*
    | DECLARE LOCAL_ID AS? xml_type_definition
    | WITH XMLNAMESPACES LPAREN xml_dec += xml_declaration (COMMA xml_dec += xml_declaration)* RPAREN
    ;

xml_declaration
    : xml_namespace_uri = STRING AS id_
    | DEFAULT STRING
    ;

// https://msdn.microsoft.com/en-us/library/ms181441(v=sql.120).aspx
cursor_statement
    // https://msdn.microsoft.com/en-us/library/ms175035(v=sql.120).aspx
    : CLOSE GLOBAL? cursor_name SEMI?
    // https://msdn.microsoft.com/en-us/library/ms188782(v=sql.120).aspx
    | DEALLOCATE GLOBAL? CURSOR? cursor_name SEMI?
    // https://msdn.microsoft.com/en-us/library/ms180169(v=sql.120).aspx
    | declare_cursor
    // https://msdn.microsoft.com/en-us/library/ms180152(v=sql.120).aspx
    | fetch_cursor
    // https://msdn.microsoft.com/en-us/library/ms190500(v=sql.120).aspx
    | OPEN GLOBAL? cursor_name SEMI?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/backup-transact-sql
backup_database
    : BACKUP DATABASE (database_name = id_) (
        READ_WRITE_FILEGROUPS (COMMA? (FILE | FILEGROUP) EQ file_or_filegroup = STRING)*
    )? (COMMA? (FILE | FILEGROUP) EQ file_or_filegroup = STRING)* (
        TO ( COMMA? logical_device_name = id_)+
        | TO ( COMMA? (DISK | TAPE | URL) EQ (STRING | id_))+
    ) (
        (MIRROR TO ( COMMA? logical_device_name = id_)+)+
        | ( MIRROR TO ( COMMA? (DISK | TAPE | URL) EQ (STRING | id_))+)+
    )? (
        WITH (
            COMMA? DIFFERENTIAL
            | COMMA? COPY_ONLY
            | COMMA? (COMPRESSION | NO_COMPRESSION)
            | COMMA? DESCRIPTION EQ (STRING | id_)
            | COMMA? NAME EQ backup_set_name = id_
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
            | COMMA? STATS (EQ stats_percent = INT)?
            | COMMA? (REWIND | NOREWIND)
            | COMMA? (LOAD | NOUNLOAD)
            | COMMA? ENCRYPTION LPAREN ALGORITHM EQ (
                AES_128
                | AES_192
                | AES_256
                | TRIPLE_DES_3KEY
            ) COMMA SERVER CERTIFICATE EQ (
                encryptor_name = id_
                | SERVER ASYMMETRIC KEY EQ encryptor_name = id_
            )
        )*
    )?
    ;

backup_log
    : BACKUP LOG (database_name = id_) (
        TO ( COMMA? logical_device_name = id_)+
        | TO ( COMMA? (DISK | TAPE | URL) EQ (STRING | id_))+
    ) (
        (MIRROR TO ( COMMA? logical_device_name = id_)+)+
        | ( MIRROR TO ( COMMA? (DISK | TAPE | URL) EQ (STRING | id_))+)+
    )? (
        WITH (
            COMMA? DIFFERENTIAL
            | COMMA? COPY_ONLY
            | COMMA? (COMPRESSION | NO_COMPRESSION)
            | COMMA? DESCRIPTION EQ (STRING | id_)
            | COMMA? NAME EQ backup_set_name = id_
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
            | COMMA? STATS (EQ stats_percent = INT)?
            | COMMA? (REWIND | NOREWIND)
            | COMMA? (LOAD | NOUNLOAD)
            | COMMA? (NORECOVERY | STANDBY EQ undo_file_name = STRING)
            | COMMA? NO_TRUNCATE
            | COMMA? ENCRYPTION LPAREN ALGORITHM EQ (
                AES_128
                | AES_192
                | AES_256
                | TRIPLE_DES_3KEY
            ) COMMA SERVER CERTIFICATE EQ (
                encryptor_name = id_
                | SERVER ASYMMETRIC KEY EQ encryptor_name = id_
            )
        )*
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/backup-certificate-transact-sql
backup_certificate
    : BACKUP CERTIFICATE certname = id_ TO FILE EQ cert_file = STRING (
        WITH PRIVATE KEY LPAREN (
            COMMA? FILE EQ private_key_file = STRING
            | COMMA? ENCRYPTION BY PASSWORD EQ encryption_password = STRING
            | COMMA? DECRYPTION BY PASSWORD EQ decryption_pasword = STRING
        )+ RPAREN
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/backup-master-key-transact-sql
backup_master_key
    : BACKUP MASTER KEY TO FILE EQ master_key_backup_file = STRING ENCRYPTION BY PASSWORD EQ encryption_password = STRING
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/statements/backup-service-master-key-transact-sql
backup_service_master_key
    : BACKUP SERVICE MASTER KEY TO FILE EQ service_master_key_backup_file = STRING ENCRYPTION BY PASSWORD EQ encryption_password = STRING
    ;

kill_statement
    : KILL (kill_process | kill_query_notification | kill_stats_job)
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/kill-transact-sql
kill_process
    : (session_id = (INT | STRING) | UOW) (WITH STATUSONLY)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/kill-query-notification-subscription-transact-sql
kill_query_notification
    : QUERY NOTIFICATION SUBSCRIPTION (ALL | subscription_id = INT)
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/kill-stats-job-transact-sql
kill_stats_job
    : STATS JOB job_id = INT
    ;

// https://msdn.microsoft.com/en-us/library/ms188332.aspx
execute_statement
    : EXECUTE execute_body SEMI?
    ;

execute_body_batch
    : func_proc_name_server_database_schema (execute_statement_arg (COMMA execute_statement_arg)*)? SEMI?
    ;

//https://docs.microsoft.com/it-it/sql/t-sql/language-elements/execute-transact-sql?view=sql-server-ver15
execute_body
    : (return_status = LOCAL_ID EQ)? (func_proc_name_server_database_schema | execute_var_string) execute_statement_arg?
    | LPAREN execute_var_string (COMMA execute_var_string)* RPAREN (AS (LOGIN | USER) EQ STRING)? (
        AT_KEYWORD linkedServer = id_
    )?
    | AS ( (LOGIN | USER) EQ STRING | CALLER)
    ;

execute_statement_arg
    : execute_statement_arg_unnamed (COMMA execute_statement_arg)*     //Unnamed params can continue unnamed
    | execute_statement_arg_named (COMMA execute_statement_arg_named)* //Named can only be continued by unnamed
    ;

execute_statement_arg_named
    : name = LOCAL_ID EQ value = execute_parameter
    ;

execute_statement_arg_unnamed
    : value = execute_parameter
    ;

execute_parameter
    : (constant | LOCAL_ID (OUTPUT | OUT)? | id_ | DEFAULT | NULL_)
    ;

execute_var_string
    : LOCAL_ID (OUTPUT | OUT)? (PLUS LOCAL_ID (PLUS execute_var_string)?)?
    | STRING (PLUS LOCAL_ID (PLUS execute_var_string)?)?
    ;

// https://msdn.microsoft.com/en-us/library/ff848791.aspx
security_statement
    // https://msdn.microsoft.com/en-us/library/ms188354.aspx
    : execute_clause SEMI?
    // https://msdn.microsoft.com/en-us/library/ms187965.aspx
    | GRANT (ALL PRIVILEGES? | grant_permission (LPAREN column_name_list RPAREN)?) (
        ON (class_type_for_grant COLON COLON)? on_id = table_name
    )? TO to_principal += principal_id (COMMA to_principal += principal_id)* (WITH GRANT OPTION)? (
        AS as_principal = principal_id
    )? SEMI?
    // https://msdn.microsoft.com/en-us/library/ms178632.aspx
    | REVERT (WITH COOKIE EQ LOCAL_ID)? SEMI?
    | open_key
    | close_key
    | create_key
    | create_certificate
    ;

principal_id
    : id_
    | PUBLIC
    ;

create_certificate
    : CREATE CERTIFICATE certificate_name = id_ (AUTHORIZATION user_name = id_)? (
        FROM existing_keys
        | generate_new_keys
    ) (ACTIVE FOR BEGIN DIALOG EQ on_off)?
    ;

existing_keys
    : ASSEMBLY assembly_name = id_
    | EXECUTABLE? FILE EQ path_to_file = STRING (WITH PRIVATE KEY LPAREN private_key_options RPAREN)?
    ;

private_key_options
    : (FILE | HEX) EQ path = STRING (
        COMMA (DECRYPTION | ENCRYPTION) BY PASSWORD EQ password = STRING
    )?
    ;

generate_new_keys
    : (ENCRYPTION BY PASSWORD EQ password = STRING)? WITH SUBJECT EQ certificate_subject_name = STRING (
        COMMA date_options
    )*
    ;

date_options
    : (START_DATE | EXPIRY_DATE) EQ STRING
    ;

open_key
    : OPEN SYMMETRIC KEY key_name = id_ DECRYPTION BY decryption_mechanism
    | OPEN MASTER KEY DECRYPTION BY PASSWORD EQ password = STRING
    ;

close_key
    : CLOSE SYMMETRIC KEY key_name = id_
    | CLOSE ALL SYMMETRIC KEYS
    | CLOSE MASTER KEY
    ;

create_key
    : CREATE MASTER KEY ENCRYPTION BY PASSWORD EQ password = STRING
    | CREATE SYMMETRIC KEY key_name = id_ (AUTHORIZATION user_name = id_)? (
        FROM PROVIDER provider_name = id_
    )? WITH ((key_options | ENCRYPTION BY encryption_mechanism) COMMA?)+
    ;

key_options
    : KEY_SOURCE EQ pass_phrase = STRING
    | ALGORITHM EQ algorithm
    | IDENTITY_VALUE EQ identity_phrase = STRING
    | PROVIDER_KEY_NAME EQ key_name_in_provider = STRING
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

encryption_mechanism
    : CERTIFICATE certificate_name = id_
    | ASYMMETRIC KEY asym_key_name = id_
    | SYMMETRIC KEY decrypting_Key_name = id_
    | PASSWORD EQ STRING
    ;

decryption_mechanism
    : CERTIFICATE certificate_name = id_ (WITH PASSWORD EQ STRING)?
    | ASYMMETRIC KEY asym_key_name = id_ (WITH PASSWORD EQ STRING)?
    | SYMMETRIC KEY decrypting_Key_name = id_
    | PASSWORD EQ STRING
    ;

// https://docs.microsoft.com/en-us/sql/relational-databases/system-functions/sys-fn-builtin-permissions-transact-sql?view=sql-server-ver15
// SELECT DISTINCT '| ' + permission_name
// FROM sys.fn_builtin_permissions (DEFAULT)
// ORDER BY 1
grant_permission
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
set_statement
    : SET LOCAL_ID (DOT member_name = id_)? EQ expression
    | SET LOCAL_ID assignment_operator expression
    | SET LOCAL_ID EQ CURSOR declare_set_cursor_common (
        FOR (READ ONLY | UPDATE (OF column_name_list)?)
    )?
    // https://msdn.microsoft.com/en-us/library/ms189837.aspx
    | set_special
    ;

// https://msdn.microsoft.com/en-us/library/ms174377.aspx
transaction_statement
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
go_statement
    : GO (count = INT)?
    ;

// https://msdn.microsoft.com/en-us/library/ms188366.aspx
use_statement
    : USE database = id_
    ;

setuser_statement
    : SETUSER user = STRING?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/reconfigure-transact-sql
reconfigure_statement
    : RECONFIGURE (WITH OVERRIDE)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/shutdown-transact-sql
shutdown_statement
    : SHUTDOWN (WITH NOWAIT)?
    ;

checkpoint_statement
    : CHECKPOINT (checkPointDuration = INT)?
    ;

dbcc_checkalloc_option
    : ALL_ERRORMSGS
    | NO_INFOMSGS
    | TABLOCK
    | ESTIMATEONLY
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checkalloc-transact-sql?view=sql-server-ver16
dbcc_checkalloc
    : name = CHECKALLOC (
        LPAREN (database = id_ | databaseid = STRING | INT) (
            COMMA NOINDEX
            | COMMA ( REPAIR_ALLOW_DATA_LOSS | REPAIR_FAST | REPAIR_REBUILD)
        )? RPAREN (
            WITH dbcc_option = dbcc_checkalloc_option (COMMA dbcc_option = dbcc_checkalloc_option)*
        )?
    )?
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checkcatalog-transact-sql?view=sql-server-ver16
dbcc_checkcatalog
    : name = CHECKCATALOG (LPAREN ( database = id_ | databasename = STRING | INT) RPAREN)? (
        WITH dbcc_option = NO_INFOMSGS
    )?
    ;

dbcc_checkconstraints_option
    : ALL_CONSTRAINTS
    | ALL_ERRORMSGS
    | NO_INFOMSGS
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checkconstraints-transact-sql?view=sql-server-ver16
dbcc_checkconstraints
    : name = CHECKCONSTRAINTS (
        LPAREN (table_or_constraint = id_ | table_or_constraint_name = STRING) RPAREN
    )? (
        WITH dbcc_option = dbcc_checkconstraints_option (
            COMMA dbcc_option = dbcc_checkconstraints_option
        )*
    )?
    ;

dbcc_checkdb_table_option
    : ALL_ERRORMSGS
    | EXTENDED_LOGICAL_CHECKS
    | NO_INFOMSGS
    | TABLOCK
    | ESTIMATEONLY
    | PHYSICAL_ONLY
    | DATA_PURITY
    | MAXDOP EQ max_dregree_of_parallelism = INT
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checkdb-transact-sql?view=sql-server-ver16
dbcc_checkdb
    : name = CHECKDB (
        LPAREN (database = id_ | databasename = STRING | INT) (
            COMMA (NOINDEX | REPAIR_ALLOW_DATA_LOSS | REPAIR_FAST | REPAIR_REBUILD)
        )? RPAREN
    )? (
        WITH dbcc_option = dbcc_checkdb_table_option (COMMA dbcc_option = dbcc_checkdb_table_option)*
    )?
    ;

dbcc_checkfilegroup_option
    : ALL_ERRORMSGS
    | NO_INFOMSGS
    | TABLOCK
    | ESTIMATEONLY
    | PHYSICAL_ONLY
    | MAXDOP EQ max_dregree_of_parallelism = INT
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checkfilegroup-transact-sql?view=sql-server-ver16
// Additional parameters: https://dbtut.com/index.php/2019/01/01/dbcc-checkfilegroup-command-on-sql-server/
dbcc_checkfilegroup
    : name = CHECKFILEGROUP (
        LPAREN (filegroup_id = INT | filegroup_name = STRING) (
            COMMA (NOINDEX | REPAIR_ALLOW_DATA_LOSS | REPAIR_FAST | REPAIR_REBUILD)
        )? RPAREN
    )? (
        WITH dbcc_option = dbcc_checkfilegroup_option (
            COMMA dbcc_option = dbcc_checkfilegroup_option
        )*
    )?
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checktable-transact-sql?view=sql-server-ver16
dbcc_checktable
    : name = CHECKTABLE LPAREN table_or_view_name = STRING (
        COMMA (
            NOINDEX
            | index_id = expression
            | REPAIR_ALLOW_DATA_LOSS
            | REPAIR_FAST
            | REPAIR_REBUILD
        )
    )? RPAREN (
        WITH dbcc_option = dbcc_checkdb_table_option (COMMA dbcc_option = dbcc_checkdb_table_option)*
    )?
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-cleantable-transact-sql?view=sql-server-ver16
dbcc_cleantable
    : name = CLEANTABLE LPAREN (database = id_ | databasename = STRING | INT) COMMA (
        table_or_view = id_
        | table_or_view_name = STRING
    ) (COMMA batch_size = INT)? RPAREN (WITH dbcc_option = NO_INFOMSGS)?
    ;

dbcc_clonedatabase_option
    : NO_STATISTICS
    | NO_QUERYSTORE
    | SERVICEBROKER
    | VERIFY_CLONEDB
    | BACKUP_CLONEDB
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-clonedatabase-transact-sql?view=sql-server-ver16
dbcc_clonedatabase
    : name = CLONEDATABASE LPAREN source_database = id_ COMMA target_database = id_ RPAREN (
        WITH dbcc_option = dbcc_clonedatabase_option (COMMA dbcc_option = dbcc_clonedatabase_option)*
    )?
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-pdw-showspaceused-transact-sql?view=aps-pdw-2016-au7
dbcc_pdw_showspaceused
    : name = PDW_SHOWSPACEUSED (LPAREN tablename = id_ RPAREN)? (
        WITH dbcc_option = IGNORE_REPLICATED_TABLE_CACHE
    )?
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-proccache-transact-sql?view=sql-server-ver16
dbcc_proccache
    : name = PROCCACHE (WITH dbcc_option = NO_INFOMSGS)?
    ;

dbcc_showcontig_option
    : ALL_INDEXES
    | TABLERESULTS
    | FAST
    | ALL_LEVELS
    | NO_INFOMSGS
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-showcontig-transact-sql?view=sql-server-ver16
dbcc_showcontig
    : name = SHOWCONTIG (LPAREN table_or_view = expression ( COMMA index = expression)? RPAREN)? (
        WITH dbcc_option = dbcc_showcontig_option (COMMA dbcc_showcontig_option)*
    )?
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-shrinklog-azure-sql-data-warehouse?view=aps-pdw-2016-au7
dbcc_shrinklog
    : name = SHRINKLOG (LPAREN SIZE EQ ( (INT ( MB | GB | TB)) | DEFAULT) RPAREN)? (
        WITH dbcc_option = NO_INFOMSGS
    )?
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-dbreindex-transact-sql?view=sql-server-ver16
dbcc_dbreindex
    : name = DBREINDEX LPAREN table = id_or_string (
        COMMA index_name = id_or_string ( COMMA fillfactor = expression)?
    )? RPAREN (WITH dbcc_option = NO_INFOMSGS)?
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-dllname-free-transact-sql?view=sql-server-ver16
dbcc_dll_free
    : dllname = id_ LPAREN name = FREE RPAREN (WITH dbcc_option = NO_INFOMSGS)?
    ;

// https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-dropcleanbuffers-transact-sql?view=sql-server-ver16
dbcc_dropcleanbuffers
    : name = DROPCLEANBUFFERS (LPAREN COMPUTE | ALL RPAREN)? (WITH dbcc_option = NO_INFOMSGS)?
    ;

dbcc_clause
    : DBCC (
        dbcc_checkalloc
        | dbcc_checkcatalog
        | dbcc_checkconstraints
        | dbcc_checkdb
        | dbcc_checkfilegroup
        | dbcc_checktable
        | dbcc_cleantable
        | dbcc_clonedatabase
        | dbcc_dbreindex
        | dbcc_dll_free
        | dbcc_dropcleanbuffers
        | dbcc_pdw_showspaceused
        | dbcc_proccache
        | dbcc_showcontig
        | dbcc_shrinklog
    )
    ;

execute_clause
    : EXECUTE AS clause = (CALLER | SELF | OWNER | STRING)
    ;

declare_local
    : LOCAL_ID AS? data_type (EQ expression)?
    ;

table_type_definition
    : TABLE LPAREN column_def_table_constraints (COMMA? table_type_indices)* RPAREN
    ;

table_type_indices
    : (((PRIMARY KEY | INDEX id_) (CLUSTERED | NONCLUSTERED)?) | UNIQUE) LPAREN column_name_list_with_order RPAREN
    | CHECK LPAREN search_condition RPAREN
    ;

xml_type_definition
    : XML LPAREN (CONTENT | DOCUMENT)? xml_schema_collection RPAREN
    ;

xml_schema_collection
    : ID DOT ID
    ;

column_def_table_constraints
    : column_def_table_constraint (COMMA? column_def_table_constraint)*
    ;

column_def_table_constraint
    : column_definition
    | materialized_column_definition
    | table_constraint
    ;

// https://msdn.microsoft.com/en-us/library/ms187742.aspx
// There is a documentation error: column definition elements can be given in
// any order
column_definition
    : id_ (data_type | AS expression PERSISTED?) column_definition_element* column_index?
    ;

column_definition_element
    : FILESTREAM
    | COLLATE collation_name = id_
    | SPARSE
    | MASKED WITH LPAREN FUNCTION EQ mask_function = STRING RPAREN
    | (CONSTRAINT constraint = id_)? DEFAULT constant_expr = expression
    | IDENTITY (LPAREN seed = INT COMMA increment = INT RPAREN)?
    | NOT FOR REPLICATION
    | GENERATED ALWAYS AS (ROW | TRANSACTION_ID | SEQUENCE_NUMBER) (START | END) HIDDEN_KEYWORD?
    // NULL / NOT NULL is a constraint
    | ROWGUIDCOL
    | ENCRYPTED WITH LPAREN COLUMN_ENCRYPTION_KEY EQ key_name = STRING COMMA ENCRYPTION_TYPE EQ (
        DETERMINISTIC
        | RANDOMIZED
    ) COMMA ALGORITHM EQ algo = STRING RPAREN
    | column_constraint
    ;

column_modifier
    : id_ (ADD | DROP) (
        ROWGUIDCOL
        | PERSISTED
        | NOT FOR REPLICATION
        | SPARSE
        | HIDDEN_KEYWORD
        | MASKED (WITH (FUNCTION EQ STRING | LPAREN FUNCTION EQ STRING RPAREN))?
    )
    ;

materialized_column_definition
    : id_ (COMPUTE | AS) expression (MATERIALIZED | NOT MATERIALIZED)?
    ;

// https://msdn.microsoft.com/en-us/library/ms186712.aspx
// There is a documentation error: NOT NULL is a constraint
// and therefore can be given a name.
column_constraint
    : (CONSTRAINT constraint = id_)? (
        null_notnull
        | ( (PRIMARY KEY | UNIQUE) clustered? primary_key_options)
        | ( (FOREIGN KEY)? foreign_key_options)
        | check_constraint
    )
    ;

column_index
    : INDEX index_name = id_ clustered? create_table_index_options? on_partition_or_filegroup? (
        FILESTREAM_ON (filestream_filegroup_or_partition_schema_name = id_ | NULL_DOUBLE_QUOTE)
    )?
    ;

on_partition_or_filegroup
    : ON (
        (partition_scheme_name = id_ LPAREN partition_column_name = id_ RPAREN)
        | filegroup = id_
        | DEFAULT_DOUBLE_QUOTE
    )
    ;

// https://msdn.microsoft.com/en-us/library/ms188066.aspx
table_constraint
    : (CONSTRAINT constraint = id_)? (
        ((PRIMARY KEY | UNIQUE) clustered? LPAREN column_name_list_with_order RPAREN primary_key_options)
        | ( FOREIGN KEY LPAREN fk = column_name_list RPAREN foreign_key_options)
        | ( CONNECTION LPAREN connection_node ( COMMA connection_node)* RPAREN)
        | ( DEFAULT constant_expr = expression FOR column = id_ (WITH VALUES)?)
        | check_constraint
    )
    ;

connection_node
    : from_node_table = id_ TO to_node_table = id_
    ;

primary_key_options
    : (WITH FILLFACTOR EQ INT)? alter_table_index_options? on_partition_or_filegroup?
    ;

foreign_key_options
    : REFERENCES table_name LPAREN pk = column_name_list RPAREN (on_delete | on_update)* (
        NOT FOR REPLICATION
    )?
    ;

check_constraint
    : CHECK (NOT FOR REPLICATION)? LPAREN search_condition RPAREN
    ;

on_delete
    : ON DELETE (NO ACTION | CASCADE | SET NULL_ | SET DEFAULT)
    ;

on_update
    : ON UPDATE (NO ACTION | CASCADE | SET NULL_ | SET DEFAULT)
    ;

alter_table_index_options
    : WITH LPAREN alter_table_index_option (COMMA alter_table_index_option)* RPAREN
    ;

// https://msdn.microsoft.com/en-us/library/ms186869.aspx
alter_table_index_option
    : PAD_INDEX EQ on_off
    | FILLFACTOR EQ INT
    | IGNORE_DUP_KEY EQ on_off
    | STATISTICS_NORECOMPUTE EQ on_off
    | ALLOW_ROW_LOCKS EQ on_off
    | ALLOW_PAGE_LOCKS EQ on_off
    | OPTIMIZE_FOR_SEQUENTIAL_KEY EQ on_off
    | SORT_IN_TEMPDB EQ on_off
    | MAXDOP EQ max_degree_of_parallelism = INT
    | DATA_COMPRESSION EQ (NONE | ROW | PAGE | COLUMNSTORE | COLUMNSTORE_ARCHIVE) on_partitions?
    | XML_COMPRESSION EQ on_off on_partitions?
    | DISTRIBUTION EQ HASH LPAREN id_ RPAREN
    | CLUSTERED INDEX LPAREN id_ (ASC | DESC)? (COMMA id_ (ASC | DESC)?)* RPAREN
    | ONLINE EQ (ON (LPAREN low_priority_lock_wait RPAREN)? | OFF)
    | RESUMABLE EQ on_off
    | MAX_DURATION EQ times = INT MINUTES?
    ;

// https://msdn.microsoft.com/en-us/library/ms180169.aspx
declare_cursor
    : DECLARE cursor_name (
        CURSOR (declare_set_cursor_common (FOR UPDATE (OF column_name_list)?)?)?
        | (SEMI_SENSITIVE | INSENSITIVE)? SCROLL? CURSOR FOR select_statement_standalone (
            FOR (READ ONLY | UPDATE | (OF column_name_list))
        )?
    ) SEMI?
    ;

declare_set_cursor_common
    : declare_set_cursor_common_partial* FOR select_statement_standalone
    ;

declare_set_cursor_common_partial
    : (LOCAL | GLOBAL)
    | (FORWARD_ONLY | SCROLL)
    | (STATIC | KEYSET | DYNAMIC | FAST_FORWARD)
    | (READ_ONLY | SCROLL_LOCKS | OPTIMISTIC)
    | TYPE_WARNING
    ;

fetch_cursor
    : FETCH ((NEXT | PRIOR | FIRST | LAST | (ABSOLUTE | RELATIVE) expression)? FROM)? GLOBAL? cursor_name (
        INTO LOCAL_ID (COMMA LOCAL_ID)*
    )? SEMI?
    ;

// https://msdn.microsoft.com/en-us/library/ms190356.aspx
// Runtime check.
set_special
    : SET id_ (id_ | constant_LOCAL_ID | on_off) SEMI?
    | SET STATISTICS (IO | TIME | XML | PROFILE) on_off SEMI?
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
    | SET IDENTITY_INSERT table_name on_off SEMI?
    | SET special_list (COMMA special_list)* on_off
    | SET modify_method
    ;

special_list
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
    : primitive_expression
    | function_call
    | expression DOT (value_call | query_call | exist_call | modify_call)
    | expression DOT hierarchyid_call
    | expression COLLATE id_
    | case_expression
    | full_column_name
    | bracket_expression
    | unary_operator_expression
    | expression op = (STAR | DIV | MOD) expression
    | expression op = (PLUS | MINUS | BIT_AND | BIT_XOR | BIT_OR | DOUBLE_BAR) expression
    | expression time_zone
    | over_clause
    | DOLLAR_ACTION
    ;

parameter
    : PLACEHOLDER
    ;

time_zone
    : AT_KEYWORD TIME ZONE expression
    ;

primitive_expression
    : DEFAULT
    | NULL_
    | LOCAL_ID
    | primitive_constant
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/language-elements/case-transact-sql
case_expression
    : CASE caseExpr = expression switch_section+ (ELSE elseExpr = expression)? END
    | CASE switch_search_condition_section+ (ELSE elseExpr = expression)? END
    ;

unary_operator_expression
    : BIT_NOT expression
    | op = (PLUS | MINUS) expression
    ;

bracket_expression
    : LPAREN expression RPAREN
    | LPAREN subquery RPAREN
    ;

subquery
    : select_statement
    ;

// https://msdn.microsoft.com/en-us/library/ms175972.aspx
with_expression
    : WITH ctes += common_table_expression (COMMA ctes += common_table_expression)*
    ;

common_table_expression
    : expression_name = id_ (LPAREN columns = column_name_list RPAREN)? AS LPAREN cte_query = select_statement RPAREN
    ;

update_elem
    : LOCAL_ID EQ full_column_name (EQ | assignment_operator) expression //Combined variable and column update
    | (full_column_name | LOCAL_ID) (EQ | assignment_operator) expression
    | udt_column_name = id_ DOT method_name = id_ LPAREN expression_list_ RPAREN
    //| full_column_name DOT WRITE (expression, )
    ;

update_elem_merge
    : (full_column_name | LOCAL_ID) (EQ | assignment_operator) expression
    | udt_column_name = id_ DOT method_name = id_ LPAREN expression_list_ RPAREN
    //| full_column_name DOT WRITE (expression, )
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/queries/search-condition-transact-sql
search_condition
    : NOT* (predicate | LPAREN search_condition RPAREN)
    | search_condition AND search_condition // AND takes precedence over OR
    | search_condition OR search_condition
    ;

predicate
    : EXISTS LPAREN subquery RPAREN
    | freetext_predicate
    | expression comparison_operator expression
    | expression ME expression ////SQL-82 syntax for left outer joins; PE. See https://stackoverflow.com/questions/40665/in-sybase-sql
    | expression comparison_operator (ALL | SOME | ANY) LPAREN subquery RPAREN
    | expression NOT* BETWEEN expression AND expression
    | expression NOT* IN LPAREN (subquery | expression_list_) RPAREN
    | expression NOT* LIKE expression (ESCAPE expression)?
    | expression IS null_notnull
    ;

// Changed union rule to sql_union to avoid union construct with C++ target.  Issue reported by person who generates into C++.  This individual reports change causes generated code to work

query_expression
    : query_specification select_order_by_clause? unions += sql_union* //if using top, order by can be on the "top" side of union :/
    | LPAREN query_expression RPAREN (UNION ALL? query_expression)?
    ;

sql_union
    : (UNION ALL? | EXCEPT | INTERSECT) (
        spec = query_specification
        | (LPAREN op = query_expression RPAREN)
    )
    ;

// https://msdn.microsoft.com/en-us/library/ms176104.aspx
query_specification
    : SELECT allOrDistinct = (ALL | DISTINCT)? top = top_clause? columns = select_list
    // https://msdn.microsoft.com/en-us/library/ms188029.aspx
    (INTO into = table_name)? (FROM from = table_sources)? (WHERE where = search_condition)?
    // https://msdn.microsoft.com/en-us/library/ms177673.aspx
    (
        GROUP BY (
            (groupByAll = ALL? groupBys += group_by_item (COMMA groupBys += group_by_item)*)
            | GROUPING SETS LPAREN groupSets += grouping_sets_item (
                COMMA groupSets += grouping_sets_item
            )* RPAREN
        )
    )? (HAVING having = search_condition)?
    ;

// https://msdn.microsoft.com/en-us/library/ms189463.aspx
top_clause
    : TOP (top_percent | top_count) (WITH TIES)?
    ;

top_percent
    : percent_constant = (REAL | FLOAT | INT) PERCENT
    | LPAREN topper_expression = expression RPAREN PERCENT
    ;

top_count
    : count_constant = INT
    | LPAREN topcount_expression = expression RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/queries/select-over-clause-transact-sql?view=sql-server-ver16
order_by_clause
    : ORDER BY order_bys += order_by_expression (COMMA order_bys += order_by_expression)*
    ;

// https://msdn.microsoft.com/en-us/library/ms188385.aspx
select_order_by_clause
    : order_by_clause (
        OFFSET offset_exp = expression offset_rows = (ROW | ROWS) (
            FETCH fetch_offset = (FIRST | NEXT) fetch_exp = expression fetch_rows = (ROW | ROWS) ONLY
        )?
    )?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/queries/select-for-clause-transact-sql
for_clause
    : FOR BROWSE
    | FOR XML (RAW (LPAREN STRING RPAREN)? | AUTO) xml_common_directives* (
        COMMA (XMLDATA | XMLSCHEMA (LPAREN STRING RPAREN)?)
    )? (COMMA ELEMENTS (XSINIL | ABSENT)?)?
    | FOR XML EXPLICIT xml_common_directives* (COMMA XMLDATA)?
    | FOR XML PATH (LPAREN STRING RPAREN)? xml_common_directives* (COMMA ELEMENTS (XSINIL | ABSENT)?)?
    | FOR JSON (AUTO | PATH) (
        COMMA (ROOT (LPAREN STRING RPAREN) | INCLUDE_NULL_VALUES | WITHOUT_ARRAY_WRAPPER)
    )*
    ;

xml_common_directives
    : COMMA (BINARY_KEYWORD BASE64 | TYPE | ROOT (LPAREN STRING RPAREN)?)
    ;

order_by_expression
    : order_by = expression (ascending = ASC | descending = DESC)?
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/queries/select-group-by-transact-sql?view=sql-server-ver15
grouping_sets_item
    : LPAREN? groupSetItems += group_by_item (COMMA groupSetItems += group_by_item)* RPAREN?
    | LPAREN RPAREN
    ;

group_by_item
    : expression
    /*| rollup_spec
    | cube_spec
    | grouping_sets_spec
    | grand_total*/
    ;

option_clause
    // https://msdn.microsoft.com/en-us/library/ms181714.aspx
    : OPTION LPAREN options_ += option (COMMA options_ += option)* RPAREN
    ;

option
    : FAST number_rows = INT
    | (HASH | ORDER) GROUP
    | (MERGE | HASH | CONCAT) UNION
    | (LOOP | MERGE | HASH) JOIN
    | EXPAND VIEWS
    | FORCE ORDER
    | IGNORE_NONCLUSTERED_COLUMNSTORE_INDEX
    | KEEP PLAN
    | KEEPFIXED PLAN
    | MAXDOP number_of_processors = INT
    | MAXRECURSION number_recursion = INT
    | OPTIMIZE FOR LPAREN optimize_for_arg (COMMA optimize_for_arg)* RPAREN
    | OPTIMIZE FOR UNKNOWN
    | PARAMETERIZATION (SIMPLE | FORCED)
    | RECOMPILE
    | ROBUST PLAN
    | USE PLAN STRING
    ;

optimize_for_arg
    : LOCAL_ID (UNKNOWN | EQ (constant | NULL_))
    ;

// https://msdn.microsoft.com/en-us/library/ms176104.aspx
select_list
    : selectElement += select_list_elem (COMMA selectElement += select_list_elem)*
    ;

udt_method_arguments
    : LPAREN argument += execute_var_string (COMMA argument += execute_var_string)* RPAREN
    ;

// https://docs.microsoft.com/ru-ru/sql/t-sql/queries/select-clause-transact-sql
asterisk
    : (table_name DOT)? STAR
    | (INSERTED | DELETED) DOT STAR
    ;

udt_elem
    : udt_column_name = id_ DOT non_static_attr = id_ udt_method_arguments as_column_alias?
    | udt_column_name = id_ DOUBLE_COLON static_attr = id_ udt_method_arguments? as_column_alias?
    ;

expression_elem
    : leftAlias = column_alias eq = EQ leftAssignment = expression
    | expressionAs = expression as_column_alias?
    ;

select_list_elem
    : asterisk
    | udt_elem
    | LOCAL_ID (assignment_operator | EQ) expression
    | expression_elem
    ;

table_sources
    : non_ansi_join
    | source += table_source (COMMA source += table_source)*
    ;

// https://sqlenlight.com/support/help/sa0006/
non_ansi_join
    : source += table_source (COMMA source += table_source)+
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/queries/from-transact-sql
table_source
    : table_source_item joins += join_part*
    ;

table_source_item
    : full_table_name deprecated_table_hint as_table_alias // this is currently allowed
    | full_table_name as_table_alias? (
        with_table_hints
        | deprecated_table_hint
        | sybase_legacy_hints
    )?
    | rowset_function as_table_alias?
    | LPAREN derived_table RPAREN (as_table_alias column_alias_list?)?
    | change_table as_table_alias?
    | nodes_method (as_table_alias column_alias_list?)?
    | function_call (as_table_alias column_alias_list?)?
    | loc_id = LOCAL_ID as_table_alias?
    | loc_id_call = LOCAL_ID DOT loc_fcall = function_call (as_table_alias column_alias_list?)?
    | open_xml
    | open_json
    | DOUBLE_COLON oldstyle_fcall = function_call as_table_alias? // Build-in function (old syntax)
    | LPAREN table_source RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/functions/openxml-transact-sql
open_xml
    : OPENXML LPAREN expression COMMA expression (COMMA expression)? RPAREN (WITH LPAREN schema_declaration RPAREN)? as_table_alias?
    ;

open_json
    : OPENJSON LPAREN expression (COMMA expression)? RPAREN (WITH LPAREN json_declaration RPAREN)? as_table_alias?
    ;

json_declaration
    : json_col += json_column_declaration (COMMA json_col += json_column_declaration)*
    ;

json_column_declaration
    : column_declaration (AS JSON)?
    ;

schema_declaration
    : xml_col += column_declaration (COMMA xml_col += column_declaration)*
    ;

column_declaration
    : id_ data_type STRING?
    ;

change_table
    : change_table_changes
    | change_table_version
    ;

change_table_changes
    : CHANGETABLE LPAREN CHANGES changetable = table_name COMMA changesid = (NULL_ | INT | LOCAL_ID) RPAREN
    ;

change_table_version
    : CHANGETABLE LPAREN VERSION versiontable = table_name COMMA pk_columns = full_column_name_list COMMA pk_values = select_list RPAREN
    ;

// https://msdn.microsoft.com/en-us/library/ms191472.aspx
join_part
    // https://msdn.microsoft.com/en-us/library/ms173815(v=sql.120).aspx
    : join_on
    | cross_join
    | apply_
    | pivot
    | unpivot
    ;

outer_join
    : (LEFT | RIGHT | FULL) OUTER?
    ;

join_type
    : INNER
    | outer_join
    ;

join_on
    : join_type? (
        join_hint = (LOOP | HASH | MERGE | REMOTE)
    )? JOIN source = table_source ON cond = search_condition
    ;

cross_join
    : CROSS JOIN table_source_item
    ;

apply_
    : apply_style = (CROSS | OUTER) APPLY source = table_source_item
    ;

pivot
    : PIVOT pivot_clause as_table_alias
    ;

unpivot
    : UNPIVOT unpivot_clause as_table_alias
    ;

pivot_clause
    : LPAREN aggregate_windowed_function FOR full_column_name IN column_alias_list RPAREN
    ;

unpivot_clause
    : LPAREN unpivot_exp = expression FOR full_column_name IN LPAREN full_column_name_list RPAREN RPAREN
    ;

full_column_name_list
    : column += full_column_name (COMMA column += full_column_name)*
    ;

// https://msdn.microsoft.com/en-us/library/ms190312.aspx
rowset_function
    : (
        OPENROWSET LPAREN provider_name = STRING COMMA connectionString = STRING COMMA sql = STRING RPAREN
    )
    | (OPENROWSET LPAREN BULK data_file = STRING COMMA (bulk_option (COMMA bulk_option)* | id_) RPAREN)
    ;

// runtime check.
bulk_option
    : id_ EQ bulk_option_value = (INT | STRING)
    ;

derived_table
    : subquery
    | LPAREN subquery (UNION ALL subquery)* RPAREN
    | table_value_constructor
    | LPAREN table_value_constructor RPAREN
    ;

function_call
    : ranking_windowed_function                      # RANKING_WINDOWED_FUNC
    | aggregate_windowed_function                    # AGGREGATE_WINDOWED_FUNC
    | analytic_windowed_function                     # ANALYTIC_WINDOWED_FUNC
    | built_in_functions                             # BUILT_IN_FUNC
    | scalar_function_name LPAREN expression_list_? RPAREN # SCALAR_FUNCTION
    | freetext_function                              # FREE_TEXT
    | partition_function                             # PARTITION_FUNC
    | hierarchyid_static_method                      # HIERARCHYID_METHOD
    ;

partition_function
    : (database = id_ DOT)? DOLLAR_PARTITION DOT func_name = id_ LPAREN expression RPAREN
    ;

freetext_function
    : (CONTAINSTABLE | FREETEXTTABLE) LPAREN table_name COMMA (
        full_column_name
        | LPAREN full_column_name (COMMA full_column_name)* RPAREN
        | STAR
    ) COMMA expression (COMMA LANGUAGE expression)? (COMMA expression)? RPAREN
    | (SEMANTICSIMILARITYTABLE | SEMANTICKEYPHRASETABLE) LPAREN table_name COMMA (
        full_column_name
        | LPAREN full_column_name (COMMA full_column_name)* RPAREN
        | STAR
    ) COMMA expression RPAREN
    | SEMANTICSIMILARITYDETAILSTABLE LPAREN table_name COMMA full_column_name COMMA expression COMMA full_column_name COMMA expression RPAREN
    ;

freetext_predicate
    : CONTAINS LPAREN (
        full_column_name
        | LPAREN full_column_name (COMMA full_column_name)* RPAREN
        | STAR
        | PROPERTY LPAREN full_column_name COMMA expression RPAREN
    ) COMMA expression RPAREN
    | FREETEXT LPAREN table_name COMMA (
        full_column_name
        | LPAREN full_column_name (COMMA full_column_name)* RPAREN
        | STAR
    ) COMMA expression (COMMA LANGUAGE expression)? RPAREN
    ;

json_key_value
    : json_key_name = expression COLON value_expression = expression
    ;

json_null_clause
    : (ABSENT | NULL_) ON NULL_
    ;

built_in_functions
    // Metadata functions
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/app-name-transact-sql?view=sql-server-ver16
    : APP_NAME LPAREN RPAREN # APP_NAME
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/applock-mode-transact-sql?view=sql-server-ver16
    | APPLOCK_MODE LPAREN database_principal = expression COMMA resource_name = expression COMMA lock_owner = expression RPAREN # APPLOCK_MODE
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/applock-test-transact-sql?view=sql-server-ver16
    | APPLOCK_TEST LPAREN database_principal = expression COMMA resource_name = expression COMMA lock_mode = expression COMMA lock_owner = expression RPAREN #
        APPLOCK_TEST
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/assemblyproperty-transact-sql?view=sql-server-ver16
    | ASSEMBLYPROPERTY LPAREN assembly_name = expression COMMA property_name = expression RPAREN # ASSEMBLYPROPERTY
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/col-length-transact-sql?view=sql-server-ver16
    | COL_LENGTH LPAREN table = expression COMMA column = expression RPAREN # COL_LENGTH
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/col-name-transact-sql?view=sql-server-ver16
    | COL_NAME LPAREN table_id = expression COMMA column_id = expression RPAREN # COL_NAME
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/columnproperty-transact-sql?view=sql-server-ver16
    | COLUMNPROPERTY LPAREN id = expression COMMA column = expression COMMA property = expression RPAREN # COLUMNPROPERTY
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/databasepropertyex-transact-sql?view=sql-server-ver16
    | DATABASEPROPERTYEX LPAREN database = expression COMMA property = expression RPAREN # DATABASEPROPERTYEX
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/db-id-transact-sql?view=sql-server-ver16
    | DB_ID LPAREN database_name = expression? RPAREN # DB_ID
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/db-name-transact-sql?view=sql-server-ver16
    | DB_NAME LPAREN database_id = expression? RPAREN # DB_NAME
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/file-id-transact-sql?view=sql-server-ver16
    | FILE_ID LPAREN file_name = expression RPAREN # FILE_ID
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/file-idex-transact-sql?view=sql-server-ver16
    | FILE_IDEX LPAREN file_name = expression RPAREN # FILE_IDEX
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/file-name-transact-sql?view=sql-server-ver16
    | FILE_NAME LPAREN file_id = expression RPAREN # FILE_NAME
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/filegroup-id-transact-sql?view=sql-server-ver16
    | FILEGROUP_ID LPAREN filegroup_name = expression RPAREN # FILEGROUP_ID
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/filegroup-name-transact-sql?view=sql-server-ver16
    | FILEGROUP_NAME LPAREN filegroup_id = expression RPAREN # FILEGROUP_NAME
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/filegroupproperty-transact-sql?view=sql-server-ver16
    | FILEGROUPPROPERTY LPAREN filegroup_name = expression COMMA property = expression RPAREN # FILEGROUPPROPERTY
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/fileproperty-transact-sql?view=sql-server-ver16
    | FILEPROPERTY LPAREN file_name = expression COMMA property = expression RPAREN # FILEPROPERTY
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/filepropertyex-transact-sql?view=sql-server-ver16
    | FILEPROPERTYEX LPAREN name = expression COMMA property = expression RPAREN # FILEPROPERTYEX
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/fulltextcatalogproperty-transact-sql?view=sql-server-ver16
    | FULLTEXTCATALOGPROPERTY LPAREN catalog_name = expression COMMA property = expression RPAREN # FULLTEXTCATALOGPROPERTY
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/fulltextserviceproperty-transact-sql?view=sql-server-ver16
    | FULLTEXTSERVICEPROPERTY LPAREN property = expression RPAREN # FULLTEXTSERVICEPROPERTY
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/index-col-transact-sql?view=sql-server-ver16
    | INDEX_COL LPAREN table_or_view_name = expression COMMA index_id = expression COMMA key_id = expression RPAREN # INDEX_COL
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/indexkey-property-transact-sql?view=sql-server-ver16
    | INDEXKEY_PROPERTY LPAREN object_id = expression COMMA index_id = expression COMMA key_id = expression COMMA property = expression RPAREN # INDEXKEY_PROPERTY
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/indexproperty-transact-sql?view=sql-server-ver16
    | INDEXPROPERTY LPAREN object_id = expression COMMA index_or_statistics_name = expression COMMA property = expression RPAREN # INDEXPROPERTY
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/next-value-for-transact-sql?view=sql-server-ver16
    | NEXT VALUE FOR sequence_name = table_name (OVER LPAREN order_by_clause RPAREN)? # NEXT_VALUE_FOR
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/object-definition-transact-sql?view=sql-server-ver16
    | OBJECT_DEFINITION LPAREN object_id = expression RPAREN # OBJECT_DEFINITION
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/object-id-transact-sql?view=sql-server-ver16
    | OBJECT_ID LPAREN object_name = expression (COMMA object_type = expression)? RPAREN # OBJECT_ID
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/object-name-transact-sql?view=sql-server-ver16
    | OBJECT_NAME LPAREN object_id = expression (COMMA database_id = expression)? RPAREN # OBJECT_NAME
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/object-schema-name-transact-sql?view=sql-server-ver16
    | OBJECT_SCHEMA_NAME LPAREN object_id = expression (COMMA database_id = expression)? RPAREN # OBJECT_SCHEMA_NAME
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/objectproperty-transact-sql?view=sql-server-ver16
    | OBJECTPROPERTY LPAREN id = expression COMMA property = expression RPAREN # OBJECTPROPERTY
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/objectpropertyex-transact-sql?view=sql-server-ver16
    | OBJECTPROPERTYEX LPAREN id = expression COMMA property = expression RPAREN # OBJECTPROPERTYEX
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/original-db-name-transact-sql?view=sql-server-ver16
    | ORIGINAL_DB_NAME LPAREN RPAREN # ORIGINAL_DB_NAME
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/parsename-transact-sql?view=sql-server-ver16
    | PARSENAME LPAREN object_name = expression COMMA object_piece = expression RPAREN # PARSENAME
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/schema-id-transact-sql?view=sql-server-ver16
    | SCHEMA_ID LPAREN schema_name = expression? RPAREN # SCHEMA_ID
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/schema-name-transact-sql?view=sql-server-ver16
    | SCHEMA_NAME LPAREN schema_id = expression? RPAREN # SCHEMA_NAME
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/scope-identity-transact-sql?view=sql-server-ver16
    | SCOPE_IDENTITY LPAREN RPAREN # SCOPE_IDENTITY
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/serverproperty-transact-sql?view=sql-server-ver16
    | SERVERPROPERTY LPAREN property = expression RPAREN # SERVERPROPERTY
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/stats-date-transact-sql?view=sql-server-ver16
    | STATS_DATE LPAREN object_id = expression COMMA stats_id = expression RPAREN # STATS_DATE
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/type-id-transact-sql?view=sql-server-ver16
    | TYPE_ID LPAREN type_name = expression RPAREN # TYPE_ID
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/type-name-transact-sql?view=sql-server-ver16
    | TYPE_NAME LPAREN type_id = expression RPAREN # TYPE_NAME
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/typeproperty-transact-sql?view=sql-server-ver16
    | TYPEPROPERTY LPAREN type = expression COMMA property = expression RPAREN # TYPEPROPERTY
    // String functions
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/ascii-transact-sql?view=sql-server-ver16
    | ASCII LPAREN character_expression = expression RPAREN # ASCII
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/char-transact-sql?view=sql-server-ver16
    | CHAR LPAREN integer_expression = expression RPAREN # CHAR
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/charindex-transact-sql?view=sql-server-ver16
    | CHARINDEX LPAREN expressionToFind = expression COMMA expressionToSearch = expression (
        COMMA start_location = expression
    )? RPAREN # CHARINDEX
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/concat-transact-sql?view=sql-server-ver16
    | CONCAT LPAREN string_value_1 = expression COMMA string_value_2 = expression (
        COMMA string_value_n += expression
    )* RPAREN # CONCAT
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/concat-ws-transact-sql?view=sql-server-ver16
    | CONCAT_WS LPAREN separator = expression COMMA argument_1 = expression COMMA argument_2 = expression (
        COMMA argument_n += expression
    )* RPAREN # CONCAT_WS
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/difference-transact-sql?view=sql-server-ver16
    | DIFFERENCE LPAREN character_expression_1 = expression COMMA character_expression_2 = expression RPAREN # DIFFERENCE
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/format-transact-sql?view=sql-server-ver16
    | FORMAT LPAREN value = expression COMMA format = expression (COMMA culture = expression)? RPAREN # FORMAT
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/left-transact-sql?view=sql-server-ver16
    | LEFT LPAREN character_expression = expression COMMA integer_expression = expression RPAREN # LEFT
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/len-transact-sql?view=sql-server-ver16
    | LEN LPAREN string_expression = expression RPAREN # LEN
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/lower-transact-sql?view=sql-server-ver16
    | LOWER LPAREN character_expression = expression RPAREN # LOWER
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/ltrim-transact-sql?view=sql-server-ver16
    | LTRIM LPAREN character_expression = expression RPAREN # LTRIM
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/nchar-transact-sql?view=sql-server-ver16
    | NCHAR LPAREN integer_expression = expression RPAREN # NCHAR
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/patindex-transact-sql?view=sql-server-ver16
    | PATINDEX LPAREN pattern = expression COMMA string_expression = expression RPAREN # PATINDEX
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/quotename-transact-sql?view=sql-server-ver16
    | QUOTENAME LPAREN character_string = expression (COMMA quote_character = expression)? RPAREN # QUOTENAME
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/replace-transact-sql?view=sql-server-ver16
    | REPLACE LPAREN input = expression COMMA replacing = expression COMMA with = expression RPAREN # REPLACE
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/replicate-transact-sql?view=sql-server-ver16
    | REPLICATE LPAREN string_expression = expression COMMA integer_expression = expression RPAREN # REPLICATE
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/reverse-transact-sql?view=sql-server-ver16
    | REVERSE LPAREN string_expression = expression RPAREN # REVERSE
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/right-transact-sql?view=sql-server-ver16
    | RIGHT LPAREN character_expression = expression COMMA integer_expression = expression RPAREN # RIGHT
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/rtrim-transact-sql?view=sql-server-ver16
    | RTRIM LPAREN character_expression = expression RPAREN # RTRIM
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/soundex-transact-sql?view=sql-server-ver16
    | SOUNDEX LPAREN character_expression = expression RPAREN # SOUNDEX
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/space-transact-sql?view=sql-server-ver16
    | SPACE_KEYWORD LPAREN integer_expression = expression RPAREN # SPACE
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/str-transact-sql?view=sql-server-ver16
    | STR LPAREN float_expression = expression (
        COMMA length_expression = expression ( COMMA decimal = expression)?
    )? RPAREN # STR
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/string-agg-transact-sql?view=sql-server-ver16
    | STRING_AGG LPAREN expr = expression COMMA separator = expression RPAREN (
        WITHIN GROUP LPAREN order_by_clause RPAREN
    )? # STRINGAGG
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/string-escape-transact-sql?view=sql-server-ver16
    | STRING_ESCAPE LPAREN text_ = expression COMMA type_ = expression RPAREN # STRING_ESCAPE
    // https://msdn.microsoft.com/fr-fr/library/ms188043.aspx
    | STUFF LPAREN str = expression COMMA from = expression COMMA to = expression COMMA str_with = expression RPAREN # STUFF
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/substring-transact-sql?view=sql-server-ver16
    | SUBSTRING LPAREN string_expression = expression COMMA start_ = expression COMMA length = expression RPAREN # SUBSTRING
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/translate-transact-sql?view=sql-server-ver16
    | TRANSLATE LPAREN inputString = expression COMMA characters = expression COMMA translations = expression RPAREN # TRANSLATE
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/trim-transact-sql?view=sql-server-ver16
    | TRIM LPAREN (characters = expression FROM)? string_ = expression RPAREN # TRIM
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/unicode-transact-sql?view=sql-server-ver16
    | UNICODE LPAREN ncharacter_expression = expression RPAREN # UNICODE
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/upper-transact-sql?view=sql-server-ver16
    | UPPER LPAREN character_expression = expression RPAREN # UPPER
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
    | FORMATMESSAGE LPAREN (msg_number = INT | msg_string = STRING | msg_variable = LOCAL_ID) COMMA expression (
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
    | CAST LPAREN expression AS data_type RPAREN     # CAST
    | TRY_CAST LPAREN expression AS data_type RPAREN # TRY_CAST
    | CONVERT LPAREN convert_data_type = data_type COMMA convert_expression = expression (
        COMMA style = expression
    )? RPAREN # CONVERT
    // https://msdn.microsoft.com/en-us/library/ms190349.aspx
    | COALESCE LPAREN expression_list_ RPAREN # COALESCE
    // Cursor functions
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/cursor-rows-transact-sql?view=sql-server-ver16
    | CURSOR_ROWS # CURSOR_ROWS
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/cursor-rows-transact-sql?view=sql-server-ver16
    | FETCH_STATUS # FETCH_STATUS
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/cursor-status-transact-sql?view=sql-server-ver16
    | CURSOR_STATUS LPAREN scope = STRING COMMA cursor = expression RPAREN # CURSOR_STATUS
    // Cryptographic functions
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/cert-id-transact-sql?view=sql-server-ver16
    | CERT_ID LPAREN cert_name = expression RPAREN # CERT_ID
    // Data type functions
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/datalength-transact-sql?view=sql-server-ver16
    | DATALENGTH LPAREN expression RPAREN # DATALENGTH
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/ident-current-transact-sql?view=sql-server-ver16
    | IDENT_CURRENT LPAREN table_or_view = expression RPAREN # IDENT_CURRENT
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/ident-incr-transact-sql?view=sql-server-ver16
    | IDENT_INCR LPAREN table_or_view = expression RPAREN # IDENT_INCR
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/ident-seed-transact-sql?view=sql-server-ver16
    | IDENT_SEED LPAREN table_or_view = expression RPAREN # IDENT_SEED
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/ident-seed-transact-sql?view=sql-server-ver16
    | IDENTITY LPAREN datatype = data_type (COMMA seed = INT COMMA increment = INT)? RPAREN # IDENTITY
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
    | DATEDIFF LPAREN datepart = dateparts_12 COMMA date_first = expression COMMA date_second = expression RPAREN # DATEDIFF
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
        seconds = expression COMMA fractions = expression COMMA hour_offset = expression COMMA minute_offset = expression COMMA precision = INT RPAREN #
        DATETIMEOFFSETFROMPARTS
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/datetrunc-transact-sql?view=sql-server-ver16
    | DATETRUNC LPAREN datepart = dateparts_datetrunc COMMA date = expression RPAREN # DATETRUNC
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/day-transact-sql?view=sql-server-ver16
    | DAY LPAREN date = expression RPAREN # DAY
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/eomonth-transact-sql?view=sql-server-ver16
    | EOMONTH LPAREN start_date = expression (COMMA month_to_add = expression)? RPAREN # EOMONTH
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
    | SWITCHOFFSET LPAREN datetimeoffset_expression = expression COMMA timezoneoffset_expression = expression RPAREN # SWITCHOFFSET
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
    | TODATETIMEOFFSET LPAREN datetime_expression = expression COMMA timezoneoffset_expression = expression RPAREN # TODATETIMEOFFSET
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/year-transact-sql?view=sql-server-ver16
    | YEAR LPAREN date = expression RPAREN # YEAR
    // https://msdn.microsoft.com/en-us/library/ms189838.aspx
    | IDENTITY LPAREN data_type (COMMA seed = INT)? (COMMA increment = INT)? RPAREN # IDENTITY
    // https://msdn.microsoft.com/en-us/library/bb839514.aspx
    | MIN_ACTIVE_ROWVERSION LPAREN RPAREN # MIN_ACTIVE_ROWVERSION
    // https://msdn.microsoft.com/en-us/library/ms177562.aspx
    | NULLIF LPAREN left = expression COMMA right = expression RPAREN # NULLIF
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/parse-transact-sql
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/try-parse-transact-sql
    | PARSE LPAREN str = expression AS data_type (USING culture = expression)? RPAREN # PARSE
    // https://docs.microsoft.com/en-us/sql/t-sql/xml/xml-data-type-methods
    | xml_data_type_methods # XML_DATA_TYPE_FUNC
    // https://docs.microsoft.com/en-us/sql/t-sql/functions/logical-functions-iif-transact-sql
    | IIF LPAREN cond = search_condition COMMA left = expression COMMA right = expression RPAREN # IIF
    // JSON functions
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/isjson-transact-sql?view=azure-sqldw-latest
    | ISJSON LPAREN json_expr = expression (COMMA json_type_constraint = expression)? RPAREN # ISJSON
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/json-object-transact-sql?view=azure-sqldw-latest
    | JSON_OBJECT LPAREN (key_value = json_key_value (COMMA key_value = json_key_value)*)? json_null_clause? RPAREN # JSON_OBJECT
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/json-array-transact-sql?view=azure-sqldw-latest
    | JSON_ARRAY LPAREN expression_list_? json_null_clause? RPAREN # JSON_ARRAY
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/json-value-transact-sql?view=azure-sqldw-latest
    | JSON_VALUE LPAREN expr = expression COMMA path = expression RPAREN # JSON_VALUE
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/json-query-transact-sql?view=azure-sqldw-latest
    | JSON_QUERY LPAREN expr = expression (COMMA path = expression)? RPAREN # JSON_QUERY
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/json-modify-transact-sql?view=azure-sqldw-latest
    | JSON_MODIFY LPAREN expr = expression COMMA path = expression COMMA new_value = expression RPAREN # JSON_MODIFY
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/json-path-exists-transact-sql?view=azure-sqldw-latest
    | JSON_PATH_EXISTS LPAREN value_expression = expression COMMA sql_json_path = expression RPAREN # JSON_PATH_EXISTS
    // Math functions
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/abs-transact-sql?view=sql-server-ver16
    | ABS LPAREN numeric_expression = expression RPAREN # ABS
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/acos-transact-sql?view=sql-server-ver16
    | ACOS LPAREN float_expression = expression RPAREN # ACOS
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/asin-transact-sql?view=sql-server-ver16
    | ASIN LPAREN float_expression = expression RPAREN # ASIN
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/atan-transact-sql?view=sql-server-ver16
    | ATAN LPAREN float_expression = expression RPAREN # ATAN
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/atn2-transact-sql?view=sql-server-ver16
    | ATN2 LPAREN float_expression = expression COMMA float_expression = expression RPAREN # ATN2
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/ceiling-transact-sql?view=sql-server-ver16
    | CEILING LPAREN numeric_expression = expression RPAREN # CEILING
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/cos-transact-sql?view=sql-server-ver16
    | COS LPAREN float_expression = expression RPAREN # COS
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/cot-transact-sql?view=sql-server-ver16
    | COT LPAREN float_expression = expression RPAREN # COT
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/degrees-transact-sql?view=sql-server-ver16
    | DEGREES LPAREN numeric_expression = expression RPAREN # DEGREES
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/exp-transact-sql?view=sql-server-ver16
    | EXP LPAREN float_expression = expression RPAREN # EXP
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/floor-transact-sql?view=sql-server-ver16
    | FLOOR LPAREN numeric_expression = expression RPAREN # FLOOR
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/log-transact-sql?view=sql-server-ver16
    | LOG LPAREN float_expression = expression (COMMA base = expression)? RPAREN # LOG
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/log10-transact-sql?view=sql-server-ver16
    | LOG10 LPAREN float_expression = expression RPAREN # LOG10
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/pi-transact-sql?view=sql-server-ver16
    | PI LPAREN RPAREN # PI
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/power-transact-sql?view=sql-server-ver16
    | POWER LPAREN float_expression = expression COMMA y = expression RPAREN # POWER
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/radians-transact-sql?view=sql-server-ver16
    | RADIANS LPAREN numeric_expression = expression RPAREN # RADIANS
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/rand-transact-sql?view=sql-server-ver16
    | RAND LPAREN (seed = expression)? RPAREN # RAND
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/round-transact-sql?view=sql-server-ver16
    | ROUND LPAREN numeric_expression = expression COMMA length = expression (COMMA function = expression)? RPAREN # ROUND
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/sign-transact-sql?view=sql-server-ver16
    | SIGN LPAREN numeric_expression = expression RPAREN # MATH_SIGN
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/sin-transact-sql?view=sql-server-ver16
    | SIN LPAREN float_expression = expression RPAREN # SIN
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/sqrt-transact-sql?view=sql-server-ver16
    | SQRT LPAREN float_expression = expression RPAREN # SQRT
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/square-transact-sql?view=sql-server-ver16
    | SQUARE LPAREN float_expression = expression RPAREN # SQUARE
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/tan-transact-sql?view=sql-server-ver16
    | TAN LPAREN float_expression = expression RPAREN # TAN
    // Logical functions
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/logical-functions-greatest-transact-sql?view=azure-sqldw-latest
    | GREATEST LPAREN expression_list_ RPAREN # GREATEST
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/logical-functions-least-transact-sql?view=azure-sqldw-latest
    | LEAST LPAREN expression_list_ RPAREN # LEAST
    // Security functions
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/certencoded-transact-sql?view=sql-server-ver16
    | CERTENCODED LPAREN certid = expression RPAREN # CERTENCODED
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/certprivatekey-transact-sql?view=sql-server-ver16
    | CERTPRIVATEKEY LPAREN certid = expression COMMA encryption_password = expression (
        COMMA decryption_pasword = expression
    )? RPAREN # CERTPRIVATEKEY
    // https://msdn.microsoft.com/en-us/library/ms176050.aspx
    | CURRENT_USER # CURRENT_USER
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/database-principal-id-transact-sql?view=sql-server-ver16
    | DATABASE_PRINCIPAL_ID LPAREN (principal_name = expression)? RPAREN # DATABASE_PRINCIPAL_ID
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/has-dbaccess-transact-sql?view=sql-server-ver16
    | HAS_DBACCESS LPAREN database_name = expression RPAREN # HAS_DBACCESS
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/has-perms-by-name-transact-sql?view=sql-server-ver16
    | HAS_PERMS_BY_NAME LPAREN securable = expression COMMA securable_class = expression COMMA permission = expression (
        COMMA sub_securable = expression (COMMA sub_securable_class = expression)?
    )? RPAREN # HAS_PERMS_BY_NAME
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/is-member-transact-sql?view=sql-server-ver16
    | IS_MEMBER LPAREN group_or_role = expression RPAREN # IS_MEMBER
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/is-rolemember-transact-sql?view=sql-server-ver16
    | IS_ROLEMEMBER LPAREN role = expression (COMMA database_principal = expression)? RPAREN # IS_ROLEMEMBER
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/is-srvrolemember-transact-sql?view=sql-server-ver16
    | IS_SRVROLEMEMBER LPAREN role = expression (COMMA login = expression)? RPAREN # IS_SRVROLEMEMBER
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/loginproperty-transact-sql?view=sql-server-ver16
    | LOGINPROPERTY LPAREN login_name = expression COMMA property_name = expression RPAREN # LOGINPROPERTY
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/original-login-transact-sql?view=sql-server-ver16
    | ORIGINAL_LOGIN LPAREN RPAREN # ORIGINAL_LOGIN
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/permissions-transact-sql?view=sql-server-ver16
    | PERMISSIONS LPAREN (object_id = expression (COMMA column = expression)?)? RPAREN # PERMISSIONS
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/pwdencrypt-transact-sql?view=sql-server-ver16
    | PWDENCRYPT LPAREN password = expression RPAREN # PWDENCRYPT
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/pwdcompare-transact-sql?view=sql-server-ver16
    | PWDCOMPARE LPAREN clear_text_password = expression COMMA password_hash = expression (
        COMMA version = expression
    )? RPAREN # PWDCOMPARE
    // https://msdn.microsoft.com/en-us/library/ms177587.aspx
    | SESSION_USER # SESSION_USER
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/sessionproperty-transact-sql?view=sql-server-ver16
    | SESSIONPROPERTY LPAREN option_name = expression RPAREN # SESSIONPROPERTY
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/suser-id-transact-sql?view=sql-server-ver16
    | SUSER_ID LPAREN (login = expression)? RPAREN # SUSER_ID
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/suser-name-transact-sql?view=sql-server-ver16
    | SUSER_NAME LPAREN (server_user_sid = expression)? RPAREN # SUSER_SNAME
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/suser-sid-transact-sql?view=sql-server-ver16
    | SUSER_SID LPAREN (login = expression (COMMA param2 = expression)?)? RPAREN # SUSER_SID
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/suser-sname-transact-sql?view=sql-server-ver16
    | SUSER_SNAME LPAREN (server_user_sid = expression)? RPAREN # SUSER_SNAME
    // https://msdn.microsoft.com/en-us/library/ms179930.aspx
    | SYSTEM_USER # SYSTEM_USER
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/user-transact-sql?view=sql-server-ver16
    | USER # USER
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/user-id-transact-sql?view=sql-server-ver16
    | USER_ID LPAREN (user = expression)? RPAREN # USER_ID
    // https://learn.microsoft.com/en-us/sql/t-sql/functions/user-name-transact-sql?view=sql-server-ver16
    | USER_NAME LPAREN (id = expression)? RPAREN # USER_NAME
    ;

xml_data_type_methods
    : value_method
    | query_method
    | exist_method
    | modify_method
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
dateparts_datetrunc
    : dateparts_9
    | DAYOFYEAR
    | DAYOFYEAR_ABBR
    | MICROSECOND
    | MICROSECOND_ABBR
    | ISO_WEEK
    | ISO_WEEK_ABBR
    ;

value_method
    : (
        loc_id = LOCAL_ID
        | value_id = full_column_name
        | eventdata = EVENTDATA LPAREN RPAREN
        | query = query_method
        | LPAREN subquery RPAREN
    ) DOT call = value_call
    ;

value_call
    : (VALUE | VALUE_SQUARE_BRACKET) LPAREN xquery = STRING COMMA sqltype = STRING RPAREN
    ;

query_method
    : (loc_id = LOCAL_ID | value_id = full_column_name | LPAREN subquery RPAREN) DOT call = query_call
    ;

query_call
    : (QUERY | QUERY_SQUARE_BRACKET) LPAREN xquery = STRING RPAREN
    ;

exist_method
    : (loc_id = LOCAL_ID | value_id = full_column_name | LPAREN subquery RPAREN) DOT call = exist_call
    ;

exist_call
    : (EXIST | EXIST_SQUARE_BRACKET) LPAREN xquery = STRING RPAREN
    ;

modify_method
    : (loc_id = LOCAL_ID | value_id = full_column_name | LPAREN subquery RPAREN) DOT call = modify_call
    ;

modify_call
    : (MODIFY | MODIFY_SQUARE_BRACKET) LPAREN xml_dml = STRING RPAREN
    ;

hierarchyid_call
    : GETANCESTOR LPAREN n = expression RPAREN
    | GETDESCENDANT LPAREN child1 = expression COMMA child2 = expression RPAREN
    | GETLEVEL LPAREN RPAREN
    | ISDESCENDANTOF LPAREN parent_ = expression RPAREN
    | GETREPARENTEDVALUE LPAREN oldroot = expression COMMA newroot = expression RPAREN
    | TOSTRING LPAREN RPAREN
    ;

hierarchyid_static_method
    : HIERARCHYID DOUBLE_COLON (GETROOT LPAREN RPAREN | PARSE LPAREN input = expression RPAREN)
    ;

nodes_method
    : (loc_id = LOCAL_ID | value_id = full_column_name | LPAREN subquery RPAREN) DOT NODES LPAREN xquery = STRING RPAREN
    ;

switch_section
    : WHEN expression THEN expression
    ;

switch_search_condition_section
    : WHEN search_condition THEN expression
    ;

as_column_alias
    : AS? column_alias
    ;

as_table_alias
    : AS? table_alias
    ;

table_alias
    : id_
    ;

// https://msdn.microsoft.com/en-us/library/ms187373.aspx
with_table_hints
    : WITH LPAREN hint += table_hint (COMMA? hint += table_hint)* RPAREN
    ;

deprecated_table_hint
    : LPAREN table_hint RPAREN
    ;

// https://infocenter-archive.sybase.com/help/index.jsp?topic=/com.sybase.infocenter.dc00938.1502/html/locking/locking103.htm
// https://infocenter-archive.sybase.com/help/index.jsp?topic=/com.sybase.dc32300_1250/html/sqlug/sqlug792.htm
// https://infocenter-archive.sybase.com/help/index.jsp?topic=/com.sybase.dc36271_36272_36273_36274_1250/html/refman/X35229.htm
// Legacy hint with no parenthesis and no WITH keyword. Actually conflicts with table alias name except for holdlock which is
// a reserved keyword in this grammar. We might want a separate sybase grammar variant.
sybase_legacy_hints
    : sybase_legacy_hint+
    ;

sybase_legacy_hint
    : HOLDLOCK
    | NOHOLDLOCK
    | READPAST
    | SHARED
    ;

// For simplicity, we don't build subsets for INSERT/UPDATE/DELETE/SELECT/MERGE
// which means the grammar accept slightly more than the what the specification (documentation) says.
table_hint
    : NOEXPAND
    | INDEX (
        LPAREN index_value (COMMA index_value)* RPAREN
        | EQ LPAREN index_value RPAREN
        | EQ index_value // examples in the doc include this syntax
    )
    | FORCESEEK ( LPAREN index_value LPAREN column_name_list RPAREN RPAREN)?
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

index_value
    : id_
    | INT
    ;

column_alias_list
    : LPAREN alias += column_alias (COMMA alias += column_alias)* RPAREN
    ;

column_alias
    : id_
    | STRING
    ;

table_value_constructor
    : VALUES LPAREN exps += expression_list_ RPAREN (COMMA LPAREN exps += expression_list_ RPAREN)*
    ;

expression_list_
    : exp += expression (COMMA exp += expression)*
    ;

// https://msdn.microsoft.com/en-us/library/ms189798.aspx
ranking_windowed_function
    : (RANK | DENSE_RANK | ROW_NUMBER) LPAREN RPAREN over_clause
    | NTILE LPAREN expression RPAREN over_clause
    ;

// https://msdn.microsoft.com/en-us/library/ms173454.aspx
aggregate_windowed_function
    : agg_func = (AVG | MAX | MIN | SUM | STDEV | STDEVP | VAR | VARP) LPAREN all_distinct_expression RPAREN over_clause?
    | cnt = (COUNT | COUNT_BIG) LPAREN (STAR | all_distinct_expression) RPAREN over_clause?
    | CHECKSUM_AGG LPAREN all_distinct_expression RPAREN
    | GROUPING LPAREN expression RPAREN
    | GROUPING_ID LPAREN expression_list_ RPAREN
    ;

// https://docs.microsoft.com/en-us/sql/t-sql/functions/analytic-functions-transact-sql
analytic_windowed_function
    : (FIRST_VALUE | LAST_VALUE) LPAREN expression RPAREN over_clause
    | (LAG | LEAD) LPAREN expression (COMMA expression (COMMA expression)?)? RPAREN over_clause
    | (CUME_DIST | PERCENT_RANK) LPAREN RPAREN OVER LPAREN (PARTITION BY expression_list_)? order_by_clause RPAREN
    | (PERCENTILE_CONT | PERCENTILE_DISC) LPAREN expression RPAREN WITHIN GROUP LPAREN order_by_clause RPAREN OVER LPAREN (
        PARTITION BY expression_list_
    )? RPAREN
    ;

all_distinct_expression
    : (ALL | DISTINCT)? expression
    ;

// https://msdn.microsoft.com/en-us/library/ms189461.aspx
over_clause
    : OVER LPAREN (PARTITION BY expression_list_)? order_by_clause? row_or_range_clause? RPAREN
    ;

row_or_range_clause
    : (ROWS | RANGE) window_frame_extent
    ;

window_frame_extent
    : window_frame_preceding
    | BETWEEN window_frame_bound AND window_frame_bound
    ;

window_frame_bound
    : window_frame_preceding
    | window_frame_following
    ;

window_frame_preceding
    : UNBOUNDED PRECEDING
    | INT PRECEDING
    | CURRENT ROW
    ;

window_frame_following
    : UNBOUNDED FOLLOWING
    | INT FOLLOWING
    ;

create_database_option
    : FILESTREAM (database_filestream_option (COMMA database_filestream_option)*)
    | DEFAULT_LANGUAGE EQ ( id_ | STRING)
    | DEFAULT_FULLTEXT_LANGUAGE EQ ( id_ | STRING)
    | NESTED_TRIGGERS EQ ( OFF | ON)
    | TRANSFORM_NOISE_WORDS EQ ( OFF | ON)
    | TWO_DIGIT_YEAR_CUTOFF EQ INT
    | DB_CHAINING ( OFF | ON)
    | TRUSTWORTHY ( OFF | ON)
    ;

database_filestream_option
    : LPAREN (
        ( NON_TRANSACTED_ACCESS EQ ( OFF | READ_ONLY | FULL))
        | ( DIRECTORY_NAME EQ STRING)
    ) RPAREN
    ;

database_file_spec
    : file_group
    | file_spec
    ;

file_group
    : FILEGROUP id_ (CONTAINS FILESTREAM)? (DEFAULT)? (CONTAINS MEMORY_OPTIMIZED_DATA)? file_spec (
        COMMA file_spec
    )*
    ;

file_spec
    : LPAREN NAME EQ (id_ | STRING) COMMA? FILENAME EQ file = STRING COMMA? (
        SIZE EQ file_size COMMA?
    )? (MAXSIZE EQ (file_size | UNLIMITED) COMMA?)? (FILEGROWTH EQ file_size COMMA?)? RPAREN
    ;

// Primitive.
entity_name
    : (
        server = id_ DOT database = id_ DOT schema = id_ DOT
        | database = id_ DOT (schema = id_)? DOT
        | schema = id_ DOT
    )? table = id_
    ;

entity_name_for_azure_dw
    : schema = id_
    | schema = id_ DOT object_name = id_
    ;

entity_name_for_parallel_dw
    : schema_database = id_
    | schema = id_ DOT object_name = id_
    ;

full_table_name
    : (
        linkedServer = id_ DOT DOT schema = id_ DOT
        | server = id_ DOT database = id_ DOT schema = id_ DOT
        | database = id_ DOT schema = id_? DOT
        | schema = id_ DOT
    )? table = id_
    ;

table_name
    : (database = id_ DOT schema = id_? DOT | schema = id_ DOT)? (
        table = id_
        | blocking_hierarchy = BLOCKING_HIERARCHY
    )
    ;

simple_name
    : (schema = id_ DOT)? name = id_
    ;

func_proc_name_schema
    : ((schema = id_) DOT)? procedure = id_
    ;

func_proc_name_database_schema
    : database = id_? DOT schema = id_? DOT procedure = id_
    | func_proc_name_schema
    ;

func_proc_name_server_database_schema
    : server = id_? DOT database = id_? DOT schema = id_? DOT procedure = id_
    | func_proc_name_database_schema
    ;

ddl_object
    : full_table_name
    | LOCAL_ID
    ;

full_column_name
    : ((DELETED | INSERTED | full_table_name) DOT)? (
        column_name = id_
        | (DOLLAR (IDENTITY | ROWGUID))
    )
    ;

column_name_list_with_order
    : id_ (ASC | DESC)? (COMMA id_ (ASC | DESC)?)*
    ;

//For some reason, sql server allows any number of prefixes:  Here, h is the column: a.b.c.d.e.f.g.h
insert_column_name_list
    : col += insert_column_id (COMMA col += insert_column_id)*
    ;

insert_column_id
    : (ignore += id_? DOT)* id_
    ;

column_name_list
    : col += id_ (COMMA col += id_)*
    ;

cursor_name
    : id_
    | LOCAL_ID
    ;

on_off
    : ON
    | OFF
    ;

clustered
    : CLUSTERED
    | NONCLUSTERED
    ;

null_notnull
    : NOT? NULL_
    ;

scalar_function_name
    : func_proc_name_server_database_schema
    | RIGHT
    | LEFT
    | BINARY_CHECKSUM
    | CHECKSUM
    ;

begin_conversation_timer
    : BEGIN CONVERSATION TIMER LPAREN LOCAL_ID RPAREN TIMEOUT EQ time SEMI?
    ;

begin_conversation_dialog
    : BEGIN DIALOG (CONVERSATION)? dialog_handle = LOCAL_ID FROM SERVICE initiator_service_name = service_name TO SERVICE target_service_name =
        service_name (COMMA service_broker_guid = STRING)? ON CONTRACT contract_name (
        WITH ((RELATED_CONVERSATION | RELATED_CONVERSATION_GROUP) EQ LOCAL_ID COMMA?)? (
            LIFETIME EQ (INT | LOCAL_ID) COMMA?
        )? (ENCRYPTION EQ on_off)?
    )? SEMI?
    ;

contract_name
    : (id_ | expression)
    ;

service_name
    : (id_ | expression)
    ;

end_conversation
    : END CONVERSATION conversation_handle = LOCAL_ID SEMI? (
        WITH (
            ERROR EQ faliure_code = (LOCAL_ID | STRING) DESCRIPTION EQ failure_text = (
                LOCAL_ID
                | STRING
            )
        )? CLEANUP?
    )?
    ;

waitfor_conversation
    : WAITFOR? LPAREN get_conversation RPAREN (COMMA? TIMEOUT timeout = time)? SEMI?
    ;

get_conversation
    : GET CONVERSATION GROUP conversation_group_id = (STRING | LOCAL_ID) FROM queue = queue_id SEMI?
    ;

queue_id
    : (database_name = id_ DOT schema_name = id_ DOT name = id_)
    | id_
    ;

send_conversation
    : SEND ON CONVERSATION conversation_handle = (STRING | LOCAL_ID) MESSAGE TYPE message_type_name = expression (
        LPAREN message_body_expression = (STRING | LOCAL_ID) RPAREN
    )? SEMI?
    ;

// https://msdn.microsoft.com/en-us/library/ms187752.aspx
// TODO: implement runtime check or add new tokens.

data_type
    : scaled = (VARCHAR | NVARCHAR | BINARY_KEYWORD | VARBINARY_KEYWORD | SQUARE_BRACKET_ID) LPAREN MAX RPAREN
    | ext_type = id_ LPAREN scale = INT COMMA prec = INT RPAREN
    | ext_type = id_ LPAREN scale = INT RPAREN
    | ext_type = id_ IDENTITY (LPAREN seed = INT COMMA inc = INT RPAREN)?
    | double_prec = DOUBLE PRECISION?
    | unscaled_type = id_
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
primitive_constant
    : STRING // string, datetime or uniqueidentifier
    | HEX
    | (INT | REAL | FLOAT)                    // float or decimal
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
    | DOUBLE_QUOTE_BLANK
    | SQUARE_BRACKET_ID
    | keyword
    | RAW
    ;

simple_id
    : ID
    ;

id_or_string
    : id_
    | STRING
    ;

// https://msdn.microsoft.com/en-us/library/ms188074.aspx
// Spaces are allowed for comparison operators.
comparison_operator
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

assignment_operator
    : PE
    | ME
    | SE
    | DE
    | MEA
    | AND_ASSIGN
    | XOR_ASSIGN
    | OR_ASSIGN
    ;

file_size
    : INT (KB | MB | GB | TB | MOD)?
    ;