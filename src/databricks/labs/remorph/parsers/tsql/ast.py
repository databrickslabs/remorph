import functools

from dataclasses import dataclass
from databricks.labs.remorph.parsers.base import TreeNode

dataclass = functools.partial(dataclass, slots=True, match_args=True, repr=False, frozen=True)

@dataclass
class TsqlFile(TreeNode):
    batch: list["Batch"] = None
    eof: str = None
    execute_body_batch: "ExecuteBodyBatch" = None
    go_statement: list["GoStatement"] = None


@dataclass
class Batch(TreeNode):
    go_statement: "GoStatement" = None
    execute_body_batch: list["ExecuteBodyBatch"] = None
    sql_clauses: "SqlClauses" = None
    right: list["GoStatement"] = None
    batch_level_statement: "BatchLevelStatement" = None


@dataclass
class BatchLevelStatement(TreeNode):
    create_or_alter_function: "CreateOrAlterFunction" = None
    create_or_alter_procedure: "CreateOrAlterProcedure" = None
    create_or_alter_trigger: "CreateOrAlterTrigger" = None
    create_view: "CreateView" = None


@dataclass
class SqlClauses(TreeNode):
    dml_clause: "DmlClause" = None
    cfl_statement: "CflStatement" = None
    another_statement: "AnotherStatement" = None
    ddl_clause: "DdlClause" = None
    dbcc_clause: "DbccClause" = None
    backup_statement: "BackupStatement" = None
    semi: bool = False


@dataclass
class DmlClause(TreeNode):
    merge_statement: "MergeStatement" = None
    delete_statement: "DeleteStatement" = None
    insert_statement: "InsertStatement" = None
    select_statement_standalone: "SelectStatementStandalone" = None
    update_statement: "UpdateStatement" = None


@dataclass
class DdlClause(TreeNode):
    alter_application_role: "AlterApplicationRole" = None
    alter_assembly: "AlterAssembly" = None
    alter_asymmetric_key: "AlterAsymmetricKey" = None
    alter_authorization: "AlterAuthorization" = None
    alter_authorization_for_azure_dw: "AlterAuthorizationForAzureDw" = None
    alter_authorization_for_parallel_dw: "AlterAuthorizationForParallelDw" = None
    alter_authorization_for_sql_database: "AlterAuthorizationForSqlDatabase" = None
    alter_availability_group: "AlterAvailabilityGroup" = None
    alter_certificate: "AlterCertificate" = None
    alter_column_encryption_key: "AlterColumnEncryptionKey" = None
    alter_credential: "AlterCredential" = None
    alter_cryptographic_provider: "AlterCryptographicProvider" = None
    alter_database: "AlterDatabase" = None
    alter_database_audit_specification: "AlterDatabaseAuditSpecification" = None
    alter_db_role: "AlterDbRole" = None
    alter_endpoint: "AlterEndpoint" = None
    alter_external_data_source: "AlterExternalDataSource" = None
    alter_external_library: "AlterExternalLibrary" = None
    alter_external_resource_pool: "AlterExternalResourcePool" = None
    alter_fulltext_catalog: "AlterFulltextCatalog" = None
    alter_fulltext_stoplist: "AlterFulltextStoplist" = None
    alter_index: "AlterIndex" = None
    alter_login_azure_sql: "AlterLoginAzureSql" = None
    alter_login_azure_sql_dw_and_pdw: "AlterLoginAzureSqlDwAndPdw" = None
    alter_login_sql_server: "AlterLoginSqlServer" = None
    alter_master_key_azure_sql: "AlterMasterKeyAzureSql" = None
    alter_master_key_sql_server: "AlterMasterKeySqlServer" = None
    alter_message_type: "AlterMessageType" = None
    alter_partition_function: "AlterPartitionFunction" = None
    alter_partition_scheme: "AlterPartitionScheme" = None
    alter_remote_service_binding: "AlterRemoteServiceBinding" = None
    alter_resource_governor: "AlterResourceGovernor" = None
    alter_schema_azure_sql_dw_and_pdw: "AlterSchemaAzureSqlDwAndPdw" = None
    alter_schema_sql: "AlterSchemaSql" = None
    alter_sequence: "AlterSequence" = None
    alter_server_audit: "AlterServerAudit" = None
    alter_server_audit_specification: "AlterServerAuditSpecification" = None
    alter_server_configuration: "AlterServerConfiguration" = None
    alter_server_role: "AlterServerRole" = None
    alter_server_role_pdw: "AlterServerRolePdw" = None
    alter_service: "AlterService" = None
    alter_service_master_key: "AlterServiceMasterKey" = None
    alter_symmetric_key: "AlterSymmetricKey" = None
    alter_table: "AlterTable" = None
    alter_user: "AlterUser" = None
    alter_user_azure_sql: "AlterUserAzureSql" = None
    alter_workload_group: "AlterWorkloadGroup" = None
    alter_xml_schema_collection: "AlterXmlSchemaCollection" = None
    create_application_role: "CreateApplicationRole" = None
    create_assembly: "CreateAssembly" = None
    create_asymmetric_key: "CreateAsymmetricKey" = None
    create_column_encryption_key: "CreateColumnEncryptionKey" = None
    create_column_master_key: "CreateColumnMasterKey" = None
    create_columnstore_index: "CreateColumnstoreIndex" = None
    create_credential: "CreateCredential" = None
    create_cryptographic_provider: "CreateCryptographicProvider" = None
    create_database: "CreateDatabase" = None
    create_database_audit_specification: "CreateDatabaseAuditSpecification" = None
    create_db_role: "CreateDbRole" = None
    create_endpoint: "CreateEndpoint" = None
    create_event_notification: "CreateEventNotification" = None
    create_external_library: "CreateExternalLibrary" = None
    create_external_resource_pool: "CreateExternalResourcePool" = None
    create_fulltext_catalog: "CreateFulltextCatalog" = None
    create_fulltext_stoplist: "CreateFulltextStoplist" = None
    create_index: "CreateIndex" = None
    create_login_azure_sql: "CreateLoginAzureSql" = None
    create_login_pdw: "CreateLoginPdw" = None
    create_login_sql_server: "CreateLoginSqlServer" = None
    create_master_key_azure_sql: "CreateMasterKeyAzureSql" = None
    create_master_key_sql_server: "CreateMasterKeySqlServer" = None
    create_nonclustered_columnstore_index: "CreateNonclusteredColumnstoreIndex" = None
    create_or_alter_broker_priority: "CreateOrAlterBrokerPriority" = None
    create_or_alter_event_session: "CreateOrAlterEventSession" = None
    create_partition_function: "CreatePartitionFunction" = None
    create_partition_scheme: "CreatePartitionScheme" = None
    create_remote_service_binding: "CreateRemoteServiceBinding" = None
    create_resource_pool: "CreateResourcePool" = None
    create_route: "CreateRoute" = None
    create_rule: "CreateRule" = None
    create_schema: "CreateSchema" = None
    create_schema_azure_sql_dw_and_pdw: "CreateSchemaAzureSqlDwAndPdw" = None
    create_search_property_list: "CreateSearchPropertyList" = None
    create_security_policy: "CreateSecurityPolicy" = None
    create_sequence: "CreateSequence" = None
    create_server_audit: "CreateServerAudit" = None
    create_server_audit_specification: "CreateServerAuditSpecification" = None
    create_server_role: "CreateServerRole" = None
    create_service: "CreateService" = None
    create_statistics: "CreateStatistics" = None
    create_synonym: "CreateSynonym" = None
    create_table: "CreateTable" = None
    create_type: "CreateType" = None
    create_user: "CreateUser" = None
    create_user_azure_sql_dw: "CreateUserAzureSqlDw" = None
    create_workload_group: "CreateWorkloadGroup" = None
    create_xml_index: "CreateXmlIndex" = None
    create_xml_schema_collection: "CreateXmlSchemaCollection" = None
    disable_trigger: "DisableTrigger" = None
    drop_aggregate: "DropAggregate" = None
    drop_application_role: "DropApplicationRole" = None
    drop_assembly: "DropAssembly" = None
    drop_asymmetric_key: "DropAsymmetricKey" = None
    drop_availability_group: "DropAvailabilityGroup" = None
    drop_broker_priority: "DropBrokerPriority" = None
    drop_certificate: "DropCertificate" = None
    drop_column_encryption_key: "DropColumnEncryptionKey" = None
    drop_column_master_key: "DropColumnMasterKey" = None
    drop_contract: "DropContract" = None
    drop_credential: "DropCredential" = None
    drop_cryptograhic_provider: "DropCryptograhicProvider" = None
    drop_database: "DropDatabase" = None
    drop_database_audit_specification: "DropDatabaseAuditSpecification" = None
    drop_database_scoped_credential: "DropDatabaseScopedCredential" = None
    drop_db_role: "DropDbRole" = None
    drop_default: "DropDefault" = None
    drop_endpoint: "DropEndpoint" = None
    drop_event_notifications: "DropEventNotifications" = None
    drop_event_session: "DropEventSession" = None
    drop_external_data_source: "DropExternalDataSource" = None
    drop_external_file_format: "DropExternalFileFormat" = None
    drop_external_library: "DropExternalLibrary" = None
    drop_external_resource_pool: "DropExternalResourcePool" = None
    drop_external_table: "DropExternalTable" = None
    drop_fulltext_catalog: "DropFulltextCatalog" = None
    drop_fulltext_index: "DropFulltextIndex" = None
    drop_fulltext_stoplist: "DropFulltextStoplist" = None
    drop_function: "DropFunction" = None
    drop_index: "DropIndex" = None
    drop_login: "DropLogin" = None
    drop_message_type: "DropMessageType" = None
    drop_partition_function: "DropPartitionFunction" = None
    drop_partition_scheme: "DropPartitionScheme" = None
    drop_procedure: "DropProcedure" = None
    drop_queue: "DropQueue" = None
    drop_remote_service_binding: "DropRemoteServiceBinding" = None
    drop_resource_pool: "DropResourcePool" = None
    drop_route: "DropRoute" = None
    drop_rule: "DropRule" = None
    drop_schema: "DropSchema" = None
    drop_search_property_list: "DropSearchPropertyList" = None
    drop_security_policy: "DropSecurityPolicy" = None
    drop_sequence: "DropSequence" = None
    drop_server_audit: "DropServerAudit" = None
    drop_server_audit_specification: "DropServerAuditSpecification" = None
    drop_server_role: "DropServerRole" = None
    drop_service: "DropService" = None
    drop_signature: "DropSignature" = None
    drop_statistics: "DropStatistics" = None
    drop_statistics_name_azure_dw_and_pdw: "DropStatisticsNameAzureDwAndPdw" = None
    drop_symmetric_key: "DropSymmetricKey" = None
    drop_synonym: "DropSynonym" = None
    drop_table: "DropTable" = None
    drop_trigger: "DropTrigger" = None
    drop_type: "DropType" = None
    drop_user: "DropUser" = None
    drop_view: "DropView" = None
    drop_workload_group: "DropWorkloadGroup" = None
    drop_xml_schema_collection: "DropXmlSchemaCollection" = None
    enable_trigger: "EnableTrigger" = None
    lock_table: "LockTable" = None
    truncate_table: "TruncateTable" = None
    update_statistics: "UpdateStatistics" = None


@dataclass
class BackupStatement(TreeNode):
    backup_database: "BackupDatabase" = None
    backup_log: "BackupLog" = None
    backup_certificate: "BackupCertificate" = None
    backup_master_key: "BackupMasterKey" = None
    backup_service_master_key: "BackupServiceMasterKey" = None


@dataclass
class CflStatement(TreeNode):
    block_statement: "BlockStatement" = None
    goto_statement: "GotoStatement" = None
    if_statement: "IfStatement" = None
    print_statement: "PrintStatement" = None
    raiseerror_statement: "RaiseerrorStatement" = None
    return_statement: "ReturnStatement" = None
    throw_statement: "ThrowStatement" = None
    try_catch_statement: "TryCatchStatement" = None
    waitfor_statement: "WaitforStatement" = None
    while_statement: "WhileStatement" = None


@dataclass
class BlockStatement(TreeNode):
    sql_clauses: list["SqlClauses"] = None


@dataclass
class GotoStatement(TreeNode):
    goto_: bool = False
    id: "Id" = None


@dataclass
class ReturnStatement(TreeNode):
    expression: list["Expression"] = None


@dataclass
class IfStatement(TreeNode):
    search_condition: "SearchCondition" = None
    left: "SqlClauses" = None
    else_: bool = False
    right: "SqlClauses" = None


@dataclass
class ThrowStatement(TreeNode):
    throw_error_number: "ThrowErrorNumber" = None
    throw_message: "ThrowMessage" = None
    throw_state: "ThrowState" = None


@dataclass
class ThrowErrorNumber(TreeNode):
    decimal: bool = False
    local_id: str = None


@dataclass
class ThrowMessage(TreeNode):
    string: str = None
    local_id: str = None


@dataclass
class ThrowState(TreeNode):
    decimal: bool = False
    local_id: str = None


@dataclass
class TryCatchStatement(TreeNode):
    try_clauses: "SqlClauses" = None


@dataclass
class WaitforStatement(TreeNode):
    receive_statement: list["ReceiveStatement"] = None
    time: "Time" = None
    expression: list["Expression"] = None
    delay: bool = False
    time: bool = False
    timeout: bool = False


@dataclass
class WhileStatement(TreeNode):
    search_condition: "SearchCondition" = None
    sql_clauses: "SqlClauses" = None
    break_: bool = False
    continue_: bool = False


@dataclass
class PrintStatement(TreeNode):
    expression: "Expression" = None
    double_quote_id: str = None
    local_id: list[str] = None


@dataclass
class RaiseerrorStatement(TreeNode):
    raiserror: bool = False
    raiseerror_statement_msg: "RaiseerrorStatementMsg" = None
    severity: "ConstantLocalId" = None
    with_: bool = False
    null: bool = False
    log: bool = False
    seterror: bool = False
    nowait: bool = False
    decimal: bool = False
    raiseerror_statement_formatstring: "RaiseerrorStatementFormatstring" = None
    raiseerror_statement_argument: list["RaiseerrorStatementArgument"] = None


@dataclass
class AnotherStatement(TreeNode):
    alter_queue: "AlterQueue" = None
    checkpoint_statement: "CheckpointStatement" = None
    conversation_statement: "ConversationStatement" = None
    create_contract: "CreateContract" = None
    create_queue: "CreateQueue" = None
    cursor_statement: "CursorStatement" = None
    declare_statement: "DeclareStatement" = None
    execute_statement: "ExecuteStatement" = None
    kill_statement: "KillStatement" = None
    message_statement: "MessageStatement" = None
    reconfigure_statement: "ReconfigureStatement" = None
    security_statement: "SecurityStatement" = None
    set_statement: "SetStatement" = None
    setuser_statement: "SetuserStatement" = None
    shutdown_statement: "ShutdownStatement" = None
    transaction_statement: "TransactionStatement" = None
    use_statement: "UseStatement" = None


@dataclass
class AlterApplicationRole(TreeNode):
    appliction_role: "Id" = None
    left: bool = False
    name: bool = False
    left: bool = False
    right: bool = False
    password: bool = False
    right: bool = False
    application_role_password: str = None
    third: bool = False
    default_schema: bool = False
    third: bool = False


@dataclass
class AlterXmlSchemaCollection(TreeNode):
    left: "Id" = None
    right: "Id" = None
    string: str = None


@dataclass
class CreateApplicationRole(TreeNode):
    appliction_role: "Id" = None
    left: bool = False
    password: bool = False
    left: bool = False
    application_role_password: str = None
    right: bool = False
    default_schema: bool = False
    right: bool = False


@dataclass
class DropAggregate(TreeNode):
    if_: bool = False
    exists: bool = False
    schema_name: "Id" = None
    dot: bool = False


@dataclass
class DropApplicationRole(TreeNode):
    rolename: "Id" = None


@dataclass
class AlterAssembly(TreeNode):
    assembly_name: "Id" = None
    alter_assembly_clause: "AlterAssemblyClause" = None


@dataclass
class AlterAssemblyClause(TreeNode):
    alter_assembly_from_clause: list["AlterAssemblyFromClause"] = None
    alter_assembly_with_clause: list["AlterAssemblyWithClause"] = None
    alter_assembly_drop_clause: list["AlterAssemblyDropClause"] = None
    alter_assembly_add_clause: list["AlterAssemblyAddClause"] = None


@dataclass
class AlterAssemblyFromClause(TreeNode):
    client_assembly_specifier: "ClientAssemblySpecifier" = None
    alter_assembly_file_bits: "AlterAssemblyFileBits" = None


@dataclass
class AlterAssemblyDropClause(TreeNode):
    alter_assembly_drop_multiple_files: "AlterAssemblyDropMultipleFiles" = None


@dataclass
class AlterAssemblyDropMultipleFiles(TreeNode):
    all: bool = False
    multiple_local_files: "MultipleLocalFiles" = None


@dataclass
class AlterAssemblyAddClause(TreeNode):
    alter_assembly_client_file_clause: "AlterAssemblyClientFileClause" = None


@dataclass
class AlterAssemblyClientFileClause(TreeNode):
    alter_assembly_file_name: "AlterAssemblyFileName" = None
    id: "Id" = None


@dataclass
class AlterAssemblyFileName(TreeNode):
    string: str = None


@dataclass
class AlterAssemblyFileBits(TreeNode):
    id: "Id" = None


@dataclass
class AlterAssemblyWithClause(TreeNode):
    assembly_option: "AssemblyOption" = None


@dataclass
class ClientAssemblySpecifier(TreeNode):
    network_file_share: "NetworkFileShare" = None
    local_file: "LocalFile" = None
    string: str = None


@dataclass
class AssemblyOption(TreeNode):
    permission_set: bool = False
    equal: bool = False
    safe: bool = False
    external_access: bool = False
    unsafe: bool = False
    visibility: bool = False
    on_off: "OnOff" = None
    unchecked: bool = False
    data: bool = False
    assembly_option: "AssemblyOption" = None
    comma: bool = False


@dataclass
class NetworkFileShare(TreeNode):
    network_computer: "NetworkComputer" = None
    file_path: "FilePath" = None


@dataclass
class NetworkComputer(TreeNode):
    computer_name: "Id" = None


@dataclass
class FilePath(TreeNode):
    file_path: "FilePath" = None
    id: "Id" = None


@dataclass
class LocalFile(TreeNode):
    local_drive: "LocalDrive" = None
    file_path: "FilePath" = None


@dataclass
class LocalDrive(TreeNode):
    disk_drive: str = None


@dataclass
class MultipleLocalFiles(TreeNode):
    local_file: "LocalFile" = None
    single_quote: bool = False
    comma: bool = False


@dataclass
class CreateAssembly(TreeNode):
    assembly_name: "Id" = None
    authorization: bool = False
    with_: bool = False
    permission_set: bool = False
    equal: bool = False
    string: str = None
    binary: str = None
    safe: bool = False
    external_access: bool = False
    unsafe: bool = False


@dataclass
class DropAssembly(TreeNode):
    if_: bool = False
    exists: bool = False
    assembly_name: list["Id"] = None
    with_: bool = False
    no: bool = False
    dependents: bool = False


@dataclass
class AlterAsymmetricKey(TreeNode):
    asym_key_name: "Id" = None
    asymmetric_key_option: "AsymmetricKeyOption" = None
    remove: bool = False
    private: bool = False
    key: bool = False


@dataclass
class AsymmetricKeyOption(TreeNode):
    left: "AsymmetricKeyPasswordChangeOption" = None
    comma: bool = False
    right: "AsymmetricKeyPasswordChangeOption" = None


@dataclass
class AsymmetricKeyPasswordChangeOption(TreeNode):
    decryption: bool = False
    by: bool = False
    password: bool = False
    equal: bool = False
    string: str = None
    encryption: bool = False


@dataclass
class CreateAsymmetricKey(TreeNode):
    asym_key_nam: "Id" = None
    authorization: bool = False
    from_: bool = False
    with_: bool = False
    encryption: bool = False
    by: bool = False
    password: bool = False
    left: bool = False
    asymmetric_key_password: str = None
    file: bool = False
    right: bool = False
    right: str = None
    executable_file: bool = False
    third: bool = False
    third: str = None
    assembly: bool = False
    provider: bool = False
    algorithm: bool = False
    fourth: bool = False
    provider_key_name: bool = False
    fifth: bool = False
    provider_key_name: str = None
    creation_disposition: bool = False
    f_5: bool = False
    rsa_4096: bool = False
    rsa_3072: bool = False
    rsa_2048: bool = False
    rsa_1024: bool = False
    rsa_512: bool = False
    create_new: bool = False
    open_existing: bool = False


@dataclass
class DropAsymmetricKey(TreeNode):
    key_name: "Id" = None
    remove: bool = False
    provider: bool = False
    left: bool = False


@dataclass
class AlterAuthorization(TreeNode):
    class_type: "ClassType" = None
    entity: "EntityName" = None
    authorization_grantee: "AuthorizationGrantee" = None


@dataclass
class AuthorizationGrantee(TreeNode):
    principal_name: "Id" = None
    schema: bool = False
    owner: bool = False


@dataclass
class AlterAuthorizationForSqlDatabase(TreeNode):
    class_type_for_sql_database: "ClassTypeForSqlDatabase" = None
    entity: "EntityName" = None
    authorization_grantee: "AuthorizationGrantee" = None


@dataclass
class AlterAuthorizationForAzureDw(TreeNode):
    class_type_for_azure_dw: "ClassTypeForAzureDw" = None
    entity: "EntityNameForAzureDw" = None
    authorization_grantee: "AuthorizationGrantee" = None


@dataclass
class AlterAuthorizationForParallelDw(TreeNode):
    class_type_for_parallel_dw: "ClassTypeForParallelDw" = None
    entity: "EntityNameForParallelDw" = None
    authorization_grantee: "AuthorizationGrantee" = None


@dataclass
class ClassType(TreeNode):
    object: bool = False
    assembly: bool = False
    asymmetric: bool = False
    key: bool = False
    availability: bool = False
    group: bool = False
    certificate: bool = False
    contract: bool = False
    type_: bool = False
    database: bool = False
    endpoint: bool = False
    fulltext: bool = False
    catalog: bool = False
    stoplist: bool = False
    message: bool = False
    remote: bool = False
    service: bool = False
    binding: bool = False
    role: bool = False
    route: bool = False
    schema: bool = False
    search: bool = False
    property: bool = False
    list: bool = False
    server: bool = False
    symmetric: bool = False
    xml: bool = False
    collection: bool = False


@dataclass
class ClassTypeForSqlDatabase(TreeNode):
    object: bool = False
    assembly: bool = False
    asymmetric: bool = False
    key: bool = False
    certificate: bool = False
    type_: bool = False
    database: bool = False
    fulltext: bool = False
    catalog: bool = False
    stoplist: bool = False
    role: bool = False
    schema: bool = False
    search: bool = False
    property: bool = False
    list: bool = False
    symmetric: bool = False
    xml: bool = False
    collection: bool = False


@dataclass
class ClassTypeForAzureDw(TreeNode):
    schema: bool = False
    object: bool = False


@dataclass
class ClassTypeForParallelDw(TreeNode):
    database: bool = False
    schema: bool = False
    object: bool = False


@dataclass
class ClassTypeForGrant(TreeNode):
    application: bool = False
    role: bool = False
    assembly: bool = False
    asymmetric: bool = False
    key: bool = False
    audit: bool = False
    availability: bool = False
    group: bool = False
    broker: bool = False
    priority: bool = False
    certificate: bool = False
    column: bool = False
    encryption: bool = False
    master: bool = False
    contract: bool = False
    credential: bool = False
    cryptographic: bool = False
    provider: bool = False
    database: bool = False
    specification: bool = False
    event: bool = False
    session: bool = False
    scoped: bool = False
    configuration: bool = False
    resource: bool = False
    governor: bool = False
    endpoint: bool = False
    notification: bool = False
    object: bool = False
    server: bool = False
    external: bool = False
    data: bool = False
    source: bool = False
    file: bool = False
    format: bool = False
    library: bool = False
    pool: bool = False
    table: bool = False
    catalog: bool = False
    stoplist: bool = False
    login: bool = False
    message: bool = False
    type_: bool = False
    partition: bool = False
    function: bool = False
    scheme: bool = False
    remote: bool = False
    service: bool = False
    binding: bool = False
    route: bool = False
    schema: bool = False
    search: bool = False
    property: bool = False
    list: bool = False
    sql: bool = False
    symmetric: bool = False
    trigger: bool = False
    user: bool = False
    xml: bool = False
    collection: bool = False


@dataclass
class DropAvailabilityGroup(TreeNode):
    group_name: "Id" = None


@dataclass
class AlterAvailabilityGroup(TreeNode):
    alter_availability_group_start: "AlterAvailabilityGroupStart" = None
    alter_availability_group_options: "AlterAvailabilityGroupOptions" = None


@dataclass
class AlterAvailabilityGroupStart(TreeNode):
    group_name: "Id" = None


@dataclass
class AlterAvailabilityGroupOptions(TreeNode):
    set: bool = False
    lr_bracket: bool = False
    rr_bracket: bool = False
    automated_backup_preference: bool = False
    left: bool = False
    failure_condition_level: bool = False
    right: bool = False
    left: bool = False
    health_check_timeout: bool = False
    third: bool = False
    milliseconds: bool = False
    db_failover: bool = False
    fourth: bool = False
    required_synchronized_secondaries_to_commit: bool = False
    fifth: bool = False
    third: bool = False
    primary: bool = False
    secondary_only: bool = False
    secondary: bool = False
    none: bool = False
    on: bool = False
    off: bool = False
    add: bool = False
    database: bool = False
    database_name: "Id" = None
    remove: bool = False
    replica: bool = False
    server_instance: str = None
    with_: bool = False
    endpoint_url: bool = False
    left: bool = False
    availability_mode: bool = False
    right: bool = False
    failover_mode: bool = False
    third: bool = False
    seeding_mode: bool = False
    fourth: bool = False
    backup_priority: bool = False
    fifth: bool = False
    primary_role: bool = False
    right: bool = False
    left: bool = False
    f_5: bool = False
    right: bool = False
    f_5: bool = False
    secondary_role: bool = False
    third: bool = False
    right: bool = False
    f_6: bool = False
    third: bool = False
    synchronous_commit: bool = False
    asynchronous_commit: bool = False
    left: bool = False
    left: bool = False
    right: bool = False
    right: bool = False
    read_write: bool = False
    all: bool = False
    read_only: bool = False
    read_only_routing_list: bool = False
    no: bool = False
    session_timeout: bool = False
    modify: bool = False
    right: str = None
    f_7: bool = False
    right: bool = False
    f_8: bool = False
    f_9: bool = False
    fourth: bool = False
    right: bool = False
    right: bool = False
    right: bool = False
    fifth: bool = False
    third: str = None
    fourth: list[str] = None
    join: bool = False
    availability: bool = False
    group: bool = False
    listener_url: bool = False
    grant: bool = False
    create: bool = False
    any: bool = False
    deny: bool = False
    failover: bool = False
    force_failover_allow_data_loss: bool = False
    listener: bool = False
    dhcp: bool = False
    right: bool = False
    ip: bool = False
    left: "IpV4Failover" = None
    right: "IpV4Failover" = None
    port: bool = False
    third: "IpV4Failover" = None
    fourth: "IpV4Failover" = None
    ip_v6_failover: "IpV6Failover" = None
    restart: bool = False
    offline: bool = False
    dtc_support: bool = False
    per_db: bool = False


@dataclass
class IpV4Failover(TreeNode):
    string: str = None


@dataclass
class IpV6Failover(TreeNode):
    string: str = None


@dataclass
class CreateOrAlterBrokerPriority(TreeNode):
    create: bool = False
    alter: bool = False
    conversation_priority_name: "Id" = None
    contract_name: bool = False
    left: bool = False
    left: bool = False
    local_service_name: bool = False
    right: bool = False
    right: bool = False
    remote_service_name: bool = False
    third: bool = False
    third: bool = False
    priority_level: bool = False
    fourth: bool = False
    left: bool = False
    double_forward_slash: bool = False
    right: "Id" = None
    right: bool = False
    remote_service_name: str = None
    third: bool = False
    priority_value: bool = False
    default_: bool = False
    third: "Id" = None


@dataclass
class DropBrokerPriority(TreeNode):
    conversation_priority_name: "Id" = None


@dataclass
class AlterCertificate(TreeNode):
    certificate_name: "Id" = None
    remove: bool = False
    private_key: bool = False
    left: bool = False
    private: bool = False
    key: bool = False
    lr_bracket: bool = False
    rr_bracket: bool = False
    right: bool = False
    active: bool = False
    for_: bool = False
    begin_dialog: bool = False
    left: bool = False
    left: list[str] = None
    right: list[str] = None
    third: list[str] = None
    on: bool = False
    off: bool = False


@dataclass
class AlterColumnEncryptionKey(TreeNode):
    column_encryption_key: "Id" = None
    add: bool = False
    drop: bool = False
    left: bool = False
    algorithm: bool = False
    left: bool = False
    algorithm_name: str = None
    right: bool = False
    encrypted_value: bool = False
    right: bool = False
    binary: str = None


@dataclass
class CreateColumnEncryptionKey(TreeNode):
    column_encryption_key: "Id" = None
    algorithm_name: list[str] = None
    encrypted_value: list[str] = None


@dataclass
class DropCertificate(TreeNode):
    certificate_name: "Id" = None


@dataclass
class DropColumnEncryptionKey(TreeNode):
    key_name: "Id" = None


@dataclass
class DropColumnMasterKey(TreeNode):
    key_name: "Id" = None


@dataclass
class DropContract(TreeNode):
    dropped_contract_name: "Id" = None


@dataclass
class DropCredential(TreeNode):
    credential_name: "Id" = None


@dataclass
class DropCryptograhicProvider(TreeNode):
    provider_name: "Id" = None


@dataclass
class DropDatabase(TreeNode):
    if_: bool = False
    exists: bool = False
    database_name_or_database_snapshot_name: list["Id"] = None


@dataclass
class DropDatabaseAuditSpecification(TreeNode):
    audit_specification_name: "Id" = None


@dataclass
class DropDatabaseScopedCredential(TreeNode):
    credential_name: "Id" = None


@dataclass
class DropDefault(TreeNode):
    if_: bool = False
    exists: bool = False
    comma: bool = False
    default_name: "Id" = None
    dot: bool = False


@dataclass
class DropEndpoint(TreeNode):
    end_point_name: "Id" = None


@dataclass
class DropExternalDataSource(TreeNode):
    external_data_source_name: "Id" = None


@dataclass
class DropExternalFileFormat(TreeNode):
    external_file_format_name: "Id" = None


@dataclass
class DropExternalLibrary(TreeNode):
    library_name: "Id" = None
    authorization: bool = False


@dataclass
class DropExternalResourcePool(TreeNode):
    pool_name: "Id" = None


@dataclass
class DropExternalTable(TreeNode):
    database_name: "Id" = None
    left: bool = False
    right: bool = False


@dataclass
class DropEventNotifications(TreeNode):
    notification_name: list["Id"] = None
    server: bool = False
    database: bool = False
    queue: bool = False


@dataclass
class DropEventSession(TreeNode):
    event_session_name: "Id" = None


@dataclass
class DropFulltextCatalog(TreeNode):
    catalog_name: "Id" = None


@dataclass
class DropFulltextIndex(TreeNode):
    schema: "Id" = None
    dot: bool = False


@dataclass
class DropFulltextStoplist(TreeNode):
    stoplist_name: "Id" = None


@dataclass
class DropLogin(TreeNode):
    login_name: "Id" = None


@dataclass
class DropMessageType(TreeNode):
    message_type_name: "Id" = None


@dataclass
class DropPartitionFunction(TreeNode):
    partition_function_name: "Id" = None


@dataclass
class DropPartitionScheme(TreeNode):
    partition_scheme_name: "Id" = None


@dataclass
class DropQueue(TreeNode):
    database_name: "Id" = None
    left: bool = False
    right: bool = False


@dataclass
class DropRemoteServiceBinding(TreeNode):
    binding_name: "Id" = None


@dataclass
class DropResourcePool(TreeNode):
    pool_name: "Id" = None


@dataclass
class DropDbRole(TreeNode):
    if_: bool = False
    exists: bool = False
    role_name: "Id" = None


@dataclass
class DropRoute(TreeNode):
    route_name: "Id" = None


@dataclass
class DropRule(TreeNode):
    if_: bool = False
    exists: bool = False
    comma: bool = False
    rule_name: "Id" = None
    dot: bool = False


@dataclass
class DropSchema(TreeNode):
    if_: bool = False
    exists: bool = False
    schema_name: "Id" = None


@dataclass
class DropSearchPropertyList(TreeNode):
    property_list_name: "Id" = None


@dataclass
class DropSecurityPolicy(TreeNode):
    if_: bool = False
    exists: bool = False
    schema_name: "Id" = None
    dot: bool = False


@dataclass
class DropSequence(TreeNode):
    if_: bool = False
    exists: bool = False
    comma: bool = False
    sequence_name: "Id" = None
    left: bool = False
    right: bool = False


@dataclass
class DropServerAudit(TreeNode):
    audit_name: "Id" = None


@dataclass
class DropServerAuditSpecification(TreeNode):
    audit_specification_name: "Id" = None


@dataclass
class DropServerRole(TreeNode):
    role_name: "Id" = None


@dataclass
class DropService(TreeNode):
    dropped_service_name: "Id" = None


@dataclass
class DropSignature(TreeNode):
    counter: bool = False
    schema_name: "Id" = None
    dot: bool = False


@dataclass
class DropStatisticsNameAzureDwAndPdw(TreeNode):
    schema_name: "Id" = None
    left: bool = False


@dataclass
class DropSymmetricKey(TreeNode):
    symmetric_key_name: "Id" = None
    remove: bool = False
    provider: bool = False
    left: bool = False


@dataclass
class DropSynonym(TreeNode):
    if_: bool = False
    exists: bool = False
    schema: "Id" = None
    dot: bool = False


@dataclass
class DropUser(TreeNode):
    if_: bool = False
    exists: bool = False
    user_name: "Id" = None


@dataclass
class DropWorkloadGroup(TreeNode):
    group_name: "Id" = None


@dataclass
class DropXmlSchemaCollection(TreeNode):
    relational_schema: "Id" = None
    dot: bool = False


@dataclass
class DisableTrigger(TreeNode):
    left: bool = False
    object_name: "Id" = None
    database: bool = False
    right: bool = False
    server: bool = False
    left: bool = False
    right: bool = False


@dataclass
class EnableTrigger(TreeNode):
    left: bool = False
    object_name: "Id" = None
    database: bool = False
    right: bool = False
    server: bool = False
    left: bool = False
    right: bool = False


@dataclass
class LockTable(TreeNode):
    table_name: "TableName" = None
    share: bool = False
    exclusive: bool = False
    wait: bool = False
    seconds: bool = False
    nowait: bool = False


@dataclass
class TruncateTable(TreeNode):
    table_name: "TableName" = None
    with_: bool = False
    left: bool = False
    partitions: bool = False
    right: bool = False
    left: bool = False
    right: bool = False
    left: bool = False
    right: bool = False
    to: bool = False
    third: bool = False


@dataclass
class CreateColumnMasterKey(TreeNode):
    key_name: "Id" = None
    key_store_provider_name: str = None


@dataclass
class AlterCredential(TreeNode):
    credential_name: "Id" = None
    identity_name: str = None
    comma: bool = False
    secret: bool = False
    left: bool = False


@dataclass
class CreateCredential(TreeNode):
    credential_name: "Id" = None
    identity_name: str = None
    comma: bool = False
    secret: bool = False
    left: bool = False
    for_: bool = False
    cryptographic: bool = False
    provider: bool = False


@dataclass
class AlterCryptographicProvider(TreeNode):
    provider_name: "Id" = None
    from_: bool = False
    file: bool = False
    equal: bool = False
    crypto_provider_ddl_file: str = None
    enable: bool = False
    disable: bool = False


@dataclass
class CreateCryptographicProvider(TreeNode):
    provider_name: "Id" = None
    path_of_dll: str = None


@dataclass
class CreateEndpoint(TreeNode):
    endpointname: "Id" = None
    authorization: bool = False
    state: bool = False
    left: bool = False
    create_endpoint_state: "CreateEndpointState" = None
    endpoint_listener_clause: "EndpointListenerClause" = None
    left: bool = False
    tsql: bool = False
    left: bool = False
    left: bool = False
    right: bool = False
    service_broker: bool = False
    right: bool = False
    left: "EndpointAuthenticationClause" = None
    right: bool = False
    third: bool = False
    database_mirroring: bool = False
    third: bool = False
    right: "EndpointAuthenticationClause" = None
    left: bool = False
    role: bool = False
    right: bool = False
    third: bool = False
    right: bool = False
    left: "EndpointEncryptionAlogorithmClause" = None
    third: bool = False
    message_forwarding: bool = False
    third: bool = False
    fourth: bool = False
    message_forward_size: bool = False
    fourth: bool = False
    decimal: bool = False
    fifth: bool = False
    right: "EndpointEncryptionAlogorithmClause" = None
    witness: bool = False
    partner: bool = False
    all: bool = False
    enabled: bool = False
    disabled: bool = False


@dataclass
class EndpointEncryptionAlogorithmClause(TreeNode):
    disabled: bool = False
    supported: bool = False
    required: bool = False
    algorithm: bool = False
    left: bool = False
    left: bool = False
    right: bool = False
    right: bool = False


@dataclass
class EndpointAuthenticationClause(TreeNode):
    left: bool = False
    left: bool = False
    cert_name: "Id" = None
    right: bool = False
    left: bool = False
    left: bool = False
    left: bool = False
    right: bool = False
    right: bool = False
    right: bool = False
    right: bool = False


@dataclass
class EndpointListenerClause(TreeNode):
    comma: bool = False
    listener_ip: bool = False
    left: bool = False
    all: bool = False
    ipv4: str = None
    ipv6: str = None


@dataclass
class CreateEventNotification(TreeNode):
    event_notification_name: "Id" = None
    server: bool = False
    database: bool = False
    queue: bool = False
    with_: bool = False
    fan_in: bool = False
    broker_service: str = None


@dataclass
class CreateOrAlterEventSession(TreeNode):
    create: bool = False
    alter: bool = False
    event_session_name: "Id" = None
    with_: bool = False
    left: bool = False
    left: bool = False
    state: bool = False
    left: bool = False
    left: bool = False
    right: bool = False
    left: bool = False
    left: bool = False
    third: bool = False
    fourth: bool = False
    left: bool = False
    max_memory: bool = False
    right: bool = False
    max_memory: bool = False
    right: bool = False
    event_retention_mode: bool = False
    third: bool = False
    third: bool = False
    max_dispatch_latency: bool = False
    fourth: bool = False
    fourth: bool = False
    max_event_size: bool = False
    fifth: bool = False
    max_event_size: bool = False
    fifth: bool = False
    memory_partition_mode: bool = False
    f_5: bool = False
    f_5: bool = False
    track_causality: bool = False
    f_6: bool = False
    f_6: bool = False
    startup_state: bool = False
    f_7: bool = False
    start: bool = False
    stop: bool = False
    fifth: bool = False
    left: bool = False
    where: bool = False
    event_session_predicate_expression: "EventSessionPredicateExpression" = None
    f_5: bool = False
    left: bool = False
    left: bool = False
    allow_single_event_loss: bool = False
    allow_multiple_event_loss: bool = False
    no_event_loss: bool = False
    max_dispatch_latency_seconds: bool = False
    seconds: bool = False
    infinite: bool = False
    right: bool = False
    right: bool = False
    none: bool = False
    per_node: bool = False
    per_cpu: bool = False
    left: bool = False
    left: bool = False
    right: bool = False
    right: bool = False
    right: bool = False
    fourth: bool = False
    right: bool = False
    left: str = None
    fifth: bool = False
    right: str = None
    f_6: bool = False


@dataclass
class EventSessionPredicateExpression(TreeNode):
    and_: bool = False
    or_: bool = False
    event_session_predicate_factor: "EventSessionPredicateFactor" = None
    lr_bracket: bool = False
    event_session_predicate_expression: "EventSessionPredicateExpression" = None
    rr_bracket: bool = False


@dataclass
class EventSessionPredicateFactor(TreeNode):
    event_session_predicate_leaf: "EventSessionPredicateLeaf" = None
    lr_bracket: bool = False
    event_session_predicate_expression: "EventSessionPredicateExpression" = None
    rr_bracket: bool = False


@dataclass
class EventSessionPredicateLeaf(TreeNode):
    event_field_name: "Id" = None
    left: bool = False
    left: bool = False
    left: bool = False
    right: bool = False
    right: bool = False
    decimal: bool = False
    string: str = None
    left: bool = False
    third: bool = False
    right: bool = False
    exclamation: bool = False
    third: bool = False
    third: bool = False
    fourth: bool = False
    right: bool = False
    lr_bracket: bool = False
    comma: bool = False
    rr_bracket: bool = False
    third: bool = False
    fourth: bool = False


@dataclass
class AlterExternalDataSource(TreeNode):
    alter: bool = False
    external: bool = False
    data: bool = False
    source: bool = False
    data_source_name: "Id" = None
    set: bool = False
    location: list[str] = None
    with_: bool = False
    lr_bracket: bool = False
    type_: bool = False
    left: bool = False
    blob_storage: bool = False
    left: bool = False
    location: bool = False
    right: bool = False
    right: bool = False
    credential: bool = False
    third: bool = False
    rr_bracket: bool = False


@dataclass
class AlterExternalLibrary(TreeNode):
    library_name: "Id" = None
    authorization: bool = False
    set: bool = False
    add: bool = False
    lr_bracket: bool = False
    content: bool = False
    left: bool = False
    with_: bool = False
    left: bool = False
    client_library: str = None
    binary: str = None
    none: bool = False
    left: bool = False
    platform: bool = False
    right: bool = False
    right: bool = False
    windows: bool = False
    linux: bool = False
    r: bool = False
    python: bool = False


@dataclass
class CreateExternalLibrary(TreeNode):
    library_name: "Id" = None
    authorization: bool = False
    left: bool = False
    lr_bracket: bool = False
    with_: bool = False
    left: bool = False
    content: bool = False
    left: bool = False
    client_library: str = None
    binary: str = None
    none: bool = False
    right: bool = False
    platform: bool = False
    right: bool = False
    right: bool = False
    windows: bool = False
    linux: bool = False
    r: bool = False
    python: bool = False


@dataclass
class AlterExternalResourcePool(TreeNode):
    pool_name: "Id" = None
    default_double_quote: str = None
    left: bool = False
    affinity: bool = False
    cpu: bool = False
    left: bool = False
    numanode: bool = False
    right: bool = False
    right: bool = False
    max_memory_percent: bool = False
    third: bool = False
    max_memory_percent: bool = False
    third: bool = False
    max_processes: bool = False
    fourth: bool = False
    max_processes: bool = False
    auto: bool = False


@dataclass
class CreateExternalResourcePool(TreeNode):
    pool_name: "Id" = None
    left: bool = False
    affinity: bool = False
    cpu: bool = False
    left: bool = False
    numanode: bool = False
    right: bool = False
    right: bool = False
    max_memory_percent: bool = False
    third: bool = False
    max_memory_percent: bool = False
    third: bool = False
    max_processes: bool = False
    fourth: bool = False
    max_processes: bool = False
    auto: bool = False


@dataclass
class AlterFulltextCatalog(TreeNode):
    catalog_name: "Id" = None
    rebuild: bool = False
    reorganize: bool = False
    as_: bool = False
    default_: bool = False
    with_: bool = False
    accent_sensitivity: bool = False
    equal: bool = False
    on: bool = False
    off: bool = False


@dataclass
class CreateFulltextCatalog(TreeNode):
    catalog_name: "Id" = None
    left: bool = False
    filegroup: bool = False
    in_: bool = False
    path: bool = False
    rootpath: str = None
    with_: bool = False
    accent_sensitivity: bool = False
    equal: bool = False
    as_: bool = False
    default_: bool = False
    authorization: bool = False
    right: bool = False
    off: bool = False


@dataclass
class AlterFulltextStoplist(TreeNode):
    stoplist_name: "Id" = None
    add: bool = False
    stopword: str = None
    left: bool = False
    drop: bool = False
    right: str = None
    left: bool = False
    left: str = None
    stopword: str = None
    right: bool = False
    left: bool = False
    right: bool = False
    fourth: str = None
    right: bool = False
    right: str = None
    fifth: str = None
    third: bool = False
    third: str = None


@dataclass
class CreateFulltextStoplist(TreeNode):
    stoplist_name: "Id" = None
    from_: bool = False
    authorization: bool = False
    system: bool = False
    left: bool = False
    dot: bool = False


@dataclass
class AlterLoginSqlServer(TreeNode):
    login_name: "Id" = None
    with_: bool = False
    left: bool = False
    enable: bool = False
    disable: bool = False
    old_password: bool = False
    left: bool = False
    old_password: str = None
    default_database: bool = False
    right: bool = False
    default_language: bool = False
    third: bool = False
    name: bool = False
    fourth: bool = False
    check_policy: bool = False
    fifth: bool = False
    check_expiration: bool = False
    f_5: bool = False
    right: bool = False
    f_6: bool = False
    no: bool = False
    third: bool = False
    add: bool = False
    drop: bool = False
    password: bool = False
    f_7: bool = False
    left: bool = False
    left: bool = False
    right: bool = False
    right: bool = False
    password_hash: str = None
    hashed: bool = False


@dataclass
class CreateLoginSqlServer(TreeNode):
    login_name: "Id" = None
    left: bool = False
    left: bool = False
    sid: bool = False
    left: bool = False
    sid: str = None
    right: bool = False
    left: bool = False
    right: bool = False
    third: bool = False
    left: bool = False
    third: bool = False
    fourth: bool = False
    check_expiration: bool = False
    fourth: bool = False
    fifth: bool = False
    check_policy: bool = False
    fifth: bool = False
    f_5: bool = False
    credential: bool = False
    f_5: bool = False
    from_: bool = False
    password: bool = False
    f_6: bool = False
    left: bool = False
    left: bool = False
    right: bool = False
    right: bool = False
    windows: bool = False
    certificate: bool = False
    asymmetric: bool = False
    key: bool = False
    password: str = None
    hashed: bool = False
    right: bool = False
    f_6: bool = False
    right: bool = False
    f_7: bool = False
    f_7: bool = False
    right: bool = False
    f_8: bool = False


@dataclass
class AlterLoginAzureSql(TreeNode):
    login_name: "Id" = None
    with_: bool = False
    enable: bool = False
    disable: bool = False
    password: bool = False
    left: bool = False
    password: str = None
    name: bool = False
    right: bool = False
    old_password: bool = False
    third: bool = False


@dataclass
class CreateLoginAzureSql(TreeNode):
    login_name: "Id" = None
    string: str = None
    sid: bool = False
    left: bool = False
    sid: str = None


@dataclass
class AlterLoginAzureSqlDwAndPdw(TreeNode):
    login_name: "Id" = None
    with_: bool = False
    enable: bool = False
    disable: bool = False
    password: bool = False
    left: bool = False
    password: str = None
    name: bool = False
    right: bool = False
    old_password: bool = False
    third: bool = False


@dataclass
class CreateLoginPdw(TreeNode):
    login_name: "Id" = None
    with_: bool = False
    from_: bool = False
    windows: bool = False
    password: bool = False
    left: bool = False
    password: str = None
    must_change: bool = False
    check_policy: bool = False
    right: bool = False
    on: bool = False
    off: bool = False


@dataclass
class AlterMasterKeySqlServer(TreeNode):
    regenerate: bool = False
    with_: bool = False
    left: bool = False
    left: bool = False
    left: bool = False
    left: bool = False
    password: str = None
    right: bool = False
    right: bool = False
    force: bool = False
    add: bool = False
    drop: bool = False
    service: bool = False
    left: bool = False
    left: bool = False
    right: bool = False
    right: bool = False


@dataclass
class CreateMasterKeySqlServer(TreeNode):
    password: str = None


@dataclass
class AlterMasterKeyAzureSql(TreeNode):
    regenerate: bool = False
    with_: bool = False
    left: bool = False
    left: bool = False
    left: bool = False
    left: bool = False
    password: str = None
    add: bool = False
    right: bool = False
    right: bool = False
    drop: bool = False
    third: bool = False
    third: bool = False
    right: bool = False
    right: bool = False
    force: bool = False
    service: bool = False
    left: bool = False
    left: bool = False
    third: bool = False
    third: bool = False


@dataclass
class CreateMasterKeyAzureSql(TreeNode):
    encryption: bool = False
    by: bool = False
    password: bool = False
    equal: bool = False
    password: str = None


@dataclass
class AlterMessageType(TreeNode):
    message_type_name: "Id" = None
    none: bool = False
    empty: bool = False
    well_formed_xml: bool = False
    valid_xml: bool = False
    with_: bool = False
    schema: bool = False
    collection: bool = False


@dataclass
class AlterPartitionFunction(TreeNode):
    partition_function_name: "Id" = None
    split: bool = False
    merge: bool = False


@dataclass
class AlterPartitionScheme(TreeNode):
    partition_scheme_name: "Id" = None


@dataclass
class AlterRemoteServiceBinding(TreeNode):
    binding_name: "Id" = None
    user: bool = False
    left: bool = False
    comma: bool = False
    anonymous: bool = False
    right: bool = False
    on: bool = False
    off: bool = False


@dataclass
class CreateRemoteServiceBinding(TreeNode):
    binding_name: "Id" = None
    authorization: bool = False
    remote_service_name: str = None
    user: bool = False
    left: bool = False
    comma: bool = False
    anonymous: bool = False
    right: bool = False
    on: bool = False
    off: bool = False


@dataclass
class CreateResourcePool(TreeNode):
    pool_name: "Id" = None
    with_: bool = False
    left: bool = False
    left: bool = False
    left: bool = False
    min_cpu_percent: bool = False
    left: bool = False
    left: bool = False
    right: bool = False
    max_cpu_percent: bool = False
    right: bool = False
    right: bool = False
    third: bool = False
    cap_cpu_percent: bool = False
    third: bool = False
    third: bool = False
    fourth: bool = False
    affinity: bool = False
    scheduler: bool = False
    fourth: bool = False
    fifth: bool = False
    min_memory_percent: bool = False
    fifth: bool = False
    fourth: bool = False
    f_5: bool = False
    max_memory_percent: bool = False
    f_5: bool = False
    fifth: bool = False
    f_6: bool = False
    min_iops_per_volume: bool = False
    f_6: bool = False
    f_5: bool = False
    f_7: bool = False
    max_iops_per_volume: bool = False
    f_7: bool = False
    f_6: bool = False
    auto: bool = False
    right: bool = False
    right: bool = False
    numanode: bool = False
    f_8: bool = False
    third: bool = False
    third: bool = False
    f_7: bool = False
    f_8: bool = False
    left: bool = False
    f_9: bool = False
    f10: bool = False
    f11: bool = False
    right: bool = False
    f12: bool = False


@dataclass
class AlterResourceGovernor(TreeNode):
    left: bool = False
    left: bool = False
    classifier_function: bool = False
    left: bool = False
    left: bool = False
    reset: bool = False
    statistics: bool = False
    right: bool = False
    right: bool = False
    max_outstanding_io_per_volume: bool = False
    right: bool = False
    max_outstanding_io_per_volume: bool = False
    right: bool = False
    disable: bool = False
    reconfigure: bool = False
    schema_name: "Id" = None
    dot: bool = False
    null: bool = False


@dataclass
class AlterDatabaseAuditSpecification(TreeNode):
    audit_specification_name: "Id" = None
    for_: bool = False
    server: bool = False
    left: bool = False
    left: "AuditActionSpecGroup" = None
    with_: bool = False
    state: bool = False
    right: list["AuditActionSpecGroup"] = None
    on: bool = False
    off: bool = False


@dataclass
class AuditActionSpecGroup(TreeNode):
    add: bool = False
    drop: bool = False
    audit_action_specification: "AuditActionSpecification" = None
    audit_action_group_name: "Id" = None


@dataclass
class AuditActionSpecification(TreeNode):
    left: "ActionSpecification" = None
    right: list["ActionSpecification"] = None
    audit_class_name: "AuditClassName" = None
    audit_securable: "AuditSecurable" = None
    left: "PrincipalId" = None
    right: list["PrincipalId"] = None


@dataclass
class ActionSpecification(TreeNode):
    select_: bool = False
    insert: bool = False
    update: bool = False
    delete: bool = False
    execute: str = None
    receive: bool = False
    references: bool = False


@dataclass
class AuditClassName(TreeNode):
    object: bool = False
    schema: bool = False
    table: bool = False


@dataclass
class AuditSecurable(TreeNode):
    left: "Id" = None
    right: "Id" = None
    third: "Id" = None


@dataclass
class AlterDbRole(TreeNode):
    role_name: "Id" = None
    member: bool = False
    with_: bool = False
    name: bool = False
    equal: bool = False
    add: bool = False
    drop: bool = False


@dataclass
class CreateDatabaseAuditSpecification(TreeNode):
    audit_specification_name: "Id" = None
    for_: bool = False
    server: bool = False
    left: bool = False
    left: "AuditActionSpecGroup" = None
    with_: bool = False
    state: bool = False
    right: list["AuditActionSpecGroup"] = None
    on: bool = False
    off: bool = False


@dataclass
class CreateDbRole(TreeNode):
    role_name: "Id" = None
    authorization: bool = False


@dataclass
class CreateRoute(TreeNode):
    route_name: "Id" = None
    authorization: bool = False
    left: bool = False
    service_name: bool = False
    left: bool = False
    route_service_name: str = None
    right: bool = False
    broker_instance: bool = False
    right: bool = False
    broker_instance_identifier: str = None
    third: bool = False
    lifetime: bool = False
    third: bool = False
    decimal: bool = False
    third: str = None
    fourth: bool = False
    mirror_address: bool = False
    fourth: bool = False
    fourth: str = None


@dataclass
class CreateRule(TreeNode):
    schema_name: "Id" = None
    dot: bool = False
    search_condition: "SearchCondition" = None


@dataclass
class AlterSchemaSql(TreeNode):
    schema_name: "Id" = None
    double_colon: bool = False
    right: "Id" = None
    dot: bool = False
    third: "Id" = None
    object: bool = False
    type_: bool = False
    xml: bool = False
    left: bool = False
    collection: bool = False


@dataclass
class CreateSchema(TreeNode):
    schema_name: "Id" = None
    left: bool = False
    right: bool = False
    create_table: list["CreateTable"] = None
    create_view: list["CreateView"] = None
    grant: bool = False
    deny: bool = False
    left: bool = False
    left: bool = False
    left: bool = False
    left: bool = False
    left: bool = False
    left: bool = False
    right: bool = False
    right: bool = False
    right: bool = False
    right: bool = False
    right: bool = False
    right: bool = False


@dataclass
class CreateSchemaAzureSqlDwAndPdw(TreeNode):
    schema_name: "Id" = None
    authorization: bool = False


@dataclass
class AlterSchemaAzureSqlDwAndPdw(TreeNode):
    schema_name: "Id" = None
    object: bool = False
    double_colon: bool = False
    dot: bool = False
    id: str = None


@dataclass
class CreateSearchPropertyList(TreeNode):
    new_list_name: "Id" = None
    from_: bool = False
    authorization: bool = False
    dot: bool = False


@dataclass
class CreateSecurityPolicy(TreeNode):
    schema_name: "Id" = None
    left: bool = False
    with_: bool = False
    left: bool = False
    state: bool = False
    equal: bool = False
    left: bool = False
    not_: bool = False
    for_: bool = False
    replication: bool = False
    filter: bool = False
    block: bool = False
    left: bool = False
    left: bool = False
    schemabinding: bool = False
    insert: bool = False
    left: bool = False
    right: bool = False
    delete: bool = False
    right: bool = False
    right: bool = False


@dataclass
class AlterSequence(TreeNode):
    schema_name: "Id" = None
    dot: bool = False
    restart: bool = False
    increment: bool = False
    by: bool = False
    sequnce_increment: bool = False
    left: bool = False
    right: bool = False
    left: bool = False
    right: bool = False
    left: bool = False
    third: bool = False
    right: bool = False
    right: bool = False
    left: bool = False
    third: bool = False
    right: bool = False
    left: bool = False
    fourth: bool = False
    fourth: bool = False
    right: bool = False
    with_: bool = False
    fifth: bool = False


@dataclass
class CreateSequence(TreeNode):
    schema_name: "Id" = None
    dot: bool = False
    as_: bool = False
    data_type: "DataType" = None
    start: bool = False
    with_: bool = False
    left: bool = False
    increment: bool = False
    by: bool = False
    left: bool = False
    right: bool = False
    left: bool = False
    left: bool = False
    right: bool = False
    left: bool = False
    right: bool = False
    right: bool = False
    left: bool = False
    third: bool = False
    right: bool = False
    left: bool = False
    third: bool = False
    fourth: bool = False
    right: bool = False
    right: bool = False
    fourth: bool = False
    third: bool = False
    fifth: bool = False


@dataclass
class AlterServerAudit(TreeNode):
    audit_name: "Id" = None
    remove: bool = False
    left: bool = False
    modify: bool = False
    name: bool = False
    left: bool = False
    to: bool = False
    with_: bool = False
    left: bool = False
    left: bool = False
    right: bool = False
    file: bool = False
    application_log: bool = False
    security_log: bool = False
    left: bool = False
    right: bool = False
    left: bool = False
    right: bool = False
    right: bool = False
    continue_: bool = False
    shutdown: bool = False
    fail_operation: bool = False
    left: bool = False
    left: bool = False
    right: bool = False
    right: bool = False
    left: bool = False
    left: bool = False
    right: bool = False
    third: bool = False
    left: bool = False
    left: str = None
    and_: bool = False
    or_: bool = False
    fourth: bool = False
    right: bool = False
    third: bool = False
    fourth: bool = False
    fifth: bool = False
    right: bool = False
    right: str = None
    filepath: list[str] = None
    alter_server_audit_max_rollover_files: list["AlterServerAuditMaxRolloverFiles"] = None
    fifth: bool = False
    third: bool = False
    left: bool = False
    f_5: bool = False
    fourth: bool = False
    f_6: bool = False
    f_5: bool = False
    fifth: bool = False
    right: bool = False
    f_7: bool = False
    f_5: bool = False
    f_8: bool = False
    third: bool = False
    unlimited: bool = False
    right: bool = False
    right: bool = False
    mb: bool = False
    gb: bool = False
    tb: bool = False


@dataclass
class CreateServerAudit(TreeNode):
    audit_name: "Id" = None
    remove: bool = False
    left: bool = False
    modify: bool = False
    name: bool = False
    left: bool = False
    to: bool = False
    with_: bool = False
    left: bool = False
    left: bool = False
    right: bool = False
    file: bool = False
    application_log: bool = False
    security_log: bool = False
    left: bool = False
    right: bool = False
    left: bool = False
    right: bool = False
    right: bool = False
    continue_: bool = False
    shutdown: bool = False
    fail_operation: bool = False
    left: bool = False
    left: bool = False
    right: bool = False
    right: bool = False
    left: bool = False
    left: bool = False
    right: bool = False
    third: bool = False
    left: bool = False
    left: str = None
    and_: bool = False
    or_: bool = False
    fourth: bool = False
    right: bool = False
    third: bool = False
    fourth: bool = False
    fifth: bool = False
    right: bool = False
    right: str = None
    filepath: list[str] = None
    create_server_audit_max_rollover_files: list["CreateServerAuditMaxRolloverFiles"] = None
    fifth: bool = False
    third: bool = False
    left: bool = False
    f_5: bool = False
    fourth: bool = False
    f_6: bool = False
    f_5: bool = False
    fifth: bool = False
    right: bool = False
    f_7: bool = False
    f_5: bool = False
    f_8: bool = False
    third: bool = False
    unlimited: bool = False
    right: bool = False
    right: bool = False
    mb: bool = False
    gb: bool = False
    tb: bool = False


@dataclass
class AlterServerAuditSpecification(TreeNode):
    audit_specification_name: "Id" = None
    for_: bool = False
    left: bool = False
    left: bool = False
    with_: bool = False
    left: bool = False
    state: bool = False
    equal: bool = False
    left: bool = False
    add: bool = False
    drop: bool = False
    on: bool = False
    off: bool = False


@dataclass
class CreateServerAuditSpecification(TreeNode):
    audit_specification_name: "Id" = None
    for_: bool = False
    left: bool = False
    left: bool = False
    with_: bool = False
    left: bool = False
    state: bool = False
    equal: bool = False
    left: bool = False
    on: bool = False
    off: bool = False


@dataclass
class AlterServerConfiguration(TreeNode):
    process: bool = False
    affinity: bool = False
    diagnostics: bool = False
    log: bool = False
    failover: bool = False
    left: bool = False
    property: bool = False
    hadr: bool = False
    right: bool = False
    context: bool = False
    left: bool = False
    buffer: bool = False
    pool: bool = False
    extension: bool = False
    left: bool = False
    softnuma: bool = False
    cpu: bool = False
    right: bool = False
    numanode: bool = False
    third: bool = False
    left: bool = False
    left: bool = False
    path: bool = False
    fourth: bool = False
    max_size: bool = False
    fifth: bool = False
    max_files: bool = False
    f_5: bool = False
    verboselogging: bool = False
    f_6: bool = False
    sqldumperflags: bool = False
    f_7: bool = False
    sqldumperpath: bool = False
    f_8: bool = False
    sqldumpertimeout: bool = False
    failureconditionlevel: bool = False
    f_9: bool = False
    healthchecktimeout: bool = False
    f10: bool = False
    left: str = None
    local: bool = False
    right: bool = False
    lr_bracket: bool = False
    filename: bool = False
    f11: bool = False
    right: str = None
    left: bool = False
    size: bool = False
    f12: bool = False
    left: bool = False
    rr_bracket: bool = False
    right: bool = False
    third: bool = False
    third: bool = False
    auto: bool = False
    third: str = None
    left: bool = False
    right: bool = False
    left: bool = False
    right: bool = False
    third: bool = False
    third: bool = False
    fourth: str = None
    fourth: bool = False
    fifth: str = None
    fifth: bool = False
    f_5: str = None
    f_5: bool = False
    f_6: str = None
    f_6: bool = False
    f_7: str = None
    f_7: bool = False
    fourth: bool = False
    f_8: bool = False
    kb: bool = False
    right: bool = False
    gb: bool = False


@dataclass
class AlterServerRole(TreeNode):
    server_role_name: "Id" = None
    member: bool = False
    with_: bool = False
    name: bool = False
    equal: bool = False
    add: bool = False
    drop: bool = False


@dataclass
class CreateServerRole(TreeNode):
    server_role: "Id" = None
    authorization: bool = False


@dataclass
class AlterServerRolePdw(TreeNode):
    server_role_name: "Id" = None
    add: bool = False
    drop: bool = False


@dataclass
class AlterService(TreeNode):
    modified_service_name: "Id" = None
    on: bool = False
    queue: bool = False
    left: "OptArgClause" = None
    dot: bool = False
    right: list["OptArgClause"] = None


@dataclass
class OptArgClause(TreeNode):
    add: bool = False
    drop: bool = False
    modified_contract_name: "Id" = None


@dataclass
class CreateService(TreeNode):
    create_service_name: "Id" = None
    authorization: bool = False
    dot: bool = False
    lr_bracket: bool = False
    rr_bracket: bool = False
    default_: bool = False


@dataclass
class AlterServiceMasterKey(TreeNode):
    force: bool = False
    regenerate: bool = False
    with_: bool = False
    old_account: bool = False
    left: bool = False
    acold_account_name: str = None
    left: bool = False
    old_password: bool = False
    right: bool = False
    new_account: bool = False
    third: bool = False
    right: bool = False
    new_password: bool = False
    fourth: bool = False


@dataclass
class AlterSymmetricKey(TreeNode):
    key_name: "Id" = None
    encryption: bool = False
    by: bool = False
    add: bool = False
    drop: bool = False
    certificate: bool = False
    password: bool = False
    equal: bool = False
    password: str = None
    left: bool = False
    left: bool = False
    asymmetric: bool = False
    right: bool = False


@dataclass
class CreateSynonym(TreeNode):
    schema_name_1: "Id" = None
    left: bool = False
    right: bool = False
    third: bool = False
    fourth: bool = False
    fifth: bool = False
    f_5: bool = False


@dataclass
class AlterUser(TreeNode):
    username: "Id" = None
    left: list[str] = None
    null: bool = False
    right: list[str] = None
    none: bool = False
    lcid: bool = False
    on: bool = False
    off: bool = False


@dataclass
class CreateUser(TreeNode):
    create: bool = False
    user: bool = False
    user_name: "Id" = None
    login: bool = False
    with_: bool = False
    for_: bool = False
    from_: bool = False
    on: bool = False
    off: bool = False
    password: bool = False
    left: bool = False
    password: str = None
    external: bool = False
    provider: bool = False
    right: bool = False
    left: list[str] = None
    right: list[str] = None
    left: bool = False
    left: bool = False
    right: bool = False
    right: bool = False
    right: bool = False
    right: bool = False
    without: bool = False
    certificate: bool = False
    asymmetric: bool = False
    key: bool = False
    right: bool = False
    right: bool = False


@dataclass
class CreateUserAzureSqlDw(TreeNode):
    create: bool = False
    user: bool = False
    user_name: "Id" = None
    left: bool = False
    without: bool = False
    right: bool = False
    with_: bool = False
    default_schema: bool = False
    equal: bool = False
    for_: bool = False
    from_: bool = False
    external: bool = False
    provider: bool = False


@dataclass
class AlterUserAzureSql(TreeNode):
    username: "Id" = None
    on: bool = False
    off: bool = False


@dataclass
class AlterWorkloadGroup(TreeNode):
    workload_group_group_name: "Id" = None
    left: str = None
    with_: bool = False
    lr_bracket: bool = False
    rr_bracket: bool = False
    using: bool = False
    right: str = None
    low: bool = False
    medium: bool = False
    high: bool = False


@dataclass
class CreateWorkloadGroup(TreeNode):
    workload_group_group_name: "Id" = None
    with_: bool = False
    lr_bracket: bool = False
    rr_bracket: bool = False
    using: bool = False
    left: str = None
    left: bool = False
    external: bool = False
    right: str = None
    low: bool = False
    medium: bool = False
    high: bool = False


@dataclass
class CreateXmlSchemaCollection(TreeNode):
    relational_schema: "Id" = None
    dot: bool = False
    string: str = None
    local_id: str = None


@dataclass
class CreatePartitionFunction(TreeNode):
    partition_function_name: "Id" = None
    input_parameter_type: "DataType" = None
    left: bool = False
    right: bool = False
    boundary_values: "ExpressionList" = None


@dataclass
class CreatePartitionScheme(TreeNode):
    partition_scheme_name: "Id" = None


@dataclass
class CreateQueue(TreeNode):
    full_table_name: "FullTableName" = None
    queue_name: "Id" = None
    queue_settings: list["QueueSettings"] = None
    on: bool = False
    default_: bool = False


@dataclass
class QueueSettings(TreeNode):
    left: bool = False
    left: bool = False
    left: "OnOff" = None
    left: bool = False
    retention: bool = False
    right: bool = False
    right: "OnOff" = None
    right: bool = False
    activation: bool = False
    left: bool = False
    left: bool = False
    third: bool = False
    poison_message_handling: bool = False
    right: bool = False
    right: bool = False
    drop: bool = False
    right: bool = False
    third: bool = False
    third: "OnOff" = None
    third: bool = False
    fourth: bool = False
    fourth: "OnOff" = None
    fourth: bool = False
    procedure_name: bool = False
    fifth: bool = False
    func_proc_name_database_schema: "FuncProcNameDatabaseSchema" = None
    fifth: bool = False
    max_queue_readers: bool = False
    f_5: bool = False
    max_readers: bool = False
    f_5: bool = False
    execute: str = None
    as_: bool = False
    f_6: bool = False
    self: bool = False
    user_name: str = None
    owner: bool = False


@dataclass
class AlterQueue(TreeNode):
    full_table_name: "FullTableName" = None
    queue_name: "Id" = None
    queue_settings: "QueueSettings" = None
    queue_action: "QueueAction" = None


@dataclass
class QueueAction(TreeNode):
    rebuild: bool = False
    with_: bool = False
    lr_bracket: bool = False
    rr_bracket: bool = False
    reorganize: bool = False
    lob_compaction: bool = False
    equal: bool = False
    on_off: "OnOff" = None
    move: bool = False
    to: bool = False
    id: "Id" = None
    default_: bool = False


@dataclass
class CreateContract(TreeNode):
    contract_name: "ContractName" = None
    authorization: bool = False
    owner_name: "Id" = None
    default_: bool = False
    initiator: bool = False
    target: bool = False
    any: bool = False


@dataclass
class ConversationStatement(TreeNode):
    begin_conversation_timer: "BeginConversationTimer" = None
    begin_conversation_dialog: "BeginConversationDialog" = None
    end_conversation: "EndConversation" = None
    get_conversation: "GetConversation" = None
    send_conversation: "SendConversation" = None
    waitfor_conversation: "WaitforConversation" = None


@dataclass
class MessageStatement(TreeNode):
    message_type_name: "Id" = None
    authorization: bool = False
    validation: bool = False
    equal: bool = False
    none: bool = False
    empty: bool = False
    well_formed_xml: bool = False
    valid_xml: bool = False
    with_: bool = False
    schema: bool = False
    collection: bool = False


@dataclass
class MergeStatement(TreeNode):
    with_expression: list["WithExpression"] = None
    top: bool = False
    expression: "Expression" = None
    percent: bool = False
    ddl_object: "DdlObject" = None
    with_table_hints: list["WithTableHints"] = None
    as_table_alias: list["AsTableAlias"] = None
    table_sources: "TableSources" = None
    search_condition: "SearchCondition" = None
    when_matches: "WhenMatches" = None
    output_clause: list["OutputClause"] = None
    option_clause: list["OptionClause"] = None


@dataclass
class WhenMatches(TreeNode):
    merge_matched: list["MergeMatched"] = None
    and_: bool = False
    search_condition: "SearchCondition" = None
    when: bool = False
    not_: bool = False
    matched: bool = False
    then: bool = False
    merge_not_matched: "MergeNotMatched" = None
    by: bool = False
    target: bool = False


@dataclass
class MergeMatched(TreeNode):
    update: bool = False
    set: bool = False
    left: "UpdateElemMerge" = None
    right: list["UpdateElemMerge"] = None
    delete: bool = False


@dataclass
class MergeNotMatched(TreeNode):
    column_name_list: "ColumnNameList" = None
    table_value_constructor: "TableValueConstructor" = None
    default_: bool = False
    values: bool = False


@dataclass
class DeleteStatement(TreeNode):
    with_expression: list["WithExpression"] = None
    left: bool = False
    expression: "Expression" = None
    percent: bool = False
    right: bool = False
    decimal: bool = False
    delete_statement_from: "DeleteStatementFrom" = None
    with_table_hints: list["WithTableHints"] = None
    output_clause: list["OutputClause"] = None
    left: bool = False
    table_sources: "TableSources" = None
    where: bool = False
    for_clause: list["ForClause"] = None
    option_clause: list["OptionClause"] = None
    search_condition: "SearchCondition" = None
    current: bool = False
    of: bool = False
    global_: bool = False
    cursor_name: "CursorName" = None
    cursor_var: str = None


@dataclass
class DeleteStatementFrom(TreeNode):
    ddl_object: "DdlObject" = None
    rowset_function_limited: "RowsetFunctionLimited" = None
    table_var: str = None


@dataclass
class InsertStatement(TreeNode):
    with_expression: list["WithExpression"] = None
    top: bool = False
    expression: "Expression" = None
    percent: bool = False
    ddl_object: "DdlObject" = None
    rowset_function_limited: "RowsetFunctionLimited" = None
    with_table_hints: list["WithTableHints"] = None
    insert_column_name_list: "InsertColumnNameList" = None
    output_clause: list["OutputClause"] = None
    insert_statement_value: "InsertStatementValue" = None
    for_clause: list["ForClause"] = None
    option_clause: list["OptionClause"] = None


@dataclass
class InsertStatementValue(TreeNode):
    table_value_constructor: "TableValueConstructor" = None
    derived_table: "DerivedTable" = None
    execute_statement: "ExecuteStatement" = None
    default_: bool = False
    values: bool = False


@dataclass
class ReceiveStatement(TreeNode):
    all: bool = False
    distinct: bool = False
    top_clause: "TopClause" = None
    local_id: list[str] = None
    expression: list["Expression"] = None
    full_table_name: "FullTableName" = None
    into: bool = False
    table_variable: "Id" = None
    where: bool = False
    where: "SearchCondition" = None


@dataclass
class SelectStatementStandalone(TreeNode):
    with_expression: list["WithExpression"] = None
    select_statement: "SelectStatement" = None


@dataclass
class SelectStatement(TreeNode):
    query_expression: "QueryExpression" = None
    select_order_by_clause: list["SelectOrderByClause"] = None
    for_clause: list["ForClause"] = None
    option_clause: list["OptionClause"] = None


@dataclass
class Time(TreeNode):
    local_id: str = None
    constant: "Constant" = None


@dataclass
class UpdateStatement(TreeNode):
    with_expression: list["WithExpression"] = None
    top: bool = False
    expression: "Expression" = None
    percent: bool = False
    ddl_object: "DdlObject" = None
    rowset_function_limited: "RowsetFunctionLimited" = None
    with_table_hints: list["WithTableHints"] = None
    left: "UpdateElem" = None
    right: list["UpdateElem"] = None
    output_clause: list["OutputClause"] = None
    from_: bool = False
    table_sources: "TableSources" = None
    where: bool = False
    for_clause: list["ForClause"] = None
    option_clause: list["OptionClause"] = None
    search_condition: "SearchCondition" = None
    current: bool = False
    of: bool = False
    global_: bool = False
    cursor_name: "CursorName" = None
    cursor_var: str = None


@dataclass
class OutputClause(TreeNode):
    left: "OutputDmlListElem" = None
    right: list["OutputDmlListElem"] = None
    into: bool = False
    local_id: str = None
    table_name: "TableName" = None
    column_name_list: "ColumnNameList" = None


@dataclass
class OutputDmlListElem(TreeNode):
    expression: "Expression" = None
    asterisk: "Asterisk" = None
    as_column_alias: list["AsColumnAlias"] = None


@dataclass
class CreateDatabase(TreeNode):
    database: "Id" = None
    containment: bool = False
    left: bool = False
    primary: bool = False
    left: "DatabaseFileSpec" = None
    log: bool = False
    right: bool = False
    right: "DatabaseFileSpec" = None
    collate: bool = False
    with_: bool = False
    left: "CreateDatabaseOption" = None
    none: bool = False
    partial: bool = False
    third: list["DatabaseFileSpec"] = None
    fourth: list["DatabaseFileSpec"] = None
    right: list["CreateDatabaseOption"] = None


@dataclass
class CreateIndex(TreeNode):
    clustered: list["Clustered"] = None
    left: "Id" = None
    table_name: "TableName" = None
    column_name_list_with_order: "ColumnNameListWithOrder" = None
    include: bool = False
    column_name_list: "ColumnNameList" = None
    where: bool = False
    where: "SearchCondition" = None
    create_index_options: "CreateIndexOptions" = None
    left: bool = False
    right: "Id" = None


@dataclass
class CreateIndexOptions(TreeNode):
    left: "RelationalIndexOption" = None
    right: list["RelationalIndexOption"] = None


@dataclass
class RelationalIndexOption(TreeNode):
    rebuild_index_option: "RebuildIndexOption" = None
    drop_existing: bool = False
    on_off: "OnOff" = None
    optimize_for_sequential_key: bool = False


@dataclass
class AlterIndex(TreeNode):
    id: "Id" = None
    all: bool = False
    table_name: "TableName" = None
    disable: bool = False
    pause: bool = False
    abort: bool = False
    resume: bool = False
    resumable_index_options: "ResumableIndexOptions" = None
    reorganize_partition: "ReorganizePartition" = None
    set_index_options: "SetIndexOptions" = None
    rebuild_partition: "RebuildPartition" = None


@dataclass
class ResumableIndexOptions(TreeNode):
    left: "ResumableIndexOption" = None
    right: list["ResumableIndexOption"] = None


@dataclass
class ResumableIndexOption(TreeNode):
    maxdop: bool = False
    max_degree_of_parallelism: bool = False
    max_duration: bool = False
    low_priority_lock_wait: "LowPriorityLockWait" = None


@dataclass
class ReorganizePartition(TreeNode):
    partition: bool = False
    decimal: bool = False
    reorganize_options: list["ReorganizeOptions"] = None


@dataclass
class ReorganizeOptions(TreeNode):
    left: "ReorganizeOption" = None
    right: list["ReorganizeOption"] = None


@dataclass
class ReorganizeOption(TreeNode):
    lob_compaction: bool = False
    on_off: "OnOff" = None
    compress_all_row_groups: bool = False


@dataclass
class SetIndexOptions(TreeNode):
    left: "SetIndexOption" = None
    right: list["SetIndexOption"] = None


@dataclass
class SetIndexOption(TreeNode):
    allow_row_locks: bool = False
    on_off: "OnOff" = None
    allow_page_locks: bool = False
    optimize_for_sequential_key: bool = False
    ignore_dup_key: bool = False
    statistics_norecompute: bool = False
    compression_delay: bool = False
    delay: bool = False


@dataclass
class RebuildPartition(TreeNode):
    rebuild: bool = False
    partition: bool = False
    all: bool = False
    rebuild_index_options: list["RebuildIndexOptions"] = None
    decimal: bool = False
    single_partition_rebuild_index_options: list["SinglePartitionRebuildIndexOptions"] = None


@dataclass
class RebuildIndexOptions(TreeNode):
    left: "RebuildIndexOption" = None
    right: list["RebuildIndexOption"] = None


@dataclass
class RebuildIndexOption(TreeNode):
    pad_index: bool = False
    on_off: "OnOff" = None
    fillfactor: bool = False
    decimal: bool = False
    sort_in_tempdb: bool = False
    ignore_dup_key: bool = False
    statistics_norecompute: bool = False
    statistics_incremental: bool = False
    online: bool = False
    on: bool = False
    off: bool = False
    low_priority_lock_wait: "LowPriorityLockWait" = None
    resumable: bool = False
    max_duration: bool = False
    allow_row_locks: bool = False
    allow_page_locks: bool = False
    maxdop: bool = False
    data_compression: bool = False
    none: bool = False
    row: bool = False
    page: bool = False
    columnstore: bool = False
    columnstore_archive: bool = False
    on_partitions: list["OnPartitions"] = None
    xml_compression: bool = False


@dataclass
class SinglePartitionRebuildIndexOptions(TreeNode):
    left: "SinglePartitionRebuildIndexOption" = None
    right: list["SinglePartitionRebuildIndexOption"] = None


@dataclass
class SinglePartitionRebuildIndexOption(TreeNode):
    sort_in_tempdb: bool = False
    on_off: "OnOff" = None
    maxdop: bool = False
    max_degree_of_parallelism: bool = False
    resumable: bool = False
    data_compression: bool = False
    none: bool = False
    row: bool = False
    page: bool = False
    columnstore: bool = False
    columnstore_archive: bool = False
    on_partitions: list["OnPartitions"] = None
    xml_compression: bool = False
    online: bool = False
    on: bool = False
    off: bool = False
    low_priority_lock_wait: "LowPriorityLockWait" = None


@dataclass
class OnPartitions(TreeNode):
    to_partition_number: bool = False


@dataclass
class CreateColumnstoreIndex(TreeNode):
    left: "Id" = None
    table_name: "TableName" = None
    create_columnstore_index_options: list["CreateColumnstoreIndexOptions"] = None
    left: bool = False
    right: "Id" = None


@dataclass
class CreateColumnstoreIndexOptions(TreeNode):
    left: "ColumnstoreIndexOption" = None
    right: list["ColumnstoreIndexOption"] = None


@dataclass
class ColumnstoreIndexOption(TreeNode):
    drop_existing: bool = False
    on_off: "OnOff" = None
    maxdop: bool = False
    max_degree_of_parallelism: bool = False
    online: bool = False
    compression_delay: bool = False
    data_compression: bool = False
    columnstore: bool = False
    columnstore_archive: bool = False
    on_partitions: list["OnPartitions"] = None


@dataclass
class CreateNonclusteredColumnstoreIndex(TreeNode):
    left: "Id" = None
    table_name: "TableName" = None
    column_name_list_with_order: "ColumnNameListWithOrder" = None
    where: bool = False
    search_condition: "SearchCondition" = None
    create_columnstore_index_options: list["CreateColumnstoreIndexOptions"] = None
    left: bool = False
    right: "Id" = None


@dataclass
class CreateXmlIndex(TreeNode):
    left: "Id" = None
    table_name: "TableName" = None
    right: "Id" = None
    using: bool = False
    left: bool = False
    left: bool = False
    third: "Id" = None
    xml_index_options: list["XmlIndexOptions"] = None
    for_: bool = False
    value: bool = False
    path: bool = False
    property: bool = False


@dataclass
class XmlIndexOptions(TreeNode):
    left: "XmlIndexOption" = None
    right: list["XmlIndexOption"] = None


@dataclass
class XmlIndexOption(TreeNode):
    pad_index: bool = False
    on_off: "OnOff" = None
    fillfactor: bool = False
    decimal: bool = False
    sort_in_tempdb: bool = False
    ignore_dup_key: bool = False
    drop_existing: bool = False
    online: bool = False
    on: bool = False
    off: bool = False
    low_priority_lock_wait: "LowPriorityLockWait" = None
    allow_row_locks: bool = False
    allow_page_locks: bool = False
    maxdop: bool = False
    xml_compression: bool = False


@dataclass
class CreateOrAlterProcedure(TreeNode):
    left: bool = False
    create_or_alter_procedure_proc: "CreateOrAlterProcedureProc" = None
    proc_name: "FuncProcNameSchema" = None
    decimal: bool = False
    left: "ProcedureParam" = None
    with_: bool = False
    left: "ProcedureOption" = None
    for_: bool = False
    replication: bool = False
    as_external_name: "AsExternalName" = None
    sql_clauses: "SqlClauses" = None
    create: bool = False
    right: list["ProcedureParam"] = None
    right: list["ProcedureOption"] = None
    or_: bool = False
    right: bool = False
    replace: bool = False


@dataclass
class AsExternalName(TreeNode):
    assembly_name: "Id" = None


@dataclass
class CreateOrAlterTrigger(TreeNode):
    create_or_alter_dml_trigger: "CreateOrAlterDmlTrigger" = None
    create_or_alter_ddl_trigger: "CreateOrAlterDdlTrigger" = None


@dataclass
class CreateOrAlterDmlTrigger(TreeNode):
    create: bool = False
    left: bool = False
    simple_name: "SimpleName" = None
    table_name: "TableName" = None
    left: bool = False
    left: "DmlTriggerOption" = None
    left: bool = False
    after: bool = False
    instead: bool = False
    of: bool = False
    left: "DmlTriggerOperation" = None
    right: list["DmlTriggerOperation"] = None
    right: bool = False
    append_: bool = False
    not_: bool = False
    right: bool = False
    replication: bool = False
    sql_clauses: "SqlClauses" = None
    or_: bool = False
    right: list["DmlTriggerOption"] = None
    right: bool = False
    replace: bool = False


@dataclass
class DmlTriggerOption(TreeNode):
    encryption: bool = False
    execute_clause: "ExecuteClause" = None


@dataclass
class DmlTriggerOperation(TreeNode):
    insert: bool = False
    update: bool = False
    delete: bool = False


@dataclass
class CreateOrAlterDdlTrigger(TreeNode):
    create: bool = False
    left: bool = False
    simple_name: "SimpleName" = None
    all: bool = False
    server: bool = False
    database: bool = False
    with_: bool = False
    left: "DmlTriggerOption" = None
    for_: bool = False
    after: bool = False
    left: "SimpleId" = None
    right: list["SimpleId"] = None
    sql_clauses: "SqlClauses" = None
    or_: bool = False
    right: list["DmlTriggerOption"] = None
    right: bool = False
    replace: bool = False


@dataclass
class CreateOrAlterFunction(TreeNode):
    left: bool = False
    func_name: "FuncProcNameSchema" = None
    func_body_returns_select: "FuncBodyReturnsSelect" = None
    func_body_returns_table: "FuncBodyReturnsTable" = None
    func_body_returns_scalar: "FuncBodyReturnsScalar" = None
    create: bool = False
    left: "ProcedureParam" = None
    or_: bool = False
    right: bool = False
    right: list["ProcedureParam"] = None


@dataclass
class FuncBodyReturnsSelect(TreeNode):
    with_: bool = False
    left: "FunctionOption" = None
    as_external_name: "AsExternalName" = None
    return_: bool = False
    right: list["FunctionOption"] = None
    left: "SelectStatementStandalone" = None
    right: "SelectStatementStandalone" = None


@dataclass
class FuncBodyReturnsTable(TreeNode):
    local_id: str = None
    table_type_definition: "TableTypeDefinition" = None
    with_: bool = False
    left: "FunctionOption" = None
    as_external_name: "AsExternalName" = None
    begin: bool = False
    sql_clauses: "SqlClauses" = None
    return_: bool = False
    end: bool = False
    right: list["FunctionOption"] = None


@dataclass
class FuncBodyReturnsScalar(TreeNode):
    data_type: "DataType" = None
    with_: bool = False
    left: "FunctionOption" = None
    as_external_name: "AsExternalName" = None
    begin: bool = False
    sql_clauses: "SqlClauses" = None
    return_: bool = False
    ret: "Expression" = None
    end: bool = False
    right: list["FunctionOption"] = None


@dataclass
class ProcedureParamDefaultValue(TreeNode):
    null: bool = False
    default_: bool = False
    constant: "Constant" = None
    local_id: str = None


@dataclass
class ProcedureParam(TreeNode):
    local_id: str = None
    type_schema: "Id" = None
    data_type: "DataType" = None
    default_val: "ProcedureParamDefaultValue" = None
    out: bool = False
    output: bool = False
    readonly: bool = False


@dataclass
class ProcedureOption(TreeNode):
    encryption: bool = False
    recompile: bool = False
    execute_clause: "ExecuteClause" = None


@dataclass
class FunctionOption(TreeNode):
    encryption: bool = False
    schemabinding: bool = False
    returns: bool = False
    left: bool = False
    on: bool = False
    right: bool = False
    input: bool = False
    called: bool = False
    execute_clause: "ExecuteClause" = None


@dataclass
class CreateStatistics(TreeNode):
    id: "Id" = None
    table_name: "TableName" = None
    column_name_list: "ColumnNameList" = None
    with_: bool = False
    fullscan: bool = False
    sample: bool = False
    decimal: bool = False
    stats_stream: bool = False
    norecompute: bool = False
    incremental: bool = False
    equal: bool = False
    on_off: "OnOff" = None
    percent: bool = False
    rows: bool = False


@dataclass
class UpdateStatistics(TreeNode):
    full_table_name: "FullTableName" = None
    left: "Id" = None
    right: "Id" = None
    update_statistics_options: list["UpdateStatisticsOptions"] = None
    third: list["Id"] = None


@dataclass
class UpdateStatisticsOptions(TreeNode):
    left: "UpdateStatisticsOption" = None
    right: list["UpdateStatisticsOption"] = None


@dataclass
class UpdateStatisticsOption(TreeNode):
    fullscan: bool = False
    persist_sample_percent: bool = False
    on_off: "OnOff" = None
    sample: bool = False
    number: bool = False
    percent: bool = False
    rows: bool = False
    resample: bool = False
    on_partitions: list["OnPartitions"] = None
    stats_stream: bool = False
    stats_stream: "Expression" = None
    rowcount: bool = False
    pagecount: bool = False
    all: bool = False
    columns: bool = False
    index: bool = False
    norecompute: bool = False
    incremental: bool = False
    maxdop: bool = False
    auto_drop: bool = False


@dataclass
class CreateTable(TreeNode):
    table_name: "TableName" = None
    column_def_table_constraints: "ColumnDefTableConstraints" = None
    table_indices: list["TableIndices"] = None
    lock: bool = False
    simple_id: "SimpleId" = None
    table_options: list["TableOptions"] = None
    on: bool = False
    left: "Id" = None
    left: bool = False
    on_partition_or_filegroup: "OnPartitionOrFilegroup" = None
    textimage_on: bool = False
    right: "Id" = None
    right: bool = False


@dataclass
class TableIndices(TreeNode):
    index: bool = False
    id: "Id" = None
    clustered: list["Clustered"] = None
    column_name_list_with_order: "ColumnNameListWithOrder" = None
    clustered: bool = False
    columnstore: bool = False
    column_name_list: "ColumnNameList" = None
    create_table_index_options: list["CreateTableIndexOptions"] = None
    on: bool = False
    right: "Id" = None


@dataclass
class TableOptions(TreeNode):
    left: "TableOption" = None
    right: "TableOption" = None
    third: list["TableOption"] = None
    fourth: list["TableOption"] = None


@dataclass
class TableOption(TreeNode):
    left: "SimpleId" = None
    left: "Keyword" = None
    right: "SimpleId" = None
    right: "Keyword" = None
    on_off: "OnOff" = None
    decimal: bool = False
    clustered: bool = False
    columnstore: bool = False
    index: bool = False
    heap: bool = False
    fillfactor: bool = False
    distribution: bool = False
    hash: bool = False
    id: "Id" = None
    left: bool = False
    left: bool = False
    right: list["Id"] = None
    right: bool = False
    right: bool = False
    data_compression: bool = False
    none: bool = False
    row: bool = False
    page: bool = False
    on_partitions: list["OnPartitions"] = None
    xml_compression: bool = False


@dataclass
class CreateTableIndexOptions(TreeNode):
    left: "CreateTableIndexOption" = None
    right: list["CreateTableIndexOption"] = None


@dataclass
class CreateTableIndexOption(TreeNode):
    pad_index: bool = False
    on_off: "OnOff" = None
    fillfactor: bool = False
    decimal: bool = False
    ignore_dup_key: bool = False
    statistics_norecompute: bool = False
    statistics_incremental: bool = False
    allow_row_locks: bool = False
    allow_page_locks: bool = False
    optimize_for_sequential_key: bool = False
    data_compression: bool = False
    none: bool = False
    row: bool = False
    page: bool = False
    columnstore: bool = False
    columnstore_archive: bool = False
    on_partitions: list["OnPartitions"] = None
    xml_compression: bool = False


@dataclass
class CreateView(TreeNode):
    create: bool = False
    left: bool = False
    simple_name: "SimpleName" = None
    column_name_list: "ColumnNameList" = None
    left: bool = False
    left: "ViewAttribute" = None
    select_statement_standalone: "SelectStatementStandalone" = None
    right: bool = False
    check: bool = False
    option: bool = False
    or_: bool = False
    right: list["ViewAttribute"] = None
    right: bool = False
    replace: bool = False


@dataclass
class ViewAttribute(TreeNode):
    encryption: bool = False
    schemabinding: bool = False
    view_metadata: bool = False


@dataclass
class AlterTable(TreeNode):
    left: "TableName" = None
    set: bool = False
    lock_escalation: bool = False
    left: bool = False
    column_def_table_constraints: "ColumnDefTableConstraints" = None
    left: bool = False
    left: bool = False
    left: bool = False
    right: bool = False
    left: "Id" = None
    right: bool = False
    left: bool = False
    constraint: "Id" = None
    with_: bool = False
    right: bool = False
    right: bool = False
    constraint: "Id" = None
    trigger: bool = False
    fourth: "Id" = None
    rebuild: bool = False
    table_options: "TableOptions" = None
    switch_: bool = False
    switch_partition: "SwitchPartition" = None
    auto: bool = False
    left: bool = False
    left: bool = False
    column_definition: "ColumnDefinition" = None
    column_modifier: "ColumnModifier" = None
    fifth: list["Id"] = None
    left: bool = False
    left: bool = False
    third: bool = False
    constraint: "Id" = None
    foreign: bool = False
    key: bool = False
    fk: "ColumnNameList" = None
    references: bool = False
    right: "TableName" = None
    right: bool = False
    search_condition: "SearchCondition" = None
    right: bool = False
    third: bool = False
    enable: bool = False
    right: bool = False
    on_delete: list["OnDelete"] = None
    on_update: list["OnUpdate"] = None


@dataclass
class SwitchPartition(TreeNode):
    left: bool = False
    source_partition_number_expression: "Expression" = None
    target_table: "TableName" = None
    right: bool = False
    with_: bool = False
    low_priority_lock_wait: "LowPriorityLockWait" = None


@dataclass
class LowPriorityLockWait(TreeNode):
    max_duration: "Time" = None
    low_priority_lock_wait_abort_after_wait: "LowPriorityLockWaitAbortAfterWait" = None


@dataclass
class AlterDatabase(TreeNode):
    database: "Id" = None
    current: bool = False
    modify: bool = False
    name: bool = False
    collate: bool = False
    set: bool = False
    database_optionspec: "DatabaseOptionspec" = None
    add_or_modify_files: "AddOrModifyFiles" = None
    add_or_modify_filegroups: "AddOrModifyFilegroups" = None
    with_: bool = False
    termination: "Termination" = None


@dataclass
class AddOrModifyFiles(TreeNode):
    add: bool = False
    file: bool = False
    left: "Filespec" = None
    right: list["Filespec"] = None
    to: bool = False
    filegroup: bool = False
    filegroup_name: "Id" = None
    log: bool = False
    remove: bool = False
    modify: bool = False


@dataclass
class Filespec(TreeNode):
    name: "IdOrString" = None
    newname: bool = False
    filename: bool = False
    file_name: str = None
    size: bool = False
    size: "FileSize" = None
    maxsize: bool = False
    unlimited: bool = False
    filegrowth: bool = False
    offline: bool = False


@dataclass
class AddOrModifyFilegroups(TreeNode):
    add: bool = False
    filegroup: bool = False
    filegroup_name: "Id" = None
    left: bool = False
    filestream: bool = False
    right: bool = False
    memory_optimized_data: bool = False
    remove: bool = False
    modify: bool = False
    filegroup_updatability_option: "FilegroupUpdatabilityOption" = None
    default_: bool = False
    name: bool = False
    autogrow_single_file: bool = False
    autogrow_all_files: bool = False


@dataclass
class FilegroupUpdatabilityOption(TreeNode):
    readonly: bool = False
    readwrite: bool = False
    read_only: bool = False
    read_write: bool = False


@dataclass
class DatabaseOptionspec(TreeNode):
    auto_option: "AutoOption" = None
    change_tracking_option: "ChangeTrackingOption" = None
    containment_option: "ContainmentOption" = None
    cursor_option: "CursorOption" = None
    database_mirroring_option: "MirroringSetOption" = None
    date_correlation_optimization_option: "DateCorrelationOptimizationOption" = None
    db_encryption_option: "DbEncryptionOption" = None
    db_state_option: "DbStateOption" = None
    db_update_option: "DbUpdateOption" = None
    db_user_access_option: "DbUserAccessOption" = None
    delayed_durability_option: "DelayedDurabilityOption" = None
    external_access_option: "ExternalAccessOption" = None
    filestream: bool = False
    database_filestream_option: "DatabaseFilestreamOption" = None
    hadr_options: "HadrOptions" = None
    mixed_page_allocation_option: "MixedPageAllocationOption" = None
    parameterization_option: "ParameterizationOption" = None
    recovery_option: "RecoveryOption" = None
    service_broker_option: "ServiceBrokerOption" = None
    snapshot_option: "SnapshotOption" = None
    sql_option: "SqlOption" = None
    target_recovery_time_option: "TargetRecoveryTimeOption" = None
    termination: "Termination" = None


@dataclass
class AutoOption(TreeNode):
    auto_close: bool = False
    on_off: "OnOff" = None
    auto_create_statistics: bool = False
    off: bool = False
    left: bool = False
    incremental: bool = False
    equal: bool = False
    right: bool = False
    auto_shrink: bool = False
    auto_update_statistics: bool = False
    auto_update_statistics_async: bool = False


@dataclass
class ChangeTrackingOption(TreeNode):
    off: bool = False
    on: bool = False
    left: list["ChangeTrackingOptionList"] = None
    right: list["ChangeTrackingOptionList"] = None


@dataclass
class ChangeTrackingOptionList(TreeNode):
    auto_cleanup: bool = False
    equal: bool = False
    on_off: "OnOff" = None
    change_retention: bool = False
    decimal: bool = False
    days: bool = False
    hours: bool = False
    minutes: bool = False


@dataclass
class ContainmentOption(TreeNode):
    none: bool = False
    partial: bool = False


@dataclass
class CursorOption(TreeNode):
    cursor_close_on_commit: bool = False
    on_off: "OnOff" = None
    cursor_default: bool = False
    local: bool = False
    global_: bool = False


@dataclass
class AlterEndpoint(TreeNode):
    endpointname: "Id" = None
    authorization: bool = False
    state: bool = False
    left: bool = False
    alter_endpoint_state: "AlterEndpointState" = None
    endpoint_listener_clause: "EndpointListenerClause" = None
    left: bool = False
    tsql: bool = False
    left: bool = False
    left: bool = False
    right: bool = False
    service_broker: bool = False
    right: bool = False
    left: "EndpointAuthenticationClause" = None
    right: bool = False
    third: bool = False
    database_mirroring: bool = False
    third: bool = False
    right: "EndpointAuthenticationClause" = None
    left: bool = False
    role: bool = False
    right: bool = False
    third: bool = False
    right: bool = False
    left: "EndpointEncryptionAlogorithmClause" = None
    third: bool = False
    message_forwarding: bool = False
    third: bool = False
    fourth: bool = False
    message_forward_size: bool = False
    fourth: bool = False
    decimal: bool = False
    fifth: bool = False
    right: "EndpointEncryptionAlogorithmClause" = None
    witness: bool = False
    partner: bool = False
    all: bool = False
    enabled: bool = False
    disabled: bool = False


@dataclass
class MirroringSetOption(TreeNode):
    partner_option: "PartnerOption" = None
    witness_option: "WitnessOption" = None


@dataclass
class PartnerOption(TreeNode):
    partner_server: "PartnerServer" = None
    failover: bool = False
    force_service_allow_data_loss: bool = False
    off: bool = False
    resume: bool = False
    safety: bool = False
    full: bool = False
    suspend: bool = False
    timeout: bool = False
    decimal: bool = False


@dataclass
class WitnessOption(TreeNode):
    witness_server: "PartnerServer" = None
    off: bool = False


@dataclass
class PartnerServer(TreeNode):
    host: "Host" = None


@dataclass
class Host(TreeNode):
    id: "Id" = None
    dot: bool = False
    host: "Host" = None
    right: "Id" = None


@dataclass
class DateCorrelationOptimizationOption(TreeNode):
    on_off: "OnOff" = None


@dataclass
class DbEncryptionOption(TreeNode):
    on_off: "OnOff" = None


@dataclass
class DbStateOption(TreeNode):
    online: bool = False
    offline: bool = False
    emergency: bool = False


@dataclass
class DbUpdateOption(TreeNode):
    read_only: bool = False
    read_write: bool = False


@dataclass
class DbUserAccessOption(TreeNode):
    single_user: bool = False
    restricted_user: bool = False
    multi_user: bool = False


@dataclass
class DelayedDurabilityOption(TreeNode):
    disabled: bool = False
    allowed: bool = False
    forced: bool = False


@dataclass
class ExternalAccessOption(TreeNode):
    db_chaining: bool = False
    on_off: "OnOff" = None
    trustworthy: bool = False
    default_language: bool = False
    equal: bool = False
    id: "Id" = None
    string: str = None
    default_fulltext_language: bool = False
    nested_triggers: bool = False
    off: bool = False
    on: bool = False
    transform_noise_words: bool = False
    two_digit_year_cutoff: bool = False
    decimal: bool = False


@dataclass
class HadrOptions(TreeNode):
    availability: bool = False
    group: bool = False
    equal: bool = False
    availability_group_name: "Id" = None
    off: bool = False
    suspend: bool = False
    resume: bool = False


@dataclass
class MixedPageAllocationOption(TreeNode):
    off: bool = False
    on: bool = False


@dataclass
class ParameterizationOption(TreeNode):
    simple: bool = False
    forced: bool = False


@dataclass
class RecoveryOption(TreeNode):
    recovery: bool = False
    full: bool = False
    bulk_logged: bool = False
    simple: bool = False
    torn_page_detection: bool = False
    on_off: "OnOff" = None
    accelerated_database_recovery: bool = False
    page_verify: bool = False
    checksum: bool = False
    none: bool = False


@dataclass
class ServiceBrokerOption(TreeNode):
    enable_broker: bool = False
    disable_broker: bool = False
    new_broker: bool = False
    error_broker_conversations: bool = False
    honor_broker_priority: bool = False
    on_off: "OnOff" = None


@dataclass
class SnapshotOption(TreeNode):
    allow_snapshot_isolation: bool = False
    on_off: "OnOff" = None
    read_committed_snapshot: bool = False
    on: bool = False
    off: bool = False
    snapshot_option_memory_optimized_elevate_to_snapshot: "SnapshotOptionMemoryOptimizedElevateToSnapshot" = None


@dataclass
class SqlOption(TreeNode):
    ansi_null_default: bool = False
    on_off: "OnOff" = None
    ansi_nulls: bool = False
    ansi_padding: bool = False
    ansi_warnings: bool = False
    arithabort: bool = False
    compatibility_level: bool = False
    equal: bool = False
    decimal: bool = False
    concat_null_yields_null: bool = False
    numeric_roundabort: bool = False
    quoted_identifier: bool = False
    recursive_triggers: bool = False


@dataclass
class TargetRecoveryTimeOption(TreeNode):
    seconds: bool = False
    minutes: bool = False


@dataclass
class Termination(TreeNode):
    rollback: bool = False
    after: bool = False
    seconds: bool = False
    immediate: bool = False
    no_wait: bool = False


@dataclass
class DropIndex(TreeNode):
    if_: bool = False
    exists: bool = False
    left: "DropRelationalOrXmlOrSpatialIndex" = None
    left: "DropBackwardCompatibleIndex" = None
    right: list["DropRelationalOrXmlOrSpatialIndex"] = None
    right: list["DropBackwardCompatibleIndex"] = None


@dataclass
class DropRelationalOrXmlOrSpatialIndex(TreeNode):
    index_name: "Id" = None
    full_table_name: "FullTableName" = None


@dataclass
class DropBackwardCompatibleIndex(TreeNode):
    owner_name: "Id" = None


@dataclass
class DropProcedure(TreeNode):
    drop_procedure_proc: "DropProcedureProc" = None
    if_: bool = False
    exists: bool = False
    left: "FuncProcNameSchema" = None
    right: list["FuncProcNameSchema"] = None


@dataclass
class DropTrigger(TreeNode):
    drop_dml_trigger: "DropDmlTrigger" = None
    drop_ddl_trigger: "DropDdlTrigger" = None


@dataclass
class DropDmlTrigger(TreeNode):
    if_: bool = False
    exists: bool = False
    left: "SimpleName" = None
    right: list["SimpleName"] = None


@dataclass
class DropDdlTrigger(TreeNode):
    if_: bool = False
    exists: bool = False
    left: "SimpleName" = None
    right: list["SimpleName"] = None
    database: bool = False
    all: bool = False
    server: bool = False


@dataclass
class DropFunction(TreeNode):
    if_: bool = False
    exists: bool = False
    left: "FuncProcNameSchema" = None
    right: list["FuncProcNameSchema"] = None


@dataclass
class DropStatistics(TreeNode):
    name: list["Id"] = None
    table_name: "TableName" = None


@dataclass
class DropTable(TreeNode):
    if_: bool = False
    exists: bool = False
    left: "TableName" = None
    right: list["TableName"] = None


@dataclass
class DropView(TreeNode):
    if_: bool = False
    exists: bool = False
    left: "SimpleName" = None
    right: list["SimpleName"] = None


@dataclass
class CreateType(TreeNode):
    name: "SimpleName" = None
    from_: bool = False
    data_type: "DataType" = None
    as_: bool = False
    table: bool = False
    lr_bracket: bool = False
    column_def_table_constraints: "ColumnDefTableConstraints" = None
    rr_bracket: bool = False


@dataclass
class DropType(TreeNode):
    if_: bool = False
    exists: bool = False
    name: "SimpleName" = None


@dataclass
class RowsetFunctionLimited(TreeNode):
    openquery: "Openquery" = None
    opendatasource: "Opendatasource" = None


@dataclass
class Openquery(TreeNode):
    linked_server: "Id" = None
    query: str = None


@dataclass
class Opendatasource(TreeNode):
    provider: str = None
    database: "Id" = None


@dataclass
class DeclareStatement(TreeNode):
    declare: bool = False
    local_id: str = None
    data_type: "DataType" = None
    table_type_definition: "TableTypeDefinition" = None
    table_name: "TableName" = None
    loc: "DeclareLocal" = None
    xml_type_definition: "XmlTypeDefinition" = None
    with_: bool = False
    xmlnamespaces: bool = False
    xml_dec: "XmlDeclaration" = None


@dataclass
class XmlDeclaration(TreeNode):
    xml_namespace_uri: str = None
    as_: bool = False
    id: "Id" = None
    default_: bool = False


@dataclass
class CursorStatement(TreeNode):
    close: bool = False
    cursor_name: "CursorName" = None
    deallocate: bool = False
    declare_cursor: "DeclareCursor" = None
    fetch_cursor: "FetchCursor" = None
    open: bool = False


@dataclass
class BackupDatabase(TreeNode):
    database_name: "Id" = None
    read_write_filegroups: bool = False
    file_or_filegroup: list[str] = None
    left: bool = False
    right: bool = False
    with_: bool = False
    file_or_filegroup: list[str] = None
    left: bool = False
    left: bool = False
    logical_device_name: list["Id"] = None
    backup_set_name: list["Id"] = None
    right: bool = False
    right: bool = False
    left: bool = False
    left: bool = False
    left: bool = False
    third: str = None
    fourth: "Id" = None
    logical_device_name: list["Id"] = None
    compression: bool = False
    no_compression: bool = False
    fourth: str = None
    f_5: "Id" = None
    expiredate: bool = False
    left: bool = False
    retaindays: bool = False
    right: bool = False
    noinit: bool = False
    init: bool = False
    noskip: bool = False
    skip_keyword: bool = False
    noformat: bool = False
    format: bool = False
    fifth: str = None
    f_6: "Id" = None
    medianame: str = None
    left: bool = False
    f_7: "Id" = None
    right: bool = False
    f_8: "Id" = None
    third: bool = False
    f_9: "Id" = None
    no_checksum: bool = False
    checksum: bool = False
    stop_on_error: bool = False
    continue_after_error: bool = False
    third: bool = False
    stats_percent: bool = False
    rewind: bool = False
    norewind: bool = False
    load: bool = False
    nounload: bool = False
    aes_128: bool = False
    aes_192: bool = False
    aes_256: bool = False
    triple_des_3key: bool = False
    encryptor_name: "Id" = None
    left: bool = False
    asymmetric: bool = False
    key: bool = False
    fourth: bool = False
    encryptor_name: "Id" = None
    right: bool = False
    right: bool = False
    right: bool = False
    f_6: str = None
    f12: "Id" = None
    f_7: str = None
    f13: "Id" = None
    fifth: bool = False
    f14: "Id" = None


@dataclass
class BackupLog(TreeNode):
    database_name: "Id" = None
    left: bool = False
    right: bool = False
    with_: bool = False
    logical_device_name: list["Id"] = None
    backup_set_name: list["Id"] = None
    left: bool = False
    left: bool = False
    left: bool = False
    left: str = None
    fourth: "Id" = None
    logical_device_name: list["Id"] = None
    compression: bool = False
    no_compression: bool = False
    right: str = None
    f_5: "Id" = None
    expiredate: bool = False
    left: bool = False
    retaindays: bool = False
    right: bool = False
    noinit: bool = False
    init: bool = False
    noskip: bool = False
    skip_keyword: bool = False
    noformat: bool = False
    format: bool = False
    third: str = None
    f_6: "Id" = None
    medianame: str = None
    left: bool = False
    f_7: "Id" = None
    right: bool = False
    f_8: "Id" = None
    third: bool = False
    f_9: "Id" = None
    no_checksum: bool = False
    checksum: bool = False
    stop_on_error: bool = False
    continue_after_error: bool = False
    third: bool = False
    stats_percent: bool = False
    rewind: bool = False
    norewind: bool = False
    load: bool = False
    nounload: bool = False
    norecovery: bool = False
    standby: bool = False
    fourth: bool = False
    undo_file_name: str = None
    aes_128: bool = False
    aes_192: bool = False
    aes_256: bool = False
    triple_des_3key: bool = False
    encryptor_name: "Id" = None
    left: bool = False
    asymmetric: bool = False
    key: bool = False
    fifth: bool = False
    encryptor_name: "Id" = None
    right: bool = False
    right: bool = False
    right: bool = False
    f_5: str = None
    f12: "Id" = None
    f_6: str = None
    f13: "Id" = None
    fifth: bool = False
    f14: "Id" = None


@dataclass
class BackupCertificate(TreeNode):
    certname: "Id" = None
    cert_file: str = None
    with_: bool = False
    private: bool = False
    key: bool = False
    lr_bracket: bool = False
    rr_bracket: bool = False


@dataclass
class BackupMasterKey(TreeNode):
    master_key_backup_file: str = None


@dataclass
class BackupServiceMasterKey(TreeNode):
    service_master_key_backup_file: str = None


@dataclass
class KillStatement(TreeNode):
    kill_process: "KillProcess" = None
    kill_query_notification: "KillQueryNotification" = None


@dataclass
class KillProcess(TreeNode):
    kill_process_session_id: "KillProcessSessionId" = None
    uow: bool = False
    with_: bool = False
    statusonly: bool = False


@dataclass
class KillQueryNotification(TreeNode):
    all: bool = False
    subscription_id: bool = False


@dataclass
class ExecuteStatement(TreeNode):
    execute: str = None
    execute_body: "ExecuteBody" = None


@dataclass
class ExecuteBodyBatch(TreeNode):
    func_proc_name_server_database_schema: "FuncProcNameServerDatabaseSchema" = None
    left: "ExecuteStatementArg" = None
    right: list["ExecuteStatementArg"] = None


@dataclass
class ExecuteBody(TreeNode):
    return_status: str = None
    func_proc_name_server_database_schema: "FuncProcNameServerDatabaseSchema" = None
    execute_var_string: "ExecuteVarString" = None
    execute_statement_arg: list["ExecuteStatementArg"] = None
    right: list["ExecuteVarString"] = None
    as_: bool = False
    string: str = None
    at_keyword: bool = False
    linked_server: "Id" = None
    login: bool = False
    user: bool = False
    caller: bool = False


@dataclass
class ExecuteStatementArg(TreeNode):
    execute_statement_arg_unnamed: "ExecuteStatementArgUnnamed" = None
    execute_statement_arg: list["ExecuteStatementArg"] = None
    left: "ExecuteStatementArgNamed" = None
    right: list["ExecuteStatementArgNamed"] = None


@dataclass
class ExecuteStatementArgNamed(TreeNode):
    name: str = None
    value: "ExecuteParameter" = None


@dataclass
class ExecuteStatementArgUnnamed(TreeNode):
    value: "ExecuteParameter" = None


@dataclass
class ExecuteParameter(TreeNode):
    constant: "Constant" = None
    local_id: str = None
    id: "Id" = None
    default_: bool = False
    null: bool = False
    output: bool = False
    out: bool = False


@dataclass
class ExecuteVarString(TreeNode):
    left: str = None
    output: bool = False
    out: bool = False
    right: str = None
    execute_var_string: "ExecuteVarString" = None
    string: str = None


@dataclass
class SecurityStatement(TreeNode):
    execute_clause: "ExecuteClause" = None
    left: bool = False
    all: bool = False
    privileges: bool = False
    grant_permission: "GrantPermission" = None
    on: bool = False
    on_id: "TableName" = None
    to: bool = False
    to_principal: "PrincipalId" = None
    with_: bool = False
    right: bool = False
    option: bool = False
    as_: bool = False
    column_name_list: "ColumnNameList" = None
    class_type_for_grant: "ClassTypeForGrant" = None
    revert: bool = False
    cookie: bool = False
    local_id: str = None
    open_key: "OpenKey" = None
    close_key: "CloseKey" = None
    create_key: "CreateKey" = None
    create_certificate: "CreateCertificate" = None


@dataclass
class PrincipalId(TreeNode):
    id: "Id" = None
    public: bool = False


@dataclass
class CreateCertificate(TreeNode):
    certificate_name: "Id" = None
    authorization: bool = False
    from_: bool = False
    existing_keys: "ExistingKeys" = None
    generate_new_keys: "GenerateNewKeys" = None
    active: bool = False
    for_: bool = False
    begin: bool = False
    dialog: bool = False
    on_off: "OnOff" = None


@dataclass
class ExistingKeys(TreeNode):
    assembly: bool = False
    assembly_name: "Id" = None
    file: bool = False
    equal: bool = False
    path_to_file: str = None
    with_: bool = False
    private: bool = False
    key: bool = False
    private_key_options: "PrivateKeyOptions" = None


@dataclass
class PrivateKeyOptions(TreeNode):
    file: bool = False
    binary: str = None
    path: str = None
    by: bool = False
    password: bool = False
    decryption: bool = False
    encryption: bool = False


@dataclass
class GenerateNewKeys(TreeNode):
    encryption: bool = False
    by: bool = False
    password: bool = False
    password: str = None
    date_options: list["DateOptions"] = None


@dataclass
class DateOptions(TreeNode):
    start_date: bool = False
    expiry_date: bool = False
    string: str = None


@dataclass
class OpenKey(TreeNode):
    open: bool = False
    symmetric: bool = False
    key: bool = False
    key_name: "Id" = None
    decryption: bool = False
    by: bool = False
    decryption_mechanism: "DecryptionMechanism" = None
    master: bool = False
    password: bool = False
    password: str = None


@dataclass
class CloseKey(TreeNode):
    close: bool = False
    symmetric: bool = False
    key: bool = False
    key_name: "Id" = None
    all: bool = False
    keys: bool = False
    master: bool = False


@dataclass
class CreateKey(TreeNode):
    create: bool = False
    master: bool = False
    key: bool = False
    encryption: bool = False
    by: bool = False
    password: bool = False
    password: str = None
    symmetric: bool = False
    key_name: "Id" = None
    authorization: bool = False
    from_: bool = False
    provider: bool = False
    with_: bool = False
    key_options: "KeyOptions" = None
    encryption_mechanism: "EncryptionMechanism" = None


@dataclass
class KeyOptions(TreeNode):
    key_source: bool = False
    equal: bool = False
    pass_phrase: str = None
    algorithm: bool = False
    algorithm: "Algorithm" = None
    identity_value: bool = False
    provider_key_name: bool = False
    creation_disposition: bool = False
    create_new: bool = False
    open_existing: bool = False


@dataclass
class Algorithm(TreeNode):
    des: bool = False
    triple_des: bool = False
    triple_des_3key: bool = False
    rc2: bool = False
    rc4: bool = False
    rc4_128: bool = False
    desx: bool = False
    aes_128: bool = False
    aes_192: bool = False
    aes_256: bool = False


@dataclass
class EncryptionMechanism(TreeNode):
    certificate: bool = False
    certificate_name: "Id" = None
    asymmetric: bool = False
    key: bool = False
    symmetric: bool = False
    password: bool = False
    string: str = None


@dataclass
class DecryptionMechanism(TreeNode):
    certificate: bool = False
    certificate_name: "Id" = None
    with_: bool = False
    password: bool = False
    equal: bool = False
    string: str = None
    asymmetric: bool = False
    key: bool = False
    symmetric: bool = False


@dataclass
class GrantPermission(TreeNode):
    administer: bool = False
    left: bool = False
    left: bool = False
    database: bool = False
    right: bool = False
    right: bool = False
    alter: bool = False
    any: bool = False
    resources: bool = False
    left: bool = False
    state: bool = False
    settings: bool = False
    trace: bool = False
    application: bool = False
    left: bool = False
    assembly: bool = False
    asymmetric: bool = False
    left: bool = False
    availability: bool = False
    group: bool = False
    certificate: bool = False
    column: bool = False
    connection: bool = False
    contract: bool = False
    credential: bool = False
    dataspace: bool = False
    endpoint: bool = False
    left: bool = False
    external: bool = False
    fulltext: bool = False
    catalog: bool = False
    linked: bool = False
    right: bool = False
    login: bool = False
    mask: bool = False
    message: bool = False
    type_: bool = False
    remote: bool = False
    left: bool = False
    binding: bool = False
    right: bool = False
    route: bool = False
    schema: bool = False
    security: bool = False
    policy: bool = False
    third: bool = False
    right: bool = False
    symmetric: bool = False
    right: bool = False
    user: bool = False
    encryption: bool = False
    third: bool = False
    master: bool = False
    fourth: bool = False
    left: bool = False
    ddl: bool = False
    trigger: bool = False
    right: bool = False
    scoped: bool = False
    configuration: bool = False
    left: bool = False
    left: bool = False
    data: bool = False
    source: bool = False
    file: bool = False
    format: bool = False
    library: bool = False
    right: bool = False
    third: bool = False
    right: bool = False
    right: bool = False
    authenticate: bool = False
    backup: bool = False
    log: bool = False
    checkpoint: bool = False
    connect: bool = False
    replication: bool = False
    sql: bool = False
    control: bool = False
    create: bool = False
    aggregate: bool = False
    right: bool = False
    default_: bool = False
    function: bool = False
    procedure: bool = False
    queue: bool = False
    rule: bool = False
    sequence: bool = False
    synonym: bool = False
    table: bool = False
    right: bool = False
    view: bool = False
    xml: bool = False
    right: bool = False
    collection: bool = False
    right: bool = False
    third: bool = False
    third: bool = False
    delete: bool = False
    execute: str = None
    script: bool = False
    access: bool = False
    impersonate: bool = False
    insert: bool = False
    kill: bool = False
    receive: bool = False
    references: bool = False
    select_: bool = False
    all: bool = False
    securables: bool = False
    send: bool = False
    showplan: bool = False
    shutdown: bool = False
    subscribe: bool = False
    query: bool = False
    notifications: bool = False
    take: bool = False
    ownership: bool = False
    unmask: bool = False
    unsafe: bool = False
    update: bool = False
    change: bool = False
    tracking: bool = False
    left: bool = False
    right: bool = False
    right: bool = False
    third: bool = False


@dataclass
class SetStatement(TreeNode):
    set: bool = False
    local_id: str = None
    member_name: "Id" = None
    expression: "Expression" = None
    cursor: bool = False
    declare_set_cursor_common: "DeclareSetCursorCommon" = None
    for_: bool = False
    read: bool = False
    only: bool = False
    update: bool = False
    of: bool = False
    column_name_list: "ColumnNameList" = None
    set_special: "SetSpecial" = None


@dataclass
class TransactionStatement(TreeNode):
    begin: bool = False
    distributed: bool = False
    tran: bool = False
    transaction: bool = False
    id: "Id" = None
    local_id: str = None
    with_: bool = False
    mark: bool = False
    string: str = None
    commit: bool = False
    delayed_durability: bool = False
    equal: bool = False
    off: bool = False
    on: bool = False
    rollback: bool = False
    save: bool = False


@dataclass
class GoStatement(TreeNode):
    count: bool = False


@dataclass
class UseStatement(TreeNode):
    database: "Id" = None


@dataclass
class SetuserStatement(TreeNode):
    user: list[str] = None


@dataclass
class ReconfigureStatement(TreeNode):
    with_: bool = False
    override: bool = False


@dataclass
class ShutdownStatement(TreeNode):
    with_: bool = False
    nowait: bool = False


@dataclass
class CheckpointStatement(TreeNode):
    check_point_duration: bool = False


@dataclass
class DbccCheckallocOption(TreeNode):
    all_errormsgs: bool = False
    no_infomsgs: bool = False
    tablock: bool = False
    estimateonly: bool = False


@dataclass
class DbccCheckalloc(TreeNode):
    database: "Id" = None
    databaseid: str = None
    decimal: bool = False
    noindex: bool = False
    with_: bool = False
    dbcc_option: "DbccCheckallocOption" = None
    repair_allow_data_loss: bool = False
    repair_fast: bool = False
    repair_rebuild: bool = False


@dataclass
class DbccCheckcatalog(TreeNode):
    with_: bool = False
    dbcc_option: bool = False
    database: "Id" = None
    databasename: str = None
    decimal: bool = False


@dataclass
class DbccCheckconstraintsOption(TreeNode):
    all_constraints: bool = False
    all_errormsgs: bool = False
    no_infomsgs: bool = False


@dataclass
class DbccCheckconstraints(TreeNode):
    with_: bool = False
    dbcc_option: "DbccCheckconstraintsOption" = None
    table_or_constraint: "Id" = None
    table_or_constraint_name: str = None


@dataclass
class DbccCheckdbTableOption(TreeNode):
    all_errormsgs: bool = False
    extended_logical_checks: bool = False
    no_infomsgs: bool = False
    tablock: bool = False
    estimateonly: bool = False
    physical_only: bool = False
    data_purity: bool = False
    maxdop: bool = False
    max_dregree_of_parallelism: bool = False


@dataclass
class DbccCheckdb(TreeNode):
    with_: bool = False
    dbcc_option: "DbccCheckdbTableOption" = None
    database: "Id" = None
    databasename: str = None
    decimal: bool = False
    noindex: bool = False
    repair_allow_data_loss: bool = False
    repair_fast: bool = False
    repair_rebuild: bool = False


@dataclass
class DbccCheckfilegroupOption(TreeNode):
    all_errormsgs: bool = False
    no_infomsgs: bool = False
    tablock: bool = False
    estimateonly: bool = False
    physical_only: bool = False
    maxdop: bool = False
    max_dregree_of_parallelism: bool = False


@dataclass
class DbccCheckfilegroup(TreeNode):
    with_: bool = False
    dbcc_option: "DbccCheckfilegroupOption" = None
    filegroup_id: bool = False
    filegroup_name: str = None
    noindex: bool = False
    repair_allow_data_loss: bool = False
    repair_fast: bool = False
    repair_rebuild: bool = False


@dataclass
class DbccChecktable(TreeNode):
    table_or_view_name: str = None
    with_: bool = False
    dbcc_option: "DbccCheckdbTableOption" = None
    noindex: bool = False
    index_id: "Expression" = None
    repair_allow_data_loss: bool = False
    repair_fast: bool = False
    repair_rebuild: bool = False


@dataclass
class DbccCleantable(TreeNode):
    database: "Id" = None
    databasename: str = None
    decimal: bool = False
    with_: bool = False
    dbcc_option: bool = False


@dataclass
class DbccClonedatabaseOption(TreeNode):
    no_statistics: bool = False
    no_querystore: bool = False
    servicebroker: bool = False
    verify_clonedb: bool = False
    backup_clonedb: bool = False


@dataclass
class DbccClonedatabase(TreeNode):
    source_database: "Id" = None
    with_: bool = False
    dbcc_option: "DbccClonedatabaseOption" = None


@dataclass
class DbccPdwShowspaceused(TreeNode):
    tablename: "Id" = None
    with_: bool = False
    dbcc_option: bool = False


@dataclass
class DbccProccache(TreeNode):
    with_: bool = False
    dbcc_option: bool = False


@dataclass
class DbccShowcontigOption(TreeNode):
    all_indexes: bool = False
    tableresults: bool = False
    fast: bool = False
    all_levels: bool = False
    no_infomsgs: bool = False


@dataclass
class DbccShowcontig(TreeNode):
    table_or_view: "Expression" = None
    with_: bool = False
    dbcc_option: "DbccShowcontigOption" = None


@dataclass
class DbccShrinklog(TreeNode):
    size: bool = False
    with_: bool = False
    dbcc_option: bool = False
    default_: bool = False
    decimal: bool = False
    mb: bool = False
    gb: bool = False
    tb: bool = False


@dataclass
class DbccDbreindex(TreeNode):
    table: "IdOrString" = None
    with_: bool = False
    dbcc_option: bool = False
    fillfactor: "Expression" = None


@dataclass
class DbccDllFree(TreeNode):
    dllname: "Id" = None
    with_: bool = False
    dbcc_option: bool = False


@dataclass
class DbccDropcleanbuffers(TreeNode):
    compute: bool = False
    all: bool = False
    with_: bool = False
    dbcc_option: bool = False


@dataclass
class DbccClause(TreeNode):
    dbcc_checkalloc: "DbccCheckalloc" = None
    dbcc_checkcatalog: "DbccCheckcatalog" = None
    dbcc_checkconstraints: "DbccCheckconstraints" = None
    dbcc_checkdb: "DbccCheckdb" = None
    dbcc_checkfilegroup: "DbccCheckfilegroup" = None
    dbcc_checktable: "DbccChecktable" = None
    dbcc_cleantable: "DbccCleantable" = None
    dbcc_clonedatabase: "DbccClonedatabase" = None
    dbcc_dbreindex: "DbccDbreindex" = None
    dbcc_dll_free: "DbccDllFree" = None
    dbcc_dropcleanbuffers: "DbccDropcleanbuffers" = None
    dbcc_pdw_showspaceused: "DbccPdwShowspaceused" = None
    dbcc_proccache: "DbccProccache" = None
    dbcc_showcontig: "DbccShowcontig" = None
    dbcc_shrinklog: "DbccShrinklog" = None


@dataclass
class ExecuteClause(TreeNode):
    execute: str = None
    execute_clause_clause: "ExecuteClauseClause" = None


@dataclass
class DeclareLocal(TreeNode):
    local_id: str = None
    data_type: "DataType" = None
    expression: "Expression" = None


@dataclass
class TableTypeDefinition(TreeNode):
    column_def_table_constraints: "ColumnDefTableConstraints" = None
    table_type_indices: list["TableTypeIndices"] = None


@dataclass
class TableTypeIndices(TreeNode):
    unique: bool = False
    column_name_list_with_order: "ColumnNameListWithOrder" = None
    primary: bool = False
    key: bool = False
    index: bool = False
    id: "Id" = None
    clustered: bool = False
    nonclustered: bool = False
    check: bool = False
    search_condition: "SearchCondition" = None


@dataclass
class XmlTypeDefinition(TreeNode):
    content: bool = False
    document: bool = False
    xml_schema_collection: "XmlSchemaCollection" = None


@dataclass
class XmlSchemaCollection(TreeNode):
    left: str = None
    right: str = None


@dataclass
class ColumnDefTableConstraints(TreeNode):
    left: "ColumnDefTableConstraint" = None
    right: list["ColumnDefTableConstraint"] = None


@dataclass
class ColumnDefTableConstraint(TreeNode):
    column_definition: "ColumnDefinition" = None
    materialized_column_definition: "MaterializedColumnDefinition" = None
    table_constraint: "TableConstraint" = None


@dataclass
class ColumnDefinition(TreeNode):
    id: "Id" = None
    data_type: "DataType" = None
    as_: bool = False
    expression: "Expression" = None
    persisted: bool = False
    column_definition_element: list["ColumnDefinitionElement"] = None
    column_index: list["ColumnIndex"] = None


@dataclass
class ColumnDefinitionElement(TreeNode):
    filestream: bool = False
    collate: bool = False
    collation_name: "Id" = None
    sparse: bool = False
    masked: bool = False
    with_: bool = False
    function: bool = False
    mask_function: str = None
    constraint: bool = False
    default_: bool = False
    constant_expr: "Expression" = None
    identity: bool = False
    seed: bool = False
    not_: bool = False
    for_: bool = False
    replication: bool = False
    generated: bool = False
    always: bool = False
    as_: bool = False
    row: bool = False
    transaction_id: bool = False
    sequence_number: bool = False
    start: bool = False
    end: bool = False
    rowguidcol: bool = False
    encrypted: bool = False
    column_encryption_key: bool = False
    encryption_type: bool = False
    deterministic: bool = False
    randomized: bool = False
    algorithm: bool = False
    column_constraint: "ColumnConstraint" = None


@dataclass
class ColumnModifier(TreeNode):
    id: "Id" = None
    add: bool = False
    drop: bool = False
    rowguidcol: bool = False
    persisted: bool = False
    not_: bool = False
    for_: bool = False
    replication: bool = False
    sparse: bool = False
    hidden_keyword: bool = False
    masked: bool = False
    with_: bool = False
    left: bool = False
    left: bool = False
    left: str = None
    lr_bracket: bool = False
    right: bool = False
    right: bool = False
    right: str = None
    rr_bracket: bool = False


@dataclass
class MaterializedColumnDefinition(TreeNode):
    id: "Id" = None
    compute: bool = False
    as_: bool = False
    expression: "Expression" = None
    left: bool = False
    not_: bool = False
    right: bool = False


@dataclass
class ColumnConstraint(TreeNode):
    constraint: bool = False
    constraint: "Id" = None
    check_constraint: "CheckConstraint" = None
    clustered: "Clustered" = None
    primary_key_options: "PrimaryKeyOptions" = None
    foreign_key_options: "ForeignKeyOptions" = None
    primary: bool = False
    left: bool = False
    unique: bool = False
    foreign: bool = False
    right: bool = False


@dataclass
class ColumnIndex(TreeNode):
    index_name: "Id" = None
    clustered: list["Clustered"] = None
    create_table_index_options: list["CreateTableIndexOptions"] = None
    on_partition_or_filegroup: list["OnPartitionOrFilegroup"] = None
    filestream_on: bool = False
    null_double_quote: str = None


@dataclass
class OnPartitionOrFilegroup(TreeNode):
    filegroup: "Id" = None
    default_double_quote: str = None


@dataclass
class TableConstraint(TreeNode):
    constraint: bool = False
    constraint: "Id" = None
    check_constraint: "CheckConstraint" = None
    clustered: "Clustered" = None
    column_name_list_with_order: "ColumnNameListWithOrder" = None
    primary_key_options: "PrimaryKeyOptions" = None
    foreign: bool = False
    left: bool = False
    fk: "ColumnNameList" = None
    foreign_key_options: "ForeignKeyOptions" = None
    connection: bool = False
    left: "ConnectionNode" = None
    default_: bool = False
    constant_expr: "Expression" = None
    for_: bool = False
    primary: bool = False
    right: bool = False
    unique: bool = False
    right: list["ConnectionNode"] = None
    with_: bool = False
    values: bool = False


@dataclass
class ConnectionNode(TreeNode):
    from_node_table: "Id" = None


@dataclass
class PrimaryKeyOptions(TreeNode):
    with_: bool = False
    fillfactor: bool = False
    decimal: bool = False
    alter_table_index_options: list["AlterTableIndexOptions"] = None
    on_partition_or_filegroup: list["OnPartitionOrFilegroup"] = None


@dataclass
class ForeignKeyOptions(TreeNode):
    table_name: "TableName" = None
    pk: "ColumnNameList" = None
    on_delete: list["OnDelete"] = None
    on_update: list["OnUpdate"] = None
    not_: bool = False
    for_: bool = False
    replication: bool = False


@dataclass
class CheckConstraint(TreeNode):
    not_: bool = False
    for_: bool = False
    replication: bool = False
    search_condition: "SearchCondition" = None


@dataclass
class OnDelete(TreeNode):
    no: bool = False
    action: bool = False
    cascade: bool = False
    left: bool = False
    null: bool = False
    right: bool = False
    default_: bool = False


@dataclass
class OnUpdate(TreeNode):
    no: bool = False
    action: bool = False
    cascade: bool = False
    left: bool = False
    null: bool = False
    right: bool = False
    default_: bool = False


@dataclass
class AlterTableIndexOptions(TreeNode):
    left: "AlterTableIndexOption" = None
    right: list["AlterTableIndexOption"] = None


@dataclass
class AlterTableIndexOption(TreeNode):
    pad_index: bool = False
    on_off: "OnOff" = None
    fillfactor: bool = False
    decimal: bool = False
    ignore_dup_key: bool = False
    statistics_norecompute: bool = False
    allow_row_locks: bool = False
    allow_page_locks: bool = False
    optimize_for_sequential_key: bool = False
    sort_in_tempdb: bool = False
    maxdop: bool = False
    data_compression: bool = False
    none: bool = False
    row: bool = False
    page: bool = False
    columnstore: bool = False
    columnstore_archive: bool = False
    on_partitions: list["OnPartitions"] = None
    xml_compression: bool = False
    distribution: bool = False
    hash: bool = False
    id: "Id" = None
    clustered: bool = False
    index: bool = False
    left: bool = False
    left: bool = False
    right: list["Id"] = None
    right: bool = False
    right: bool = False
    online: bool = False
    on: bool = False
    off: bool = False
    low_priority_lock_wait: "LowPriorityLockWait" = None
    resumable: bool = False
    max_duration: bool = False


@dataclass
class DeclareCursor(TreeNode):
    cursor_name: "CursorName" = None
    left: bool = False
    scroll: bool = False
    right: bool = False
    left: bool = False
    select_statement_standalone: "SelectStatementStandalone" = None
    declare_set_cursor_common: "DeclareSetCursorCommon" = None
    semi_sensitive: bool = False
    insensitive: bool = False
    right: bool = False
    third: bool = False
    left: bool = False
    read: bool = False
    only: bool = False
    right: bool = False
    left: bool = False
    left: "ColumnNameList" = None
    right: bool = False
    right: "ColumnNameList" = None


@dataclass
class DeclareSetCursorCommon(TreeNode):
    declare_set_cursor_common_partial: list["DeclareSetCursorCommonPartial"] = None
    select_statement_standalone: "SelectStatementStandalone" = None


@dataclass
class DeclareSetCursorCommonPartial(TreeNode):
    local: bool = False
    global_: bool = False
    forward_only: bool = False
    scroll: bool = False
    static: bool = False
    keyset: bool = False
    dynamic: bool = False
    fast_forward: bool = False
    read_only: bool = False
    scroll_locks: bool = False
    optimistic: bool = False
    type_warning: bool = False


@dataclass
class FetchCursor(TreeNode):
    from_: bool = False
    cursor_name: "CursorName" = None
    into: bool = False
    left: str = None
    next: bool = False
    prior: bool = False
    first: bool = False
    last: bool = False
    expression: "Expression" = None
    right: list[str] = None
    absolute: bool = False
    relative: bool = False


@dataclass
class SetSpecial(TreeNode):
    set: bool = False
    left: "Id" = None
    right: "Id" = None
    constant_local_id: "ConstantLocalId" = None
    on_off: "OnOff" = None
    statistics: bool = False
    io: bool = False
    time: bool = False
    xml: bool = False
    profile: bool = False
    rowcount: bool = False
    local_id: str = None
    decimal: bool = False
    textsize: bool = False
    transaction: bool = False
    isolation: bool = False
    level: bool = False
    left: bool = False
    uncommitted: bool = False
    right: bool = False
    committed: bool = False
    repeatable: bool = False
    third: bool = False
    snapshot: bool = False
    serializable: bool = False
    identity_insert: bool = False
    table_name: "TableName" = None
    left: "SpecialList" = None
    right: list["SpecialList"] = None
    modify_method: "ModifyMethod" = None


@dataclass
class SpecialList(TreeNode):
    ansi_nulls: bool = False
    quoted_identifier: bool = False
    ansi_padding: bool = False
    ansi_warnings: bool = False
    ansi_defaults: bool = False
    ansi_null_dflt_off: bool = False
    ansi_null_dflt_on: bool = False
    arithabort: bool = False
    arithignore: bool = False
    concat_null_yields_null: bool = False
    cursor_close_on_commit: bool = False
    fmtonly: bool = False
    forceplan: bool = False
    implicit_transactions: bool = False
    nocount: bool = False
    noexec: bool = False
    numeric_roundabort: bool = False
    parseonly: bool = False
    remote_proc_transactions: bool = False
    showplan_all: bool = False
    showplan_text: bool = False
    showplan_xml: bool = False
    xact_abort: bool = False


@dataclass
class ConstantLocalId(TreeNode):
    constant: "Constant" = None
    local_id: str = None


@dataclass
class Expression(TreeNode):
    primitive_expression: "PrimitiveExpression" = None
    function_call: "FunctionCall" = None
    expression: "Expression" = None
    value_call: "ValueCall" = None
    query_call: "QueryCall" = None
    exist_call: "ExistCall" = None
    modify_call: "ModifyCall" = None
    hierarchyid_call: "HierarchyidCall" = None
    collate: bool = False
    id: "Id" = None
    case_expression: "CaseExpression" = None
    full_column_name: "FullColumnName" = None
    bracket_expression: "BracketExpression" = None
    unary_operator_expression: "UnaryOperatorExpression" = None
    right: "Expression" = None
    time_zone: "TimeZone" = None
    over_clause: "OverClause" = None
    dollar_action: bool = False


@dataclass
class TimeZone(TreeNode):
    expression: "Expression" = None


@dataclass
class PrimitiveExpression(TreeNode):
    default_: bool = False
    null: bool = False
    local_id: str = None
    primitive_constant: "PrimitiveConstant" = None


@dataclass
class CaseExpression(TreeNode):
    case_: bool = False
    case_expr: "Expression" = None
    switch_section: "SwitchSection" = None
    else_: bool = False
    end: bool = False
    switch_search_condition_section: "SwitchSearchConditionSection" = None


@dataclass
class UnaryOperatorExpression(TreeNode):
    expression: "Expression" = None


@dataclass
class BracketExpression(TreeNode):
    expression: "Expression" = None
    subquery: "SelectStatement" = None


@dataclass
class WithExpression(TreeNode):
    ctes: "CommonTableExpression" = None


@dataclass
class CommonTableExpression(TreeNode):
    expression_name: "Id" = None
    columns: "ColumnNameList" = None
    cte_query: "SelectStatement" = None


@dataclass
class UpdateElem(TreeNode):
    local_id: str = None
    full_column_name: "FullColumnName" = None
    expression: "Expression" = None
    udt_column_name: "Id" = None
    expression_list: "ExpressionList" = None


@dataclass
class UpdateElemMerge(TreeNode):
    full_column_name: "FullColumnName" = None
    local_id: str = None
    expression: "Expression" = None
    udt_column_name: "Id" = None
    expression_list: "ExpressionList" = None


@dataclass
class SearchCondition(TreeNode):
    predicate: "Predicate" = None
    search_condition: "SearchCondition" = None
    and_: bool = False
    right: "SearchCondition" = None
    or_: bool = False


@dataclass
class Predicate(TreeNode):
    exists: bool = False
    subquery: "SelectStatement" = None
    freetext_predicate: "FreetextPredicate" = None
    left: "Expression" = None
    right: "Expression" = None
    mult_assign: bool = False
    all: bool = False
    some: bool = False
    any: bool = False
    between: bool = False
    and_: bool = False
    third: "Expression" = None
    in_: bool = False
    expression_list: "ExpressionList" = None
    like: bool = False
    escape: bool = False
    is_: bool = False


@dataclass
class QueryExpression(TreeNode):
    query_specification: "QuerySpecification" = None
    select_order_by_clause: list["SelectOrderByClause"] = None
    unions: list["SqlUnion"] = None
    left: "QueryExpression" = None
    union: bool = False
    all: bool = False
    right: "QueryExpression" = None


@dataclass
class SqlUnion(TreeNode):
    union: bool = False
    all: bool = False
    except_: bool = False
    intersect: bool = False
    spec: "QuerySpecification" = None
    op: "QueryExpression" = None


@dataclass
class QuerySpecification(TreeNode):
    top: list["TopClause"] = None
    columns: "SelectList" = None
    into: bool = False
    into: "TableName" = None
    from_: bool = False
    from_: "TableSources" = None
    where: bool = False
    where: "SearchCondition" = None
    group: bool = False
    by: bool = False
    having: bool = False
    grouping: bool = False
    sets: bool = False
    group_sets: "GroupingSetsItem" = None
    group_by_all: bool = False
    group_bys: "Expression" = None


@dataclass
class TopClause(TreeNode):
    top_percent: "TopPercent" = None
    top_count: "TopCount" = None
    with_: bool = False
    ties: bool = False


@dataclass
class TopPercent(TreeNode):
    top_percent_percent_constant: "TopPercentPercentConstant" = None
    percent: bool = False
    topper_expression: "Expression" = None


@dataclass
class TopCount(TreeNode):
    count_constant: bool = False
    topcount_expression: "Expression" = None


@dataclass
class OrderByClause(TreeNode):
    order_bys: "OrderByExpression" = None


@dataclass
class SelectOrderByClause(TreeNode):
    order_by_clause: "OrderByClause" = None
    offset: bool = False
    offset_exp: "Expression" = None
    select_order_by_clause_offset_rows: "SelectOrderByClauseOffsetRows" = None
    fetch: bool = False
    select_order_by_clause_fetch_offset: "SelectOrderByClauseFetchOffset" = None
    select_order_by_clause_fetch_rows: "SelectOrderByClauseFetchRows" = None
    only: bool = False


@dataclass
class ForClause(TreeNode):
    for_: bool = False
    browse: bool = False
    xml: bool = False
    raw: bool = False
    auto: bool = False
    xml_common_directives: list["XmlCommonDirectives"] = None
    left: bool = False
    right: bool = False
    elements: bool = False
    left: str = None
    xmldata: bool = False
    xmlschema: bool = False
    xsinil: bool = False
    absent: bool = False
    right: str = None
    explicit: bool = False
    path: bool = False
    json: bool = False
    root: bool = False
    include_null_values: bool = False
    without_array_wrapper: bool = False


@dataclass
class XmlCommonDirectives(TreeNode):
    binary_keyword: bool = False
    base64: bool = False
    type_: bool = False
    root: bool = False
    string: str = None


@dataclass
class OrderByExpression(TreeNode):
    order_by: "Expression" = None
    ascending: bool = False
    descending: bool = False


@dataclass
class GroupingSetsItem(TreeNode):
    group_set_items: "Expression" = None


@dataclass
class OptionClause(TreeNode):
    options: "Option" = None


@dataclass
class Option(TreeNode):
    fast: bool = False
    number_rows: bool = False
    hash: bool = False
    order: bool = False
    group: bool = False
    merge: bool = False
    concat: bool = False
    union: bool = False
    loop: bool = False
    join: bool = False
    expand: bool = False
    views: bool = False
    force: bool = False
    ignore_nonclustered_columnstore_index: bool = False
    keep: bool = False
    plan: bool = False
    keepfixed: bool = False
    maxdop: bool = False
    maxrecursion: bool = False
    optimize: bool = False
    for_: bool = False
    left: "OptimizeForArg" = None
    right: list["OptimizeForArg"] = None
    unknown: bool = False
    parameterization: bool = False
    simple: bool = False
    forced: bool = False
    recompile: bool = False
    robust: bool = False
    use: bool = False
    string: str = None


@dataclass
class OptimizeForArg(TreeNode):
    local_id: str = None
    unknown: bool = False
    constant: "Constant" = None
    null: bool = False


@dataclass
class SelectList(TreeNode):
    select_element: "SelectListElem" = None


@dataclass
class UdtMethodArguments(TreeNode):
    argument: "ExecuteVarString" = None


@dataclass
class Asterisk(TreeNode):
    table_name: "TableName" = None
    inserted: bool = False
    deleted: bool = False


@dataclass
class UdtElem(TreeNode):
    udt_column_name: "Id" = None
    udt_method_arguments: "UdtMethodArguments" = None
    as_column_alias: list["AsColumnAlias"] = None
    double_colon: bool = False


@dataclass
class ExpressionElem(TreeNode):
    left_alias: "ColumnAlias" = None
    left_assignment: "Expression" = None
    as_column_alias: list["AsColumnAlias"] = None


@dataclass
class SelectListElem(TreeNode):
    asterisk: "Asterisk" = None
    udt_elem: "UdtElem" = None
    local_id: str = None
    expression: "Expression" = None
    expression_elem: "ExpressionElem" = None


@dataclass
class TableSources(TreeNode):
    non_ansi_join: "NonAnsiJoin" = None
    source: "TableSource" = None


@dataclass
class NonAnsiJoin(TreeNode):
    source: "TableSource" = None


@dataclass
class TableSource(TreeNode):
    table_source_item: "TableSourceItem" = None
    joins: list["JoinPart"] = None


@dataclass
class TableSourceItem(TreeNode):
    full_table_name: "FullTableName" = None
    deprecated_table_hint: "DeprecatedTableHint" = None
    as_table_alias: "AsTableAlias" = None
    with_table_hints: "WithTableHints" = None
    sybase_legacy_hints: "SybaseLegacyHint" = None
    rowset_function: "RowsetFunction" = None
    derived_table: "DerivedTable" = None
    column_alias_list: "ColumnAliasList" = None
    change_table: "ChangeTable" = None
    nodes_method: "NodesMethod" = None
    function_call: "FunctionCall" = None
    loc_id: str = None
    open_xml: "OpenXml" = None
    open_json: "OpenJson" = None
    double_colon: bool = False
    table_source: "TableSource" = None


@dataclass
class OpenXml(TreeNode):
    left: "Expression" = None
    right: "Expression" = None
    third: "Expression" = None
    with_: bool = False
    schema_declaration: "SchemaDeclaration" = None
    as_table_alias: list["AsTableAlias"] = None


@dataclass
class OpenJson(TreeNode):
    left: "Expression" = None
    right: "Expression" = None
    with_: bool = False
    json_declaration: "JsonDeclaration" = None
    as_table_alias: list["AsTableAlias"] = None


@dataclass
class JsonDeclaration(TreeNode):
    json_col: "JsonColumnDeclaration" = None


@dataclass
class JsonColumnDeclaration(TreeNode):
    column_declaration: "ColumnDeclaration" = None
    as_: bool = False
    json: bool = False


@dataclass
class SchemaDeclaration(TreeNode):
    xml_col: "ColumnDeclaration" = None


@dataclass
class ColumnDeclaration(TreeNode):
    id: "Id" = None
    data_type: "DataType" = None
    string: list[str] = None


@dataclass
class ChangeTable(TreeNode):
    change_table_changes: "ChangeTableChanges" = None
    change_table_version: "ChangeTableVersion" = None


@dataclass
class ChangeTableChanges(TreeNode):
    changetable: "TableName" = None
    change_table_changes_changesid: "ChangeTableChangesChangesid" = None


@dataclass
class ChangeTableVersion(TreeNode):
    versiontable: "TableName" = None
    pk_columns: "FullColumnNameList" = None
    pk_values: "SelectList" = None


@dataclass
class JoinPart(TreeNode):
    join_on: "JoinOn" = None
    cross_join: "CrossJoin" = None
    apply: "Apply" = None
    pivot: "Pivot" = None
    unpivot: "Unpivot" = None


@dataclass
class JoinOn(TreeNode):
    inner: bool = False
    join_on_join_type: "JoinOnJoinType" = None
    outer: bool = False
    join_on_join_hint: "JoinOnJoinHint" = None
    source: "TableSource" = None
    cond: "SearchCondition" = None


@dataclass
class CrossJoin(TreeNode):
    table_source_item: "TableSourceItem" = None


@dataclass
class Apply(TreeNode):
    apply_apply_style: "ApplyApplyStyle" = None
    source: "TableSourceItem" = None


@dataclass
class Pivot(TreeNode):
    pivot_clause: "PivotClause" = None
    as_table_alias: "AsTableAlias" = None


@dataclass
class Unpivot(TreeNode):
    unpivot_clause: "UnpivotClause" = None
    as_table_alias: "AsTableAlias" = None


@dataclass
class PivotClause(TreeNode):
    aggregate_windowed_function: "AggregateWindowedFunction" = None
    full_column_name: "FullColumnName" = None
    column_alias_list: "ColumnAliasList" = None


@dataclass
class UnpivotClause(TreeNode):
    unpivot_exp: "Expression" = None
    full_column_name: "FullColumnName" = None
    full_column_name_list: "FullColumnNameList" = None


@dataclass
class FullColumnNameList(TreeNode):
    column: "FullColumnName" = None


@dataclass
class RowsetFunction(TreeNode):
    openrowset: bool = False
    lr_bracket: bool = False
    provider_name: str = None
    left: bool = False
    right: bool = False
    rr_bracket: bool = False
    bulk: bool = False
    left: "BulkOption" = None
    id: "Id" = None
    right: list["BulkOption"] = None


@dataclass
class BulkOption(TreeNode):
    id: "Id" = None
    bulk_option_bulk_option_value: "BulkOptionBulkOptionValue" = None


@dataclass
class DerivedTable(TreeNode):
    subquery: "SelectStatement" = None
    right: list["SelectStatement"] = None
    table_value_constructor: "TableValueConstructor" = None


@dataclass
class FunctionCall(TreeNode):
    ranking_windowed_function: "RankingWindowedFunction" = None
    aggregate_windowed_function: "AggregateWindowedFunction" = None
    analytic_windowed_function: "AnalyticWindowedFunction" = None
    built_in_functions: "BuiltInFunctions" = None
    scalar_function_name: "ScalarFunctionName" = None
    expression_list: list["ExpressionList"] = None
    freetext_function: "FreetextFunction" = None
    partition_function: "PartitionFunction" = None
    hierarchyid_static_method: "HierarchyidStaticMethod" = None


@dataclass
class PartitionFunction(TreeNode):
    database: "Id" = None
    expression: "Expression" = None


@dataclass
class FreetextFunction(TreeNode):
    containstable: bool = False
    freetexttable: bool = False
    table_name: "TableName" = None
    left: "FullColumnName" = None
    right: "FullColumnName" = None
    left: "Expression" = None
    language: bool = False
    right: "Expression" = None
    third: "Expression" = None
    third: list["FullColumnName"] = None
    semanticsimilaritytable: bool = False
    semantickeyphrasetable: bool = False
    semanticsimilaritydetailstable: bool = False


@dataclass
class FreetextPredicate(TreeNode):
    contains: bool = False
    left: "FullColumnName" = None
    right: "FullColumnName" = None
    property: bool = False
    third: "FullColumnName" = None
    left: "Expression" = None
    right: "Expression" = None
    fourth: list["FullColumnName"] = None
    freetext: bool = False
    table_name: "TableName" = None
    language: bool = False


@dataclass
class JsonKeyValue(TreeNode):
    json_key_name: "Expression" = None


@dataclass
class JsonNullClause(TreeNode):
    absent: bool = False
    left: bool = False


@dataclass
class BuiltInFunctions(TreeNode):
    app_name: bool = False
    applock_mode: bool = False
    database_principal: "Expression" = None
    applock_test: bool = False
    assemblyproperty: bool = False
    col_length: bool = False
    col_name: bool = False
    columnproperty: bool = False
    databasepropertyex: bool = False
    db_id: bool = False
    db_name: bool = False
    file_id: bool = False
    file_idex: bool = False
    file_name: bool = False
    filegroup_id: bool = False
    filegroup_name: bool = False
    filegroupproperty: bool = False
    fileproperty: bool = False
    filepropertyex: bool = False
    fulltextcatalogproperty: bool = False
    fulltextserviceproperty: bool = False
    index_col: bool = False
    indexkey_property: bool = False
    indexproperty: bool = False
    next: bool = False
    value: bool = False
    for_: bool = False
    sequence_name: "TableName" = None
    over: bool = False
    order_by_clause: "OrderByClause" = None
    object_definition: bool = False
    object_id: bool = False
    object_name: bool = False
    object_schema_name: bool = False
    objectproperty: bool = False
    objectpropertyex: bool = False
    original_db_name: bool = False
    parsename: bool = False
    schema_id: bool = False
    schema_name: bool = False
    scope_identity: bool = False
    serverproperty: bool = False
    stats_date: bool = False
    type_id: bool = False
    type_name: bool = False
    typeproperty: bool = False
    ascii: bool = False
    char: bool = False
    charindex: bool = False
    concat: bool = False
    concat_ws: bool = False
    difference: bool = False
    format: bool = False
    left: bool = False
    len_: bool = False
    lower: bool = False
    ltrim: bool = False
    nchar: bool = False
    patindex: bool = False
    quotename: bool = False
    replace: bool = False
    replicate: bool = False
    reverse: bool = False
    right: bool = False
    rtrim: bool = False
    soundex: bool = False
    space_keyword: bool = False
    str: bool = False
    string_agg: bool = False
    within: bool = False
    group: bool = False
    string_escape: bool = False
    stuff: bool = False
    substring: bool = False
    translate: bool = False
    trim: bool = False
    from_: bool = False
    unicode: bool = False
    upper: bool = False
    binary_checksum: bool = False
    right: list["Expression"] = None
    checksum: bool = False
    compress: bool = False
    connectionproperty: bool = False
    property: str = None
    context_info: bool = False
    current_request_id: bool = False
    current_transaction_id: bool = False
    decompress: bool = False
    error_line: bool = False
    error_message: bool = False
    error_number: bool = False
    error_procedure: bool = False
    error_severity: bool = False
    error_state: bool = False
    formatmessage: bool = False
    msg_number: bool = False
    msg_variable: str = None
    get_filestream_transaction_context: bool = False
    getansinull: bool = False
    host_id: bool = False
    host_name: bool = False
    isnull: bool = False
    isnumeric: bool = False
    min_active_rowversion: bool = False
    newid: bool = False
    newsequentialid: bool = False
    rowcount_big: bool = False
    session_context: bool = False
    xact_state: bool = False
    cast: bool = False
    as_: bool = False
    data_type: "DataType" = None
    try_cast: bool = False
    convert: str = None
    coalesce: bool = False
    expression_list: "ExpressionList" = None
    cursor_rows: bool = False
    fetch_status: bool = False
    cursor_status: bool = False
    cert_id: bool = False
    datalength: bool = False
    ident_current: bool = False
    ident_incr: bool = False
    ident_seed: bool = False
    identity: bool = False
    sql_variant_property: bool = False
    current_date: bool = False
    current_timestamp: bool = False
    current_timezone: bool = False
    current_timezone_id: bool = False
    date_bucket: bool = False
    datepart: "Dateparts9" = None
    dateadd: bool = False
    datepart: "Dateparts12" = None
    datediff: bool = False
    datediff_big: bool = False
    datefromparts: bool = False
    datename: bool = False
    datepart: "Dateparts15" = None
    datepart: bool = False
    datetime2fromparts: bool = False
    datetimefromparts: bool = False
    datetimeoffsetfromparts: bool = False
    datetrunc: bool = False
    datepart: "DatepartsDatetrunc" = None
    day: bool = False
    eomonth: bool = False
    getdate: bool = False
    getutcdate: bool = False
    isdate: bool = False
    month: bool = False
    smalldatetimefromparts: bool = False
    switchoffset: bool = False
    sysdatetime: bool = False
    sysdatetimeoffset: bool = False
    sysutcdatetime: bool = False
    timefromparts: bool = False
    todatetimeoffset: bool = False
    year: bool = False
    nullif: bool = False
    parse: str = None
    using: bool = False
    xml_data_type_methods: "XmlDataTypeMethods" = None
    iif: bool = False
    cond: "SearchCondition" = None
    isjson: bool = False
    json_object: bool = False
    key_value: "JsonKeyValue" = None
    json_null_clause: list["JsonNullClause"] = None
    json_array: bool = False
    json_value: bool = False
    json_query: bool = False
    json_modify: bool = False
    json_path_exists: bool = False
    abs: bool = False
    acos: bool = False
    asin: bool = False
    atan: bool = False
    atn2: bool = False
    ceiling: bool = False
    cos: bool = False
    cot: bool = False
    degrees: bool = False
    exp: bool = False
    floor: bool = False
    log: bool = False
    log10: bool = False
    pi: bool = False
    power: bool = False
    radians: bool = False
    rand: bool = False
    round: bool = False
    sign: bool = False
    sin: bool = False
    sqrt: bool = False
    square: bool = False
    tan: bool = False
    greatest: bool = False
    least: bool = False
    certencoded: bool = False
    certprivatekey: bool = False
    current_user: bool = False
    database_principal_id: bool = False
    has_dbaccess: bool = False
    has_perms_by_name: bool = False
    is_member: bool = False
    is_rolemember: bool = False
    is_srvrolemember: bool = False
    loginproperty: bool = False
    original_login: bool = False
    permissions: bool = False
    pwdencrypt: bool = False
    pwdcompare: bool = False
    session_user: bool = False
    sessionproperty: bool = False
    suser_id: bool = False
    suser_name: bool = False
    suser_sid: bool = False
    suser_sname: bool = False
    system_user: bool = False
    user: bool = False
    user_id: bool = False
    user_name: bool = False


@dataclass
class XmlDataTypeMethods(TreeNode):
    value_method: "ValueMethod" = None
    query_method: "QueryMethod" = None
    exist_method: "ExistMethod" = None
    modify_method: "ModifyMethod" = None


@dataclass
class Dateparts9(TreeNode):
    year: bool = False
    year_abbr: str = None
    quarter: bool = False
    quarter_abbr: str = None
    month: bool = False
    month_abbr: str = None
    day: bool = False
    day_abbr: str = None
    week: bool = False
    week_abbr: str = None
    hour: bool = False
    hour_abbr: bool = False
    minute: bool = False
    minute_abbr: str = None
    second: bool = False
    second_abbr: str = None
    millisecond: bool = False
    millisecond_abbr: bool = False


@dataclass
class Dateparts12(TreeNode):
    dateparts_9: "Dateparts9" = None
    dayofyear: bool = False
    dayofyear_abbr: str = None
    microsecond: bool = False
    microsecond_abbr: bool = False
    nanosecond: bool = False
    nanosecond_abbr: bool = False


@dataclass
class Dateparts15(TreeNode):
    dateparts_12: "Dateparts12" = None
    weekday: bool = False
    weekday_abbr: bool = False
    tzoffset: bool = False
    tzoffset_abbr: bool = False
    iso_week: bool = False
    iso_week_abbr: str = None


@dataclass
class DatepartsDatetrunc(TreeNode):
    dateparts_9: "Dateparts9" = None
    dayofyear: bool = False
    dayofyear_abbr: str = None
    microsecond: bool = False
    microsecond_abbr: bool = False
    iso_week: bool = False
    iso_week_abbr: str = None


@dataclass
class ValueMethod(TreeNode):
    loc_id: str = None
    value_id: "FullColumnName" = None
    eventdata: bool = False
    query: "QueryMethod" = None
    subquery: "SelectStatement" = None
    call: "ValueCall" = None


@dataclass
class ValueCall(TreeNode):
    value: bool = False
    value_square_bracket: bool = False
    xquery: str = None


@dataclass
class QueryMethod(TreeNode):
    loc_id: str = None
    value_id: "FullColumnName" = None
    subquery: "SelectStatement" = None
    call: "QueryCall" = None


@dataclass
class QueryCall(TreeNode):
    query: bool = False
    query_square_bracket: bool = False
    xquery: str = None


@dataclass
class ExistMethod(TreeNode):
    loc_id: str = None
    value_id: "FullColumnName" = None
    subquery: "SelectStatement" = None
    call: "ExistCall" = None


@dataclass
class ExistCall(TreeNode):
    exist: bool = False
    exist_square_bracket: bool = False
    xquery: str = None


@dataclass
class ModifyMethod(TreeNode):
    loc_id: str = None
    value_id: "FullColumnName" = None
    subquery: "SelectStatement" = None
    call: "ModifyCall" = None


@dataclass
class ModifyCall(TreeNode):
    modify: bool = False
    modify_square_bracket: bool = False
    xml_dml: str = None


@dataclass
class HierarchyidCall(TreeNode):
    getancestor: bool = False
    n: "Expression" = None
    getdescendant: bool = False
    getlevel: bool = False
    isdescendantof: bool = False
    getreparentedvalue: bool = False
    tostring: bool = False


@dataclass
class HierarchyidStaticMethod(TreeNode):
    getroot: bool = False
    parse: str = None
    input: "Expression" = None


@dataclass
class NodesMethod(TreeNode):
    loc_id: str = None
    value_id: "FullColumnName" = None
    subquery: "SelectStatement" = None
    xquery: str = None


@dataclass
class SwitchSection(TreeNode):
    left: "Expression" = None
    right: "Expression" = None


@dataclass
class SwitchSearchConditionSection(TreeNode):
    search_condition: "SearchCondition" = None
    expression: "Expression" = None


@dataclass
class AsColumnAlias(TreeNode):
    column_alias: "ColumnAlias" = None


@dataclass
class AsTableAlias(TreeNode):
    table_alias: "Id" = None


@dataclass
class WithTableHints(TreeNode):
    hint: "TableHint" = None


@dataclass
class DeprecatedTableHint(TreeNode):
    table_hint: "TableHint" = None


@dataclass
class SybaseLegacyHint(TreeNode):
    holdlock: bool = False
    noholdlock: bool = False
    readpast: bool = False
    shared: bool = False


@dataclass
class TableHint(TreeNode):
    noexpand: bool = False
    index: bool = False
    left: "IndexValue" = None
    right: "IndexValue" = None
    third: "IndexValue" = None
    fourth: list["IndexValue"] = None
    forceseek: bool = False
    column_name_list: "ColumnNameList" = None
    forcescan: bool = False
    holdlock: bool = False
    nolock: bool = False
    nowait: bool = False
    paglock: bool = False
    readcommitted: bool = False
    readcommittedlock: bool = False
    readpast: bool = False
    readuncommitted: bool = False
    repeatableread: bool = False
    rowlock: bool = False
    serializable: bool = False
    snapshot: bool = False
    spatial_window_max_cells: bool = False
    decimal: bool = False
    tablock: bool = False
    tablockx: bool = False
    updlock: bool = False
    xlock: bool = False
    keepidentity: bool = False
    keepdefaults: bool = False
    ignore_constraints: bool = False
    ignore_triggers: bool = False


@dataclass
class IndexValue(TreeNode):
    id: "Id" = None
    decimal: bool = False


@dataclass
class ColumnAliasList(TreeNode):
    alias: "ColumnAlias" = None


@dataclass
class ColumnAlias(TreeNode):
    id: "Id" = None
    string: str = None


@dataclass
class TableValueConstructor(TreeNode):
    exps: "ExpressionList" = None


@dataclass
class ExpressionList(TreeNode):
    exp: "Expression" = None


@dataclass
class RankingWindowedFunction(TreeNode):
    rank: bool = False
    dense_rank: bool = False
    row_number: bool = False
    over_clause: "OverClause" = None
    ntile: bool = False
    expression: "Expression" = None


@dataclass
class AggregateWindowedFunction(TreeNode):
    aggregate_windowed_function_agg_func: "AggregateWindowedFunctionAggFunc" = None
    all_distinct_expression: "AllDistinctExpression" = None
    over_clause: list["OverClause"] = None
    aggregate_windowed_function_cnt: "AggregateWindowedFunctionCnt" = None
    checksum_agg: bool = False
    grouping: bool = False
    expression: "Expression" = None
    grouping_id: bool = False
    expression_list: "ExpressionList" = None


@dataclass
class AnalyticWindowedFunction(TreeNode):
    first_value: bool = False
    last_value: bool = False
    expression: "Expression" = None
    over_clause: "OverClause" = None
    lag: bool = False
    lead: bool = False
    right: "Expression" = None
    third: "Expression" = None
    cume_dist: bool = False
    percent_rank: bool = False
    over: bool = False
    partition: bool = False
    by: bool = False
    expression_list: "ExpressionList" = None
    order_by_clause: "OrderByClause" = None
    percentile_cont: bool = False
    percentile_disc: bool = False
    within: bool = False
    group: bool = False


@dataclass
class AllDistinctExpression(TreeNode):
    all: bool = False
    distinct: bool = False
    expression: "Expression" = None


@dataclass
class OverClause(TreeNode):
    partition: bool = False
    by: bool = False
    expression_list: "ExpressionList" = None
    order_by_clause: list["OrderByClause"] = None
    row_or_range_clause: list["RowOrRangeClause"] = None


@dataclass
class RowOrRangeClause(TreeNode):
    rows: bool = False
    range_: bool = False
    window_frame_extent: "WindowFrameExtent" = None


@dataclass
class WindowFrameExtent(TreeNode):
    window_frame_preceding: "WindowFramePreceding" = None
    between: bool = False
    left: "WindowFrameBound" = None
    and_: bool = False
    right: "WindowFrameBound" = None


@dataclass
class WindowFrameBound(TreeNode):
    window_frame_preceding: "WindowFramePreceding" = None
    window_frame_following: "WindowFrameFollowing" = None


@dataclass
class WindowFramePreceding(TreeNode):
    unbounded: bool = False
    preceding: bool = False
    decimal: bool = False
    current: bool = False
    row: bool = False


@dataclass
class WindowFrameFollowing(TreeNode):
    unbounded: bool = False
    following: bool = False
    decimal: bool = False


@dataclass
class CreateDatabaseOption(TreeNode):
    filestream: bool = False
    left: "DatabaseFilestreamOption" = None
    right: list["DatabaseFilestreamOption"] = None
    default_language: bool = False
    equal: bool = False
    id: "Id" = None
    string: str = None
    default_fulltext_language: bool = False
    nested_triggers: bool = False
    off: bool = False
    on: bool = False
    transform_noise_words: bool = False
    two_digit_year_cutoff: bool = False
    decimal: bool = False
    db_chaining: bool = False
    trustworthy: bool = False


@dataclass
class DatabaseFilestreamOption(TreeNode):
    non_transacted_access: bool = False
    left: bool = False
    directory_name: bool = False
    right: bool = False
    string: str = None
    off: bool = False
    read_only: bool = False
    full: bool = False


@dataclass
class DatabaseFileSpec(TreeNode):
    file_group: "FileGroup" = None
    file_spec: "FileSpec" = None


@dataclass
class FileGroup(TreeNode):
    id: "Id" = None
    left: bool = False
    filestream: bool = False
    default_: bool = False
    right: bool = False
    memory_optimized_data: bool = False
    left: "FileSpec" = None
    right: list["FileSpec"] = None


@dataclass
class FileSpec(TreeNode):
    id: "Id" = None
    string: str = None
    size: bool = False
    left: bool = False
    left: "FileSize" = None
    maxsize: bool = False
    right: bool = False
    filegrowth: bool = False
    third: bool = False
    right: "FileSize" = None
    third: "FileSize" = None
    unlimited: bool = False


@dataclass
class EntityName(TreeNode):
    server: "Id" = None


@dataclass
class EntityNameForAzureDw(TreeNode):
    schema: "Id" = None


@dataclass
class EntityNameForParallelDw(TreeNode):
    schema_database: "Id" = None


@dataclass
class FullTableName(TreeNode):
    linked_server: "Id" = None


@dataclass
class TableName(TreeNode):
    database: "Id" = None
    blocking_hierarchy: bool = False


@dataclass
class SimpleName(TreeNode):
    schema: "Id" = None


@dataclass
class FuncProcNameSchema(TreeNode):
    procedure: "Id" = None


@dataclass
class FuncProcNameDatabaseSchema(TreeNode):
    database: list["Id"] = None
    func_proc_name_schema: "FuncProcNameSchema" = None


@dataclass
class FuncProcNameServerDatabaseSchema(TreeNode):
    server: list["Id"] = None
    func_proc_name_database_schema: "FuncProcNameDatabaseSchema" = None


@dataclass
class DdlObject(TreeNode):
    full_table_name: "FullTableName" = None
    local_id: str = None


@dataclass
class FullColumnName(TreeNode):
    column_name: "Id" = None
    deleted: bool = False
    inserted: bool = False
    full_table_name: "FullTableName" = None
    identity: bool = False
    rowguid: bool = False


@dataclass
class ColumnNameListWithOrder(TreeNode):
    left: "Id" = None
    left: bool = False
    left: bool = False
    right: list["Id"] = None
    right: bool = False
    right: bool = False


@dataclass
class InsertColumnNameList(TreeNode):
    col: "InsertColumnId" = None


@dataclass
class InsertColumnId(TreeNode):
    ignore: list["Id"] = None


@dataclass
class ColumnNameList(TreeNode):
    col: "Id" = None


@dataclass
class CursorName(TreeNode):
    id: "Id" = None
    local_id: str = None


@dataclass
class OnOff(TreeNode):
    on: bool = False
    off: bool = False


@dataclass
class Clustered(TreeNode):
    clustered: bool = False
    nonclustered: bool = False


@dataclass
class ScalarFunctionName(TreeNode):
    func_proc_name_server_database_schema: "FuncProcNameServerDatabaseSchema" = None
    right: bool = False
    left: bool = False
    binary_checksum: bool = False
    checksum: bool = False


@dataclass
class BeginConversationTimer(TreeNode):
    local_id: str = None
    time: "Time" = None


@dataclass
class BeginConversationDialog(TreeNode):
    conversation: bool = False
    dialog_handle: str = None
    initiator_service_name: "ServiceName" = None
    service_broker_guid: str = None
    contract_name: "ContractName" = None
    with_: bool = False
    right: str = None
    lifetime: bool = False
    encryption: bool = False
    on_off: "OnOff" = None
    related_conversation: bool = False
    related_conversation_group: bool = False
    decimal: bool = False
    third: str = None


@dataclass
class ContractName(TreeNode):
    id: "Id" = None
    expression: "Expression" = None


@dataclass
class ServiceName(TreeNode):
    id: "Id" = None
    expression: "Expression" = None


@dataclass
class EndConversation(TreeNode):
    conversation_handle: str = None
    with_: bool = False
    cleanup: bool = False
    error: bool = False
    end_conversation_faliure_code: "EndConversationFaliureCode" = None
    description: bool = False
    end_conversation_failure_text: "EndConversationFailureText" = None


@dataclass
class WaitforConversation(TreeNode):
    get_conversation: "GetConversation" = None
    timeout: bool = False
    timeout: "Time" = None


@dataclass
class GetConversation(TreeNode):
    get_conversation_conversation_group_id: "GetConversationConversationGroupId" = None
    queue: "QueueId" = None


@dataclass
class QueueId(TreeNode):
    database_name: "Id" = None


@dataclass
class SendConversation(TreeNode):
    send_conversation_conversation_handle: "SendConversationConversationHandle" = None
    message_type_name: "Expression" = None
    send_conversation_message_body_expression: "SendConversationMessageBodyExpression" = None


@dataclass
class DataType(TreeNode):
    data_type_scaled: "DataTypeScaled" = None
    max: bool = False
    ext_type: "Id" = None
    scale: bool = False
    identity: bool = False
    double_prec: bool = False


@dataclass
class Constant(TreeNode):
    string: str = None
    binary: str = None
    decimal: bool = False
    real: str = None
    float: bool = False


@dataclass
class PrimitiveConstant(TreeNode):
    string: str = None
    binary: str = None
    decimal: bool = False
    real: str = None
    float: bool = False


@dataclass
class Keyword(TreeNode):
    abort: bool = False
    absolute: bool = False
    accent_sensitivity: bool = False
    access: bool = False
    action: bool = False
    activation: bool = False
    active: bool = False
    add: bool = False
    address: bool = False
    aes_128: bool = False
    aes_192: bool = False
    aes_256: bool = False
    affinity: bool = False
    after: bool = False
    aggregate: bool = False
    algorithm: bool = False
    all_constraints: bool = False
    all_errormsgs: bool = False
    all_indexes: bool = False
    all_levels: bool = False
    allow_encrypted_value_modifications: bool = False
    allow_page_locks: bool = False
    allow_row_locks: bool = False
    allow_snapshot_isolation: bool = False
    allowed: bool = False
    always: bool = False
    ansi_defaults: bool = False
    ansi_null_default: bool = False
    ansi_null_dflt_off: bool = False
    ansi_null_dflt_on: bool = False
    ansi_nulls: bool = False
    ansi_padding: bool = False
    ansi_warnings: bool = False
    app_name: bool = False
    application_log: bool = False
    applock_mode: bool = False
    applock_test: bool = False
    apply: bool = False
    arithabort: bool = False
    arithignore: bool = False
    ascii: bool = False
    assembly: bool = False
    assemblyproperty: bool = False
    at_keyword: bool = False
    audit: bool = False
    audit_guid: bool = False
    auto: bool = False
    auto_cleanup: bool = False
    auto_close: bool = False
    auto_create_statistics: bool = False
    auto_drop: bool = False
    auto_shrink: bool = False
    auto_update_statistics: bool = False
    auto_update_statistics_async: bool = False
    autogrow_all_files: bool = False
    autogrow_single_file: bool = False
    availability: bool = False
    avg: bool = False
    backup_clonedb: bool = False
    backup_priority: bool = False
    base64: bool = False
    begin_dialog: bool = False
    bigint: bool = False
    binary_keyword: bool = False
    binary_checksum: bool = False
    binding: bool = False
    blob_storage: bool = False
    broker: bool = False
    broker_instance: bool = False
    bulk_logged: bool = False
    caller: bool = False
    cap_cpu_percent: bool = False
    cast: bool = False
    try_cast: bool = False
    catalog: bool = False
    catch: bool = False
    cert_id: bool = False
    certencoded: bool = False
    certprivatekey: bool = False
    change: bool = False
    change_retention: bool = False
    change_tracking: bool = False
    char: bool = False
    charindex: bool = False
    checkalloc: bool = False
    checkcatalog: bool = False
    checkconstraints: bool = False
    checkdb: bool = False
    checkfilegroup: bool = False
    checksum: bool = False
    checksum_agg: bool = False
    checktable: bool = False
    cleantable: bool = False
    cleanup: bool = False
    clonedatabase: bool = False
    col_length: bool = False
    col_name: bool = False
    collection: bool = False
    column_encryption_key: bool = False
    column_master_key: bool = False
    columnproperty: bool = False
    columns: bool = False
    columnstore: bool = False
    columnstore_archive: bool = False
    committed: bool = False
    compatibility_level: bool = False
    compress_all_row_groups: bool = False
    compression_delay: bool = False
    concat: bool = False
    concat_ws: bool = False
    concat_null_yields_null: bool = False
    content: bool = False
    control: bool = False
    cookie: bool = False
    count: bool = False
    count_big: bool = False
    counter: bool = False
    cpu: bool = False
    create_new: bool = False
    creation_disposition: bool = False
    credential: bool = False
    cryptographic: bool = False
    cume_dist: bool = False
    cursor_close_on_commit: bool = False
    cursor_default: bool = False
    cursor_status: bool = False
    data: bool = False
    data_purity: bool = False
    database_principal_id: bool = False
    databasepropertyex: bool = False
    datalength: bool = False
    date_correlation_optimization: bool = False
    dateadd: bool = False
    datediff: bool = False
    datename: bool = False
    datepart: bool = False
    days: bool = False
    db_chaining: bool = False
    db_failover: bool = False
    db_id: bool = False
    db_name: bool = False
    dbcc: bool = False
    dbreindex: bool = False
    decryption: bool = False
    default_double_quote: str = None
    default_fulltext_language: bool = False
    default_language: bool = False
    definition: bool = False
    delay: bool = False
    delayed_durability: bool = False
    deleted: bool = False
    dense_rank: bool = False
    dependents: bool = False
    des: bool = False
    description: bool = False
    desx: bool = False
    deterministic: bool = False
    dhcp: bool = False
    dialog: bool = False
    difference: bool = False
    directory_name: bool = False
    disable: bool = False
    disable_broker: bool = False
    disabled: bool = False
    document: bool = False
    drop_existing: bool = False
    dropcleanbuffers: bool = False
    dynamic: bool = False
    elements: bool = False
    emergency: bool = False
    empty: bool = False
    enable: bool = False
    enable_broker: bool = False
    encrypted: bool = False
    encrypted_value: bool = False
    encryption: bool = False
    encryption_type: bool = False
    endpoint_url: bool = False
    error_broker_conversations: bool = False
    estimateonly: bool = False
    exclusive: bool = False
    executable: bool = False
    exist: bool = False
    exist_square_bracket: bool = False
    expand: bool = False
    expiry_date: bool = False
    explicit: bool = False
    extended_logical_checks: bool = False
    fail_operation: bool = False
    failover_mode: bool = False
    failure: bool = False
    failure_condition_level: bool = False
    fast: bool = False
    fast_forward: bool = False
    file_id: bool = False
    file_idex: bool = False
    file_name: bool = False
    filegroup: bool = False
    filegroup_id: bool = False
    filegroup_name: bool = False
    filegroupproperty: bool = False
    filegrowth: bool = False
    filename: bool = False
    filepath: bool = False
    fileproperty: bool = False
    filepropertyex: bool = False
    filestream: bool = False
    filter: bool = False
    first: bool = False
    first_value: bool = False
    fmtonly: bool = False
    following: bool = False
    force: bool = False
    force_failover_allow_data_loss: bool = False
    forced: bool = False
    forceplan: bool = False
    forcescan: bool = False
    format: bool = False
    forward_only: bool = False
    free: bool = False
    fullscan: bool = False
    fulltext: bool = False
    fulltextcatalogproperty: bool = False
    fulltextserviceproperty: bool = False
    gb: bool = False
    generated: bool = False
    getdate: bool = False
    getutcdate: bool = False
    global_: bool = False
    go_: bool = False
    greatest: bool = False
    group_max_requests: bool = False
    grouping: bool = False
    grouping_id: bool = False
    hadr: bool = False
    has_dbaccess: bool = False
    has_perms_by_name: bool = False
    hash: bool = False
    health_check_timeout: bool = False
    hidden_keyword: bool = False
    high: bool = False
    honor_broker_priority: bool = False
    hours: bool = False
    ident_current: bool = False
    ident_incr: bool = False
    ident_seed: bool = False
    identity_value: bool = False
    ignore_constraints: bool = False
    ignore_dup_key: bool = False
    ignore_nonclustered_columnstore_index: bool = False
    ignore_replicated_table_cache: bool = False
    ignore_triggers: bool = False
    immediate: bool = False
    impersonate: bool = False
    implicit_transactions: bool = False
    importance: bool = False
    include_null_values: bool = False
    incremental: bool = False
    index_col: bool = False
    indexkey_property: bool = False
    indexproperty: bool = False
    initiator: bool = False
    input: bool = False
    insensitive: bool = False
    inserted: bool = False
    int: bool = False
    ip: bool = False
    is_member: bool = False
    is_rolemember: bool = False
    is_srvrolemember: bool = False
    isjson: bool = False
    isolation: bool = False
    job: bool = False
    json: bool = False
    json_object: bool = False
    json_array: bool = False
    json_value: bool = False
    json_query: bool = False
    json_modify: bool = False
    json_path_exists: bool = False
    kb: bool = False
    keep: bool = False
    keepdefaults: bool = False
    keepfixed: bool = False
    keepidentity: bool = False
    key_source: bool = False
    keys: bool = False
    keyset: bool = False
    lag: bool = False
    last: bool = False
    last_value: bool = False
    lead: bool = False
    least: bool = False
    len_: bool = False
    level: bool = False
    list: bool = False
    listener: bool = False
    listener_url: bool = False
    lob_compaction: bool = False
    local: bool = False
    location: bool = False
    lock: bool = False
    lock_escalation: bool = False
    login: bool = False
    loginproperty: bool = False
    loop: bool = False
    low: bool = False
    lower: bool = False
    ltrim: bool = False
    manual: bool = False
    mark: bool = False
    masked: bool = False
    materialized: bool = False
    max: bool = False
    max_cpu_percent: bool = False
    max_dop: bool = False
    max_files: bool = False
    max_iops_per_volume: bool = False
    max_memory_percent: bool = False
    max_processes: bool = False
    max_queue_readers: bool = False
    max_rollover_files: bool = False
    maxdop: bool = False
    maxrecursion: bool = False
    maxsize: bool = False
    mb: bool = False
    medium: bool = False
    memory_optimized_data: bool = False
    message: bool = False
    min: bool = False
    min_active_rowversion: bool = False
    min_cpu_percent: bool = False
    min_iops_per_volume: bool = False
    min_memory_percent: bool = False
    minutes: bool = False
    mirror_address: bool = False
    mixed_page_allocation: bool = False
    mode: bool = False
    modify: bool = False
    modify_square_bracket: bool = False
    move: bool = False
    multi_user: bool = False
    name: bool = False
    nchar: bool = False
    nested_triggers: bool = False
    new_account: bool = False
    new_broker: bool = False
    new_password: bool = False
    newname: bool = False
    next: bool = False
    no: bool = False
    no_infomsgs: bool = False
    no_querystore: bool = False
    no_statistics: bool = False
    no_truncate: bool = False
    no_wait: bool = False
    nocount: bool = False
    nodes: bool = False
    noexec: bool = False
    noexpand: bool = False
    noindex: bool = False
    nolock: bool = False
    non_transacted_access: bool = False
    norecompute: bool = False
    norecovery: bool = False
    notifications: bool = False
    nowait: bool = False
    ntile: bool = False
    null_double_quote: str = None
    numanode: bool = False
    number: bool = False
    numeric_roundabort: bool = False
    object: bool = False
    object_definition: bool = False
    object_id: bool = False
    object_name: bool = False
    object_schema_name: bool = False
    objectproperty: bool = False
    objectpropertyex: bool = False
    offline: bool = False
    offset: bool = False
    old_account: bool = False
    online: bool = False
    only: bool = False
    open_existing: bool = False
    openjson: bool = False
    optimistic: bool = False
    optimize: bool = False
    optimize_for_sequential_key: bool = False
    original_db_name: bool = False
    original_login: bool = False
    out: bool = False
    output: bool = False
    override: bool = False
    owner: bool = False
    ownership: bool = False
    pad_index: bool = False
    page_verify: bool = False
    pagecount: bool = False
    paglock: bool = False
    parameterization: bool = False
    parsename: bool = False
    parseonly: bool = False
    partition: bool = False
    partitions: bool = False
    partner: bool = False
    path: bool = False
    patindex: bool = False
    pause: bool = False
    pdw_showspaceused: bool = False
    percent_rank: bool = False
    percentile_cont: bool = False
    percentile_disc: bool = False
    permissions: bool = False
    persist_sample_percent: bool = False
    physical_only: bool = False
    poison_message_handling: bool = False
    pool: bool = False
    port: bool = False
    preceding: bool = False
    primary_role: bool = False
    prior: bool = False
    priority: bool = False
    priority_level: bool = False
    private: bool = False
    private_key: bool = False
    privileges: bool = False
    proccache: bool = False
    procedure_name: bool = False
    property: bool = False
    provider: bool = False
    provider_key_name: bool = False
    pwdcompare: bool = False
    pwdencrypt: bool = False
    query: bool = False
    query_square_bracket: bool = False
    queue: bool = False
    queue_delay: bool = False
    quoted_identifier: bool = False
    quotename: bool = False
    randomized: bool = False
    range_: bool = False
    rank: bool = False
    rc2: bool = False
    rc4: bool = False
    rc4_128: bool = False
    read_committed_snapshot: bool = False
    read_only: bool = False
    read_only_routing_list: bool = False
    read_write: bool = False
    readcommitted: bool = False
    readcommittedlock: bool = False
    readonly: bool = False
    readpast: bool = False
    readuncommitted: bool = False
    readwrite: bool = False
    rebuild: bool = False
    receive: bool = False
    recompile: bool = False
    recovery: bool = False
    recursive_triggers: bool = False
    relative: bool = False
    remote: bool = False
    remote_proc_transactions: bool = False
    remote_service_name: bool = False
    remove: bool = False
    reorganize: bool = False
    repair_allow_data_loss: bool = False
    repair_fast: bool = False
    repair_rebuild: bool = False
    repeatable: bool = False
    repeatableread: bool = False
    replace: bool = False
    replica: bool = False
    replicate: bool = False
    request_max_cpu_time_sec: bool = False
    request_max_memory_grant_percent: bool = False
    request_memory_grant_timeout_sec: bool = False
    required_synchronized_secondaries_to_commit: bool = False
    resample: bool = False
    reserve_disk_space: bool = False
    resource: bool = False
    resource_manager_location: bool = False
    restricted_user: bool = False
    resumable: bool = False
    retention: bool = False
    reverse: bool = False
    robust: bool = False
    root: bool = False
    route: bool = False
    row: bool = False
    row_number: bool = False
    rowguid: bool = False
    rowlock: bool = False
    rows: bool = False
    rtrim: bool = False
    sample: bool = False
    schema_id: bool = False
    schema_name: bool = False
    schemabinding: bool = False
    scope_identity: bool = False
    scoped: bool = False
    scroll: bool = False
    scroll_locks: bool = False
    search: bool = False
    secondary: bool = False
    secondary_only: bool = False
    secondary_role: bool = False
    seconds: bool = False
    secret: bool = False
    securables: bool = False
    security: bool = False
    security_log: bool = False
    seeding_mode: bool = False
    self: bool = False
    semi_sensitive: bool = False
    send: bool = False
    sent: bool = False
    sequence: bool = False
    sequence_number: bool = False
    serializable: bool = False
    serverproperty: bool = False
    servicebroker: bool = False
    sessionproperty: bool = False
    session_timeout: bool = False
    seterror: bool = False
    share: bool = False
    shared: bool = False
    showcontig: bool = False
    showplan: bool = False
    showplan_all: bool = False
    showplan_text: bool = False
    showplan_xml: bool = False
    signature: bool = False
    simple: bool = False
    single_user: bool = False
    size: bool = False
    smallint: bool = False
    snapshot: bool = False
    sort_in_tempdb: bool = False
    soundex: bool = False
    space_keyword: bool = False
    sparse: bool = False
    spatial_window_max_cells: bool = False
    sql_variant_property: bool = False
    standby: bool = False
    start_date: bool = False
    static: bool = False
    statistics_incremental: bool = False
    statistics_norecompute: bool = False
    stats_date: bool = False
    stats_stream: bool = False
    status: bool = False
    statusonly: bool = False
    stdev: bool = False
    stdevp: bool = False
    stoplist: bool = False
    str: bool = False
    string_agg: bool = False
    string_escape: bool = False
    stuff: bool = False
    subject: bool = False
    subscribe: bool = False
    subscription: bool = False
    substring: bool = False
    sum: bool = False
    suser_id: bool = False
    suser_name: bool = False
    suser_sid: bool = False
    suser_sname: bool = False
    suspend: bool = False
    symmetric: bool = False
    synchronous_commit: bool = False
    synonym: bool = False
    system: bool = False
    tableresults: bool = False
    tablock: bool = False
    tablockx: bool = False
    take: bool = False
    target_recovery_time: bool = False
    tb: bool = False
    textimage_on: bool = False
    throw: bool = False
    ties: bool = False
    time: bool = False
    timeout: bool = False
    timer: bool = False
    tinyint: bool = False
    torn_page_detection: bool = False
    tracking: bool = False
    transaction_id: bool = False
    transform_noise_words: bool = False
    translate: bool = False
    trim: bool = False
    triple_des: bool = False
    triple_des_3key: bool = False
    trustworthy: bool = False
    try_: bool = False
    tsql: bool = False
    two_digit_year_cutoff: bool = False
    type_: bool = False
    type_id: bool = False
    type_name: bool = False
    type_warning: bool = False
    typeproperty: bool = False
    unbounded: bool = False
    uncommitted: bool = False
    unicode: bool = False
    unknown: bool = False
    unlimited: bool = False
    unmask: bool = False
    uow: bool = False
    updlock: bool = False
    upper: bool = False
    user_id: bool = False
    user_name: bool = False
    using: bool = False
    valid_xml: bool = False
    validation: bool = False
    value: bool = False
    value_square_bracket: bool = False
    var_: bool = False
    varbinary_keyword: bool = False
    varp: bool = False
    verify_clonedb: bool = False
    version: bool = False
    view_metadata: bool = False
    views: bool = False
    wait: bool = False
    well_formed_xml: bool = False
    without_array_wrapper: bool = False
    work: bool = False
    workload: bool = False
    xlock: bool = False
    xml: bool = False
    xml_compression: bool = False
    xmldata: bool = False
    xmlnamespaces: bool = False
    xmlschema: bool = False
    xsinil: bool = False
    zone: bool = False
    abort_after_wait: bool = False
    absent: bool = False
    administer: bool = False
    aes: bool = False
    allow_connections: bool = False
    allow_multiple_event_loss: bool = False
    allow_single_event_loss: bool = False
    anonymous: bool = False
    append_: bool = False
    application: bool = False
    asymmetric: bool = False
    asynchronous_commit: bool = False
    authenticate: bool = False
    authentication: bool = False
    automated_backup_preference: bool = False
    automatic: bool = False
    availability_mode: bool = False
    before: bool = False
    block: bool = False
    blockers: bool = False
    blocksize: bool = False
    blocking_hierarchy: bool = False
    buffer: bool = False
    buffercount: bool = False
    cache: bool = False
    called: bool = False
    certificate: bool = False
    changetable: bool = False
    changes: bool = False
    check_policy: bool = False
    check_expiration: bool = False
    classifier_function: bool = False
    cluster: bool = False
    compress: bool = False
    compression: bool = False
    connect: bool = False
    connection: bool = False
    configuration: bool = False
    connectionproperty: bool = False
    containment: bool = False
    context: bool = False
    context_info: bool = False
    continue_after_error: bool = False
    contract: bool = False
    contract_name: bool = False
    conversation: bool = False
    copy_only: bool = False
    current_request_id: bool = False
    current_transaction_id: bool = False
    cycle: bool = False
    data_compression: bool = False
    data_source: bool = False
    database_mirroring: bool = False
    dataspace: bool = False
    ddl: bool = False
    decompress: bool = False
    default_database: bool = False
    default_schema: bool = False
    diagnostics: bool = False
    differential: bool = False
    distribution: bool = False
    dtc_support: bool = False
    enabled: bool = False
    endpoint: bool = False
    error: bool = False
    error_line: bool = False
    error_message: bool = False
    error_number: bool = False
    error_procedure: bool = False
    error_severity: bool = False
    error_state: bool = False
    event: bool = False
    eventdata: bool = False
    event_retention_mode: bool = False
    executable_file: bool = False
    expiredate: bool = False
    extension: bool = False
    external_access: bool = False
    failover: bool = False
    failureconditionlevel: bool = False
    fan_in: bool = False
    file_snapshot: bool = False
    forceseek: bool = False
    force_service_allow_data_loss: bool = False
    formatmessage: bool = False
    get: bool = False
    get_filestream_transaction_context: bool = False
    getancestor: bool = False
    getansinull: bool = False
    getdescendant: bool = False
    getlevel: bool = False
    getreparentedvalue: bool = False
    getroot: bool = False
    governor: bool = False
    hashed: bool = False
    healthchecktimeout: bool = False
    heap: bool = False
    hierarchyid: bool = False
    host_id: bool = False
    host_name: bool = False
    iif: bool = False
    io: bool = False
    include: bool = False
    increment: bool = False
    infinite: bool = False
    init: bool = False
    instead: bool = False
    isdescendantof: bool = False
    isnull: bool = False
    isnumeric: bool = False
    kerberos: bool = False
    key_path: bool = False
    key_store_provider_name: bool = False
    language: bool = False
    library: bool = False
    lifetime: bool = False
    linked: bool = False
    linux: bool = False
    listener_ip: bool = False
    listener_port: bool = False
    local_service_name: bool = False
    log: bool = False
    mask: bool = False
    matched: bool = False
    master: bool = False
    max_memory: bool = False
    maxtransfer: bool = False
    maxvalue: bool = False
    max_dispatch_latency: bool = False
    max_duration: bool = False
    max_event_size: bool = False
    max_size: bool = False
    max_outstanding_io_per_volume: bool = False
    mediadescription: bool = False
    medianame: bool = False
    member: bool = False
    memory_partition_mode: bool = False
    message_forwarding: bool = False
    message_forward_size: bool = False
    minvalue: bool = False
    mirror: bool = False
    must_change: bool = False
    newid: bool = False
    newsequentialid: bool = False
    noformat: bool = False
    noinit: bool = False
    none: bool = False
    norewind: bool = False
    noskip: bool = False
    nounload: bool = False
    no_checksum: bool = False
    no_compression: bool = False
    no_event_loss: bool = False
    notification: bool = False
    ntlm: bool = False
    old_password: bool = False
    on_failure: bool = False
    operations: bool = False
    page: bool = False
    param_node: bool = False
    partial: bool = False
    password: bool = False
    permission_set: bool = False
    per_cpu: bool = False
    per_db: bool = False
    per_node: bool = False
    persisted: bool = False
    platform: bool = False
    policy: bool = False
    predicate: bool = False
    process: bool = False
    profile: bool = False
    python: bool = False
    r: bool = False
    read_write_filegroups: bool = False
    regenerate: bool = False
    related_conversation: bool = False
    related_conversation_group: bool = False
    required: bool = False
    reset: bool = False
    resources: bool = False
    restart: bool = False
    resume: bool = False
    retaindays: bool = False
    returns: bool = False
    rewind: bool = False
    role: bool = False
    round_robin: bool = False
    rowcount_big: bool = False
    rsa_512: bool = False
    rsa_1024: bool = False
    rsa_2048: bool = False
    rsa_3072: bool = False
    rsa_4096: bool = False
    safety: bool = False
    safe: bool = False
    scheduler: bool = False
    scheme: bool = False
    script: bool = False
    server: bool = False
    service: bool = False
    service_broker: bool = False
    service_name: bool = False
    session: bool = False
    session_context: bool = False
    settings: bool = False
    shrinklog: bool = False
    sid: bool = False
    skip_keyword: bool = False
    softnuma: bool = False
    source: bool = False
    specification: bool = False
    split: bool = False
    sql: bool = False
    sqldumperflags: bool = False
    sqldumperpath: bool = False
    sqldumpertimeout: bool = False
    state: bool = False
    stats: bool = False
    start: bool = False
    started: bool = False
    startup_state: bool = False
    stop: bool = False
    stopped: bool = False
    stop_on_error: bool = False
    supported: bool = False
    switch_: bool = False
    tape: bool = False
    target: bool = False
    tcp: bool = False
    tostring: bool = False
    trace: bool = False
    track_causality: bool = False
    transfer: bool = False
    unchecked: bool = False
    unlock: bool = False
    unsafe: bool = False
    url: bool = False
    used: bool = False
    verboselogging: bool = False
    visibility: bool = False
    wait_at_low_priority: bool = False
    windows: bool = False
    without: bool = False
    witness: bool = False
    xact_abort: bool = False
    xact_state: bool = False
    abs: bool = False
    acos: bool = False
    asin: bool = False
    atan: bool = False
    atn2: bool = False
    ceiling: bool = False
    cos: bool = False
    cot: bool = False
    degrees: bool = False
    exp: bool = False
    floor: bool = False
    log10: bool = False
    pi: bool = False
    power: bool = False
    radians: bool = False
    rand: bool = False
    round: bool = False
    sign: bool = False
    sin: bool = False
    sqrt: bool = False
    square: bool = False
    tan: bool = False
    current_timezone: bool = False
    current_timezone_id: bool = False
    date_bucket: bool = False
    datediff_big: bool = False
    datefromparts: bool = False
    datetime2fromparts: bool = False
    datetimefromparts: bool = False
    datetimeoffsetfromparts: bool = False
    datetrunc: bool = False
    day: bool = False
    eomonth: bool = False
    isdate: bool = False
    month: bool = False
    smalldatetimefromparts: bool = False
    switchoffset: bool = False
    sysdatetime: bool = False
    sysdatetimeoffset: bool = False
    sysutcdatetime: bool = False
    timefromparts: bool = False
    todatetimeoffset: bool = False
    year: bool = False
    quarter: bool = False
    dayofyear: bool = False
    week: bool = False
    hour: bool = False
    minute: bool = False
    second: bool = False
    millisecond: bool = False
    microsecond: bool = False
    nanosecond: bool = False
    tzoffset: bool = False
    iso_week: bool = False
    weekday: bool = False
    year_abbr: str = None
    quarter_abbr: str = None
    month_abbr: str = None
    dayofyear_abbr: str = None
    day_abbr: str = None
    week_abbr: str = None
    hour_abbr: bool = False
    minute_abbr: str = None
    second_abbr: str = None
    millisecond_abbr: bool = False
    microsecond_abbr: bool = False
    nanosecond_abbr: bool = False
    tzoffset_abbr: bool = False
    iso_week_abbr: str = None
    weekday_abbr: bool = False
    sp_executesql: bool = False
    varchar: bool = False
    nvarchar: bool = False
    precision: bool = False
    filestream_on: bool = False


@dataclass
class Id(TreeNode):
    id: str = None
    temp_id: str = None
    double_quote_id: str = None
    double_quote_blank: bool = False
    square_bracket_id: str = None
    keyword: "Keyword" = None
    raw: bool = False


@dataclass
class SimpleId(TreeNode):
    id: str = None


@dataclass
class IdOrString(TreeNode):
    id: "Id" = None
    string: str = None


@dataclass
class FileSize(TreeNode):
    kb: bool = False
    mb: bool = False
    gb: bool = False
    tb: bool = False


@dataclass
class RaiseerrorStatementMsg(TreeNode):
    decimal: bool = False
    string: str = None
    local_id: str = None


@dataclass
class RaiseerrorStatementFormatstring(TreeNode):
    string: str = None
    local_id: str = None
    double_quote_id: str = None


@dataclass
class RaiseerrorStatementArgument(TreeNode):
    decimal: bool = False
    string: str = None
    local_id: str = None


@dataclass
class CreateEndpointState(TreeNode):
    started: bool = False
    stopped: bool = False
    disabled: bool = False


@dataclass
class AlterServerAuditMaxRolloverFiles(TreeNode):
    decimal: bool = False
    unlimited: bool = False


@dataclass
class CreateServerAuditMaxRolloverFiles(TreeNode):
    decimal: bool = False
    unlimited: bool = False


@dataclass
class CreateOrAlterProcedureProc(TreeNode):
    proc: bool = False
    procedure: bool = False


@dataclass
class LowPriorityLockWaitAbortAfterWait(TreeNode):
    none: bool = False
    self: bool = False
    blockers: bool = False


@dataclass
class AlterEndpointState(TreeNode):
    started: bool = False
    stopped: bool = False
    disabled: bool = False


@dataclass
class SnapshotOptionMemoryOptimizedElevateToSnapshot(TreeNode):
    on: bool = False
    off: bool = False


@dataclass
class DropProcedureProc(TreeNode):
    proc: bool = False
    procedure: bool = False


@dataclass
class KillProcessSessionId(TreeNode):
    decimal: bool = False
    string: str = None


@dataclass
class ExecuteClauseClause(TreeNode):
    caller: bool = False
    self: bool = False
    owner: bool = False
    string: str = None


@dataclass
class TopPercentPercentConstant(TreeNode):
    real: str = None
    float: bool = False
    decimal: bool = False


@dataclass
class SelectOrderByClauseOffsetRows(TreeNode):
    row: bool = False
    rows: bool = False


@dataclass
class SelectOrderByClauseFetchOffset(TreeNode):
    first: bool = False
    next: bool = False


@dataclass
class SelectOrderByClauseFetchRows(TreeNode):
    row: bool = False
    rows: bool = False


@dataclass
class ChangeTableChangesChangesid(TreeNode):
    null: bool = False
    decimal: bool = False
    local_id: str = None


@dataclass
class JoinOnJoinType(TreeNode):
    left: bool = False
    right: bool = False
    full: bool = False


@dataclass
class JoinOnJoinHint(TreeNode):
    loop: bool = False
    hash: bool = False
    merge: bool = False
    remote: bool = False


@dataclass
class ApplyApplyStyle(TreeNode):
    cross: bool = False
    outer: bool = False


@dataclass
class BulkOptionBulkOptionValue(TreeNode):
    decimal: bool = False
    string: str = None


@dataclass
class AggregateWindowedFunctionAggFunc(TreeNode):
    avg: bool = False
    max: bool = False
    min: bool = False
    sum: bool = False
    stdev: bool = False
    stdevp: bool = False
    var_: bool = False
    varp: bool = False


@dataclass
class AggregateWindowedFunctionCnt(TreeNode):
    count: bool = False
    count_big: bool = False


@dataclass
class EndConversationFaliureCode(TreeNode):
    local_id: str = None
    string: str = None


@dataclass
class EndConversationFailureText(TreeNode):
    local_id: str = None
    string: str = None


@dataclass
class GetConversationConversationGroupId(TreeNode):
    string: str = None
    local_id: str = None


@dataclass
class SendConversationConversationHandle(TreeNode):
    string: str = None
    local_id: str = None


@dataclass
class SendConversationMessageBodyExpression(TreeNode):
    string: str = None
    local_id: str = None


@dataclass
class DataTypeScaled(TreeNode):
    varchar: bool = False
    nvarchar: bool = False
    binary_keyword: bool = False
    varbinary_keyword: bool = False
    square_bracket_id: str = None


