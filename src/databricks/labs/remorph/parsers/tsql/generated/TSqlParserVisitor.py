# Generated from src/databricks/labs/remorph/parsers/tsql/TSqlParser.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .TSqlParser import TSqlParser
else:
    from TSqlParser import TSqlParser

# This class defines a complete generic visitor for a parse tree produced by TSqlParser.

class TSqlParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by TSqlParser#tsql_file.
    def visitTsql_file(self, ctx:TSqlParser.Tsql_fileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#batch.
    def visitBatch(self, ctx:TSqlParser.BatchContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#batch_level_statement.
    def visitBatch_level_statement(self, ctx:TSqlParser.Batch_level_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#sql_clauses.
    def visitSql_clauses(self, ctx:TSqlParser.Sql_clausesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dml_clause.
    def visitDml_clause(self, ctx:TSqlParser.Dml_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#ddl_clause.
    def visitDdl_clause(self, ctx:TSqlParser.Ddl_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#backup_statement.
    def visitBackup_statement(self, ctx:TSqlParser.Backup_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#cfl_statement.
    def visitCfl_statement(self, ctx:TSqlParser.Cfl_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#block_statement.
    def visitBlock_statement(self, ctx:TSqlParser.Block_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#break_statement.
    def visitBreak_statement(self, ctx:TSqlParser.Break_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#continue_statement.
    def visitContinue_statement(self, ctx:TSqlParser.Continue_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#goto_statement.
    def visitGoto_statement(self, ctx:TSqlParser.Goto_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#return_statement.
    def visitReturn_statement(self, ctx:TSqlParser.Return_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#if_statement.
    def visitIf_statement(self, ctx:TSqlParser.If_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#throw_statement.
    def visitThrow_statement(self, ctx:TSqlParser.Throw_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#throw_error_number.
    def visitThrow_error_number(self, ctx:TSqlParser.Throw_error_numberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#throw_message.
    def visitThrow_message(self, ctx:TSqlParser.Throw_messageContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#throw_state.
    def visitThrow_state(self, ctx:TSqlParser.Throw_stateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#try_catch_statement.
    def visitTry_catch_statement(self, ctx:TSqlParser.Try_catch_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#waitfor_statement.
    def visitWaitfor_statement(self, ctx:TSqlParser.Waitfor_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#while_statement.
    def visitWhile_statement(self, ctx:TSqlParser.While_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#print_statement.
    def visitPrint_statement(self, ctx:TSqlParser.Print_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#raiseerror_statement.
    def visitRaiseerror_statement(self, ctx:TSqlParser.Raiseerror_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#empty_statement.
    def visitEmpty_statement(self, ctx:TSqlParser.Empty_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#another_statement.
    def visitAnother_statement(self, ctx:TSqlParser.Another_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_application_role.
    def visitAlter_application_role(self, ctx:TSqlParser.Alter_application_roleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_xml_schema_collection.
    def visitAlter_xml_schema_collection(self, ctx:TSqlParser.Alter_xml_schema_collectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_application_role.
    def visitCreate_application_role(self, ctx:TSqlParser.Create_application_roleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_aggregate.
    def visitDrop_aggregate(self, ctx:TSqlParser.Drop_aggregateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_application_role.
    def visitDrop_application_role(self, ctx:TSqlParser.Drop_application_roleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_assembly.
    def visitAlter_assembly(self, ctx:TSqlParser.Alter_assemblyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_assembly_start.
    def visitAlter_assembly_start(self, ctx:TSqlParser.Alter_assembly_startContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_assembly_clause.
    def visitAlter_assembly_clause(self, ctx:TSqlParser.Alter_assembly_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_assembly_from_clause.
    def visitAlter_assembly_from_clause(self, ctx:TSqlParser.Alter_assembly_from_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_assembly_from_clause_start.
    def visitAlter_assembly_from_clause_start(self, ctx:TSqlParser.Alter_assembly_from_clause_startContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_assembly_drop_clause.
    def visitAlter_assembly_drop_clause(self, ctx:TSqlParser.Alter_assembly_drop_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_assembly_drop_multiple_files.
    def visitAlter_assembly_drop_multiple_files(self, ctx:TSqlParser.Alter_assembly_drop_multiple_filesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_assembly_drop.
    def visitAlter_assembly_drop(self, ctx:TSqlParser.Alter_assembly_dropContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_assembly_add_clause.
    def visitAlter_assembly_add_clause(self, ctx:TSqlParser.Alter_assembly_add_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_asssembly_add_clause_start.
    def visitAlter_asssembly_add_clause_start(self, ctx:TSqlParser.Alter_asssembly_add_clause_startContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_assembly_client_file_clause.
    def visitAlter_assembly_client_file_clause(self, ctx:TSqlParser.Alter_assembly_client_file_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_assembly_file_name.
    def visitAlter_assembly_file_name(self, ctx:TSqlParser.Alter_assembly_file_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_assembly_file_bits.
    def visitAlter_assembly_file_bits(self, ctx:TSqlParser.Alter_assembly_file_bitsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_assembly_as.
    def visitAlter_assembly_as(self, ctx:TSqlParser.Alter_assembly_asContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_assembly_with_clause.
    def visitAlter_assembly_with_clause(self, ctx:TSqlParser.Alter_assembly_with_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_assembly_with.
    def visitAlter_assembly_with(self, ctx:TSqlParser.Alter_assembly_withContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#client_assembly_specifier.
    def visitClient_assembly_specifier(self, ctx:TSqlParser.Client_assembly_specifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#assembly_option.
    def visitAssembly_option(self, ctx:TSqlParser.Assembly_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#network_file_share.
    def visitNetwork_file_share(self, ctx:TSqlParser.Network_file_shareContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#network_computer.
    def visitNetwork_computer(self, ctx:TSqlParser.Network_computerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#network_file_start.
    def visitNetwork_file_start(self, ctx:TSqlParser.Network_file_startContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#file_path.
    def visitFile_path(self, ctx:TSqlParser.File_pathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#file_directory_path_separator.
    def visitFile_directory_path_separator(self, ctx:TSqlParser.File_directory_path_separatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#local_file.
    def visitLocal_file(self, ctx:TSqlParser.Local_fileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#local_drive.
    def visitLocal_drive(self, ctx:TSqlParser.Local_driveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#multiple_local_files.
    def visitMultiple_local_files(self, ctx:TSqlParser.Multiple_local_filesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#multiple_local_file_start.
    def visitMultiple_local_file_start(self, ctx:TSqlParser.Multiple_local_file_startContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_assembly.
    def visitCreate_assembly(self, ctx:TSqlParser.Create_assemblyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_assembly.
    def visitDrop_assembly(self, ctx:TSqlParser.Drop_assemblyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_asymmetric_key.
    def visitAlter_asymmetric_key(self, ctx:TSqlParser.Alter_asymmetric_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_asymmetric_key_start.
    def visitAlter_asymmetric_key_start(self, ctx:TSqlParser.Alter_asymmetric_key_startContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#asymmetric_key_option.
    def visitAsymmetric_key_option(self, ctx:TSqlParser.Asymmetric_key_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#asymmetric_key_option_start.
    def visitAsymmetric_key_option_start(self, ctx:TSqlParser.Asymmetric_key_option_startContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#asymmetric_key_password_change_option.
    def visitAsymmetric_key_password_change_option(self, ctx:TSqlParser.Asymmetric_key_password_change_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_asymmetric_key.
    def visitCreate_asymmetric_key(self, ctx:TSqlParser.Create_asymmetric_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_asymmetric_key.
    def visitDrop_asymmetric_key(self, ctx:TSqlParser.Drop_asymmetric_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_authorization.
    def visitAlter_authorization(self, ctx:TSqlParser.Alter_authorizationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#authorization_grantee.
    def visitAuthorization_grantee(self, ctx:TSqlParser.Authorization_granteeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#entity_to.
    def visitEntity_to(self, ctx:TSqlParser.Entity_toContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#colon_colon.
    def visitColon_colon(self, ctx:TSqlParser.Colon_colonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_authorization_start.
    def visitAlter_authorization_start(self, ctx:TSqlParser.Alter_authorization_startContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_authorization_for_sql_database.
    def visitAlter_authorization_for_sql_database(self, ctx:TSqlParser.Alter_authorization_for_sql_databaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_authorization_for_azure_dw.
    def visitAlter_authorization_for_azure_dw(self, ctx:TSqlParser.Alter_authorization_for_azure_dwContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_authorization_for_parallel_dw.
    def visitAlter_authorization_for_parallel_dw(self, ctx:TSqlParser.Alter_authorization_for_parallel_dwContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#class_type.
    def visitClass_type(self, ctx:TSqlParser.Class_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#class_type_for_sql_database.
    def visitClass_type_for_sql_database(self, ctx:TSqlParser.Class_type_for_sql_databaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#class_type_for_azure_dw.
    def visitClass_type_for_azure_dw(self, ctx:TSqlParser.Class_type_for_azure_dwContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#class_type_for_parallel_dw.
    def visitClass_type_for_parallel_dw(self, ctx:TSqlParser.Class_type_for_parallel_dwContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#class_type_for_grant.
    def visitClass_type_for_grant(self, ctx:TSqlParser.Class_type_for_grantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_availability_group.
    def visitDrop_availability_group(self, ctx:TSqlParser.Drop_availability_groupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_availability_group.
    def visitAlter_availability_group(self, ctx:TSqlParser.Alter_availability_groupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_availability_group_start.
    def visitAlter_availability_group_start(self, ctx:TSqlParser.Alter_availability_group_startContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_availability_group_options.
    def visitAlter_availability_group_options(self, ctx:TSqlParser.Alter_availability_group_optionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#ip_v4_failover.
    def visitIp_v4_failover(self, ctx:TSqlParser.Ip_v4_failoverContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#ip_v6_failover.
    def visitIp_v6_failover(self, ctx:TSqlParser.Ip_v6_failoverContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_or_alter_broker_priority.
    def visitCreate_or_alter_broker_priority(self, ctx:TSqlParser.Create_or_alter_broker_priorityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_broker_priority.
    def visitDrop_broker_priority(self, ctx:TSqlParser.Drop_broker_priorityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_certificate.
    def visitAlter_certificate(self, ctx:TSqlParser.Alter_certificateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_column_encryption_key.
    def visitAlter_column_encryption_key(self, ctx:TSqlParser.Alter_column_encryption_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_column_encryption_key.
    def visitCreate_column_encryption_key(self, ctx:TSqlParser.Create_column_encryption_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_certificate.
    def visitDrop_certificate(self, ctx:TSqlParser.Drop_certificateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_column_encryption_key.
    def visitDrop_column_encryption_key(self, ctx:TSqlParser.Drop_column_encryption_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_column_master_key.
    def visitDrop_column_master_key(self, ctx:TSqlParser.Drop_column_master_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_contract.
    def visitDrop_contract(self, ctx:TSqlParser.Drop_contractContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_credential.
    def visitDrop_credential(self, ctx:TSqlParser.Drop_credentialContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_cryptograhic_provider.
    def visitDrop_cryptograhic_provider(self, ctx:TSqlParser.Drop_cryptograhic_providerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_database.
    def visitDrop_database(self, ctx:TSqlParser.Drop_databaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_database_audit_specification.
    def visitDrop_database_audit_specification(self, ctx:TSqlParser.Drop_database_audit_specificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_database_encryption_key.
    def visitDrop_database_encryption_key(self, ctx:TSqlParser.Drop_database_encryption_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_database_scoped_credential.
    def visitDrop_database_scoped_credential(self, ctx:TSqlParser.Drop_database_scoped_credentialContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_default.
    def visitDrop_default(self, ctx:TSqlParser.Drop_defaultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_endpoint.
    def visitDrop_endpoint(self, ctx:TSqlParser.Drop_endpointContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_external_data_source.
    def visitDrop_external_data_source(self, ctx:TSqlParser.Drop_external_data_sourceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_external_file_format.
    def visitDrop_external_file_format(self, ctx:TSqlParser.Drop_external_file_formatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_external_library.
    def visitDrop_external_library(self, ctx:TSqlParser.Drop_external_libraryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_external_resource_pool.
    def visitDrop_external_resource_pool(self, ctx:TSqlParser.Drop_external_resource_poolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_external_table.
    def visitDrop_external_table(self, ctx:TSqlParser.Drop_external_tableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_event_notifications.
    def visitDrop_event_notifications(self, ctx:TSqlParser.Drop_event_notificationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_event_session.
    def visitDrop_event_session(self, ctx:TSqlParser.Drop_event_sessionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_fulltext_catalog.
    def visitDrop_fulltext_catalog(self, ctx:TSqlParser.Drop_fulltext_catalogContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_fulltext_index.
    def visitDrop_fulltext_index(self, ctx:TSqlParser.Drop_fulltext_indexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_fulltext_stoplist.
    def visitDrop_fulltext_stoplist(self, ctx:TSqlParser.Drop_fulltext_stoplistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_login.
    def visitDrop_login(self, ctx:TSqlParser.Drop_loginContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_master_key.
    def visitDrop_master_key(self, ctx:TSqlParser.Drop_master_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_message_type.
    def visitDrop_message_type(self, ctx:TSqlParser.Drop_message_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_partition_function.
    def visitDrop_partition_function(self, ctx:TSqlParser.Drop_partition_functionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_partition_scheme.
    def visitDrop_partition_scheme(self, ctx:TSqlParser.Drop_partition_schemeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_queue.
    def visitDrop_queue(self, ctx:TSqlParser.Drop_queueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_remote_service_binding.
    def visitDrop_remote_service_binding(self, ctx:TSqlParser.Drop_remote_service_bindingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_resource_pool.
    def visitDrop_resource_pool(self, ctx:TSqlParser.Drop_resource_poolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_db_role.
    def visitDrop_db_role(self, ctx:TSqlParser.Drop_db_roleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_route.
    def visitDrop_route(self, ctx:TSqlParser.Drop_routeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_rule.
    def visitDrop_rule(self, ctx:TSqlParser.Drop_ruleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_schema.
    def visitDrop_schema(self, ctx:TSqlParser.Drop_schemaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_search_property_list.
    def visitDrop_search_property_list(self, ctx:TSqlParser.Drop_search_property_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_security_policy.
    def visitDrop_security_policy(self, ctx:TSqlParser.Drop_security_policyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_sequence.
    def visitDrop_sequence(self, ctx:TSqlParser.Drop_sequenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_server_audit.
    def visitDrop_server_audit(self, ctx:TSqlParser.Drop_server_auditContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_server_audit_specification.
    def visitDrop_server_audit_specification(self, ctx:TSqlParser.Drop_server_audit_specificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_server_role.
    def visitDrop_server_role(self, ctx:TSqlParser.Drop_server_roleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_service.
    def visitDrop_service(self, ctx:TSqlParser.Drop_serviceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_signature.
    def visitDrop_signature(self, ctx:TSqlParser.Drop_signatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_statistics_name_azure_dw_and_pdw.
    def visitDrop_statistics_name_azure_dw_and_pdw(self, ctx:TSqlParser.Drop_statistics_name_azure_dw_and_pdwContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_symmetric_key.
    def visitDrop_symmetric_key(self, ctx:TSqlParser.Drop_symmetric_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_synonym.
    def visitDrop_synonym(self, ctx:TSqlParser.Drop_synonymContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_user.
    def visitDrop_user(self, ctx:TSqlParser.Drop_userContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_workload_group.
    def visitDrop_workload_group(self, ctx:TSqlParser.Drop_workload_groupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_xml_schema_collection.
    def visitDrop_xml_schema_collection(self, ctx:TSqlParser.Drop_xml_schema_collectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#disable_trigger.
    def visitDisable_trigger(self, ctx:TSqlParser.Disable_triggerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#enable_trigger.
    def visitEnable_trigger(self, ctx:TSqlParser.Enable_triggerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#lock_table.
    def visitLock_table(self, ctx:TSqlParser.Lock_tableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#truncate_table.
    def visitTruncate_table(self, ctx:TSqlParser.Truncate_tableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_column_master_key.
    def visitCreate_column_master_key(self, ctx:TSqlParser.Create_column_master_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_credential.
    def visitAlter_credential(self, ctx:TSqlParser.Alter_credentialContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_credential.
    def visitCreate_credential(self, ctx:TSqlParser.Create_credentialContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_cryptographic_provider.
    def visitAlter_cryptographic_provider(self, ctx:TSqlParser.Alter_cryptographic_providerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_cryptographic_provider.
    def visitCreate_cryptographic_provider(self, ctx:TSqlParser.Create_cryptographic_providerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_endpoint.
    def visitCreate_endpoint(self, ctx:TSqlParser.Create_endpointContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#endpoint_encryption_alogorithm_clause.
    def visitEndpoint_encryption_alogorithm_clause(self, ctx:TSqlParser.Endpoint_encryption_alogorithm_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#endpoint_authentication_clause.
    def visitEndpoint_authentication_clause(self, ctx:TSqlParser.Endpoint_authentication_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#endpoint_listener_clause.
    def visitEndpoint_listener_clause(self, ctx:TSqlParser.Endpoint_listener_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_event_notification.
    def visitCreate_event_notification(self, ctx:TSqlParser.Create_event_notificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_or_alter_event_session.
    def visitCreate_or_alter_event_session(self, ctx:TSqlParser.Create_or_alter_event_sessionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#event_session_predicate_expression.
    def visitEvent_session_predicate_expression(self, ctx:TSqlParser.Event_session_predicate_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#event_session_predicate_factor.
    def visitEvent_session_predicate_factor(self, ctx:TSqlParser.Event_session_predicate_factorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#event_session_predicate_leaf.
    def visitEvent_session_predicate_leaf(self, ctx:TSqlParser.Event_session_predicate_leafContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_external_data_source.
    def visitAlter_external_data_source(self, ctx:TSqlParser.Alter_external_data_sourceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_external_library.
    def visitAlter_external_library(self, ctx:TSqlParser.Alter_external_libraryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_external_library.
    def visitCreate_external_library(self, ctx:TSqlParser.Create_external_libraryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_external_resource_pool.
    def visitAlter_external_resource_pool(self, ctx:TSqlParser.Alter_external_resource_poolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_external_resource_pool.
    def visitCreate_external_resource_pool(self, ctx:TSqlParser.Create_external_resource_poolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_fulltext_catalog.
    def visitAlter_fulltext_catalog(self, ctx:TSqlParser.Alter_fulltext_catalogContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_fulltext_catalog.
    def visitCreate_fulltext_catalog(self, ctx:TSqlParser.Create_fulltext_catalogContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_fulltext_stoplist.
    def visitAlter_fulltext_stoplist(self, ctx:TSqlParser.Alter_fulltext_stoplistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_fulltext_stoplist.
    def visitCreate_fulltext_stoplist(self, ctx:TSqlParser.Create_fulltext_stoplistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_login_sql_server.
    def visitAlter_login_sql_server(self, ctx:TSqlParser.Alter_login_sql_serverContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_login_sql_server.
    def visitCreate_login_sql_server(self, ctx:TSqlParser.Create_login_sql_serverContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_login_azure_sql.
    def visitAlter_login_azure_sql(self, ctx:TSqlParser.Alter_login_azure_sqlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_login_azure_sql.
    def visitCreate_login_azure_sql(self, ctx:TSqlParser.Create_login_azure_sqlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_login_azure_sql_dw_and_pdw.
    def visitAlter_login_azure_sql_dw_and_pdw(self, ctx:TSqlParser.Alter_login_azure_sql_dw_and_pdwContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_login_pdw.
    def visitCreate_login_pdw(self, ctx:TSqlParser.Create_login_pdwContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_master_key_sql_server.
    def visitAlter_master_key_sql_server(self, ctx:TSqlParser.Alter_master_key_sql_serverContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_master_key_sql_server.
    def visitCreate_master_key_sql_server(self, ctx:TSqlParser.Create_master_key_sql_serverContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_master_key_azure_sql.
    def visitAlter_master_key_azure_sql(self, ctx:TSqlParser.Alter_master_key_azure_sqlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_master_key_azure_sql.
    def visitCreate_master_key_azure_sql(self, ctx:TSqlParser.Create_master_key_azure_sqlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_message_type.
    def visitAlter_message_type(self, ctx:TSqlParser.Alter_message_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_partition_function.
    def visitAlter_partition_function(self, ctx:TSqlParser.Alter_partition_functionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_partition_scheme.
    def visitAlter_partition_scheme(self, ctx:TSqlParser.Alter_partition_schemeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_remote_service_binding.
    def visitAlter_remote_service_binding(self, ctx:TSqlParser.Alter_remote_service_bindingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_remote_service_binding.
    def visitCreate_remote_service_binding(self, ctx:TSqlParser.Create_remote_service_bindingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_resource_pool.
    def visitCreate_resource_pool(self, ctx:TSqlParser.Create_resource_poolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_resource_governor.
    def visitAlter_resource_governor(self, ctx:TSqlParser.Alter_resource_governorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_database_audit_specification.
    def visitAlter_database_audit_specification(self, ctx:TSqlParser.Alter_database_audit_specificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#audit_action_spec_group.
    def visitAudit_action_spec_group(self, ctx:TSqlParser.Audit_action_spec_groupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#audit_action_specification.
    def visitAudit_action_specification(self, ctx:TSqlParser.Audit_action_specificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#action_specification.
    def visitAction_specification(self, ctx:TSqlParser.Action_specificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#audit_class_name.
    def visitAudit_class_name(self, ctx:TSqlParser.Audit_class_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#audit_securable.
    def visitAudit_securable(self, ctx:TSqlParser.Audit_securableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_db_role.
    def visitAlter_db_role(self, ctx:TSqlParser.Alter_db_roleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_database_audit_specification.
    def visitCreate_database_audit_specification(self, ctx:TSqlParser.Create_database_audit_specificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_db_role.
    def visitCreate_db_role(self, ctx:TSqlParser.Create_db_roleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_route.
    def visitCreate_route(self, ctx:TSqlParser.Create_routeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_rule.
    def visitCreate_rule(self, ctx:TSqlParser.Create_ruleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_schema_sql.
    def visitAlter_schema_sql(self, ctx:TSqlParser.Alter_schema_sqlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_schema.
    def visitCreate_schema(self, ctx:TSqlParser.Create_schemaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_schema_azure_sql_dw_and_pdw.
    def visitCreate_schema_azure_sql_dw_and_pdw(self, ctx:TSqlParser.Create_schema_azure_sql_dw_and_pdwContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_schema_azure_sql_dw_and_pdw.
    def visitAlter_schema_azure_sql_dw_and_pdw(self, ctx:TSqlParser.Alter_schema_azure_sql_dw_and_pdwContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_search_property_list.
    def visitCreate_search_property_list(self, ctx:TSqlParser.Create_search_property_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_security_policy.
    def visitCreate_security_policy(self, ctx:TSqlParser.Create_security_policyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_sequence.
    def visitAlter_sequence(self, ctx:TSqlParser.Alter_sequenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_sequence.
    def visitCreate_sequence(self, ctx:TSqlParser.Create_sequenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_server_audit.
    def visitAlter_server_audit(self, ctx:TSqlParser.Alter_server_auditContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_server_audit.
    def visitCreate_server_audit(self, ctx:TSqlParser.Create_server_auditContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_server_audit_specification.
    def visitAlter_server_audit_specification(self, ctx:TSqlParser.Alter_server_audit_specificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_server_audit_specification.
    def visitCreate_server_audit_specification(self, ctx:TSqlParser.Create_server_audit_specificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_server_configuration.
    def visitAlter_server_configuration(self, ctx:TSqlParser.Alter_server_configurationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_server_role.
    def visitAlter_server_role(self, ctx:TSqlParser.Alter_server_roleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_server_role.
    def visitCreate_server_role(self, ctx:TSqlParser.Create_server_roleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_server_role_pdw.
    def visitAlter_server_role_pdw(self, ctx:TSqlParser.Alter_server_role_pdwContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_service.
    def visitAlter_service(self, ctx:TSqlParser.Alter_serviceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#opt_arg_clause.
    def visitOpt_arg_clause(self, ctx:TSqlParser.Opt_arg_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_service.
    def visitCreate_service(self, ctx:TSqlParser.Create_serviceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_service_master_key.
    def visitAlter_service_master_key(self, ctx:TSqlParser.Alter_service_master_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_symmetric_key.
    def visitAlter_symmetric_key(self, ctx:TSqlParser.Alter_symmetric_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_synonym.
    def visitCreate_synonym(self, ctx:TSqlParser.Create_synonymContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_user.
    def visitAlter_user(self, ctx:TSqlParser.Alter_userContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_user.
    def visitCreate_user(self, ctx:TSqlParser.Create_userContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_user_azure_sql_dw.
    def visitCreate_user_azure_sql_dw(self, ctx:TSqlParser.Create_user_azure_sql_dwContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_user_azure_sql.
    def visitAlter_user_azure_sql(self, ctx:TSqlParser.Alter_user_azure_sqlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_workload_group.
    def visitAlter_workload_group(self, ctx:TSqlParser.Alter_workload_groupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_workload_group.
    def visitCreate_workload_group(self, ctx:TSqlParser.Create_workload_groupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_xml_schema_collection.
    def visitCreate_xml_schema_collection(self, ctx:TSqlParser.Create_xml_schema_collectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_partition_function.
    def visitCreate_partition_function(self, ctx:TSqlParser.Create_partition_functionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_partition_scheme.
    def visitCreate_partition_scheme(self, ctx:TSqlParser.Create_partition_schemeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_queue.
    def visitCreate_queue(self, ctx:TSqlParser.Create_queueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#queue_settings.
    def visitQueue_settings(self, ctx:TSqlParser.Queue_settingsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_queue.
    def visitAlter_queue(self, ctx:TSqlParser.Alter_queueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#queue_action.
    def visitQueue_action(self, ctx:TSqlParser.Queue_actionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#queue_rebuild_options.
    def visitQueue_rebuild_options(self, ctx:TSqlParser.Queue_rebuild_optionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_contract.
    def visitCreate_contract(self, ctx:TSqlParser.Create_contractContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#conversation_statement.
    def visitConversation_statement(self, ctx:TSqlParser.Conversation_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#message_statement.
    def visitMessage_statement(self, ctx:TSqlParser.Message_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#merge_statement.
    def visitMerge_statement(self, ctx:TSqlParser.Merge_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#when_matches.
    def visitWhen_matches(self, ctx:TSqlParser.When_matchesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#merge_matched.
    def visitMerge_matched(self, ctx:TSqlParser.Merge_matchedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#merge_not_matched.
    def visitMerge_not_matched(self, ctx:TSqlParser.Merge_not_matchedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#delete_statement.
    def visitDelete_statement(self, ctx:TSqlParser.Delete_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#delete_statement_from.
    def visitDelete_statement_from(self, ctx:TSqlParser.Delete_statement_fromContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#insert_statement.
    def visitInsert_statement(self, ctx:TSqlParser.Insert_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#insert_statement_value.
    def visitInsert_statement_value(self, ctx:TSqlParser.Insert_statement_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#receive_statement.
    def visitReceive_statement(self, ctx:TSqlParser.Receive_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#select_statement_standalone.
    def visitSelect_statement_standalone(self, ctx:TSqlParser.Select_statement_standaloneContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#select_statement.
    def visitSelect_statement(self, ctx:TSqlParser.Select_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#time.
    def visitTime(self, ctx:TSqlParser.TimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#update_statement.
    def visitUpdate_statement(self, ctx:TSqlParser.Update_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#output_clause.
    def visitOutput_clause(self, ctx:TSqlParser.Output_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#output_dml_list_elem.
    def visitOutput_dml_list_elem(self, ctx:TSqlParser.Output_dml_list_elemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_database.
    def visitCreate_database(self, ctx:TSqlParser.Create_databaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_index.
    def visitCreate_index(self, ctx:TSqlParser.Create_indexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_index_options.
    def visitCreate_index_options(self, ctx:TSqlParser.Create_index_optionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#relational_index_option.
    def visitRelational_index_option(self, ctx:TSqlParser.Relational_index_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_index.
    def visitAlter_index(self, ctx:TSqlParser.Alter_indexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#resumable_index_options.
    def visitResumable_index_options(self, ctx:TSqlParser.Resumable_index_optionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#resumable_index_option.
    def visitResumable_index_option(self, ctx:TSqlParser.Resumable_index_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#reorganize_partition.
    def visitReorganize_partition(self, ctx:TSqlParser.Reorganize_partitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#reorganize_options.
    def visitReorganize_options(self, ctx:TSqlParser.Reorganize_optionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#reorganize_option.
    def visitReorganize_option(self, ctx:TSqlParser.Reorganize_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#set_index_options.
    def visitSet_index_options(self, ctx:TSqlParser.Set_index_optionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#set_index_option.
    def visitSet_index_option(self, ctx:TSqlParser.Set_index_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#rebuild_partition.
    def visitRebuild_partition(self, ctx:TSqlParser.Rebuild_partitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#rebuild_index_options.
    def visitRebuild_index_options(self, ctx:TSqlParser.Rebuild_index_optionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#rebuild_index_option.
    def visitRebuild_index_option(self, ctx:TSqlParser.Rebuild_index_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#single_partition_rebuild_index_options.
    def visitSingle_partition_rebuild_index_options(self, ctx:TSqlParser.Single_partition_rebuild_index_optionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#single_partition_rebuild_index_option.
    def visitSingle_partition_rebuild_index_option(self, ctx:TSqlParser.Single_partition_rebuild_index_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#on_partitions.
    def visitOn_partitions(self, ctx:TSqlParser.On_partitionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_columnstore_index.
    def visitCreate_columnstore_index(self, ctx:TSqlParser.Create_columnstore_indexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_columnstore_index_options.
    def visitCreate_columnstore_index_options(self, ctx:TSqlParser.Create_columnstore_index_optionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#columnstore_index_option.
    def visitColumnstore_index_option(self, ctx:TSqlParser.Columnstore_index_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_nonclustered_columnstore_index.
    def visitCreate_nonclustered_columnstore_index(self, ctx:TSqlParser.Create_nonclustered_columnstore_indexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_xml_index.
    def visitCreate_xml_index(self, ctx:TSqlParser.Create_xml_indexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#xml_index_options.
    def visitXml_index_options(self, ctx:TSqlParser.Xml_index_optionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#xml_index_option.
    def visitXml_index_option(self, ctx:TSqlParser.Xml_index_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_or_alter_procedure.
    def visitCreate_or_alter_procedure(self, ctx:TSqlParser.Create_or_alter_procedureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#as_external_name.
    def visitAs_external_name(self, ctx:TSqlParser.As_external_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_or_alter_trigger.
    def visitCreate_or_alter_trigger(self, ctx:TSqlParser.Create_or_alter_triggerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_or_alter_dml_trigger.
    def visitCreate_or_alter_dml_trigger(self, ctx:TSqlParser.Create_or_alter_dml_triggerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dml_trigger_option.
    def visitDml_trigger_option(self, ctx:TSqlParser.Dml_trigger_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dml_trigger_operation.
    def visitDml_trigger_operation(self, ctx:TSqlParser.Dml_trigger_operationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_or_alter_ddl_trigger.
    def visitCreate_or_alter_ddl_trigger(self, ctx:TSqlParser.Create_or_alter_ddl_triggerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#ddl_trigger_operation.
    def visitDdl_trigger_operation(self, ctx:TSqlParser.Ddl_trigger_operationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_or_alter_function.
    def visitCreate_or_alter_function(self, ctx:TSqlParser.Create_or_alter_functionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#func_body_returns_select.
    def visitFunc_body_returns_select(self, ctx:TSqlParser.Func_body_returns_selectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#func_body_returns_table.
    def visitFunc_body_returns_table(self, ctx:TSqlParser.Func_body_returns_tableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#func_body_returns_scalar.
    def visitFunc_body_returns_scalar(self, ctx:TSqlParser.Func_body_returns_scalarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#procedure_param_default_value.
    def visitProcedure_param_default_value(self, ctx:TSqlParser.Procedure_param_default_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#procedure_param.
    def visitProcedure_param(self, ctx:TSqlParser.Procedure_paramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#procedure_option.
    def visitProcedure_option(self, ctx:TSqlParser.Procedure_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#function_option.
    def visitFunction_option(self, ctx:TSqlParser.Function_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_statistics.
    def visitCreate_statistics(self, ctx:TSqlParser.Create_statisticsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#update_statistics.
    def visitUpdate_statistics(self, ctx:TSqlParser.Update_statisticsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#update_statistics_options.
    def visitUpdate_statistics_options(self, ctx:TSqlParser.Update_statistics_optionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#update_statistics_option.
    def visitUpdate_statistics_option(self, ctx:TSqlParser.Update_statistics_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_table.
    def visitCreate_table(self, ctx:TSqlParser.Create_tableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#table_indices.
    def visitTable_indices(self, ctx:TSqlParser.Table_indicesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#table_options.
    def visitTable_options(self, ctx:TSqlParser.Table_optionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#table_option.
    def visitTable_option(self, ctx:TSqlParser.Table_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_table_index_options.
    def visitCreate_table_index_options(self, ctx:TSqlParser.Create_table_index_optionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_table_index_option.
    def visitCreate_table_index_option(self, ctx:TSqlParser.Create_table_index_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_view.
    def visitCreate_view(self, ctx:TSqlParser.Create_viewContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#view_attribute.
    def visitView_attribute(self, ctx:TSqlParser.View_attributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_table.
    def visitAlter_table(self, ctx:TSqlParser.Alter_tableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#switch_partition.
    def visitSwitch_partition(self, ctx:TSqlParser.Switch_partitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#low_priority_lock_wait.
    def visitLow_priority_lock_wait(self, ctx:TSqlParser.Low_priority_lock_waitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_database.
    def visitAlter_database(self, ctx:TSqlParser.Alter_databaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#add_or_modify_files.
    def visitAdd_or_modify_files(self, ctx:TSqlParser.Add_or_modify_filesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#filespec.
    def visitFilespec(self, ctx:TSqlParser.FilespecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#add_or_modify_filegroups.
    def visitAdd_or_modify_filegroups(self, ctx:TSqlParser.Add_or_modify_filegroupsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#filegroup_updatability_option.
    def visitFilegroup_updatability_option(self, ctx:TSqlParser.Filegroup_updatability_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#database_optionspec.
    def visitDatabase_optionspec(self, ctx:TSqlParser.Database_optionspecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#auto_option.
    def visitAuto_option(self, ctx:TSqlParser.Auto_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#change_tracking_option.
    def visitChange_tracking_option(self, ctx:TSqlParser.Change_tracking_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#change_tracking_option_list.
    def visitChange_tracking_option_list(self, ctx:TSqlParser.Change_tracking_option_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#containment_option.
    def visitContainment_option(self, ctx:TSqlParser.Containment_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#cursor_option.
    def visitCursor_option(self, ctx:TSqlParser.Cursor_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_endpoint.
    def visitAlter_endpoint(self, ctx:TSqlParser.Alter_endpointContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#database_mirroring_option.
    def visitDatabase_mirroring_option(self, ctx:TSqlParser.Database_mirroring_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#mirroring_set_option.
    def visitMirroring_set_option(self, ctx:TSqlParser.Mirroring_set_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#mirroring_partner.
    def visitMirroring_partner(self, ctx:TSqlParser.Mirroring_partnerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#mirroring_witness.
    def visitMirroring_witness(self, ctx:TSqlParser.Mirroring_witnessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#witness_partner_equal.
    def visitWitness_partner_equal(self, ctx:TSqlParser.Witness_partner_equalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#partner_option.
    def visitPartner_option(self, ctx:TSqlParser.Partner_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#witness_option.
    def visitWitness_option(self, ctx:TSqlParser.Witness_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#witness_server.
    def visitWitness_server(self, ctx:TSqlParser.Witness_serverContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#partner_server.
    def visitPartner_server(self, ctx:TSqlParser.Partner_serverContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#mirroring_host_port_seperator.
    def visitMirroring_host_port_seperator(self, ctx:TSqlParser.Mirroring_host_port_seperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#partner_server_tcp_prefix.
    def visitPartner_server_tcp_prefix(self, ctx:TSqlParser.Partner_server_tcp_prefixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#port_number.
    def visitPort_number(self, ctx:TSqlParser.Port_numberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#host.
    def visitHost(self, ctx:TSqlParser.HostContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#date_correlation_optimization_option.
    def visitDate_correlation_optimization_option(self, ctx:TSqlParser.Date_correlation_optimization_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#db_encryption_option.
    def visitDb_encryption_option(self, ctx:TSqlParser.Db_encryption_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#db_state_option.
    def visitDb_state_option(self, ctx:TSqlParser.Db_state_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#db_update_option.
    def visitDb_update_option(self, ctx:TSqlParser.Db_update_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#db_user_access_option.
    def visitDb_user_access_option(self, ctx:TSqlParser.Db_user_access_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#delayed_durability_option.
    def visitDelayed_durability_option(self, ctx:TSqlParser.Delayed_durability_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#external_access_option.
    def visitExternal_access_option(self, ctx:TSqlParser.External_access_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#hadr_options.
    def visitHadr_options(self, ctx:TSqlParser.Hadr_optionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#mixed_page_allocation_option.
    def visitMixed_page_allocation_option(self, ctx:TSqlParser.Mixed_page_allocation_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#parameterization_option.
    def visitParameterization_option(self, ctx:TSqlParser.Parameterization_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#recovery_option.
    def visitRecovery_option(self, ctx:TSqlParser.Recovery_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#service_broker_option.
    def visitService_broker_option(self, ctx:TSqlParser.Service_broker_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#snapshot_option.
    def visitSnapshot_option(self, ctx:TSqlParser.Snapshot_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#sql_option.
    def visitSql_option(self, ctx:TSqlParser.Sql_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#target_recovery_time_option.
    def visitTarget_recovery_time_option(self, ctx:TSqlParser.Target_recovery_time_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#termination.
    def visitTermination(self, ctx:TSqlParser.TerminationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_index.
    def visitDrop_index(self, ctx:TSqlParser.Drop_indexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_relational_or_xml_or_spatial_index.
    def visitDrop_relational_or_xml_or_spatial_index(self, ctx:TSqlParser.Drop_relational_or_xml_or_spatial_indexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_backward_compatible_index.
    def visitDrop_backward_compatible_index(self, ctx:TSqlParser.Drop_backward_compatible_indexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_procedure.
    def visitDrop_procedure(self, ctx:TSqlParser.Drop_procedureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_trigger.
    def visitDrop_trigger(self, ctx:TSqlParser.Drop_triggerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_dml_trigger.
    def visitDrop_dml_trigger(self, ctx:TSqlParser.Drop_dml_triggerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_ddl_trigger.
    def visitDrop_ddl_trigger(self, ctx:TSqlParser.Drop_ddl_triggerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_function.
    def visitDrop_function(self, ctx:TSqlParser.Drop_functionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_statistics.
    def visitDrop_statistics(self, ctx:TSqlParser.Drop_statisticsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_table.
    def visitDrop_table(self, ctx:TSqlParser.Drop_tableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_view.
    def visitDrop_view(self, ctx:TSqlParser.Drop_viewContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_type.
    def visitCreate_type(self, ctx:TSqlParser.Create_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#drop_type.
    def visitDrop_type(self, ctx:TSqlParser.Drop_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#rowset_function_limited.
    def visitRowset_function_limited(self, ctx:TSqlParser.Rowset_function_limitedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#openquery.
    def visitOpenquery(self, ctx:TSqlParser.OpenqueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#opendatasource.
    def visitOpendatasource(self, ctx:TSqlParser.OpendatasourceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#declare_statement.
    def visitDeclare_statement(self, ctx:TSqlParser.Declare_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#xml_declaration.
    def visitXml_declaration(self, ctx:TSqlParser.Xml_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#cursor_statement.
    def visitCursor_statement(self, ctx:TSqlParser.Cursor_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#backup_database.
    def visitBackup_database(self, ctx:TSqlParser.Backup_databaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#backup_log.
    def visitBackup_log(self, ctx:TSqlParser.Backup_logContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#backup_certificate.
    def visitBackup_certificate(self, ctx:TSqlParser.Backup_certificateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#backup_master_key.
    def visitBackup_master_key(self, ctx:TSqlParser.Backup_master_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#backup_service_master_key.
    def visitBackup_service_master_key(self, ctx:TSqlParser.Backup_service_master_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#kill_statement.
    def visitKill_statement(self, ctx:TSqlParser.Kill_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#kill_process.
    def visitKill_process(self, ctx:TSqlParser.Kill_processContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#kill_query_notification.
    def visitKill_query_notification(self, ctx:TSqlParser.Kill_query_notificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#kill_stats_job.
    def visitKill_stats_job(self, ctx:TSqlParser.Kill_stats_jobContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#execute_statement.
    def visitExecute_statement(self, ctx:TSqlParser.Execute_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#execute_body_batch.
    def visitExecute_body_batch(self, ctx:TSqlParser.Execute_body_batchContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#execute_body.
    def visitExecute_body(self, ctx:TSqlParser.Execute_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#execute_statement_arg.
    def visitExecute_statement_arg(self, ctx:TSqlParser.Execute_statement_argContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#execute_statement_arg_named.
    def visitExecute_statement_arg_named(self, ctx:TSqlParser.Execute_statement_arg_namedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#execute_statement_arg_unnamed.
    def visitExecute_statement_arg_unnamed(self, ctx:TSqlParser.Execute_statement_arg_unnamedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#execute_parameter.
    def visitExecute_parameter(self, ctx:TSqlParser.Execute_parameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#execute_var_string.
    def visitExecute_var_string(self, ctx:TSqlParser.Execute_var_stringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#security_statement.
    def visitSecurity_statement(self, ctx:TSqlParser.Security_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#principal_id.
    def visitPrincipal_id(self, ctx:TSqlParser.Principal_idContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_certificate.
    def visitCreate_certificate(self, ctx:TSqlParser.Create_certificateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#existing_keys.
    def visitExisting_keys(self, ctx:TSqlParser.Existing_keysContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#private_key_options.
    def visitPrivate_key_options(self, ctx:TSqlParser.Private_key_optionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#generate_new_keys.
    def visitGenerate_new_keys(self, ctx:TSqlParser.Generate_new_keysContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#date_options.
    def visitDate_options(self, ctx:TSqlParser.Date_optionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#open_key.
    def visitOpen_key(self, ctx:TSqlParser.Open_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#close_key.
    def visitClose_key(self, ctx:TSqlParser.Close_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_key.
    def visitCreate_key(self, ctx:TSqlParser.Create_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#key_options.
    def visitKey_options(self, ctx:TSqlParser.Key_optionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#algorithm.
    def visitAlgorithm(self, ctx:TSqlParser.AlgorithmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#encryption_mechanism.
    def visitEncryption_mechanism(self, ctx:TSqlParser.Encryption_mechanismContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#decryption_mechanism.
    def visitDecryption_mechanism(self, ctx:TSqlParser.Decryption_mechanismContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#grant_permission.
    def visitGrant_permission(self, ctx:TSqlParser.Grant_permissionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#set_statement.
    def visitSet_statement(self, ctx:TSqlParser.Set_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#transaction_statement.
    def visitTransaction_statement(self, ctx:TSqlParser.Transaction_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#go_statement.
    def visitGo_statement(self, ctx:TSqlParser.Go_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#use_statement.
    def visitUse_statement(self, ctx:TSqlParser.Use_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#setuser_statement.
    def visitSetuser_statement(self, ctx:TSqlParser.Setuser_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#reconfigure_statement.
    def visitReconfigure_statement(self, ctx:TSqlParser.Reconfigure_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#shutdown_statement.
    def visitShutdown_statement(self, ctx:TSqlParser.Shutdown_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#checkpoint_statement.
    def visitCheckpoint_statement(self, ctx:TSqlParser.Checkpoint_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dbcc_checkalloc_option.
    def visitDbcc_checkalloc_option(self, ctx:TSqlParser.Dbcc_checkalloc_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dbcc_checkalloc.
    def visitDbcc_checkalloc(self, ctx:TSqlParser.Dbcc_checkallocContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dbcc_checkcatalog.
    def visitDbcc_checkcatalog(self, ctx:TSqlParser.Dbcc_checkcatalogContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dbcc_checkconstraints_option.
    def visitDbcc_checkconstraints_option(self, ctx:TSqlParser.Dbcc_checkconstraints_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dbcc_checkconstraints.
    def visitDbcc_checkconstraints(self, ctx:TSqlParser.Dbcc_checkconstraintsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dbcc_checkdb_table_option.
    def visitDbcc_checkdb_table_option(self, ctx:TSqlParser.Dbcc_checkdb_table_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dbcc_checkdb.
    def visitDbcc_checkdb(self, ctx:TSqlParser.Dbcc_checkdbContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dbcc_checkfilegroup_option.
    def visitDbcc_checkfilegroup_option(self, ctx:TSqlParser.Dbcc_checkfilegroup_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dbcc_checkfilegroup.
    def visitDbcc_checkfilegroup(self, ctx:TSqlParser.Dbcc_checkfilegroupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dbcc_checktable.
    def visitDbcc_checktable(self, ctx:TSqlParser.Dbcc_checktableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dbcc_cleantable.
    def visitDbcc_cleantable(self, ctx:TSqlParser.Dbcc_cleantableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dbcc_clonedatabase_option.
    def visitDbcc_clonedatabase_option(self, ctx:TSqlParser.Dbcc_clonedatabase_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dbcc_clonedatabase.
    def visitDbcc_clonedatabase(self, ctx:TSqlParser.Dbcc_clonedatabaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dbcc_pdw_showspaceused.
    def visitDbcc_pdw_showspaceused(self, ctx:TSqlParser.Dbcc_pdw_showspaceusedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dbcc_proccache.
    def visitDbcc_proccache(self, ctx:TSqlParser.Dbcc_proccacheContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dbcc_showcontig_option.
    def visitDbcc_showcontig_option(self, ctx:TSqlParser.Dbcc_showcontig_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dbcc_showcontig.
    def visitDbcc_showcontig(self, ctx:TSqlParser.Dbcc_showcontigContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dbcc_shrinklog.
    def visitDbcc_shrinklog(self, ctx:TSqlParser.Dbcc_shrinklogContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dbcc_dbreindex.
    def visitDbcc_dbreindex(self, ctx:TSqlParser.Dbcc_dbreindexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dbcc_dll_free.
    def visitDbcc_dll_free(self, ctx:TSqlParser.Dbcc_dll_freeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dbcc_dropcleanbuffers.
    def visitDbcc_dropcleanbuffers(self, ctx:TSqlParser.Dbcc_dropcleanbuffersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dbcc_clause.
    def visitDbcc_clause(self, ctx:TSqlParser.Dbcc_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#execute_clause.
    def visitExecute_clause(self, ctx:TSqlParser.Execute_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#declare_local.
    def visitDeclare_local(self, ctx:TSqlParser.Declare_localContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#table_type_definition.
    def visitTable_type_definition(self, ctx:TSqlParser.Table_type_definitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#table_type_indices.
    def visitTable_type_indices(self, ctx:TSqlParser.Table_type_indicesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#xml_type_definition.
    def visitXml_type_definition(self, ctx:TSqlParser.Xml_type_definitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#xml_schema_collection.
    def visitXml_schema_collection(self, ctx:TSqlParser.Xml_schema_collectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#column_def_table_constraints.
    def visitColumn_def_table_constraints(self, ctx:TSqlParser.Column_def_table_constraintsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#column_def_table_constraint.
    def visitColumn_def_table_constraint(self, ctx:TSqlParser.Column_def_table_constraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#column_definition.
    def visitColumn_definition(self, ctx:TSqlParser.Column_definitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#column_definition_element.
    def visitColumn_definition_element(self, ctx:TSqlParser.Column_definition_elementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#column_modifier.
    def visitColumn_modifier(self, ctx:TSqlParser.Column_modifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#materialized_column_definition.
    def visitMaterialized_column_definition(self, ctx:TSqlParser.Materialized_column_definitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#column_constraint.
    def visitColumn_constraint(self, ctx:TSqlParser.Column_constraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#column_index.
    def visitColumn_index(self, ctx:TSqlParser.Column_indexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#on_partition_or_filegroup.
    def visitOn_partition_or_filegroup(self, ctx:TSqlParser.On_partition_or_filegroupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#table_constraint.
    def visitTable_constraint(self, ctx:TSqlParser.Table_constraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#connection_node.
    def visitConnection_node(self, ctx:TSqlParser.Connection_nodeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#primary_key_options.
    def visitPrimary_key_options(self, ctx:TSqlParser.Primary_key_optionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#foreign_key_options.
    def visitForeign_key_options(self, ctx:TSqlParser.Foreign_key_optionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#check_constraint.
    def visitCheck_constraint(self, ctx:TSqlParser.Check_constraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#on_delete.
    def visitOn_delete(self, ctx:TSqlParser.On_deleteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#on_update.
    def visitOn_update(self, ctx:TSqlParser.On_updateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_table_index_options.
    def visitAlter_table_index_options(self, ctx:TSqlParser.Alter_table_index_optionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#alter_table_index_option.
    def visitAlter_table_index_option(self, ctx:TSqlParser.Alter_table_index_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#declare_cursor.
    def visitDeclare_cursor(self, ctx:TSqlParser.Declare_cursorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#declare_set_cursor_common.
    def visitDeclare_set_cursor_common(self, ctx:TSqlParser.Declare_set_cursor_commonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#declare_set_cursor_common_partial.
    def visitDeclare_set_cursor_common_partial(self, ctx:TSqlParser.Declare_set_cursor_common_partialContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#fetch_cursor.
    def visitFetch_cursor(self, ctx:TSqlParser.Fetch_cursorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#set_special.
    def visitSet_special(self, ctx:TSqlParser.Set_specialContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#special_list.
    def visitSpecial_list(self, ctx:TSqlParser.Special_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#constant_LOCAL_ID.
    def visitConstant_LOCAL_ID(self, ctx:TSqlParser.Constant_LOCAL_IDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#expression.
    def visitExpression(self, ctx:TSqlParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#parameter.
    def visitParameter(self, ctx:TSqlParser.ParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#time_zone.
    def visitTime_zone(self, ctx:TSqlParser.Time_zoneContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#primitive_expression.
    def visitPrimitive_expression(self, ctx:TSqlParser.Primitive_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#case_expression.
    def visitCase_expression(self, ctx:TSqlParser.Case_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#unary_operator_expression.
    def visitUnary_operator_expression(self, ctx:TSqlParser.Unary_operator_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#bracket_expression.
    def visitBracket_expression(self, ctx:TSqlParser.Bracket_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#subquery.
    def visitSubquery(self, ctx:TSqlParser.SubqueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#with_expression.
    def visitWith_expression(self, ctx:TSqlParser.With_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#common_table_expression.
    def visitCommon_table_expression(self, ctx:TSqlParser.Common_table_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#update_elem.
    def visitUpdate_elem(self, ctx:TSqlParser.Update_elemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#update_elem_merge.
    def visitUpdate_elem_merge(self, ctx:TSqlParser.Update_elem_mergeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#search_condition.
    def visitSearch_condition(self, ctx:TSqlParser.Search_conditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#predicate.
    def visitPredicate(self, ctx:TSqlParser.PredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#query_expression.
    def visitQuery_expression(self, ctx:TSqlParser.Query_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#sql_union.
    def visitSql_union(self, ctx:TSqlParser.Sql_unionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#query_specification.
    def visitQuery_specification(self, ctx:TSqlParser.Query_specificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#top_clause.
    def visitTop_clause(self, ctx:TSqlParser.Top_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#top_percent.
    def visitTop_percent(self, ctx:TSqlParser.Top_percentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#top_count.
    def visitTop_count(self, ctx:TSqlParser.Top_countContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#order_by_clause.
    def visitOrder_by_clause(self, ctx:TSqlParser.Order_by_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#select_order_by_clause.
    def visitSelect_order_by_clause(self, ctx:TSqlParser.Select_order_by_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#for_clause.
    def visitFor_clause(self, ctx:TSqlParser.For_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#xml_common_directives.
    def visitXml_common_directives(self, ctx:TSqlParser.Xml_common_directivesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#order_by_expression.
    def visitOrder_by_expression(self, ctx:TSqlParser.Order_by_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#grouping_sets_item.
    def visitGrouping_sets_item(self, ctx:TSqlParser.Grouping_sets_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#group_by_item.
    def visitGroup_by_item(self, ctx:TSqlParser.Group_by_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#option_clause.
    def visitOption_clause(self, ctx:TSqlParser.Option_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#option.
    def visitOption(self, ctx:TSqlParser.OptionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#optimize_for_arg.
    def visitOptimize_for_arg(self, ctx:TSqlParser.Optimize_for_argContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#select_list.
    def visitSelect_list(self, ctx:TSqlParser.Select_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#udt_method_arguments.
    def visitUdt_method_arguments(self, ctx:TSqlParser.Udt_method_argumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#asterisk.
    def visitAsterisk(self, ctx:TSqlParser.AsteriskContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#udt_elem.
    def visitUdt_elem(self, ctx:TSqlParser.Udt_elemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#expression_elem.
    def visitExpression_elem(self, ctx:TSqlParser.Expression_elemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#select_list_elem.
    def visitSelect_list_elem(self, ctx:TSqlParser.Select_list_elemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#table_sources.
    def visitTable_sources(self, ctx:TSqlParser.Table_sourcesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#non_ansi_join.
    def visitNon_ansi_join(self, ctx:TSqlParser.Non_ansi_joinContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#table_source.
    def visitTable_source(self, ctx:TSqlParser.Table_sourceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#table_source_item.
    def visitTable_source_item(self, ctx:TSqlParser.Table_source_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#open_xml.
    def visitOpen_xml(self, ctx:TSqlParser.Open_xmlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#open_json.
    def visitOpen_json(self, ctx:TSqlParser.Open_jsonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#json_declaration.
    def visitJson_declaration(self, ctx:TSqlParser.Json_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#json_column_declaration.
    def visitJson_column_declaration(self, ctx:TSqlParser.Json_column_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#schema_declaration.
    def visitSchema_declaration(self, ctx:TSqlParser.Schema_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#column_declaration.
    def visitColumn_declaration(self, ctx:TSqlParser.Column_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#change_table.
    def visitChange_table(self, ctx:TSqlParser.Change_tableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#change_table_changes.
    def visitChange_table_changes(self, ctx:TSqlParser.Change_table_changesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#change_table_version.
    def visitChange_table_version(self, ctx:TSqlParser.Change_table_versionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#join_part.
    def visitJoin_part(self, ctx:TSqlParser.Join_partContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#join_on.
    def visitJoin_on(self, ctx:TSqlParser.Join_onContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#cross_join.
    def visitCross_join(self, ctx:TSqlParser.Cross_joinContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#apply_.
    def visitApply_(self, ctx:TSqlParser.Apply_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#pivot.
    def visitPivot(self, ctx:TSqlParser.PivotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#unpivot.
    def visitUnpivot(self, ctx:TSqlParser.UnpivotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#pivot_clause.
    def visitPivot_clause(self, ctx:TSqlParser.Pivot_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#unpivot_clause.
    def visitUnpivot_clause(self, ctx:TSqlParser.Unpivot_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#full_column_name_list.
    def visitFull_column_name_list(self, ctx:TSqlParser.Full_column_name_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#rowset_function.
    def visitRowset_function(self, ctx:TSqlParser.Rowset_functionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#bulk_option.
    def visitBulk_option(self, ctx:TSqlParser.Bulk_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#derived_table.
    def visitDerived_table(self, ctx:TSqlParser.Derived_tableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#RANKING_WINDOWED_FUNC.
    def visitRANKING_WINDOWED_FUNC(self, ctx:TSqlParser.RANKING_WINDOWED_FUNCContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#AGGREGATE_WINDOWED_FUNC.
    def visitAGGREGATE_WINDOWED_FUNC(self, ctx:TSqlParser.AGGREGATE_WINDOWED_FUNCContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#ANALYTIC_WINDOWED_FUNC.
    def visitANALYTIC_WINDOWED_FUNC(self, ctx:TSqlParser.ANALYTIC_WINDOWED_FUNCContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#BUILT_IN_FUNC.
    def visitBUILT_IN_FUNC(self, ctx:TSqlParser.BUILT_IN_FUNCContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#SCALAR_FUNCTION.
    def visitSCALAR_FUNCTION(self, ctx:TSqlParser.SCALAR_FUNCTIONContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#FREE_TEXT.
    def visitFREE_TEXT(self, ctx:TSqlParser.FREE_TEXTContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#PARTITION_FUNC.
    def visitPARTITION_FUNC(self, ctx:TSqlParser.PARTITION_FUNCContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#HIERARCHYID_METHOD.
    def visitHIERARCHYID_METHOD(self, ctx:TSqlParser.HIERARCHYID_METHODContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#partition_function.
    def visitPartition_function(self, ctx:TSqlParser.Partition_functionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#freetext_function.
    def visitFreetext_function(self, ctx:TSqlParser.Freetext_functionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#freetext_predicate.
    def visitFreetext_predicate(self, ctx:TSqlParser.Freetext_predicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#json_key_value.
    def visitJson_key_value(self, ctx:TSqlParser.Json_key_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#json_null_clause.
    def visitJson_null_clause(self, ctx:TSqlParser.Json_null_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#APP_NAME.
    def visitAPP_NAME(self, ctx:TSqlParser.APP_NAMEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#APPLOCK_MODE.
    def visitAPPLOCK_MODE(self, ctx:TSqlParser.APPLOCK_MODEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#APPLOCK_TEST.
    def visitAPPLOCK_TEST(self, ctx:TSqlParser.APPLOCK_TESTContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#ASSEMBLYPROPERTY.
    def visitASSEMBLYPROPERTY(self, ctx:TSqlParser.ASSEMBLYPROPERTYContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#COL_LENGTH.
    def visitCOL_LENGTH(self, ctx:TSqlParser.COL_LENGTHContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#COL_NAME.
    def visitCOL_NAME(self, ctx:TSqlParser.COL_NAMEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#COLUMNPROPERTY.
    def visitCOLUMNPROPERTY(self, ctx:TSqlParser.COLUMNPROPERTYContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#DATABASEPROPERTYEX.
    def visitDATABASEPROPERTYEX(self, ctx:TSqlParser.DATABASEPROPERTYEXContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#DB_ID.
    def visitDB_ID(self, ctx:TSqlParser.DB_IDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#DB_NAME.
    def visitDB_NAME(self, ctx:TSqlParser.DB_NAMEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#FILE_ID.
    def visitFILE_ID(self, ctx:TSqlParser.FILE_IDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#FILE_IDEX.
    def visitFILE_IDEX(self, ctx:TSqlParser.FILE_IDEXContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#FILE_NAME.
    def visitFILE_NAME(self, ctx:TSqlParser.FILE_NAMEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#FILEGROUP_ID.
    def visitFILEGROUP_ID(self, ctx:TSqlParser.FILEGROUP_IDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#FILEGROUP_NAME.
    def visitFILEGROUP_NAME(self, ctx:TSqlParser.FILEGROUP_NAMEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#FILEGROUPPROPERTY.
    def visitFILEGROUPPROPERTY(self, ctx:TSqlParser.FILEGROUPPROPERTYContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#FILEPROPERTY.
    def visitFILEPROPERTY(self, ctx:TSqlParser.FILEPROPERTYContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#FILEPROPERTYEX.
    def visitFILEPROPERTYEX(self, ctx:TSqlParser.FILEPROPERTYEXContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#FULLTEXTCATALOGPROPERTY.
    def visitFULLTEXTCATALOGPROPERTY(self, ctx:TSqlParser.FULLTEXTCATALOGPROPERTYContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#FULLTEXTSERVICEPROPERTY.
    def visitFULLTEXTSERVICEPROPERTY(self, ctx:TSqlParser.FULLTEXTSERVICEPROPERTYContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#INDEX_COL.
    def visitINDEX_COL(self, ctx:TSqlParser.INDEX_COLContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#INDEXKEY_PROPERTY.
    def visitINDEXKEY_PROPERTY(self, ctx:TSqlParser.INDEXKEY_PROPERTYContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#INDEXPROPERTY.
    def visitINDEXPROPERTY(self, ctx:TSqlParser.INDEXPROPERTYContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#NEXT_VALUE_FOR.
    def visitNEXT_VALUE_FOR(self, ctx:TSqlParser.NEXT_VALUE_FORContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#OBJECT_DEFINITION.
    def visitOBJECT_DEFINITION(self, ctx:TSqlParser.OBJECT_DEFINITIONContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#OBJECT_ID.
    def visitOBJECT_ID(self, ctx:TSqlParser.OBJECT_IDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#OBJECT_NAME.
    def visitOBJECT_NAME(self, ctx:TSqlParser.OBJECT_NAMEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#OBJECT_SCHEMA_NAME.
    def visitOBJECT_SCHEMA_NAME(self, ctx:TSqlParser.OBJECT_SCHEMA_NAMEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#OBJECTPROPERTY.
    def visitOBJECTPROPERTY(self, ctx:TSqlParser.OBJECTPROPERTYContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#OBJECTPROPERTYEX.
    def visitOBJECTPROPERTYEX(self, ctx:TSqlParser.OBJECTPROPERTYEXContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#ORIGINAL_DB_NAME.
    def visitORIGINAL_DB_NAME(self, ctx:TSqlParser.ORIGINAL_DB_NAMEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#PARSENAME.
    def visitPARSENAME(self, ctx:TSqlParser.PARSENAMEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#SCHEMA_ID.
    def visitSCHEMA_ID(self, ctx:TSqlParser.SCHEMA_IDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#SCHEMA_NAME.
    def visitSCHEMA_NAME(self, ctx:TSqlParser.SCHEMA_NAMEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#SCOPE_IDENTITY.
    def visitSCOPE_IDENTITY(self, ctx:TSqlParser.SCOPE_IDENTITYContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#SERVERPROPERTY.
    def visitSERVERPROPERTY(self, ctx:TSqlParser.SERVERPROPERTYContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#STATS_DATE.
    def visitSTATS_DATE(self, ctx:TSqlParser.STATS_DATEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#TYPE_ID.
    def visitTYPE_ID(self, ctx:TSqlParser.TYPE_IDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#TYPE_NAME.
    def visitTYPE_NAME(self, ctx:TSqlParser.TYPE_NAMEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#TYPEPROPERTY.
    def visitTYPEPROPERTY(self, ctx:TSqlParser.TYPEPROPERTYContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#ASCII.
    def visitASCII(self, ctx:TSqlParser.ASCIIContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#CHAR.
    def visitCHAR(self, ctx:TSqlParser.CHARContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#CHARINDEX.
    def visitCHARINDEX(self, ctx:TSqlParser.CHARINDEXContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#CONCAT.
    def visitCONCAT(self, ctx:TSqlParser.CONCATContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#CONCAT_WS.
    def visitCONCAT_WS(self, ctx:TSqlParser.CONCAT_WSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#DIFFERENCE.
    def visitDIFFERENCE(self, ctx:TSqlParser.DIFFERENCEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#FORMAT.
    def visitFORMAT(self, ctx:TSqlParser.FORMATContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#LEFT.
    def visitLEFT(self, ctx:TSqlParser.LEFTContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#LEN.
    def visitLEN(self, ctx:TSqlParser.LENContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#LOWER.
    def visitLOWER(self, ctx:TSqlParser.LOWERContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#LTRIM.
    def visitLTRIM(self, ctx:TSqlParser.LTRIMContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#NCHAR.
    def visitNCHAR(self, ctx:TSqlParser.NCHARContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#PATINDEX.
    def visitPATINDEX(self, ctx:TSqlParser.PATINDEXContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#QUOTENAME.
    def visitQUOTENAME(self, ctx:TSqlParser.QUOTENAMEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#REPLACE.
    def visitREPLACE(self, ctx:TSqlParser.REPLACEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#REPLICATE.
    def visitREPLICATE(self, ctx:TSqlParser.REPLICATEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#REVERSE.
    def visitREVERSE(self, ctx:TSqlParser.REVERSEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#RIGHT.
    def visitRIGHT(self, ctx:TSqlParser.RIGHTContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#RTRIM.
    def visitRTRIM(self, ctx:TSqlParser.RTRIMContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#SOUNDEX.
    def visitSOUNDEX(self, ctx:TSqlParser.SOUNDEXContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#SPACE.
    def visitSPACE(self, ctx:TSqlParser.SPACEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#STR.
    def visitSTR(self, ctx:TSqlParser.STRContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#STRINGAGG.
    def visitSTRINGAGG(self, ctx:TSqlParser.STRINGAGGContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#STRING_ESCAPE.
    def visitSTRING_ESCAPE(self, ctx:TSqlParser.STRING_ESCAPEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#STUFF.
    def visitSTUFF(self, ctx:TSqlParser.STUFFContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#SUBSTRING.
    def visitSUBSTRING(self, ctx:TSqlParser.SUBSTRINGContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#TRANSLATE.
    def visitTRANSLATE(self, ctx:TSqlParser.TRANSLATEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#TRIM.
    def visitTRIM(self, ctx:TSqlParser.TRIMContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#UNICODE.
    def visitUNICODE(self, ctx:TSqlParser.UNICODEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#UPPER.
    def visitUPPER(self, ctx:TSqlParser.UPPERContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#BINARY_CHECKSUM.
    def visitBINARY_CHECKSUM(self, ctx:TSqlParser.BINARY_CHECKSUMContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#CHECKSUM.
    def visitCHECKSUM(self, ctx:TSqlParser.CHECKSUMContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#COMPRESS.
    def visitCOMPRESS(self, ctx:TSqlParser.COMPRESSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#CONNECTIONPROPERTY.
    def visitCONNECTIONPROPERTY(self, ctx:TSqlParser.CONNECTIONPROPERTYContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#CONTEXT_INFO.
    def visitCONTEXT_INFO(self, ctx:TSqlParser.CONTEXT_INFOContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#CURRENT_REQUEST_ID.
    def visitCURRENT_REQUEST_ID(self, ctx:TSqlParser.CURRENT_REQUEST_IDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#CURRENT_TRANSACTION_ID.
    def visitCURRENT_TRANSACTION_ID(self, ctx:TSqlParser.CURRENT_TRANSACTION_IDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#DECOMPRESS.
    def visitDECOMPRESS(self, ctx:TSqlParser.DECOMPRESSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#ERROR_LINE.
    def visitERROR_LINE(self, ctx:TSqlParser.ERROR_LINEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#ERROR_MESSAGE.
    def visitERROR_MESSAGE(self, ctx:TSqlParser.ERROR_MESSAGEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#ERROR_NUMBER.
    def visitERROR_NUMBER(self, ctx:TSqlParser.ERROR_NUMBERContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#ERROR_PROCEDURE.
    def visitERROR_PROCEDURE(self, ctx:TSqlParser.ERROR_PROCEDUREContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#ERROR_SEVERITY.
    def visitERROR_SEVERITY(self, ctx:TSqlParser.ERROR_SEVERITYContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#ERROR_STATE.
    def visitERROR_STATE(self, ctx:TSqlParser.ERROR_STATEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#FORMATMESSAGE.
    def visitFORMATMESSAGE(self, ctx:TSqlParser.FORMATMESSAGEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#GET_FILESTREAM_TRANSACTION_CONTEXT.
    def visitGET_FILESTREAM_TRANSACTION_CONTEXT(self, ctx:TSqlParser.GET_FILESTREAM_TRANSACTION_CONTEXTContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#GETANSINULL.
    def visitGETANSINULL(self, ctx:TSqlParser.GETANSINULLContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#HOST_ID.
    def visitHOST_ID(self, ctx:TSqlParser.HOST_IDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#HOST_NAME.
    def visitHOST_NAME(self, ctx:TSqlParser.HOST_NAMEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#ISNULL.
    def visitISNULL(self, ctx:TSqlParser.ISNULLContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#ISNUMERIC.
    def visitISNUMERIC(self, ctx:TSqlParser.ISNUMERICContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#MIN_ACTIVE_ROWVERSION.
    def visitMIN_ACTIVE_ROWVERSION(self, ctx:TSqlParser.MIN_ACTIVE_ROWVERSIONContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#NEWID.
    def visitNEWID(self, ctx:TSqlParser.NEWIDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#NEWSEQUENTIALID.
    def visitNEWSEQUENTIALID(self, ctx:TSqlParser.NEWSEQUENTIALIDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#ROWCOUNT_BIG.
    def visitROWCOUNT_BIG(self, ctx:TSqlParser.ROWCOUNT_BIGContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#SESSION_CONTEXT.
    def visitSESSION_CONTEXT(self, ctx:TSqlParser.SESSION_CONTEXTContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#XACT_STATE.
    def visitXACT_STATE(self, ctx:TSqlParser.XACT_STATEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#CAST.
    def visitCAST(self, ctx:TSqlParser.CASTContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#TRY_CAST.
    def visitTRY_CAST(self, ctx:TSqlParser.TRY_CASTContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#CONVERT.
    def visitCONVERT(self, ctx:TSqlParser.CONVERTContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#COALESCE.
    def visitCOALESCE(self, ctx:TSqlParser.COALESCEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#CURSOR_ROWS.
    def visitCURSOR_ROWS(self, ctx:TSqlParser.CURSOR_ROWSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#FETCH_STATUS.
    def visitFETCH_STATUS(self, ctx:TSqlParser.FETCH_STATUSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#CURSOR_STATUS.
    def visitCURSOR_STATUS(self, ctx:TSqlParser.CURSOR_STATUSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#CERT_ID.
    def visitCERT_ID(self, ctx:TSqlParser.CERT_IDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#DATALENGTH.
    def visitDATALENGTH(self, ctx:TSqlParser.DATALENGTHContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#IDENT_CURRENT.
    def visitIDENT_CURRENT(self, ctx:TSqlParser.IDENT_CURRENTContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#IDENT_INCR.
    def visitIDENT_INCR(self, ctx:TSqlParser.IDENT_INCRContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#IDENT_SEED.
    def visitIDENT_SEED(self, ctx:TSqlParser.IDENT_SEEDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#IDENTITY.
    def visitIDENTITY(self, ctx:TSqlParser.IDENTITYContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#SQL_VARIANT_PROPERTY.
    def visitSQL_VARIANT_PROPERTY(self, ctx:TSqlParser.SQL_VARIANT_PROPERTYContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#CURRENT_DATE.
    def visitCURRENT_DATE(self, ctx:TSqlParser.CURRENT_DATEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#CURRENT_TIMESTAMP.
    def visitCURRENT_TIMESTAMP(self, ctx:TSqlParser.CURRENT_TIMESTAMPContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#CURRENT_TIMEZONE.
    def visitCURRENT_TIMEZONE(self, ctx:TSqlParser.CURRENT_TIMEZONEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#CURRENT_TIMEZONE_ID.
    def visitCURRENT_TIMEZONE_ID(self, ctx:TSqlParser.CURRENT_TIMEZONE_IDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#DATE_BUCKET.
    def visitDATE_BUCKET(self, ctx:TSqlParser.DATE_BUCKETContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#DATEADD.
    def visitDATEADD(self, ctx:TSqlParser.DATEADDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#DATEDIFF.
    def visitDATEDIFF(self, ctx:TSqlParser.DATEDIFFContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#DATEDIFF_BIG.
    def visitDATEDIFF_BIG(self, ctx:TSqlParser.DATEDIFF_BIGContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#DATEFROMPARTS.
    def visitDATEFROMPARTS(self, ctx:TSqlParser.DATEFROMPARTSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#DATENAME.
    def visitDATENAME(self, ctx:TSqlParser.DATENAMEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#DATEPART.
    def visitDATEPART(self, ctx:TSqlParser.DATEPARTContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#DATETIME2FROMPARTS.
    def visitDATETIME2FROMPARTS(self, ctx:TSqlParser.DATETIME2FROMPARTSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#DATETIMEFROMPARTS.
    def visitDATETIMEFROMPARTS(self, ctx:TSqlParser.DATETIMEFROMPARTSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#DATETIMEOFFSETFROMPARTS.
    def visitDATETIMEOFFSETFROMPARTS(self, ctx:TSqlParser.DATETIMEOFFSETFROMPARTSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#DATETRUNC.
    def visitDATETRUNC(self, ctx:TSqlParser.DATETRUNCContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#DAY.
    def visitDAY(self, ctx:TSqlParser.DAYContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#EOMONTH.
    def visitEOMONTH(self, ctx:TSqlParser.EOMONTHContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#GETDATE.
    def visitGETDATE(self, ctx:TSqlParser.GETDATEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#GETUTCDATE.
    def visitGETUTCDATE(self, ctx:TSqlParser.GETUTCDATEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#ISDATE.
    def visitISDATE(self, ctx:TSqlParser.ISDATEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#MONTH.
    def visitMONTH(self, ctx:TSqlParser.MONTHContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#SMALLDATETIMEFROMPARTS.
    def visitSMALLDATETIMEFROMPARTS(self, ctx:TSqlParser.SMALLDATETIMEFROMPARTSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#SWITCHOFFSET.
    def visitSWITCHOFFSET(self, ctx:TSqlParser.SWITCHOFFSETContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#SYSDATETIME.
    def visitSYSDATETIME(self, ctx:TSqlParser.SYSDATETIMEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#SYSDATETIMEOFFSET.
    def visitSYSDATETIMEOFFSET(self, ctx:TSqlParser.SYSDATETIMEOFFSETContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#SYSUTCDATETIME.
    def visitSYSUTCDATETIME(self, ctx:TSqlParser.SYSUTCDATETIMEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#TIMEFROMPARTS.
    def visitTIMEFROMPARTS(self, ctx:TSqlParser.TIMEFROMPARTSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#TODATETIMEOFFSET.
    def visitTODATETIMEOFFSET(self, ctx:TSqlParser.TODATETIMEOFFSETContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#YEAR.
    def visitYEAR(self, ctx:TSqlParser.YEARContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#NULLIF.
    def visitNULLIF(self, ctx:TSqlParser.NULLIFContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#PARSE.
    def visitPARSE(self, ctx:TSqlParser.PARSEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#XML_DATA_TYPE_FUNC.
    def visitXML_DATA_TYPE_FUNC(self, ctx:TSqlParser.XML_DATA_TYPE_FUNCContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#IIF.
    def visitIIF(self, ctx:TSqlParser.IIFContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#ISJSON.
    def visitISJSON(self, ctx:TSqlParser.ISJSONContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#JSON_OBJECT.
    def visitJSON_OBJECT(self, ctx:TSqlParser.JSON_OBJECTContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#JSON_ARRAY.
    def visitJSON_ARRAY(self, ctx:TSqlParser.JSON_ARRAYContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#JSON_VALUE.
    def visitJSON_VALUE(self, ctx:TSqlParser.JSON_VALUEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#JSON_QUERY.
    def visitJSON_QUERY(self, ctx:TSqlParser.JSON_QUERYContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#JSON_MODIFY.
    def visitJSON_MODIFY(self, ctx:TSqlParser.JSON_MODIFYContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#JSON_PATH_EXISTS.
    def visitJSON_PATH_EXISTS(self, ctx:TSqlParser.JSON_PATH_EXISTSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#ABS.
    def visitABS(self, ctx:TSqlParser.ABSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#ACOS.
    def visitACOS(self, ctx:TSqlParser.ACOSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#ASIN.
    def visitASIN(self, ctx:TSqlParser.ASINContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#ATAN.
    def visitATAN(self, ctx:TSqlParser.ATANContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#ATN2.
    def visitATN2(self, ctx:TSqlParser.ATN2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#CEILING.
    def visitCEILING(self, ctx:TSqlParser.CEILINGContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#COS.
    def visitCOS(self, ctx:TSqlParser.COSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#COT.
    def visitCOT(self, ctx:TSqlParser.COTContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#DEGREES.
    def visitDEGREES(self, ctx:TSqlParser.DEGREESContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#EXP.
    def visitEXP(self, ctx:TSqlParser.EXPContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#FLOOR.
    def visitFLOOR(self, ctx:TSqlParser.FLOORContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#LOG.
    def visitLOG(self, ctx:TSqlParser.LOGContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#LOG10.
    def visitLOG10(self, ctx:TSqlParser.LOG10Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#PI.
    def visitPI(self, ctx:TSqlParser.PIContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#POWER.
    def visitPOWER(self, ctx:TSqlParser.POWERContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#RADIANS.
    def visitRADIANS(self, ctx:TSqlParser.RADIANSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#RAND.
    def visitRAND(self, ctx:TSqlParser.RANDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#ROUND.
    def visitROUND(self, ctx:TSqlParser.ROUNDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#MATH_SIGN.
    def visitMATH_SIGN(self, ctx:TSqlParser.MATH_SIGNContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#SIN.
    def visitSIN(self, ctx:TSqlParser.SINContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#SQRT.
    def visitSQRT(self, ctx:TSqlParser.SQRTContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#SQUARE.
    def visitSQUARE(self, ctx:TSqlParser.SQUAREContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#TAN.
    def visitTAN(self, ctx:TSqlParser.TANContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#GREATEST.
    def visitGREATEST(self, ctx:TSqlParser.GREATESTContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#LEAST.
    def visitLEAST(self, ctx:TSqlParser.LEASTContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#CERTENCODED.
    def visitCERTENCODED(self, ctx:TSqlParser.CERTENCODEDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#CERTPRIVATEKEY.
    def visitCERTPRIVATEKEY(self, ctx:TSqlParser.CERTPRIVATEKEYContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#CURRENT_USER.
    def visitCURRENT_USER(self, ctx:TSqlParser.CURRENT_USERContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#DATABASE_PRINCIPAL_ID.
    def visitDATABASE_PRINCIPAL_ID(self, ctx:TSqlParser.DATABASE_PRINCIPAL_IDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#HAS_DBACCESS.
    def visitHAS_DBACCESS(self, ctx:TSqlParser.HAS_DBACCESSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#HAS_PERMS_BY_NAME.
    def visitHAS_PERMS_BY_NAME(self, ctx:TSqlParser.HAS_PERMS_BY_NAMEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#IS_MEMBER.
    def visitIS_MEMBER(self, ctx:TSqlParser.IS_MEMBERContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#IS_ROLEMEMBER.
    def visitIS_ROLEMEMBER(self, ctx:TSqlParser.IS_ROLEMEMBERContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#IS_SRVROLEMEMBER.
    def visitIS_SRVROLEMEMBER(self, ctx:TSqlParser.IS_SRVROLEMEMBERContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#LOGINPROPERTY.
    def visitLOGINPROPERTY(self, ctx:TSqlParser.LOGINPROPERTYContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#ORIGINAL_LOGIN.
    def visitORIGINAL_LOGIN(self, ctx:TSqlParser.ORIGINAL_LOGINContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#PERMISSIONS.
    def visitPERMISSIONS(self, ctx:TSqlParser.PERMISSIONSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#PWDENCRYPT.
    def visitPWDENCRYPT(self, ctx:TSqlParser.PWDENCRYPTContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#PWDCOMPARE.
    def visitPWDCOMPARE(self, ctx:TSqlParser.PWDCOMPAREContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#SESSION_USER.
    def visitSESSION_USER(self, ctx:TSqlParser.SESSION_USERContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#SESSIONPROPERTY.
    def visitSESSIONPROPERTY(self, ctx:TSqlParser.SESSIONPROPERTYContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#SUSER_ID.
    def visitSUSER_ID(self, ctx:TSqlParser.SUSER_IDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#SUSER_SNAME.
    def visitSUSER_SNAME(self, ctx:TSqlParser.SUSER_SNAMEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#SUSER_SID.
    def visitSUSER_SID(self, ctx:TSqlParser.SUSER_SIDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#SYSTEM_USER.
    def visitSYSTEM_USER(self, ctx:TSqlParser.SYSTEM_USERContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#USER.
    def visitUSER(self, ctx:TSqlParser.USERContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#USER_ID.
    def visitUSER_ID(self, ctx:TSqlParser.USER_IDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#USER_NAME.
    def visitUSER_NAME(self, ctx:TSqlParser.USER_NAMEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#xml_data_type_methods.
    def visitXml_data_type_methods(self, ctx:TSqlParser.Xml_data_type_methodsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dateparts_9.
    def visitDateparts_9(self, ctx:TSqlParser.Dateparts_9Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dateparts_12.
    def visitDateparts_12(self, ctx:TSqlParser.Dateparts_12Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dateparts_15.
    def visitDateparts_15(self, ctx:TSqlParser.Dateparts_15Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#dateparts_datetrunc.
    def visitDateparts_datetrunc(self, ctx:TSqlParser.Dateparts_datetruncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#value_method.
    def visitValue_method(self, ctx:TSqlParser.Value_methodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#value_call.
    def visitValue_call(self, ctx:TSqlParser.Value_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#query_method.
    def visitQuery_method(self, ctx:TSqlParser.Query_methodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#query_call.
    def visitQuery_call(self, ctx:TSqlParser.Query_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#exist_method.
    def visitExist_method(self, ctx:TSqlParser.Exist_methodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#exist_call.
    def visitExist_call(self, ctx:TSqlParser.Exist_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#modify_method.
    def visitModify_method(self, ctx:TSqlParser.Modify_methodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#modify_call.
    def visitModify_call(self, ctx:TSqlParser.Modify_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#hierarchyid_call.
    def visitHierarchyid_call(self, ctx:TSqlParser.Hierarchyid_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#hierarchyid_static_method.
    def visitHierarchyid_static_method(self, ctx:TSqlParser.Hierarchyid_static_methodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#nodes_method.
    def visitNodes_method(self, ctx:TSqlParser.Nodes_methodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#switch_section.
    def visitSwitch_section(self, ctx:TSqlParser.Switch_sectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#switch_search_condition_section.
    def visitSwitch_search_condition_section(self, ctx:TSqlParser.Switch_search_condition_sectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#as_column_alias.
    def visitAs_column_alias(self, ctx:TSqlParser.As_column_aliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#as_table_alias.
    def visitAs_table_alias(self, ctx:TSqlParser.As_table_aliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#table_alias.
    def visitTable_alias(self, ctx:TSqlParser.Table_aliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#with_table_hints.
    def visitWith_table_hints(self, ctx:TSqlParser.With_table_hintsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#deprecated_table_hint.
    def visitDeprecated_table_hint(self, ctx:TSqlParser.Deprecated_table_hintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#sybase_legacy_hints.
    def visitSybase_legacy_hints(self, ctx:TSqlParser.Sybase_legacy_hintsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#sybase_legacy_hint.
    def visitSybase_legacy_hint(self, ctx:TSqlParser.Sybase_legacy_hintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#table_hint.
    def visitTable_hint(self, ctx:TSqlParser.Table_hintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#index_value.
    def visitIndex_value(self, ctx:TSqlParser.Index_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#column_alias_list.
    def visitColumn_alias_list(self, ctx:TSqlParser.Column_alias_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#column_alias.
    def visitColumn_alias(self, ctx:TSqlParser.Column_aliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#table_value_constructor.
    def visitTable_value_constructor(self, ctx:TSqlParser.Table_value_constructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#expression_list_.
    def visitExpression_list_(self, ctx:TSqlParser.Expression_list_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#ranking_windowed_function.
    def visitRanking_windowed_function(self, ctx:TSqlParser.Ranking_windowed_functionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#aggregate_windowed_function.
    def visitAggregate_windowed_function(self, ctx:TSqlParser.Aggregate_windowed_functionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#analytic_windowed_function.
    def visitAnalytic_windowed_function(self, ctx:TSqlParser.Analytic_windowed_functionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#all_distinct_expression.
    def visitAll_distinct_expression(self, ctx:TSqlParser.All_distinct_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#over_clause.
    def visitOver_clause(self, ctx:TSqlParser.Over_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#row_or_range_clause.
    def visitRow_or_range_clause(self, ctx:TSqlParser.Row_or_range_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#window_frame_extent.
    def visitWindow_frame_extent(self, ctx:TSqlParser.Window_frame_extentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#window_frame_bound.
    def visitWindow_frame_bound(self, ctx:TSqlParser.Window_frame_boundContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#window_frame_preceding.
    def visitWindow_frame_preceding(self, ctx:TSqlParser.Window_frame_precedingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#window_frame_following.
    def visitWindow_frame_following(self, ctx:TSqlParser.Window_frame_followingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#create_database_option.
    def visitCreate_database_option(self, ctx:TSqlParser.Create_database_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#database_filestream_option.
    def visitDatabase_filestream_option(self, ctx:TSqlParser.Database_filestream_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#database_file_spec.
    def visitDatabase_file_spec(self, ctx:TSqlParser.Database_file_specContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#file_group.
    def visitFile_group(self, ctx:TSqlParser.File_groupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#file_spec.
    def visitFile_spec(self, ctx:TSqlParser.File_specContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#entity_name.
    def visitEntity_name(self, ctx:TSqlParser.Entity_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#entity_name_for_azure_dw.
    def visitEntity_name_for_azure_dw(self, ctx:TSqlParser.Entity_name_for_azure_dwContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#entity_name_for_parallel_dw.
    def visitEntity_name_for_parallel_dw(self, ctx:TSqlParser.Entity_name_for_parallel_dwContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#full_table_name.
    def visitFull_table_name(self, ctx:TSqlParser.Full_table_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#table_name.
    def visitTable_name(self, ctx:TSqlParser.Table_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#simple_name.
    def visitSimple_name(self, ctx:TSqlParser.Simple_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#func_proc_name_schema.
    def visitFunc_proc_name_schema(self, ctx:TSqlParser.Func_proc_name_schemaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#func_proc_name_database_schema.
    def visitFunc_proc_name_database_schema(self, ctx:TSqlParser.Func_proc_name_database_schemaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#func_proc_name_server_database_schema.
    def visitFunc_proc_name_server_database_schema(self, ctx:TSqlParser.Func_proc_name_server_database_schemaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#ddl_object.
    def visitDdl_object(self, ctx:TSqlParser.Ddl_objectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#full_column_name.
    def visitFull_column_name(self, ctx:TSqlParser.Full_column_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#column_name_list_with_order.
    def visitColumn_name_list_with_order(self, ctx:TSqlParser.Column_name_list_with_orderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#insert_column_name_list.
    def visitInsert_column_name_list(self, ctx:TSqlParser.Insert_column_name_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#insert_column_id.
    def visitInsert_column_id(self, ctx:TSqlParser.Insert_column_idContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#column_name_list.
    def visitColumn_name_list(self, ctx:TSqlParser.Column_name_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#cursor_name.
    def visitCursor_name(self, ctx:TSqlParser.Cursor_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#on_off.
    def visitOn_off(self, ctx:TSqlParser.On_offContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#clustered.
    def visitClustered(self, ctx:TSqlParser.ClusteredContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#null_notnull.
    def visitNull_notnull(self, ctx:TSqlParser.Null_notnullContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#scalar_function_name.
    def visitScalar_function_name(self, ctx:TSqlParser.Scalar_function_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#begin_conversation_timer.
    def visitBegin_conversation_timer(self, ctx:TSqlParser.Begin_conversation_timerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#begin_conversation_dialog.
    def visitBegin_conversation_dialog(self, ctx:TSqlParser.Begin_conversation_dialogContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#contract_name.
    def visitContract_name(self, ctx:TSqlParser.Contract_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#service_name.
    def visitService_name(self, ctx:TSqlParser.Service_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#end_conversation.
    def visitEnd_conversation(self, ctx:TSqlParser.End_conversationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#waitfor_conversation.
    def visitWaitfor_conversation(self, ctx:TSqlParser.Waitfor_conversationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#get_conversation.
    def visitGet_conversation(self, ctx:TSqlParser.Get_conversationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#queue_id.
    def visitQueue_id(self, ctx:TSqlParser.Queue_idContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#send_conversation.
    def visitSend_conversation(self, ctx:TSqlParser.Send_conversationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#data_type.
    def visitData_type(self, ctx:TSqlParser.Data_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#constant.
    def visitConstant(self, ctx:TSqlParser.ConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#primitive_constant.
    def visitPrimitive_constant(self, ctx:TSqlParser.Primitive_constantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#keyword.
    def visitKeyword(self, ctx:TSqlParser.KeywordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#id_.
    def visitId_(self, ctx:TSqlParser.Id_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#simple_id.
    def visitSimple_id(self, ctx:TSqlParser.Simple_idContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#id_or_string.
    def visitId_or_string(self, ctx:TSqlParser.Id_or_stringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#comparison_operator.
    def visitComparison_operator(self, ctx:TSqlParser.Comparison_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#assignment_operator.
    def visitAssignment_operator(self, ctx:TSqlParser.Assignment_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TSqlParser#file_size.
    def visitFile_size(self, ctx:TSqlParser.File_sizeContext):
        return self.visitChildren(ctx)



del TSqlParser