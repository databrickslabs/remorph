import antlr4
from antlr4.tree.Tree import TerminalNodeImpl

from databricks.labs.remorph.parsers.tsql.generated.TSqlParser import TSqlParser as tsql
from databricks.labs.remorph.parsers.tsql.generated.TSqlParserVisitor import TSqlParserVisitor
from databricks.labs.remorph.parsers.tsql.ast import *


class TSqlAST(TSqlParserVisitor):
    def _(self, ctx: antlr4.ParserRuleContext):
        if not ctx:
            return None
        if type(ctx) == list: # TODO: looks like a hack, but it's still better
            return [self.visit(_) for _ in ctx]
        return self.visit(ctx)

    def repeated(self, ctx: antlr4.ParserRuleContext, ctx_type: type) -> list[any]:
        if not ctx:
            return []
        out = []
        for rc in ctx.getTypedRuleContexts(ctx_type):
            mapped = self._(rc)
            if not mapped:
                continue
            out.append(mapped)
        return out

    def visitTerminal(self, ctx: TerminalNodeImpl):
        return ctx.getText()

    def visitTsql_file(self, ctx: tsql.Tsql_fileContext):
        batch = self.repeated(ctx, tsql.BatchContext)
        eof = self._(ctx.EOF())
        execute_body_batch = self._(ctx.execute_body_batch())
        go_statement = self.repeated(ctx, tsql.Go_statementContext)
        return TsqlFile(batch, eof, execute_body_batch, go_statement)

    def visitBatch(self, ctx: tsql.BatchContext):
        go_statement = self._(ctx.go_statement(0))
        execute_body_batch = self.repeated(ctx, tsql.Execute_body_batchContext)
        sql_clauses = self._(ctx.sql_clauses())
        right = self.repeated(ctx, tsql.Go_statementContext)
        batch_level_statement = self._(ctx.batch_level_statement())
        return Batch(go_statement, execute_body_batch, sql_clauses, right, batch_level_statement)

    def visitBatch_level_statement(self, ctx: tsql.Batch_level_statementContext):
        create_or_alter_function = self._(ctx.create_or_alter_function())
        create_or_alter_procedure = self._(ctx.create_or_alter_procedure())
        create_or_alter_trigger = self._(ctx.create_or_alter_trigger())
        create_view = self._(ctx.create_view())
        return BatchLevelStatement(create_or_alter_function, create_or_alter_procedure, create_or_alter_trigger, create_view)

    def visitSql_clauses(self, ctx: tsql.Sql_clausesContext):
        dml_clause = self._(ctx.dml_clause())
        cfl_statement = self._(ctx.cfl_statement())
        another_statement = self._(ctx.another_statement())
        ddl_clause = self._(ctx.ddl_clause())
        dbcc_clause = self._(ctx.dbcc_clause())
        backup_statement = self._(ctx.backup_statement())
        semi = self._(ctx.SEMI()) is not None
        return SqlClauses(dml_clause, cfl_statement, another_statement, ddl_clause, dbcc_clause, backup_statement, semi)

    def visitDml_clause(self, ctx: tsql.Dml_clauseContext):
        merge_statement = self._(ctx.merge_statement())
        delete_statement = self._(ctx.delete_statement())
        insert_statement = self._(ctx.insert_statement())
        select_statement_standalone = self._(ctx.select_statement_standalone())
        update_statement = self._(ctx.update_statement())
        return DmlClause(merge_statement, delete_statement, insert_statement, select_statement_standalone, update_statement)

    def visitDdl_clause(self, ctx: tsql.Ddl_clauseContext):
        alter_application_role = self._(ctx.alter_application_role())
        alter_assembly = self._(ctx.alter_assembly())
        alter_asymmetric_key = self._(ctx.alter_asymmetric_key())
        alter_authorization = self._(ctx.alter_authorization())
        alter_authorization_for_azure_dw = self._(ctx.alter_authorization_for_azure_dw())
        alter_authorization_for_parallel_dw = self._(ctx.alter_authorization_for_parallel_dw())
        alter_authorization_for_sql_database = self._(ctx.alter_authorization_for_sql_database())
        alter_availability_group = self._(ctx.alter_availability_group())
        alter_certificate = self._(ctx.alter_certificate())
        alter_column_encryption_key = self._(ctx.alter_column_encryption_key())
        alter_credential = self._(ctx.alter_credential())
        alter_cryptographic_provider = self._(ctx.alter_cryptographic_provider())
        alter_database = self._(ctx.alter_database())
        alter_database_audit_specification = self._(ctx.alter_database_audit_specification())
        alter_db_role = self._(ctx.alter_db_role())
        alter_endpoint = self._(ctx.alter_endpoint())
        alter_external_data_source = self._(ctx.alter_external_data_source())
        alter_external_library = self._(ctx.alter_external_library())
        alter_external_resource_pool = self._(ctx.alter_external_resource_pool())
        alter_fulltext_catalog = self._(ctx.alter_fulltext_catalog())
        alter_fulltext_stoplist = self._(ctx.alter_fulltext_stoplist())
        alter_index = self._(ctx.alter_index())
        alter_login_azure_sql = self._(ctx.alter_login_azure_sql())
        alter_login_azure_sql_dw_and_pdw = self._(ctx.alter_login_azure_sql_dw_and_pdw())
        alter_login_sql_server = self._(ctx.alter_login_sql_server())
        alter_master_key_azure_sql = self._(ctx.alter_master_key_azure_sql())
        alter_master_key_sql_server = self._(ctx.alter_master_key_sql_server())
        alter_message_type = self._(ctx.alter_message_type())
        alter_partition_function = self._(ctx.alter_partition_function())
        alter_partition_scheme = self._(ctx.alter_partition_scheme())
        alter_remote_service_binding = self._(ctx.alter_remote_service_binding())
        alter_resource_governor = self._(ctx.alter_resource_governor())
        alter_schema_azure_sql_dw_and_pdw = self._(ctx.alter_schema_azure_sql_dw_and_pdw())
        alter_schema_sql = self._(ctx.alter_schema_sql())
        alter_sequence = self._(ctx.alter_sequence())
        alter_server_audit = self._(ctx.alter_server_audit())
        alter_server_audit_specification = self._(ctx.alter_server_audit_specification())
        alter_server_configuration = self._(ctx.alter_server_configuration())
        alter_server_role = self._(ctx.alter_server_role())
        alter_server_role_pdw = self._(ctx.alter_server_role_pdw())
        alter_service = self._(ctx.alter_service())
        alter_service_master_key = self._(ctx.alter_service_master_key())
        alter_symmetric_key = self._(ctx.alter_symmetric_key())
        alter_table = self._(ctx.alter_table())
        alter_user = self._(ctx.alter_user())
        alter_user_azure_sql = self._(ctx.alter_user_azure_sql())
        alter_workload_group = self._(ctx.alter_workload_group())
        alter_xml_schema_collection = self._(ctx.alter_xml_schema_collection())
        create_application_role = self._(ctx.create_application_role())
        create_assembly = self._(ctx.create_assembly())
        create_asymmetric_key = self._(ctx.create_asymmetric_key())
        create_column_encryption_key = self._(ctx.create_column_encryption_key())
        create_column_master_key = self._(ctx.create_column_master_key())
        create_columnstore_index = self._(ctx.create_columnstore_index())
        create_credential = self._(ctx.create_credential())
        create_cryptographic_provider = self._(ctx.create_cryptographic_provider())
        create_database = self._(ctx.create_database())
        create_database_audit_specification = self._(ctx.create_database_audit_specification())
        create_db_role = self._(ctx.create_db_role())
        create_endpoint = self._(ctx.create_endpoint())
        create_event_notification = self._(ctx.create_event_notification())
        create_external_library = self._(ctx.create_external_library())
        create_external_resource_pool = self._(ctx.create_external_resource_pool())
        create_fulltext_catalog = self._(ctx.create_fulltext_catalog())
        create_fulltext_stoplist = self._(ctx.create_fulltext_stoplist())
        create_index = self._(ctx.create_index())
        create_login_azure_sql = self._(ctx.create_login_azure_sql())
        create_login_pdw = self._(ctx.create_login_pdw())
        create_login_sql_server = self._(ctx.create_login_sql_server())
        create_master_key_azure_sql = self._(ctx.create_master_key_azure_sql())
        create_master_key_sql_server = self._(ctx.create_master_key_sql_server())
        create_nonclustered_columnstore_index = self._(ctx.create_nonclustered_columnstore_index())
        create_or_alter_broker_priority = self._(ctx.create_or_alter_broker_priority())
        create_or_alter_event_session = self._(ctx.create_or_alter_event_session())
        create_partition_function = self._(ctx.create_partition_function())
        create_partition_scheme = self._(ctx.create_partition_scheme())
        create_remote_service_binding = self._(ctx.create_remote_service_binding())
        create_resource_pool = self._(ctx.create_resource_pool())
        create_route = self._(ctx.create_route())
        create_rule = self._(ctx.create_rule())
        create_schema = self._(ctx.create_schema())
        create_schema_azure_sql_dw_and_pdw = self._(ctx.create_schema_azure_sql_dw_and_pdw())
        create_search_property_list = self._(ctx.create_search_property_list())
        create_security_policy = self._(ctx.create_security_policy())
        create_sequence = self._(ctx.create_sequence())
        create_server_audit = self._(ctx.create_server_audit())
        create_server_audit_specification = self._(ctx.create_server_audit_specification())
        create_server_role = self._(ctx.create_server_role())
        create_service = self._(ctx.create_service())
        create_statistics = self._(ctx.create_statistics())
        create_synonym = self._(ctx.create_synonym())
        create_table = self._(ctx.create_table())
        create_type = self._(ctx.create_type())
        create_user = self._(ctx.create_user())
        create_user_azure_sql_dw = self._(ctx.create_user_azure_sql_dw())
        create_workload_group = self._(ctx.create_workload_group())
        create_xml_index = self._(ctx.create_xml_index())
        create_xml_schema_collection = self._(ctx.create_xml_schema_collection())
        disable_trigger = self._(ctx.disable_trigger())
        drop_aggregate = self._(ctx.drop_aggregate())
        drop_application_role = self._(ctx.drop_application_role())
        drop_assembly = self._(ctx.drop_assembly())
        drop_asymmetric_key = self._(ctx.drop_asymmetric_key())
        drop_availability_group = self._(ctx.drop_availability_group())
        drop_broker_priority = self._(ctx.drop_broker_priority())
        drop_certificate = self._(ctx.drop_certificate())
        drop_column_encryption_key = self._(ctx.drop_column_encryption_key())
        drop_column_master_key = self._(ctx.drop_column_master_key())
        drop_contract = self._(ctx.drop_contract())
        drop_credential = self._(ctx.drop_credential())
        drop_cryptograhic_provider = self._(ctx.drop_cryptograhic_provider())
        drop_database = self._(ctx.drop_database())
        drop_database_audit_specification = self._(ctx.drop_database_audit_specification())
        drop_database_scoped_credential = self._(ctx.drop_database_scoped_credential())
        drop_db_role = self._(ctx.drop_db_role())
        drop_default = self._(ctx.drop_default())
        drop_endpoint = self._(ctx.drop_endpoint())
        drop_event_notifications = self._(ctx.drop_event_notifications())
        drop_event_session = self._(ctx.drop_event_session())
        drop_external_data_source = self._(ctx.drop_external_data_source())
        drop_external_file_format = self._(ctx.drop_external_file_format())
        drop_external_library = self._(ctx.drop_external_library())
        drop_external_resource_pool = self._(ctx.drop_external_resource_pool())
        drop_external_table = self._(ctx.drop_external_table())
        drop_fulltext_catalog = self._(ctx.drop_fulltext_catalog())
        drop_fulltext_index = self._(ctx.drop_fulltext_index())
        drop_fulltext_stoplist = self._(ctx.drop_fulltext_stoplist())
        drop_function = self._(ctx.drop_function())
        drop_index = self._(ctx.drop_index())
        drop_login = self._(ctx.drop_login())
        drop_message_type = self._(ctx.drop_message_type())
        drop_partition_function = self._(ctx.drop_partition_function())
        drop_partition_scheme = self._(ctx.drop_partition_scheme())
        drop_procedure = self._(ctx.drop_procedure())
        drop_queue = self._(ctx.drop_queue())
        drop_remote_service_binding = self._(ctx.drop_remote_service_binding())
        drop_resource_pool = self._(ctx.drop_resource_pool())
        drop_route = self._(ctx.drop_route())
        drop_rule = self._(ctx.drop_rule())
        drop_schema = self._(ctx.drop_schema())
        drop_search_property_list = self._(ctx.drop_search_property_list())
        drop_security_policy = self._(ctx.drop_security_policy())
        drop_sequence = self._(ctx.drop_sequence())
        drop_server_audit = self._(ctx.drop_server_audit())
        drop_server_audit_specification = self._(ctx.drop_server_audit_specification())
        drop_server_role = self._(ctx.drop_server_role())
        drop_service = self._(ctx.drop_service())
        drop_signature = self._(ctx.drop_signature())
        drop_statistics = self._(ctx.drop_statistics())
        drop_statistics_name_azure_dw_and_pdw = self._(ctx.drop_statistics_name_azure_dw_and_pdw())
        drop_symmetric_key = self._(ctx.drop_symmetric_key())
        drop_synonym = self._(ctx.drop_synonym())
        drop_table = self._(ctx.drop_table())
        drop_trigger = self._(ctx.drop_trigger())
        drop_type = self._(ctx.drop_type())
        drop_user = self._(ctx.drop_user())
        drop_view = self._(ctx.drop_view())
        drop_workload_group = self._(ctx.drop_workload_group())
        drop_xml_schema_collection = self._(ctx.drop_xml_schema_collection())
        enable_trigger = self._(ctx.enable_trigger())
        lock_table = self._(ctx.lock_table())
        truncate_table = self._(ctx.truncate_table())
        update_statistics = self._(ctx.update_statistics())
        return DdlClause(alter_application_role, alter_assembly, alter_asymmetric_key, alter_authorization, alter_authorization_for_azure_dw, alter_authorization_for_parallel_dw, alter_authorization_for_sql_database, alter_availability_group, alter_certificate, alter_column_encryption_key, alter_credential, alter_cryptographic_provider, alter_database, alter_database_audit_specification, alter_db_role, alter_endpoint, alter_external_data_source, alter_external_library, alter_external_resource_pool, alter_fulltext_catalog, alter_fulltext_stoplist, alter_index, alter_login_azure_sql, alter_login_azure_sql_dw_and_pdw, alter_login_sql_server, alter_master_key_azure_sql, alter_master_key_sql_server, alter_message_type, alter_partition_function, alter_partition_scheme, alter_remote_service_binding, alter_resource_governor, alter_schema_azure_sql_dw_and_pdw, alter_schema_sql, alter_sequence, alter_server_audit, alter_server_audit_specification, alter_server_configuration, alter_server_role, alter_server_role_pdw, alter_service, alter_service_master_key, alter_symmetric_key, alter_table, alter_user, alter_user_azure_sql, alter_workload_group, alter_xml_schema_collection, create_application_role, create_assembly, create_asymmetric_key, create_column_encryption_key, create_column_master_key, create_columnstore_index, create_credential, create_cryptographic_provider, create_database, create_database_audit_specification, create_db_role, create_endpoint, create_event_notification, create_external_library, create_external_resource_pool, create_fulltext_catalog, create_fulltext_stoplist, create_index, create_login_azure_sql, create_login_pdw, create_login_sql_server, create_master_key_azure_sql, create_master_key_sql_server, create_nonclustered_columnstore_index, create_or_alter_broker_priority, create_or_alter_event_session, create_partition_function, create_partition_scheme, create_remote_service_binding, create_resource_pool, create_route, create_rule, create_schema, create_schema_azure_sql_dw_and_pdw, create_search_property_list, create_security_policy, create_sequence, create_server_audit, create_server_audit_specification, create_server_role, create_service, create_statistics, create_synonym, create_table, create_type, create_user, create_user_azure_sql_dw, create_workload_group, create_xml_index, create_xml_schema_collection, disable_trigger, drop_aggregate, drop_application_role, drop_assembly, drop_asymmetric_key, drop_availability_group, drop_broker_priority, drop_certificate, drop_column_encryption_key, drop_column_master_key, drop_contract, drop_credential, drop_cryptograhic_provider, drop_database, drop_database_audit_specification, drop_database_scoped_credential, drop_db_role, drop_default, drop_endpoint, drop_event_notifications, drop_event_session, drop_external_data_source, drop_external_file_format, drop_external_library, drop_external_resource_pool, drop_external_table, drop_fulltext_catalog, drop_fulltext_index, drop_fulltext_stoplist, drop_function, drop_index, drop_login, drop_message_type, drop_partition_function, drop_partition_scheme, drop_procedure, drop_queue, drop_remote_service_binding, drop_resource_pool, drop_route, drop_rule, drop_schema, drop_search_property_list, drop_security_policy, drop_sequence, drop_server_audit, drop_server_audit_specification, drop_server_role, drop_service, drop_signature, drop_statistics, drop_statistics_name_azure_dw_and_pdw, drop_symmetric_key, drop_synonym, drop_table, drop_trigger, drop_type, drop_user, drop_view, drop_workload_group, drop_xml_schema_collection, enable_trigger, lock_table, truncate_table, update_statistics)

    def visitBackup_statement(self, ctx: tsql.Backup_statementContext):
        backup_database = self._(ctx.backup_database())
        backup_log = self._(ctx.backup_log())
        backup_certificate = self._(ctx.backup_certificate())
        backup_master_key = self._(ctx.backup_master_key())
        backup_service_master_key = self._(ctx.backup_service_master_key())
        return BackupStatement(backup_database, backup_log, backup_certificate, backup_master_key, backup_service_master_key)

    def visitCfl_statement(self, ctx: tsql.Cfl_statementContext):
        block_statement = self._(ctx.block_statement())
        goto_statement = self._(ctx.goto_statement())
        if_statement = self._(ctx.if_statement())
        print_statement = self._(ctx.print_statement())
        raiseerror_statement = self._(ctx.raiseerror_statement())
        return_statement = self._(ctx.return_statement())
        throw_statement = self._(ctx.throw_statement())
        try_catch_statement = self._(ctx.try_catch_statement())
        waitfor_statement = self._(ctx.waitfor_statement())
        while_statement = self._(ctx.while_statement())
        return CflStatement(block_statement, goto_statement, if_statement, print_statement, raiseerror_statement, return_statement, throw_statement, try_catch_statement, waitfor_statement, while_statement)

    def visitBlock_statement(self, ctx: tsql.Block_statementContext):
        sql_clauses = self.repeated(ctx, tsql.Sql_clausesContext)
        return BlockStatement(sql_clauses)

    def visitGoto_statement(self, ctx: tsql.Goto_statementContext):
        goto_ = self._(ctx.GOTO()) is not None
        id = self._(ctx.id_())
        return GotoStatement(goto_, id)

    def visitReturn_statement(self, ctx: tsql.Return_statementContext):
        expression = self.repeated(ctx, tsql.ExpressionContext)
        return ReturnStatement(expression)

    def visitIf_statement(self, ctx: tsql.If_statementContext):
        search_condition = self._(ctx.search_condition())
        left = self._(ctx.sql_clauses(0))
        else_ = self._(ctx.ELSE()) is not None
        right = self._(ctx.sql_clauses(1))
        return IfStatement(search_condition, left, else_, right)

    def visitThrow_statement(self, ctx: tsql.Throw_statementContext):
        throw_error_number = self._(ctx.throw_error_number())
        throw_message = self._(ctx.throw_message())
        throw_state = self._(ctx.throw_state())
        return ThrowStatement(throw_error_number, throw_message, throw_state)

    def visitThrow_error_number(self, ctx: tsql.Throw_error_numberContext):
        decimal = self._(ctx.DECIMAL()) is not None
        local_id = self._(ctx.LOCAL_ID())
        return ThrowErrorNumber(decimal, local_id)

    def visitThrow_message(self, ctx: tsql.Throw_messageContext):
        string = self._(ctx.STRING())
        local_id = self._(ctx.LOCAL_ID())
        return ThrowMessage(string, local_id)

    def visitThrow_state(self, ctx: tsql.Throw_stateContext):
        decimal = self._(ctx.DECIMAL()) is not None
        local_id = self._(ctx.LOCAL_ID())
        return ThrowState(decimal, local_id)

    def visitTry_catch_statement(self, ctx: tsql.Try_catch_statementContext):
        try_clauses = self._(ctx.sql_clauses())
        return TryCatchStatement(try_clauses)

    def visitWaitfor_statement(self, ctx: tsql.Waitfor_statementContext):
        receive_statement = self.repeated(ctx, tsql.Receive_statementContext)
        time = self._(ctx.time())
        expression = self.repeated(ctx, tsql.ExpressionContext)
        delay = self._(ctx.DELAY()) is not None
        time = self._(ctx.TIME()) is not None
        timeout = self._(ctx.TIMEOUT()) is not None
        return WaitforStatement(receive_statement, time, expression, delay, time, timeout)

    def visitWhile_statement(self, ctx: tsql.While_statementContext):
        search_condition = self._(ctx.search_condition())
        sql_clauses = self._(ctx.sql_clauses())
        break_ = self._(ctx.BREAK()) is not None
        continue_ = self._(ctx.CONTINUE()) is not None
        return WhileStatement(search_condition, sql_clauses, break_, continue_)

    def visitPrint_statement(self, ctx: tsql.Print_statementContext):
        expression = self._(ctx.expression())
        double_quote_id = self._(ctx.DOUBLE_QUOTE_ID())
        local_id = self.repeated(ctx, tsql.LOCAL_IDContext)
        return PrintStatement(expression, double_quote_id, local_id)

    def visitRaiseerror_statement(self, ctx: tsql.Raiseerror_statementContext):
        raiserror = self._(ctx.RAISERROR()) is not None
        raiseerror_statement_msg = self._(ctx.raiseerror_statement_msg())
        severity = self._(ctx.constant_LOCAL_ID())
        with_ = self._(ctx.WITH()) is not None
        null = self._(ctx.NULL_()) is not None
        log = self._(ctx.LOG()) is not None
        seterror = self._(ctx.SETERROR()) is not None
        nowait = self._(ctx.NOWAIT()) is not None
        decimal = self._(ctx.DECIMAL()) is not None
        raiseerror_statement_formatstring = self._(ctx.raiseerror_statement_formatstring())
        raiseerror_statement_argument = self.repeated(ctx, tsql.Raiseerror_statement_argumentContext)
        return RaiseerrorStatement(raiserror, raiseerror_statement_msg, severity, with_, null, log, seterror, nowait, decimal, raiseerror_statement_formatstring, raiseerror_statement_argument)

    def visitAnother_statement(self, ctx: tsql.Another_statementContext):
        alter_queue = self._(ctx.alter_queue())
        checkpoint_statement = self._(ctx.checkpoint_statement())
        conversation_statement = self._(ctx.conversation_statement())
        create_contract = self._(ctx.create_contract())
        create_queue = self._(ctx.create_queue())
        cursor_statement = self._(ctx.cursor_statement())
        declare_statement = self._(ctx.declare_statement())
        execute_statement = self._(ctx.execute_statement())
        kill_statement = self._(ctx.kill_statement())
        message_statement = self._(ctx.message_statement())
        reconfigure_statement = self._(ctx.reconfigure_statement())
        security_statement = self._(ctx.security_statement())
        set_statement = self._(ctx.set_statement())
        setuser_statement = self._(ctx.setuser_statement())
        shutdown_statement = self._(ctx.shutdown_statement())
        transaction_statement = self._(ctx.transaction_statement())
        use_statement = self._(ctx.use_statement())
        return AnotherStatement(alter_queue, checkpoint_statement, conversation_statement, create_contract, create_queue, cursor_statement, declare_statement, execute_statement, kill_statement, message_statement, reconfigure_statement, security_statement, set_statement, setuser_statement, shutdown_statement, transaction_statement, use_statement)

    def visitAlter_application_role(self, ctx: tsql.Alter_application_roleContext):
        appliction_role = self._(ctx.id_())
        left = self._(ctx.COMMA()) is not None
        name = self._(ctx.NAME()) is not None
        left = self._(ctx.EQUAL()) is not None
        right = self._(ctx.COMMA()) is not None
        password = self._(ctx.PASSWORD()) is not None
        right = self._(ctx.EQUAL()) is not None
        application_role_password = self._(ctx.STRING())
        third = self._(ctx.COMMA()) is not None
        default_schema = self._(ctx.DEFAULT_SCHEMA()) is not None
        third = self._(ctx.EQUAL()) is not None
        return AlterApplicationRole(appliction_role, left, name, left, right, password, right, application_role_password, third, default_schema, third)

    def visitAlter_xml_schema_collection(self, ctx: tsql.Alter_xml_schema_collectionContext):
        left = self._(ctx.id_(0))
        right = self._(ctx.id_(1))
        string = self._(ctx.STRING())
        return AlterXmlSchemaCollection(left, right, string)

    def visitCreate_application_role(self, ctx: tsql.Create_application_roleContext):
        appliction_role = self._(ctx.id_())
        left = self._(ctx.COMMA()) is not None
        password = self._(ctx.PASSWORD()) is not None
        left = self._(ctx.EQUAL()) is not None
        application_role_password = self._(ctx.STRING())
        right = self._(ctx.COMMA()) is not None
        default_schema = self._(ctx.DEFAULT_SCHEMA()) is not None
        right = self._(ctx.EQUAL()) is not None
        return CreateApplicationRole(appliction_role, left, password, left, application_role_password, right, default_schema, right)

    def visitDrop_aggregate(self, ctx: tsql.Drop_aggregateContext):
        if_ = self._(ctx.IF()) is not None
        exists = self._(ctx.EXISTS()) is not None
        schema_name = self._(ctx.id_())
        dot = self._(ctx.DOT()) is not None
        return DropAggregate(if_, exists, schema_name, dot)

    def visitDrop_application_role(self, ctx: tsql.Drop_application_roleContext):
        rolename = self._(ctx.id_())
        return DropApplicationRole(rolename)

    def visitAlter_assembly(self, ctx: tsql.Alter_assemblyContext):
        assembly_name = self._(ctx.id_())
        alter_assembly_clause = self._(ctx.alter_assembly_clause())
        return AlterAssembly(assembly_name, alter_assembly_clause)

    def visitAlter_assembly_clause(self, ctx: tsql.Alter_assembly_clauseContext):
        alter_assembly_from_clause = self.repeated(ctx, tsql.Alter_assembly_from_clauseContext)
        alter_assembly_with_clause = self.repeated(ctx, tsql.Alter_assembly_with_clauseContext)
        alter_assembly_drop_clause = self.repeated(ctx, tsql.Alter_assembly_drop_clauseContext)
        alter_assembly_add_clause = self.repeated(ctx, tsql.Alter_assembly_add_clauseContext)
        return AlterAssemblyClause(alter_assembly_from_clause, alter_assembly_with_clause, alter_assembly_drop_clause, alter_assembly_add_clause)

    def visitAlter_assembly_from_clause(self, ctx: tsql.Alter_assembly_from_clauseContext):
        client_assembly_specifier = self._(ctx.client_assembly_specifier())
        alter_assembly_file_bits = self._(ctx.alter_assembly_file_bits())
        return AlterAssemblyFromClause(client_assembly_specifier, alter_assembly_file_bits)

    def visitAlter_assembly_drop_clause(self, ctx: tsql.Alter_assembly_drop_clauseContext):
        alter_assembly_drop_multiple_files = self._(ctx.alter_assembly_drop_multiple_files())
        return AlterAssemblyDropClause(alter_assembly_drop_multiple_files)

    def visitAlter_assembly_drop_multiple_files(self, ctx: tsql.Alter_assembly_drop_multiple_filesContext):
        all = self._(ctx.ALL()) is not None
        multiple_local_files = self._(ctx.multiple_local_files())
        return AlterAssemblyDropMultipleFiles(all, multiple_local_files)

    def visitAlter_assembly_add_clause(self, ctx: tsql.Alter_assembly_add_clauseContext):
        alter_assembly_client_file_clause = self._(ctx.alter_assembly_client_file_clause())
        return AlterAssemblyAddClause(alter_assembly_client_file_clause)

    def visitAlter_assembly_client_file_clause(self, ctx: tsql.Alter_assembly_client_file_clauseContext):
        alter_assembly_file_name = self._(ctx.alter_assembly_file_name())
        id = self._(ctx.id_())
        return AlterAssemblyClientFileClause(alter_assembly_file_name, id)

    def visitAlter_assembly_file_name(self, ctx: tsql.Alter_assembly_file_nameContext):
        string = self._(ctx.STRING())
        return AlterAssemblyFileName(string)

    def visitAlter_assembly_file_bits(self, ctx: tsql.Alter_assembly_file_bitsContext):
        id = self._(ctx.id_())
        return AlterAssemblyFileBits(id)

    def visitAlter_assembly_with_clause(self, ctx: tsql.Alter_assembly_with_clauseContext):
        assembly_option = self._(ctx.assembly_option())
        return AlterAssemblyWithClause(assembly_option)

    def visitClient_assembly_specifier(self, ctx: tsql.Client_assembly_specifierContext):
        network_file_share = self._(ctx.network_file_share())
        local_file = self._(ctx.local_file())
        string = self._(ctx.STRING())
        return ClientAssemblySpecifier(network_file_share, local_file, string)

    def visitAssembly_option(self, ctx: tsql.Assembly_optionContext):
        permission_set = self._(ctx.PERMISSION_SET()) is not None
        equal = self._(ctx.EQUAL()) is not None
        safe = self._(ctx.SAFE()) is not None
        external_access = self._(ctx.EXTERNAL_ACCESS()) is not None
        unsafe = self._(ctx.UNSAFE()) is not None
        visibility = self._(ctx.VISIBILITY()) is not None
        on_off = self._(ctx.on_off())
        unchecked = self._(ctx.UNCHECKED()) is not None
        data = self._(ctx.DATA()) is not None
        assembly_option = self._(ctx.assembly_option())
        comma = self._(ctx.COMMA()) is not None
        return AssemblyOption(permission_set, equal, safe, external_access, unsafe, visibility, on_off, unchecked, data, assembly_option, comma)

    def visitNetwork_file_share(self, ctx: tsql.Network_file_shareContext):
        network_computer = self._(ctx.network_computer())
        file_path = self._(ctx.file_path())
        return NetworkFileShare(network_computer, file_path)

    def visitNetwork_computer(self, ctx: tsql.Network_computerContext):
        computer_name = self._(ctx.id_())
        return NetworkComputer(computer_name)

    def visitFile_path(self, ctx: tsql.File_pathContext):
        file_path = self._(ctx.file_path())
        id = self._(ctx.id_())
        return FilePath(file_path, id)

    def visitLocal_file(self, ctx: tsql.Local_fileContext):
        local_drive = self._(ctx.local_drive())
        file_path = self._(ctx.file_path())
        return LocalFile(local_drive, file_path)

    def visitLocal_drive(self, ctx: tsql.Local_driveContext):
        disk_drive = self._(ctx.DISK_DRIVE())
        return LocalDrive(disk_drive)

    def visitMultiple_local_files(self, ctx: tsql.Multiple_local_filesContext):
        local_file = self._(ctx.local_file())
        single_quote = self._(ctx.SINGLE_QUOTE()) is not None
        comma = self._(ctx.COMMA()) is not None
        return MultipleLocalFiles(local_file, single_quote, comma)

    def visitCreate_assembly(self, ctx: tsql.Create_assemblyContext):
        assembly_name = self._(ctx.id_())
        authorization = self._(ctx.AUTHORIZATION()) is not None
        with_ = self._(ctx.WITH()) is not None
        permission_set = self._(ctx.PERMISSION_SET()) is not None
        equal = self._(ctx.EQUAL()) is not None
        string = self._(ctx.STRING())
        binary = self._(ctx.BINARY())
        safe = self._(ctx.SAFE()) is not None
        external_access = self._(ctx.EXTERNAL_ACCESS()) is not None
        unsafe = self._(ctx.UNSAFE()) is not None
        return CreateAssembly(assembly_name, authorization, with_, permission_set, equal, string, binary, safe, external_access, unsafe)

    def visitDrop_assembly(self, ctx: tsql.Drop_assemblyContext):
        if_ = self._(ctx.IF()) is not None
        exists = self._(ctx.EXISTS()) is not None
        assembly_name = self.repeated(ctx, tsql.Id_Context)
        with_ = self._(ctx.WITH()) is not None
        no = self._(ctx.NO()) is not None
        dependents = self._(ctx.DEPENDENTS()) is not None
        return DropAssembly(if_, exists, assembly_name, with_, no, dependents)

    def visitAlter_asymmetric_key(self, ctx: tsql.Alter_asymmetric_keyContext):
        asym_key_name = self._(ctx.id_())
        asymmetric_key_option = self._(ctx.asymmetric_key_option())
        remove = self._(ctx.REMOVE()) is not None
        private = self._(ctx.PRIVATE()) is not None
        key = self._(ctx.KEY()) is not None
        return AlterAsymmetricKey(asym_key_name, asymmetric_key_option, remove, private, key)

    def visitAsymmetric_key_option(self, ctx: tsql.Asymmetric_key_optionContext):
        left = self._(ctx.asymmetric_key_password_change_option(0))
        comma = self._(ctx.COMMA()) is not None
        right = self._(ctx.asymmetric_key_password_change_option(1))
        return AsymmetricKeyOption(left, comma, right)

    def visitAsymmetric_key_password_change_option(self, ctx: tsql.Asymmetric_key_password_change_optionContext):
        decryption = self._(ctx.DECRYPTION()) is not None
        by = self._(ctx.BY()) is not None
        password = self._(ctx.PASSWORD()) is not None
        equal = self._(ctx.EQUAL()) is not None
        string = self._(ctx.STRING())
        encryption = self._(ctx.ENCRYPTION()) is not None
        return AsymmetricKeyPasswordChangeOption(decryption, by, password, equal, string, encryption)

    def visitCreate_asymmetric_key(self, ctx: tsql.Create_asymmetric_keyContext):
        asym_key_nam = self._(ctx.id_())
        authorization = self._(ctx.AUTHORIZATION()) is not None
        from_ = self._(ctx.FROM()) is not None
        with_ = self._(ctx.WITH()) is not None
        encryption = self._(ctx.ENCRYPTION()) is not None
        by = self._(ctx.BY()) is not None
        password = self._(ctx.PASSWORD()) is not None
        left = self._(ctx.EQUAL()) is not None
        asymmetric_key_password = self._(ctx.STRING(0))
        file = self._(ctx.FILE()) is not None
        right = self._(ctx.EQUAL()) is not None
        right = self._(ctx.STRING(1))
        executable_file = self._(ctx.EXECUTABLE_FILE()) is not None
        third = self._(ctx.EQUAL()) is not None
        third = self._(ctx.STRING(2))
        assembly = self._(ctx.ASSEMBLY()) is not None
        provider = self._(ctx.PROVIDER()) is not None
        algorithm = self._(ctx.ALGORITHM()) is not None
        fourth = self._(ctx.EQUAL()) is not None
        provider_key_name = self._(ctx.PROVIDER_KEY_NAME()) is not None
        fifth = self._(ctx.EQUAL()) is not None
        provider_key_name = self._(ctx.STRING(3))
        creation_disposition = self._(ctx.CREATION_DISPOSITION()) is not None
        f_5 = self._(ctx.EQUAL()) is not None
        rsa_4096 = self._(ctx.RSA_4096()) is not None
        rsa_3072 = self._(ctx.RSA_3072()) is not None
        rsa_2048 = self._(ctx.RSA_2048()) is not None
        rsa_1024 = self._(ctx.RSA_1024()) is not None
        rsa_512 = self._(ctx.RSA_512()) is not None
        create_new = self._(ctx.CREATE_NEW()) is not None
        open_existing = self._(ctx.OPEN_EXISTING()) is not None
        return CreateAsymmetricKey(asym_key_nam, authorization, from_, with_, encryption, by, password, left, asymmetric_key_password, file, right, right, executable_file, third, third, assembly, provider, algorithm, fourth, provider_key_name, fifth, provider_key_name, creation_disposition, f_5, rsa_4096, rsa_3072, rsa_2048, rsa_1024, rsa_512, create_new, open_existing)

    def visitDrop_asymmetric_key(self, ctx: tsql.Drop_asymmetric_keyContext):
        key_name = self._(ctx.id_())
        remove = self._(ctx.REMOVE()) is not None
        provider = self._(ctx.PROVIDER()) is not None
        left = self._(ctx.KEY()) is not None
        return DropAsymmetricKey(key_name, remove, provider, left)

    def visitAlter_authorization(self, ctx: tsql.Alter_authorizationContext):
        class_type = self._(ctx.class_type())
        entity = self._(ctx.entity_name())
        authorization_grantee = self._(ctx.authorization_grantee())
        return AlterAuthorization(class_type, entity, authorization_grantee)

    def visitAuthorization_grantee(self, ctx: tsql.Authorization_granteeContext):
        principal_name = self._(ctx.id_())
        schema = self._(ctx.SCHEMA()) is not None
        owner = self._(ctx.OWNER()) is not None
        return AuthorizationGrantee(principal_name, schema, owner)

    def visitAlter_authorization_for_sql_database(self, ctx: tsql.Alter_authorization_for_sql_databaseContext):
        class_type_for_sql_database = self._(ctx.class_type_for_sql_database())
        entity = self._(ctx.entity_name())
        authorization_grantee = self._(ctx.authorization_grantee())
        return AlterAuthorizationForSqlDatabase(class_type_for_sql_database, entity, authorization_grantee)

    def visitAlter_authorization_for_azure_dw(self, ctx: tsql.Alter_authorization_for_azure_dwContext):
        class_type_for_azure_dw = self._(ctx.class_type_for_azure_dw())
        entity = self._(ctx.entity_name_for_azure_dw())
        authorization_grantee = self._(ctx.authorization_grantee())
        return AlterAuthorizationForAzureDw(class_type_for_azure_dw, entity, authorization_grantee)

    def visitAlter_authorization_for_parallel_dw(self, ctx: tsql.Alter_authorization_for_parallel_dwContext):
        class_type_for_parallel_dw = self._(ctx.class_type_for_parallel_dw())
        entity = self._(ctx.entity_name_for_parallel_dw())
        authorization_grantee = self._(ctx.authorization_grantee())
        return AlterAuthorizationForParallelDw(class_type_for_parallel_dw, entity, authorization_grantee)

    def visitClass_type(self, ctx: tsql.Class_typeContext):
        object = self._(ctx.OBJECT()) is not None
        assembly = self._(ctx.ASSEMBLY()) is not None
        asymmetric = self._(ctx.ASYMMETRIC()) is not None
        key = self._(ctx.KEY()) is not None
        availability = self._(ctx.AVAILABILITY()) is not None
        group = self._(ctx.GROUP()) is not None
        certificate = self._(ctx.CERTIFICATE()) is not None
        contract = self._(ctx.CONTRACT()) is not None
        type_ = self._(ctx.TYPE()) is not None
        database = self._(ctx.DATABASE()) is not None
        endpoint = self._(ctx.ENDPOINT()) is not None
        fulltext = self._(ctx.FULLTEXT()) is not None
        catalog = self._(ctx.CATALOG()) is not None
        stoplist = self._(ctx.STOPLIST()) is not None
        message = self._(ctx.MESSAGE()) is not None
        remote = self._(ctx.REMOTE()) is not None
        service = self._(ctx.SERVICE()) is not None
        binding = self._(ctx.BINDING()) is not None
        role = self._(ctx.ROLE()) is not None
        route = self._(ctx.ROUTE()) is not None
        schema = self._(ctx.SCHEMA()) is not None
        search = self._(ctx.SEARCH()) is not None
        property = self._(ctx.PROPERTY()) is not None
        list = self._(ctx.LIST()) is not None
        server = self._(ctx.SERVER()) is not None
        symmetric = self._(ctx.SYMMETRIC()) is not None
        xml = self._(ctx.XML()) is not None
        collection = self._(ctx.COLLECTION()) is not None
        return ClassType(object, assembly, asymmetric, key, availability, group, certificate, contract, type_, database, endpoint, fulltext, catalog, stoplist, message, remote, service, binding, role, route, schema, search, property, list, server, symmetric, xml, collection)

    def visitClass_type_for_sql_database(self, ctx: tsql.Class_type_for_sql_databaseContext):
        object = self._(ctx.OBJECT()) is not None
        assembly = self._(ctx.ASSEMBLY()) is not None
        asymmetric = self._(ctx.ASYMMETRIC()) is not None
        key = self._(ctx.KEY()) is not None
        certificate = self._(ctx.CERTIFICATE()) is not None
        type_ = self._(ctx.TYPE()) is not None
        database = self._(ctx.DATABASE()) is not None
        fulltext = self._(ctx.FULLTEXT()) is not None
        catalog = self._(ctx.CATALOG()) is not None
        stoplist = self._(ctx.STOPLIST()) is not None
        role = self._(ctx.ROLE()) is not None
        schema = self._(ctx.SCHEMA()) is not None
        search = self._(ctx.SEARCH()) is not None
        property = self._(ctx.PROPERTY()) is not None
        list = self._(ctx.LIST()) is not None
        symmetric = self._(ctx.SYMMETRIC()) is not None
        xml = self._(ctx.XML()) is not None
        collection = self._(ctx.COLLECTION()) is not None
        return ClassTypeForSqlDatabase(object, assembly, asymmetric, key, certificate, type_, database, fulltext, catalog, stoplist, role, schema, search, property, list, symmetric, xml, collection)

    def visitClass_type_for_azure_dw(self, ctx: tsql.Class_type_for_azure_dwContext):
        schema = self._(ctx.SCHEMA()) is not None
        object = self._(ctx.OBJECT()) is not None
        return ClassTypeForAzureDw(schema, object)

    def visitClass_type_for_parallel_dw(self, ctx: tsql.Class_type_for_parallel_dwContext):
        database = self._(ctx.DATABASE()) is not None
        schema = self._(ctx.SCHEMA()) is not None
        object = self._(ctx.OBJECT()) is not None
        return ClassTypeForParallelDw(database, schema, object)

    def visitClass_type_for_grant(self, ctx: tsql.Class_type_for_grantContext):
        application = self._(ctx.APPLICATION()) is not None
        role = self._(ctx.ROLE()) is not None
        assembly = self._(ctx.ASSEMBLY()) is not None
        asymmetric = self._(ctx.ASYMMETRIC()) is not None
        key = self._(ctx.KEY()) is not None
        audit = self._(ctx.AUDIT()) is not None
        availability = self._(ctx.AVAILABILITY()) is not None
        group = self._(ctx.GROUP()) is not None
        broker = self._(ctx.BROKER()) is not None
        priority = self._(ctx.PRIORITY()) is not None
        certificate = self._(ctx.CERTIFICATE()) is not None
        column = self._(ctx.COLUMN()) is not None
        encryption = self._(ctx.ENCRYPTION()) is not None
        master = self._(ctx.MASTER()) is not None
        contract = self._(ctx.CONTRACT()) is not None
        credential = self._(ctx.CREDENTIAL()) is not None
        cryptographic = self._(ctx.CRYPTOGRAPHIC()) is not None
        provider = self._(ctx.PROVIDER()) is not None
        database = self._(ctx.DATABASE()) is not None
        specification = self._(ctx.SPECIFICATION()) is not None
        event = self._(ctx.EVENT()) is not None
        session = self._(ctx.SESSION()) is not None
        scoped = self._(ctx.SCOPED()) is not None
        configuration = self._(ctx.CONFIGURATION()) is not None
        resource = self._(ctx.RESOURCE()) is not None
        governor = self._(ctx.GOVERNOR()) is not None
        endpoint = self._(ctx.ENDPOINT()) is not None
        notification = self._(ctx.NOTIFICATION()) is not None
        object = self._(ctx.OBJECT()) is not None
        server = self._(ctx.SERVER()) is not None
        external = self._(ctx.EXTERNAL()) is not None
        data = self._(ctx.DATA()) is not None
        source = self._(ctx.SOURCE()) is not None
        file = self._(ctx.FILE()) is not None
        format = self._(ctx.FORMAT()) is not None
        library = self._(ctx.LIBRARY()) is not None
        pool = self._(ctx.POOL()) is not None
        table = self._(ctx.TABLE()) is not None
        catalog = self._(ctx.CATALOG()) is not None
        stoplist = self._(ctx.STOPLIST()) is not None
        login = self._(ctx.LOGIN()) is not None
        message = self._(ctx.MESSAGE()) is not None
        type_ = self._(ctx.TYPE()) is not None
        partition = self._(ctx.PARTITION()) is not None
        function = self._(ctx.FUNCTION()) is not None
        scheme = self._(ctx.SCHEME()) is not None
        remote = self._(ctx.REMOTE()) is not None
        service = self._(ctx.SERVICE()) is not None
        binding = self._(ctx.BINDING()) is not None
        route = self._(ctx.ROUTE()) is not None
        schema = self._(ctx.SCHEMA()) is not None
        search = self._(ctx.SEARCH()) is not None
        property = self._(ctx.PROPERTY()) is not None
        list = self._(ctx.LIST()) is not None
        sql = self._(ctx.SQL()) is not None
        symmetric = self._(ctx.SYMMETRIC()) is not None
        trigger = self._(ctx.TRIGGER()) is not None
        user = self._(ctx.USER()) is not None
        xml = self._(ctx.XML()) is not None
        collection = self._(ctx.COLLECTION()) is not None
        return ClassTypeForGrant(application, role, assembly, asymmetric, key, audit, availability, group, broker, priority, certificate, column, encryption, master, contract, credential, cryptographic, provider, database, specification, event, session, scoped, configuration, resource, governor, endpoint, notification, object, server, external, data, source, file, format, library, pool, table, catalog, stoplist, login, message, type_, partition, function, scheme, remote, service, binding, route, schema, search, property, list, sql, symmetric, trigger, user, xml, collection)

    def visitDrop_availability_group(self, ctx: tsql.Drop_availability_groupContext):
        group_name = self._(ctx.id_())
        return DropAvailabilityGroup(group_name)

    def visitAlter_availability_group(self, ctx: tsql.Alter_availability_groupContext):
        alter_availability_group_start = self._(ctx.alter_availability_group_start())
        alter_availability_group_options = self._(ctx.alter_availability_group_options())
        return AlterAvailabilityGroup(alter_availability_group_start, alter_availability_group_options)

    def visitAlter_availability_group_start(self, ctx: tsql.Alter_availability_group_startContext):
        group_name = self._(ctx.id_())
        return AlterAvailabilityGroupStart(group_name)

    def visitAlter_availability_group_options(self, ctx: tsql.Alter_availability_group_optionsContext):
        set = self._(ctx.SET()) is not None
        lr_bracket = self._(ctx.LR_BRACKET()) is not None
        rr_bracket = self._(ctx.RR_BRACKET()) is not None
        automated_backup_preference = self._(ctx.AUTOMATED_BACKUP_PREFERENCE()) is not None
        left = self._(ctx.EQUAL()) is not None
        failure_condition_level = self._(ctx.FAILURE_CONDITION_LEVEL()) is not None
        right = self._(ctx.EQUAL()) is not None
        left = self._(ctx.DECIMAL()) is not None
        health_check_timeout = self._(ctx.HEALTH_CHECK_TIMEOUT()) is not None
        third = self._(ctx.EQUAL()) is not None
        milliseconds = self._(ctx.DECIMAL()) is not None
        db_failover = self._(ctx.DB_FAILOVER()) is not None
        fourth = self._(ctx.EQUAL()) is not None
        required_synchronized_secondaries_to_commit = self._(ctx.REQUIRED_SYNCHRONIZED_SECONDARIES_TO_COMMIT()) is not None
        fifth = self._(ctx.EQUAL()) is not None
        third = self._(ctx.DECIMAL()) is not None
        primary = self._(ctx.PRIMARY()) is not None
        secondary_only = self._(ctx.SECONDARY_ONLY()) is not None
        secondary = self._(ctx.SECONDARY()) is not None
        none = self._(ctx.NONE()) is not None
        on = self._(ctx.ON()) is not None
        off = self._(ctx.OFF()) is not None
        add = self._(ctx.ADD()) is not None
        database = self._(ctx.DATABASE()) is not None
        database_name = self._(ctx.id_())
        remove = self._(ctx.REMOVE()) is not None
        replica = self._(ctx.REPLICA()) is not None
        server_instance = self._(ctx.STRING(0))
        with_ = self._(ctx.WITH()) is not None
        endpoint_url = self._(ctx.ENDPOINT_URL()) is not None
        left = self._(ctx.COMMA()) is not None
        availability_mode = self._(ctx.AVAILABILITY_MODE()) is not None
        right = self._(ctx.COMMA()) is not None
        failover_mode = self._(ctx.FAILOVER_MODE()) is not None
        third = self._(ctx.COMMA()) is not None
        seeding_mode = self._(ctx.SEEDING_MODE()) is not None
        fourth = self._(ctx.COMMA()) is not None
        backup_priority = self._(ctx.BACKUP_PRIORITY()) is not None
        fifth = self._(ctx.COMMA()) is not None
        primary_role = self._(ctx.PRIMARY_ROLE()) is not None
        right = self._(ctx.LR_BRACKET()) is not None
        left = self._(ctx.ALLOW_CONNECTIONS()) is not None
        f_5 = self._(ctx.EQUAL()) is not None
        right = self._(ctx.RR_BRACKET()) is not None
        f_5 = self._(ctx.COMMA()) is not None
        secondary_role = self._(ctx.SECONDARY_ROLE()) is not None
        third = self._(ctx.LR_BRACKET()) is not None
        right = self._(ctx.ALLOW_CONNECTIONS()) is not None
        f_6 = self._(ctx.EQUAL()) is not None
        third = self._(ctx.RR_BRACKET()) is not None
        synchronous_commit = self._(ctx.SYNCHRONOUS_COMMIT()) is not None
        asynchronous_commit = self._(ctx.ASYNCHRONOUS_COMMIT()) is not None
        left = self._(ctx.AUTOMATIC()) is not None
        left = self._(ctx.MANUAL()) is not None
        right = self._(ctx.AUTOMATIC()) is not None
        right = self._(ctx.MANUAL()) is not None
        read_write = self._(ctx.READ_WRITE()) is not None
        all = self._(ctx.ALL()) is not None
        read_only = self._(ctx.READ_ONLY()) is not None
        read_only_routing_list = self._(ctx.READ_ONLY_ROUTING_LIST()) is not None
        no = self._(ctx.NO()) is not None
        session_timeout = self._(ctx.SESSION_TIMEOUT()) is not None
        modify = self._(ctx.MODIFY()) is not None
        right = self._(ctx.STRING(1))
        f_7 = self._(ctx.EQUAL()) is not None
        right = self._(ctx.READ_ONLY_ROUTING_LIST()) is not None
        f_8 = self._(ctx.EQUAL()) is not None
        f_9 = self._(ctx.EQUAL()) is not None
        fourth = self._(ctx.LR_BRACKET()) is not None
        right = self._(ctx.NO()) is not None
        right = self._(ctx.READ_ONLY()) is not None
        right = self._(ctx.ALL()) is not None
        fifth = self._(ctx.LR_BRACKET()) is not None
        third = self._(ctx.STRING(2))
        fourth = self.repeated(ctx, tsql.STRINGContext)
        join = self._(ctx.JOIN()) is not None
        availability = self._(ctx.AVAILABILITY()) is not None
        group = self._(ctx.GROUP()) is not None
        listener_url = self._(ctx.LISTENER_URL()) is not None
        grant = self._(ctx.GRANT()) is not None
        create = self._(ctx.CREATE()) is not None
        any = self._(ctx.ANY()) is not None
        deny = self._(ctx.DENY()) is not None
        failover = self._(ctx.FAILOVER()) is not None
        force_failover_allow_data_loss = self._(ctx.FORCE_FAILOVER_ALLOW_DATA_LOSS()) is not None
        listener = self._(ctx.LISTENER()) is not None
        dhcp = self._(ctx.DHCP()) is not None
        right = self._(ctx.WITH()) is not None
        ip = self._(ctx.IP()) is not None
        left = self._(ctx.ip_v4_failover(0))
        right = self._(ctx.ip_v4_failover(1))
        port = self._(ctx.PORT()) is not None
        third = self._(ctx.ip_v4_failover(2))
        fourth = self._(ctx.ip_v4_failover(3))
        ip_v6_failover = self._(ctx.ip_v6_failover())
        restart = self._(ctx.RESTART()) is not None
        offline = self._(ctx.OFFLINE()) is not None
        dtc_support = self._(ctx.DTC_SUPPORT()) is not None
        per_db = self._(ctx.PER_DB()) is not None
        return AlterAvailabilityGroupOptions(set, lr_bracket, rr_bracket, automated_backup_preference, left, failure_condition_level, right, left, health_check_timeout, third, milliseconds, db_failover, fourth, required_synchronized_secondaries_to_commit, fifth, third, primary, secondary_only, secondary, none, on, off, add, database, database_name, remove, replica, server_instance, with_, endpoint_url, left, availability_mode, right, failover_mode, third, seeding_mode, fourth, backup_priority, fifth, primary_role, right, left, f_5, right, f_5, secondary_role, third, right, f_6, third, synchronous_commit, asynchronous_commit, left, left, right, right, read_write, all, read_only, read_only_routing_list, no, session_timeout, modify, right, f_7, right, f_8, f_9, fourth, right, right, right, fifth, third, fourth, join, availability, group, listener_url, grant, create, any, deny, failover, force_failover_allow_data_loss, listener, dhcp, right, ip, left, right, port, third, fourth, ip_v6_failover, restart, offline, dtc_support, per_db)

    def visitIp_v4_failover(self, ctx: tsql.Ip_v4_failoverContext):
        string = self._(ctx.STRING())
        return IpV4Failover(string)

    def visitIp_v6_failover(self, ctx: tsql.Ip_v6_failoverContext):
        string = self._(ctx.STRING())
        return IpV6Failover(string)

    def visitCreate_or_alter_broker_priority(self, ctx: tsql.Create_or_alter_broker_priorityContext):
        create = self._(ctx.CREATE()) is not None
        alter = self._(ctx.ALTER()) is not None
        conversation_priority_name = self._(ctx.id_(0))
        contract_name = self._(ctx.CONTRACT_NAME()) is not None
        left = self._(ctx.EQUAL()) is not None
        left = self._(ctx.COMMA()) is not None
        local_service_name = self._(ctx.LOCAL_SERVICE_NAME()) is not None
        right = self._(ctx.EQUAL()) is not None
        right = self._(ctx.COMMA()) is not None
        remote_service_name = self._(ctx.REMOTE_SERVICE_NAME()) is not None
        third = self._(ctx.EQUAL()) is not None
        third = self._(ctx.COMMA()) is not None
        priority_level = self._(ctx.PRIORITY_LEVEL()) is not None
        fourth = self._(ctx.EQUAL()) is not None
        left = self._(ctx.ANY()) is not None
        double_forward_slash = self._(ctx.DOUBLE_FORWARD_SLASH()) is not None
        right = self._(ctx.id_(1))
        right = self._(ctx.ANY()) is not None
        remote_service_name = self._(ctx.STRING())
        third = self._(ctx.ANY()) is not None
        priority_value = self._(ctx.DECIMAL()) is not None
        default_ = self._(ctx.DEFAULT()) is not None
        third = self._(ctx.id_(2))
        return CreateOrAlterBrokerPriority(create, alter, conversation_priority_name, contract_name, left, left, local_service_name, right, right, remote_service_name, third, third, priority_level, fourth, left, double_forward_slash, right, right, remote_service_name, third, priority_value, default_, third)

    def visitDrop_broker_priority(self, ctx: tsql.Drop_broker_priorityContext):
        conversation_priority_name = self._(ctx.id_())
        return DropBrokerPriority(conversation_priority_name)

    def visitAlter_certificate(self, ctx: tsql.Alter_certificateContext):
        certificate_name = self._(ctx.id_())
        remove = self._(ctx.REMOVE()) is not None
        private_key = self._(ctx.PRIVATE_KEY()) is not None
        left = self._(ctx.WITH()) is not None
        private = self._(ctx.PRIVATE()) is not None
        key = self._(ctx.KEY()) is not None
        lr_bracket = self._(ctx.LR_BRACKET()) is not None
        rr_bracket = self._(ctx.RR_BRACKET()) is not None
        right = self._(ctx.WITH()) is not None
        active = self._(ctx.ACTIVE()) is not None
        for_ = self._(ctx.FOR()) is not None
        begin_dialog = self._(ctx.BEGIN_DIALOG()) is not None
        left = self._(ctx.EQUAL()) is not None
        left = self.repeated(ctx, tsql.STRINGContext)
        right = self.repeated(ctx, tsql.STRINGContext)
        third = self.repeated(ctx, tsql.STRINGContext)
        on = self._(ctx.ON()) is not None
        off = self._(ctx.OFF()) is not None
        return AlterCertificate(certificate_name, remove, private_key, left, private, key, lr_bracket, rr_bracket, right, active, for_, begin_dialog, left, left, right, third, on, off)

    def visitAlter_column_encryption_key(self, ctx: tsql.Alter_column_encryption_keyContext):
        column_encryption_key = self._(ctx.id_())
        add = self._(ctx.ADD()) is not None
        drop = self._(ctx.DROP()) is not None
        left = self._(ctx.COMMA()) is not None
        algorithm = self._(ctx.ALGORITHM()) is not None
        left = self._(ctx.EQUAL()) is not None
        algorithm_name = self._(ctx.STRING())
        right = self._(ctx.COMMA()) is not None
        encrypted_value = self._(ctx.ENCRYPTED_VALUE()) is not None
        right = self._(ctx.EQUAL()) is not None
        binary = self._(ctx.BINARY())
        return AlterColumnEncryptionKey(column_encryption_key, add, drop, left, algorithm, left, algorithm_name, right, encrypted_value, right, binary)

    def visitCreate_column_encryption_key(self, ctx: tsql.Create_column_encryption_keyContext):
        column_encryption_key = self._(ctx.id_())
        algorithm_name = self.repeated(ctx, tsql.STRINGContext)
        encrypted_value = self.repeated(ctx, tsql.BINARYContext)
        return CreateColumnEncryptionKey(column_encryption_key, algorithm_name, encrypted_value)

    def visitDrop_certificate(self, ctx: tsql.Drop_certificateContext):
        certificate_name = self._(ctx.id_())
        return DropCertificate(certificate_name)

    def visitDrop_column_encryption_key(self, ctx: tsql.Drop_column_encryption_keyContext):
        key_name = self._(ctx.id_())
        return DropColumnEncryptionKey(key_name)

    def visitDrop_column_master_key(self, ctx: tsql.Drop_column_master_keyContext):
        key_name = self._(ctx.id_())
        return DropColumnMasterKey(key_name)

    def visitDrop_contract(self, ctx: tsql.Drop_contractContext):
        dropped_contract_name = self._(ctx.id_())
        return DropContract(dropped_contract_name)

    def visitDrop_credential(self, ctx: tsql.Drop_credentialContext):
        credential_name = self._(ctx.id_())
        return DropCredential(credential_name)

    def visitDrop_cryptograhic_provider(self, ctx: tsql.Drop_cryptograhic_providerContext):
        provider_name = self._(ctx.id_())
        return DropCryptograhicProvider(provider_name)

    def visitDrop_database(self, ctx: tsql.Drop_databaseContext):
        if_ = self._(ctx.IF()) is not None
        exists = self._(ctx.EXISTS()) is not None
        database_name_or_database_snapshot_name = self.repeated(ctx, tsql.Id_Context)
        return DropDatabase(if_, exists, database_name_or_database_snapshot_name)

    def visitDrop_database_audit_specification(self, ctx: tsql.Drop_database_audit_specificationContext):
        audit_specification_name = self._(ctx.id_())
        return DropDatabaseAuditSpecification(audit_specification_name)

    def visitDrop_database_scoped_credential(self, ctx: tsql.Drop_database_scoped_credentialContext):
        credential_name = self._(ctx.id_())
        return DropDatabaseScopedCredential(credential_name)

    def visitDrop_default(self, ctx: tsql.Drop_defaultContext):
        if_ = self._(ctx.IF()) is not None
        exists = self._(ctx.EXISTS()) is not None
        comma = self._(ctx.COMMA()) is not None
        default_name = self._(ctx.id_())
        dot = self._(ctx.DOT()) is not None
        return DropDefault(if_, exists, comma, default_name, dot)

    def visitDrop_endpoint(self, ctx: tsql.Drop_endpointContext):
        end_point_name = self._(ctx.id_())
        return DropEndpoint(end_point_name)

    def visitDrop_external_data_source(self, ctx: tsql.Drop_external_data_sourceContext):
        external_data_source_name = self._(ctx.id_())
        return DropExternalDataSource(external_data_source_name)

    def visitDrop_external_file_format(self, ctx: tsql.Drop_external_file_formatContext):
        external_file_format_name = self._(ctx.id_())
        return DropExternalFileFormat(external_file_format_name)

    def visitDrop_external_library(self, ctx: tsql.Drop_external_libraryContext):
        library_name = self._(ctx.id_())
        authorization = self._(ctx.AUTHORIZATION()) is not None
        return DropExternalLibrary(library_name, authorization)

    def visitDrop_external_resource_pool(self, ctx: tsql.Drop_external_resource_poolContext):
        pool_name = self._(ctx.id_())
        return DropExternalResourcePool(pool_name)

    def visitDrop_external_table(self, ctx: tsql.Drop_external_tableContext):
        database_name = self._(ctx.id_())
        left = self._(ctx.DOT()) is not None
        right = self._(ctx.DOT()) is not None
        return DropExternalTable(database_name, left, right)

    def visitDrop_event_notifications(self, ctx: tsql.Drop_event_notificationsContext):
        notification_name = self.repeated(ctx, tsql.Id_Context)
        server = self._(ctx.SERVER()) is not None
        database = self._(ctx.DATABASE()) is not None
        queue = self._(ctx.QUEUE()) is not None
        return DropEventNotifications(notification_name, server, database, queue)

    def visitDrop_event_session(self, ctx: tsql.Drop_event_sessionContext):
        event_session_name = self._(ctx.id_())
        return DropEventSession(event_session_name)

    def visitDrop_fulltext_catalog(self, ctx: tsql.Drop_fulltext_catalogContext):
        catalog_name = self._(ctx.id_())
        return DropFulltextCatalog(catalog_name)

    def visitDrop_fulltext_index(self, ctx: tsql.Drop_fulltext_indexContext):
        schema = self._(ctx.id_())
        dot = self._(ctx.DOT()) is not None
        return DropFulltextIndex(schema, dot)

    def visitDrop_fulltext_stoplist(self, ctx: tsql.Drop_fulltext_stoplistContext):
        stoplist_name = self._(ctx.id_())
        return DropFulltextStoplist(stoplist_name)

    def visitDrop_login(self, ctx: tsql.Drop_loginContext):
        login_name = self._(ctx.id_())
        return DropLogin(login_name)

    def visitDrop_message_type(self, ctx: tsql.Drop_message_typeContext):
        message_type_name = self._(ctx.id_())
        return DropMessageType(message_type_name)

    def visitDrop_partition_function(self, ctx: tsql.Drop_partition_functionContext):
        partition_function_name = self._(ctx.id_())
        return DropPartitionFunction(partition_function_name)

    def visitDrop_partition_scheme(self, ctx: tsql.Drop_partition_schemeContext):
        partition_scheme_name = self._(ctx.id_())
        return DropPartitionScheme(partition_scheme_name)

    def visitDrop_queue(self, ctx: tsql.Drop_queueContext):
        database_name = self._(ctx.id_())
        left = self._(ctx.DOT()) is not None
        right = self._(ctx.DOT()) is not None
        return DropQueue(database_name, left, right)

    def visitDrop_remote_service_binding(self, ctx: tsql.Drop_remote_service_bindingContext):
        binding_name = self._(ctx.id_())
        return DropRemoteServiceBinding(binding_name)

    def visitDrop_resource_pool(self, ctx: tsql.Drop_resource_poolContext):
        pool_name = self._(ctx.id_())
        return DropResourcePool(pool_name)

    def visitDrop_db_role(self, ctx: tsql.Drop_db_roleContext):
        if_ = self._(ctx.IF()) is not None
        exists = self._(ctx.EXISTS()) is not None
        role_name = self._(ctx.id_())
        return DropDbRole(if_, exists, role_name)

    def visitDrop_route(self, ctx: tsql.Drop_routeContext):
        route_name = self._(ctx.id_())
        return DropRoute(route_name)

    def visitDrop_rule(self, ctx: tsql.Drop_ruleContext):
        if_ = self._(ctx.IF()) is not None
        exists = self._(ctx.EXISTS()) is not None
        comma = self._(ctx.COMMA()) is not None
        rule_name = self._(ctx.id_())
        dot = self._(ctx.DOT()) is not None
        return DropRule(if_, exists, comma, rule_name, dot)

    def visitDrop_schema(self, ctx: tsql.Drop_schemaContext):
        if_ = self._(ctx.IF()) is not None
        exists = self._(ctx.EXISTS()) is not None
        schema_name = self._(ctx.id_())
        return DropSchema(if_, exists, schema_name)

    def visitDrop_search_property_list(self, ctx: tsql.Drop_search_property_listContext):
        property_list_name = self._(ctx.id_())
        return DropSearchPropertyList(property_list_name)

    def visitDrop_security_policy(self, ctx: tsql.Drop_security_policyContext):
        if_ = self._(ctx.IF()) is not None
        exists = self._(ctx.EXISTS()) is not None
        schema_name = self._(ctx.id_())
        dot = self._(ctx.DOT()) is not None
        return DropSecurityPolicy(if_, exists, schema_name, dot)

    def visitDrop_sequence(self, ctx: tsql.Drop_sequenceContext):
        if_ = self._(ctx.IF()) is not None
        exists = self._(ctx.EXISTS()) is not None
        comma = self._(ctx.COMMA()) is not None
        sequence_name = self._(ctx.id_())
        left = self._(ctx.DOT()) is not None
        right = self._(ctx.DOT()) is not None
        return DropSequence(if_, exists, comma, sequence_name, left, right)

    def visitDrop_server_audit(self, ctx: tsql.Drop_server_auditContext):
        audit_name = self._(ctx.id_())
        return DropServerAudit(audit_name)

    def visitDrop_server_audit_specification(self, ctx: tsql.Drop_server_audit_specificationContext):
        audit_specification_name = self._(ctx.id_())
        return DropServerAuditSpecification(audit_specification_name)

    def visitDrop_server_role(self, ctx: tsql.Drop_server_roleContext):
        role_name = self._(ctx.id_())
        return DropServerRole(role_name)

    def visitDrop_service(self, ctx: tsql.Drop_serviceContext):
        dropped_service_name = self._(ctx.id_())
        return DropService(dropped_service_name)

    def visitDrop_signature(self, ctx: tsql.Drop_signatureContext):
        counter = self._(ctx.COUNTER()) is not None
        schema_name = self._(ctx.id_())
        dot = self._(ctx.DOT()) is not None
        return DropSignature(counter, schema_name, dot)

    def visitDrop_statistics_name_azure_dw_and_pdw(self, ctx: tsql.Drop_statistics_name_azure_dw_and_pdwContext):
        schema_name = self._(ctx.id_())
        left = self._(ctx.DOT()) is not None
        return DropStatisticsNameAzureDwAndPdw(schema_name, left)

    def visitDrop_symmetric_key(self, ctx: tsql.Drop_symmetric_keyContext):
        symmetric_key_name = self._(ctx.id_())
        remove = self._(ctx.REMOVE()) is not None
        provider = self._(ctx.PROVIDER()) is not None
        left = self._(ctx.KEY()) is not None
        return DropSymmetricKey(symmetric_key_name, remove, provider, left)

    def visitDrop_synonym(self, ctx: tsql.Drop_synonymContext):
        if_ = self._(ctx.IF()) is not None
        exists = self._(ctx.EXISTS()) is not None
        schema = self._(ctx.id_())
        dot = self._(ctx.DOT()) is not None
        return DropSynonym(if_, exists, schema, dot)

    def visitDrop_user(self, ctx: tsql.Drop_userContext):
        if_ = self._(ctx.IF()) is not None
        exists = self._(ctx.EXISTS()) is not None
        user_name = self._(ctx.id_())
        return DropUser(if_, exists, user_name)

    def visitDrop_workload_group(self, ctx: tsql.Drop_workload_groupContext):
        group_name = self._(ctx.id_())
        return DropWorkloadGroup(group_name)

    def visitDrop_xml_schema_collection(self, ctx: tsql.Drop_xml_schema_collectionContext):
        relational_schema = self._(ctx.id_())
        dot = self._(ctx.DOT()) is not None
        return DropXmlSchemaCollection(relational_schema, dot)

    def visitDisable_trigger(self, ctx: tsql.Disable_triggerContext):
        left = self._(ctx.ALL()) is not None
        object_name = self._(ctx.id_())
        database = self._(ctx.DATABASE()) is not None
        right = self._(ctx.ALL()) is not None
        server = self._(ctx.SERVER()) is not None
        left = self._(ctx.DOT()) is not None
        right = self._(ctx.DOT()) is not None
        return DisableTrigger(left, object_name, database, right, server, left, right)

    def visitEnable_trigger(self, ctx: tsql.Enable_triggerContext):
        left = self._(ctx.ALL()) is not None
        object_name = self._(ctx.id_())
        database = self._(ctx.DATABASE()) is not None
        right = self._(ctx.ALL()) is not None
        server = self._(ctx.SERVER()) is not None
        left = self._(ctx.DOT()) is not None
        right = self._(ctx.DOT()) is not None
        return EnableTrigger(left, object_name, database, right, server, left, right)

    def visitLock_table(self, ctx: tsql.Lock_tableContext):
        table_name = self._(ctx.table_name())
        share = self._(ctx.SHARE()) is not None
        exclusive = self._(ctx.EXCLUSIVE()) is not None
        wait = self._(ctx.WAIT()) is not None
        seconds = self._(ctx.DECIMAL()) is not None
        nowait = self._(ctx.NOWAIT()) is not None
        return LockTable(table_name, share, exclusive, wait, seconds, nowait)

    def visitTruncate_table(self, ctx: tsql.Truncate_tableContext):
        table_name = self._(ctx.table_name())
        with_ = self._(ctx.WITH()) is not None
        left = self._(ctx.LR_BRACKET()) is not None
        partitions = self._(ctx.PARTITIONS()) is not None
        right = self._(ctx.LR_BRACKET()) is not None
        left = self._(ctx.RR_BRACKET()) is not None
        right = self._(ctx.RR_BRACKET()) is not None
        left = self._(ctx.DECIMAL()) is not None
        right = self._(ctx.DECIMAL()) is not None
        to = self._(ctx.TO()) is not None
        third = self._(ctx.DECIMAL()) is not None
        return TruncateTable(table_name, with_, left, partitions, right, left, right, left, right, to, third)

    def visitCreate_column_master_key(self, ctx: tsql.Create_column_master_keyContext):
        key_name = self._(ctx.id_())
        key_store_provider_name = self._(ctx.STRING())
        return CreateColumnMasterKey(key_name, key_store_provider_name)

    def visitAlter_credential(self, ctx: tsql.Alter_credentialContext):
        credential_name = self._(ctx.id_())
        identity_name = self._(ctx.STRING())
        comma = self._(ctx.COMMA()) is not None
        secret = self._(ctx.SECRET()) is not None
        left = self._(ctx.EQUAL()) is not None
        return AlterCredential(credential_name, identity_name, comma, secret, left)

    def visitCreate_credential(self, ctx: tsql.Create_credentialContext):
        credential_name = self._(ctx.id_())
        identity_name = self._(ctx.STRING())
        comma = self._(ctx.COMMA()) is not None
        secret = self._(ctx.SECRET()) is not None
        left = self._(ctx.EQUAL()) is not None
        for_ = self._(ctx.FOR()) is not None
        cryptographic = self._(ctx.CRYPTOGRAPHIC()) is not None
        provider = self._(ctx.PROVIDER()) is not None
        return CreateCredential(credential_name, identity_name, comma, secret, left, for_, cryptographic, provider)

    def visitAlter_cryptographic_provider(self, ctx: tsql.Alter_cryptographic_providerContext):
        provider_name = self._(ctx.id_())
        from_ = self._(ctx.FROM()) is not None
        file = self._(ctx.FILE()) is not None
        equal = self._(ctx.EQUAL()) is not None
        crypto_provider_ddl_file = self._(ctx.STRING())
        enable = self._(ctx.ENABLE()) is not None
        disable = self._(ctx.DISABLE()) is not None
        return AlterCryptographicProvider(provider_name, from_, file, equal, crypto_provider_ddl_file, enable, disable)

    def visitCreate_cryptographic_provider(self, ctx: tsql.Create_cryptographic_providerContext):
        provider_name = self._(ctx.id_())
        path_of_dll = self._(ctx.STRING())
        return CreateCryptographicProvider(provider_name, path_of_dll)

    def visitCreate_endpoint(self, ctx: tsql.Create_endpointContext):
        endpointname = self._(ctx.id_())
        authorization = self._(ctx.AUTHORIZATION()) is not None
        state = self._(ctx.STATE()) is not None
        left = self._(ctx.EQUAL()) is not None
        create_endpoint_state = self._(ctx.create_endpoint_state())
        endpoint_listener_clause = self._(ctx.endpoint_listener_clause())
        left = self._(ctx.FOR()) is not None
        tsql = self._(ctx.TSQL()) is not None
        left = self._(ctx.LR_BRACKET()) is not None
        left = self._(ctx.RR_BRACKET()) is not None
        right = self._(ctx.FOR()) is not None
        service_broker = self._(ctx.SERVICE_BROKER()) is not None
        right = self._(ctx.LR_BRACKET()) is not None
        left = self._(ctx.endpoint_authentication_clause(0))
        right = self._(ctx.RR_BRACKET()) is not None
        third = self._(ctx.FOR()) is not None
        database_mirroring = self._(ctx.DATABASE_MIRRORING()) is not None
        third = self._(ctx.LR_BRACKET()) is not None
        right = self._(ctx.endpoint_authentication_clause(1))
        left = self._(ctx.COMMA()) is not None
        role = self._(ctx.ROLE()) is not None
        right = self._(ctx.EQUAL()) is not None
        third = self._(ctx.RR_BRACKET()) is not None
        right = self._(ctx.COMMA()) is not None
        left = self._(ctx.endpoint_encryption_alogorithm_clause(0))
        third = self._(ctx.COMMA()) is not None
        message_forwarding = self._(ctx.MESSAGE_FORWARDING()) is not None
        third = self._(ctx.EQUAL()) is not None
        fourth = self._(ctx.COMMA()) is not None
        message_forward_size = self._(ctx.MESSAGE_FORWARD_SIZE()) is not None
        fourth = self._(ctx.EQUAL()) is not None
        decimal = self._(ctx.DECIMAL()) is not None
        fifth = self._(ctx.COMMA()) is not None
        right = self._(ctx.endpoint_encryption_alogorithm_clause(1))
        witness = self._(ctx.WITNESS()) is not None
        partner = self._(ctx.PARTNER()) is not None
        all = self._(ctx.ALL()) is not None
        enabled = self._(ctx.ENABLED()) is not None
        disabled = self._(ctx.DISABLED()) is not None
        return CreateEndpoint(endpointname, authorization, state, left, create_endpoint_state, endpoint_listener_clause, left, tsql, left, left, right, service_broker, right, left, right, third, database_mirroring, third, right, left, role, right, third, right, left, third, message_forwarding, third, fourth, message_forward_size, fourth, decimal, fifth, right, witness, partner, all, enabled, disabled)

    def visitEndpoint_encryption_alogorithm_clause(self, ctx: tsql.Endpoint_encryption_alogorithm_clauseContext):
        disabled = self._(ctx.DISABLED()) is not None
        supported = self._(ctx.SUPPORTED()) is not None
        required = self._(ctx.REQUIRED()) is not None
        algorithm = self._(ctx.ALGORITHM()) is not None
        left = self._(ctx.AES()) is not None
        left = self._(ctx.RC4()) is not None
        right = self._(ctx.RC4()) is not None
        right = self._(ctx.AES()) is not None
        return EndpointEncryptionAlogorithmClause(disabled, supported, required, algorithm, left, left, right, right)

    def visitEndpoint_authentication_clause(self, ctx: tsql.Endpoint_authentication_clauseContext):
        left = self._(ctx.WINDOWS()) is not None
        left = self._(ctx.CERTIFICATE()) is not None
        cert_name = self._(ctx.id_())
        right = self._(ctx.WINDOWS()) is not None
        left = self._(ctx.NTLM()) is not None
        left = self._(ctx.KERBEROS()) is not None
        left = self._(ctx.NEGOTIATE()) is not None
        right = self._(ctx.CERTIFICATE()) is not None
        right = self._(ctx.NTLM()) is not None
        right = self._(ctx.KERBEROS()) is not None
        right = self._(ctx.NEGOTIATE()) is not None
        return EndpointAuthenticationClause(left, left, cert_name, right, left, left, left, right, right, right, right)

    def visitEndpoint_listener_clause(self, ctx: tsql.Endpoint_listener_clauseContext):
        comma = self._(ctx.COMMA()) is not None
        listener_ip = self._(ctx.LISTENER_IP()) is not None
        left = self._(ctx.EQUAL()) is not None
        all = self._(ctx.ALL()) is not None
        ipv4 = self._(ctx.IPV4_ADDR())
        ipv6 = self._(ctx.STRING())
        return EndpointListenerClause(comma, listener_ip, left, all, ipv4, ipv6)

    def visitCreate_event_notification(self, ctx: tsql.Create_event_notificationContext):
        event_notification_name = self._(ctx.id_())
        server = self._(ctx.SERVER()) is not None
        database = self._(ctx.DATABASE()) is not None
        queue = self._(ctx.QUEUE()) is not None
        with_ = self._(ctx.WITH()) is not None
        fan_in = self._(ctx.FAN_IN()) is not None
        broker_service = self._(ctx.STRING())
        return CreateEventNotification(event_notification_name, server, database, queue, with_, fan_in, broker_service)

    def visitCreate_or_alter_event_session(self, ctx: tsql.Create_or_alter_event_sessionContext):
        create = self._(ctx.CREATE()) is not None
        alter = self._(ctx.ALTER()) is not None
        event_session_name = self._(ctx.id_())
        with_ = self._(ctx.WITH()) is not None
        left = self._(ctx.LR_BRACKET()) is not None
        left = self._(ctx.RR_BRACKET()) is not None
        state = self._(ctx.STATE()) is not None
        left = self._(ctx.EQUAL()) is not None
        left = self._(ctx.DOT()) is not None
        right = self._(ctx.DOT()) is not None
        left = self._(ctx.ADD()) is not None
        left = self._(ctx.TARGET()) is not None
        third = self._(ctx.DOT()) is not None
        fourth = self._(ctx.DOT()) is not None
        left = self._(ctx.COMMA()) is not None
        max_memory = self._(ctx.MAX_MEMORY()) is not None
        right = self._(ctx.EQUAL()) is not None
        max_memory = self._(ctx.DECIMAL()) is not None
        right = self._(ctx.COMMA()) is not None
        event_retention_mode = self._(ctx.EVENT_RETENTION_MODE()) is not None
        third = self._(ctx.EQUAL()) is not None
        third = self._(ctx.COMMA()) is not None
        max_dispatch_latency = self._(ctx.MAX_DISPATCH_LATENCY()) is not None
        fourth = self._(ctx.EQUAL()) is not None
        fourth = self._(ctx.COMMA()) is not None
        max_event_size = self._(ctx.MAX_EVENT_SIZE()) is not None
        fifth = self._(ctx.EQUAL()) is not None
        max_event_size = self._(ctx.DECIMAL()) is not None
        fifth = self._(ctx.COMMA()) is not None
        memory_partition_mode = self._(ctx.MEMORY_PARTITION_MODE()) is not None
        f_5 = self._(ctx.EQUAL()) is not None
        f_5 = self._(ctx.COMMA()) is not None
        track_causality = self._(ctx.TRACK_CAUSALITY()) is not None
        f_6 = self._(ctx.EQUAL()) is not None
        f_6 = self._(ctx.COMMA()) is not None
        startup_state = self._(ctx.STARTUP_STATE()) is not None
        f_7 = self._(ctx.EQUAL()) is not None
        start = self._(ctx.START()) is not None
        stop = self._(ctx.STOP()) is not None
        fifth = self._(ctx.DOT()) is not None
        left = self._(ctx.SET()) is not None
        where = self._(ctx.WHERE()) is not None
        event_session_predicate_expression = self._(ctx.event_session_predicate_expression())
        f_5 = self._(ctx.DOT()) is not None
        left = self._(ctx.KB()) is not None
        left = self._(ctx.MB()) is not None
        allow_single_event_loss = self._(ctx.ALLOW_SINGLE_EVENT_LOSS()) is not None
        allow_multiple_event_loss = self._(ctx.ALLOW_MULTIPLE_EVENT_LOSS()) is not None
        no_event_loss = self._(ctx.NO_EVENT_LOSS()) is not None
        max_dispatch_latency_seconds = self._(ctx.DECIMAL()) is not None
        seconds = self._(ctx.SECONDS()) is not None
        infinite = self._(ctx.INFINITE()) is not None
        right = self._(ctx.KB()) is not None
        right = self._(ctx.MB()) is not None
        none = self._(ctx.NONE()) is not None
        per_node = self._(ctx.PER_NODE()) is not None
        per_cpu = self._(ctx.PER_CPU()) is not None
        left = self._(ctx.ON()) is not None
        left = self._(ctx.OFF()) is not None
        right = self._(ctx.ON()) is not None
        right = self._(ctx.OFF()) is not None
        right = self._(ctx.LR_BRACKET()) is not None
        fourth = self._(ctx.DECIMAL()) is not None
        right = self._(ctx.RR_BRACKET()) is not None
        left = self._(ctx.STRING(0))
        fifth = self._(ctx.DECIMAL()) is not None
        right = self._(ctx.STRING(1))
        f_6 = self._(ctx.DOT()) is not None
        return CreateOrAlterEventSession(create, alter, event_session_name, with_, left, left, state, left, left, right, left, left, third, fourth, left, max_memory, right, max_memory, right, event_retention_mode, third, third, max_dispatch_latency, fourth, fourth, max_event_size, fifth, max_event_size, fifth, memory_partition_mode, f_5, f_5, track_causality, f_6, f_6, startup_state, f_7, start, stop, fifth, left, where, event_session_predicate_expression, f_5, left, left, allow_single_event_loss, allow_multiple_event_loss, no_event_loss, max_dispatch_latency_seconds, seconds, infinite, right, right, none, per_node, per_cpu, left, left, right, right, right, fourth, right, left, fifth, right, f_6)

    def visitEvent_session_predicate_expression(self, ctx: tsql.Event_session_predicate_expressionContext):
        and_ = self._(ctx.AND()) is not None
        or_ = self._(ctx.OR()) is not None
        event_session_predicate_factor = self._(ctx.event_session_predicate_factor())
        lr_bracket = self._(ctx.LR_BRACKET()) is not None
        event_session_predicate_expression = self._(ctx.event_session_predicate_expression())
        rr_bracket = self._(ctx.RR_BRACKET()) is not None
        return EventSessionPredicateExpression(and_, or_, event_session_predicate_factor, lr_bracket, event_session_predicate_expression, rr_bracket)

    def visitEvent_session_predicate_factor(self, ctx: tsql.Event_session_predicate_factorContext):
        event_session_predicate_leaf = self._(ctx.event_session_predicate_leaf())
        lr_bracket = self._(ctx.LR_BRACKET()) is not None
        event_session_predicate_expression = self._(ctx.event_session_predicate_expression())
        rr_bracket = self._(ctx.RR_BRACKET()) is not None
        return EventSessionPredicateFactor(event_session_predicate_leaf, lr_bracket, event_session_predicate_expression, rr_bracket)

    def visitEvent_session_predicate_leaf(self, ctx: tsql.Event_session_predicate_leafContext):
        event_field_name = self._(ctx.id_())
        left = self._(ctx.EQUAL()) is not None
        left = self._(ctx.GREATER()) is not None
        left = self._(ctx.LESS()) is not None
        right = self._(ctx.LESS()) is not None
        right = self._(ctx.EQUAL()) is not None
        decimal = self._(ctx.DECIMAL()) is not None
        string = self._(ctx.STRING())
        left = self._(ctx.DOT()) is not None
        third = self._(ctx.LESS()) is not None
        right = self._(ctx.GREATER()) is not None
        exclamation = self._(ctx.EXCLAMATION()) is not None
        third = self._(ctx.EQUAL()) is not None
        third = self._(ctx.GREATER()) is not None
        fourth = self._(ctx.EQUAL()) is not None
        right = self._(ctx.DOT()) is not None
        lr_bracket = self._(ctx.LR_BRACKET()) is not None
        comma = self._(ctx.COMMA()) is not None
        rr_bracket = self._(ctx.RR_BRACKET()) is not None
        third = self._(ctx.DOT()) is not None
        fourth = self._(ctx.DOT()) is not None
        return EventSessionPredicateLeaf(event_field_name, left, left, left, right, right, decimal, string, left, third, right, exclamation, third, third, fourth, right, lr_bracket, comma, rr_bracket, third, fourth)

    def visitAlter_external_data_source(self, ctx: tsql.Alter_external_data_sourceContext):
        alter = self._(ctx.ALTER()) is not None
        external = self._(ctx.EXTERNAL()) is not None
        data = self._(ctx.DATA()) is not None
        source = self._(ctx.SOURCE()) is not None
        data_source_name = self._(ctx.id_())
        set = self._(ctx.SET()) is not None
        location = self.repeated(ctx, tsql.STRINGContext)
        with_ = self._(ctx.WITH()) is not None
        lr_bracket = self._(ctx.LR_BRACKET()) is not None
        type_ = self._(ctx.TYPE()) is not None
        left = self._(ctx.EQUAL()) is not None
        blob_storage = self._(ctx.BLOB_STORAGE()) is not None
        left = self._(ctx.COMMA()) is not None
        location = self._(ctx.LOCATION()) is not None
        right = self._(ctx.EQUAL()) is not None
        right = self._(ctx.COMMA()) is not None
        credential = self._(ctx.CREDENTIAL()) is not None
        third = self._(ctx.EQUAL()) is not None
        rr_bracket = self._(ctx.RR_BRACKET()) is not None
        return AlterExternalDataSource(alter, external, data, source, data_source_name, set, location, with_, lr_bracket, type_, left, blob_storage, left, location, right, right, credential, third, rr_bracket)

    def visitAlter_external_library(self, ctx: tsql.Alter_external_libraryContext):
        library_name = self._(ctx.id_())
        authorization = self._(ctx.AUTHORIZATION()) is not None
        set = self._(ctx.SET()) is not None
        add = self._(ctx.ADD()) is not None
        lr_bracket = self._(ctx.LR_BRACKET()) is not None
        content = self._(ctx.CONTENT()) is not None
        left = self._(ctx.EQUAL()) is not None
        with_ = self._(ctx.WITH()) is not None
        left = self._(ctx.RR_BRACKET()) is not None
        client_library = self._(ctx.STRING())
        binary = self._(ctx.BINARY())
        none = self._(ctx.NONE()) is not None
        left = self._(ctx.COMMA()) is not None
        platform = self._(ctx.PLATFORM()) is not None
        right = self._(ctx.EQUAL()) is not None
        right = self._(ctx.RR_BRACKET()) is not None
        windows = self._(ctx.WINDOWS()) is not None
        linux = self._(ctx.LINUX()) is not None
        r = self._(ctx.R()) is not None
        python = self._(ctx.PYTHON()) is not None
        return AlterExternalLibrary(library_name, authorization, set, add, lr_bracket, content, left, with_, left, client_library, binary, none, left, platform, right, right, windows, linux, r, python)

    def visitCreate_external_library(self, ctx: tsql.Create_external_libraryContext):
        library_name = self._(ctx.id_())
        authorization = self._(ctx.AUTHORIZATION()) is not None
        left = self._(ctx.COMMA()) is not None
        lr_bracket = self._(ctx.LR_BRACKET()) is not None
        with_ = self._(ctx.WITH()) is not None
        left = self._(ctx.RR_BRACKET()) is not None
        content = self._(ctx.CONTENT()) is not None
        left = self._(ctx.EQUAL()) is not None
        client_library = self._(ctx.STRING())
        binary = self._(ctx.BINARY())
        none = self._(ctx.NONE()) is not None
        right = self._(ctx.COMMA()) is not None
        platform = self._(ctx.PLATFORM()) is not None
        right = self._(ctx.EQUAL()) is not None
        right = self._(ctx.RR_BRACKET()) is not None
        windows = self._(ctx.WINDOWS()) is not None
        linux = self._(ctx.LINUX()) is not None
        r = self._(ctx.R()) is not None
        python = self._(ctx.PYTHON()) is not None
        return CreateExternalLibrary(library_name, authorization, left, lr_bracket, with_, left, content, left, client_library, binary, none, right, platform, right, right, windows, linux, r, python)

    def visitAlter_external_resource_pool(self, ctx: tsql.Alter_external_resource_poolContext):
        pool_name = self._(ctx.id_())
        default_double_quote = self._(ctx.DEFAULT_DOUBLE_QUOTE())
        left = self._(ctx.COMMA()) is not None
        affinity = self._(ctx.AFFINITY()) is not None
        cpu = self._(ctx.CPU()) is not None
        left = self._(ctx.EQUAL()) is not None
        numanode = self._(ctx.NUMANODE()) is not None
        right = self._(ctx.EQUAL()) is not None
        right = self._(ctx.COMMA()) is not None
        max_memory_percent = self._(ctx.MAX_MEMORY_PERCENT()) is not None
        third = self._(ctx.EQUAL()) is not None
        max_memory_percent = self._(ctx.DECIMAL()) is not None
        third = self._(ctx.COMMA()) is not None
        max_processes = self._(ctx.MAX_PROCESSES()) is not None
        fourth = self._(ctx.EQUAL()) is not None
        max_processes = self._(ctx.DECIMAL()) is not None
        auto = self._(ctx.AUTO()) is not None
        return AlterExternalResourcePool(pool_name, default_double_quote, left, affinity, cpu, left, numanode, right, right, max_memory_percent, third, max_memory_percent, third, max_processes, fourth, max_processes, auto)

    def visitCreate_external_resource_pool(self, ctx: tsql.Create_external_resource_poolContext):
        pool_name = self._(ctx.id_())
        left = self._(ctx.COMMA()) is not None
        affinity = self._(ctx.AFFINITY()) is not None
        cpu = self._(ctx.CPU()) is not None
        left = self._(ctx.EQUAL()) is not None
        numanode = self._(ctx.NUMANODE()) is not None
        right = self._(ctx.EQUAL()) is not None
        right = self._(ctx.COMMA()) is not None
        max_memory_percent = self._(ctx.MAX_MEMORY_PERCENT()) is not None
        third = self._(ctx.EQUAL()) is not None
        max_memory_percent = self._(ctx.DECIMAL()) is not None
        third = self._(ctx.COMMA()) is not None
        max_processes = self._(ctx.MAX_PROCESSES()) is not None
        fourth = self._(ctx.EQUAL()) is not None
        max_processes = self._(ctx.DECIMAL()) is not None
        auto = self._(ctx.AUTO()) is not None
        return CreateExternalResourcePool(pool_name, left, affinity, cpu, left, numanode, right, right, max_memory_percent, third, max_memory_percent, third, max_processes, fourth, max_processes, auto)

    def visitAlter_fulltext_catalog(self, ctx: tsql.Alter_fulltext_catalogContext):
        catalog_name = self._(ctx.id_())
        rebuild = self._(ctx.REBUILD()) is not None
        reorganize = self._(ctx.REORGANIZE()) is not None
        as_ = self._(ctx.AS()) is not None
        default_ = self._(ctx.DEFAULT()) is not None
        with_ = self._(ctx.WITH()) is not None
        accent_sensitivity = self._(ctx.ACCENT_SENSITIVITY()) is not None
        equal = self._(ctx.EQUAL()) is not None
        on = self._(ctx.ON()) is not None
        off = self._(ctx.OFF()) is not None
        return AlterFulltextCatalog(catalog_name, rebuild, reorganize, as_, default_, with_, accent_sensitivity, equal, on, off)

    def visitCreate_fulltext_catalog(self, ctx: tsql.Create_fulltext_catalogContext):
        catalog_name = self._(ctx.id_())
        left = self._(ctx.ON()) is not None
        filegroup = self._(ctx.FILEGROUP()) is not None
        in_ = self._(ctx.IN()) is not None
        path = self._(ctx.PATH()) is not None
        rootpath = self._(ctx.STRING())
        with_ = self._(ctx.WITH()) is not None
        accent_sensitivity = self._(ctx.ACCENT_SENSITIVITY()) is not None
        equal = self._(ctx.EQUAL()) is not None
        as_ = self._(ctx.AS()) is not None
        default_ = self._(ctx.DEFAULT()) is not None
        authorization = self._(ctx.AUTHORIZATION()) is not None
        right = self._(ctx.ON()) is not None
        off = self._(ctx.OFF()) is not None
        return CreateFulltextCatalog(catalog_name, left, filegroup, in_, path, rootpath, with_, accent_sensitivity, equal, as_, default_, authorization, right, off)

    def visitAlter_fulltext_stoplist(self, ctx: tsql.Alter_fulltext_stoplistContext):
        stoplist_name = self._(ctx.id_())
        add = self._(ctx.ADD()) is not None
        stopword = self._(ctx.STRING(0))
        left = self._(ctx.LANGUAGE()) is not None
        drop = self._(ctx.DROP()) is not None
        right = self._(ctx.STRING(1))
        left = self._(ctx.DECIMAL()) is not None
        left = self._(ctx.BINARY(0))
        stopword = self._(ctx.STRING(2))
        right = self._(ctx.LANGUAGE()) is not None
        left = self._(ctx.ALL()) is not None
        right = self._(ctx.ALL()) is not None
        fourth = self._(ctx.STRING(3))
        right = self._(ctx.DECIMAL()) is not None
        right = self._(ctx.BINARY(1))
        fifth = self._(ctx.STRING(4))
        third = self._(ctx.DECIMAL()) is not None
        third = self._(ctx.BINARY(2))
        return AlterFulltextStoplist(stoplist_name, add, stopword, left, drop, right, left, left, stopword, right, left, right, fourth, right, right, fifth, third, third)

    def visitCreate_fulltext_stoplist(self, ctx: tsql.Create_fulltext_stoplistContext):
        stoplist_name = self._(ctx.id_())
        from_ = self._(ctx.FROM()) is not None
        authorization = self._(ctx.AUTHORIZATION()) is not None
        system = self._(ctx.SYSTEM()) is not None
        left = self._(ctx.STOPLIST()) is not None
        dot = self._(ctx.DOT()) is not None
        return CreateFulltextStoplist(stoplist_name, from_, authorization, system, left, dot)

    def visitAlter_login_sql_server(self, ctx: tsql.Alter_login_sql_serverContext):
        login_name = self._(ctx.id_())
        with_ = self._(ctx.WITH()) is not None
        left = self._(ctx.CREDENTIAL()) is not None
        enable = self._(ctx.ENABLE()) is not None
        disable = self._(ctx.DISABLE()) is not None
        old_password = self._(ctx.OLD_PASSWORD()) is not None
        left = self._(ctx.EQUAL()) is not None
        old_password = self._(ctx.STRING())
        default_database = self._(ctx.DEFAULT_DATABASE()) is not None
        right = self._(ctx.EQUAL()) is not None
        default_language = self._(ctx.DEFAULT_LANGUAGE()) is not None
        third = self._(ctx.EQUAL()) is not None
        name = self._(ctx.NAME()) is not None
        fourth = self._(ctx.EQUAL()) is not None
        check_policy = self._(ctx.CHECK_POLICY()) is not None
        fifth = self._(ctx.EQUAL()) is not None
        check_expiration = self._(ctx.CHECK_EXPIRATION()) is not None
        f_5 = self._(ctx.EQUAL()) is not None
        right = self._(ctx.CREDENTIAL()) is not None
        f_6 = self._(ctx.EQUAL()) is not None
        no = self._(ctx.NO()) is not None
        third = self._(ctx.CREDENTIAL()) is not None
        add = self._(ctx.ADD()) is not None
        drop = self._(ctx.DROP()) is not None
        password = self._(ctx.PASSWORD()) is not None
        f_7 = self._(ctx.EQUAL()) is not None
        left = self._(ctx.ON()) is not None
        left = self._(ctx.OFF()) is not None
        right = self._(ctx.ON()) is not None
        right = self._(ctx.OFF()) is not None
        password_hash = self._(ctx.BINARY())
        hashed = self._(ctx.HASHED()) is not None
        return AlterLoginSqlServer(login_name, with_, left, enable, disable, old_password, left, old_password, default_database, right, default_language, third, name, fourth, check_policy, fifth, check_expiration, f_5, right, f_6, no, third, add, drop, password, f_7, left, left, right, right, password_hash, hashed)

    def visitCreate_login_sql_server(self, ctx: tsql.Create_login_sql_serverContext):
        login_name = self._(ctx.id_())
        left = self._(ctx.WITH()) is not None
        left = self._(ctx.COMMA()) is not None
        sid = self._(ctx.SID()) is not None
        left = self._(ctx.EQUAL()) is not None
        sid = self._(ctx.BINARY())
        right = self._(ctx.COMMA()) is not None
        left = self._(ctx.DEFAULT_DATABASE()) is not None
        right = self._(ctx.EQUAL()) is not None
        third = self._(ctx.COMMA()) is not None
        left = self._(ctx.DEFAULT_LANGUAGE()) is not None
        third = self._(ctx.EQUAL()) is not None
        fourth = self._(ctx.COMMA()) is not None
        check_expiration = self._(ctx.CHECK_EXPIRATION()) is not None
        fourth = self._(ctx.EQUAL()) is not None
        fifth = self._(ctx.COMMA()) is not None
        check_policy = self._(ctx.CHECK_POLICY()) is not None
        fifth = self._(ctx.EQUAL()) is not None
        f_5 = self._(ctx.COMMA()) is not None
        credential = self._(ctx.CREDENTIAL()) is not None
        f_5 = self._(ctx.EQUAL()) is not None
        from_ = self._(ctx.FROM()) is not None
        password = self._(ctx.PASSWORD()) is not None
        f_6 = self._(ctx.EQUAL()) is not None
        left = self._(ctx.ON()) is not None
        left = self._(ctx.OFF()) is not None
        right = self._(ctx.ON()) is not None
        right = self._(ctx.OFF()) is not None
        windows = self._(ctx.WINDOWS()) is not None
        certificate = self._(ctx.CERTIFICATE()) is not None
        asymmetric = self._(ctx.ASYMMETRIC()) is not None
        key = self._(ctx.KEY()) is not None
        password = self._(ctx.STRING())
        hashed = self._(ctx.HASHED()) is not None
        right = self._(ctx.WITH()) is not None
        f_6 = self._(ctx.COMMA()) is not None
        right = self._(ctx.DEFAULT_DATABASE()) is not None
        f_7 = self._(ctx.EQUAL()) is not None
        f_7 = self._(ctx.COMMA()) is not None
        right = self._(ctx.DEFAULT_LANGUAGE()) is not None
        f_8 = self._(ctx.EQUAL()) is not None
        return CreateLoginSqlServer(login_name, left, left, sid, left, sid, right, left, right, third, left, third, fourth, check_expiration, fourth, fifth, check_policy, fifth, f_5, credential, f_5, from_, password, f_6, left, left, right, right, windows, certificate, asymmetric, key, password, hashed, right, f_6, right, f_7, f_7, right, f_8)

    def visitAlter_login_azure_sql(self, ctx: tsql.Alter_login_azure_sqlContext):
        login_name = self._(ctx.id_())
        with_ = self._(ctx.WITH()) is not None
        enable = self._(ctx.ENABLE()) is not None
        disable = self._(ctx.DISABLE()) is not None
        password = self._(ctx.PASSWORD()) is not None
        left = self._(ctx.EQUAL()) is not None
        password = self._(ctx.STRING())
        name = self._(ctx.NAME()) is not None
        right = self._(ctx.EQUAL()) is not None
        old_password = self._(ctx.OLD_PASSWORD()) is not None
        third = self._(ctx.EQUAL()) is not None
        return AlterLoginAzureSql(login_name, with_, enable, disable, password, left, password, name, right, old_password, third)

    def visitCreate_login_azure_sql(self, ctx: tsql.Create_login_azure_sqlContext):
        login_name = self._(ctx.id_())
        string = self._(ctx.STRING())
        sid = self._(ctx.SID()) is not None
        left = self._(ctx.EQUAL()) is not None
        sid = self._(ctx.BINARY())
        return CreateLoginAzureSql(login_name, string, sid, left, sid)

    def visitAlter_login_azure_sql_dw_and_pdw(self, ctx: tsql.Alter_login_azure_sql_dw_and_pdwContext):
        login_name = self._(ctx.id_())
        with_ = self._(ctx.WITH()) is not None
        enable = self._(ctx.ENABLE()) is not None
        disable = self._(ctx.DISABLE()) is not None
        password = self._(ctx.PASSWORD()) is not None
        left = self._(ctx.EQUAL()) is not None
        password = self._(ctx.STRING())
        name = self._(ctx.NAME()) is not None
        right = self._(ctx.EQUAL()) is not None
        old_password = self._(ctx.OLD_PASSWORD()) is not None
        third = self._(ctx.EQUAL()) is not None
        return AlterLoginAzureSqlDwAndPdw(login_name, with_, enable, disable, password, left, password, name, right, old_password, third)

    def visitCreate_login_pdw(self, ctx: tsql.Create_login_pdwContext):
        login_name = self._(ctx.id_())
        with_ = self._(ctx.WITH()) is not None
        from_ = self._(ctx.FROM()) is not None
        windows = self._(ctx.WINDOWS()) is not None
        password = self._(ctx.PASSWORD()) is not None
        left = self._(ctx.EQUAL()) is not None
        password = self._(ctx.STRING())
        must_change = self._(ctx.MUST_CHANGE()) is not None
        check_policy = self._(ctx.CHECK_POLICY()) is not None
        right = self._(ctx.EQUAL()) is not None
        on = self._(ctx.ON()) is not None
        off = self._(ctx.OFF()) is not None
        return CreateLoginPdw(login_name, with_, from_, windows, password, left, password, must_change, check_policy, right, on, off)

    def visitAlter_master_key_sql_server(self, ctx: tsql.Alter_master_key_sql_serverContext):
        regenerate = self._(ctx.REGENERATE()) is not None
        with_ = self._(ctx.WITH()) is not None
        left = self._(ctx.ENCRYPTION()) is not None
        left = self._(ctx.BY()) is not None
        left = self._(ctx.PASSWORD()) is not None
        left = self._(ctx.EQUAL()) is not None
        password = self._(ctx.STRING())
        right = self._(ctx.ENCRYPTION()) is not None
        right = self._(ctx.BY()) is not None
        force = self._(ctx.FORCE()) is not None
        add = self._(ctx.ADD()) is not None
        drop = self._(ctx.DROP()) is not None
        service = self._(ctx.SERVICE()) is not None
        left = self._(ctx.MASTER()) is not None
        left = self._(ctx.KEY()) is not None
        right = self._(ctx.PASSWORD()) is not None
        right = self._(ctx.EQUAL()) is not None
        return AlterMasterKeySqlServer(regenerate, with_, left, left, left, left, password, right, right, force, add, drop, service, left, left, right, right)

    def visitCreate_master_key_sql_server(self, ctx: tsql.Create_master_key_sql_serverContext):
        password = self._(ctx.STRING())
        return CreateMasterKeySqlServer(password)

    def visitAlter_master_key_azure_sql(self, ctx: tsql.Alter_master_key_azure_sqlContext):
        regenerate = self._(ctx.REGENERATE()) is not None
        with_ = self._(ctx.WITH()) is not None
        left = self._(ctx.ENCRYPTION()) is not None
        left = self._(ctx.BY()) is not None
        left = self._(ctx.PASSWORD()) is not None
        left = self._(ctx.EQUAL()) is not None
        password = self._(ctx.STRING())
        add = self._(ctx.ADD()) is not None
        right = self._(ctx.ENCRYPTION()) is not None
        right = self._(ctx.BY()) is not None
        drop = self._(ctx.DROP()) is not None
        third = self._(ctx.ENCRYPTION()) is not None
        third = self._(ctx.BY()) is not None
        right = self._(ctx.PASSWORD()) is not None
        right = self._(ctx.EQUAL()) is not None
        force = self._(ctx.FORCE()) is not None
        service = self._(ctx.SERVICE()) is not None
        left = self._(ctx.MASTER()) is not None
        left = self._(ctx.KEY()) is not None
        third = self._(ctx.PASSWORD()) is not None
        third = self._(ctx.EQUAL()) is not None
        return AlterMasterKeyAzureSql(regenerate, with_, left, left, left, left, password, add, right, right, drop, third, third, right, right, force, service, left, left, third, third)

    def visitCreate_master_key_azure_sql(self, ctx: tsql.Create_master_key_azure_sqlContext):
        encryption = self._(ctx.ENCRYPTION()) is not None
        by = self._(ctx.BY()) is not None
        password = self._(ctx.PASSWORD()) is not None
        equal = self._(ctx.EQUAL()) is not None
        password = self._(ctx.STRING())
        return CreateMasterKeyAzureSql(encryption, by, password, equal, password)

    def visitAlter_message_type(self, ctx: tsql.Alter_message_typeContext):
        message_type_name = self._(ctx.id_())
        none = self._(ctx.NONE()) is not None
        empty = self._(ctx.EMPTY()) is not None
        well_formed_xml = self._(ctx.WELL_FORMED_XML()) is not None
        valid_xml = self._(ctx.VALID_XML()) is not None
        with_ = self._(ctx.WITH()) is not None
        schema = self._(ctx.SCHEMA()) is not None
        collection = self._(ctx.COLLECTION()) is not None
        return AlterMessageType(message_type_name, none, empty, well_formed_xml, valid_xml, with_, schema, collection)

    def visitAlter_partition_function(self, ctx: tsql.Alter_partition_functionContext):
        partition_function_name = self._(ctx.id_())
        split = self._(ctx.SPLIT()) is not None
        merge = self._(ctx.MERGE()) is not None
        return AlterPartitionFunction(partition_function_name, split, merge)

    def visitAlter_partition_scheme(self, ctx: tsql.Alter_partition_schemeContext):
        partition_scheme_name = self._(ctx.id_())
        return AlterPartitionScheme(partition_scheme_name)

    def visitAlter_remote_service_binding(self, ctx: tsql.Alter_remote_service_bindingContext):
        binding_name = self._(ctx.id_())
        user = self._(ctx.USER()) is not None
        left = self._(ctx.EQUAL()) is not None
        comma = self._(ctx.COMMA()) is not None
        anonymous = self._(ctx.ANONYMOUS()) is not None
        right = self._(ctx.EQUAL()) is not None
        on = self._(ctx.ON()) is not None
        off = self._(ctx.OFF()) is not None
        return AlterRemoteServiceBinding(binding_name, user, left, comma, anonymous, right, on, off)

    def visitCreate_remote_service_binding(self, ctx: tsql.Create_remote_service_bindingContext):
        binding_name = self._(ctx.id_())
        authorization = self._(ctx.AUTHORIZATION()) is not None
        remote_service_name = self._(ctx.STRING())
        user = self._(ctx.USER()) is not None
        left = self._(ctx.EQUAL()) is not None
        comma = self._(ctx.COMMA()) is not None
        anonymous = self._(ctx.ANONYMOUS()) is not None
        right = self._(ctx.EQUAL()) is not None
        on = self._(ctx.ON()) is not None
        off = self._(ctx.OFF()) is not None
        return CreateRemoteServiceBinding(binding_name, authorization, remote_service_name, user, left, comma, anonymous, right, on, off)

    def visitCreate_resource_pool(self, ctx: tsql.Create_resource_poolContext):
        pool_name = self._(ctx.id_())
        with_ = self._(ctx.WITH()) is not None
        left = self._(ctx.LR_BRACKET()) is not None
        left = self._(ctx.RR_BRACKET()) is not None
        left = self._(ctx.COMMA()) is not None
        min_cpu_percent = self._(ctx.MIN_CPU_PERCENT()) is not None
        left = self._(ctx.EQUAL()) is not None
        left = self._(ctx.DECIMAL()) is not None
        right = self._(ctx.COMMA()) is not None
        max_cpu_percent = self._(ctx.MAX_CPU_PERCENT()) is not None
        right = self._(ctx.EQUAL()) is not None
        right = self._(ctx.DECIMAL()) is not None
        third = self._(ctx.COMMA()) is not None
        cap_cpu_percent = self._(ctx.CAP_CPU_PERCENT()) is not None
        third = self._(ctx.EQUAL()) is not None
        third = self._(ctx.DECIMAL()) is not None
        fourth = self._(ctx.COMMA()) is not None
        affinity = self._(ctx.AFFINITY()) is not None
        scheduler = self._(ctx.SCHEDULER()) is not None
        fourth = self._(ctx.EQUAL()) is not None
        fifth = self._(ctx.COMMA()) is not None
        min_memory_percent = self._(ctx.MIN_MEMORY_PERCENT()) is not None
        fifth = self._(ctx.EQUAL()) is not None
        fourth = self._(ctx.DECIMAL()) is not None
        f_5 = self._(ctx.COMMA()) is not None
        max_memory_percent = self._(ctx.MAX_MEMORY_PERCENT()) is not None
        f_5 = self._(ctx.EQUAL()) is not None
        fifth = self._(ctx.DECIMAL()) is not None
        f_6 = self._(ctx.COMMA()) is not None
        min_iops_per_volume = self._(ctx.MIN_IOPS_PER_VOLUME()) is not None
        f_6 = self._(ctx.EQUAL()) is not None
        f_5 = self._(ctx.DECIMAL()) is not None
        f_7 = self._(ctx.COMMA()) is not None
        max_iops_per_volume = self._(ctx.MAX_IOPS_PER_VOLUME()) is not None
        f_7 = self._(ctx.EQUAL()) is not None
        f_6 = self._(ctx.DECIMAL()) is not None
        auto = self._(ctx.AUTO()) is not None
        right = self._(ctx.LR_BRACKET()) is not None
        right = self._(ctx.RR_BRACKET()) is not None
        numanode = self._(ctx.NUMANODE()) is not None
        f_8 = self._(ctx.EQUAL()) is not None
        third = self._(ctx.LR_BRACKET()) is not None
        third = self._(ctx.RR_BRACKET()) is not None
        f_7 = self._(ctx.DECIMAL()) is not None
        f_8 = self._(ctx.DECIMAL()) is not None
        left = self._(ctx.TO()) is not None
        f_9 = self._(ctx.DECIMAL()) is not None
        f10 = self._(ctx.DECIMAL()) is not None
        f11 = self._(ctx.DECIMAL()) is not None
        right = self._(ctx.TO()) is not None
        f12 = self._(ctx.DECIMAL()) is not None
        return CreateResourcePool(pool_name, with_, left, left, left, min_cpu_percent, left, left, right, max_cpu_percent, right, right, third, cap_cpu_percent, third, third, fourth, affinity, scheduler, fourth, fifth, min_memory_percent, fifth, fourth, f_5, max_memory_percent, f_5, fifth, f_6, min_iops_per_volume, f_6, f_5, f_7, max_iops_per_volume, f_7, f_6, auto, right, right, numanode, f_8, third, third, f_7, f_8, left, f_9, f10, f11, right, f12)

    def visitAlter_resource_governor(self, ctx: tsql.Alter_resource_governorContext):
        left = self._(ctx.WITH()) is not None
        left = self._(ctx.LR_BRACKET()) is not None
        classifier_function = self._(ctx.CLASSIFIER_FUNCTION()) is not None
        left = self._(ctx.EQUAL()) is not None
        left = self._(ctx.RR_BRACKET()) is not None
        reset = self._(ctx.RESET()) is not None
        statistics = self._(ctx.STATISTICS()) is not None
        right = self._(ctx.WITH()) is not None
        right = self._(ctx.LR_BRACKET()) is not None
        max_outstanding_io_per_volume = self._(ctx.MAX_OUTSTANDING_IO_PER_VOLUME()) is not None
        right = self._(ctx.EQUAL()) is not None
        max_outstanding_io_per_volume = self._(ctx.DECIMAL()) is not None
        right = self._(ctx.RR_BRACKET()) is not None
        disable = self._(ctx.DISABLE()) is not None
        reconfigure = self._(ctx.RECONFIGURE()) is not None
        schema_name = self._(ctx.id_())
        dot = self._(ctx.DOT()) is not None
        null = self._(ctx.NULL_()) is not None
        return AlterResourceGovernor(left, left, classifier_function, left, left, reset, statistics, right, right, max_outstanding_io_per_volume, right, max_outstanding_io_per_volume, right, disable, reconfigure, schema_name, dot, null)

    def visitAlter_database_audit_specification(self, ctx: tsql.Alter_database_audit_specificationContext):
        audit_specification_name = self._(ctx.id_())
        for_ = self._(ctx.FOR()) is not None
        server = self._(ctx.SERVER()) is not None
        left = self._(ctx.AUDIT()) is not None
        left = self._(ctx.audit_action_spec_group(0))
        with_ = self._(ctx.WITH()) is not None
        state = self._(ctx.STATE()) is not None
        right = self.repeated(ctx, tsql.Audit_action_spec_groupContext)
        on = self._(ctx.ON()) is not None
        off = self._(ctx.OFF()) is not None
        return AlterDatabaseAuditSpecification(audit_specification_name, for_, server, left, left, with_, state, right, on, off)

    def visitAudit_action_spec_group(self, ctx: tsql.Audit_action_spec_groupContext):
        add = self._(ctx.ADD()) is not None
        drop = self._(ctx.DROP()) is not None
        audit_action_specification = self._(ctx.audit_action_specification())
        audit_action_group_name = self._(ctx.id_())
        return AuditActionSpecGroup(add, drop, audit_action_specification, audit_action_group_name)

    def visitAudit_action_specification(self, ctx: tsql.Audit_action_specificationContext):
        left = self._(ctx.action_specification(0))
        right = self.repeated(ctx, tsql.Action_specificationContext)
        audit_class_name = self._(ctx.audit_class_name())
        audit_securable = self._(ctx.audit_securable())
        left = self._(ctx.principal_id(0))
        right = self.repeated(ctx, tsql.Principal_idContext)
        return AuditActionSpecification(left, right, audit_class_name, audit_securable, left, right)

    def visitAction_specification(self, ctx: tsql.Action_specificationContext):
        select_ = self._(ctx.SELECT()) is not None
        insert = self._(ctx.INSERT()) is not None
        update = self._(ctx.UPDATE()) is not None
        delete = self._(ctx.DELETE()) is not None
        execute = self._(ctx.EXECUTE())
        receive = self._(ctx.RECEIVE()) is not None
        references = self._(ctx.REFERENCES()) is not None
        return ActionSpecification(select_, insert, update, delete, execute, receive, references)

    def visitAudit_class_name(self, ctx: tsql.Audit_class_nameContext):
        object = self._(ctx.OBJECT()) is not None
        schema = self._(ctx.SCHEMA()) is not None
        table = self._(ctx.TABLE()) is not None
        return AuditClassName(object, schema, table)

    def visitAudit_securable(self, ctx: tsql.Audit_securableContext):
        left = self._(ctx.id_(0))
        right = self._(ctx.id_(1))
        third = self._(ctx.id_(2))
        return AuditSecurable(left, right, third)

    def visitAlter_db_role(self, ctx: tsql.Alter_db_roleContext):
        role_name = self._(ctx.id_())
        member = self._(ctx.MEMBER()) is not None
        with_ = self._(ctx.WITH()) is not None
        name = self._(ctx.NAME()) is not None
        equal = self._(ctx.EQUAL()) is not None
        add = self._(ctx.ADD()) is not None
        drop = self._(ctx.DROP()) is not None
        return AlterDbRole(role_name, member, with_, name, equal, add, drop)

    def visitCreate_database_audit_specification(self, ctx: tsql.Create_database_audit_specificationContext):
        audit_specification_name = self._(ctx.id_())
        for_ = self._(ctx.FOR()) is not None
        server = self._(ctx.SERVER()) is not None
        left = self._(ctx.AUDIT()) is not None
        left = self._(ctx.audit_action_spec_group(0))
        with_ = self._(ctx.WITH()) is not None
        state = self._(ctx.STATE()) is not None
        right = self.repeated(ctx, tsql.Audit_action_spec_groupContext)
        on = self._(ctx.ON()) is not None
        off = self._(ctx.OFF()) is not None
        return CreateDatabaseAuditSpecification(audit_specification_name, for_, server, left, left, with_, state, right, on, off)

    def visitCreate_db_role(self, ctx: tsql.Create_db_roleContext):
        role_name = self._(ctx.id_())
        authorization = self._(ctx.AUTHORIZATION()) is not None
        return CreateDbRole(role_name, authorization)

    def visitCreate_route(self, ctx: tsql.Create_routeContext):
        route_name = self._(ctx.id_())
        authorization = self._(ctx.AUTHORIZATION()) is not None
        left = self._(ctx.COMMA()) is not None
        service_name = self._(ctx.SERVICE_NAME()) is not None
        left = self._(ctx.EQUAL()) is not None
        route_service_name = self._(ctx.STRING(0))
        right = self._(ctx.COMMA()) is not None
        broker_instance = self._(ctx.BROKER_INSTANCE()) is not None
        right = self._(ctx.EQUAL()) is not None
        broker_instance_identifier = self._(ctx.STRING(1))
        third = self._(ctx.COMMA()) is not None
        lifetime = self._(ctx.LIFETIME()) is not None
        third = self._(ctx.EQUAL()) is not None
        decimal = self._(ctx.DECIMAL()) is not None
        third = self._(ctx.STRING(2))
        fourth = self._(ctx.COMMA()) is not None
        mirror_address = self._(ctx.MIRROR_ADDRESS()) is not None
        fourth = self._(ctx.EQUAL()) is not None
        fourth = self._(ctx.STRING(3))
        return CreateRoute(route_name, authorization, left, service_name, left, route_service_name, right, broker_instance, right, broker_instance_identifier, third, lifetime, third, decimal, third, fourth, mirror_address, fourth, fourth)

    def visitCreate_rule(self, ctx: tsql.Create_ruleContext):
        schema_name = self._(ctx.id_())
        dot = self._(ctx.DOT()) is not None
        search_condition = self._(ctx.search_condition())
        return CreateRule(schema_name, dot, search_condition)

    def visitAlter_schema_sql(self, ctx: tsql.Alter_schema_sqlContext):
        schema_name = self._(ctx.id_(0))
        double_colon = self._(ctx.DOUBLE_COLON()) is not None
        right = self._(ctx.id_(1))
        dot = self._(ctx.DOT()) is not None
        third = self._(ctx.id_(2))
        object = self._(ctx.OBJECT()) is not None
        type_ = self._(ctx.TYPE()) is not None
        xml = self._(ctx.XML()) is not None
        left = self._(ctx.SCHEMA()) is not None
        collection = self._(ctx.COLLECTION()) is not None
        return AlterSchemaSql(schema_name, double_colon, right, dot, third, object, type_, xml, left, collection)

    def visitCreate_schema(self, ctx: tsql.Create_schemaContext):
        schema_name = self._(ctx.id_())
        left = self._(ctx.AUTHORIZATION()) is not None
        right = self._(ctx.AUTHORIZATION()) is not None
        create_table = self.repeated(ctx, tsql.Create_tableContext)
        create_view = self.repeated(ctx, tsql.Create_viewContext)
        grant = self._(ctx.GRANT()) is not None
        deny = self._(ctx.DENY()) is not None
        left = self._(ctx.SELECT()) is not None
        left = self._(ctx.INSERT()) is not None
        left = self._(ctx.DELETE()) is not None
        left = self._(ctx.UPDATE()) is not None
        left = self._(ctx.SCHEMA()) is not None
        left = self._(ctx.DOUBLE_COLON()) is not None
        right = self._(ctx.SELECT()) is not None
        right = self._(ctx.INSERT()) is not None
        right = self._(ctx.DELETE()) is not None
        right = self._(ctx.UPDATE()) is not None
        right = self._(ctx.SCHEMA()) is not None
        right = self._(ctx.DOUBLE_COLON()) is not None
        return CreateSchema(schema_name, left, right, create_table, create_view, grant, deny, left, left, left, left, left, left, right, right, right, right, right, right)

    def visitCreate_schema_azure_sql_dw_and_pdw(self, ctx: tsql.Create_schema_azure_sql_dw_and_pdwContext):
        schema_name = self._(ctx.id_())
        authorization = self._(ctx.AUTHORIZATION()) is not None
        return CreateSchemaAzureSqlDwAndPdw(schema_name, authorization)

    def visitAlter_schema_azure_sql_dw_and_pdw(self, ctx: tsql.Alter_schema_azure_sql_dw_and_pdwContext):
        schema_name = self._(ctx.id_())
        object = self._(ctx.OBJECT()) is not None
        double_colon = self._(ctx.DOUBLE_COLON()) is not None
        dot = self._(ctx.DOT()) is not None
        id = self._(ctx.ID())
        return AlterSchemaAzureSqlDwAndPdw(schema_name, object, double_colon, dot, id)

    def visitCreate_search_property_list(self, ctx: tsql.Create_search_property_listContext):
        new_list_name = self._(ctx.id_())
        from_ = self._(ctx.FROM()) is not None
        authorization = self._(ctx.AUTHORIZATION()) is not None
        dot = self._(ctx.DOT()) is not None
        return CreateSearchPropertyList(new_list_name, from_, authorization, dot)

    def visitCreate_security_policy(self, ctx: tsql.Create_security_policyContext):
        schema_name = self._(ctx.id_())
        left = self._(ctx.DOT()) is not None
        with_ = self._(ctx.WITH()) is not None
        left = self._(ctx.LR_BRACKET()) is not None
        state = self._(ctx.STATE()) is not None
        equal = self._(ctx.EQUAL()) is not None
        left = self._(ctx.RR_BRACKET()) is not None
        not_ = self._(ctx.NOT()) is not None
        for_ = self._(ctx.FOR()) is not None
        replication = self._(ctx.REPLICATION()) is not None
        filter = self._(ctx.FILTER()) is not None
        block = self._(ctx.BLOCK()) is not None
        left = self._(ctx.ON()) is not None
        left = self._(ctx.OFF()) is not None
        schemabinding = self._(ctx.SCHEMABINDING()) is not None
        insert = self._(ctx.INSERT()) is not None
        left = self._(ctx.UPDATE()) is not None
        right = self._(ctx.UPDATE()) is not None
        delete = self._(ctx.DELETE()) is not None
        right = self._(ctx.ON()) is not None
        right = self._(ctx.OFF()) is not None
        return CreateSecurityPolicy(schema_name, left, with_, left, state, equal, left, not_, for_, replication, filter, block, left, left, schemabinding, insert, left, right, delete, right, right)

    def visitAlter_sequence(self, ctx: tsql.Alter_sequenceContext):
        schema_name = self._(ctx.id_())
        dot = self._(ctx.DOT()) is not None
        restart = self._(ctx.RESTART()) is not None
        increment = self._(ctx.INCREMENT()) is not None
        by = self._(ctx.BY()) is not None
        sequnce_increment = self._(ctx.DECIMAL()) is not None
        left = self._(ctx.MINVALUE()) is not None
        right = self._(ctx.DECIMAL()) is not None
        left = self._(ctx.NO()) is not None
        right = self._(ctx.MINVALUE()) is not None
        left = self._(ctx.MAXVALUE()) is not None
        third = self._(ctx.DECIMAL()) is not None
        right = self._(ctx.NO()) is not None
        right = self._(ctx.MAXVALUE()) is not None
        left = self._(ctx.CYCLE()) is not None
        third = self._(ctx.NO()) is not None
        right = self._(ctx.CYCLE()) is not None
        left = self._(ctx.CACHE()) is not None
        fourth = self._(ctx.DECIMAL()) is not None
        fourth = self._(ctx.NO()) is not None
        right = self._(ctx.CACHE()) is not None
        with_ = self._(ctx.WITH()) is not None
        fifth = self._(ctx.DECIMAL()) is not None
        return AlterSequence(schema_name, dot, restart, increment, by, sequnce_increment, left, right, left, right, left, third, right, right, left, third, right, left, fourth, fourth, right, with_, fifth)

    def visitCreate_sequence(self, ctx: tsql.Create_sequenceContext):
        schema_name = self._(ctx.id_())
        dot = self._(ctx.DOT()) is not None
        as_ = self._(ctx.AS()) is not None
        data_type = self._(ctx.data_type())
        start = self._(ctx.START()) is not None
        with_ = self._(ctx.WITH()) is not None
        left = self._(ctx.DECIMAL()) is not None
        increment = self._(ctx.INCREMENT()) is not None
        by = self._(ctx.BY()) is not None
        left = self._(ctx.MINUS()) is not None
        right = self._(ctx.DECIMAL()) is not None
        left = self._(ctx.MINVALUE()) is not None
        left = self._(ctx.NO()) is not None
        right = self._(ctx.MINVALUE()) is not None
        left = self._(ctx.MAXVALUE()) is not None
        right = self._(ctx.NO()) is not None
        right = self._(ctx.MAXVALUE()) is not None
        left = self._(ctx.CYCLE()) is not None
        third = self._(ctx.NO()) is not None
        right = self._(ctx.CYCLE()) is not None
        left = self._(ctx.CACHE()) is not None
        third = self._(ctx.DECIMAL()) is not None
        fourth = self._(ctx.NO()) is not None
        right = self._(ctx.CACHE()) is not None
        right = self._(ctx.MINUS()) is not None
        fourth = self._(ctx.DECIMAL()) is not None
        third = self._(ctx.MINUS()) is not None
        fifth = self._(ctx.DECIMAL()) is not None
        return CreateSequence(schema_name, dot, as_, data_type, start, with_, left, increment, by, left, right, left, left, right, left, right, right, left, third, right, left, third, fourth, right, right, fourth, third, fifth)

    def visitAlter_server_audit(self, ctx: tsql.Alter_server_auditContext):
        audit_name = self._(ctx.id_())
        remove = self._(ctx.REMOVE()) is not None
        left = self._(ctx.WHERE()) is not None
        modify = self._(ctx.MODIFY()) is not None
        name = self._(ctx.NAME()) is not None
        left = self._(ctx.EQUAL()) is not None
        to = self._(ctx.TO()) is not None
        with_ = self._(ctx.WITH()) is not None
        left = self._(ctx.LR_BRACKET()) is not None
        left = self._(ctx.RR_BRACKET()) is not None
        right = self._(ctx.WHERE()) is not None
        file = self._(ctx.FILE()) is not None
        application_log = self._(ctx.APPLICATION_LOG()) is not None
        security_log = self._(ctx.SECURITY_LOG()) is not None
        left = self._(ctx.COMMA()) is not None
        right = self._(ctx.COMMA()) is not None
        left = self._(ctx.NOT()) is not None
        right = self._(ctx.LR_BRACKET()) is not None
        right = self._(ctx.RR_BRACKET()) is not None
        continue_ = self._(ctx.CONTINUE()) is not None
        shutdown = self._(ctx.SHUTDOWN()) is not None
        fail_operation = self._(ctx.FAIL_OPERATION()) is not None
        left = self._(ctx.ON()) is not None
        left = self._(ctx.OFF()) is not None
        right = self._(ctx.NOT()) is not None
        right = self._(ctx.EQUAL()) is not None
        left = self._(ctx.GREATER()) is not None
        left = self._(ctx.LESS()) is not None
        right = self._(ctx.LESS()) is not None
        third = self._(ctx.EQUAL()) is not None
        left = self._(ctx.DECIMAL()) is not None
        left = self._(ctx.STRING(0))
        and_ = self._(ctx.AND()) is not None
        or_ = self._(ctx.OR()) is not None
        fourth = self._(ctx.EQUAL()) is not None
        right = self._(ctx.GREATER()) is not None
        third = self._(ctx.LESS()) is not None
        fourth = self._(ctx.LESS()) is not None
        fifth = self._(ctx.EQUAL()) is not None
        right = self._(ctx.DECIMAL()) is not None
        right = self._(ctx.STRING(1))
        filepath = self.repeated(ctx, tsql.STRINGContext)
        alter_server_audit_max_rollover_files = self.repeated(ctx, tsql.Alter_server_audit_max_rollover_filesContext)
        fifth = self._(ctx.LESS()) is not None
        third = self._(ctx.GREATER()) is not None
        left = self._(ctx.EXCLAMATION()) is not None
        f_5 = self._(ctx.EQUAL()) is not None
        fourth = self._(ctx.GREATER()) is not None
        f_6 = self._(ctx.EQUAL()) is not None
        f_5 = self._(ctx.LESS()) is not None
        fifth = self._(ctx.GREATER()) is not None
        right = self._(ctx.EXCLAMATION()) is not None
        f_7 = self._(ctx.EQUAL()) is not None
        f_5 = self._(ctx.GREATER()) is not None
        f_8 = self._(ctx.EQUAL()) is not None
        third = self._(ctx.DECIMAL()) is not None
        unlimited = self._(ctx.UNLIMITED()) is not None
        right = self._(ctx.ON()) is not None
        right = self._(ctx.OFF()) is not None
        mb = self._(ctx.MB()) is not None
        gb = self._(ctx.GB()) is not None
        tb = self._(ctx.TB()) is not None
        return AlterServerAudit(audit_name, remove, left, modify, name, left, to, with_, left, left, right, file, application_log, security_log, left, right, left, right, right, continue_, shutdown, fail_operation, left, left, right, right, left, left, right, third, left, left, and_, or_, fourth, right, third, fourth, fifth, right, right, filepath, alter_server_audit_max_rollover_files, fifth, third, left, f_5, fourth, f_6, f_5, fifth, right, f_7, f_5, f_8, third, unlimited, right, right, mb, gb, tb)

    def visitCreate_server_audit(self, ctx: tsql.Create_server_auditContext):
        audit_name = self._(ctx.id_())
        remove = self._(ctx.REMOVE()) is not None
        left = self._(ctx.WHERE()) is not None
        modify = self._(ctx.MODIFY()) is not None
        name = self._(ctx.NAME()) is not None
        left = self._(ctx.EQUAL()) is not None
        to = self._(ctx.TO()) is not None
        with_ = self._(ctx.WITH()) is not None
        left = self._(ctx.LR_BRACKET()) is not None
        left = self._(ctx.RR_BRACKET()) is not None
        right = self._(ctx.WHERE()) is not None
        file = self._(ctx.FILE()) is not None
        application_log = self._(ctx.APPLICATION_LOG()) is not None
        security_log = self._(ctx.SECURITY_LOG()) is not None
        left = self._(ctx.COMMA()) is not None
        right = self._(ctx.COMMA()) is not None
        left = self._(ctx.NOT()) is not None
        right = self._(ctx.LR_BRACKET()) is not None
        right = self._(ctx.RR_BRACKET()) is not None
        continue_ = self._(ctx.CONTINUE()) is not None
        shutdown = self._(ctx.SHUTDOWN()) is not None
        fail_operation = self._(ctx.FAIL_OPERATION()) is not None
        left = self._(ctx.ON()) is not None
        left = self._(ctx.OFF()) is not None
        right = self._(ctx.NOT()) is not None
        right = self._(ctx.EQUAL()) is not None
        left = self._(ctx.GREATER()) is not None
        left = self._(ctx.LESS()) is not None
        right = self._(ctx.LESS()) is not None
        third = self._(ctx.EQUAL()) is not None
        left = self._(ctx.DECIMAL()) is not None
        left = self._(ctx.STRING(0))
        and_ = self._(ctx.AND()) is not None
        or_ = self._(ctx.OR()) is not None
        fourth = self._(ctx.EQUAL()) is not None
        right = self._(ctx.GREATER()) is not None
        third = self._(ctx.LESS()) is not None
        fourth = self._(ctx.LESS()) is not None
        fifth = self._(ctx.EQUAL()) is not None
        right = self._(ctx.DECIMAL()) is not None
        right = self._(ctx.STRING(1))
        filepath = self.repeated(ctx, tsql.STRINGContext)
        create_server_audit_max_rollover_files = self.repeated(ctx, tsql.Create_server_audit_max_rollover_filesContext)
        fifth = self._(ctx.LESS()) is not None
        third = self._(ctx.GREATER()) is not None
        left = self._(ctx.EXCLAMATION()) is not None
        f_5 = self._(ctx.EQUAL()) is not None
        fourth = self._(ctx.GREATER()) is not None
        f_6 = self._(ctx.EQUAL()) is not None
        f_5 = self._(ctx.LESS()) is not None
        fifth = self._(ctx.GREATER()) is not None
        right = self._(ctx.EXCLAMATION()) is not None
        f_7 = self._(ctx.EQUAL()) is not None
        f_5 = self._(ctx.GREATER()) is not None
        f_8 = self._(ctx.EQUAL()) is not None
        third = self._(ctx.DECIMAL()) is not None
        unlimited = self._(ctx.UNLIMITED()) is not None
        right = self._(ctx.ON()) is not None
        right = self._(ctx.OFF()) is not None
        mb = self._(ctx.MB()) is not None
        gb = self._(ctx.GB()) is not None
        tb = self._(ctx.TB()) is not None
        return CreateServerAudit(audit_name, remove, left, modify, name, left, to, with_, left, left, right, file, application_log, security_log, left, right, left, right, right, continue_, shutdown, fail_operation, left, left, right, right, left, left, right, third, left, left, and_, or_, fourth, right, third, fourth, fifth, right, right, filepath, create_server_audit_max_rollover_files, fifth, third, left, f_5, fourth, f_6, f_5, fifth, right, f_7, f_5, f_8, third, unlimited, right, right, mb, gb, tb)

    def visitAlter_server_audit_specification(self, ctx: tsql.Alter_server_audit_specificationContext):
        audit_specification_name = self._(ctx.id_())
        for_ = self._(ctx.FOR()) is not None
        left = self._(ctx.SERVER()) is not None
        left = self._(ctx.AUDIT()) is not None
        with_ = self._(ctx.WITH()) is not None
        left = self._(ctx.LR_BRACKET()) is not None
        state = self._(ctx.STATE()) is not None
        equal = self._(ctx.EQUAL()) is not None
        left = self._(ctx.RR_BRACKET()) is not None
        add = self._(ctx.ADD()) is not None
        drop = self._(ctx.DROP()) is not None
        on = self._(ctx.ON()) is not None
        off = self._(ctx.OFF()) is not None
        return AlterServerAuditSpecification(audit_specification_name, for_, left, left, with_, left, state, equal, left, add, drop, on, off)

    def visitCreate_server_audit_specification(self, ctx: tsql.Create_server_audit_specificationContext):
        audit_specification_name = self._(ctx.id_())
        for_ = self._(ctx.FOR()) is not None
        left = self._(ctx.SERVER()) is not None
        left = self._(ctx.AUDIT()) is not None
        with_ = self._(ctx.WITH()) is not None
        left = self._(ctx.LR_BRACKET()) is not None
        state = self._(ctx.STATE()) is not None
        equal = self._(ctx.EQUAL()) is not None
        left = self._(ctx.RR_BRACKET()) is not None
        on = self._(ctx.ON()) is not None
        off = self._(ctx.OFF()) is not None
        return CreateServerAuditSpecification(audit_specification_name, for_, left, left, with_, left, state, equal, left, on, off)

    def visitAlter_server_configuration(self, ctx: tsql.Alter_server_configurationContext):
        process = self._(ctx.PROCESS()) is not None
        affinity = self._(ctx.AFFINITY()) is not None
        diagnostics = self._(ctx.DIAGNOSTICS()) is not None
        log = self._(ctx.LOG()) is not None
        failover = self._(ctx.FAILOVER()) is not None
        left = self._(ctx.CLUSTER()) is not None
        property = self._(ctx.PROPERTY()) is not None
        hadr = self._(ctx.HADR()) is not None
        right = self._(ctx.CLUSTER()) is not None
        context = self._(ctx.CONTEXT()) is not None
        left = self._(ctx.EQUAL()) is not None
        buffer = self._(ctx.BUFFER()) is not None
        pool = self._(ctx.POOL()) is not None
        extension = self._(ctx.EXTENSION()) is not None
        left = self._(ctx.SET()) is not None
        softnuma = self._(ctx.SOFTNUMA()) is not None
        cpu = self._(ctx.CPU()) is not None
        right = self._(ctx.EQUAL()) is not None
        numanode = self._(ctx.NUMANODE()) is not None
        third = self._(ctx.EQUAL()) is not None
        left = self._(ctx.ON()) is not None
        left = self._(ctx.OFF()) is not None
        path = self._(ctx.PATH()) is not None
        fourth = self._(ctx.EQUAL()) is not None
        max_size = self._(ctx.MAX_SIZE()) is not None
        fifth = self._(ctx.EQUAL()) is not None
        max_files = self._(ctx.MAX_FILES()) is not None
        f_5 = self._(ctx.EQUAL()) is not None
        verboselogging = self._(ctx.VERBOSELOGGING()) is not None
        f_6 = self._(ctx.EQUAL()) is not None
        sqldumperflags = self._(ctx.SQLDUMPERFLAGS()) is not None
        f_7 = self._(ctx.EQUAL()) is not None
        sqldumperpath = self._(ctx.SQLDUMPERPATH()) is not None
        f_8 = self._(ctx.EQUAL()) is not None
        sqldumpertimeout = self._(ctx.SQLDUMPERTIMEOUT()) is not None
        failureconditionlevel = self._(ctx.FAILURECONDITIONLEVEL()) is not None
        f_9 = self._(ctx.EQUAL()) is not None
        healthchecktimeout = self._(ctx.HEALTHCHECKTIMEOUT()) is not None
        f10 = self._(ctx.EQUAL()) is not None
        left = self._(ctx.STRING(0))
        local = self._(ctx.LOCAL()) is not None
        right = self._(ctx.ON()) is not None
        lr_bracket = self._(ctx.LR_BRACKET()) is not None
        filename = self._(ctx.FILENAME()) is not None
        f11 = self._(ctx.EQUAL()) is not None
        right = self._(ctx.STRING(1))
        left = self._(ctx.COMMA()) is not None
        size = self._(ctx.SIZE()) is not None
        f12 = self._(ctx.EQUAL()) is not None
        left = self._(ctx.DECIMAL()) is not None
        rr_bracket = self._(ctx.RR_BRACKET()) is not None
        right = self._(ctx.OFF()) is not None
        third = self._(ctx.ON()) is not None
        third = self._(ctx.OFF()) is not None
        auto = self._(ctx.AUTO()) is not None
        third = self._(ctx.STRING(2))
        left = self._(ctx.DEFAULT()) is not None
        right = self._(ctx.DECIMAL()) is not None
        left = self._(ctx.MB()) is not None
        right = self._(ctx.DEFAULT()) is not None
        third = self._(ctx.DECIMAL()) is not None
        third = self._(ctx.DEFAULT()) is not None
        fourth = self._(ctx.STRING(3))
        fourth = self._(ctx.DEFAULT()) is not None
        fifth = self._(ctx.STRING(4))
        fifth = self._(ctx.DEFAULT()) is not None
        f_5 = self._(ctx.STRING(5))
        f_5 = self._(ctx.DEFAULT()) is not None
        f_6 = self._(ctx.STRING(6))
        f_6 = self._(ctx.DEFAULT()) is not None
        f_7 = self._(ctx.STRING(7))
        f_7 = self._(ctx.DEFAULT()) is not None
        fourth = self._(ctx.DECIMAL()) is not None
        f_8 = self._(ctx.DEFAULT()) is not None
        kb = self._(ctx.KB()) is not None
        right = self._(ctx.MB()) is not None
        gb = self._(ctx.GB()) is not None
        return AlterServerConfiguration(process, affinity, diagnostics, log, failover, left, property, hadr, right, context, left, buffer, pool, extension, left, softnuma, cpu, right, numanode, third, left, left, path, fourth, max_size, fifth, max_files, f_5, verboselogging, f_6, sqldumperflags, f_7, sqldumperpath, f_8, sqldumpertimeout, failureconditionlevel, f_9, healthchecktimeout, f10, left, local, right, lr_bracket, filename, f11, right, left, size, f12, left, rr_bracket, right, third, third, auto, third, left, right, left, right, third, third, fourth, fourth, fifth, fifth, f_5, f_5, f_6, f_6, f_7, f_7, fourth, f_8, kb, right, gb)

    def visitAlter_server_role(self, ctx: tsql.Alter_server_roleContext):
        server_role_name = self._(ctx.id_())
        member = self._(ctx.MEMBER()) is not None
        with_ = self._(ctx.WITH()) is not None
        name = self._(ctx.NAME()) is not None
        equal = self._(ctx.EQUAL()) is not None
        add = self._(ctx.ADD()) is not None
        drop = self._(ctx.DROP()) is not None
        return AlterServerRole(server_role_name, member, with_, name, equal, add, drop)

    def visitCreate_server_role(self, ctx: tsql.Create_server_roleContext):
        server_role = self._(ctx.id_())
        authorization = self._(ctx.AUTHORIZATION()) is not None
        return CreateServerRole(server_role, authorization)

    def visitAlter_server_role_pdw(self, ctx: tsql.Alter_server_role_pdwContext):
        server_role_name = self._(ctx.id_())
        add = self._(ctx.ADD()) is not None
        drop = self._(ctx.DROP()) is not None
        return AlterServerRolePdw(server_role_name, add, drop)

    def visitAlter_service(self, ctx: tsql.Alter_serviceContext):
        modified_service_name = self._(ctx.id_())
        on = self._(ctx.ON()) is not None
        queue = self._(ctx.QUEUE()) is not None
        left = self._(ctx.opt_arg_clause(0))
        dot = self._(ctx.DOT()) is not None
        right = self.repeated(ctx, tsql.Opt_arg_clauseContext)
        return AlterService(modified_service_name, on, queue, left, dot, right)

    def visitOpt_arg_clause(self, ctx: tsql.Opt_arg_clauseContext):
        add = self._(ctx.ADD()) is not None
        drop = self._(ctx.DROP()) is not None
        modified_contract_name = self._(ctx.id_())
        return OptArgClause(add, drop, modified_contract_name)

    def visitCreate_service(self, ctx: tsql.Create_serviceContext):
        create_service_name = self._(ctx.id_())
        authorization = self._(ctx.AUTHORIZATION()) is not None
        dot = self._(ctx.DOT()) is not None
        lr_bracket = self._(ctx.LR_BRACKET()) is not None
        rr_bracket = self._(ctx.RR_BRACKET()) is not None
        default_ = self._(ctx.DEFAULT()) is not None
        return CreateService(create_service_name, authorization, dot, lr_bracket, rr_bracket, default_)

    def visitAlter_service_master_key(self, ctx: tsql.Alter_service_master_keyContext):
        force = self._(ctx.FORCE()) is not None
        regenerate = self._(ctx.REGENERATE()) is not None
        with_ = self._(ctx.WITH()) is not None
        old_account = self._(ctx.OLD_ACCOUNT()) is not None
        left = self._(ctx.EQUAL()) is not None
        acold_account_name = self._(ctx.STRING())
        left = self._(ctx.COMMA()) is not None
        old_password = self._(ctx.OLD_PASSWORD()) is not None
        right = self._(ctx.EQUAL()) is not None
        new_account = self._(ctx.NEW_ACCOUNT()) is not None
        third = self._(ctx.EQUAL()) is not None
        right = self._(ctx.COMMA()) is not None
        new_password = self._(ctx.NEW_PASSWORD()) is not None
        fourth = self._(ctx.EQUAL()) is not None
        return AlterServiceMasterKey(force, regenerate, with_, old_account, left, acold_account_name, left, old_password, right, new_account, third, right, new_password, fourth)

    def visitAlter_symmetric_key(self, ctx: tsql.Alter_symmetric_keyContext):
        key_name = self._(ctx.id_())
        encryption = self._(ctx.ENCRYPTION()) is not None
        by = self._(ctx.BY()) is not None
        add = self._(ctx.ADD()) is not None
        drop = self._(ctx.DROP()) is not None
        certificate = self._(ctx.CERTIFICATE()) is not None
        password = self._(ctx.PASSWORD()) is not None
        equal = self._(ctx.EQUAL()) is not None
        password = self._(ctx.STRING())
        left = self._(ctx.SYMMETRIC()) is not None
        left = self._(ctx.KEY()) is not None
        asymmetric = self._(ctx.ASYMMETRIC()) is not None
        right = self._(ctx.KEY()) is not None
        return AlterSymmetricKey(key_name, encryption, by, add, drop, certificate, password, equal, password, left, left, asymmetric, right)

    def visitCreate_synonym(self, ctx: tsql.Create_synonymContext):
        schema_name_1 = self._(ctx.id_())
        left = self._(ctx.DOT()) is not None
        right = self._(ctx.DOT()) is not None
        third = self._(ctx.DOT()) is not None
        fourth = self._(ctx.DOT()) is not None
        fifth = self._(ctx.DOT()) is not None
        f_5 = self._(ctx.DOT()) is not None
        return CreateSynonym(schema_name_1, left, right, third, fourth, fifth, f_5)

    def visitAlter_user(self, ctx: tsql.Alter_userContext):
        username = self._(ctx.id_())
        left = self.repeated(ctx, tsql.STRINGContext)
        null = self._(ctx.NULL_()) is not None
        right = self.repeated(ctx, tsql.STRINGContext)
        none = self._(ctx.NONE()) is not None
        lcid = self._(ctx.DECIMAL()) is not None
        on = self._(ctx.ON()) is not None
        off = self._(ctx.OFF()) is not None
        return AlterUser(username, left, null, right, none, lcid, on, off)

    def visitCreate_user(self, ctx: tsql.Create_userContext):
        create = self._(ctx.CREATE()) is not None
        user = self._(ctx.USER()) is not None
        user_name = self._(ctx.id_())
        login = self._(ctx.LOGIN()) is not None
        with_ = self._(ctx.WITH()) is not None
        for_ = self._(ctx.FOR()) is not None
        from_ = self._(ctx.FROM()) is not None
        on = self._(ctx.ON()) is not None
        off = self._(ctx.OFF()) is not None
        password = self._(ctx.PASSWORD()) is not None
        left = self._(ctx.EQUAL()) is not None
        password = self._(ctx.STRING())
        external = self._(ctx.EXTERNAL()) is not None
        provider = self._(ctx.PROVIDER()) is not None
        right = self._(ctx.WITH()) is not None
        left = self.repeated(ctx, tsql.BINARYContext)
        right = self.repeated(ctx, tsql.BINARYContext)
        left = self._(ctx.NONE()) is not None
        left = self._(ctx.DECIMAL()) is not None
        right = self._(ctx.NONE()) is not None
        right = self._(ctx.DECIMAL()) is not None
        right = self._(ctx.ON()) is not None
        right = self._(ctx.OFF()) is not None
        without = self._(ctx.WITHOUT()) is not None
        certificate = self._(ctx.CERTIFICATE()) is not None
        asymmetric = self._(ctx.ASYMMETRIC()) is not None
        key = self._(ctx.KEY()) is not None
        right = self._(ctx.FOR()) is not None
        right = self._(ctx.FROM()) is not None
        return CreateUser(create, user, user_name, login, with_, for_, from_, on, off, password, left, password, external, provider, right, left, right, left, left, right, right, right, right, without, certificate, asymmetric, key, right, right)

    def visitCreate_user_azure_sql_dw(self, ctx: tsql.Create_user_azure_sql_dwContext):
        create = self._(ctx.CREATE()) is not None
        user = self._(ctx.USER()) is not None
        user_name = self._(ctx.id_())
        left = self._(ctx.LOGIN()) is not None
        without = self._(ctx.WITHOUT()) is not None
        right = self._(ctx.LOGIN()) is not None
        with_ = self._(ctx.WITH()) is not None
        default_schema = self._(ctx.DEFAULT_SCHEMA()) is not None
        equal = self._(ctx.EQUAL()) is not None
        for_ = self._(ctx.FOR()) is not None
        from_ = self._(ctx.FROM()) is not None
        external = self._(ctx.EXTERNAL()) is not None
        provider = self._(ctx.PROVIDER()) is not None
        return CreateUserAzureSqlDw(create, user, user_name, left, without, right, with_, default_schema, equal, for_, from_, external, provider)

    def visitAlter_user_azure_sql(self, ctx: tsql.Alter_user_azure_sqlContext):
        username = self._(ctx.id_())
        on = self._(ctx.ON()) is not None
        off = self._(ctx.OFF()) is not None
        return AlterUserAzureSql(username, on, off)

    def visitAlter_workload_group(self, ctx: tsql.Alter_workload_groupContext):
        workload_group_group_name = self._(ctx.id_())
        left = self._(ctx.DEFAULT_DOUBLE_QUOTE(0))
        with_ = self._(ctx.WITH()) is not None
        lr_bracket = self._(ctx.LR_BRACKET()) is not None
        rr_bracket = self._(ctx.RR_BRACKET()) is not None
        using = self._(ctx.USING()) is not None
        right = self._(ctx.DEFAULT_DOUBLE_QUOTE(1))
        low = self._(ctx.LOW()) is not None
        medium = self._(ctx.MEDIUM()) is not None
        high = self._(ctx.HIGH()) is not None
        return AlterWorkloadGroup(workload_group_group_name, left, with_, lr_bracket, rr_bracket, using, right, low, medium, high)

    def visitCreate_workload_group(self, ctx: tsql.Create_workload_groupContext):
        workload_group_group_name = self._(ctx.id_())
        with_ = self._(ctx.WITH()) is not None
        lr_bracket = self._(ctx.LR_BRACKET()) is not None
        rr_bracket = self._(ctx.RR_BRACKET()) is not None
        using = self._(ctx.USING()) is not None
        left = self._(ctx.DEFAULT_DOUBLE_QUOTE(0))
        left = self._(ctx.COMMA()) is not None
        external = self._(ctx.EXTERNAL()) is not None
        right = self._(ctx.DEFAULT_DOUBLE_QUOTE(1))
        low = self._(ctx.LOW()) is not None
        medium = self._(ctx.MEDIUM()) is not None
        high = self._(ctx.HIGH()) is not None
        return CreateWorkloadGroup(workload_group_group_name, with_, lr_bracket, rr_bracket, using, left, left, external, right, low, medium, high)

    def visitCreate_xml_schema_collection(self, ctx: tsql.Create_xml_schema_collectionContext):
        relational_schema = self._(ctx.id_())
        dot = self._(ctx.DOT()) is not None
        string = self._(ctx.STRING())
        local_id = self._(ctx.LOCAL_ID())
        return CreateXmlSchemaCollection(relational_schema, dot, string, local_id)

    def visitCreate_partition_function(self, ctx: tsql.Create_partition_functionContext):
        partition_function_name = self._(ctx.id_())
        input_parameter_type = self._(ctx.data_type())
        left = self._(ctx.LEFT()) is not None
        right = self._(ctx.RIGHT()) is not None
        boundary_values = self._(ctx.expression_list_())
        return CreatePartitionFunction(partition_function_name, input_parameter_type, left, right, boundary_values)

    def visitCreate_partition_scheme(self, ctx: tsql.Create_partition_schemeContext):
        partition_scheme_name = self._(ctx.id_())
        return CreatePartitionScheme(partition_scheme_name)

    def visitCreate_queue(self, ctx: tsql.Create_queueContext):
        full_table_name = self._(ctx.full_table_name())
        queue_name = self._(ctx.id_())
        queue_settings = self.repeated(ctx, tsql.Queue_settingsContext)
        on = self._(ctx.ON()) is not None
        default_ = self._(ctx.DEFAULT()) is not None
        return CreateQueue(full_table_name, queue_name, queue_settings, on, default_)

    def visitQueue_settings(self, ctx: tsql.Queue_settingsContext):
        left = self._(ctx.STATUS()) is not None
        left = self._(ctx.EQUAL()) is not None
        left = self._(ctx.on_off(0))
        left = self._(ctx.COMMA()) is not None
        retention = self._(ctx.RETENTION()) is not None
        right = self._(ctx.EQUAL()) is not None
        right = self._(ctx.on_off(1))
        right = self._(ctx.COMMA()) is not None
        activation = self._(ctx.ACTIVATION()) is not None
        left = self._(ctx.LR_BRACKET()) is not None
        left = self._(ctx.RR_BRACKET()) is not None
        third = self._(ctx.COMMA()) is not None
        poison_message_handling = self._(ctx.POISON_MESSAGE_HANDLING()) is not None
        right = self._(ctx.LR_BRACKET()) is not None
        right = self._(ctx.RR_BRACKET()) is not None
        drop = self._(ctx.DROP()) is not None
        right = self._(ctx.STATUS()) is not None
        third = self._(ctx.EQUAL()) is not None
        third = self._(ctx.on_off(2))
        third = self._(ctx.STATUS()) is not None
        fourth = self._(ctx.EQUAL()) is not None
        fourth = self._(ctx.on_off(3))
        fourth = self._(ctx.COMMA()) is not None
        procedure_name = self._(ctx.PROCEDURE_NAME()) is not None
        fifth = self._(ctx.EQUAL()) is not None
        func_proc_name_database_schema = self._(ctx.func_proc_name_database_schema())
        fifth = self._(ctx.COMMA()) is not None
        max_queue_readers = self._(ctx.MAX_QUEUE_READERS()) is not None
        f_5 = self._(ctx.EQUAL()) is not None
        max_readers = self._(ctx.DECIMAL()) is not None
        f_5 = self._(ctx.COMMA()) is not None
        execute = self._(ctx.EXECUTE())
        as_ = self._(ctx.AS()) is not None
        f_6 = self._(ctx.COMMA()) is not None
        self = self._(ctx.SELF()) is not None
        user_name = self._(ctx.STRING())
        owner = self._(ctx.OWNER()) is not None
        return QueueSettings(left, left, left, left, retention, right, right, right, activation, left, left, third, poison_message_handling, right, right, drop, right, third, third, third, fourth, fourth, fourth, procedure_name, fifth, func_proc_name_database_schema, fifth, max_queue_readers, f_5, max_readers, f_5, execute, as_, f_6, self, user_name, owner)

    def visitAlter_queue(self, ctx: tsql.Alter_queueContext):
        full_table_name = self._(ctx.full_table_name())
        queue_name = self._(ctx.id_())
        queue_settings = self._(ctx.queue_settings())
        queue_action = self._(ctx.queue_action())
        return AlterQueue(full_table_name, queue_name, queue_settings, queue_action)

    def visitQueue_action(self, ctx: tsql.Queue_actionContext):
        rebuild = self._(ctx.REBUILD()) is not None
        with_ = self._(ctx.WITH()) is not None
        lr_bracket = self._(ctx.LR_BRACKET()) is not None
        rr_bracket = self._(ctx.RR_BRACKET()) is not None
        reorganize = self._(ctx.REORGANIZE()) is not None
        lob_compaction = self._(ctx.LOB_COMPACTION()) is not None
        equal = self._(ctx.EQUAL()) is not None
        on_off = self._(ctx.on_off())
        move = self._(ctx.MOVE()) is not None
        to = self._(ctx.TO()) is not None
        id = self._(ctx.id_())
        default_ = self._(ctx.DEFAULT()) is not None
        return QueueAction(rebuild, with_, lr_bracket, rr_bracket, reorganize, lob_compaction, equal, on_off, move, to, id, default_)

    def visitCreate_contract(self, ctx: tsql.Create_contractContext):
        contract_name = self._(ctx.contract_name())
        authorization = self._(ctx.AUTHORIZATION()) is not None
        owner_name = self._(ctx.id_())
        default_ = self._(ctx.DEFAULT()) is not None
        initiator = self._(ctx.INITIATOR()) is not None
        target = self._(ctx.TARGET()) is not None
        any = self._(ctx.ANY()) is not None
        return CreateContract(contract_name, authorization, owner_name, default_, initiator, target, any)

    def visitConversation_statement(self, ctx: tsql.Conversation_statementContext):
        begin_conversation_timer = self._(ctx.begin_conversation_timer())
        begin_conversation_dialog = self._(ctx.begin_conversation_dialog())
        end_conversation = self._(ctx.end_conversation())
        get_conversation = self._(ctx.get_conversation())
        send_conversation = self._(ctx.send_conversation())
        waitfor_conversation = self._(ctx.waitfor_conversation())
        return ConversationStatement(begin_conversation_timer, begin_conversation_dialog, end_conversation, get_conversation, send_conversation, waitfor_conversation)

    def visitMessage_statement(self, ctx: tsql.Message_statementContext):
        message_type_name = self._(ctx.id_())
        authorization = self._(ctx.AUTHORIZATION()) is not None
        validation = self._(ctx.VALIDATION()) is not None
        equal = self._(ctx.EQUAL()) is not None
        none = self._(ctx.NONE()) is not None
        empty = self._(ctx.EMPTY()) is not None
        well_formed_xml = self._(ctx.WELL_FORMED_XML()) is not None
        valid_xml = self._(ctx.VALID_XML()) is not None
        with_ = self._(ctx.WITH()) is not None
        schema = self._(ctx.SCHEMA()) is not None
        collection = self._(ctx.COLLECTION()) is not None
        return MessageStatement(message_type_name, authorization, validation, equal, none, empty, well_formed_xml, valid_xml, with_, schema, collection)

    def visitMerge_statement(self, ctx: tsql.Merge_statementContext):
        with_expression = self.repeated(ctx, tsql.With_expressionContext)
        top = self._(ctx.TOP()) is not None
        expression = self._(ctx.expression())
        percent = self._(ctx.PERCENT()) is not None
        ddl_object = self._(ctx.ddl_object())
        with_table_hints = self.repeated(ctx, tsql.With_table_hintsContext)
        as_table_alias = self.repeated(ctx, tsql.As_table_aliasContext)
        table_sources = self._(ctx.table_sources())
        search_condition = self._(ctx.search_condition())
        when_matches = self._(ctx.when_matches())
        output_clause = self.repeated(ctx, tsql.Output_clauseContext)
        option_clause = self.repeated(ctx, tsql.Option_clauseContext)
        return MergeStatement(with_expression, top, expression, percent, ddl_object, with_table_hints, as_table_alias, table_sources, search_condition, when_matches, output_clause, option_clause)

    def visitWhen_matches(self, ctx: tsql.When_matchesContext):
        merge_matched = self.repeated(ctx, tsql.Merge_matchedContext)
        and_ = self._(ctx.AND()) is not None
        search_condition = self._(ctx.search_condition())
        when = self._(ctx.WHEN()) is not None
        not_ = self._(ctx.NOT()) is not None
        matched = self._(ctx.MATCHED()) is not None
        then = self._(ctx.THEN()) is not None
        merge_not_matched = self._(ctx.merge_not_matched())
        by = self._(ctx.BY()) is not None
        target = self._(ctx.TARGET()) is not None
        return WhenMatches(merge_matched, and_, search_condition, when, not_, matched, then, merge_not_matched, by, target)

    def visitMerge_matched(self, ctx: tsql.Merge_matchedContext):
        update = self._(ctx.UPDATE()) is not None
        set = self._(ctx.SET()) is not None
        left = self._(ctx.update_elem_merge(0))
        right = self.repeated(ctx, tsql.Update_elem_mergeContext)
        delete = self._(ctx.DELETE()) is not None
        return MergeMatched(update, set, left, right, delete)

    def visitMerge_not_matched(self, ctx: tsql.Merge_not_matchedContext):
        column_name_list = self._(ctx.column_name_list())
        table_value_constructor = self._(ctx.table_value_constructor())
        default_ = self._(ctx.DEFAULT()) is not None
        values = self._(ctx.VALUES()) is not None
        return MergeNotMatched(column_name_list, table_value_constructor, default_, values)

    def visitDelete_statement(self, ctx: tsql.Delete_statementContext):
        with_expression = self.repeated(ctx, tsql.With_expressionContext)
        left = self._(ctx.TOP()) is not None
        expression = self._(ctx.expression())
        percent = self._(ctx.PERCENT()) is not None
        right = self._(ctx.TOP()) is not None
        decimal = self._(ctx.DECIMAL()) is not None
        delete_statement_from = self._(ctx.delete_statement_from())
        with_table_hints = self.repeated(ctx, tsql.With_table_hintsContext)
        output_clause = self.repeated(ctx, tsql.Output_clauseContext)
        left = self._(ctx.FROM()) is not None
        table_sources = self._(ctx.table_sources())
        where = self._(ctx.WHERE()) is not None
        for_clause = self.repeated(ctx, tsql.For_clauseContext)
        option_clause = self.repeated(ctx, tsql.Option_clauseContext)
        search_condition = self._(ctx.search_condition())
        current = self._(ctx.CURRENT()) is not None
        of = self._(ctx.OF()) is not None
        global_ = self._(ctx.GLOBAL()) is not None
        cursor_name = self._(ctx.cursor_name())
        cursor_var = self._(ctx.LOCAL_ID())
        return DeleteStatement(with_expression, left, expression, percent, right, decimal, delete_statement_from, with_table_hints, output_clause, left, table_sources, where, for_clause, option_clause, search_condition, current, of, global_, cursor_name, cursor_var)

    def visitDelete_statement_from(self, ctx: tsql.Delete_statement_fromContext):
        ddl_object = self._(ctx.ddl_object())
        rowset_function_limited = self._(ctx.rowset_function_limited())
        table_var = self._(ctx.LOCAL_ID())
        return DeleteStatementFrom(ddl_object, rowset_function_limited, table_var)

    def visitInsert_statement(self, ctx: tsql.Insert_statementContext):
        with_expression = self.repeated(ctx, tsql.With_expressionContext)
        top = self._(ctx.TOP()) is not None
        expression = self._(ctx.expression())
        percent = self._(ctx.PERCENT()) is not None
        ddl_object = self._(ctx.ddl_object())
        rowset_function_limited = self._(ctx.rowset_function_limited())
        with_table_hints = self.repeated(ctx, tsql.With_table_hintsContext)
        insert_column_name_list = self._(ctx.insert_column_name_list())
        output_clause = self.repeated(ctx, tsql.Output_clauseContext)
        insert_statement_value = self._(ctx.insert_statement_value())
        for_clause = self.repeated(ctx, tsql.For_clauseContext)
        option_clause = self.repeated(ctx, tsql.Option_clauseContext)
        return InsertStatement(with_expression, top, expression, percent, ddl_object, rowset_function_limited, with_table_hints, insert_column_name_list, output_clause, insert_statement_value, for_clause, option_clause)

    def visitInsert_statement_value(self, ctx: tsql.Insert_statement_valueContext):
        table_value_constructor = self._(ctx.table_value_constructor())
        derived_table = self._(ctx.derived_table())
        execute_statement = self._(ctx.execute_statement())
        default_ = self._(ctx.DEFAULT()) is not None
        values = self._(ctx.VALUES()) is not None
        return InsertStatementValue(table_value_constructor, derived_table, execute_statement, default_, values)

    def visitReceive_statement(self, ctx: tsql.Receive_statementContext):
        all = self._(ctx.ALL()) is not None
        distinct = self._(ctx.DISTINCT()) is not None
        top_clause = self._(ctx.top_clause())
        local_id = self.repeated(ctx, tsql.LOCAL_IDContext)
        expression = self.repeated(ctx, tsql.ExpressionContext)
        full_table_name = self._(ctx.full_table_name())
        into = self._(ctx.INTO()) is not None
        table_variable = self._(ctx.id_())
        where = self._(ctx.WHERE()) is not None
        where = self._(ctx.search_condition())
        return ReceiveStatement(all, distinct, top_clause, local_id, expression, full_table_name, into, table_variable, where, where)

    def visitSelect_statement_standalone(self, ctx: tsql.Select_statement_standaloneContext):
        with_expression = self.repeated(ctx, tsql.With_expressionContext)
        select_statement = self._(ctx.select_statement())
        return SelectStatementStandalone(with_expression, select_statement)

    def visitSelect_statement(self, ctx: tsql.Select_statementContext):
        query_expression = self._(ctx.query_expression())
        select_order_by_clause = self.repeated(ctx, tsql.Select_order_by_clauseContext)
        for_clause = self.repeated(ctx, tsql.For_clauseContext)
        option_clause = self.repeated(ctx, tsql.Option_clauseContext)
        return SelectStatement(query_expression, select_order_by_clause, for_clause, option_clause)

    def visitTime(self, ctx: tsql.TimeContext):
        local_id = self._(ctx.LOCAL_ID())
        constant = self._(ctx.constant())
        return Time(local_id, constant)

    def visitUpdate_statement(self, ctx: tsql.Update_statementContext):
        with_expression = self.repeated(ctx, tsql.With_expressionContext)
        top = self._(ctx.TOP()) is not None
        expression = self._(ctx.expression())
        percent = self._(ctx.PERCENT()) is not None
        ddl_object = self._(ctx.ddl_object())
        rowset_function_limited = self._(ctx.rowset_function_limited())
        with_table_hints = self.repeated(ctx, tsql.With_table_hintsContext)
        left = self._(ctx.update_elem(0))
        right = self.repeated(ctx, tsql.Update_elemContext)
        output_clause = self.repeated(ctx, tsql.Output_clauseContext)
        from_ = self._(ctx.FROM()) is not None
        table_sources = self._(ctx.table_sources())
        where = self._(ctx.WHERE()) is not None
        for_clause = self.repeated(ctx, tsql.For_clauseContext)
        option_clause = self.repeated(ctx, tsql.Option_clauseContext)
        search_condition = self._(ctx.search_condition())
        current = self._(ctx.CURRENT()) is not None
        of = self._(ctx.OF()) is not None
        global_ = self._(ctx.GLOBAL()) is not None
        cursor_name = self._(ctx.cursor_name())
        cursor_var = self._(ctx.LOCAL_ID())
        return UpdateStatement(with_expression, top, expression, percent, ddl_object, rowset_function_limited, with_table_hints, left, right, output_clause, from_, table_sources, where, for_clause, option_clause, search_condition, current, of, global_, cursor_name, cursor_var)

    def visitOutput_clause(self, ctx: tsql.Output_clauseContext):
        left = self._(ctx.output_dml_list_elem(0))
        right = self.repeated(ctx, tsql.Output_dml_list_elemContext)
        into = self._(ctx.INTO()) is not None
        local_id = self._(ctx.LOCAL_ID())
        table_name = self._(ctx.table_name())
        column_name_list = self._(ctx.column_name_list())
        return OutputClause(left, right, into, local_id, table_name, column_name_list)

    def visitOutput_dml_list_elem(self, ctx: tsql.Output_dml_list_elemContext):
        expression = self._(ctx.expression())
        asterisk = self._(ctx.asterisk())
        as_column_alias = self.repeated(ctx, tsql.As_column_aliasContext)
        return OutputDmlListElem(expression, asterisk, as_column_alias)

    def visitCreate_database(self, ctx: tsql.Create_databaseContext):
        database = self._(ctx.id_())
        containment = self._(ctx.CONTAINMENT()) is not None
        left = self._(ctx.ON()) is not None
        primary = self._(ctx.PRIMARY()) is not None
        left = self._(ctx.database_file_spec(0))
        log = self._(ctx.LOG()) is not None
        right = self._(ctx.ON()) is not None
        right = self._(ctx.database_file_spec(1))
        collate = self._(ctx.COLLATE()) is not None
        with_ = self._(ctx.WITH()) is not None
        left = self._(ctx.create_database_option(0))
        none = self._(ctx.NONE()) is not None
        partial = self._(ctx.PARTIAL()) is not None
        third = self.repeated(ctx, tsql.Database_file_specContext)
        fourth = self.repeated(ctx, tsql.Database_file_specContext)
        right = self.repeated(ctx, tsql.Create_database_optionContext)
        return CreateDatabase(database, containment, left, primary, left, log, right, right, collate, with_, left, none, partial, third, fourth, right)

    def visitCreate_index(self, ctx: tsql.Create_indexContext):
        clustered = self.repeated(ctx, tsql.ClusteredContext)
        left = self._(ctx.id_(0))
        table_name = self._(ctx.table_name())
        column_name_list_with_order = self._(ctx.column_name_list_with_order())
        include = self._(ctx.INCLUDE()) is not None
        column_name_list = self._(ctx.column_name_list())
        where = self._(ctx.WHERE()) is not None
        where = self._(ctx.search_condition())
        create_index_options = self._(ctx.create_index_options())
        left = self._(ctx.ON()) is not None
        right = self._(ctx.id_(1))
        return CreateIndex(clustered, left, table_name, column_name_list_with_order, include, column_name_list, where, where, create_index_options, left, right)

    def visitCreate_index_options(self, ctx: tsql.Create_index_optionsContext):
        left = self._(ctx.relational_index_option(0))
        right = self.repeated(ctx, tsql.Relational_index_optionContext)
        return CreateIndexOptions(left, right)

    def visitRelational_index_option(self, ctx: tsql.Relational_index_optionContext):
        rebuild_index_option = self._(ctx.rebuild_index_option())
        drop_existing = self._(ctx.DROP_EXISTING()) is not None
        on_off = self._(ctx.on_off())
        optimize_for_sequential_key = self._(ctx.OPTIMIZE_FOR_SEQUENTIAL_KEY()) is not None
        return RelationalIndexOption(rebuild_index_option, drop_existing, on_off, optimize_for_sequential_key)

    def visitAlter_index(self, ctx: tsql.Alter_indexContext):
        id = self._(ctx.id_())
        all = self._(ctx.ALL()) is not None
        table_name = self._(ctx.table_name())
        disable = self._(ctx.DISABLE()) is not None
        pause = self._(ctx.PAUSE()) is not None
        abort = self._(ctx.ABORT()) is not None
        resume = self._(ctx.RESUME()) is not None
        resumable_index_options = self._(ctx.resumable_index_options())
        reorganize_partition = self._(ctx.reorganize_partition())
        set_index_options = self._(ctx.set_index_options())
        rebuild_partition = self._(ctx.rebuild_partition())
        return AlterIndex(id, all, table_name, disable, pause, abort, resume, resumable_index_options, reorganize_partition, set_index_options, rebuild_partition)

    def visitResumable_index_options(self, ctx: tsql.Resumable_index_optionsContext):
        left = self._(ctx.resumable_index_option(0))
        right = self.repeated(ctx, tsql.Resumable_index_optionContext)
        return ResumableIndexOptions(left, right)

    def visitResumable_index_option(self, ctx: tsql.Resumable_index_optionContext):
        maxdop = self._(ctx.MAXDOP()) is not None
        max_degree_of_parallelism = self._(ctx.DECIMAL()) is not None
        max_duration = self._(ctx.MAX_DURATION()) is not None
        low_priority_lock_wait = self._(ctx.low_priority_lock_wait())
        return ResumableIndexOption(maxdop, max_degree_of_parallelism, max_duration, low_priority_lock_wait)

    def visitReorganize_partition(self, ctx: tsql.Reorganize_partitionContext):
        partition = self._(ctx.PARTITION()) is not None
        decimal = self._(ctx.DECIMAL()) is not None
        reorganize_options = self.repeated(ctx, tsql.Reorganize_optionsContext)
        return ReorganizePartition(partition, decimal, reorganize_options)

    def visitReorganize_options(self, ctx: tsql.Reorganize_optionsContext):
        left = self._(ctx.reorganize_option(0))
        right = self.repeated(ctx, tsql.Reorganize_optionContext)
        return ReorganizeOptions(left, right)

    def visitReorganize_option(self, ctx: tsql.Reorganize_optionContext):
        lob_compaction = self._(ctx.LOB_COMPACTION()) is not None
        on_off = self._(ctx.on_off())
        compress_all_row_groups = self._(ctx.COMPRESS_ALL_ROW_GROUPS()) is not None
        return ReorganizeOption(lob_compaction, on_off, compress_all_row_groups)

    def visitSet_index_options(self, ctx: tsql.Set_index_optionsContext):
        left = self._(ctx.set_index_option(0))
        right = self.repeated(ctx, tsql.Set_index_optionContext)
        return SetIndexOptions(left, right)

    def visitSet_index_option(self, ctx: tsql.Set_index_optionContext):
        allow_row_locks = self._(ctx.ALLOW_ROW_LOCKS()) is not None
        on_off = self._(ctx.on_off())
        allow_page_locks = self._(ctx.ALLOW_PAGE_LOCKS()) is not None
        optimize_for_sequential_key = self._(ctx.OPTIMIZE_FOR_SEQUENTIAL_KEY()) is not None
        ignore_dup_key = self._(ctx.IGNORE_DUP_KEY()) is not None
        statistics_norecompute = self._(ctx.STATISTICS_NORECOMPUTE()) is not None
        compression_delay = self._(ctx.COMPRESSION_DELAY()) is not None
        delay = self._(ctx.DECIMAL()) is not None
        return SetIndexOption(allow_row_locks, on_off, allow_page_locks, optimize_for_sequential_key, ignore_dup_key, statistics_norecompute, compression_delay, delay)

    def visitRebuild_partition(self, ctx: tsql.Rebuild_partitionContext):
        rebuild = self._(ctx.REBUILD()) is not None
        partition = self._(ctx.PARTITION()) is not None
        all = self._(ctx.ALL()) is not None
        rebuild_index_options = self.repeated(ctx, tsql.Rebuild_index_optionsContext)
        decimal = self._(ctx.DECIMAL()) is not None
        single_partition_rebuild_index_options = self.repeated(ctx, tsql.Single_partition_rebuild_index_optionsContext)
        return RebuildPartition(rebuild, partition, all, rebuild_index_options, decimal, single_partition_rebuild_index_options)

    def visitRebuild_index_options(self, ctx: tsql.Rebuild_index_optionsContext):
        left = self._(ctx.rebuild_index_option(0))
        right = self.repeated(ctx, tsql.Rebuild_index_optionContext)
        return RebuildIndexOptions(left, right)

    def visitRebuild_index_option(self, ctx: tsql.Rebuild_index_optionContext):
        pad_index = self._(ctx.PAD_INDEX()) is not None
        on_off = self._(ctx.on_off())
        fillfactor = self._(ctx.FILLFACTOR()) is not None
        decimal = self._(ctx.DECIMAL()) is not None
        sort_in_tempdb = self._(ctx.SORT_IN_TEMPDB()) is not None
        ignore_dup_key = self._(ctx.IGNORE_DUP_KEY()) is not None
        statistics_norecompute = self._(ctx.STATISTICS_NORECOMPUTE()) is not None
        statistics_incremental = self._(ctx.STATISTICS_INCREMENTAL()) is not None
        online = self._(ctx.ONLINE()) is not None
        on = self._(ctx.ON()) is not None
        off = self._(ctx.OFF()) is not None
        low_priority_lock_wait = self._(ctx.low_priority_lock_wait())
        resumable = self._(ctx.RESUMABLE()) is not None
        max_duration = self._(ctx.MAX_DURATION()) is not None
        allow_row_locks = self._(ctx.ALLOW_ROW_LOCKS()) is not None
        allow_page_locks = self._(ctx.ALLOW_PAGE_LOCKS()) is not None
        maxdop = self._(ctx.MAXDOP()) is not None
        data_compression = self._(ctx.DATA_COMPRESSION()) is not None
        none = self._(ctx.NONE()) is not None
        row = self._(ctx.ROW()) is not None
        page = self._(ctx.PAGE()) is not None
        columnstore = self._(ctx.COLUMNSTORE()) is not None
        columnstore_archive = self._(ctx.COLUMNSTORE_ARCHIVE()) is not None
        on_partitions = self.repeated(ctx, tsql.On_partitionsContext)
        xml_compression = self._(ctx.XML_COMPRESSION()) is not None
        return RebuildIndexOption(pad_index, on_off, fillfactor, decimal, sort_in_tempdb, ignore_dup_key, statistics_norecompute, statistics_incremental, online, on, off, low_priority_lock_wait, resumable, max_duration, allow_row_locks, allow_page_locks, maxdop, data_compression, none, row, page, columnstore, columnstore_archive, on_partitions, xml_compression)

    def visitSingle_partition_rebuild_index_options(self, ctx: tsql.Single_partition_rebuild_index_optionsContext):
        left = self._(ctx.single_partition_rebuild_index_option(0))
        right = self.repeated(ctx, tsql.Single_partition_rebuild_index_optionContext)
        return SinglePartitionRebuildIndexOptions(left, right)

    def visitSingle_partition_rebuild_index_option(self, ctx: tsql.Single_partition_rebuild_index_optionContext):
        sort_in_tempdb = self._(ctx.SORT_IN_TEMPDB()) is not None
        on_off = self._(ctx.on_off())
        maxdop = self._(ctx.MAXDOP()) is not None
        max_degree_of_parallelism = self._(ctx.DECIMAL()) is not None
        resumable = self._(ctx.RESUMABLE()) is not None
        data_compression = self._(ctx.DATA_COMPRESSION()) is not None
        none = self._(ctx.NONE()) is not None
        row = self._(ctx.ROW()) is not None
        page = self._(ctx.PAGE()) is not None
        columnstore = self._(ctx.COLUMNSTORE()) is not None
        columnstore_archive = self._(ctx.COLUMNSTORE_ARCHIVE()) is not None
        on_partitions = self.repeated(ctx, tsql.On_partitionsContext)
        xml_compression = self._(ctx.XML_COMPRESSION()) is not None
        online = self._(ctx.ONLINE()) is not None
        on = self._(ctx.ON()) is not None
        off = self._(ctx.OFF()) is not None
        low_priority_lock_wait = self._(ctx.low_priority_lock_wait())
        return SinglePartitionRebuildIndexOption(sort_in_tempdb, on_off, maxdop, max_degree_of_parallelism, resumable, data_compression, none, row, page, columnstore, columnstore_archive, on_partitions, xml_compression, online, on, off, low_priority_lock_wait)

    def visitOn_partitions(self, ctx: tsql.On_partitionsContext):
        to_partition_number = self._(ctx.DECIMAL()) is not None
        return OnPartitions(to_partition_number)

    def visitCreate_columnstore_index(self, ctx: tsql.Create_columnstore_indexContext):
        left = self._(ctx.id_(0))
        table_name = self._(ctx.table_name())
        create_columnstore_index_options = self.repeated(ctx, tsql.Create_columnstore_index_optionsContext)
        left = self._(ctx.ON()) is not None
        right = self._(ctx.id_(1))
        return CreateColumnstoreIndex(left, table_name, create_columnstore_index_options, left, right)

    def visitCreate_columnstore_index_options(self, ctx: tsql.Create_columnstore_index_optionsContext):
        left = self._(ctx.columnstore_index_option(0))
        right = self.repeated(ctx, tsql.Columnstore_index_optionContext)
        return CreateColumnstoreIndexOptions(left, right)

    def visitColumnstore_index_option(self, ctx: tsql.Columnstore_index_optionContext):
        drop_existing = self._(ctx.DROP_EXISTING()) is not None
        on_off = self._(ctx.on_off())
        maxdop = self._(ctx.MAXDOP()) is not None
        max_degree_of_parallelism = self._(ctx.DECIMAL()) is not None
        online = self._(ctx.ONLINE()) is not None
        compression_delay = self._(ctx.COMPRESSION_DELAY()) is not None
        data_compression = self._(ctx.DATA_COMPRESSION()) is not None
        columnstore = self._(ctx.COLUMNSTORE()) is not None
        columnstore_archive = self._(ctx.COLUMNSTORE_ARCHIVE()) is not None
        on_partitions = self.repeated(ctx, tsql.On_partitionsContext)
        return ColumnstoreIndexOption(drop_existing, on_off, maxdop, max_degree_of_parallelism, online, compression_delay, data_compression, columnstore, columnstore_archive, on_partitions)

    def visitCreate_nonclustered_columnstore_index(self, ctx: tsql.Create_nonclustered_columnstore_indexContext):
        left = self._(ctx.id_(0))
        table_name = self._(ctx.table_name())
        column_name_list_with_order = self._(ctx.column_name_list_with_order())
        where = self._(ctx.WHERE()) is not None
        search_condition = self._(ctx.search_condition())
        create_columnstore_index_options = self.repeated(ctx, tsql.Create_columnstore_index_optionsContext)
        left = self._(ctx.ON()) is not None
        right = self._(ctx.id_(1))
        return CreateNonclusteredColumnstoreIndex(left, table_name, column_name_list_with_order, where, search_condition, create_columnstore_index_options, left, right)

    def visitCreate_xml_index(self, ctx: tsql.Create_xml_indexContext):
        left = self._(ctx.id_(0))
        table_name = self._(ctx.table_name())
        right = self._(ctx.id_(1))
        using = self._(ctx.USING()) is not None
        left = self._(ctx.XML()) is not None
        left = self._(ctx.INDEX()) is not None
        third = self._(ctx.id_(2))
        xml_index_options = self.repeated(ctx, tsql.Xml_index_optionsContext)
        for_ = self._(ctx.FOR()) is not None
        value = self._(ctx.VALUE()) is not None
        path = self._(ctx.PATH()) is not None
        property = self._(ctx.PROPERTY()) is not None
        return CreateXmlIndex(left, table_name, right, using, left, left, third, xml_index_options, for_, value, path, property)

    def visitXml_index_options(self, ctx: tsql.Xml_index_optionsContext):
        left = self._(ctx.xml_index_option(0))
        right = self.repeated(ctx, tsql.Xml_index_optionContext)
        return XmlIndexOptions(left, right)

    def visitXml_index_option(self, ctx: tsql.Xml_index_optionContext):
        pad_index = self._(ctx.PAD_INDEX()) is not None
        on_off = self._(ctx.on_off())
        fillfactor = self._(ctx.FILLFACTOR()) is not None
        decimal = self._(ctx.DECIMAL()) is not None
        sort_in_tempdb = self._(ctx.SORT_IN_TEMPDB()) is not None
        ignore_dup_key = self._(ctx.IGNORE_DUP_KEY()) is not None
        drop_existing = self._(ctx.DROP_EXISTING()) is not None
        online = self._(ctx.ONLINE()) is not None
        on = self._(ctx.ON()) is not None
        off = self._(ctx.OFF()) is not None
        low_priority_lock_wait = self._(ctx.low_priority_lock_wait())
        allow_row_locks = self._(ctx.ALLOW_ROW_LOCKS()) is not None
        allow_page_locks = self._(ctx.ALLOW_PAGE_LOCKS()) is not None
        maxdop = self._(ctx.MAXDOP()) is not None
        xml_compression = self._(ctx.XML_COMPRESSION()) is not None
        return XmlIndexOption(pad_index, on_off, fillfactor, decimal, sort_in_tempdb, ignore_dup_key, drop_existing, online, on, off, low_priority_lock_wait, allow_row_locks, allow_page_locks, maxdop, xml_compression)

    def visitCreate_or_alter_procedure(self, ctx: tsql.Create_or_alter_procedureContext):
        left = self._(ctx.ALTER()) is not None
        create_or_alter_procedure_proc = self._(ctx.create_or_alter_procedure_proc())
        proc_name = self._(ctx.func_proc_name_schema())
        decimal = self._(ctx.DECIMAL()) is not None
        left = self._(ctx.procedure_param(0))
        with_ = self._(ctx.WITH()) is not None
        left = self._(ctx.procedure_option(0))
        for_ = self._(ctx.FOR()) is not None
        replication = self._(ctx.REPLICATION()) is not None
        as_external_name = self._(ctx.as_external_name())
        sql_clauses = self._(ctx.sql_clauses())
        create = self._(ctx.CREATE()) is not None
        right = self.repeated(ctx, tsql.Procedure_paramContext)
        right = self.repeated(ctx, tsql.Procedure_optionContext)
        or_ = self._(ctx.OR()) is not None
        right = self._(ctx.ALTER()) is not None
        replace = self._(ctx.REPLACE()) is not None
        return CreateOrAlterProcedure(left, create_or_alter_procedure_proc, proc_name, decimal, left, with_, left, for_, replication, as_external_name, sql_clauses, create, right, right, or_, right, replace)

    def visitAs_external_name(self, ctx: tsql.As_external_nameContext):
        assembly_name = self._(ctx.id_())
        return AsExternalName(assembly_name)

    def visitCreate_or_alter_trigger(self, ctx: tsql.Create_or_alter_triggerContext):
        create_or_alter_dml_trigger = self._(ctx.create_or_alter_dml_trigger())
        create_or_alter_ddl_trigger = self._(ctx.create_or_alter_ddl_trigger())
        return CreateOrAlterTrigger(create_or_alter_dml_trigger, create_or_alter_ddl_trigger)

    def visitCreate_or_alter_dml_trigger(self, ctx: tsql.Create_or_alter_dml_triggerContext):
        create = self._(ctx.CREATE()) is not None
        left = self._(ctx.ALTER()) is not None
        simple_name = self._(ctx.simple_name())
        table_name = self._(ctx.table_name())
        left = self._(ctx.WITH()) is not None
        left = self._(ctx.dml_trigger_option(0))
        left = self._(ctx.FOR()) is not None
        after = self._(ctx.AFTER()) is not None
        instead = self._(ctx.INSTEAD()) is not None
        of = self._(ctx.OF()) is not None
        left = self._(ctx.dml_trigger_operation(0))
        right = self.repeated(ctx, tsql.Dml_trigger_operationContext)
        right = self._(ctx.WITH()) is not None
        append_ = self._(ctx.APPEND()) is not None
        not_ = self._(ctx.NOT()) is not None
        right = self._(ctx.FOR()) is not None
        replication = self._(ctx.REPLICATION()) is not None
        sql_clauses = self._(ctx.sql_clauses())
        or_ = self._(ctx.OR()) is not None
        right = self.repeated(ctx, tsql.Dml_trigger_optionContext)
        right = self._(ctx.ALTER()) is not None
        replace = self._(ctx.REPLACE()) is not None
        return CreateOrAlterDmlTrigger(create, left, simple_name, table_name, left, left, left, after, instead, of, left, right, right, append_, not_, right, replication, sql_clauses, or_, right, right, replace)

    def visitDml_trigger_option(self, ctx: tsql.Dml_trigger_optionContext):
        encryption = self._(ctx.ENCRYPTION()) is not None
        execute_clause = self._(ctx.execute_clause())
        return DmlTriggerOption(encryption, execute_clause)

    def visitDml_trigger_operation(self, ctx: tsql.Dml_trigger_operationContext):
        insert = self._(ctx.INSERT()) is not None
        update = self._(ctx.UPDATE()) is not None
        delete = self._(ctx.DELETE()) is not None
        return DmlTriggerOperation(insert, update, delete)

    def visitCreate_or_alter_ddl_trigger(self, ctx: tsql.Create_or_alter_ddl_triggerContext):
        create = self._(ctx.CREATE()) is not None
        left = self._(ctx.ALTER()) is not None
        simple_name = self._(ctx.simple_name())
        all = self._(ctx.ALL()) is not None
        server = self._(ctx.SERVER()) is not None
        database = self._(ctx.DATABASE()) is not None
        with_ = self._(ctx.WITH()) is not None
        left = self._(ctx.dml_trigger_option(0))
        for_ = self._(ctx.FOR()) is not None
        after = self._(ctx.AFTER()) is not None
        left = self._(ctx.ddl_trigger_operation(0))
        right = self.repeated(ctx, tsql.Ddl_trigger_operationContext)
        sql_clauses = self._(ctx.sql_clauses())
        or_ = self._(ctx.OR()) is not None
        right = self.repeated(ctx, tsql.Dml_trigger_optionContext)
        right = self._(ctx.ALTER()) is not None
        replace = self._(ctx.REPLACE()) is not None
        return CreateOrAlterDdlTrigger(create, left, simple_name, all, server, database, with_, left, for_, after, left, right, sql_clauses, or_, right, right, replace)

    def visitCreate_or_alter_function(self, ctx: tsql.Create_or_alter_functionContext):
        left = self._(ctx.ALTER()) is not None
        func_name = self._(ctx.func_proc_name_schema())
        func_body_returns_select = self._(ctx.func_body_returns_select())
        func_body_returns_table = self._(ctx.func_body_returns_table())
        func_body_returns_scalar = self._(ctx.func_body_returns_scalar())
        create = self._(ctx.CREATE()) is not None
        left = self._(ctx.procedure_param(0))
        or_ = self._(ctx.OR()) is not None
        right = self._(ctx.ALTER()) is not None
        right = self.repeated(ctx, tsql.Procedure_paramContext)
        return CreateOrAlterFunction(left, func_name, func_body_returns_select, func_body_returns_table, func_body_returns_scalar, create, left, or_, right, right)

    def visitFunc_body_returns_select(self, ctx: tsql.Func_body_returns_selectContext):
        with_ = self._(ctx.WITH()) is not None
        left = self._(ctx.function_option(0))
        as_external_name = self._(ctx.as_external_name())
        return_ = self._(ctx.RETURN()) is not None
        right = self.repeated(ctx, tsql.Function_optionContext)
        left = self._(ctx.select_statement_standalone(0))
        right = self._(ctx.select_statement_standalone(1))
        return FuncBodyReturnsSelect(with_, left, as_external_name, return_, right, left, right)

    def visitFunc_body_returns_table(self, ctx: tsql.Func_body_returns_tableContext):
        local_id = self._(ctx.LOCAL_ID())
        table_type_definition = self._(ctx.table_type_definition())
        with_ = self._(ctx.WITH()) is not None
        left = self._(ctx.function_option(0))
        as_external_name = self._(ctx.as_external_name())
        begin = self._(ctx.BEGIN()) is not None
        sql_clauses = self._(ctx.sql_clauses())
        return_ = self._(ctx.RETURN()) is not None
        end = self._(ctx.END()) is not None
        right = self.repeated(ctx, tsql.Function_optionContext)
        return FuncBodyReturnsTable(local_id, table_type_definition, with_, left, as_external_name, begin, sql_clauses, return_, end, right)

    def visitFunc_body_returns_scalar(self, ctx: tsql.Func_body_returns_scalarContext):
        data_type = self._(ctx.data_type())
        with_ = self._(ctx.WITH()) is not None
        left = self._(ctx.function_option(0))
        as_external_name = self._(ctx.as_external_name())
        begin = self._(ctx.BEGIN()) is not None
        sql_clauses = self._(ctx.sql_clauses())
        return_ = self._(ctx.RETURN()) is not None
        ret = self._(ctx.expression())
        end = self._(ctx.END()) is not None
        right = self.repeated(ctx, tsql.Function_optionContext)
        return FuncBodyReturnsScalar(data_type, with_, left, as_external_name, begin, sql_clauses, return_, ret, end, right)

    def visitProcedure_param_default_value(self, ctx: tsql.Procedure_param_default_valueContext):
        null = self._(ctx.NULL_()) is not None
        default_ = self._(ctx.DEFAULT()) is not None
        constant = self._(ctx.constant())
        local_id = self._(ctx.LOCAL_ID())
        return ProcedureParamDefaultValue(null, default_, constant, local_id)

    def visitProcedure_param(self, ctx: tsql.Procedure_paramContext):
        local_id = self._(ctx.LOCAL_ID())
        type_schema = self._(ctx.id_())
        data_type = self._(ctx.data_type())
        default_val = self._(ctx.procedure_param_default_value())
        out = self._(ctx.OUT()) is not None
        output = self._(ctx.OUTPUT()) is not None
        readonly = self._(ctx.READONLY()) is not None
        return ProcedureParam(local_id, type_schema, data_type, default_val, out, output, readonly)

    def visitProcedure_option(self, ctx: tsql.Procedure_optionContext):
        encryption = self._(ctx.ENCRYPTION()) is not None
        recompile = self._(ctx.RECOMPILE()) is not None
        execute_clause = self._(ctx.execute_clause())
        return ProcedureOption(encryption, recompile, execute_clause)

    def visitFunction_option(self, ctx: tsql.Function_optionContext):
        encryption = self._(ctx.ENCRYPTION()) is not None
        schemabinding = self._(ctx.SCHEMABINDING()) is not None
        returns = self._(ctx.RETURNS()) is not None
        left = self._(ctx.NULL_()) is not None
        on = self._(ctx.ON()) is not None
        right = self._(ctx.NULL_()) is not None
        input = self._(ctx.INPUT()) is not None
        called = self._(ctx.CALLED()) is not None
        execute_clause = self._(ctx.execute_clause())
        return FunctionOption(encryption, schemabinding, returns, left, on, right, input, called, execute_clause)

    def visitCreate_statistics(self, ctx: tsql.Create_statisticsContext):
        id = self._(ctx.id_())
        table_name = self._(ctx.table_name())
        column_name_list = self._(ctx.column_name_list())
        with_ = self._(ctx.WITH()) is not None
        fullscan = self._(ctx.FULLSCAN()) is not None
        sample = self._(ctx.SAMPLE()) is not None
        decimal = self._(ctx.DECIMAL()) is not None
        stats_stream = self._(ctx.STATS_STREAM()) is not None
        norecompute = self._(ctx.NORECOMPUTE()) is not None
        incremental = self._(ctx.INCREMENTAL()) is not None
        equal = self._(ctx.EQUAL()) is not None
        on_off = self._(ctx.on_off())
        percent = self._(ctx.PERCENT()) is not None
        rows = self._(ctx.ROWS()) is not None
        return CreateStatistics(id, table_name, column_name_list, with_, fullscan, sample, decimal, stats_stream, norecompute, incremental, equal, on_off, percent, rows)

    def visitUpdate_statistics(self, ctx: tsql.Update_statisticsContext):
        full_table_name = self._(ctx.full_table_name())
        left = self._(ctx.id_(0))
        right = self._(ctx.id_(1))
        update_statistics_options = self.repeated(ctx, tsql.Update_statistics_optionsContext)
        third = self.repeated(ctx, tsql.Id_Context)
        return UpdateStatistics(full_table_name, left, right, update_statistics_options, third)

    def visitUpdate_statistics_options(self, ctx: tsql.Update_statistics_optionsContext):
        left = self._(ctx.update_statistics_option(0))
        right = self.repeated(ctx, tsql.Update_statistics_optionContext)
        return UpdateStatisticsOptions(left, right)

    def visitUpdate_statistics_option(self, ctx: tsql.Update_statistics_optionContext):
        fullscan = self._(ctx.FULLSCAN()) is not None
        persist_sample_percent = self._(ctx.PERSIST_SAMPLE_PERCENT()) is not None
        on_off = self._(ctx.on_off())
        sample = self._(ctx.SAMPLE()) is not None
        number = self._(ctx.DECIMAL()) is not None
        percent = self._(ctx.PERCENT()) is not None
        rows = self._(ctx.ROWS()) is not None
        resample = self._(ctx.RESAMPLE()) is not None
        on_partitions = self.repeated(ctx, tsql.On_partitionsContext)
        stats_stream = self._(ctx.STATS_STREAM()) is not None
        stats_stream = self._(ctx.expression())
        rowcount = self._(ctx.ROWCOUNT()) is not None
        pagecount = self._(ctx.PAGECOUNT()) is not None
        all = self._(ctx.ALL()) is not None
        columns = self._(ctx.COLUMNS()) is not None
        index = self._(ctx.INDEX()) is not None
        norecompute = self._(ctx.NORECOMPUTE()) is not None
        incremental = self._(ctx.INCREMENTAL()) is not None
        maxdop = self._(ctx.MAXDOP()) is not None
        auto_drop = self._(ctx.AUTO_DROP()) is not None
        return UpdateStatisticsOption(fullscan, persist_sample_percent, on_off, sample, number, percent, rows, resample, on_partitions, stats_stream, stats_stream, rowcount, pagecount, all, columns, index, norecompute, incremental, maxdop, auto_drop)

    def visitCreate_table(self, ctx: tsql.Create_tableContext):
        table_name = self._(ctx.table_name())
        column_def_table_constraints = self._(ctx.column_def_table_constraints())
        table_indices = self.repeated(ctx, tsql.Table_indicesContext)
        lock = self._(ctx.LOCK()) is not None
        simple_id = self._(ctx.simple_id())
        table_options = self.repeated(ctx, tsql.Table_optionsContext)
        on = self._(ctx.ON()) is not None
        left = self._(ctx.id_(0))
        left = self._(ctx.DEFAULT()) is not None
        on_partition_or_filegroup = self._(ctx.on_partition_or_filegroup())
        textimage_on = self._(ctx.TEXTIMAGE_ON()) is not None
        right = self._(ctx.id_(1))
        right = self._(ctx.DEFAULT()) is not None
        return CreateTable(table_name, column_def_table_constraints, table_indices, lock, simple_id, table_options, on, left, left, on_partition_or_filegroup, textimage_on, right, right)

    def visitTable_indices(self, ctx: tsql.Table_indicesContext):
        index = self._(ctx.INDEX()) is not None
        id = self._(ctx.id_(0))
        clustered = self.repeated(ctx, tsql.ClusteredContext)
        column_name_list_with_order = self._(ctx.column_name_list_with_order())
        clustered = self._(ctx.CLUSTERED()) is not None
        columnstore = self._(ctx.COLUMNSTORE()) is not None
        column_name_list = self._(ctx.column_name_list())
        create_table_index_options = self.repeated(ctx, tsql.Create_table_index_optionsContext)
        on = self._(ctx.ON()) is not None
        right = self._(ctx.id_(1))
        return TableIndices(index, id, clustered, column_name_list_with_order, clustered, columnstore, column_name_list, create_table_index_options, on, right)

    def visitTable_options(self, ctx: tsql.Table_optionsContext):
        left = self._(ctx.table_option(0))
        right = self._(ctx.table_option(1))
        third = self.repeated(ctx, tsql.Table_optionContext)
        fourth = self.repeated(ctx, tsql.Table_optionContext)
        return TableOptions(left, right, third, fourth)

    def visitTable_option(self, ctx: tsql.Table_optionContext):
        left = self._(ctx.simple_id(0))
        left = self._(ctx.keyword(0))
        right = self._(ctx.simple_id(1))
        right = self._(ctx.keyword(1))
        on_off = self._(ctx.on_off())
        decimal = self._(ctx.DECIMAL()) is not None
        clustered = self._(ctx.CLUSTERED()) is not None
        columnstore = self._(ctx.COLUMNSTORE()) is not None
        index = self._(ctx.INDEX()) is not None
        heap = self._(ctx.HEAP()) is not None
        fillfactor = self._(ctx.FILLFACTOR()) is not None
        distribution = self._(ctx.DISTRIBUTION()) is not None
        hash = self._(ctx.HASH()) is not None
        id = self._(ctx.id_(0))
        left = self._(ctx.ASC()) is not None
        left = self._(ctx.DESC()) is not None
        right = self.repeated(ctx, tsql.Id_Context)
        right = self._(ctx.ASC()) is not None
        right = self._(ctx.DESC()) is not None
        data_compression = self._(ctx.DATA_COMPRESSION()) is not None
        none = self._(ctx.NONE()) is not None
        row = self._(ctx.ROW()) is not None
        page = self._(ctx.PAGE()) is not None
        on_partitions = self.repeated(ctx, tsql.On_partitionsContext)
        xml_compression = self._(ctx.XML_COMPRESSION()) is not None
        return TableOption(left, left, right, right, on_off, decimal, clustered, columnstore, index, heap, fillfactor, distribution, hash, id, left, left, right, right, right, data_compression, none, row, page, on_partitions, xml_compression)

    def visitCreate_table_index_options(self, ctx: tsql.Create_table_index_optionsContext):
        left = self._(ctx.create_table_index_option(0))
        right = self.repeated(ctx, tsql.Create_table_index_optionContext)
        return CreateTableIndexOptions(left, right)

    def visitCreate_table_index_option(self, ctx: tsql.Create_table_index_optionContext):
        pad_index = self._(ctx.PAD_INDEX()) is not None
        on_off = self._(ctx.on_off())
        fillfactor = self._(ctx.FILLFACTOR()) is not None
        decimal = self._(ctx.DECIMAL()) is not None
        ignore_dup_key = self._(ctx.IGNORE_DUP_KEY()) is not None
        statistics_norecompute = self._(ctx.STATISTICS_NORECOMPUTE()) is not None
        statistics_incremental = self._(ctx.STATISTICS_INCREMENTAL()) is not None
        allow_row_locks = self._(ctx.ALLOW_ROW_LOCKS()) is not None
        allow_page_locks = self._(ctx.ALLOW_PAGE_LOCKS()) is not None
        optimize_for_sequential_key = self._(ctx.OPTIMIZE_FOR_SEQUENTIAL_KEY()) is not None
        data_compression = self._(ctx.DATA_COMPRESSION()) is not None
        none = self._(ctx.NONE()) is not None
        row = self._(ctx.ROW()) is not None
        page = self._(ctx.PAGE()) is not None
        columnstore = self._(ctx.COLUMNSTORE()) is not None
        columnstore_archive = self._(ctx.COLUMNSTORE_ARCHIVE()) is not None
        on_partitions = self.repeated(ctx, tsql.On_partitionsContext)
        xml_compression = self._(ctx.XML_COMPRESSION()) is not None
        return CreateTableIndexOption(pad_index, on_off, fillfactor, decimal, ignore_dup_key, statistics_norecompute, statistics_incremental, allow_row_locks, allow_page_locks, optimize_for_sequential_key, data_compression, none, row, page, columnstore, columnstore_archive, on_partitions, xml_compression)

    def visitCreate_view(self, ctx: tsql.Create_viewContext):
        create = self._(ctx.CREATE()) is not None
        left = self._(ctx.ALTER()) is not None
        simple_name = self._(ctx.simple_name())
        column_name_list = self._(ctx.column_name_list())
        left = self._(ctx.WITH()) is not None
        left = self._(ctx.view_attribute(0))
        select_statement_standalone = self._(ctx.select_statement_standalone())
        right = self._(ctx.WITH()) is not None
        check = self._(ctx.CHECK()) is not None
        option = self._(ctx.OPTION()) is not None
        or_ = self._(ctx.OR()) is not None
        right = self.repeated(ctx, tsql.View_attributeContext)
        right = self._(ctx.ALTER()) is not None
        replace = self._(ctx.REPLACE()) is not None
        return CreateView(create, left, simple_name, column_name_list, left, left, select_statement_standalone, right, check, option, or_, right, right, replace)

    def visitView_attribute(self, ctx: tsql.View_attributeContext):
        encryption = self._(ctx.ENCRYPTION()) is not None
        schemabinding = self._(ctx.SCHEMABINDING()) is not None
        view_metadata = self._(ctx.VIEW_METADATA()) is not None
        return ViewAttribute(encryption, schemabinding, view_metadata)

    def visitAlter_table(self, ctx: tsql.Alter_tableContext):
        left = self._(ctx.table_name(0))
        set = self._(ctx.SET()) is not None
        lock_escalation = self._(ctx.LOCK_ESCALATION()) is not None
        left = self._(ctx.ADD()) is not None
        column_def_table_constraints = self._(ctx.column_def_table_constraints())
        left = self._(ctx.ALTER()) is not None
        left = self._(ctx.COLUMN()) is not None
        left = self._(ctx.DROP()) is not None
        right = self._(ctx.COLUMN()) is not None
        left = self._(ctx.id_(0))
        right = self._(ctx.DROP()) is not None
        left = self._(ctx.CONSTRAINT()) is not None
        constraint = self._(ctx.id_(1))
        with_ = self._(ctx.WITH()) is not None
        right = self._(ctx.ADD()) is not None
        right = self._(ctx.CONSTRAINT()) is not None
        constraint = self._(ctx.id_(2))
        trigger = self._(ctx.TRIGGER()) is not None
        fourth = self._(ctx.id_(3))
        rebuild = self._(ctx.REBUILD()) is not None
        table_options = self._(ctx.table_options())
        switch_ = self._(ctx.SWITCH()) is not None
        switch_partition = self._(ctx.switch_partition())
        auto = self._(ctx.AUTO()) is not None
        left = self._(ctx.TABLE()) is not None
        left = self._(ctx.DISABLE()) is not None
        column_definition = self._(ctx.column_definition())
        column_modifier = self._(ctx.column_modifier())
        fifth = self.repeated(ctx, tsql.Id_Context)
        left = self._(ctx.CHECK()) is not None
        left = self._(ctx.NOCHECK()) is not None
        third = self._(ctx.CONSTRAINT()) is not None
        constraint = self._(ctx.id_(5))
        foreign = self._(ctx.FOREIGN()) is not None
        key = self._(ctx.KEY()) is not None
        fk = self._(ctx.column_name_list())
        references = self._(ctx.REFERENCES()) is not None
        right = self._(ctx.table_name(1))
        right = self._(ctx.CHECK()) is not None
        search_condition = self._(ctx.search_condition())
        right = self._(ctx.NOCHECK()) is not None
        third = self._(ctx.CHECK()) is not None
        enable = self._(ctx.ENABLE()) is not None
        right = self._(ctx.DISABLE()) is not None
        on_delete = self.repeated(ctx, tsql.On_deleteContext)
        on_update = self.repeated(ctx, tsql.On_updateContext)
        return AlterTable(left, set, lock_escalation, left, column_def_table_constraints, left, left, left, right, left, right, left, constraint, with_, right, right, constraint, trigger, fourth, rebuild, table_options, switch_, switch_partition, auto, left, left, column_definition, column_modifier, fifth, left, left, third, constraint, foreign, key, fk, references, right, right, search_condition, right, third, enable, right, on_delete, on_update)

    def visitSwitch_partition(self, ctx: tsql.Switch_partitionContext):
        left = self._(ctx.PARTITION()) is not None
        source_partition_number_expression = self._(ctx.expression())
        target_table = self._(ctx.table_name())
        right = self._(ctx.PARTITION()) is not None
        with_ = self._(ctx.WITH()) is not None
        low_priority_lock_wait = self._(ctx.low_priority_lock_wait())
        return SwitchPartition(left, source_partition_number_expression, target_table, right, with_, low_priority_lock_wait)

    def visitLow_priority_lock_wait(self, ctx: tsql.Low_priority_lock_waitContext):
        max_duration = self._(ctx.time())
        low_priority_lock_wait_abort_after_wait = self._(ctx.low_priority_lock_wait_abort_after_wait())
        return LowPriorityLockWait(max_duration, low_priority_lock_wait_abort_after_wait)

    def visitAlter_database(self, ctx: tsql.Alter_databaseContext):
        database = self._(ctx.id_())
        current = self._(ctx.CURRENT()) is not None
        modify = self._(ctx.MODIFY()) is not None
        name = self._(ctx.NAME()) is not None
        collate = self._(ctx.COLLATE()) is not None
        set = self._(ctx.SET()) is not None
        database_optionspec = self._(ctx.database_optionspec())
        add_or_modify_files = self._(ctx.add_or_modify_files())
        add_or_modify_filegroups = self._(ctx.add_or_modify_filegroups())
        with_ = self._(ctx.WITH()) is not None
        termination = self._(ctx.termination())
        return AlterDatabase(database, current, modify, name, collate, set, database_optionspec, add_or_modify_files, add_or_modify_filegroups, with_, termination)

    def visitAdd_or_modify_files(self, ctx: tsql.Add_or_modify_filesContext):
        add = self._(ctx.ADD()) is not None
        file = self._(ctx.FILE()) is not None
        left = self._(ctx.filespec(0))
        right = self.repeated(ctx, tsql.FilespecContext)
        to = self._(ctx.TO()) is not None
        filegroup = self._(ctx.FILEGROUP()) is not None
        filegroup_name = self._(ctx.id_())
        log = self._(ctx.LOG()) is not None
        remove = self._(ctx.REMOVE()) is not None
        modify = self._(ctx.MODIFY()) is not None
        return AddOrModifyFiles(add, file, left, right, to, filegroup, filegroup_name, log, remove, modify)

    def visitFilespec(self, ctx: tsql.FilespecContext):
        name = self._(ctx.id_or_string())
        newname = self._(ctx.NEWNAME()) is not None
        filename = self._(ctx.FILENAME()) is not None
        file_name = self._(ctx.STRING())
        size = self._(ctx.SIZE()) is not None
        size = self._(ctx.file_size())
        maxsize = self._(ctx.MAXSIZE()) is not None
        unlimited = self._(ctx.UNLIMITED()) is not None
        filegrowth = self._(ctx.FILEGROWTH()) is not None
        offline = self._(ctx.OFFLINE()) is not None
        return Filespec(name, newname, filename, file_name, size, size, maxsize, unlimited, filegrowth, offline)

    def visitAdd_or_modify_filegroups(self, ctx: tsql.Add_or_modify_filegroupsContext):
        add = self._(ctx.ADD()) is not None
        filegroup = self._(ctx.FILEGROUP()) is not None
        filegroup_name = self._(ctx.id_())
        left = self._(ctx.CONTAINS()) is not None
        filestream = self._(ctx.FILESTREAM()) is not None
        right = self._(ctx.CONTAINS()) is not None
        memory_optimized_data = self._(ctx.MEMORY_OPTIMIZED_DATA()) is not None
        remove = self._(ctx.REMOVE()) is not None
        modify = self._(ctx.MODIFY()) is not None
        filegroup_updatability_option = self._(ctx.filegroup_updatability_option())
        default_ = self._(ctx.DEFAULT()) is not None
        name = self._(ctx.NAME()) is not None
        autogrow_single_file = self._(ctx.AUTOGROW_SINGLE_FILE()) is not None
        autogrow_all_files = self._(ctx.AUTOGROW_ALL_FILES()) is not None
        return AddOrModifyFilegroups(add, filegroup, filegroup_name, left, filestream, right, memory_optimized_data, remove, modify, filegroup_updatability_option, default_, name, autogrow_single_file, autogrow_all_files)

    def visitFilegroup_updatability_option(self, ctx: tsql.Filegroup_updatability_optionContext):
        readonly = self._(ctx.READONLY()) is not None
        readwrite = self._(ctx.READWRITE()) is not None
        read_only = self._(ctx.READ_ONLY()) is not None
        read_write = self._(ctx.READ_WRITE()) is not None
        return FilegroupUpdatabilityOption(readonly, readwrite, read_only, read_write)

    def visitDatabase_optionspec(self, ctx: tsql.Database_optionspecContext):
        auto_option = self._(ctx.auto_option())
        change_tracking_option = self._(ctx.change_tracking_option())
        containment_option = self._(ctx.containment_option())
        cursor_option = self._(ctx.cursor_option())
        database_mirroring_option = self._(ctx.database_mirroring_option())
        date_correlation_optimization_option = self._(ctx.date_correlation_optimization_option())
        db_encryption_option = self._(ctx.db_encryption_option())
        db_state_option = self._(ctx.db_state_option())
        db_update_option = self._(ctx.db_update_option())
        db_user_access_option = self._(ctx.db_user_access_option())
        delayed_durability_option = self._(ctx.delayed_durability_option())
        external_access_option = self._(ctx.external_access_option())
        filestream = self._(ctx.FILESTREAM()) is not None
        database_filestream_option = self._(ctx.database_filestream_option())
        hadr_options = self._(ctx.hadr_options())
        mixed_page_allocation_option = self._(ctx.mixed_page_allocation_option())
        parameterization_option = self._(ctx.parameterization_option())
        recovery_option = self._(ctx.recovery_option())
        service_broker_option = self._(ctx.service_broker_option())
        snapshot_option = self._(ctx.snapshot_option())
        sql_option = self._(ctx.sql_option())
        target_recovery_time_option = self._(ctx.target_recovery_time_option())
        termination = self._(ctx.termination())
        return DatabaseOptionspec(auto_option, change_tracking_option, containment_option, cursor_option, database_mirroring_option, date_correlation_optimization_option, db_encryption_option, db_state_option, db_update_option, db_user_access_option, delayed_durability_option, external_access_option, filestream, database_filestream_option, hadr_options, mixed_page_allocation_option, parameterization_option, recovery_option, service_broker_option, snapshot_option, sql_option, target_recovery_time_option, termination)

    def visitAuto_option(self, ctx: tsql.Auto_optionContext):
        auto_close = self._(ctx.AUTO_CLOSE()) is not None
        on_off = self._(ctx.on_off())
        auto_create_statistics = self._(ctx.AUTO_CREATE_STATISTICS()) is not None
        off = self._(ctx.OFF()) is not None
        left = self._(ctx.ON()) is not None
        incremental = self._(ctx.INCREMENTAL()) is not None
        equal = self._(ctx.EQUAL()) is not None
        right = self._(ctx.ON()) is not None
        auto_shrink = self._(ctx.AUTO_SHRINK()) is not None
        auto_update_statistics = self._(ctx.AUTO_UPDATE_STATISTICS()) is not None
        auto_update_statistics_async = self._(ctx.AUTO_UPDATE_STATISTICS_ASYNC()) is not None
        return AutoOption(auto_close, on_off, auto_create_statistics, off, left, incremental, equal, right, auto_shrink, auto_update_statistics, auto_update_statistics_async)

    def visitChange_tracking_option(self, ctx: tsql.Change_tracking_optionContext):
        off = self._(ctx.OFF()) is not None
        on = self._(ctx.ON()) is not None
        left = self.repeated(ctx, tsql.Change_tracking_option_listContext)
        right = self.repeated(ctx, tsql.Change_tracking_option_listContext)
        return ChangeTrackingOption(off, on, left, right)

    def visitChange_tracking_option_list(self, ctx: tsql.Change_tracking_option_listContext):
        auto_cleanup = self._(ctx.AUTO_CLEANUP()) is not None
        equal = self._(ctx.EQUAL()) is not None
        on_off = self._(ctx.on_off())
        change_retention = self._(ctx.CHANGE_RETENTION()) is not None
        decimal = self._(ctx.DECIMAL()) is not None
        days = self._(ctx.DAYS()) is not None
        hours = self._(ctx.HOURS()) is not None
        minutes = self._(ctx.MINUTES()) is not None
        return ChangeTrackingOptionList(auto_cleanup, equal, on_off, change_retention, decimal, days, hours, minutes)

    def visitContainment_option(self, ctx: tsql.Containment_optionContext):
        none = self._(ctx.NONE()) is not None
        partial = self._(ctx.PARTIAL()) is not None
        return ContainmentOption(none, partial)

    def visitCursor_option(self, ctx: tsql.Cursor_optionContext):
        cursor_close_on_commit = self._(ctx.CURSOR_CLOSE_ON_COMMIT()) is not None
        on_off = self._(ctx.on_off())
        cursor_default = self._(ctx.CURSOR_DEFAULT()) is not None
        local = self._(ctx.LOCAL()) is not None
        global_ = self._(ctx.GLOBAL()) is not None
        return CursorOption(cursor_close_on_commit, on_off, cursor_default, local, global_)

    def visitAlter_endpoint(self, ctx: tsql.Alter_endpointContext):
        endpointname = self._(ctx.id_())
        authorization = self._(ctx.AUTHORIZATION()) is not None
        state = self._(ctx.STATE()) is not None
        left = self._(ctx.EQUAL()) is not None
        alter_endpoint_state = self._(ctx.alter_endpoint_state())
        endpoint_listener_clause = self._(ctx.endpoint_listener_clause())
        left = self._(ctx.FOR()) is not None
        tsql = self._(ctx.TSQL()) is not None
        left = self._(ctx.LR_BRACKET()) is not None
        left = self._(ctx.RR_BRACKET()) is not None
        right = self._(ctx.FOR()) is not None
        service_broker = self._(ctx.SERVICE_BROKER()) is not None
        right = self._(ctx.LR_BRACKET()) is not None
        left = self._(ctx.endpoint_authentication_clause(0))
        right = self._(ctx.RR_BRACKET()) is not None
        third = self._(ctx.FOR()) is not None
        database_mirroring = self._(ctx.DATABASE_MIRRORING()) is not None
        third = self._(ctx.LR_BRACKET()) is not None
        right = self._(ctx.endpoint_authentication_clause(1))
        left = self._(ctx.COMMA()) is not None
        role = self._(ctx.ROLE()) is not None
        right = self._(ctx.EQUAL()) is not None
        third = self._(ctx.RR_BRACKET()) is not None
        right = self._(ctx.COMMA()) is not None
        left = self._(ctx.endpoint_encryption_alogorithm_clause(0))
        third = self._(ctx.COMMA()) is not None
        message_forwarding = self._(ctx.MESSAGE_FORWARDING()) is not None
        third = self._(ctx.EQUAL()) is not None
        fourth = self._(ctx.COMMA()) is not None
        message_forward_size = self._(ctx.MESSAGE_FORWARD_SIZE()) is not None
        fourth = self._(ctx.EQUAL()) is not None
        decimal = self._(ctx.DECIMAL()) is not None
        fifth = self._(ctx.COMMA()) is not None
        right = self._(ctx.endpoint_encryption_alogorithm_clause(1))
        witness = self._(ctx.WITNESS()) is not None
        partner = self._(ctx.PARTNER()) is not None
        all = self._(ctx.ALL()) is not None
        enabled = self._(ctx.ENABLED()) is not None
        disabled = self._(ctx.DISABLED()) is not None
        return AlterEndpoint(endpointname, authorization, state, left, alter_endpoint_state, endpoint_listener_clause, left, tsql, left, left, right, service_broker, right, left, right, third, database_mirroring, third, right, left, role, right, third, right, left, third, message_forwarding, third, fourth, message_forward_size, fourth, decimal, fifth, right, witness, partner, all, enabled, disabled)

    def visitMirroring_set_option(self, ctx: tsql.Mirroring_set_optionContext):
        partner_option = self._(ctx.partner_option())
        witness_option = self._(ctx.witness_option())
        return MirroringSetOption(partner_option, witness_option)

    def visitPartner_option(self, ctx: tsql.Partner_optionContext):
        partner_server = self._(ctx.partner_server())
        failover = self._(ctx.FAILOVER()) is not None
        force_service_allow_data_loss = self._(ctx.FORCE_SERVICE_ALLOW_DATA_LOSS()) is not None
        off = self._(ctx.OFF()) is not None
        resume = self._(ctx.RESUME()) is not None
        safety = self._(ctx.SAFETY()) is not None
        full = self._(ctx.FULL()) is not None
        suspend = self._(ctx.SUSPEND()) is not None
        timeout = self._(ctx.TIMEOUT()) is not None
        decimal = self._(ctx.DECIMAL()) is not None
        return PartnerOption(partner_server, failover, force_service_allow_data_loss, off, resume, safety, full, suspend, timeout, decimal)

    def visitWitness_option(self, ctx: tsql.Witness_optionContext):
        witness_server = self._(ctx.witness_server())
        off = self._(ctx.OFF()) is not None
        return WitnessOption(witness_server, off)

    def visitPartner_server(self, ctx: tsql.Partner_serverContext):
        host = self._(ctx.host())
        return PartnerServer(host)

    def visitHost(self, ctx: tsql.HostContext):
        id = self._(ctx.id_(0))
        dot = self._(ctx.DOT()) is not None
        host = self._(ctx.host())
        right = self._(ctx.id_(1))
        return Host(id, dot, host, right)

    def visitDate_correlation_optimization_option(self, ctx: tsql.Date_correlation_optimization_optionContext):
        on_off = self._(ctx.on_off())
        return DateCorrelationOptimizationOption(on_off)

    def visitDb_encryption_option(self, ctx: tsql.Db_encryption_optionContext):
        on_off = self._(ctx.on_off())
        return DbEncryptionOption(on_off)

    def visitDb_state_option(self, ctx: tsql.Db_state_optionContext):
        online = self._(ctx.ONLINE()) is not None
        offline = self._(ctx.OFFLINE()) is not None
        emergency = self._(ctx.EMERGENCY()) is not None
        return DbStateOption(online, offline, emergency)

    def visitDb_update_option(self, ctx: tsql.Db_update_optionContext):
        read_only = self._(ctx.READ_ONLY()) is not None
        read_write = self._(ctx.READ_WRITE()) is not None
        return DbUpdateOption(read_only, read_write)

    def visitDb_user_access_option(self, ctx: tsql.Db_user_access_optionContext):
        single_user = self._(ctx.SINGLE_USER()) is not None
        restricted_user = self._(ctx.RESTRICTED_USER()) is not None
        multi_user = self._(ctx.MULTI_USER()) is not None
        return DbUserAccessOption(single_user, restricted_user, multi_user)

    def visitDelayed_durability_option(self, ctx: tsql.Delayed_durability_optionContext):
        disabled = self._(ctx.DISABLED()) is not None
        allowed = self._(ctx.ALLOWED()) is not None
        forced = self._(ctx.FORCED()) is not None
        return DelayedDurabilityOption(disabled, allowed, forced)

    def visitExternal_access_option(self, ctx: tsql.External_access_optionContext):
        db_chaining = self._(ctx.DB_CHAINING()) is not None
        on_off = self._(ctx.on_off())
        trustworthy = self._(ctx.TRUSTWORTHY()) is not None
        default_language = self._(ctx.DEFAULT_LANGUAGE()) is not None
        equal = self._(ctx.EQUAL()) is not None
        id = self._(ctx.id_())
        string = self._(ctx.STRING())
        default_fulltext_language = self._(ctx.DEFAULT_FULLTEXT_LANGUAGE()) is not None
        nested_triggers = self._(ctx.NESTED_TRIGGERS()) is not None
        off = self._(ctx.OFF()) is not None
        on = self._(ctx.ON()) is not None
        transform_noise_words = self._(ctx.TRANSFORM_NOISE_WORDS()) is not None
        two_digit_year_cutoff = self._(ctx.TWO_DIGIT_YEAR_CUTOFF()) is not None
        decimal = self._(ctx.DECIMAL()) is not None
        return ExternalAccessOption(db_chaining, on_off, trustworthy, default_language, equal, id, string, default_fulltext_language, nested_triggers, off, on, transform_noise_words, two_digit_year_cutoff, decimal)

    def visitHadr_options(self, ctx: tsql.Hadr_optionsContext):
        availability = self._(ctx.AVAILABILITY()) is not None
        group = self._(ctx.GROUP()) is not None
        equal = self._(ctx.EQUAL()) is not None
        availability_group_name = self._(ctx.id_())
        off = self._(ctx.OFF()) is not None
        suspend = self._(ctx.SUSPEND()) is not None
        resume = self._(ctx.RESUME()) is not None
        return HadrOptions(availability, group, equal, availability_group_name, off, suspend, resume)

    def visitMixed_page_allocation_option(self, ctx: tsql.Mixed_page_allocation_optionContext):
        off = self._(ctx.OFF()) is not None
        on = self._(ctx.ON()) is not None
        return MixedPageAllocationOption(off, on)

    def visitParameterization_option(self, ctx: tsql.Parameterization_optionContext):
        simple = self._(ctx.SIMPLE()) is not None
        forced = self._(ctx.FORCED()) is not None
        return ParameterizationOption(simple, forced)

    def visitRecovery_option(self, ctx: tsql.Recovery_optionContext):
        recovery = self._(ctx.RECOVERY()) is not None
        full = self._(ctx.FULL()) is not None
        bulk_logged = self._(ctx.BULK_LOGGED()) is not None
        simple = self._(ctx.SIMPLE()) is not None
        torn_page_detection = self._(ctx.TORN_PAGE_DETECTION()) is not None
        on_off = self._(ctx.on_off())
        accelerated_database_recovery = self._(ctx.ACCELERATED_DATABASE_RECOVERY()) is not None
        page_verify = self._(ctx.PAGE_VERIFY()) is not None
        checksum = self._(ctx.CHECKSUM()) is not None
        none = self._(ctx.NONE()) is not None
        return RecoveryOption(recovery, full, bulk_logged, simple, torn_page_detection, on_off, accelerated_database_recovery, page_verify, checksum, none)

    def visitService_broker_option(self, ctx: tsql.Service_broker_optionContext):
        enable_broker = self._(ctx.ENABLE_BROKER()) is not None
        disable_broker = self._(ctx.DISABLE_BROKER()) is not None
        new_broker = self._(ctx.NEW_BROKER()) is not None
        error_broker_conversations = self._(ctx.ERROR_BROKER_CONVERSATIONS()) is not None
        honor_broker_priority = self._(ctx.HONOR_BROKER_PRIORITY()) is not None
        on_off = self._(ctx.on_off())
        return ServiceBrokerOption(enable_broker, disable_broker, new_broker, error_broker_conversations, honor_broker_priority, on_off)

    def visitSnapshot_option(self, ctx: tsql.Snapshot_optionContext):
        allow_snapshot_isolation = self._(ctx.ALLOW_SNAPSHOT_ISOLATION()) is not None
        on_off = self._(ctx.on_off())
        read_committed_snapshot = self._(ctx.READ_COMMITTED_SNAPSHOT()) is not None
        on = self._(ctx.ON()) is not None
        off = self._(ctx.OFF()) is not None
        snapshot_option_memory_optimized_elevate_to_snapshot = self._(ctx.snapshot_option_MEMORY_OPTIMIZED_ELEVATE_TO_SNAPSHOT())
        return SnapshotOption(allow_snapshot_isolation, on_off, read_committed_snapshot, on, off, snapshot_option_memory_optimized_elevate_to_snapshot)

    def visitSql_option(self, ctx: tsql.Sql_optionContext):
        ansi_null_default = self._(ctx.ANSI_NULL_DEFAULT()) is not None
        on_off = self._(ctx.on_off())
        ansi_nulls = self._(ctx.ANSI_NULLS()) is not None
        ansi_padding = self._(ctx.ANSI_PADDING()) is not None
        ansi_warnings = self._(ctx.ANSI_WARNINGS()) is not None
        arithabort = self._(ctx.ARITHABORT()) is not None
        compatibility_level = self._(ctx.COMPATIBILITY_LEVEL()) is not None
        equal = self._(ctx.EQUAL()) is not None
        decimal = self._(ctx.DECIMAL()) is not None
        concat_null_yields_null = self._(ctx.CONCAT_NULL_YIELDS_NULL()) is not None
        numeric_roundabort = self._(ctx.NUMERIC_ROUNDABORT()) is not None
        quoted_identifier = self._(ctx.QUOTED_IDENTIFIER()) is not None
        recursive_triggers = self._(ctx.RECURSIVE_TRIGGERS()) is not None
        return SqlOption(ansi_null_default, on_off, ansi_nulls, ansi_padding, ansi_warnings, arithabort, compatibility_level, equal, decimal, concat_null_yields_null, numeric_roundabort, quoted_identifier, recursive_triggers)

    def visitTarget_recovery_time_option(self, ctx: tsql.Target_recovery_time_optionContext):
        seconds = self._(ctx.SECONDS()) is not None
        minutes = self._(ctx.MINUTES()) is not None
        return TargetRecoveryTimeOption(seconds, minutes)

    def visitTermination(self, ctx: tsql.TerminationContext):
        rollback = self._(ctx.ROLLBACK()) is not None
        after = self._(ctx.AFTER()) is not None
        seconds = self._(ctx.DECIMAL()) is not None
        immediate = self._(ctx.IMMEDIATE()) is not None
        no_wait = self._(ctx.NO_WAIT()) is not None
        return Termination(rollback, after, seconds, immediate, no_wait)

    def visitDrop_index(self, ctx: tsql.Drop_indexContext):
        if_ = self._(ctx.IF()) is not None
        exists = self._(ctx.EXISTS()) is not None
        left = self._(ctx.drop_relational_or_xml_or_spatial_index(0))
        left = self._(ctx.drop_backward_compatible_index(0))
        right = self.repeated(ctx, tsql.Drop_relational_or_xml_or_spatial_indexContext)
        right = self.repeated(ctx, tsql.Drop_backward_compatible_indexContext)
        return DropIndex(if_, exists, left, left, right, right)

    def visitDrop_relational_or_xml_or_spatial_index(self, ctx: tsql.Drop_relational_or_xml_or_spatial_indexContext):
        index_name = self._(ctx.id_())
        full_table_name = self._(ctx.full_table_name())
        return DropRelationalOrXmlOrSpatialIndex(index_name, full_table_name)

    def visitDrop_backward_compatible_index(self, ctx: tsql.Drop_backward_compatible_indexContext):
        owner_name = self._(ctx.id_())
        return DropBackwardCompatibleIndex(owner_name)

    def visitDrop_procedure(self, ctx: tsql.Drop_procedureContext):
        drop_procedure_proc = self._(ctx.drop_procedure_proc())
        if_ = self._(ctx.IF()) is not None
        exists = self._(ctx.EXISTS()) is not None
        left = self._(ctx.func_proc_name_schema(0))
        right = self.repeated(ctx, tsql.Func_proc_name_schemaContext)
        return DropProcedure(drop_procedure_proc, if_, exists, left, right)

    def visitDrop_trigger(self, ctx: tsql.Drop_triggerContext):
        drop_dml_trigger = self._(ctx.drop_dml_trigger())
        drop_ddl_trigger = self._(ctx.drop_ddl_trigger())
        return DropTrigger(drop_dml_trigger, drop_ddl_trigger)

    def visitDrop_dml_trigger(self, ctx: tsql.Drop_dml_triggerContext):
        if_ = self._(ctx.IF()) is not None
        exists = self._(ctx.EXISTS()) is not None
        left = self._(ctx.simple_name(0))
        right = self.repeated(ctx, tsql.Simple_nameContext)
        return DropDmlTrigger(if_, exists, left, right)

    def visitDrop_ddl_trigger(self, ctx: tsql.Drop_ddl_triggerContext):
        if_ = self._(ctx.IF()) is not None
        exists = self._(ctx.EXISTS()) is not None
        left = self._(ctx.simple_name(0))
        right = self.repeated(ctx, tsql.Simple_nameContext)
        database = self._(ctx.DATABASE()) is not None
        all = self._(ctx.ALL()) is not None
        server = self._(ctx.SERVER()) is not None
        return DropDdlTrigger(if_, exists, left, right, database, all, server)

    def visitDrop_function(self, ctx: tsql.Drop_functionContext):
        if_ = self._(ctx.IF()) is not None
        exists = self._(ctx.EXISTS()) is not None
        left = self._(ctx.func_proc_name_schema(0))
        right = self.repeated(ctx, tsql.Func_proc_name_schemaContext)
        return DropFunction(if_, exists, left, right)

    def visitDrop_statistics(self, ctx: tsql.Drop_statisticsContext):
        name = self.repeated(ctx, tsql.Id_Context)
        table_name = self._(ctx.table_name())
        return DropStatistics(name, table_name)

    def visitDrop_table(self, ctx: tsql.Drop_tableContext):
        if_ = self._(ctx.IF()) is not None
        exists = self._(ctx.EXISTS()) is not None
        left = self._(ctx.table_name(0))
        right = self.repeated(ctx, tsql.Table_nameContext)
        return DropTable(if_, exists, left, right)

    def visitDrop_view(self, ctx: tsql.Drop_viewContext):
        if_ = self._(ctx.IF()) is not None
        exists = self._(ctx.EXISTS()) is not None
        left = self._(ctx.simple_name(0))
        right = self.repeated(ctx, tsql.Simple_nameContext)
        return DropView(if_, exists, left, right)

    def visitCreate_type(self, ctx: tsql.Create_typeContext):
        name = self._(ctx.simple_name())
        from_ = self._(ctx.FROM()) is not None
        data_type = self._(ctx.data_type())
        as_ = self._(ctx.AS()) is not None
        table = self._(ctx.TABLE()) is not None
        lr_bracket = self._(ctx.LR_BRACKET()) is not None
        column_def_table_constraints = self._(ctx.column_def_table_constraints())
        rr_bracket = self._(ctx.RR_BRACKET()) is not None
        return CreateType(name, from_, data_type, as_, table, lr_bracket, column_def_table_constraints, rr_bracket)

    def visitDrop_type(self, ctx: tsql.Drop_typeContext):
        if_ = self._(ctx.IF()) is not None
        exists = self._(ctx.EXISTS()) is not None
        name = self._(ctx.simple_name())
        return DropType(if_, exists, name)

    def visitRowset_function_limited(self, ctx: tsql.Rowset_function_limitedContext):
        openquery = self._(ctx.openquery())
        opendatasource = self._(ctx.opendatasource())
        return RowsetFunctionLimited(openquery, opendatasource)

    def visitOpenquery(self, ctx: tsql.OpenqueryContext):
        linked_server = self._(ctx.id_())
        query = self._(ctx.STRING())
        return Openquery(linked_server, query)

    def visitOpendatasource(self, ctx: tsql.OpendatasourceContext):
        provider = self._(ctx.STRING())
        database = self._(ctx.id_())
        return Opendatasource(provider, database)

    def visitDeclare_statement(self, ctx: tsql.Declare_statementContext):
        declare = self._(ctx.DECLARE()) is not None
        local_id = self._(ctx.LOCAL_ID())
        data_type = self._(ctx.data_type())
        table_type_definition = self._(ctx.table_type_definition())
        table_name = self._(ctx.table_name())
        loc = self._(ctx.declare_local())
        xml_type_definition = self._(ctx.xml_type_definition())
        with_ = self._(ctx.WITH()) is not None
        xmlnamespaces = self._(ctx.XMLNAMESPACES()) is not None
        xml_dec = self._(ctx.xml_declaration())
        return DeclareStatement(declare, local_id, data_type, table_type_definition, table_name, loc, xml_type_definition, with_, xmlnamespaces, xml_dec)

    def visitXml_declaration(self, ctx: tsql.Xml_declarationContext):
        xml_namespace_uri = self._(ctx.STRING())
        as_ = self._(ctx.AS()) is not None
        id = self._(ctx.id_())
        default_ = self._(ctx.DEFAULT()) is not None
        return XmlDeclaration(xml_namespace_uri, as_, id, default_)

    def visitCursor_statement(self, ctx: tsql.Cursor_statementContext):
        close = self._(ctx.CLOSE()) is not None
        cursor_name = self._(ctx.cursor_name())
        deallocate = self._(ctx.DEALLOCATE()) is not None
        declare_cursor = self._(ctx.declare_cursor())
        fetch_cursor = self._(ctx.fetch_cursor())
        open = self._(ctx.OPEN()) is not None
        return CursorStatement(close, cursor_name, deallocate, declare_cursor, fetch_cursor, open)

    def visitBackup_database(self, ctx: tsql.Backup_databaseContext):
        database_name = self._(ctx.id_(0))
        read_write_filegroups = self._(ctx.READ_WRITE_FILEGROUPS()) is not None
        file_or_filegroup = self.repeated(ctx, tsql.STRINGContext)
        left = self._(ctx.TO()) is not None
        right = self._(ctx.TO()) is not None
        with_ = self._(ctx.WITH()) is not None
        file_or_filegroup = self.repeated(ctx, tsql.STRINGContext)
        left = self._(ctx.FILE()) is not None
        left = self._(ctx.FILEGROUP()) is not None
        logical_device_name = self.repeated(ctx, tsql.Id_Context)
        backup_set_name = self.repeated(ctx, tsql.Id_Context)
        right = self._(ctx.FILE()) is not None
        right = self._(ctx.FILEGROUP()) is not None
        left = self._(ctx.DISK()) is not None
        left = self._(ctx.TAPE()) is not None
        left = self._(ctx.URL()) is not None
        third = self._(ctx.STRING(2))
        fourth = self._(ctx.id_(3))
        logical_device_name = self.repeated(ctx, tsql.Id_Context)
        compression = self._(ctx.COMPRESSION()) is not None
        no_compression = self._(ctx.NO_COMPRESSION()) is not None
        fourth = self._(ctx.STRING(3))
        f_5 = self._(ctx.id_(5))
        expiredate = self._(ctx.EXPIREDATE()) is not None
        left = self._(ctx.EQUAL()) is not None
        retaindays = self._(ctx.RETAINDAYS()) is not None
        right = self._(ctx.EQUAL()) is not None
        noinit = self._(ctx.NOINIT()) is not None
        init = self._(ctx.INIT()) is not None
        noskip = self._(ctx.NOSKIP()) is not None
        skip_keyword = self._(ctx.SKIP_KEYWORD()) is not None
        noformat = self._(ctx.NOFORMAT()) is not None
        format = self._(ctx.FORMAT()) is not None
        fifth = self._(ctx.STRING(4))
        f_6 = self._(ctx.id_(6))
        medianame = self._(ctx.STRING(5))
        left = self._(ctx.DECIMAL()) is not None
        f_7 = self._(ctx.id_(7))
        right = self._(ctx.DECIMAL()) is not None
        f_8 = self._(ctx.id_(8))
        third = self._(ctx.DECIMAL()) is not None
        f_9 = self._(ctx.id_(9))
        no_checksum = self._(ctx.NO_CHECKSUM()) is not None
        checksum = self._(ctx.CHECKSUM()) is not None
        stop_on_error = self._(ctx.STOP_ON_ERROR()) is not None
        continue_after_error = self._(ctx.CONTINUE_AFTER_ERROR()) is not None
        third = self._(ctx.EQUAL()) is not None
        stats_percent = self._(ctx.DECIMAL()) is not None
        rewind = self._(ctx.REWIND()) is not None
        norewind = self._(ctx.NOREWIND()) is not None
        load = self._(ctx.LOAD()) is not None
        nounload = self._(ctx.NOUNLOAD()) is not None
        aes_128 = self._(ctx.AES_128()) is not None
        aes_192 = self._(ctx.AES_192()) is not None
        aes_256 = self._(ctx.AES_256()) is not None
        triple_des_3key = self._(ctx.TRIPLE_DES_3KEY()) is not None
        encryptor_name = self._(ctx.id_(10))
        left = self._(ctx.SERVER()) is not None
        asymmetric = self._(ctx.ASYMMETRIC()) is not None
        key = self._(ctx.KEY()) is not None
        fourth = self._(ctx.EQUAL()) is not None
        encryptor_name = self._(ctx.id_(11))
        right = self._(ctx.DISK()) is not None
        right = self._(ctx.TAPE()) is not None
        right = self._(ctx.URL()) is not None
        f_6 = self._(ctx.STRING(6))
        f12 = self._(ctx.id_(12))
        f_7 = self._(ctx.STRING(7))
        f13 = self._(ctx.id_(13))
        fifth = self._(ctx.DECIMAL()) is not None
        f14 = self._(ctx.id_(14))
        return BackupDatabase(database_name, read_write_filegroups, file_or_filegroup, left, right, with_, file_or_filegroup, left, left, logical_device_name, backup_set_name, right, right, left, left, left, third, fourth, logical_device_name, compression, no_compression, fourth, f_5, expiredate, left, retaindays, right, noinit, init, noskip, skip_keyword, noformat, format, fifth, f_6, medianame, left, f_7, right, f_8, third, f_9, no_checksum, checksum, stop_on_error, continue_after_error, third, stats_percent, rewind, norewind, load, nounload, aes_128, aes_192, aes_256, triple_des_3key, encryptor_name, left, asymmetric, key, fourth, encryptor_name, right, right, right, f_6, f12, f_7, f13, fifth, f14)

    def visitBackup_log(self, ctx: tsql.Backup_logContext):
        database_name = self._(ctx.id_(0))
        left = self._(ctx.TO()) is not None
        right = self._(ctx.TO()) is not None
        with_ = self._(ctx.WITH()) is not None
        logical_device_name = self.repeated(ctx, tsql.Id_Context)
        backup_set_name = self.repeated(ctx, tsql.Id_Context)
        left = self._(ctx.DISK()) is not None
        left = self._(ctx.TAPE()) is not None
        left = self._(ctx.URL()) is not None
        left = self._(ctx.STRING(0))
        fourth = self._(ctx.id_(3))
        logical_device_name = self.repeated(ctx, tsql.Id_Context)
        compression = self._(ctx.COMPRESSION()) is not None
        no_compression = self._(ctx.NO_COMPRESSION()) is not None
        right = self._(ctx.STRING(1))
        f_5 = self._(ctx.id_(5))
        expiredate = self._(ctx.EXPIREDATE()) is not None
        left = self._(ctx.EQUAL()) is not None
        retaindays = self._(ctx.RETAINDAYS()) is not None
        right = self._(ctx.EQUAL()) is not None
        noinit = self._(ctx.NOINIT()) is not None
        init = self._(ctx.INIT()) is not None
        noskip = self._(ctx.NOSKIP()) is not None
        skip_keyword = self._(ctx.SKIP_KEYWORD()) is not None
        noformat = self._(ctx.NOFORMAT()) is not None
        format = self._(ctx.FORMAT()) is not None
        third = self._(ctx.STRING(2))
        f_6 = self._(ctx.id_(6))
        medianame = self._(ctx.STRING(3))
        left = self._(ctx.DECIMAL()) is not None
        f_7 = self._(ctx.id_(7))
        right = self._(ctx.DECIMAL()) is not None
        f_8 = self._(ctx.id_(8))
        third = self._(ctx.DECIMAL()) is not None
        f_9 = self._(ctx.id_(9))
        no_checksum = self._(ctx.NO_CHECKSUM()) is not None
        checksum = self._(ctx.CHECKSUM()) is not None
        stop_on_error = self._(ctx.STOP_ON_ERROR()) is not None
        continue_after_error = self._(ctx.CONTINUE_AFTER_ERROR()) is not None
        third = self._(ctx.EQUAL()) is not None
        stats_percent = self._(ctx.DECIMAL()) is not None
        rewind = self._(ctx.REWIND()) is not None
        norewind = self._(ctx.NOREWIND()) is not None
        load = self._(ctx.LOAD()) is not None
        nounload = self._(ctx.NOUNLOAD()) is not None
        norecovery = self._(ctx.NORECOVERY()) is not None
        standby = self._(ctx.STANDBY()) is not None
        fourth = self._(ctx.EQUAL()) is not None
        undo_file_name = self._(ctx.STRING(4))
        aes_128 = self._(ctx.AES_128()) is not None
        aes_192 = self._(ctx.AES_192()) is not None
        aes_256 = self._(ctx.AES_256()) is not None
        triple_des_3key = self._(ctx.TRIPLE_DES_3KEY()) is not None
        encryptor_name = self._(ctx.id_(10))
        left = self._(ctx.SERVER()) is not None
        asymmetric = self._(ctx.ASYMMETRIC()) is not None
        key = self._(ctx.KEY()) is not None
        fifth = self._(ctx.EQUAL()) is not None
        encryptor_name = self._(ctx.id_(11))
        right = self._(ctx.DISK()) is not None
        right = self._(ctx.TAPE()) is not None
        right = self._(ctx.URL()) is not None
        f_5 = self._(ctx.STRING(5))
        f12 = self._(ctx.id_(12))
        f_6 = self._(ctx.STRING(6))
        f13 = self._(ctx.id_(13))
        fifth = self._(ctx.DECIMAL()) is not None
        f14 = self._(ctx.id_(14))
        return BackupLog(database_name, left, right, with_, logical_device_name, backup_set_name, left, left, left, left, fourth, logical_device_name, compression, no_compression, right, f_5, expiredate, left, retaindays, right, noinit, init, noskip, skip_keyword, noformat, format, third, f_6, medianame, left, f_7, right, f_8, third, f_9, no_checksum, checksum, stop_on_error, continue_after_error, third, stats_percent, rewind, norewind, load, nounload, norecovery, standby, fourth, undo_file_name, aes_128, aes_192, aes_256, triple_des_3key, encryptor_name, left, asymmetric, key, fifth, encryptor_name, right, right, right, f_5, f12, f_6, f13, fifth, f14)

    def visitBackup_certificate(self, ctx: tsql.Backup_certificateContext):
        certname = self._(ctx.id_())
        cert_file = self._(ctx.STRING())
        with_ = self._(ctx.WITH()) is not None
        private = self._(ctx.PRIVATE()) is not None
        key = self._(ctx.KEY()) is not None
        lr_bracket = self._(ctx.LR_BRACKET()) is not None
        rr_bracket = self._(ctx.RR_BRACKET()) is not None
        return BackupCertificate(certname, cert_file, with_, private, key, lr_bracket, rr_bracket)

    def visitBackup_master_key(self, ctx: tsql.Backup_master_keyContext):
        master_key_backup_file = self._(ctx.STRING())
        return BackupMasterKey(master_key_backup_file)

    def visitBackup_service_master_key(self, ctx: tsql.Backup_service_master_keyContext):
        service_master_key_backup_file = self._(ctx.STRING())
        return BackupServiceMasterKey(service_master_key_backup_file)

    def visitKill_statement(self, ctx: tsql.Kill_statementContext):
        kill_process = self._(ctx.kill_process())
        kill_query_notification = self._(ctx.kill_query_notification())
        return KillStatement(kill_process, kill_query_notification)

    def visitKill_process(self, ctx: tsql.Kill_processContext):
        kill_process_session_id = self._(ctx.kill_process_session_id())
        uow = self._(ctx.UOW()) is not None
        with_ = self._(ctx.WITH()) is not None
        statusonly = self._(ctx.STATUSONLY()) is not None
        return KillProcess(kill_process_session_id, uow, with_, statusonly)

    def visitKill_query_notification(self, ctx: tsql.Kill_query_notificationContext):
        all = self._(ctx.ALL()) is not None
        subscription_id = self._(ctx.DECIMAL()) is not None
        return KillQueryNotification(all, subscription_id)

    def visitExecute_statement(self, ctx: tsql.Execute_statementContext):
        execute = self._(ctx.EXECUTE())
        execute_body = self._(ctx.execute_body())
        return ExecuteStatement(execute, execute_body)

    def visitExecute_body_batch(self, ctx: tsql.Execute_body_batchContext):
        func_proc_name_server_database_schema = self._(ctx.func_proc_name_server_database_schema())
        left = self._(ctx.execute_statement_arg(0))
        right = self.repeated(ctx, tsql.Execute_statement_argContext)
        return ExecuteBodyBatch(func_proc_name_server_database_schema, left, right)

    def visitExecute_body(self, ctx: tsql.Execute_bodyContext):
        return_status = self._(ctx.LOCAL_ID())
        func_proc_name_server_database_schema = self._(ctx.func_proc_name_server_database_schema())
        execute_var_string = self._(ctx.execute_var_string(0))
        execute_statement_arg = self.repeated(ctx, tsql.Execute_statement_argContext)
        right = self.repeated(ctx, tsql.Execute_var_stringContext)
        as_ = self._(ctx.AS()) is not None
        string = self._(ctx.STRING())
        at_keyword = self._(ctx.AT_KEYWORD()) is not None
        linked_server = self._(ctx.id_())
        login = self._(ctx.LOGIN()) is not None
        user = self._(ctx.USER()) is not None
        caller = self._(ctx.CALLER()) is not None
        return ExecuteBody(return_status, func_proc_name_server_database_schema, execute_var_string, execute_statement_arg, right, as_, string, at_keyword, linked_server, login, user, caller)

    def visitExecute_statement_arg(self, ctx: tsql.Execute_statement_argContext):
        execute_statement_arg_unnamed = self._(ctx.execute_statement_arg_unnamed())
        execute_statement_arg = self.repeated(ctx, tsql.Execute_statement_argContext)
        left = self._(ctx.execute_statement_arg_named(0))
        right = self.repeated(ctx, tsql.Execute_statement_arg_namedContext)
        return ExecuteStatementArg(execute_statement_arg_unnamed, execute_statement_arg, left, right)

    def visitExecute_statement_arg_named(self, ctx: tsql.Execute_statement_arg_namedContext):
        name = self._(ctx.LOCAL_ID())
        value = self._(ctx.execute_parameter())
        return ExecuteStatementArgNamed(name, value)

    def visitExecute_statement_arg_unnamed(self, ctx: tsql.Execute_statement_arg_unnamedContext):
        value = self._(ctx.execute_parameter())
        return ExecuteStatementArgUnnamed(value)

    def visitExecute_parameter(self, ctx: tsql.Execute_parameterContext):
        constant = self._(ctx.constant())
        local_id = self._(ctx.LOCAL_ID())
        id = self._(ctx.id_())
        default_ = self._(ctx.DEFAULT()) is not None
        null = self._(ctx.NULL_()) is not None
        output = self._(ctx.OUTPUT()) is not None
        out = self._(ctx.OUT()) is not None
        return ExecuteParameter(constant, local_id, id, default_, null, output, out)

    def visitExecute_var_string(self, ctx: tsql.Execute_var_stringContext):
        left = self._(ctx.LOCAL_ID(0))
        output = self._(ctx.OUTPUT()) is not None
        out = self._(ctx.OUT()) is not None
        right = self._(ctx.LOCAL_ID(1))
        execute_var_string = self._(ctx.execute_var_string())
        string = self._(ctx.STRING())
        return ExecuteVarString(left, output, out, right, execute_var_string, string)

    def visitSecurity_statement(self, ctx: tsql.Security_statementContext):
        execute_clause = self._(ctx.execute_clause())
        left = self._(ctx.GRANT()) is not None
        all = self._(ctx.ALL()) is not None
        privileges = self._(ctx.PRIVILEGES()) is not None
        grant_permission = self._(ctx.grant_permission())
        on = self._(ctx.ON()) is not None
        on_id = self._(ctx.table_name())
        to = self._(ctx.TO()) is not None
        to_principal = self._(ctx.principal_id())
        with_ = self._(ctx.WITH()) is not None
        right = self._(ctx.GRANT()) is not None
        option = self._(ctx.OPTION()) is not None
        as_ = self._(ctx.AS()) is not None
        column_name_list = self._(ctx.column_name_list())
        class_type_for_grant = self._(ctx.class_type_for_grant())
        revert = self._(ctx.REVERT()) is not None
        cookie = self._(ctx.COOKIE()) is not None
        local_id = self._(ctx.LOCAL_ID())
        open_key = self._(ctx.open_key())
        close_key = self._(ctx.close_key())
        create_key = self._(ctx.create_key())
        create_certificate = self._(ctx.create_certificate())
        return SecurityStatement(execute_clause, left, all, privileges, grant_permission, on, on_id, to, to_principal, with_, right, option, as_, column_name_list, class_type_for_grant, revert, cookie, local_id, open_key, close_key, create_key, create_certificate)

    def visitPrincipal_id(self, ctx: tsql.Principal_idContext):
        id = self._(ctx.id_())
        public = self._(ctx.PUBLIC()) is not None
        return PrincipalId(id, public)

    def visitCreate_certificate(self, ctx: tsql.Create_certificateContext):
        certificate_name = self._(ctx.id_())
        authorization = self._(ctx.AUTHORIZATION()) is not None
        from_ = self._(ctx.FROM()) is not None
        existing_keys = self._(ctx.existing_keys())
        generate_new_keys = self._(ctx.generate_new_keys())
        active = self._(ctx.ACTIVE()) is not None
        for_ = self._(ctx.FOR()) is not None
        begin = self._(ctx.BEGIN()) is not None
        dialog = self._(ctx.DIALOG()) is not None
        on_off = self._(ctx.on_off())
        return CreateCertificate(certificate_name, authorization, from_, existing_keys, generate_new_keys, active, for_, begin, dialog, on_off)

    def visitExisting_keys(self, ctx: tsql.Existing_keysContext):
        assembly = self._(ctx.ASSEMBLY()) is not None
        assembly_name = self._(ctx.id_())
        file = self._(ctx.FILE()) is not None
        equal = self._(ctx.EQUAL()) is not None
        path_to_file = self._(ctx.STRING())
        with_ = self._(ctx.WITH()) is not None
        private = self._(ctx.PRIVATE()) is not None
        key = self._(ctx.KEY()) is not None
        private_key_options = self._(ctx.private_key_options())
        return ExistingKeys(assembly, assembly_name, file, equal, path_to_file, with_, private, key, private_key_options)

    def visitPrivate_key_options(self, ctx: tsql.Private_key_optionsContext):
        file = self._(ctx.FILE()) is not None
        binary = self._(ctx.BINARY())
        path = self._(ctx.STRING())
        by = self._(ctx.BY()) is not None
        password = self._(ctx.PASSWORD()) is not None
        decryption = self._(ctx.DECRYPTION()) is not None
        encryption = self._(ctx.ENCRYPTION()) is not None
        return PrivateKeyOptions(file, binary, path, by, password, decryption, encryption)

    def visitGenerate_new_keys(self, ctx: tsql.Generate_new_keysContext):
        encryption = self._(ctx.ENCRYPTION()) is not None
        by = self._(ctx.BY()) is not None
        password = self._(ctx.PASSWORD()) is not None
        password = self._(ctx.STRING())
        date_options = self.repeated(ctx, tsql.Date_optionsContext)
        return GenerateNewKeys(encryption, by, password, password, date_options)

    def visitDate_options(self, ctx: tsql.Date_optionsContext):
        start_date = self._(ctx.START_DATE()) is not None
        expiry_date = self._(ctx.EXPIRY_DATE()) is not None
        string = self._(ctx.STRING())
        return DateOptions(start_date, expiry_date, string)

    def visitOpen_key(self, ctx: tsql.Open_keyContext):
        open = self._(ctx.OPEN()) is not None
        symmetric = self._(ctx.SYMMETRIC()) is not None
        key = self._(ctx.KEY()) is not None
        key_name = self._(ctx.id_())
        decryption = self._(ctx.DECRYPTION()) is not None
        by = self._(ctx.BY()) is not None
        decryption_mechanism = self._(ctx.decryption_mechanism())
        master = self._(ctx.MASTER()) is not None
        password = self._(ctx.PASSWORD()) is not None
        password = self._(ctx.STRING())
        return OpenKey(open, symmetric, key, key_name, decryption, by, decryption_mechanism, master, password, password)

    def visitClose_key(self, ctx: tsql.Close_keyContext):
        close = self._(ctx.CLOSE()) is not None
        symmetric = self._(ctx.SYMMETRIC()) is not None
        key = self._(ctx.KEY()) is not None
        key_name = self._(ctx.id_())
        all = self._(ctx.ALL()) is not None
        keys = self._(ctx.KEYS()) is not None
        master = self._(ctx.MASTER()) is not None
        return CloseKey(close, symmetric, key, key_name, all, keys, master)

    def visitCreate_key(self, ctx: tsql.Create_keyContext):
        create = self._(ctx.CREATE()) is not None
        master = self._(ctx.MASTER()) is not None
        key = self._(ctx.KEY()) is not None
        encryption = self._(ctx.ENCRYPTION()) is not None
        by = self._(ctx.BY()) is not None
        password = self._(ctx.PASSWORD()) is not None
        password = self._(ctx.STRING())
        symmetric = self._(ctx.SYMMETRIC()) is not None
        key_name = self._(ctx.id_())
        authorization = self._(ctx.AUTHORIZATION()) is not None
        from_ = self._(ctx.FROM()) is not None
        provider = self._(ctx.PROVIDER()) is not None
        with_ = self._(ctx.WITH()) is not None
        key_options = self._(ctx.key_options())
        encryption_mechanism = self._(ctx.encryption_mechanism())
        return CreateKey(create, master, key, encryption, by, password, password, symmetric, key_name, authorization, from_, provider, with_, key_options, encryption_mechanism)

    def visitKey_options(self, ctx: tsql.Key_optionsContext):
        key_source = self._(ctx.KEY_SOURCE()) is not None
        equal = self._(ctx.EQUAL()) is not None
        pass_phrase = self._(ctx.STRING())
        algorithm = self._(ctx.ALGORITHM()) is not None
        algorithm = self._(ctx.algorithm())
        identity_value = self._(ctx.IDENTITY_VALUE()) is not None
        provider_key_name = self._(ctx.PROVIDER_KEY_NAME()) is not None
        creation_disposition = self._(ctx.CREATION_DISPOSITION()) is not None
        create_new = self._(ctx.CREATE_NEW()) is not None
        open_existing = self._(ctx.OPEN_EXISTING()) is not None
        return KeyOptions(key_source, equal, pass_phrase, algorithm, algorithm, identity_value, provider_key_name, creation_disposition, create_new, open_existing)

    def visitAlgorithm(self, ctx: tsql.AlgorithmContext):
        des = self._(ctx.DES()) is not None
        triple_des = self._(ctx.TRIPLE_DES()) is not None
        triple_des_3key = self._(ctx.TRIPLE_DES_3KEY()) is not None
        rc2 = self._(ctx.RC2()) is not None
        rc4 = self._(ctx.RC4()) is not None
        rc4_128 = self._(ctx.RC4_128()) is not None
        desx = self._(ctx.DESX()) is not None
        aes_128 = self._(ctx.AES_128()) is not None
        aes_192 = self._(ctx.AES_192()) is not None
        aes_256 = self._(ctx.AES_256()) is not None
        return Algorithm(des, triple_des, triple_des_3key, rc2, rc4, rc4_128, desx, aes_128, aes_192, aes_256)

    def visitEncryption_mechanism(self, ctx: tsql.Encryption_mechanismContext):
        certificate = self._(ctx.CERTIFICATE()) is not None
        certificate_name = self._(ctx.id_())
        asymmetric = self._(ctx.ASYMMETRIC()) is not None
        key = self._(ctx.KEY()) is not None
        symmetric = self._(ctx.SYMMETRIC()) is not None
        password = self._(ctx.PASSWORD()) is not None
        string = self._(ctx.STRING())
        return EncryptionMechanism(certificate, certificate_name, asymmetric, key, symmetric, password, string)

    def visitDecryption_mechanism(self, ctx: tsql.Decryption_mechanismContext):
        certificate = self._(ctx.CERTIFICATE()) is not None
        certificate_name = self._(ctx.id_())
        with_ = self._(ctx.WITH()) is not None
        password = self._(ctx.PASSWORD()) is not None
        equal = self._(ctx.EQUAL()) is not None
        string = self._(ctx.STRING())
        asymmetric = self._(ctx.ASYMMETRIC()) is not None
        key = self._(ctx.KEY()) is not None
        symmetric = self._(ctx.SYMMETRIC()) is not None
        return DecryptionMechanism(certificate, certificate_name, with_, password, equal, string, asymmetric, key, symmetric)

    def visitGrant_permission(self, ctx: tsql.Grant_permissionContext):
        administer = self._(ctx.ADMINISTER()) is not None
        left = self._(ctx.BULK()) is not None
        left = self._(ctx.OPERATIONS()) is not None
        database = self._(ctx.DATABASE()) is not None
        right = self._(ctx.BULK()) is not None
        right = self._(ctx.OPERATIONS()) is not None
        alter = self._(ctx.ALTER()) is not None
        any = self._(ctx.ANY()) is not None
        resources = self._(ctx.RESOURCES()) is not None
        left = self._(ctx.SERVER()) is not None
        state = self._(ctx.STATE()) is not None
        settings = self._(ctx.SETTINGS()) is not None
        trace = self._(ctx.TRACE()) is not None
        application = self._(ctx.APPLICATION()) is not None
        left = self._(ctx.ROLE()) is not None
        assembly = self._(ctx.ASSEMBLY()) is not None
        asymmetric = self._(ctx.ASYMMETRIC()) is not None
        left = self._(ctx.KEY()) is not None
        availability = self._(ctx.AVAILABILITY()) is not None
        group = self._(ctx.GROUP()) is not None
        certificate = self._(ctx.CERTIFICATE()) is not None
        column = self._(ctx.COLUMN()) is not None
        connection = self._(ctx.CONNECTION()) is not None
        contract = self._(ctx.CONTRACT()) is not None
        credential = self._(ctx.CREDENTIAL()) is not None
        dataspace = self._(ctx.DATASPACE()) is not None
        endpoint = self._(ctx.ENDPOINT()) is not None
        left = self._(ctx.EVENT()) is not None
        external = self._(ctx.EXTERNAL()) is not None
        fulltext = self._(ctx.FULLTEXT()) is not None
        catalog = self._(ctx.CATALOG()) is not None
        linked = self._(ctx.LINKED()) is not None
        right = self._(ctx.SERVER()) is not None
        login = self._(ctx.LOGIN()) is not None
        mask = self._(ctx.MASK()) is not None
        message = self._(ctx.MESSAGE()) is not None
        type_ = self._(ctx.TYPE()) is not None
        remote = self._(ctx.REMOTE()) is not None
        left = self._(ctx.SERVICE()) is not None
        binding = self._(ctx.BINDING()) is not None
        right = self._(ctx.ROLE()) is not None
        route = self._(ctx.ROUTE()) is not None
        schema = self._(ctx.SCHEMA()) is not None
        security = self._(ctx.SECURITY()) is not None
        policy = self._(ctx.POLICY()) is not None
        third = self._(ctx.SERVER()) is not None
        right = self._(ctx.SERVICE()) is not None
        symmetric = self._(ctx.SYMMETRIC()) is not None
        right = self._(ctx.KEY()) is not None
        user = self._(ctx.USER()) is not None
        encryption = self._(ctx.ENCRYPTION()) is not None
        third = self._(ctx.KEY()) is not None
        master = self._(ctx.MASTER()) is not None
        fourth = self._(ctx.KEY()) is not None
        left = self._(ctx.AUDIT()) is not None
        ddl = self._(ctx.DDL()) is not None
        trigger = self._(ctx.TRIGGER()) is not None
        right = self._(ctx.EVENT()) is not None
        scoped = self._(ctx.SCOPED()) is not None
        configuration = self._(ctx.CONFIGURATION()) is not None
        left = self._(ctx.NOTIFICATION()) is not None
        left = self._(ctx.SESSION()) is not None
        data = self._(ctx.DATA()) is not None
        source = self._(ctx.SOURCE()) is not None
        file = self._(ctx.FILE()) is not None
        format = self._(ctx.FORMAT()) is not None
        library = self._(ctx.LIBRARY()) is not None
        right = self._(ctx.AUDIT()) is not None
        third = self._(ctx.ROLE()) is not None
        right = self._(ctx.NOTIFICATION()) is not None
        right = self._(ctx.SESSION()) is not None
        authenticate = self._(ctx.AUTHENTICATE()) is not None
        backup = self._(ctx.BACKUP()) is not None
        log = self._(ctx.LOG()) is not None
        checkpoint = self._(ctx.CHECKPOINT()) is not None
        connect = self._(ctx.CONNECT()) is not None
        replication = self._(ctx.REPLICATION()) is not None
        sql = self._(ctx.SQL()) is not None
        control = self._(ctx.CONTROL()) is not None
        create = self._(ctx.CREATE()) is not None
        aggregate = self._(ctx.AGGREGATE()) is not None
        right = self._(ctx.DATABASE()) is not None
        default_ = self._(ctx.DEFAULT()) is not None
        function = self._(ctx.FUNCTION()) is not None
        procedure = self._(ctx.PROCEDURE()) is not None
        queue = self._(ctx.QUEUE()) is not None
        rule = self._(ctx.RULE()) is not None
        sequence = self._(ctx.SEQUENCE()) is not None
        synonym = self._(ctx.SYNONYM()) is not None
        table = self._(ctx.TABLE()) is not None
        right = self._(ctx.TYPE()) is not None
        view = self._(ctx.VIEW()) is not None
        xml = self._(ctx.XML()) is not None
        right = self._(ctx.SCHEMA()) is not None
        collection = self._(ctx.COLLECTION()) is not None
        right = self._(ctx.DDL()) is not None
        third = self._(ctx.EVENT()) is not None
        third = self._(ctx.NOTIFICATION()) is not None
        delete = self._(ctx.DELETE()) is not None
        execute = self._(ctx.EXECUTE())
        script = self._(ctx.SCRIPT()) is not None
        access = self._(ctx.ACCESS()) is not None
        impersonate = self._(ctx.IMPERSONATE()) is not None
        insert = self._(ctx.INSERT()) is not None
        kill = self._(ctx.KILL()) is not None
        receive = self._(ctx.RECEIVE()) is not None
        references = self._(ctx.REFERENCES()) is not None
        select_ = self._(ctx.SELECT()) is not None
        all = self._(ctx.ALL()) is not None
        securables = self._(ctx.SECURABLES()) is not None
        send = self._(ctx.SEND()) is not None
        showplan = self._(ctx.SHOWPLAN()) is not None
        shutdown = self._(ctx.SHUTDOWN()) is not None
        subscribe = self._(ctx.SUBSCRIBE()) is not None
        query = self._(ctx.QUERY()) is not None
        notifications = self._(ctx.NOTIFICATIONS()) is not None
        take = self._(ctx.TAKE()) is not None
        ownership = self._(ctx.OWNERSHIP()) is not None
        unmask = self._(ctx.UNMASK()) is not None
        unsafe = self._(ctx.UNSAFE()) is not None
        update = self._(ctx.UPDATE()) is not None
        change = self._(ctx.CHANGE()) is not None
        tracking = self._(ctx.TRACKING()) is not None
        left = self._(ctx.DEFINITION()) is not None
        right = self._(ctx.STATE()) is not None
        right = self._(ctx.DEFINITION()) is not None
        third = self._(ctx.DEFINITION()) is not None
        return GrantPermission(administer, left, left, database, right, right, alter, any, resources, left, state, settings, trace, application, left, assembly, asymmetric, left, availability, group, certificate, column, connection, contract, credential, dataspace, endpoint, left, external, fulltext, catalog, linked, right, login, mask, message, type_, remote, left, binding, right, route, schema, security, policy, third, right, symmetric, right, user, encryption, third, master, fourth, left, ddl, trigger, right, scoped, configuration, left, left, data, source, file, format, library, right, third, right, right, authenticate, backup, log, checkpoint, connect, replication, sql, control, create, aggregate, right, default_, function, procedure, queue, rule, sequence, synonym, table, right, view, xml, right, collection, right, third, third, delete, execute, script, access, impersonate, insert, kill, receive, references, select_, all, securables, send, showplan, shutdown, subscribe, query, notifications, take, ownership, unmask, unsafe, update, change, tracking, left, right, right, third)

    def visitSet_statement(self, ctx: tsql.Set_statementContext):
        set = self._(ctx.SET()) is not None
        local_id = self._(ctx.LOCAL_ID())
        member_name = self._(ctx.id_())
        expression = self._(ctx.expression())
        cursor = self._(ctx.CURSOR()) is not None
        declare_set_cursor_common = self._(ctx.declare_set_cursor_common())
        for_ = self._(ctx.FOR()) is not None
        read = self._(ctx.READ()) is not None
        only = self._(ctx.ONLY()) is not None
        update = self._(ctx.UPDATE()) is not None
        of = self._(ctx.OF()) is not None
        column_name_list = self._(ctx.column_name_list())
        set_special = self._(ctx.set_special())
        return SetStatement(set, local_id, member_name, expression, cursor, declare_set_cursor_common, for_, read, only, update, of, column_name_list, set_special)

    def visitTransaction_statement(self, ctx: tsql.Transaction_statementContext):
        begin = self._(ctx.BEGIN()) is not None
        distributed = self._(ctx.DISTRIBUTED()) is not None
        tran = self._(ctx.TRAN()) is not None
        transaction = self._(ctx.TRANSACTION()) is not None
        id = self._(ctx.id_())
        local_id = self._(ctx.LOCAL_ID())
        with_ = self._(ctx.WITH()) is not None
        mark = self._(ctx.MARK()) is not None
        string = self._(ctx.STRING())
        commit = self._(ctx.COMMIT()) is not None
        delayed_durability = self._(ctx.DELAYED_DURABILITY()) is not None
        equal = self._(ctx.EQUAL()) is not None
        off = self._(ctx.OFF()) is not None
        on = self._(ctx.ON()) is not None
        rollback = self._(ctx.ROLLBACK()) is not None
        save = self._(ctx.SAVE()) is not None
        return TransactionStatement(begin, distributed, tran, transaction, id, local_id, with_, mark, string, commit, delayed_durability, equal, off, on, rollback, save)

    def visitGo_statement(self, ctx: tsql.Go_statementContext):
        count = self._(ctx.DECIMAL()) is not None
        return GoStatement(count)

    def visitUse_statement(self, ctx: tsql.Use_statementContext):
        database = self._(ctx.id_())
        return UseStatement(database)

    def visitSetuser_statement(self, ctx: tsql.Setuser_statementContext):
        user = self.repeated(ctx, tsql.STRINGContext)
        return SetuserStatement(user)

    def visitReconfigure_statement(self, ctx: tsql.Reconfigure_statementContext):
        with_ = self._(ctx.WITH()) is not None
        override = self._(ctx.OVERRIDE()) is not None
        return ReconfigureStatement(with_, override)

    def visitShutdown_statement(self, ctx: tsql.Shutdown_statementContext):
        with_ = self._(ctx.WITH()) is not None
        nowait = self._(ctx.NOWAIT()) is not None
        return ShutdownStatement(with_, nowait)

    def visitCheckpoint_statement(self, ctx: tsql.Checkpoint_statementContext):
        check_point_duration = self._(ctx.DECIMAL()) is not None
        return CheckpointStatement(check_point_duration)

    def visitDbcc_checkalloc_option(self, ctx: tsql.Dbcc_checkalloc_optionContext):
        all_errormsgs = self._(ctx.ALL_ERRORMSGS()) is not None
        no_infomsgs = self._(ctx.NO_INFOMSGS()) is not None
        tablock = self._(ctx.TABLOCK()) is not None
        estimateonly = self._(ctx.ESTIMATEONLY()) is not None
        return DbccCheckallocOption(all_errormsgs, no_infomsgs, tablock, estimateonly)

    def visitDbcc_checkalloc(self, ctx: tsql.Dbcc_checkallocContext):
        database = self._(ctx.id_())
        databaseid = self._(ctx.STRING())
        decimal = self._(ctx.DECIMAL()) is not None
        noindex = self._(ctx.NOINDEX()) is not None
        with_ = self._(ctx.WITH()) is not None
        dbcc_option = self._(ctx.dbcc_checkalloc_option())
        repair_allow_data_loss = self._(ctx.REPAIR_ALLOW_DATA_LOSS()) is not None
        repair_fast = self._(ctx.REPAIR_FAST()) is not None
        repair_rebuild = self._(ctx.REPAIR_REBUILD()) is not None
        return DbccCheckalloc(database, databaseid, decimal, noindex, with_, dbcc_option, repair_allow_data_loss, repair_fast, repair_rebuild)

    def visitDbcc_checkcatalog(self, ctx: tsql.Dbcc_checkcatalogContext):
        with_ = self._(ctx.WITH()) is not None
        dbcc_option = self._(ctx.NO_INFOMSGS()) is not None
        database = self._(ctx.id_())
        databasename = self._(ctx.STRING())
        decimal = self._(ctx.DECIMAL()) is not None
        return DbccCheckcatalog(with_, dbcc_option, database, databasename, decimal)

    def visitDbcc_checkconstraints_option(self, ctx: tsql.Dbcc_checkconstraints_optionContext):
        all_constraints = self._(ctx.ALL_CONSTRAINTS()) is not None
        all_errormsgs = self._(ctx.ALL_ERRORMSGS()) is not None
        no_infomsgs = self._(ctx.NO_INFOMSGS()) is not None
        return DbccCheckconstraintsOption(all_constraints, all_errormsgs, no_infomsgs)

    def visitDbcc_checkconstraints(self, ctx: tsql.Dbcc_checkconstraintsContext):
        with_ = self._(ctx.WITH()) is not None
        dbcc_option = self._(ctx.dbcc_checkconstraints_option())
        table_or_constraint = self._(ctx.id_())
        table_or_constraint_name = self._(ctx.STRING())
        return DbccCheckconstraints(with_, dbcc_option, table_or_constraint, table_or_constraint_name)

    def visitDbcc_checkdb_table_option(self, ctx: tsql.Dbcc_checkdb_table_optionContext):
        all_errormsgs = self._(ctx.ALL_ERRORMSGS()) is not None
        extended_logical_checks = self._(ctx.EXTENDED_LOGICAL_CHECKS()) is not None
        no_infomsgs = self._(ctx.NO_INFOMSGS()) is not None
        tablock = self._(ctx.TABLOCK()) is not None
        estimateonly = self._(ctx.ESTIMATEONLY()) is not None
        physical_only = self._(ctx.PHYSICAL_ONLY()) is not None
        data_purity = self._(ctx.DATA_PURITY()) is not None
        maxdop = self._(ctx.MAXDOP()) is not None
        max_dregree_of_parallelism = self._(ctx.DECIMAL()) is not None
        return DbccCheckdbTableOption(all_errormsgs, extended_logical_checks, no_infomsgs, tablock, estimateonly, physical_only, data_purity, maxdop, max_dregree_of_parallelism)

    def visitDbcc_checkdb(self, ctx: tsql.Dbcc_checkdbContext):
        with_ = self._(ctx.WITH()) is not None
        dbcc_option = self._(ctx.dbcc_checkdb_table_option())
        database = self._(ctx.id_())
        databasename = self._(ctx.STRING())
        decimal = self._(ctx.DECIMAL()) is not None
        noindex = self._(ctx.NOINDEX()) is not None
        repair_allow_data_loss = self._(ctx.REPAIR_ALLOW_DATA_LOSS()) is not None
        repair_fast = self._(ctx.REPAIR_FAST()) is not None
        repair_rebuild = self._(ctx.REPAIR_REBUILD()) is not None
        return DbccCheckdb(with_, dbcc_option, database, databasename, decimal, noindex, repair_allow_data_loss, repair_fast, repair_rebuild)

    def visitDbcc_checkfilegroup_option(self, ctx: tsql.Dbcc_checkfilegroup_optionContext):
        all_errormsgs = self._(ctx.ALL_ERRORMSGS()) is not None
        no_infomsgs = self._(ctx.NO_INFOMSGS()) is not None
        tablock = self._(ctx.TABLOCK()) is not None
        estimateonly = self._(ctx.ESTIMATEONLY()) is not None
        physical_only = self._(ctx.PHYSICAL_ONLY()) is not None
        maxdop = self._(ctx.MAXDOP()) is not None
        max_dregree_of_parallelism = self._(ctx.DECIMAL()) is not None
        return DbccCheckfilegroupOption(all_errormsgs, no_infomsgs, tablock, estimateonly, physical_only, maxdop, max_dregree_of_parallelism)

    def visitDbcc_checkfilegroup(self, ctx: tsql.Dbcc_checkfilegroupContext):
        with_ = self._(ctx.WITH()) is not None
        dbcc_option = self._(ctx.dbcc_checkfilegroup_option())
        filegroup_id = self._(ctx.DECIMAL()) is not None
        filegroup_name = self._(ctx.STRING())
        noindex = self._(ctx.NOINDEX()) is not None
        repair_allow_data_loss = self._(ctx.REPAIR_ALLOW_DATA_LOSS()) is not None
        repair_fast = self._(ctx.REPAIR_FAST()) is not None
        repair_rebuild = self._(ctx.REPAIR_REBUILD()) is not None
        return DbccCheckfilegroup(with_, dbcc_option, filegroup_id, filegroup_name, noindex, repair_allow_data_loss, repair_fast, repair_rebuild)

    def visitDbcc_checktable(self, ctx: tsql.Dbcc_checktableContext):
        table_or_view_name = self._(ctx.STRING())
        with_ = self._(ctx.WITH()) is not None
        dbcc_option = self._(ctx.dbcc_checkdb_table_option())
        noindex = self._(ctx.NOINDEX()) is not None
        index_id = self._(ctx.expression())
        repair_allow_data_loss = self._(ctx.REPAIR_ALLOW_DATA_LOSS()) is not None
        repair_fast = self._(ctx.REPAIR_FAST()) is not None
        repair_rebuild = self._(ctx.REPAIR_REBUILD()) is not None
        return DbccChecktable(table_or_view_name, with_, dbcc_option, noindex, index_id, repair_allow_data_loss, repair_fast, repair_rebuild)

    def visitDbcc_cleantable(self, ctx: tsql.Dbcc_cleantableContext):
        database = self._(ctx.id_())
        databasename = self._(ctx.STRING())
        decimal = self._(ctx.DECIMAL()) is not None
        with_ = self._(ctx.WITH()) is not None
        dbcc_option = self._(ctx.NO_INFOMSGS()) is not None
        return DbccCleantable(database, databasename, decimal, with_, dbcc_option)

    def visitDbcc_clonedatabase_option(self, ctx: tsql.Dbcc_clonedatabase_optionContext):
        no_statistics = self._(ctx.NO_STATISTICS()) is not None
        no_querystore = self._(ctx.NO_QUERYSTORE()) is not None
        servicebroker = self._(ctx.SERVICEBROKER()) is not None
        verify_clonedb = self._(ctx.VERIFY_CLONEDB()) is not None
        backup_clonedb = self._(ctx.BACKUP_CLONEDB()) is not None
        return DbccClonedatabaseOption(no_statistics, no_querystore, servicebroker, verify_clonedb, backup_clonedb)

    def visitDbcc_clonedatabase(self, ctx: tsql.Dbcc_clonedatabaseContext):
        source_database = self._(ctx.id_())
        with_ = self._(ctx.WITH()) is not None
        dbcc_option = self._(ctx.dbcc_clonedatabase_option())
        return DbccClonedatabase(source_database, with_, dbcc_option)

    def visitDbcc_pdw_showspaceused(self, ctx: tsql.Dbcc_pdw_showspaceusedContext):
        tablename = self._(ctx.id_())
        with_ = self._(ctx.WITH()) is not None
        dbcc_option = self._(ctx.IGNORE_REPLICATED_TABLE_CACHE()) is not None
        return DbccPdwShowspaceused(tablename, with_, dbcc_option)

    def visitDbcc_proccache(self, ctx: tsql.Dbcc_proccacheContext):
        with_ = self._(ctx.WITH()) is not None
        dbcc_option = self._(ctx.NO_INFOMSGS()) is not None
        return DbccProccache(with_, dbcc_option)

    def visitDbcc_showcontig_option(self, ctx: tsql.Dbcc_showcontig_optionContext):
        all_indexes = self._(ctx.ALL_INDEXES()) is not None
        tableresults = self._(ctx.TABLERESULTS()) is not None
        fast = self._(ctx.FAST()) is not None
        all_levels = self._(ctx.ALL_LEVELS()) is not None
        no_infomsgs = self._(ctx.NO_INFOMSGS()) is not None
        return DbccShowcontigOption(all_indexes, tableresults, fast, all_levels, no_infomsgs)

    def visitDbcc_showcontig(self, ctx: tsql.Dbcc_showcontigContext):
        table_or_view = self._(ctx.expression())
        with_ = self._(ctx.WITH()) is not None
        dbcc_option = self._(ctx.dbcc_showcontig_option())
        return DbccShowcontig(table_or_view, with_, dbcc_option)

    def visitDbcc_shrinklog(self, ctx: tsql.Dbcc_shrinklogContext):
        size = self._(ctx.SIZE()) is not None
        with_ = self._(ctx.WITH()) is not None
        dbcc_option = self._(ctx.NO_INFOMSGS()) is not None
        default_ = self._(ctx.DEFAULT()) is not None
        decimal = self._(ctx.DECIMAL()) is not None
        mb = self._(ctx.MB()) is not None
        gb = self._(ctx.GB()) is not None
        tb = self._(ctx.TB()) is not None
        return DbccShrinklog(size, with_, dbcc_option, default_, decimal, mb, gb, tb)

    def visitDbcc_dbreindex(self, ctx: tsql.Dbcc_dbreindexContext):
        table = self._(ctx.id_or_string())
        with_ = self._(ctx.WITH()) is not None
        dbcc_option = self._(ctx.NO_INFOMSGS()) is not None
        fillfactor = self._(ctx.expression())
        return DbccDbreindex(table, with_, dbcc_option, fillfactor)

    def visitDbcc_dll_free(self, ctx: tsql.Dbcc_dll_freeContext):
        dllname = self._(ctx.id_())
        with_ = self._(ctx.WITH()) is not None
        dbcc_option = self._(ctx.NO_INFOMSGS()) is not None
        return DbccDllFree(dllname, with_, dbcc_option)

    def visitDbcc_dropcleanbuffers(self, ctx: tsql.Dbcc_dropcleanbuffersContext):
        compute = self._(ctx.COMPUTE()) is not None
        all = self._(ctx.ALL()) is not None
        with_ = self._(ctx.WITH()) is not None
        dbcc_option = self._(ctx.NO_INFOMSGS()) is not None
        return DbccDropcleanbuffers(compute, all, with_, dbcc_option)

    def visitDbcc_clause(self, ctx: tsql.Dbcc_clauseContext):
        dbcc_checkalloc = self._(ctx.dbcc_checkalloc())
        dbcc_checkcatalog = self._(ctx.dbcc_checkcatalog())
        dbcc_checkconstraints = self._(ctx.dbcc_checkconstraints())
        dbcc_checkdb = self._(ctx.dbcc_checkdb())
        dbcc_checkfilegroup = self._(ctx.dbcc_checkfilegroup())
        dbcc_checktable = self._(ctx.dbcc_checktable())
        dbcc_cleantable = self._(ctx.dbcc_cleantable())
        dbcc_clonedatabase = self._(ctx.dbcc_clonedatabase())
        dbcc_dbreindex = self._(ctx.dbcc_dbreindex())
        dbcc_dll_free = self._(ctx.dbcc_dll_free())
        dbcc_dropcleanbuffers = self._(ctx.dbcc_dropcleanbuffers())
        dbcc_pdw_showspaceused = self._(ctx.dbcc_pdw_showspaceused())
        dbcc_proccache = self._(ctx.dbcc_proccache())
        dbcc_showcontig = self._(ctx.dbcc_showcontig())
        dbcc_shrinklog = self._(ctx.dbcc_shrinklog())
        return DbccClause(dbcc_checkalloc, dbcc_checkcatalog, dbcc_checkconstraints, dbcc_checkdb, dbcc_checkfilegroup, dbcc_checktable, dbcc_cleantable, dbcc_clonedatabase, dbcc_dbreindex, dbcc_dll_free, dbcc_dropcleanbuffers, dbcc_pdw_showspaceused, dbcc_proccache, dbcc_showcontig, dbcc_shrinklog)

    def visitExecute_clause(self, ctx: tsql.Execute_clauseContext):
        execute = self._(ctx.EXECUTE())
        execute_clause_clause = self._(ctx.execute_clause_clause())
        return ExecuteClause(execute, execute_clause_clause)

    def visitDeclare_local(self, ctx: tsql.Declare_localContext):
        local_id = self._(ctx.LOCAL_ID())
        data_type = self._(ctx.data_type())
        expression = self._(ctx.expression())
        return DeclareLocal(local_id, data_type, expression)

    def visitTable_type_definition(self, ctx: tsql.Table_type_definitionContext):
        column_def_table_constraints = self._(ctx.column_def_table_constraints())
        table_type_indices = self.repeated(ctx, tsql.Table_type_indicesContext)
        return TableTypeDefinition(column_def_table_constraints, table_type_indices)

    def visitTable_type_indices(self, ctx: tsql.Table_type_indicesContext):
        unique = self._(ctx.UNIQUE()) is not None
        column_name_list_with_order = self._(ctx.column_name_list_with_order())
        primary = self._(ctx.PRIMARY()) is not None
        key = self._(ctx.KEY()) is not None
        index = self._(ctx.INDEX()) is not None
        id = self._(ctx.id_())
        clustered = self._(ctx.CLUSTERED()) is not None
        nonclustered = self._(ctx.NONCLUSTERED()) is not None
        check = self._(ctx.CHECK()) is not None
        search_condition = self._(ctx.search_condition())
        return TableTypeIndices(unique, column_name_list_with_order, primary, key, index, id, clustered, nonclustered, check, search_condition)

    def visitXml_type_definition(self, ctx: tsql.Xml_type_definitionContext):
        content = self._(ctx.CONTENT()) is not None
        document = self._(ctx.DOCUMENT()) is not None
        xml_schema_collection = self._(ctx.xml_schema_collection())
        return XmlTypeDefinition(content, document, xml_schema_collection)

    def visitXml_schema_collection(self, ctx: tsql.Xml_schema_collectionContext):
        left = self._(ctx.ID(0))
        right = self._(ctx.ID(1))
        return XmlSchemaCollection(left, right)

    def visitColumn_def_table_constraints(self, ctx: tsql.Column_def_table_constraintsContext):
        left = self._(ctx.column_def_table_constraint(0))
        right = self.repeated(ctx, tsql.Column_def_table_constraintContext)
        return ColumnDefTableConstraints(left, right)

    def visitColumn_def_table_constraint(self, ctx: tsql.Column_def_table_constraintContext):
        column_definition = self._(ctx.column_definition())
        materialized_column_definition = self._(ctx.materialized_column_definition())
        table_constraint = self._(ctx.table_constraint())
        return ColumnDefTableConstraint(column_definition, materialized_column_definition, table_constraint)

    def visitColumn_definition(self, ctx: tsql.Column_definitionContext):
        id = self._(ctx.id_())
        data_type = self._(ctx.data_type())
        as_ = self._(ctx.AS()) is not None
        expression = self._(ctx.expression())
        persisted = self._(ctx.PERSISTED()) is not None
        column_definition_element = self.repeated(ctx, tsql.Column_definition_elementContext)
        column_index = self.repeated(ctx, tsql.Column_indexContext)
        return ColumnDefinition(id, data_type, as_, expression, persisted, column_definition_element, column_index)

    def visitColumn_definition_element(self, ctx: tsql.Column_definition_elementContext):
        filestream = self._(ctx.FILESTREAM()) is not None
        collate = self._(ctx.COLLATE()) is not None
        collation_name = self._(ctx.id_())
        sparse = self._(ctx.SPARSE()) is not None
        masked = self._(ctx.MASKED()) is not None
        with_ = self._(ctx.WITH()) is not None
        function = self._(ctx.FUNCTION()) is not None
        mask_function = self._(ctx.STRING())
        constraint = self._(ctx.CONSTRAINT()) is not None
        default_ = self._(ctx.DEFAULT()) is not None
        constant_expr = self._(ctx.expression())
        identity = self._(ctx.IDENTITY()) is not None
        seed = self._(ctx.DECIMAL()) is not None
        not_ = self._(ctx.NOT()) is not None
        for_ = self._(ctx.FOR()) is not None
        replication = self._(ctx.REPLICATION()) is not None
        generated = self._(ctx.GENERATED()) is not None
        always = self._(ctx.ALWAYS()) is not None
        as_ = self._(ctx.AS()) is not None
        row = self._(ctx.ROW()) is not None
        transaction_id = self._(ctx.TRANSACTION_ID()) is not None
        sequence_number = self._(ctx.SEQUENCE_NUMBER()) is not None
        start = self._(ctx.START()) is not None
        end = self._(ctx.END()) is not None
        rowguidcol = self._(ctx.ROWGUIDCOL()) is not None
        encrypted = self._(ctx.ENCRYPTED()) is not None
        column_encryption_key = self._(ctx.COLUMN_ENCRYPTION_KEY()) is not None
        encryption_type = self._(ctx.ENCRYPTION_TYPE()) is not None
        deterministic = self._(ctx.DETERMINISTIC()) is not None
        randomized = self._(ctx.RANDOMIZED()) is not None
        algorithm = self._(ctx.ALGORITHM()) is not None
        column_constraint = self._(ctx.column_constraint())
        return ColumnDefinitionElement(filestream, collate, collation_name, sparse, masked, with_, function, mask_function, constraint, default_, constant_expr, identity, seed, not_, for_, replication, generated, always, as_, row, transaction_id, sequence_number, start, end, rowguidcol, encrypted, column_encryption_key, encryption_type, deterministic, randomized, algorithm, column_constraint)

    def visitColumn_modifier(self, ctx: tsql.Column_modifierContext):
        id = self._(ctx.id_())
        add = self._(ctx.ADD()) is not None
        drop = self._(ctx.DROP()) is not None
        rowguidcol = self._(ctx.ROWGUIDCOL()) is not None
        persisted = self._(ctx.PERSISTED()) is not None
        not_ = self._(ctx.NOT()) is not None
        for_ = self._(ctx.FOR()) is not None
        replication = self._(ctx.REPLICATION()) is not None
        sparse = self._(ctx.SPARSE()) is not None
        hidden_keyword = self._(ctx.HIDDEN_KEYWORD()) is not None
        masked = self._(ctx.MASKED()) is not None
        with_ = self._(ctx.WITH()) is not None
        left = self._(ctx.FUNCTION()) is not None
        left = self._(ctx.EQUAL()) is not None
        left = self._(ctx.STRING(0))
        lr_bracket = self._(ctx.LR_BRACKET()) is not None
        right = self._(ctx.FUNCTION()) is not None
        right = self._(ctx.EQUAL()) is not None
        right = self._(ctx.STRING(1))
        rr_bracket = self._(ctx.RR_BRACKET()) is not None
        return ColumnModifier(id, add, drop, rowguidcol, persisted, not_, for_, replication, sparse, hidden_keyword, masked, with_, left, left, left, lr_bracket, right, right, right, rr_bracket)

    def visitMaterialized_column_definition(self, ctx: tsql.Materialized_column_definitionContext):
        id = self._(ctx.id_())
        compute = self._(ctx.COMPUTE()) is not None
        as_ = self._(ctx.AS()) is not None
        expression = self._(ctx.expression())
        left = self._(ctx.MATERIALIZED()) is not None
        not_ = self._(ctx.NOT()) is not None
        right = self._(ctx.MATERIALIZED()) is not None
        return MaterializedColumnDefinition(id, compute, as_, expression, left, not_, right)

    def visitColumn_constraint(self, ctx: tsql.Column_constraintContext):
        constraint = self._(ctx.CONSTRAINT()) is not None
        constraint = self._(ctx.id_())
        check_constraint = self._(ctx.check_constraint())
        clustered = self._(ctx.clustered())
        primary_key_options = self._(ctx.primary_key_options())
        foreign_key_options = self._(ctx.foreign_key_options())
        primary = self._(ctx.PRIMARY()) is not None
        left = self._(ctx.KEY()) is not None
        unique = self._(ctx.UNIQUE()) is not None
        foreign = self._(ctx.FOREIGN()) is not None
        right = self._(ctx.KEY()) is not None
        return ColumnConstraint(constraint, constraint, check_constraint, clustered, primary_key_options, foreign_key_options, primary, left, unique, foreign, right)

    def visitColumn_index(self, ctx: tsql.Column_indexContext):
        index_name = self._(ctx.id_())
        clustered = self.repeated(ctx, tsql.ClusteredContext)
        create_table_index_options = self.repeated(ctx, tsql.Create_table_index_optionsContext)
        on_partition_or_filegroup = self.repeated(ctx, tsql.On_partition_or_filegroupContext)
        filestream_on = self._(ctx.FILESTREAM_ON()) is not None
        null_double_quote = self._(ctx.NULL_DOUBLE_QUOTE())
        return ColumnIndex(index_name, clustered, create_table_index_options, on_partition_or_filegroup, filestream_on, null_double_quote)

    def visitOn_partition_or_filegroup(self, ctx: tsql.On_partition_or_filegroupContext):
        filegroup = self._(ctx.id_())
        default_double_quote = self._(ctx.DEFAULT_DOUBLE_QUOTE())
        return OnPartitionOrFilegroup(filegroup, default_double_quote)

    def visitTable_constraint(self, ctx: tsql.Table_constraintContext):
        constraint = self._(ctx.CONSTRAINT()) is not None
        constraint = self._(ctx.id_())
        check_constraint = self._(ctx.check_constraint())
        clustered = self._(ctx.clustered())
        column_name_list_with_order = self._(ctx.column_name_list_with_order())
        primary_key_options = self._(ctx.primary_key_options())
        foreign = self._(ctx.FOREIGN()) is not None
        left = self._(ctx.KEY()) is not None
        fk = self._(ctx.column_name_list())
        foreign_key_options = self._(ctx.foreign_key_options())
        connection = self._(ctx.CONNECTION()) is not None
        left = self._(ctx.connection_node(0))
        default_ = self._(ctx.DEFAULT()) is not None
        constant_expr = self._(ctx.expression())
        for_ = self._(ctx.FOR()) is not None
        primary = self._(ctx.PRIMARY()) is not None
        right = self._(ctx.KEY()) is not None
        unique = self._(ctx.UNIQUE()) is not None
        right = self.repeated(ctx, tsql.Connection_nodeContext)
        with_ = self._(ctx.WITH()) is not None
        values = self._(ctx.VALUES()) is not None
        return TableConstraint(constraint, constraint, check_constraint, clustered, column_name_list_with_order, primary_key_options, foreign, left, fk, foreign_key_options, connection, left, default_, constant_expr, for_, primary, right, unique, right, with_, values)

    def visitConnection_node(self, ctx: tsql.Connection_nodeContext):
        from_node_table = self._(ctx.id_())
        return ConnectionNode(from_node_table)

    def visitPrimary_key_options(self, ctx: tsql.Primary_key_optionsContext):
        with_ = self._(ctx.WITH()) is not None
        fillfactor = self._(ctx.FILLFACTOR()) is not None
        decimal = self._(ctx.DECIMAL()) is not None
        alter_table_index_options = self.repeated(ctx, tsql.Alter_table_index_optionsContext)
        on_partition_or_filegroup = self.repeated(ctx, tsql.On_partition_or_filegroupContext)
        return PrimaryKeyOptions(with_, fillfactor, decimal, alter_table_index_options, on_partition_or_filegroup)

    def visitForeign_key_options(self, ctx: tsql.Foreign_key_optionsContext):
        table_name = self._(ctx.table_name())
        pk = self._(ctx.column_name_list())
        on_delete = self.repeated(ctx, tsql.On_deleteContext)
        on_update = self.repeated(ctx, tsql.On_updateContext)
        not_ = self._(ctx.NOT()) is not None
        for_ = self._(ctx.FOR()) is not None
        replication = self._(ctx.REPLICATION()) is not None
        return ForeignKeyOptions(table_name, pk, on_delete, on_update, not_, for_, replication)

    def visitCheck_constraint(self, ctx: tsql.Check_constraintContext):
        not_ = self._(ctx.NOT()) is not None
        for_ = self._(ctx.FOR()) is not None
        replication = self._(ctx.REPLICATION()) is not None
        search_condition = self._(ctx.search_condition())
        return CheckConstraint(not_, for_, replication, search_condition)

    def visitOn_delete(self, ctx: tsql.On_deleteContext):
        no = self._(ctx.NO()) is not None
        action = self._(ctx.ACTION()) is not None
        cascade = self._(ctx.CASCADE()) is not None
        left = self._(ctx.SET()) is not None
        null = self._(ctx.NULL_()) is not None
        right = self._(ctx.SET()) is not None
        default_ = self._(ctx.DEFAULT()) is not None
        return OnDelete(no, action, cascade, left, null, right, default_)

    def visitOn_update(self, ctx: tsql.On_updateContext):
        no = self._(ctx.NO()) is not None
        action = self._(ctx.ACTION()) is not None
        cascade = self._(ctx.CASCADE()) is not None
        left = self._(ctx.SET()) is not None
        null = self._(ctx.NULL_()) is not None
        right = self._(ctx.SET()) is not None
        default_ = self._(ctx.DEFAULT()) is not None
        return OnUpdate(no, action, cascade, left, null, right, default_)

    def visitAlter_table_index_options(self, ctx: tsql.Alter_table_index_optionsContext):
        left = self._(ctx.alter_table_index_option(0))
        right = self.repeated(ctx, tsql.Alter_table_index_optionContext)
        return AlterTableIndexOptions(left, right)

    def visitAlter_table_index_option(self, ctx: tsql.Alter_table_index_optionContext):
        pad_index = self._(ctx.PAD_INDEX()) is not None
        on_off = self._(ctx.on_off())
        fillfactor = self._(ctx.FILLFACTOR()) is not None
        decimal = self._(ctx.DECIMAL()) is not None
        ignore_dup_key = self._(ctx.IGNORE_DUP_KEY()) is not None
        statistics_norecompute = self._(ctx.STATISTICS_NORECOMPUTE()) is not None
        allow_row_locks = self._(ctx.ALLOW_ROW_LOCKS()) is not None
        allow_page_locks = self._(ctx.ALLOW_PAGE_LOCKS()) is not None
        optimize_for_sequential_key = self._(ctx.OPTIMIZE_FOR_SEQUENTIAL_KEY()) is not None
        sort_in_tempdb = self._(ctx.SORT_IN_TEMPDB()) is not None
        maxdop = self._(ctx.MAXDOP()) is not None
        data_compression = self._(ctx.DATA_COMPRESSION()) is not None
        none = self._(ctx.NONE()) is not None
        row = self._(ctx.ROW()) is not None
        page = self._(ctx.PAGE()) is not None
        columnstore = self._(ctx.COLUMNSTORE()) is not None
        columnstore_archive = self._(ctx.COLUMNSTORE_ARCHIVE()) is not None
        on_partitions = self.repeated(ctx, tsql.On_partitionsContext)
        xml_compression = self._(ctx.XML_COMPRESSION()) is not None
        distribution = self._(ctx.DISTRIBUTION()) is not None
        hash = self._(ctx.HASH()) is not None
        id = self._(ctx.id_(0))
        clustered = self._(ctx.CLUSTERED()) is not None
        index = self._(ctx.INDEX()) is not None
        left = self._(ctx.ASC()) is not None
        left = self._(ctx.DESC()) is not None
        right = self.repeated(ctx, tsql.Id_Context)
        right = self._(ctx.ASC()) is not None
        right = self._(ctx.DESC()) is not None
        online = self._(ctx.ONLINE()) is not None
        on = self._(ctx.ON()) is not None
        off = self._(ctx.OFF()) is not None
        low_priority_lock_wait = self._(ctx.low_priority_lock_wait())
        resumable = self._(ctx.RESUMABLE()) is not None
        max_duration = self._(ctx.MAX_DURATION()) is not None
        return AlterTableIndexOption(pad_index, on_off, fillfactor, decimal, ignore_dup_key, statistics_norecompute, allow_row_locks, allow_page_locks, optimize_for_sequential_key, sort_in_tempdb, maxdop, data_compression, none, row, page, columnstore, columnstore_archive, on_partitions, xml_compression, distribution, hash, id, clustered, index, left, left, right, right, right, online, on, off, low_priority_lock_wait, resumable, max_duration)

    def visitDeclare_cursor(self, ctx: tsql.Declare_cursorContext):
        cursor_name = self._(ctx.cursor_name())
        left = self._(ctx.CURSOR()) is not None
        scroll = self._(ctx.SCROLL()) is not None
        right = self._(ctx.CURSOR()) is not None
        left = self._(ctx.FOR()) is not None
        select_statement_standalone = self._(ctx.select_statement_standalone())
        declare_set_cursor_common = self._(ctx.declare_set_cursor_common())
        semi_sensitive = self._(ctx.SEMI_SENSITIVE()) is not None
        insensitive = self._(ctx.INSENSITIVE()) is not None
        right = self._(ctx.FOR()) is not None
        third = self._(ctx.FOR()) is not None
        left = self._(ctx.UPDATE()) is not None
        read = self._(ctx.READ()) is not None
        only = self._(ctx.ONLY()) is not None
        right = self._(ctx.UPDATE()) is not None
        left = self._(ctx.OF()) is not None
        left = self._(ctx.column_name_list(0))
        right = self._(ctx.OF()) is not None
        right = self._(ctx.column_name_list(1))
        return DeclareCursor(cursor_name, left, scroll, right, left, select_statement_standalone, declare_set_cursor_common, semi_sensitive, insensitive, right, third, left, read, only, right, left, left, right, right)

    def visitDeclare_set_cursor_common(self, ctx: tsql.Declare_set_cursor_commonContext):
        declare_set_cursor_common_partial = self.repeated(ctx, tsql.Declare_set_cursor_common_partialContext)
        select_statement_standalone = self._(ctx.select_statement_standalone())
        return DeclareSetCursorCommon(declare_set_cursor_common_partial, select_statement_standalone)

    def visitDeclare_set_cursor_common_partial(self, ctx: tsql.Declare_set_cursor_common_partialContext):
        local = self._(ctx.LOCAL()) is not None
        global_ = self._(ctx.GLOBAL()) is not None
        forward_only = self._(ctx.FORWARD_ONLY()) is not None
        scroll = self._(ctx.SCROLL()) is not None
        static = self._(ctx.STATIC()) is not None
        keyset = self._(ctx.KEYSET()) is not None
        dynamic = self._(ctx.DYNAMIC()) is not None
        fast_forward = self._(ctx.FAST_FORWARD()) is not None
        read_only = self._(ctx.READ_ONLY()) is not None
        scroll_locks = self._(ctx.SCROLL_LOCKS()) is not None
        optimistic = self._(ctx.OPTIMISTIC()) is not None
        type_warning = self._(ctx.TYPE_WARNING()) is not None
        return DeclareSetCursorCommonPartial(local, global_, forward_only, scroll, static, keyset, dynamic, fast_forward, read_only, scroll_locks, optimistic, type_warning)

    def visitFetch_cursor(self, ctx: tsql.Fetch_cursorContext):
        from_ = self._(ctx.FROM()) is not None
        cursor_name = self._(ctx.cursor_name())
        into = self._(ctx.INTO()) is not None
        left = self._(ctx.LOCAL_ID(0))
        next = self._(ctx.NEXT()) is not None
        prior = self._(ctx.PRIOR()) is not None
        first = self._(ctx.FIRST()) is not None
        last = self._(ctx.LAST()) is not None
        expression = self._(ctx.expression())
        right = self.repeated(ctx, tsql.LOCAL_IDContext)
        absolute = self._(ctx.ABSOLUTE()) is not None
        relative = self._(ctx.RELATIVE()) is not None
        return FetchCursor(from_, cursor_name, into, left, next, prior, first, last, expression, right, absolute, relative)

    def visitSet_special(self, ctx: tsql.Set_specialContext):
        set = self._(ctx.SET()) is not None
        left = self._(ctx.id_(0))
        right = self._(ctx.id_(1))
        constant_local_id = self._(ctx.constant_LOCAL_ID())
        on_off = self._(ctx.on_off())
        statistics = self._(ctx.STATISTICS()) is not None
        io = self._(ctx.IO()) is not None
        time = self._(ctx.TIME()) is not None
        xml = self._(ctx.XML()) is not None
        profile = self._(ctx.PROFILE()) is not None
        rowcount = self._(ctx.ROWCOUNT()) is not None
        local_id = self._(ctx.LOCAL_ID())
        decimal = self._(ctx.DECIMAL()) is not None
        textsize = self._(ctx.TEXTSIZE()) is not None
        transaction = self._(ctx.TRANSACTION()) is not None
        isolation = self._(ctx.ISOLATION()) is not None
        level = self._(ctx.LEVEL()) is not None
        left = self._(ctx.READ()) is not None
        uncommitted = self._(ctx.UNCOMMITTED()) is not None
        right = self._(ctx.READ()) is not None
        committed = self._(ctx.COMMITTED()) is not None
        repeatable = self._(ctx.REPEATABLE()) is not None
        third = self._(ctx.READ()) is not None
        snapshot = self._(ctx.SNAPSHOT()) is not None
        serializable = self._(ctx.SERIALIZABLE()) is not None
        identity_insert = self._(ctx.IDENTITY_INSERT()) is not None
        table_name = self._(ctx.table_name())
        left = self._(ctx.special_list(0))
        right = self.repeated(ctx, tsql.Special_listContext)
        modify_method = self._(ctx.modify_method())
        return SetSpecial(set, left, right, constant_local_id, on_off, statistics, io, time, xml, profile, rowcount, local_id, decimal, textsize, transaction, isolation, level, left, uncommitted, right, committed, repeatable, third, snapshot, serializable, identity_insert, table_name, left, right, modify_method)

    def visitSpecial_list(self, ctx: tsql.Special_listContext):
        ansi_nulls = self._(ctx.ANSI_NULLS()) is not None
        quoted_identifier = self._(ctx.QUOTED_IDENTIFIER()) is not None
        ansi_padding = self._(ctx.ANSI_PADDING()) is not None
        ansi_warnings = self._(ctx.ANSI_WARNINGS()) is not None
        ansi_defaults = self._(ctx.ANSI_DEFAULTS()) is not None
        ansi_null_dflt_off = self._(ctx.ANSI_NULL_DFLT_OFF()) is not None
        ansi_null_dflt_on = self._(ctx.ANSI_NULL_DFLT_ON()) is not None
        arithabort = self._(ctx.ARITHABORT()) is not None
        arithignore = self._(ctx.ARITHIGNORE()) is not None
        concat_null_yields_null = self._(ctx.CONCAT_NULL_YIELDS_NULL()) is not None
        cursor_close_on_commit = self._(ctx.CURSOR_CLOSE_ON_COMMIT()) is not None
        fmtonly = self._(ctx.FMTONLY()) is not None
        forceplan = self._(ctx.FORCEPLAN()) is not None
        implicit_transactions = self._(ctx.IMPLICIT_TRANSACTIONS()) is not None
        nocount = self._(ctx.NOCOUNT()) is not None
        noexec = self._(ctx.NOEXEC()) is not None
        numeric_roundabort = self._(ctx.NUMERIC_ROUNDABORT()) is not None
        parseonly = self._(ctx.PARSEONLY()) is not None
        remote_proc_transactions = self._(ctx.REMOTE_PROC_TRANSACTIONS()) is not None
        showplan_all = self._(ctx.SHOWPLAN_ALL()) is not None
        showplan_text = self._(ctx.SHOWPLAN_TEXT()) is not None
        showplan_xml = self._(ctx.SHOWPLAN_XML()) is not None
        xact_abort = self._(ctx.XACT_ABORT()) is not None
        return SpecialList(ansi_nulls, quoted_identifier, ansi_padding, ansi_warnings, ansi_defaults, ansi_null_dflt_off, ansi_null_dflt_on, arithabort, arithignore, concat_null_yields_null, cursor_close_on_commit, fmtonly, forceplan, implicit_transactions, nocount, noexec, numeric_roundabort, parseonly, remote_proc_transactions, showplan_all, showplan_text, showplan_xml, xact_abort)

    def visitConstant_LOCAL_ID(self, ctx: tsql.Constant_LOCAL_IDContext):
        constant = self._(ctx.constant())
        local_id = self._(ctx.LOCAL_ID())
        return ConstantLocalId(constant, local_id)

    def visitExpression(self, ctx: tsql.ExpressionContext):
        primitive_expression = self._(ctx.primitive_expression())
        function_call = self._(ctx.function_call())
        expression = self._(ctx.expression(0))
        value_call = self._(ctx.value_call())
        query_call = self._(ctx.query_call())
        exist_call = self._(ctx.exist_call())
        modify_call = self._(ctx.modify_call())
        hierarchyid_call = self._(ctx.hierarchyid_call())
        collate = self._(ctx.COLLATE()) is not None
        id = self._(ctx.id_())
        case_expression = self._(ctx.case_expression())
        full_column_name = self._(ctx.full_column_name())
        bracket_expression = self._(ctx.bracket_expression())
        unary_operator_expression = self._(ctx.unary_operator_expression())
        right = self._(ctx.expression(1))
        time_zone = self._(ctx.time_zone())
        over_clause = self._(ctx.over_clause())
        dollar_action = self._(ctx.DOLLAR_ACTION()) is not None
        return Expression(primitive_expression, function_call, expression, value_call, query_call, exist_call, modify_call, hierarchyid_call, collate, id, case_expression, full_column_name, bracket_expression, unary_operator_expression, right, time_zone, over_clause, dollar_action)

    def visitTime_zone(self, ctx: tsql.Time_zoneContext):
        expression = self._(ctx.expression())
        return TimeZone(expression)

    def visitPrimitive_expression(self, ctx: tsql.Primitive_expressionContext):
        default_ = self._(ctx.DEFAULT()) is not None
        null = self._(ctx.NULL_()) is not None
        local_id = self._(ctx.LOCAL_ID())
        primitive_constant = self._(ctx.primitive_constant())
        return PrimitiveExpression(default_, null, local_id, primitive_constant)

    def visitCase_expression(self, ctx: tsql.Case_expressionContext):
        case_ = self._(ctx.CASE()) is not None
        case_expr = self._(ctx.expression())
        switch_section = self._(ctx.switch_section())
        else_ = self._(ctx.ELSE()) is not None
        end = self._(ctx.END()) is not None
        switch_search_condition_section = self._(ctx.switch_search_condition_section())
        return CaseExpression(case_, case_expr, switch_section, else_, end, switch_search_condition_section)

    def visitUnary_operator_expression(self, ctx: tsql.Unary_operator_expressionContext):
        expression = self._(ctx.expression())
        return UnaryOperatorExpression(expression)

    def visitBracket_expression(self, ctx: tsql.Bracket_expressionContext):
        expression = self._(ctx.expression())
        subquery = self._(ctx.subquery())
        return BracketExpression(expression, subquery)

    def visitWith_expression(self, ctx: tsql.With_expressionContext):
        ctes = self._(ctx.common_table_expression())
        return WithExpression(ctes)

    def visitCommon_table_expression(self, ctx: tsql.Common_table_expressionContext):
        expression_name = self._(ctx.id_())
        columns = self._(ctx.column_name_list())
        cte_query = self._(ctx.select_statement())
        return CommonTableExpression(expression_name, columns, cte_query)

    def visitUpdate_elem(self, ctx: tsql.Update_elemContext):
        local_id = self._(ctx.LOCAL_ID())
        full_column_name = self._(ctx.full_column_name())
        expression = self._(ctx.expression())
        udt_column_name = self._(ctx.id_())
        expression_list = self._(ctx.expression_list_())
        return UpdateElem(local_id, full_column_name, expression, udt_column_name, expression_list)

    def visitUpdate_elem_merge(self, ctx: tsql.Update_elem_mergeContext):
        full_column_name = self._(ctx.full_column_name())
        local_id = self._(ctx.LOCAL_ID())
        expression = self._(ctx.expression())
        udt_column_name = self._(ctx.id_())
        expression_list = self._(ctx.expression_list_())
        return UpdateElemMerge(full_column_name, local_id, expression, udt_column_name, expression_list)

    def visitSearch_condition(self, ctx: tsql.Search_conditionContext):
        predicate = self._(ctx.predicate())
        search_condition = self._(ctx.search_condition(0))
        and_ = self._(ctx.AND()) is not None
        right = self._(ctx.search_condition(1))
        or_ = self._(ctx.OR()) is not None
        return SearchCondition(predicate, search_condition, and_, right, or_)

    def visitPredicate(self, ctx: tsql.PredicateContext):
        exists = self._(ctx.EXISTS()) is not None
        subquery = self._(ctx.subquery())
        freetext_predicate = self._(ctx.freetext_predicate())
        left = self._(ctx.expression(0))
        right = self._(ctx.expression(1))
        mult_assign = self._(ctx.MULT_ASSIGN()) is not None
        all = self._(ctx.ALL()) is not None
        some = self._(ctx.SOME()) is not None
        any = self._(ctx.ANY()) is not None
        between = self._(ctx.BETWEEN()) is not None
        and_ = self._(ctx.AND()) is not None
        third = self._(ctx.expression(2))
        in_ = self._(ctx.IN()) is not None
        expression_list = self._(ctx.expression_list_())
        like = self._(ctx.LIKE()) is not None
        escape = self._(ctx.ESCAPE()) is not None
        is_ = self._(ctx.IS()) is not None
        return Predicate(exists, subquery, freetext_predicate, left, right, mult_assign, all, some, any, between, and_, third, in_, expression_list, like, escape, is_)

    def visitQuery_expression(self, ctx: tsql.Query_expressionContext):
        query_specification = self._(ctx.query_specification())
        select_order_by_clause = self.repeated(ctx, tsql.Select_order_by_clauseContext)
        unions = self.repeated(ctx, tsql.Sql_unionContext)
        left = self._(ctx.query_expression(0))
        union = self._(ctx.UNION()) is not None
        all = self._(ctx.ALL()) is not None
        right = self._(ctx.query_expression(1))
        return QueryExpression(query_specification, select_order_by_clause, unions, left, union, all, right)

    def visitSql_union(self, ctx: tsql.Sql_unionContext):
        union = self._(ctx.UNION()) is not None
        all = self._(ctx.ALL()) is not None
        except_ = self._(ctx.EXCEPT()) is not None
        intersect = self._(ctx.INTERSECT()) is not None
        spec = self._(ctx.query_specification())
        op = self._(ctx.query_expression())
        return SqlUnion(union, all, except_, intersect, spec, op)

    def visitQuery_specification(self, ctx: tsql.Query_specificationContext):
        top = self.repeated(ctx, tsql.Top_clauseContext)
        columns = self._(ctx.select_list())
        into = self._(ctx.INTO()) is not None
        into = self._(ctx.table_name())
        from_ = self._(ctx.FROM()) is not None
        from_ = self._(ctx.table_sources())
        where = self._(ctx.WHERE()) is not None
        where = self._(ctx.search_condition())
        group = self._(ctx.GROUP()) is not None
        by = self._(ctx.BY()) is not None
        having = self._(ctx.HAVING()) is not None
        grouping = self._(ctx.GROUPING()) is not None
        sets = self._(ctx.SETS()) is not None
        group_sets = self._(ctx.grouping_sets_item())
        group_by_all = self._(ctx.ALL()) is not None
        group_bys = self._(ctx.group_by_item())
        return QuerySpecification(top, columns, into, into, from_, from_, where, where, group, by, having, grouping, sets, group_sets, group_by_all, group_bys)

    def visitTop_clause(self, ctx: tsql.Top_clauseContext):
        top_percent = self._(ctx.top_percent())
        top_count = self._(ctx.top_count())
        with_ = self._(ctx.WITH()) is not None
        ties = self._(ctx.TIES()) is not None
        return TopClause(top_percent, top_count, with_, ties)

    def visitTop_percent(self, ctx: tsql.Top_percentContext):
        top_percent_percent_constant = self._(ctx.top_percent_percent_constant())
        percent = self._(ctx.PERCENT()) is not None
        topper_expression = self._(ctx.expression())
        return TopPercent(top_percent_percent_constant, percent, topper_expression)

    def visitTop_count(self, ctx: tsql.Top_countContext):
        count_constant = self._(ctx.DECIMAL()) is not None
        topcount_expression = self._(ctx.expression())
        return TopCount(count_constant, topcount_expression)

    def visitOrder_by_clause(self, ctx: tsql.Order_by_clauseContext):
        order_bys = self._(ctx.order_by_expression())
        return OrderByClause(order_bys)

    def visitSelect_order_by_clause(self, ctx: tsql.Select_order_by_clauseContext):
        order_by_clause = self._(ctx.order_by_clause())
        offset = self._(ctx.OFFSET()) is not None
        offset_exp = self._(ctx.expression())
        select_order_by_clause_offset_rows = self._(ctx.select_order_by_clause_offset_rows())
        fetch = self._(ctx.FETCH()) is not None
        select_order_by_clause_fetch_offset = self._(ctx.select_order_by_clause_fetch_offset())
        select_order_by_clause_fetch_rows = self._(ctx.select_order_by_clause_fetch_rows())
        only = self._(ctx.ONLY()) is not None
        return SelectOrderByClause(order_by_clause, offset, offset_exp, select_order_by_clause_offset_rows, fetch, select_order_by_clause_fetch_offset, select_order_by_clause_fetch_rows, only)

    def visitFor_clause(self, ctx: tsql.For_clauseContext):
        for_ = self._(ctx.FOR()) is not None
        browse = self._(ctx.BROWSE()) is not None
        xml = self._(ctx.XML()) is not None
        raw = self._(ctx.RAW()) is not None
        auto = self._(ctx.AUTO()) is not None
        xml_common_directives = self.repeated(ctx, tsql.Xml_common_directivesContext)
        left = self._(ctx.COMMA()) is not None
        right = self._(ctx.COMMA()) is not None
        elements = self._(ctx.ELEMENTS()) is not None
        left = self._(ctx.STRING(0))
        xmldata = self._(ctx.XMLDATA()) is not None
        xmlschema = self._(ctx.XMLSCHEMA()) is not None
        xsinil = self._(ctx.XSINIL()) is not None
        absent = self._(ctx.ABSENT()) is not None
        right = self._(ctx.STRING(1))
        explicit = self._(ctx.EXPLICIT()) is not None
        path = self._(ctx.PATH()) is not None
        json = self._(ctx.JSON()) is not None
        root = self._(ctx.ROOT()) is not None
        include_null_values = self._(ctx.INCLUDE_NULL_VALUES()) is not None
        without_array_wrapper = self._(ctx.WITHOUT_ARRAY_WRAPPER()) is not None
        return ForClause(for_, browse, xml, raw, auto, xml_common_directives, left, right, elements, left, xmldata, xmlschema, xsinil, absent, right, explicit, path, json, root, include_null_values, without_array_wrapper)

    def visitXml_common_directives(self, ctx: tsql.Xml_common_directivesContext):
        binary_keyword = self._(ctx.BINARY_KEYWORD()) is not None
        base64 = self._(ctx.BASE64()) is not None
        type_ = self._(ctx.TYPE()) is not None
        root = self._(ctx.ROOT()) is not None
        string = self._(ctx.STRING())
        return XmlCommonDirectives(binary_keyword, base64, type_, root, string)

    def visitOrder_by_expression(self, ctx: tsql.Order_by_expressionContext):
        order_by = self._(ctx.expression())
        ascending = self._(ctx.ASC()) is not None
        descending = self._(ctx.DESC()) is not None
        return OrderByExpression(order_by, ascending, descending)

    def visitGrouping_sets_item(self, ctx: tsql.Grouping_sets_itemContext):
        group_set_items = self._(ctx.group_by_item())
        return GroupingSetsItem(group_set_items)

    def visitOption_clause(self, ctx: tsql.Option_clauseContext):
        options = self._(ctx.option())
        return OptionClause(options)

    def visitOption(self, ctx: tsql.OptionContext):
        fast = self._(ctx.FAST()) is not None
        number_rows = self._(ctx.DECIMAL()) is not None
        hash = self._(ctx.HASH()) is not None
        order = self._(ctx.ORDER()) is not None
        group = self._(ctx.GROUP()) is not None
        merge = self._(ctx.MERGE()) is not None
        concat = self._(ctx.CONCAT()) is not None
        union = self._(ctx.UNION()) is not None
        loop = self._(ctx.LOOP()) is not None
        join = self._(ctx.JOIN()) is not None
        expand = self._(ctx.EXPAND()) is not None
        views = self._(ctx.VIEWS()) is not None
        force = self._(ctx.FORCE()) is not None
        ignore_nonclustered_columnstore_index = self._(ctx.IGNORE_NONCLUSTERED_COLUMNSTORE_INDEX()) is not None
        keep = self._(ctx.KEEP()) is not None
        plan = self._(ctx.PLAN()) is not None
        keepfixed = self._(ctx.KEEPFIXED()) is not None
        maxdop = self._(ctx.MAXDOP()) is not None
        maxrecursion = self._(ctx.MAXRECURSION()) is not None
        optimize = self._(ctx.OPTIMIZE()) is not None
        for_ = self._(ctx.FOR()) is not None
        left = self._(ctx.optimize_for_arg(0))
        right = self.repeated(ctx, tsql.Optimize_for_argContext)
        unknown = self._(ctx.UNKNOWN()) is not None
        parameterization = self._(ctx.PARAMETERIZATION()) is not None
        simple = self._(ctx.SIMPLE()) is not None
        forced = self._(ctx.FORCED()) is not None
        recompile = self._(ctx.RECOMPILE()) is not None
        robust = self._(ctx.ROBUST()) is not None
        use = self._(ctx.USE()) is not None
        string = self._(ctx.STRING())
        return Option(fast, number_rows, hash, order, group, merge, concat, union, loop, join, expand, views, force, ignore_nonclustered_columnstore_index, keep, plan, keepfixed, maxdop, maxrecursion, optimize, for_, left, right, unknown, parameterization, simple, forced, recompile, robust, use, string)

    def visitOptimize_for_arg(self, ctx: tsql.Optimize_for_argContext):
        local_id = self._(ctx.LOCAL_ID())
        unknown = self._(ctx.UNKNOWN()) is not None
        constant = self._(ctx.constant())
        null = self._(ctx.NULL_()) is not None
        return OptimizeForArg(local_id, unknown, constant, null)

    def visitSelect_list(self, ctx: tsql.Select_listContext):
        select_element = self._(ctx.select_list_elem())
        return SelectList(select_element)

    def visitUdt_method_arguments(self, ctx: tsql.Udt_method_argumentsContext):
        argument = self._(ctx.execute_var_string())
        return UdtMethodArguments(argument)

    def visitAsterisk(self, ctx: tsql.AsteriskContext):
        table_name = self._(ctx.table_name())
        inserted = self._(ctx.INSERTED()) is not None
        deleted = self._(ctx.DELETED()) is not None
        return Asterisk(table_name, inserted, deleted)

    def visitUdt_elem(self, ctx: tsql.Udt_elemContext):
        udt_column_name = self._(ctx.id_())
        udt_method_arguments = self._(ctx.udt_method_arguments())
        as_column_alias = self.repeated(ctx, tsql.As_column_aliasContext)
        double_colon = self._(ctx.DOUBLE_COLON()) is not None
        return UdtElem(udt_column_name, udt_method_arguments, as_column_alias, double_colon)

    def visitExpression_elem(self, ctx: tsql.Expression_elemContext):
        left_alias = self._(ctx.column_alias())
        left_assignment = self._(ctx.expression())
        as_column_alias = self.repeated(ctx, tsql.As_column_aliasContext)
        return ExpressionElem(left_alias, left_assignment, as_column_alias)

    def visitSelect_list_elem(self, ctx: tsql.Select_list_elemContext):
        asterisk = self._(ctx.asterisk())
        udt_elem = self._(ctx.udt_elem())
        local_id = self._(ctx.LOCAL_ID())
        expression = self._(ctx.expression())
        expression_elem = self._(ctx.expression_elem())
        return SelectListElem(asterisk, udt_elem, local_id, expression, expression_elem)

    def visitTable_sources(self, ctx: tsql.Table_sourcesContext):
        non_ansi_join = self._(ctx.non_ansi_join())
        source = self._(ctx.table_source())
        return TableSources(non_ansi_join, source)

    def visitNon_ansi_join(self, ctx: tsql.Non_ansi_joinContext):
        source = self._(ctx.table_source())
        return NonAnsiJoin(source)

    def visitTable_source(self, ctx: tsql.Table_sourceContext):
        table_source_item = self._(ctx.table_source_item())
        joins = self.repeated(ctx, tsql.Join_partContext)
        return TableSource(table_source_item, joins)

    def visitTable_source_item(self, ctx: tsql.Table_source_itemContext):
        full_table_name = self._(ctx.full_table_name())
        deprecated_table_hint = self._(ctx.deprecated_table_hint())
        as_table_alias = self._(ctx.as_table_alias())
        with_table_hints = self._(ctx.with_table_hints())
        sybase_legacy_hints = self._(ctx.sybase_legacy_hints())
        rowset_function = self._(ctx.rowset_function())
        derived_table = self._(ctx.derived_table())
        column_alias_list = self._(ctx.column_alias_list())
        change_table = self._(ctx.change_table())
        nodes_method = self._(ctx.nodes_method())
        function_call = self._(ctx.function_call())
        loc_id = self._(ctx.LOCAL_ID())
        open_xml = self._(ctx.open_xml())
        open_json = self._(ctx.open_json())
        double_colon = self._(ctx.DOUBLE_COLON()) is not None
        table_source = self._(ctx.table_source())
        return TableSourceItem(full_table_name, deprecated_table_hint, as_table_alias, with_table_hints, sybase_legacy_hints, rowset_function, derived_table, column_alias_list, change_table, nodes_method, function_call, loc_id, open_xml, open_json, double_colon, table_source)

    def visitOpen_xml(self, ctx: tsql.Open_xmlContext):
        left = self._(ctx.expression(0))
        right = self._(ctx.expression(1))
        third = self._(ctx.expression(2))
        with_ = self._(ctx.WITH()) is not None
        schema_declaration = self._(ctx.schema_declaration())
        as_table_alias = self.repeated(ctx, tsql.As_table_aliasContext)
        return OpenXml(left, right, third, with_, schema_declaration, as_table_alias)

    def visitOpen_json(self, ctx: tsql.Open_jsonContext):
        left = self._(ctx.expression(0))
        right = self._(ctx.expression(1))
        with_ = self._(ctx.WITH()) is not None
        json_declaration = self._(ctx.json_declaration())
        as_table_alias = self.repeated(ctx, tsql.As_table_aliasContext)
        return OpenJson(left, right, with_, json_declaration, as_table_alias)

    def visitJson_declaration(self, ctx: tsql.Json_declarationContext):
        json_col = self._(ctx.json_column_declaration())
        return JsonDeclaration(json_col)

    def visitJson_column_declaration(self, ctx: tsql.Json_column_declarationContext):
        column_declaration = self._(ctx.column_declaration())
        as_ = self._(ctx.AS()) is not None
        json = self._(ctx.JSON()) is not None
        return JsonColumnDeclaration(column_declaration, as_, json)

    def visitSchema_declaration(self, ctx: tsql.Schema_declarationContext):
        xml_col = self._(ctx.column_declaration())
        return SchemaDeclaration(xml_col)

    def visitColumn_declaration(self, ctx: tsql.Column_declarationContext):
        id = self._(ctx.id_())
        data_type = self._(ctx.data_type())
        string = self.repeated(ctx, tsql.STRINGContext)
        return ColumnDeclaration(id, data_type, string)

    def visitChange_table(self, ctx: tsql.Change_tableContext):
        change_table_changes = self._(ctx.change_table_changes())
        change_table_version = self._(ctx.change_table_version())
        return ChangeTable(change_table_changes, change_table_version)

    def visitChange_table_changes(self, ctx: tsql.Change_table_changesContext):
        changetable = self._(ctx.table_name())
        change_table_changes_changesid = self._(ctx.change_table_changes_changesid())
        return ChangeTableChanges(changetable, change_table_changes_changesid)

    def visitChange_table_version(self, ctx: tsql.Change_table_versionContext):
        versiontable = self._(ctx.table_name())
        pk_columns = self._(ctx.full_column_name_list())
        pk_values = self._(ctx.select_list())
        return ChangeTableVersion(versiontable, pk_columns, pk_values)

    def visitJoin_part(self, ctx: tsql.Join_partContext):
        join_on = self._(ctx.join_on())
        cross_join = self._(ctx.cross_join())
        apply = self._(ctx.apply_())
        pivot = self._(ctx.pivot())
        unpivot = self._(ctx.unpivot())
        return JoinPart(join_on, cross_join, apply, pivot, unpivot)

    def visitJoin_on(self, ctx: tsql.Join_onContext):
        inner = self._(ctx.INNER()) is not None
        join_on_join_type = self._(ctx.join_on_join_type())
        outer = self._(ctx.OUTER()) is not None
        join_on_join_hint = self._(ctx.join_on_join_hint())
        source = self._(ctx.table_source())
        cond = self._(ctx.search_condition())
        return JoinOn(inner, join_on_join_type, outer, join_on_join_hint, source, cond)

    def visitCross_join(self, ctx: tsql.Cross_joinContext):
        table_source_item = self._(ctx.table_source_item())
        return CrossJoin(table_source_item)

    def visitApply_(self, ctx: tsql.Apply_Context):
        apply_apply_style = self._(ctx.apply__apply_style())
        source = self._(ctx.table_source_item())
        return Apply(apply_apply_style, source)

    def visitPivot(self, ctx: tsql.PivotContext):
        pivot_clause = self._(ctx.pivot_clause())
        as_table_alias = self._(ctx.as_table_alias())
        return Pivot(pivot_clause, as_table_alias)

    def visitUnpivot(self, ctx: tsql.UnpivotContext):
        unpivot_clause = self._(ctx.unpivot_clause())
        as_table_alias = self._(ctx.as_table_alias())
        return Unpivot(unpivot_clause, as_table_alias)

    def visitPivot_clause(self, ctx: tsql.Pivot_clauseContext):
        aggregate_windowed_function = self._(ctx.aggregate_windowed_function())
        full_column_name = self._(ctx.full_column_name())
        column_alias_list = self._(ctx.column_alias_list())
        return PivotClause(aggregate_windowed_function, full_column_name, column_alias_list)

    def visitUnpivot_clause(self, ctx: tsql.Unpivot_clauseContext):
        unpivot_exp = self._(ctx.expression())
        full_column_name = self._(ctx.full_column_name())
        full_column_name_list = self._(ctx.full_column_name_list())
        return UnpivotClause(unpivot_exp, full_column_name, full_column_name_list)

    def visitFull_column_name_list(self, ctx: tsql.Full_column_name_listContext):
        column = self._(ctx.full_column_name())
        return FullColumnNameList(column)

    def visitRowset_function(self, ctx: tsql.Rowset_functionContext):
        openrowset = self._(ctx.OPENROWSET()) is not None
        lr_bracket = self._(ctx.LR_BRACKET()) is not None
        provider_name = self._(ctx.STRING())
        left = self._(ctx.COMMA()) is not None
        right = self._(ctx.COMMA()) is not None
        rr_bracket = self._(ctx.RR_BRACKET()) is not None
        bulk = self._(ctx.BULK()) is not None
        left = self._(ctx.bulk_option(0))
        id = self._(ctx.id_())
        right = self.repeated(ctx, tsql.Bulk_optionContext)
        return RowsetFunction(openrowset, lr_bracket, provider_name, left, right, rr_bracket, bulk, left, id, right)

    def visitBulk_option(self, ctx: tsql.Bulk_optionContext):
        id = self._(ctx.id_())
        bulk_option_bulk_option_value = self._(ctx.bulk_option_bulk_option_value())
        return BulkOption(id, bulk_option_bulk_option_value)

    def visitDerived_table(self, ctx: tsql.Derived_tableContext):
        subquery = self._(ctx.subquery(0))
        right = self.repeated(ctx, tsql.SubqueryContext)
        table_value_constructor = self._(ctx.table_value_constructor())
        return DerivedTable(subquery, right, table_value_constructor)

    def visitFunction_call(self, ctx: tsql.Function_callContext):
        ranking_windowed_function = self._(ctx.ranking_windowed_function())
        aggregate_windowed_function = self._(ctx.aggregate_windowed_function())
        analytic_windowed_function = self._(ctx.analytic_windowed_function())
        built_in_functions = self._(ctx.built_in_functions())
        scalar_function_name = self._(ctx.scalar_function_name())
        expression_list = self.repeated(ctx, tsql.Expression_list_Context)
        freetext_function = self._(ctx.freetext_function())
        partition_function = self._(ctx.partition_function())
        hierarchyid_static_method = self._(ctx.hierarchyid_static_method())
        return FunctionCall(ranking_windowed_function, aggregate_windowed_function, analytic_windowed_function, built_in_functions, scalar_function_name, expression_list, freetext_function, partition_function, hierarchyid_static_method)

    def visitPartition_function(self, ctx: tsql.Partition_functionContext):
        database = self._(ctx.id_())
        expression = self._(ctx.expression())
        return PartitionFunction(database, expression)

    def visitFreetext_function(self, ctx: tsql.Freetext_functionContext):
        containstable = self._(ctx.CONTAINSTABLE()) is not None
        freetexttable = self._(ctx.FREETEXTTABLE()) is not None
        table_name = self._(ctx.table_name())
        left = self._(ctx.full_column_name(0))
        right = self._(ctx.full_column_name(1))
        left = self._(ctx.expression(0))
        language = self._(ctx.LANGUAGE()) is not None
        right = self._(ctx.expression(1))
        third = self._(ctx.expression(2))
        third = self.repeated(ctx, tsql.Full_column_nameContext)
        semanticsimilaritytable = self._(ctx.SEMANTICSIMILARITYTABLE()) is not None
        semantickeyphrasetable = self._(ctx.SEMANTICKEYPHRASETABLE()) is not None
        semanticsimilaritydetailstable = self._(ctx.SEMANTICSIMILARITYDETAILSTABLE()) is not None
        return FreetextFunction(containstable, freetexttable, table_name, left, right, left, language, right, third, third, semanticsimilaritytable, semantickeyphrasetable, semanticsimilaritydetailstable)

    def visitFreetext_predicate(self, ctx: tsql.Freetext_predicateContext):
        contains = self._(ctx.CONTAINS()) is not None
        left = self._(ctx.full_column_name(0))
        right = self._(ctx.full_column_name(1))
        property = self._(ctx.PROPERTY()) is not None
        third = self._(ctx.full_column_name(2))
        left = self._(ctx.expression(0))
        right = self._(ctx.expression(1))
        fourth = self.repeated(ctx, tsql.Full_column_nameContext)
        freetext = self._(ctx.FREETEXT()) is not None
        table_name = self._(ctx.table_name())
        language = self._(ctx.LANGUAGE()) is not None
        return FreetextPredicate(contains, left, right, property, third, left, right, fourth, freetext, table_name, language)

    def visitJson_key_value(self, ctx: tsql.Json_key_valueContext):
        json_key_name = self._(ctx.expression())
        return JsonKeyValue(json_key_name)

    def visitJson_null_clause(self, ctx: tsql.Json_null_clauseContext):
        absent = self._(ctx.ABSENT()) is not None
        left = self._(ctx.NULL_()) is not None
        return JsonNullClause(absent, left)

    def visitBuilt_in_functions(self, ctx: tsql.Built_in_functionsContext):
        app_name = self._(ctx.APP_NAME()) is not None
        applock_mode = self._(ctx.APPLOCK_MODE()) is not None
        database_principal = self._(ctx.expression(0))
        applock_test = self._(ctx.APPLOCK_TEST()) is not None
        assemblyproperty = self._(ctx.ASSEMBLYPROPERTY()) is not None
        col_length = self._(ctx.COL_LENGTH()) is not None
        col_name = self._(ctx.COL_NAME()) is not None
        columnproperty = self._(ctx.COLUMNPROPERTY()) is not None
        databasepropertyex = self._(ctx.DATABASEPROPERTYEX()) is not None
        db_id = self._(ctx.DB_ID()) is not None
        db_name = self._(ctx.DB_NAME()) is not None
        file_id = self._(ctx.FILE_ID()) is not None
        file_idex = self._(ctx.FILE_IDEX()) is not None
        file_name = self._(ctx.FILE_NAME()) is not None
        filegroup_id = self._(ctx.FILEGROUP_ID()) is not None
        filegroup_name = self._(ctx.FILEGROUP_NAME()) is not None
        filegroupproperty = self._(ctx.FILEGROUPPROPERTY()) is not None
        fileproperty = self._(ctx.FILEPROPERTY()) is not None
        filepropertyex = self._(ctx.FILEPROPERTYEX()) is not None
        fulltextcatalogproperty = self._(ctx.FULLTEXTCATALOGPROPERTY()) is not None
        fulltextserviceproperty = self._(ctx.FULLTEXTSERVICEPROPERTY()) is not None
        index_col = self._(ctx.INDEX_COL()) is not None
        indexkey_property = self._(ctx.INDEXKEY_PROPERTY()) is not None
        indexproperty = self._(ctx.INDEXPROPERTY()) is not None
        next = self._(ctx.NEXT()) is not None
        value = self._(ctx.VALUE()) is not None
        for_ = self._(ctx.FOR()) is not None
        sequence_name = self._(ctx.table_name())
        over = self._(ctx.OVER()) is not None
        order_by_clause = self._(ctx.order_by_clause())
        object_definition = self._(ctx.OBJECT_DEFINITION()) is not None
        object_id = self._(ctx.OBJECT_ID()) is not None
        object_name = self._(ctx.OBJECT_NAME()) is not None
        object_schema_name = self._(ctx.OBJECT_SCHEMA_NAME()) is not None
        objectproperty = self._(ctx.OBJECTPROPERTY()) is not None
        objectpropertyex = self._(ctx.OBJECTPROPERTYEX()) is not None
        original_db_name = self._(ctx.ORIGINAL_DB_NAME()) is not None
        parsename = self._(ctx.PARSENAME()) is not None
        schema_id = self._(ctx.SCHEMA_ID()) is not None
        schema_name = self._(ctx.SCHEMA_NAME()) is not None
        scope_identity = self._(ctx.SCOPE_IDENTITY()) is not None
        serverproperty = self._(ctx.SERVERPROPERTY()) is not None
        stats_date = self._(ctx.STATS_DATE()) is not None
        type_id = self._(ctx.TYPE_ID()) is not None
        type_name = self._(ctx.TYPE_NAME()) is not None
        typeproperty = self._(ctx.TYPEPROPERTY()) is not None
        ascii = self._(ctx.ASCII()) is not None
        char = self._(ctx.CHAR()) is not None
        charindex = self._(ctx.CHARINDEX()) is not None
        concat = self._(ctx.CONCAT()) is not None
        concat_ws = self._(ctx.CONCAT_WS()) is not None
        difference = self._(ctx.DIFFERENCE()) is not None
        format = self._(ctx.FORMAT()) is not None
        left = self._(ctx.LEFT()) is not None
        len_ = self._(ctx.LEN()) is not None
        lower = self._(ctx.LOWER()) is not None
        ltrim = self._(ctx.LTRIM()) is not None
        nchar = self._(ctx.NCHAR()) is not None
        patindex = self._(ctx.PATINDEX()) is not None
        quotename = self._(ctx.QUOTENAME()) is not None
        replace = self._(ctx.REPLACE()) is not None
        replicate = self._(ctx.REPLICATE()) is not None
        reverse = self._(ctx.REVERSE()) is not None
        right = self._(ctx.RIGHT()) is not None
        rtrim = self._(ctx.RTRIM()) is not None
        soundex = self._(ctx.SOUNDEX()) is not None
        space_keyword = self._(ctx.SPACE_KEYWORD()) is not None
        str = self._(ctx.STR()) is not None
        string_agg = self._(ctx.STRING_AGG()) is not None
        within = self._(ctx.WITHIN()) is not None
        group = self._(ctx.GROUP()) is not None
        string_escape = self._(ctx.STRING_ESCAPE()) is not None
        stuff = self._(ctx.STUFF()) is not None
        substring = self._(ctx.SUBSTRING()) is not None
        translate = self._(ctx.TRANSLATE()) is not None
        trim = self._(ctx.TRIM()) is not None
        from_ = self._(ctx.FROM()) is not None
        unicode = self._(ctx.UNICODE()) is not None
        upper = self._(ctx.UPPER()) is not None
        binary_checksum = self._(ctx.BINARY_CHECKSUM()) is not None
        right = self.repeated(ctx, tsql.ExpressionContext)
        checksum = self._(ctx.CHECKSUM()) is not None
        compress = self._(ctx.COMPRESS()) is not None
        connectionproperty = self._(ctx.CONNECTIONPROPERTY()) is not None
        property = self._(ctx.STRING())
        context_info = self._(ctx.CONTEXT_INFO()) is not None
        current_request_id = self._(ctx.CURRENT_REQUEST_ID()) is not None
        current_transaction_id = self._(ctx.CURRENT_TRANSACTION_ID()) is not None
        decompress = self._(ctx.DECOMPRESS()) is not None
        error_line = self._(ctx.ERROR_LINE()) is not None
        error_message = self._(ctx.ERROR_MESSAGE()) is not None
        error_number = self._(ctx.ERROR_NUMBER()) is not None
        error_procedure = self._(ctx.ERROR_PROCEDURE()) is not None
        error_severity = self._(ctx.ERROR_SEVERITY()) is not None
        error_state = self._(ctx.ERROR_STATE()) is not None
        formatmessage = self._(ctx.FORMATMESSAGE()) is not None
        msg_number = self._(ctx.DECIMAL()) is not None
        msg_variable = self._(ctx.LOCAL_ID())
        get_filestream_transaction_context = self._(ctx.GET_FILESTREAM_TRANSACTION_CONTEXT()) is not None
        getansinull = self._(ctx.GETANSINULL()) is not None
        host_id = self._(ctx.HOST_ID()) is not None
        host_name = self._(ctx.HOST_NAME()) is not None
        isnull = self._(ctx.ISNULL()) is not None
        isnumeric = self._(ctx.ISNUMERIC()) is not None
        min_active_rowversion = self._(ctx.MIN_ACTIVE_ROWVERSION()) is not None
        newid = self._(ctx.NEWID()) is not None
        newsequentialid = self._(ctx.NEWSEQUENTIALID()) is not None
        rowcount_big = self._(ctx.ROWCOUNT_BIG()) is not None
        session_context = self._(ctx.SESSION_CONTEXT()) is not None
        xact_state = self._(ctx.XACT_STATE()) is not None
        cast = self._(ctx.CAST()) is not None
        as_ = self._(ctx.AS()) is not None
        data_type = self._(ctx.data_type())
        try_cast = self._(ctx.TRY_CAST()) is not None
        convert = self._(ctx.CONVERT())
        coalesce = self._(ctx.COALESCE()) is not None
        expression_list = self._(ctx.expression_list_())
        cursor_rows = self._(ctx.CURSOR_ROWS()) is not None
        fetch_status = self._(ctx.FETCH_STATUS()) is not None
        cursor_status = self._(ctx.CURSOR_STATUS()) is not None
        cert_id = self._(ctx.CERT_ID()) is not None
        datalength = self._(ctx.DATALENGTH()) is not None
        ident_current = self._(ctx.IDENT_CURRENT()) is not None
        ident_incr = self._(ctx.IDENT_INCR()) is not None
        ident_seed = self._(ctx.IDENT_SEED()) is not None
        identity = self._(ctx.IDENTITY()) is not None
        sql_variant_property = self._(ctx.SQL_VARIANT_PROPERTY()) is not None
        current_date = self._(ctx.CURRENT_DATE()) is not None
        current_timestamp = self._(ctx.CURRENT_TIMESTAMP()) is not None
        current_timezone = self._(ctx.CURRENT_TIMEZONE()) is not None
        current_timezone_id = self._(ctx.CURRENT_TIMEZONE_ID()) is not None
        date_bucket = self._(ctx.DATE_BUCKET()) is not None
        datepart = self._(ctx.dateparts_9())
        dateadd = self._(ctx.DATEADD()) is not None
        datepart = self._(ctx.dateparts_12())
        datediff = self._(ctx.DATEDIFF()) is not None
        datediff_big = self._(ctx.DATEDIFF_BIG()) is not None
        datefromparts = self._(ctx.DATEFROMPARTS()) is not None
        datename = self._(ctx.DATENAME()) is not None
        datepart = self._(ctx.dateparts_15())
        datepart = self._(ctx.DATEPART()) is not None
        datetime2fromparts = self._(ctx.DATETIME2FROMPARTS()) is not None
        datetimefromparts = self._(ctx.DATETIMEFROMPARTS()) is not None
        datetimeoffsetfromparts = self._(ctx.DATETIMEOFFSETFROMPARTS()) is not None
        datetrunc = self._(ctx.DATETRUNC()) is not None
        datepart = self._(ctx.dateparts_datetrunc())
        day = self._(ctx.DAY()) is not None
        eomonth = self._(ctx.EOMONTH()) is not None
        getdate = self._(ctx.GETDATE()) is not None
        getutcdate = self._(ctx.GETUTCDATE()) is not None
        isdate = self._(ctx.ISDATE()) is not None
        month = self._(ctx.MONTH()) is not None
        smalldatetimefromparts = self._(ctx.SMALLDATETIMEFROMPARTS()) is not None
        switchoffset = self._(ctx.SWITCHOFFSET()) is not None
        sysdatetime = self._(ctx.SYSDATETIME()) is not None
        sysdatetimeoffset = self._(ctx.SYSDATETIMEOFFSET()) is not None
        sysutcdatetime = self._(ctx.SYSUTCDATETIME()) is not None
        timefromparts = self._(ctx.TIMEFROMPARTS()) is not None
        todatetimeoffset = self._(ctx.TODATETIMEOFFSET()) is not None
        year = self._(ctx.YEAR()) is not None
        nullif = self._(ctx.NULLIF()) is not None
        parse = self._(ctx.PARSE())
        using = self._(ctx.USING()) is not None
        xml_data_type_methods = self._(ctx.xml_data_type_methods())
        iif = self._(ctx.IIF()) is not None
        cond = self._(ctx.search_condition())
        isjson = self._(ctx.ISJSON()) is not None
        json_object = self._(ctx.JSON_OBJECT()) is not None
        key_value = self._(ctx.json_key_value())
        json_null_clause = self.repeated(ctx, tsql.Json_null_clauseContext)
        json_array = self._(ctx.JSON_ARRAY()) is not None
        json_value = self._(ctx.JSON_VALUE()) is not None
        json_query = self._(ctx.JSON_QUERY()) is not None
        json_modify = self._(ctx.JSON_MODIFY()) is not None
        json_path_exists = self._(ctx.JSON_PATH_EXISTS()) is not None
        abs = self._(ctx.ABS()) is not None
        acos = self._(ctx.ACOS()) is not None
        asin = self._(ctx.ASIN()) is not None
        atan = self._(ctx.ATAN()) is not None
        atn2 = self._(ctx.ATN2()) is not None
        ceiling = self._(ctx.CEILING()) is not None
        cos = self._(ctx.COS()) is not None
        cot = self._(ctx.COT()) is not None
        degrees = self._(ctx.DEGREES()) is not None
        exp = self._(ctx.EXP()) is not None
        floor = self._(ctx.FLOOR()) is not None
        log = self._(ctx.LOG()) is not None
        log10 = self._(ctx.LOG10()) is not None
        pi = self._(ctx.PI()) is not None
        power = self._(ctx.POWER()) is not None
        radians = self._(ctx.RADIANS()) is not None
        rand = self._(ctx.RAND()) is not None
        round = self._(ctx.ROUND()) is not None
        sign = self._(ctx.SIGN()) is not None
        sin = self._(ctx.SIN()) is not None
        sqrt = self._(ctx.SQRT()) is not None
        square = self._(ctx.SQUARE()) is not None
        tan = self._(ctx.TAN()) is not None
        greatest = self._(ctx.GREATEST()) is not None
        least = self._(ctx.LEAST()) is not None
        certencoded = self._(ctx.CERTENCODED()) is not None
        certprivatekey = self._(ctx.CERTPRIVATEKEY()) is not None
        current_user = self._(ctx.CURRENT_USER()) is not None
        database_principal_id = self._(ctx.DATABASE_PRINCIPAL_ID()) is not None
        has_dbaccess = self._(ctx.HAS_DBACCESS()) is not None
        has_perms_by_name = self._(ctx.HAS_PERMS_BY_NAME()) is not None
        is_member = self._(ctx.IS_MEMBER()) is not None
        is_rolemember = self._(ctx.IS_ROLEMEMBER()) is not None
        is_srvrolemember = self._(ctx.IS_SRVROLEMEMBER()) is not None
        loginproperty = self._(ctx.LOGINPROPERTY()) is not None
        original_login = self._(ctx.ORIGINAL_LOGIN()) is not None
        permissions = self._(ctx.PERMISSIONS()) is not None
        pwdencrypt = self._(ctx.PWDENCRYPT()) is not None
        pwdcompare = self._(ctx.PWDCOMPARE()) is not None
        session_user = self._(ctx.SESSION_USER()) is not None
        sessionproperty = self._(ctx.SESSIONPROPERTY()) is not None
        suser_id = self._(ctx.SUSER_ID()) is not None
        suser_name = self._(ctx.SUSER_NAME()) is not None
        suser_sid = self._(ctx.SUSER_SID()) is not None
        suser_sname = self._(ctx.SUSER_SNAME()) is not None
        system_user = self._(ctx.SYSTEM_USER()) is not None
        user = self._(ctx.USER()) is not None
        user_id = self._(ctx.USER_ID()) is not None
        user_name = self._(ctx.USER_NAME()) is not None
        return BuiltInFunctions(app_name, applock_mode, database_principal, applock_test, assemblyproperty, col_length, col_name, columnproperty, databasepropertyex, db_id, db_name, file_id, file_idex, file_name, filegroup_id, filegroup_name, filegroupproperty, fileproperty, filepropertyex, fulltextcatalogproperty, fulltextserviceproperty, index_col, indexkey_property, indexproperty, next, value, for_, sequence_name, over, order_by_clause, object_definition, object_id, object_name, object_schema_name, objectproperty, objectpropertyex, original_db_name, parsename, schema_id, schema_name, scope_identity, serverproperty, stats_date, type_id, type_name, typeproperty, ascii, char, charindex, concat, concat_ws, difference, format, left, len_, lower, ltrim, nchar, patindex, quotename, replace, replicate, reverse, right, rtrim, soundex, space_keyword, str, string_agg, within, group, string_escape, stuff, substring, translate, trim, from_, unicode, upper, binary_checksum, right, checksum, compress, connectionproperty, property, context_info, current_request_id, current_transaction_id, decompress, error_line, error_message, error_number, error_procedure, error_severity, error_state, formatmessage, msg_number, msg_variable, get_filestream_transaction_context, getansinull, host_id, host_name, isnull, isnumeric, min_active_rowversion, newid, newsequentialid, rowcount_big, session_context, xact_state, cast, as_, data_type, try_cast, convert, coalesce, expression_list, cursor_rows, fetch_status, cursor_status, cert_id, datalength, ident_current, ident_incr, ident_seed, identity, sql_variant_property, current_date, current_timestamp, current_timezone, current_timezone_id, date_bucket, datepart, dateadd, datepart, datediff, datediff_big, datefromparts, datename, datepart, datepart, datetime2fromparts, datetimefromparts, datetimeoffsetfromparts, datetrunc, datepart, day, eomonth, getdate, getutcdate, isdate, month, smalldatetimefromparts, switchoffset, sysdatetime, sysdatetimeoffset, sysutcdatetime, timefromparts, todatetimeoffset, year, nullif, parse, using, xml_data_type_methods, iif, cond, isjson, json_object, key_value, json_null_clause, json_array, json_value, json_query, json_modify, json_path_exists, abs, acos, asin, atan, atn2, ceiling, cos, cot, degrees, exp, floor, log, log10, pi, power, radians, rand, round, sign, sin, sqrt, square, tan, greatest, least, certencoded, certprivatekey, current_user, database_principal_id, has_dbaccess, has_perms_by_name, is_member, is_rolemember, is_srvrolemember, loginproperty, original_login, permissions, pwdencrypt, pwdcompare, session_user, sessionproperty, suser_id, suser_name, suser_sid, suser_sname, system_user, user, user_id, user_name)

    def visitXml_data_type_methods(self, ctx: tsql.Xml_data_type_methodsContext):
        value_method = self._(ctx.value_method())
        query_method = self._(ctx.query_method())
        exist_method = self._(ctx.exist_method())
        modify_method = self._(ctx.modify_method())
        return XmlDataTypeMethods(value_method, query_method, exist_method, modify_method)

    def visitDateparts_9(self, ctx: tsql.Dateparts_9Context):
        year = self._(ctx.YEAR()) is not None
        year_abbr = self._(ctx.YEAR_ABBR())
        quarter = self._(ctx.QUARTER()) is not None
        quarter_abbr = self._(ctx.QUARTER_ABBR())
        month = self._(ctx.MONTH()) is not None
        month_abbr = self._(ctx.MONTH_ABBR())
        day = self._(ctx.DAY()) is not None
        day_abbr = self._(ctx.DAY_ABBR())
        week = self._(ctx.WEEK()) is not None
        week_abbr = self._(ctx.WEEK_ABBR())
        hour = self._(ctx.HOUR()) is not None
        hour_abbr = self._(ctx.HOUR_ABBR()) is not None
        minute = self._(ctx.MINUTE()) is not None
        minute_abbr = self._(ctx.MINUTE_ABBR())
        second = self._(ctx.SECOND()) is not None
        second_abbr = self._(ctx.SECOND_ABBR())
        millisecond = self._(ctx.MILLISECOND()) is not None
        millisecond_abbr = self._(ctx.MILLISECOND_ABBR()) is not None
        return Dateparts9(year, year_abbr, quarter, quarter_abbr, month, month_abbr, day, day_abbr, week, week_abbr, hour, hour_abbr, minute, minute_abbr, second, second_abbr, millisecond, millisecond_abbr)

    def visitDateparts_12(self, ctx: tsql.Dateparts_12Context):
        dateparts_9 = self._(ctx.dateparts_9())
        dayofyear = self._(ctx.DAYOFYEAR()) is not None
        dayofyear_abbr = self._(ctx.DAYOFYEAR_ABBR())
        microsecond = self._(ctx.MICROSECOND()) is not None
        microsecond_abbr = self._(ctx.MICROSECOND_ABBR()) is not None
        nanosecond = self._(ctx.NANOSECOND()) is not None
        nanosecond_abbr = self._(ctx.NANOSECOND_ABBR()) is not None
        return Dateparts12(dateparts_9, dayofyear, dayofyear_abbr, microsecond, microsecond_abbr, nanosecond, nanosecond_abbr)

    def visitDateparts_15(self, ctx: tsql.Dateparts_15Context):
        dateparts_12 = self._(ctx.dateparts_12())
        weekday = self._(ctx.WEEKDAY()) is not None
        weekday_abbr = self._(ctx.WEEKDAY_ABBR()) is not None
        tzoffset = self._(ctx.TZOFFSET()) is not None
        tzoffset_abbr = self._(ctx.TZOFFSET_ABBR()) is not None
        iso_week = self._(ctx.ISO_WEEK()) is not None
        iso_week_abbr = self._(ctx.ISO_WEEK_ABBR())
        return Dateparts15(dateparts_12, weekday, weekday_abbr, tzoffset, tzoffset_abbr, iso_week, iso_week_abbr)

    def visitDateparts_datetrunc(self, ctx: tsql.Dateparts_datetruncContext):
        dateparts_9 = self._(ctx.dateparts_9())
        dayofyear = self._(ctx.DAYOFYEAR()) is not None
        dayofyear_abbr = self._(ctx.DAYOFYEAR_ABBR())
        microsecond = self._(ctx.MICROSECOND()) is not None
        microsecond_abbr = self._(ctx.MICROSECOND_ABBR()) is not None
        iso_week = self._(ctx.ISO_WEEK()) is not None
        iso_week_abbr = self._(ctx.ISO_WEEK_ABBR())
        return DatepartsDatetrunc(dateparts_9, dayofyear, dayofyear_abbr, microsecond, microsecond_abbr, iso_week, iso_week_abbr)

    def visitValue_method(self, ctx: tsql.Value_methodContext):
        loc_id = self._(ctx.LOCAL_ID())
        value_id = self._(ctx.full_column_name())
        eventdata = self._(ctx.EVENTDATA()) is not None
        query = self._(ctx.query_method())
        subquery = self._(ctx.subquery())
        call = self._(ctx.value_call())
        return ValueMethod(loc_id, value_id, eventdata, query, subquery, call)

    def visitValue_call(self, ctx: tsql.Value_callContext):
        value = self._(ctx.VALUE()) is not None
        value_square_bracket = self._(ctx.VALUE_SQUARE_BRACKET()) is not None
        xquery = self._(ctx.STRING())
        return ValueCall(value, value_square_bracket, xquery)

    def visitQuery_method(self, ctx: tsql.Query_methodContext):
        loc_id = self._(ctx.LOCAL_ID())
        value_id = self._(ctx.full_column_name())
        subquery = self._(ctx.subquery())
        call = self._(ctx.query_call())
        return QueryMethod(loc_id, value_id, subquery, call)

    def visitQuery_call(self, ctx: tsql.Query_callContext):
        query = self._(ctx.QUERY()) is not None
        query_square_bracket = self._(ctx.QUERY_SQUARE_BRACKET()) is not None
        xquery = self._(ctx.STRING())
        return QueryCall(query, query_square_bracket, xquery)

    def visitExist_method(self, ctx: tsql.Exist_methodContext):
        loc_id = self._(ctx.LOCAL_ID())
        value_id = self._(ctx.full_column_name())
        subquery = self._(ctx.subquery())
        call = self._(ctx.exist_call())
        return ExistMethod(loc_id, value_id, subquery, call)

    def visitExist_call(self, ctx: tsql.Exist_callContext):
        exist = self._(ctx.EXIST()) is not None
        exist_square_bracket = self._(ctx.EXIST_SQUARE_BRACKET()) is not None
        xquery = self._(ctx.STRING())
        return ExistCall(exist, exist_square_bracket, xquery)

    def visitModify_method(self, ctx: tsql.Modify_methodContext):
        loc_id = self._(ctx.LOCAL_ID())
        value_id = self._(ctx.full_column_name())
        subquery = self._(ctx.subquery())
        call = self._(ctx.modify_call())
        return ModifyMethod(loc_id, value_id, subquery, call)

    def visitModify_call(self, ctx: tsql.Modify_callContext):
        modify = self._(ctx.MODIFY()) is not None
        modify_square_bracket = self._(ctx.MODIFY_SQUARE_BRACKET()) is not None
        xml_dml = self._(ctx.STRING())
        return ModifyCall(modify, modify_square_bracket, xml_dml)

    def visitHierarchyid_call(self, ctx: tsql.Hierarchyid_callContext):
        getancestor = self._(ctx.GETANCESTOR()) is not None
        n = self._(ctx.expression())
        getdescendant = self._(ctx.GETDESCENDANT()) is not None
        getlevel = self._(ctx.GETLEVEL()) is not None
        isdescendantof = self._(ctx.ISDESCENDANTOF()) is not None
        getreparentedvalue = self._(ctx.GETREPARENTEDVALUE()) is not None
        tostring = self._(ctx.TOSTRING()) is not None
        return HierarchyidCall(getancestor, n, getdescendant, getlevel, isdescendantof, getreparentedvalue, tostring)

    def visitHierarchyid_static_method(self, ctx: tsql.Hierarchyid_static_methodContext):
        getroot = self._(ctx.GETROOT()) is not None
        parse = self._(ctx.PARSE())
        input = self._(ctx.expression())
        return HierarchyidStaticMethod(getroot, parse, input)

    def visitNodes_method(self, ctx: tsql.Nodes_methodContext):
        loc_id = self._(ctx.LOCAL_ID())
        value_id = self._(ctx.full_column_name())
        subquery = self._(ctx.subquery())
        xquery = self._(ctx.STRING())
        return NodesMethod(loc_id, value_id, subquery, xquery)

    def visitSwitch_section(self, ctx: tsql.Switch_sectionContext):
        left = self._(ctx.expression(0))
        right = self._(ctx.expression(1))
        return SwitchSection(left, right)

    def visitSwitch_search_condition_section(self, ctx: tsql.Switch_search_condition_sectionContext):
        search_condition = self._(ctx.search_condition())
        expression = self._(ctx.expression())
        return SwitchSearchConditionSection(search_condition, expression)

    def visitAs_column_alias(self, ctx: tsql.As_column_aliasContext):
        column_alias = self._(ctx.column_alias())
        return AsColumnAlias(column_alias)

    def visitAs_table_alias(self, ctx: tsql.As_table_aliasContext):
        table_alias = self._(ctx.table_alias())
        return AsTableAlias(table_alias)

    def visitWith_table_hints(self, ctx: tsql.With_table_hintsContext):
        hint = self._(ctx.table_hint())
        return WithTableHints(hint)

    def visitDeprecated_table_hint(self, ctx: tsql.Deprecated_table_hintContext):
        table_hint = self._(ctx.table_hint())
        return DeprecatedTableHint(table_hint)

    def visitSybase_legacy_hint(self, ctx: tsql.Sybase_legacy_hintContext):
        holdlock = self._(ctx.HOLDLOCK()) is not None
        noholdlock = self._(ctx.NOHOLDLOCK()) is not None
        readpast = self._(ctx.READPAST()) is not None
        shared = self._(ctx.SHARED()) is not None
        return SybaseLegacyHint(holdlock, noholdlock, readpast, shared)

    def visitTable_hint(self, ctx: tsql.Table_hintContext):
        noexpand = self._(ctx.NOEXPAND()) is not None
        index = self._(ctx.INDEX()) is not None
        left = self._(ctx.index_value(0))
        right = self._(ctx.index_value(1))
        third = self._(ctx.index_value(2))
        fourth = self.repeated(ctx, tsql.Index_valueContext)
        forceseek = self._(ctx.FORCESEEK()) is not None
        column_name_list = self._(ctx.column_name_list())
        forcescan = self._(ctx.FORCESCAN()) is not None
        holdlock = self._(ctx.HOLDLOCK()) is not None
        nolock = self._(ctx.NOLOCK()) is not None
        nowait = self._(ctx.NOWAIT()) is not None
        paglock = self._(ctx.PAGLOCK()) is not None
        readcommitted = self._(ctx.READCOMMITTED()) is not None
        readcommittedlock = self._(ctx.READCOMMITTEDLOCK()) is not None
        readpast = self._(ctx.READPAST()) is not None
        readuncommitted = self._(ctx.READUNCOMMITTED()) is not None
        repeatableread = self._(ctx.REPEATABLEREAD()) is not None
        rowlock = self._(ctx.ROWLOCK()) is not None
        serializable = self._(ctx.SERIALIZABLE()) is not None
        snapshot = self._(ctx.SNAPSHOT()) is not None
        spatial_window_max_cells = self._(ctx.SPATIAL_WINDOW_MAX_CELLS()) is not None
        decimal = self._(ctx.DECIMAL()) is not None
        tablock = self._(ctx.TABLOCK()) is not None
        tablockx = self._(ctx.TABLOCKX()) is not None
        updlock = self._(ctx.UPDLOCK()) is not None
        xlock = self._(ctx.XLOCK()) is not None
        keepidentity = self._(ctx.KEEPIDENTITY()) is not None
        keepdefaults = self._(ctx.KEEPDEFAULTS()) is not None
        ignore_constraints = self._(ctx.IGNORE_CONSTRAINTS()) is not None
        ignore_triggers = self._(ctx.IGNORE_TRIGGERS()) is not None
        return TableHint(noexpand, index, left, right, third, fourth, forceseek, column_name_list, forcescan, holdlock, nolock, nowait, paglock, readcommitted, readcommittedlock, readpast, readuncommitted, repeatableread, rowlock, serializable, snapshot, spatial_window_max_cells, decimal, tablock, tablockx, updlock, xlock, keepidentity, keepdefaults, ignore_constraints, ignore_triggers)

    def visitIndex_value(self, ctx: tsql.Index_valueContext):
        id = self._(ctx.id_())
        decimal = self._(ctx.DECIMAL()) is not None
        return IndexValue(id, decimal)

    def visitColumn_alias_list(self, ctx: tsql.Column_alias_listContext):
        alias = self._(ctx.column_alias())
        return ColumnAliasList(alias)

    def visitColumn_alias(self, ctx: tsql.Column_aliasContext):
        id = self._(ctx.id_())
        string = self._(ctx.STRING())
        return ColumnAlias(id, string)

    def visitTable_value_constructor(self, ctx: tsql.Table_value_constructorContext):
        exps = self._(ctx.expression_list_())
        return TableValueConstructor(exps)

    def visitExpression_list_(self, ctx: tsql.Expression_list_Context):
        exp = self._(ctx.expression())
        return ExpressionList(exp)

    def visitRanking_windowed_function(self, ctx: tsql.Ranking_windowed_functionContext):
        rank = self._(ctx.RANK()) is not None
        dense_rank = self._(ctx.DENSE_RANK()) is not None
        row_number = self._(ctx.ROW_NUMBER()) is not None
        over_clause = self._(ctx.over_clause())
        ntile = self._(ctx.NTILE()) is not None
        expression = self._(ctx.expression())
        return RankingWindowedFunction(rank, dense_rank, row_number, over_clause, ntile, expression)

    def visitAggregate_windowed_function(self, ctx: tsql.Aggregate_windowed_functionContext):
        aggregate_windowed_function_agg_func = self._(ctx.aggregate_windowed_function_agg_func())
        all_distinct_expression = self._(ctx.all_distinct_expression())
        over_clause = self.repeated(ctx, tsql.Over_clauseContext)
        aggregate_windowed_function_cnt = self._(ctx.aggregate_windowed_function_cnt())
        checksum_agg = self._(ctx.CHECKSUM_AGG()) is not None
        grouping = self._(ctx.GROUPING()) is not None
        expression = self._(ctx.expression())
        grouping_id = self._(ctx.GROUPING_ID()) is not None
        expression_list = self._(ctx.expression_list_())
        return AggregateWindowedFunction(aggregate_windowed_function_agg_func, all_distinct_expression, over_clause, aggregate_windowed_function_cnt, checksum_agg, grouping, expression, grouping_id, expression_list)

    def visitAnalytic_windowed_function(self, ctx: tsql.Analytic_windowed_functionContext):
        first_value = self._(ctx.FIRST_VALUE()) is not None
        last_value = self._(ctx.LAST_VALUE()) is not None
        expression = self._(ctx.expression(0))
        over_clause = self._(ctx.over_clause())
        lag = self._(ctx.LAG()) is not None
        lead = self._(ctx.LEAD()) is not None
        right = self._(ctx.expression(1))
        third = self._(ctx.expression(2))
        cume_dist = self._(ctx.CUME_DIST()) is not None
        percent_rank = self._(ctx.PERCENT_RANK()) is not None
        over = self._(ctx.OVER()) is not None
        partition = self._(ctx.PARTITION()) is not None
        by = self._(ctx.BY()) is not None
        expression_list = self._(ctx.expression_list_())
        order_by_clause = self._(ctx.order_by_clause())
        percentile_cont = self._(ctx.PERCENTILE_CONT()) is not None
        percentile_disc = self._(ctx.PERCENTILE_DISC()) is not None
        within = self._(ctx.WITHIN()) is not None
        group = self._(ctx.GROUP()) is not None
        return AnalyticWindowedFunction(first_value, last_value, expression, over_clause, lag, lead, right, third, cume_dist, percent_rank, over, partition, by, expression_list, order_by_clause, percentile_cont, percentile_disc, within, group)

    def visitAll_distinct_expression(self, ctx: tsql.All_distinct_expressionContext):
        all = self._(ctx.ALL()) is not None
        distinct = self._(ctx.DISTINCT()) is not None
        expression = self._(ctx.expression())
        return AllDistinctExpression(all, distinct, expression)

    def visitOver_clause(self, ctx: tsql.Over_clauseContext):
        partition = self._(ctx.PARTITION()) is not None
        by = self._(ctx.BY()) is not None
        expression_list = self._(ctx.expression_list_())
        order_by_clause = self.repeated(ctx, tsql.Order_by_clauseContext)
        row_or_range_clause = self.repeated(ctx, tsql.Row_or_range_clauseContext)
        return OverClause(partition, by, expression_list, order_by_clause, row_or_range_clause)

    def visitRow_or_range_clause(self, ctx: tsql.Row_or_range_clauseContext):
        rows = self._(ctx.ROWS()) is not None
        range_ = self._(ctx.RANGE()) is not None
        window_frame_extent = self._(ctx.window_frame_extent())
        return RowOrRangeClause(rows, range_, window_frame_extent)

    def visitWindow_frame_extent(self, ctx: tsql.Window_frame_extentContext):
        window_frame_preceding = self._(ctx.window_frame_preceding())
        between = self._(ctx.BETWEEN()) is not None
        left = self._(ctx.window_frame_bound(0))
        and_ = self._(ctx.AND()) is not None
        right = self._(ctx.window_frame_bound(1))
        return WindowFrameExtent(window_frame_preceding, between, left, and_, right)

    def visitWindow_frame_bound(self, ctx: tsql.Window_frame_boundContext):
        window_frame_preceding = self._(ctx.window_frame_preceding())
        window_frame_following = self._(ctx.window_frame_following())
        return WindowFrameBound(window_frame_preceding, window_frame_following)

    def visitWindow_frame_preceding(self, ctx: tsql.Window_frame_precedingContext):
        unbounded = self._(ctx.UNBOUNDED()) is not None
        preceding = self._(ctx.PRECEDING()) is not None
        decimal = self._(ctx.DECIMAL()) is not None
        current = self._(ctx.CURRENT()) is not None
        row = self._(ctx.ROW()) is not None
        return WindowFramePreceding(unbounded, preceding, decimal, current, row)

    def visitWindow_frame_following(self, ctx: tsql.Window_frame_followingContext):
        unbounded = self._(ctx.UNBOUNDED()) is not None
        following = self._(ctx.FOLLOWING()) is not None
        decimal = self._(ctx.DECIMAL()) is not None
        return WindowFrameFollowing(unbounded, following, decimal)

    def visitCreate_database_option(self, ctx: tsql.Create_database_optionContext):
        filestream = self._(ctx.FILESTREAM()) is not None
        left = self._(ctx.database_filestream_option(0))
        right = self.repeated(ctx, tsql.Database_filestream_optionContext)
        default_language = self._(ctx.DEFAULT_LANGUAGE()) is not None
        equal = self._(ctx.EQUAL()) is not None
        id = self._(ctx.id_())
        string = self._(ctx.STRING())
        default_fulltext_language = self._(ctx.DEFAULT_FULLTEXT_LANGUAGE()) is not None
        nested_triggers = self._(ctx.NESTED_TRIGGERS()) is not None
        off = self._(ctx.OFF()) is not None
        on = self._(ctx.ON()) is not None
        transform_noise_words = self._(ctx.TRANSFORM_NOISE_WORDS()) is not None
        two_digit_year_cutoff = self._(ctx.TWO_DIGIT_YEAR_CUTOFF()) is not None
        decimal = self._(ctx.DECIMAL()) is not None
        db_chaining = self._(ctx.DB_CHAINING()) is not None
        trustworthy = self._(ctx.TRUSTWORTHY()) is not None
        return CreateDatabaseOption(filestream, left, right, default_language, equal, id, string, default_fulltext_language, nested_triggers, off, on, transform_noise_words, two_digit_year_cutoff, decimal, db_chaining, trustworthy)

    def visitDatabase_filestream_option(self, ctx: tsql.Database_filestream_optionContext):
        non_transacted_access = self._(ctx.NON_TRANSACTED_ACCESS()) is not None
        left = self._(ctx.EQUAL()) is not None
        directory_name = self._(ctx.DIRECTORY_NAME()) is not None
        right = self._(ctx.EQUAL()) is not None
        string = self._(ctx.STRING())
        off = self._(ctx.OFF()) is not None
        read_only = self._(ctx.READ_ONLY()) is not None
        full = self._(ctx.FULL()) is not None
        return DatabaseFilestreamOption(non_transacted_access, left, directory_name, right, string, off, read_only, full)

    def visitDatabase_file_spec(self, ctx: tsql.Database_file_specContext):
        file_group = self._(ctx.file_group())
        file_spec = self._(ctx.file_spec())
        return DatabaseFileSpec(file_group, file_spec)

    def visitFile_group(self, ctx: tsql.File_groupContext):
        id = self._(ctx.id_())
        left = self._(ctx.CONTAINS()) is not None
        filestream = self._(ctx.FILESTREAM()) is not None
        default_ = self._(ctx.DEFAULT()) is not None
        right = self._(ctx.CONTAINS()) is not None
        memory_optimized_data = self._(ctx.MEMORY_OPTIMIZED_DATA()) is not None
        left = self._(ctx.file_spec(0))
        right = self.repeated(ctx, tsql.File_specContext)
        return FileGroup(id, left, filestream, default_, right, memory_optimized_data, left, right)

    def visitFile_spec(self, ctx: tsql.File_specContext):
        id = self._(ctx.id_())
        string = self._(ctx.STRING())
        size = self._(ctx.SIZE()) is not None
        left = self._(ctx.EQUAL()) is not None
        left = self._(ctx.file_size(0))
        maxsize = self._(ctx.MAXSIZE()) is not None
        right = self._(ctx.EQUAL()) is not None
        filegrowth = self._(ctx.FILEGROWTH()) is not None
        third = self._(ctx.EQUAL()) is not None
        right = self._(ctx.file_size(1))
        third = self._(ctx.file_size(2))
        unlimited = self._(ctx.UNLIMITED()) is not None
        return FileSpec(id, string, size, left, left, maxsize, right, filegrowth, third, right, third, unlimited)

    def visitEntity_name(self, ctx: tsql.Entity_nameContext):
        server = self._(ctx.id_())
        return EntityName(server)

    def visitEntity_name_for_azure_dw(self, ctx: tsql.Entity_name_for_azure_dwContext):
        schema = self._(ctx.id_())
        return EntityNameForAzureDw(schema)

    def visitEntity_name_for_parallel_dw(self, ctx: tsql.Entity_name_for_parallel_dwContext):
        schema_database = self._(ctx.id_())
        return EntityNameForParallelDw(schema_database)

    def visitFull_table_name(self, ctx: tsql.Full_table_nameContext):
        linked_server = self._(ctx.id_())
        return FullTableName(linked_server)

    def visitTable_name(self, ctx: tsql.Table_nameContext):
        database = self._(ctx.id_())
        blocking_hierarchy = self._(ctx.BLOCKING_HIERARCHY()) is not None
        return TableName(database, blocking_hierarchy)

    def visitSimple_name(self, ctx: tsql.Simple_nameContext):
        schema = self._(ctx.id_())
        return SimpleName(schema)

    def visitFunc_proc_name_schema(self, ctx: tsql.Func_proc_name_schemaContext):
        procedure = self._(ctx.id_())
        return FuncProcNameSchema(procedure)

    def visitFunc_proc_name_database_schema(self, ctx: tsql.Func_proc_name_database_schemaContext):
        database = self.repeated(ctx, tsql.Id_Context)
        func_proc_name_schema = self._(ctx.func_proc_name_schema())
        return FuncProcNameDatabaseSchema(database, func_proc_name_schema)

    def visitFunc_proc_name_server_database_schema(self, ctx: tsql.Func_proc_name_server_database_schemaContext):
        server = self.repeated(ctx, tsql.Id_Context)
        func_proc_name_database_schema = self._(ctx.func_proc_name_database_schema())
        return FuncProcNameServerDatabaseSchema(server, func_proc_name_database_schema)

    def visitDdl_object(self, ctx: tsql.Ddl_objectContext):
        full_table_name = self._(ctx.full_table_name())
        local_id = self._(ctx.LOCAL_ID())
        return DdlObject(full_table_name, local_id)

    def visitFull_column_name(self, ctx: tsql.Full_column_nameContext):
        column_name = self._(ctx.id_())
        deleted = self._(ctx.DELETED()) is not None
        inserted = self._(ctx.INSERTED()) is not None
        full_table_name = self._(ctx.full_table_name())
        identity = self._(ctx.IDENTITY()) is not None
        rowguid = self._(ctx.ROWGUID()) is not None
        return FullColumnName(column_name, deleted, inserted, full_table_name, identity, rowguid)

    def visitColumn_name_list_with_order(self, ctx: tsql.Column_name_list_with_orderContext):
        left = self._(ctx.id_(0))
        left = self._(ctx.ASC()) is not None
        left = self._(ctx.DESC()) is not None
        right = self.repeated(ctx, tsql.Id_Context)
        right = self._(ctx.ASC()) is not None
        right = self._(ctx.DESC()) is not None
        return ColumnNameListWithOrder(left, left, left, right, right, right)

    def visitInsert_column_name_list(self, ctx: tsql.Insert_column_name_listContext):
        col = self._(ctx.insert_column_id())
        return InsertColumnNameList(col)

    def visitInsert_column_id(self, ctx: tsql.Insert_column_idContext):
        ignore = self.repeated(ctx, tsql.Id_Context)
        return InsertColumnId(ignore)

    def visitColumn_name_list(self, ctx: tsql.Column_name_listContext):
        col = self._(ctx.id_())
        return ColumnNameList(col)

    def visitCursor_name(self, ctx: tsql.Cursor_nameContext):
        id = self._(ctx.id_())
        local_id = self._(ctx.LOCAL_ID())
        return CursorName(id, local_id)

    def visitOn_off(self, ctx: tsql.On_offContext):
        on = self._(ctx.ON()) is not None
        off = self._(ctx.OFF()) is not None
        return OnOff(on, off)

    def visitClustered(self, ctx: tsql.ClusteredContext):
        clustered = self._(ctx.CLUSTERED()) is not None
        nonclustered = self._(ctx.NONCLUSTERED()) is not None
        return Clustered(clustered, nonclustered)

    def visitScalar_function_name(self, ctx: tsql.Scalar_function_nameContext):
        func_proc_name_server_database_schema = self._(ctx.func_proc_name_server_database_schema())
        right = self._(ctx.RIGHT()) is not None
        left = self._(ctx.LEFT()) is not None
        binary_checksum = self._(ctx.BINARY_CHECKSUM()) is not None
        checksum = self._(ctx.CHECKSUM()) is not None
        return ScalarFunctionName(func_proc_name_server_database_schema, right, left, binary_checksum, checksum)

    def visitBegin_conversation_timer(self, ctx: tsql.Begin_conversation_timerContext):
        local_id = self._(ctx.LOCAL_ID())
        time = self._(ctx.time())
        return BeginConversationTimer(local_id, time)

    def visitBegin_conversation_dialog(self, ctx: tsql.Begin_conversation_dialogContext):
        conversation = self._(ctx.CONVERSATION()) is not None
        dialog_handle = self._(ctx.LOCAL_ID(0))
        initiator_service_name = self._(ctx.service_name())
        service_broker_guid = self._(ctx.STRING())
        contract_name = self._(ctx.contract_name())
        with_ = self._(ctx.WITH()) is not None
        right = self._(ctx.LOCAL_ID(1))
        lifetime = self._(ctx.LIFETIME()) is not None
        encryption = self._(ctx.ENCRYPTION()) is not None
        on_off = self._(ctx.on_off())
        related_conversation = self._(ctx.RELATED_CONVERSATION()) is not None
        related_conversation_group = self._(ctx.RELATED_CONVERSATION_GROUP()) is not None
        decimal = self._(ctx.DECIMAL()) is not None
        third = self._(ctx.LOCAL_ID(2))
        return BeginConversationDialog(conversation, dialog_handle, initiator_service_name, service_broker_guid, contract_name, with_, right, lifetime, encryption, on_off, related_conversation, related_conversation_group, decimal, third)

    def visitContract_name(self, ctx: tsql.Contract_nameContext):
        id = self._(ctx.id_())
        expression = self._(ctx.expression())
        return ContractName(id, expression)

    def visitService_name(self, ctx: tsql.Service_nameContext):
        id = self._(ctx.id_())
        expression = self._(ctx.expression())
        return ServiceName(id, expression)

    def visitEnd_conversation(self, ctx: tsql.End_conversationContext):
        conversation_handle = self._(ctx.LOCAL_ID())
        with_ = self._(ctx.WITH()) is not None
        cleanup = self._(ctx.CLEANUP()) is not None
        error = self._(ctx.ERROR()) is not None
        end_conversation_faliure_code = self._(ctx.end_conversation_faliure_code())
        description = self._(ctx.DESCRIPTION()) is not None
        end_conversation_failure_text = self._(ctx.end_conversation_failure_text())
        return EndConversation(conversation_handle, with_, cleanup, error, end_conversation_faliure_code, description, end_conversation_failure_text)

    def visitWaitfor_conversation(self, ctx: tsql.Waitfor_conversationContext):
        get_conversation = self._(ctx.get_conversation())
        timeout = self._(ctx.TIMEOUT()) is not None
        timeout = self._(ctx.time())
        return WaitforConversation(get_conversation, timeout, timeout)

    def visitGet_conversation(self, ctx: tsql.Get_conversationContext):
        get_conversation_conversation_group_id = self._(ctx.get_conversation_conversation_group_id())
        queue = self._(ctx.queue_id())
        return GetConversation(get_conversation_conversation_group_id, queue)

    def visitQueue_id(self, ctx: tsql.Queue_idContext):
        database_name = self._(ctx.id_())
        return QueueId(database_name)

    def visitSend_conversation(self, ctx: tsql.Send_conversationContext):
        send_conversation_conversation_handle = self._(ctx.send_conversation_conversation_handle())
        message_type_name = self._(ctx.expression())
        send_conversation_message_body_expression = self._(ctx.send_conversation_message_body_expression())
        return SendConversation(send_conversation_conversation_handle, message_type_name, send_conversation_message_body_expression)

    def visitData_type(self, ctx: tsql.Data_typeContext):
        data_type_scaled = self._(ctx.data_type_scaled())
        max = self._(ctx.MAX()) is not None
        ext_type = self._(ctx.id_())
        scale = self._(ctx.DECIMAL()) is not None
        identity = self._(ctx.IDENTITY()) is not None
        double_prec = self._(ctx.DOUBLE()) is not None
        return DataType(data_type_scaled, max, ext_type, scale, identity, double_prec)

    def visitConstant(self, ctx: tsql.ConstantContext):
        string = self._(ctx.STRING())
        binary = self._(ctx.BINARY())
        decimal = self._(ctx.DECIMAL()) is not None
        real = self._(ctx.REAL())
        float = self._(ctx.FLOAT()) is not None
        return Constant(string, binary, decimal, real, float)

    def visitPrimitive_constant(self, ctx: tsql.Primitive_constantContext):
        string = self._(ctx.STRING())
        binary = self._(ctx.BINARY())
        decimal = self._(ctx.DECIMAL()) is not None
        real = self._(ctx.REAL())
        float = self._(ctx.FLOAT()) is not None
        return PrimitiveConstant(string, binary, decimal, real, float)

    def visitKeyword(self, ctx: tsql.KeywordContext):
        abort = self._(ctx.ABORT()) is not None
        absolute = self._(ctx.ABSOLUTE()) is not None
        accent_sensitivity = self._(ctx.ACCENT_SENSITIVITY()) is not None
        access = self._(ctx.ACCESS()) is not None
        action = self._(ctx.ACTION()) is not None
        activation = self._(ctx.ACTIVATION()) is not None
        active = self._(ctx.ACTIVE()) is not None
        add = self._(ctx.ADD()) is not None
        address = self._(ctx.ADDRESS()) is not None
        aes_128 = self._(ctx.AES_128()) is not None
        aes_192 = self._(ctx.AES_192()) is not None
        aes_256 = self._(ctx.AES_256()) is not None
        affinity = self._(ctx.AFFINITY()) is not None
        after = self._(ctx.AFTER()) is not None
        aggregate = self._(ctx.AGGREGATE()) is not None
        algorithm = self._(ctx.ALGORITHM()) is not None
        all_constraints = self._(ctx.ALL_CONSTRAINTS()) is not None
        all_errormsgs = self._(ctx.ALL_ERRORMSGS()) is not None
        all_indexes = self._(ctx.ALL_INDEXES()) is not None
        all_levels = self._(ctx.ALL_LEVELS()) is not None
        allow_encrypted_value_modifications = self._(ctx.ALLOW_ENCRYPTED_VALUE_MODIFICATIONS()) is not None
        allow_page_locks = self._(ctx.ALLOW_PAGE_LOCKS()) is not None
        allow_row_locks = self._(ctx.ALLOW_ROW_LOCKS()) is not None
        allow_snapshot_isolation = self._(ctx.ALLOW_SNAPSHOT_ISOLATION()) is not None
        allowed = self._(ctx.ALLOWED()) is not None
        always = self._(ctx.ALWAYS()) is not None
        ansi_defaults = self._(ctx.ANSI_DEFAULTS()) is not None
        ansi_null_default = self._(ctx.ANSI_NULL_DEFAULT()) is not None
        ansi_null_dflt_off = self._(ctx.ANSI_NULL_DFLT_OFF()) is not None
        ansi_null_dflt_on = self._(ctx.ANSI_NULL_DFLT_ON()) is not None
        ansi_nulls = self._(ctx.ANSI_NULLS()) is not None
        ansi_padding = self._(ctx.ANSI_PADDING()) is not None
        ansi_warnings = self._(ctx.ANSI_WARNINGS()) is not None
        app_name = self._(ctx.APP_NAME()) is not None
        application_log = self._(ctx.APPLICATION_LOG()) is not None
        applock_mode = self._(ctx.APPLOCK_MODE()) is not None
        applock_test = self._(ctx.APPLOCK_TEST()) is not None
        apply = self._(ctx.APPLY()) is not None
        arithabort = self._(ctx.ARITHABORT()) is not None
        arithignore = self._(ctx.ARITHIGNORE()) is not None
        ascii = self._(ctx.ASCII()) is not None
        assembly = self._(ctx.ASSEMBLY()) is not None
        assemblyproperty = self._(ctx.ASSEMBLYPROPERTY()) is not None
        at_keyword = self._(ctx.AT_KEYWORD()) is not None
        audit = self._(ctx.AUDIT()) is not None
        audit_guid = self._(ctx.AUDIT_GUID()) is not None
        auto = self._(ctx.AUTO()) is not None
        auto_cleanup = self._(ctx.AUTO_CLEANUP()) is not None
        auto_close = self._(ctx.AUTO_CLOSE()) is not None
        auto_create_statistics = self._(ctx.AUTO_CREATE_STATISTICS()) is not None
        auto_drop = self._(ctx.AUTO_DROP()) is not None
        auto_shrink = self._(ctx.AUTO_SHRINK()) is not None
        auto_update_statistics = self._(ctx.AUTO_UPDATE_STATISTICS()) is not None
        auto_update_statistics_async = self._(ctx.AUTO_UPDATE_STATISTICS_ASYNC()) is not None
        autogrow_all_files = self._(ctx.AUTOGROW_ALL_FILES()) is not None
        autogrow_single_file = self._(ctx.AUTOGROW_SINGLE_FILE()) is not None
        availability = self._(ctx.AVAILABILITY()) is not None
        avg = self._(ctx.AVG()) is not None
        backup_clonedb = self._(ctx.BACKUP_CLONEDB()) is not None
        backup_priority = self._(ctx.BACKUP_PRIORITY()) is not None
        base64 = self._(ctx.BASE64()) is not None
        begin_dialog = self._(ctx.BEGIN_DIALOG()) is not None
        bigint = self._(ctx.BIGINT()) is not None
        binary_keyword = self._(ctx.BINARY_KEYWORD()) is not None
        binary_checksum = self._(ctx.BINARY_CHECKSUM()) is not None
        binding = self._(ctx.BINDING()) is not None
        blob_storage = self._(ctx.BLOB_STORAGE()) is not None
        broker = self._(ctx.BROKER()) is not None
        broker_instance = self._(ctx.BROKER_INSTANCE()) is not None
        bulk_logged = self._(ctx.BULK_LOGGED()) is not None
        caller = self._(ctx.CALLER()) is not None
        cap_cpu_percent = self._(ctx.CAP_CPU_PERCENT()) is not None
        cast = self._(ctx.CAST()) is not None
        try_cast = self._(ctx.TRY_CAST()) is not None
        catalog = self._(ctx.CATALOG()) is not None
        catch = self._(ctx.CATCH()) is not None
        cert_id = self._(ctx.CERT_ID()) is not None
        certencoded = self._(ctx.CERTENCODED()) is not None
        certprivatekey = self._(ctx.CERTPRIVATEKEY()) is not None
        change = self._(ctx.CHANGE()) is not None
        change_retention = self._(ctx.CHANGE_RETENTION()) is not None
        change_tracking = self._(ctx.CHANGE_TRACKING()) is not None
        char = self._(ctx.CHAR()) is not None
        charindex = self._(ctx.CHARINDEX()) is not None
        checkalloc = self._(ctx.CHECKALLOC()) is not None
        checkcatalog = self._(ctx.CHECKCATALOG()) is not None
        checkconstraints = self._(ctx.CHECKCONSTRAINTS()) is not None
        checkdb = self._(ctx.CHECKDB()) is not None
        checkfilegroup = self._(ctx.CHECKFILEGROUP()) is not None
        checksum = self._(ctx.CHECKSUM()) is not None
        checksum_agg = self._(ctx.CHECKSUM_AGG()) is not None
        checktable = self._(ctx.CHECKTABLE()) is not None
        cleantable = self._(ctx.CLEANTABLE()) is not None
        cleanup = self._(ctx.CLEANUP()) is not None
        clonedatabase = self._(ctx.CLONEDATABASE()) is not None
        col_length = self._(ctx.COL_LENGTH()) is not None
        col_name = self._(ctx.COL_NAME()) is not None
        collection = self._(ctx.COLLECTION()) is not None
        column_encryption_key = self._(ctx.COLUMN_ENCRYPTION_KEY()) is not None
        column_master_key = self._(ctx.COLUMN_MASTER_KEY()) is not None
        columnproperty = self._(ctx.COLUMNPROPERTY()) is not None
        columns = self._(ctx.COLUMNS()) is not None
        columnstore = self._(ctx.COLUMNSTORE()) is not None
        columnstore_archive = self._(ctx.COLUMNSTORE_ARCHIVE()) is not None
        committed = self._(ctx.COMMITTED()) is not None
        compatibility_level = self._(ctx.COMPATIBILITY_LEVEL()) is not None
        compress_all_row_groups = self._(ctx.COMPRESS_ALL_ROW_GROUPS()) is not None
        compression_delay = self._(ctx.COMPRESSION_DELAY()) is not None
        concat = self._(ctx.CONCAT()) is not None
        concat_ws = self._(ctx.CONCAT_WS()) is not None
        concat_null_yields_null = self._(ctx.CONCAT_NULL_YIELDS_NULL()) is not None
        content = self._(ctx.CONTENT()) is not None
        control = self._(ctx.CONTROL()) is not None
        cookie = self._(ctx.COOKIE()) is not None
        count = self._(ctx.COUNT()) is not None
        count_big = self._(ctx.COUNT_BIG()) is not None
        counter = self._(ctx.COUNTER()) is not None
        cpu = self._(ctx.CPU()) is not None
        create_new = self._(ctx.CREATE_NEW()) is not None
        creation_disposition = self._(ctx.CREATION_DISPOSITION()) is not None
        credential = self._(ctx.CREDENTIAL()) is not None
        cryptographic = self._(ctx.CRYPTOGRAPHIC()) is not None
        cume_dist = self._(ctx.CUME_DIST()) is not None
        cursor_close_on_commit = self._(ctx.CURSOR_CLOSE_ON_COMMIT()) is not None
        cursor_default = self._(ctx.CURSOR_DEFAULT()) is not None
        cursor_status = self._(ctx.CURSOR_STATUS()) is not None
        data = self._(ctx.DATA()) is not None
        data_purity = self._(ctx.DATA_PURITY()) is not None
        database_principal_id = self._(ctx.DATABASE_PRINCIPAL_ID()) is not None
        databasepropertyex = self._(ctx.DATABASEPROPERTYEX()) is not None
        datalength = self._(ctx.DATALENGTH()) is not None
        date_correlation_optimization = self._(ctx.DATE_CORRELATION_OPTIMIZATION()) is not None
        dateadd = self._(ctx.DATEADD()) is not None
        datediff = self._(ctx.DATEDIFF()) is not None
        datename = self._(ctx.DATENAME()) is not None
        datepart = self._(ctx.DATEPART()) is not None
        days = self._(ctx.DAYS()) is not None
        db_chaining = self._(ctx.DB_CHAINING()) is not None
        db_failover = self._(ctx.DB_FAILOVER()) is not None
        db_id = self._(ctx.DB_ID()) is not None
        db_name = self._(ctx.DB_NAME()) is not None
        dbcc = self._(ctx.DBCC()) is not None
        dbreindex = self._(ctx.DBREINDEX()) is not None
        decryption = self._(ctx.DECRYPTION()) is not None
        default_double_quote = self._(ctx.DEFAULT_DOUBLE_QUOTE())
        default_fulltext_language = self._(ctx.DEFAULT_FULLTEXT_LANGUAGE()) is not None
        default_language = self._(ctx.DEFAULT_LANGUAGE()) is not None
        definition = self._(ctx.DEFINITION()) is not None
        delay = self._(ctx.DELAY()) is not None
        delayed_durability = self._(ctx.DELAYED_DURABILITY()) is not None
        deleted = self._(ctx.DELETED()) is not None
        dense_rank = self._(ctx.DENSE_RANK()) is not None
        dependents = self._(ctx.DEPENDENTS()) is not None
        des = self._(ctx.DES()) is not None
        description = self._(ctx.DESCRIPTION()) is not None
        desx = self._(ctx.DESX()) is not None
        deterministic = self._(ctx.DETERMINISTIC()) is not None
        dhcp = self._(ctx.DHCP()) is not None
        dialog = self._(ctx.DIALOG()) is not None
        difference = self._(ctx.DIFFERENCE()) is not None
        directory_name = self._(ctx.DIRECTORY_NAME()) is not None
        disable = self._(ctx.DISABLE()) is not None
        disable_broker = self._(ctx.DISABLE_BROKER()) is not None
        disabled = self._(ctx.DISABLED()) is not None
        document = self._(ctx.DOCUMENT()) is not None
        drop_existing = self._(ctx.DROP_EXISTING()) is not None
        dropcleanbuffers = self._(ctx.DROPCLEANBUFFERS()) is not None
        dynamic = self._(ctx.DYNAMIC()) is not None
        elements = self._(ctx.ELEMENTS()) is not None
        emergency = self._(ctx.EMERGENCY()) is not None
        empty = self._(ctx.EMPTY()) is not None
        enable = self._(ctx.ENABLE()) is not None
        enable_broker = self._(ctx.ENABLE_BROKER()) is not None
        encrypted = self._(ctx.ENCRYPTED()) is not None
        encrypted_value = self._(ctx.ENCRYPTED_VALUE()) is not None
        encryption = self._(ctx.ENCRYPTION()) is not None
        encryption_type = self._(ctx.ENCRYPTION_TYPE()) is not None
        endpoint_url = self._(ctx.ENDPOINT_URL()) is not None
        error_broker_conversations = self._(ctx.ERROR_BROKER_CONVERSATIONS()) is not None
        estimateonly = self._(ctx.ESTIMATEONLY()) is not None
        exclusive = self._(ctx.EXCLUSIVE()) is not None
        executable = self._(ctx.EXECUTABLE()) is not None
        exist = self._(ctx.EXIST()) is not None
        exist_square_bracket = self._(ctx.EXIST_SQUARE_BRACKET()) is not None
        expand = self._(ctx.EXPAND()) is not None
        expiry_date = self._(ctx.EXPIRY_DATE()) is not None
        explicit = self._(ctx.EXPLICIT()) is not None
        extended_logical_checks = self._(ctx.EXTENDED_LOGICAL_CHECKS()) is not None
        fail_operation = self._(ctx.FAIL_OPERATION()) is not None
        failover_mode = self._(ctx.FAILOVER_MODE()) is not None
        failure = self._(ctx.FAILURE()) is not None
        failure_condition_level = self._(ctx.FAILURE_CONDITION_LEVEL()) is not None
        fast = self._(ctx.FAST()) is not None
        fast_forward = self._(ctx.FAST_FORWARD()) is not None
        file_id = self._(ctx.FILE_ID()) is not None
        file_idex = self._(ctx.FILE_IDEX()) is not None
        file_name = self._(ctx.FILE_NAME()) is not None
        filegroup = self._(ctx.FILEGROUP()) is not None
        filegroup_id = self._(ctx.FILEGROUP_ID()) is not None
        filegroup_name = self._(ctx.FILEGROUP_NAME()) is not None
        filegroupproperty = self._(ctx.FILEGROUPPROPERTY()) is not None
        filegrowth = self._(ctx.FILEGROWTH()) is not None
        filename = self._(ctx.FILENAME()) is not None
        filepath = self._(ctx.FILEPATH()) is not None
        fileproperty = self._(ctx.FILEPROPERTY()) is not None
        filepropertyex = self._(ctx.FILEPROPERTYEX()) is not None
        filestream = self._(ctx.FILESTREAM()) is not None
        filter = self._(ctx.FILTER()) is not None
        first = self._(ctx.FIRST()) is not None
        first_value = self._(ctx.FIRST_VALUE()) is not None
        fmtonly = self._(ctx.FMTONLY()) is not None
        following = self._(ctx.FOLLOWING()) is not None
        force = self._(ctx.FORCE()) is not None
        force_failover_allow_data_loss = self._(ctx.FORCE_FAILOVER_ALLOW_DATA_LOSS()) is not None
        forced = self._(ctx.FORCED()) is not None
        forceplan = self._(ctx.FORCEPLAN()) is not None
        forcescan = self._(ctx.FORCESCAN()) is not None
        format = self._(ctx.FORMAT()) is not None
        forward_only = self._(ctx.FORWARD_ONLY()) is not None
        free = self._(ctx.FREE()) is not None
        fullscan = self._(ctx.FULLSCAN()) is not None
        fulltext = self._(ctx.FULLTEXT()) is not None
        fulltextcatalogproperty = self._(ctx.FULLTEXTCATALOGPROPERTY()) is not None
        fulltextserviceproperty = self._(ctx.FULLTEXTSERVICEPROPERTY()) is not None
        gb = self._(ctx.GB()) is not None
        generated = self._(ctx.GENERATED()) is not None
        getdate = self._(ctx.GETDATE()) is not None
        getutcdate = self._(ctx.GETUTCDATE()) is not None
        global_ = self._(ctx.GLOBAL()) is not None
        go_ = self._(ctx.GO()) is not None
        greatest = self._(ctx.GREATEST()) is not None
        group_max_requests = self._(ctx.GROUP_MAX_REQUESTS()) is not None
        grouping = self._(ctx.GROUPING()) is not None
        grouping_id = self._(ctx.GROUPING_ID()) is not None
        hadr = self._(ctx.HADR()) is not None
        has_dbaccess = self._(ctx.HAS_DBACCESS()) is not None
        has_perms_by_name = self._(ctx.HAS_PERMS_BY_NAME()) is not None
        hash = self._(ctx.HASH()) is not None
        health_check_timeout = self._(ctx.HEALTH_CHECK_TIMEOUT()) is not None
        hidden_keyword = self._(ctx.HIDDEN_KEYWORD()) is not None
        high = self._(ctx.HIGH()) is not None
        honor_broker_priority = self._(ctx.HONOR_BROKER_PRIORITY()) is not None
        hours = self._(ctx.HOURS()) is not None
        ident_current = self._(ctx.IDENT_CURRENT()) is not None
        ident_incr = self._(ctx.IDENT_INCR()) is not None
        ident_seed = self._(ctx.IDENT_SEED()) is not None
        identity_value = self._(ctx.IDENTITY_VALUE()) is not None
        ignore_constraints = self._(ctx.IGNORE_CONSTRAINTS()) is not None
        ignore_dup_key = self._(ctx.IGNORE_DUP_KEY()) is not None
        ignore_nonclustered_columnstore_index = self._(ctx.IGNORE_NONCLUSTERED_COLUMNSTORE_INDEX()) is not None
        ignore_replicated_table_cache = self._(ctx.IGNORE_REPLICATED_TABLE_CACHE()) is not None
        ignore_triggers = self._(ctx.IGNORE_TRIGGERS()) is not None
        immediate = self._(ctx.IMMEDIATE()) is not None
        impersonate = self._(ctx.IMPERSONATE()) is not None
        implicit_transactions = self._(ctx.IMPLICIT_TRANSACTIONS()) is not None
        importance = self._(ctx.IMPORTANCE()) is not None
        include_null_values = self._(ctx.INCLUDE_NULL_VALUES()) is not None
        incremental = self._(ctx.INCREMENTAL()) is not None
        index_col = self._(ctx.INDEX_COL()) is not None
        indexkey_property = self._(ctx.INDEXKEY_PROPERTY()) is not None
        indexproperty = self._(ctx.INDEXPROPERTY()) is not None
        initiator = self._(ctx.INITIATOR()) is not None
        input = self._(ctx.INPUT()) is not None
        insensitive = self._(ctx.INSENSITIVE()) is not None
        inserted = self._(ctx.INSERTED()) is not None
        int = self._(ctx.INT()) is not None
        ip = self._(ctx.IP()) is not None
        is_member = self._(ctx.IS_MEMBER()) is not None
        is_rolemember = self._(ctx.IS_ROLEMEMBER()) is not None
        is_srvrolemember = self._(ctx.IS_SRVROLEMEMBER()) is not None
        isjson = self._(ctx.ISJSON()) is not None
        isolation = self._(ctx.ISOLATION()) is not None
        job = self._(ctx.JOB()) is not None
        json = self._(ctx.JSON()) is not None
        json_object = self._(ctx.JSON_OBJECT()) is not None
        json_array = self._(ctx.JSON_ARRAY()) is not None
        json_value = self._(ctx.JSON_VALUE()) is not None
        json_query = self._(ctx.JSON_QUERY()) is not None
        json_modify = self._(ctx.JSON_MODIFY()) is not None
        json_path_exists = self._(ctx.JSON_PATH_EXISTS()) is not None
        kb = self._(ctx.KB()) is not None
        keep = self._(ctx.KEEP()) is not None
        keepdefaults = self._(ctx.KEEPDEFAULTS()) is not None
        keepfixed = self._(ctx.KEEPFIXED()) is not None
        keepidentity = self._(ctx.KEEPIDENTITY()) is not None
        key_source = self._(ctx.KEY_SOURCE()) is not None
        keys = self._(ctx.KEYS()) is not None
        keyset = self._(ctx.KEYSET()) is not None
        lag = self._(ctx.LAG()) is not None
        last = self._(ctx.LAST()) is not None
        last_value = self._(ctx.LAST_VALUE()) is not None
        lead = self._(ctx.LEAD()) is not None
        least = self._(ctx.LEAST()) is not None
        len_ = self._(ctx.LEN()) is not None
        level = self._(ctx.LEVEL()) is not None
        list = self._(ctx.LIST()) is not None
        listener = self._(ctx.LISTENER()) is not None
        listener_url = self._(ctx.LISTENER_URL()) is not None
        lob_compaction = self._(ctx.LOB_COMPACTION()) is not None
        local = self._(ctx.LOCAL()) is not None
        location = self._(ctx.LOCATION()) is not None
        lock = self._(ctx.LOCK()) is not None
        lock_escalation = self._(ctx.LOCK_ESCALATION()) is not None
        login = self._(ctx.LOGIN()) is not None
        loginproperty = self._(ctx.LOGINPROPERTY()) is not None
        loop = self._(ctx.LOOP()) is not None
        low = self._(ctx.LOW()) is not None
        lower = self._(ctx.LOWER()) is not None
        ltrim = self._(ctx.LTRIM()) is not None
        manual = self._(ctx.MANUAL()) is not None
        mark = self._(ctx.MARK()) is not None
        masked = self._(ctx.MASKED()) is not None
        materialized = self._(ctx.MATERIALIZED()) is not None
        max = self._(ctx.MAX()) is not None
        max_cpu_percent = self._(ctx.MAX_CPU_PERCENT()) is not None
        max_dop = self._(ctx.MAX_DOP()) is not None
        max_files = self._(ctx.MAX_FILES()) is not None
        max_iops_per_volume = self._(ctx.MAX_IOPS_PER_VOLUME()) is not None
        max_memory_percent = self._(ctx.MAX_MEMORY_PERCENT()) is not None
        max_processes = self._(ctx.MAX_PROCESSES()) is not None
        max_queue_readers = self._(ctx.MAX_QUEUE_READERS()) is not None
        max_rollover_files = self._(ctx.MAX_ROLLOVER_FILES()) is not None
        maxdop = self._(ctx.MAXDOP()) is not None
        maxrecursion = self._(ctx.MAXRECURSION()) is not None
        maxsize = self._(ctx.MAXSIZE()) is not None
        mb = self._(ctx.MB()) is not None
        medium = self._(ctx.MEDIUM()) is not None
        memory_optimized_data = self._(ctx.MEMORY_OPTIMIZED_DATA()) is not None
        message = self._(ctx.MESSAGE()) is not None
        min = self._(ctx.MIN()) is not None
        min_active_rowversion = self._(ctx.MIN_ACTIVE_ROWVERSION()) is not None
        min_cpu_percent = self._(ctx.MIN_CPU_PERCENT()) is not None
        min_iops_per_volume = self._(ctx.MIN_IOPS_PER_VOLUME()) is not None
        min_memory_percent = self._(ctx.MIN_MEMORY_PERCENT()) is not None
        minutes = self._(ctx.MINUTES()) is not None
        mirror_address = self._(ctx.MIRROR_ADDRESS()) is not None
        mixed_page_allocation = self._(ctx.MIXED_PAGE_ALLOCATION()) is not None
        mode = self._(ctx.MODE()) is not None
        modify = self._(ctx.MODIFY()) is not None
        modify_square_bracket = self._(ctx.MODIFY_SQUARE_BRACKET()) is not None
        move = self._(ctx.MOVE()) is not None
        multi_user = self._(ctx.MULTI_USER()) is not None
        name = self._(ctx.NAME()) is not None
        nchar = self._(ctx.NCHAR()) is not None
        nested_triggers = self._(ctx.NESTED_TRIGGERS()) is not None
        new_account = self._(ctx.NEW_ACCOUNT()) is not None
        new_broker = self._(ctx.NEW_BROKER()) is not None
        new_password = self._(ctx.NEW_PASSWORD()) is not None
        newname = self._(ctx.NEWNAME()) is not None
        next = self._(ctx.NEXT()) is not None
        no = self._(ctx.NO()) is not None
        no_infomsgs = self._(ctx.NO_INFOMSGS()) is not None
        no_querystore = self._(ctx.NO_QUERYSTORE()) is not None
        no_statistics = self._(ctx.NO_STATISTICS()) is not None
        no_truncate = self._(ctx.NO_TRUNCATE()) is not None
        no_wait = self._(ctx.NO_WAIT()) is not None
        nocount = self._(ctx.NOCOUNT()) is not None
        nodes = self._(ctx.NODES()) is not None
        noexec = self._(ctx.NOEXEC()) is not None
        noexpand = self._(ctx.NOEXPAND()) is not None
        noindex = self._(ctx.NOINDEX()) is not None
        nolock = self._(ctx.NOLOCK()) is not None
        non_transacted_access = self._(ctx.NON_TRANSACTED_ACCESS()) is not None
        norecompute = self._(ctx.NORECOMPUTE()) is not None
        norecovery = self._(ctx.NORECOVERY()) is not None
        notifications = self._(ctx.NOTIFICATIONS()) is not None
        nowait = self._(ctx.NOWAIT()) is not None
        ntile = self._(ctx.NTILE()) is not None
        null_double_quote = self._(ctx.NULL_DOUBLE_QUOTE())
        numanode = self._(ctx.NUMANODE()) is not None
        number = self._(ctx.NUMBER()) is not None
        numeric_roundabort = self._(ctx.NUMERIC_ROUNDABORT()) is not None
        object = self._(ctx.OBJECT()) is not None
        object_definition = self._(ctx.OBJECT_DEFINITION()) is not None
        object_id = self._(ctx.OBJECT_ID()) is not None
        object_name = self._(ctx.OBJECT_NAME()) is not None
        object_schema_name = self._(ctx.OBJECT_SCHEMA_NAME()) is not None
        objectproperty = self._(ctx.OBJECTPROPERTY()) is not None
        objectpropertyex = self._(ctx.OBJECTPROPERTYEX()) is not None
        offline = self._(ctx.OFFLINE()) is not None
        offset = self._(ctx.OFFSET()) is not None
        old_account = self._(ctx.OLD_ACCOUNT()) is not None
        online = self._(ctx.ONLINE()) is not None
        only = self._(ctx.ONLY()) is not None
        open_existing = self._(ctx.OPEN_EXISTING()) is not None
        openjson = self._(ctx.OPENJSON()) is not None
        optimistic = self._(ctx.OPTIMISTIC()) is not None
        optimize = self._(ctx.OPTIMIZE()) is not None
        optimize_for_sequential_key = self._(ctx.OPTIMIZE_FOR_SEQUENTIAL_KEY()) is not None
        original_db_name = self._(ctx.ORIGINAL_DB_NAME()) is not None
        original_login = self._(ctx.ORIGINAL_LOGIN()) is not None
        out = self._(ctx.OUT()) is not None
        output = self._(ctx.OUTPUT()) is not None
        override = self._(ctx.OVERRIDE()) is not None
        owner = self._(ctx.OWNER()) is not None
        ownership = self._(ctx.OWNERSHIP()) is not None
        pad_index = self._(ctx.PAD_INDEX()) is not None
        page_verify = self._(ctx.PAGE_VERIFY()) is not None
        pagecount = self._(ctx.PAGECOUNT()) is not None
        paglock = self._(ctx.PAGLOCK()) is not None
        parameterization = self._(ctx.PARAMETERIZATION()) is not None
        parsename = self._(ctx.PARSENAME()) is not None
        parseonly = self._(ctx.PARSEONLY()) is not None
        partition = self._(ctx.PARTITION()) is not None
        partitions = self._(ctx.PARTITIONS()) is not None
        partner = self._(ctx.PARTNER()) is not None
        path = self._(ctx.PATH()) is not None
        patindex = self._(ctx.PATINDEX()) is not None
        pause = self._(ctx.PAUSE()) is not None
        pdw_showspaceused = self._(ctx.PDW_SHOWSPACEUSED()) is not None
        percent_rank = self._(ctx.PERCENT_RANK()) is not None
        percentile_cont = self._(ctx.PERCENTILE_CONT()) is not None
        percentile_disc = self._(ctx.PERCENTILE_DISC()) is not None
        permissions = self._(ctx.PERMISSIONS()) is not None
        persist_sample_percent = self._(ctx.PERSIST_SAMPLE_PERCENT()) is not None
        physical_only = self._(ctx.PHYSICAL_ONLY()) is not None
        poison_message_handling = self._(ctx.POISON_MESSAGE_HANDLING()) is not None
        pool = self._(ctx.POOL()) is not None
        port = self._(ctx.PORT()) is not None
        preceding = self._(ctx.PRECEDING()) is not None
        primary_role = self._(ctx.PRIMARY_ROLE()) is not None
        prior = self._(ctx.PRIOR()) is not None
        priority = self._(ctx.PRIORITY()) is not None
        priority_level = self._(ctx.PRIORITY_LEVEL()) is not None
        private = self._(ctx.PRIVATE()) is not None
        private_key = self._(ctx.PRIVATE_KEY()) is not None
        privileges = self._(ctx.PRIVILEGES()) is not None
        proccache = self._(ctx.PROCCACHE()) is not None
        procedure_name = self._(ctx.PROCEDURE_NAME()) is not None
        property = self._(ctx.PROPERTY()) is not None
        provider = self._(ctx.PROVIDER()) is not None
        provider_key_name = self._(ctx.PROVIDER_KEY_NAME()) is not None
        pwdcompare = self._(ctx.PWDCOMPARE()) is not None
        pwdencrypt = self._(ctx.PWDENCRYPT()) is not None
        query = self._(ctx.QUERY()) is not None
        query_square_bracket = self._(ctx.QUERY_SQUARE_BRACKET()) is not None
        queue = self._(ctx.QUEUE()) is not None
        queue_delay = self._(ctx.QUEUE_DELAY()) is not None
        quoted_identifier = self._(ctx.QUOTED_IDENTIFIER()) is not None
        quotename = self._(ctx.QUOTENAME()) is not None
        randomized = self._(ctx.RANDOMIZED()) is not None
        range_ = self._(ctx.RANGE()) is not None
        rank = self._(ctx.RANK()) is not None
        rc2 = self._(ctx.RC2()) is not None
        rc4 = self._(ctx.RC4()) is not None
        rc4_128 = self._(ctx.RC4_128()) is not None
        read_committed_snapshot = self._(ctx.READ_COMMITTED_SNAPSHOT()) is not None
        read_only = self._(ctx.READ_ONLY()) is not None
        read_only_routing_list = self._(ctx.READ_ONLY_ROUTING_LIST()) is not None
        read_write = self._(ctx.READ_WRITE()) is not None
        readcommitted = self._(ctx.READCOMMITTED()) is not None
        readcommittedlock = self._(ctx.READCOMMITTEDLOCK()) is not None
        readonly = self._(ctx.READONLY()) is not None
        readpast = self._(ctx.READPAST()) is not None
        readuncommitted = self._(ctx.READUNCOMMITTED()) is not None
        readwrite = self._(ctx.READWRITE()) is not None
        rebuild = self._(ctx.REBUILD()) is not None
        receive = self._(ctx.RECEIVE()) is not None
        recompile = self._(ctx.RECOMPILE()) is not None
        recovery = self._(ctx.RECOVERY()) is not None
        recursive_triggers = self._(ctx.RECURSIVE_TRIGGERS()) is not None
        relative = self._(ctx.RELATIVE()) is not None
        remote = self._(ctx.REMOTE()) is not None
        remote_proc_transactions = self._(ctx.REMOTE_PROC_TRANSACTIONS()) is not None
        remote_service_name = self._(ctx.REMOTE_SERVICE_NAME()) is not None
        remove = self._(ctx.REMOVE()) is not None
        reorganize = self._(ctx.REORGANIZE()) is not None
        repair_allow_data_loss = self._(ctx.REPAIR_ALLOW_DATA_LOSS()) is not None
        repair_fast = self._(ctx.REPAIR_FAST()) is not None
        repair_rebuild = self._(ctx.REPAIR_REBUILD()) is not None
        repeatable = self._(ctx.REPEATABLE()) is not None
        repeatableread = self._(ctx.REPEATABLEREAD()) is not None
        replace = self._(ctx.REPLACE()) is not None
        replica = self._(ctx.REPLICA()) is not None
        replicate = self._(ctx.REPLICATE()) is not None
        request_max_cpu_time_sec = self._(ctx.REQUEST_MAX_CPU_TIME_SEC()) is not None
        request_max_memory_grant_percent = self._(ctx.REQUEST_MAX_MEMORY_GRANT_PERCENT()) is not None
        request_memory_grant_timeout_sec = self._(ctx.REQUEST_MEMORY_GRANT_TIMEOUT_SEC()) is not None
        required_synchronized_secondaries_to_commit = self._(ctx.REQUIRED_SYNCHRONIZED_SECONDARIES_TO_COMMIT()) is not None
        resample = self._(ctx.RESAMPLE()) is not None
        reserve_disk_space = self._(ctx.RESERVE_DISK_SPACE()) is not None
        resource = self._(ctx.RESOURCE()) is not None
        resource_manager_location = self._(ctx.RESOURCE_MANAGER_LOCATION()) is not None
        restricted_user = self._(ctx.RESTRICTED_USER()) is not None
        resumable = self._(ctx.RESUMABLE()) is not None
        retention = self._(ctx.RETENTION()) is not None
        reverse = self._(ctx.REVERSE()) is not None
        robust = self._(ctx.ROBUST()) is not None
        root = self._(ctx.ROOT()) is not None
        route = self._(ctx.ROUTE()) is not None
        row = self._(ctx.ROW()) is not None
        row_number = self._(ctx.ROW_NUMBER()) is not None
        rowguid = self._(ctx.ROWGUID()) is not None
        rowlock = self._(ctx.ROWLOCK()) is not None
        rows = self._(ctx.ROWS()) is not None
        rtrim = self._(ctx.RTRIM()) is not None
        sample = self._(ctx.SAMPLE()) is not None
        schema_id = self._(ctx.SCHEMA_ID()) is not None
        schema_name = self._(ctx.SCHEMA_NAME()) is not None
        schemabinding = self._(ctx.SCHEMABINDING()) is not None
        scope_identity = self._(ctx.SCOPE_IDENTITY()) is not None
        scoped = self._(ctx.SCOPED()) is not None
        scroll = self._(ctx.SCROLL()) is not None
        scroll_locks = self._(ctx.SCROLL_LOCKS()) is not None
        search = self._(ctx.SEARCH()) is not None
        secondary = self._(ctx.SECONDARY()) is not None
        secondary_only = self._(ctx.SECONDARY_ONLY()) is not None
        secondary_role = self._(ctx.SECONDARY_ROLE()) is not None
        seconds = self._(ctx.SECONDS()) is not None
        secret = self._(ctx.SECRET()) is not None
        securables = self._(ctx.SECURABLES()) is not None
        security = self._(ctx.SECURITY()) is not None
        security_log = self._(ctx.SECURITY_LOG()) is not None
        seeding_mode = self._(ctx.SEEDING_MODE()) is not None
        self = self._(ctx.SELF()) is not None
        semi_sensitive = self._(ctx.SEMI_SENSITIVE()) is not None
        send = self._(ctx.SEND()) is not None
        sent = self._(ctx.SENT()) is not None
        sequence = self._(ctx.SEQUENCE()) is not None
        sequence_number = self._(ctx.SEQUENCE_NUMBER()) is not None
        serializable = self._(ctx.SERIALIZABLE()) is not None
        serverproperty = self._(ctx.SERVERPROPERTY()) is not None
        servicebroker = self._(ctx.SERVICEBROKER()) is not None
        sessionproperty = self._(ctx.SESSIONPROPERTY()) is not None
        session_timeout = self._(ctx.SESSION_TIMEOUT()) is not None
        seterror = self._(ctx.SETERROR()) is not None
        share = self._(ctx.SHARE()) is not None
        shared = self._(ctx.SHARED()) is not None
        showcontig = self._(ctx.SHOWCONTIG()) is not None
        showplan = self._(ctx.SHOWPLAN()) is not None
        showplan_all = self._(ctx.SHOWPLAN_ALL()) is not None
        showplan_text = self._(ctx.SHOWPLAN_TEXT()) is not None
        showplan_xml = self._(ctx.SHOWPLAN_XML()) is not None
        signature = self._(ctx.SIGNATURE()) is not None
        simple = self._(ctx.SIMPLE()) is not None
        single_user = self._(ctx.SINGLE_USER()) is not None
        size = self._(ctx.SIZE()) is not None
        smallint = self._(ctx.SMALLINT()) is not None
        snapshot = self._(ctx.SNAPSHOT()) is not None
        sort_in_tempdb = self._(ctx.SORT_IN_TEMPDB()) is not None
        soundex = self._(ctx.SOUNDEX()) is not None
        space_keyword = self._(ctx.SPACE_KEYWORD()) is not None
        sparse = self._(ctx.SPARSE()) is not None
        spatial_window_max_cells = self._(ctx.SPATIAL_WINDOW_MAX_CELLS()) is not None
        sql_variant_property = self._(ctx.SQL_VARIANT_PROPERTY()) is not None
        standby = self._(ctx.STANDBY()) is not None
        start_date = self._(ctx.START_DATE()) is not None
        static = self._(ctx.STATIC()) is not None
        statistics_incremental = self._(ctx.STATISTICS_INCREMENTAL()) is not None
        statistics_norecompute = self._(ctx.STATISTICS_NORECOMPUTE()) is not None
        stats_date = self._(ctx.STATS_DATE()) is not None
        stats_stream = self._(ctx.STATS_STREAM()) is not None
        status = self._(ctx.STATUS()) is not None
        statusonly = self._(ctx.STATUSONLY()) is not None
        stdev = self._(ctx.STDEV()) is not None
        stdevp = self._(ctx.STDEVP()) is not None
        stoplist = self._(ctx.STOPLIST()) is not None
        str = self._(ctx.STR()) is not None
        string_agg = self._(ctx.STRING_AGG()) is not None
        string_escape = self._(ctx.STRING_ESCAPE()) is not None
        stuff = self._(ctx.STUFF()) is not None
        subject = self._(ctx.SUBJECT()) is not None
        subscribe = self._(ctx.SUBSCRIBE()) is not None
        subscription = self._(ctx.SUBSCRIPTION()) is not None
        substring = self._(ctx.SUBSTRING()) is not None
        sum = self._(ctx.SUM()) is not None
        suser_id = self._(ctx.SUSER_ID()) is not None
        suser_name = self._(ctx.SUSER_NAME()) is not None
        suser_sid = self._(ctx.SUSER_SID()) is not None
        suser_sname = self._(ctx.SUSER_SNAME()) is not None
        suspend = self._(ctx.SUSPEND()) is not None
        symmetric = self._(ctx.SYMMETRIC()) is not None
        synchronous_commit = self._(ctx.SYNCHRONOUS_COMMIT()) is not None
        synonym = self._(ctx.SYNONYM()) is not None
        system = self._(ctx.SYSTEM()) is not None
        tableresults = self._(ctx.TABLERESULTS()) is not None
        tablock = self._(ctx.TABLOCK()) is not None
        tablockx = self._(ctx.TABLOCKX()) is not None
        take = self._(ctx.TAKE()) is not None
        target_recovery_time = self._(ctx.TARGET_RECOVERY_TIME()) is not None
        tb = self._(ctx.TB()) is not None
        textimage_on = self._(ctx.TEXTIMAGE_ON()) is not None
        throw = self._(ctx.THROW()) is not None
        ties = self._(ctx.TIES()) is not None
        time = self._(ctx.TIME()) is not None
        timeout = self._(ctx.TIMEOUT()) is not None
        timer = self._(ctx.TIMER()) is not None
        tinyint = self._(ctx.TINYINT()) is not None
        torn_page_detection = self._(ctx.TORN_PAGE_DETECTION()) is not None
        tracking = self._(ctx.TRACKING()) is not None
        transaction_id = self._(ctx.TRANSACTION_ID()) is not None
        transform_noise_words = self._(ctx.TRANSFORM_NOISE_WORDS()) is not None
        translate = self._(ctx.TRANSLATE()) is not None
        trim = self._(ctx.TRIM()) is not None
        triple_des = self._(ctx.TRIPLE_DES()) is not None
        triple_des_3key = self._(ctx.TRIPLE_DES_3KEY()) is not None
        trustworthy = self._(ctx.TRUSTWORTHY()) is not None
        try_ = self._(ctx.TRY()) is not None
        tsql = self._(ctx.TSQL()) is not None
        two_digit_year_cutoff = self._(ctx.TWO_DIGIT_YEAR_CUTOFF()) is not None
        type_ = self._(ctx.TYPE()) is not None
        type_id = self._(ctx.TYPE_ID()) is not None
        type_name = self._(ctx.TYPE_NAME()) is not None
        type_warning = self._(ctx.TYPE_WARNING()) is not None
        typeproperty = self._(ctx.TYPEPROPERTY()) is not None
        unbounded = self._(ctx.UNBOUNDED()) is not None
        uncommitted = self._(ctx.UNCOMMITTED()) is not None
        unicode = self._(ctx.UNICODE()) is not None
        unknown = self._(ctx.UNKNOWN()) is not None
        unlimited = self._(ctx.UNLIMITED()) is not None
        unmask = self._(ctx.UNMASK()) is not None
        uow = self._(ctx.UOW()) is not None
        updlock = self._(ctx.UPDLOCK()) is not None
        upper = self._(ctx.UPPER()) is not None
        user_id = self._(ctx.USER_ID()) is not None
        user_name = self._(ctx.USER_NAME()) is not None
        using = self._(ctx.USING()) is not None
        valid_xml = self._(ctx.VALID_XML()) is not None
        validation = self._(ctx.VALIDATION()) is not None
        value = self._(ctx.VALUE()) is not None
        value_square_bracket = self._(ctx.VALUE_SQUARE_BRACKET()) is not None
        var_ = self._(ctx.VAR()) is not None
        varbinary_keyword = self._(ctx.VARBINARY_KEYWORD()) is not None
        varp = self._(ctx.VARP()) is not None
        verify_clonedb = self._(ctx.VERIFY_CLONEDB()) is not None
        version = self._(ctx.VERSION()) is not None
        view_metadata = self._(ctx.VIEW_METADATA()) is not None
        views = self._(ctx.VIEWS()) is not None
        wait = self._(ctx.WAIT()) is not None
        well_formed_xml = self._(ctx.WELL_FORMED_XML()) is not None
        without_array_wrapper = self._(ctx.WITHOUT_ARRAY_WRAPPER()) is not None
        work = self._(ctx.WORK()) is not None
        workload = self._(ctx.WORKLOAD()) is not None
        xlock = self._(ctx.XLOCK()) is not None
        xml = self._(ctx.XML()) is not None
        xml_compression = self._(ctx.XML_COMPRESSION()) is not None
        xmldata = self._(ctx.XMLDATA()) is not None
        xmlnamespaces = self._(ctx.XMLNAMESPACES()) is not None
        xmlschema = self._(ctx.XMLSCHEMA()) is not None
        xsinil = self._(ctx.XSINIL()) is not None
        zone = self._(ctx.ZONE()) is not None
        abort_after_wait = self._(ctx.ABORT_AFTER_WAIT()) is not None
        absent = self._(ctx.ABSENT()) is not None
        administer = self._(ctx.ADMINISTER()) is not None
        aes = self._(ctx.AES()) is not None
        allow_connections = self._(ctx.ALLOW_CONNECTIONS()) is not None
        allow_multiple_event_loss = self._(ctx.ALLOW_MULTIPLE_EVENT_LOSS()) is not None
        allow_single_event_loss = self._(ctx.ALLOW_SINGLE_EVENT_LOSS()) is not None
        anonymous = self._(ctx.ANONYMOUS()) is not None
        append_ = self._(ctx.APPEND()) is not None
        application = self._(ctx.APPLICATION()) is not None
        asymmetric = self._(ctx.ASYMMETRIC()) is not None
        asynchronous_commit = self._(ctx.ASYNCHRONOUS_COMMIT()) is not None
        authenticate = self._(ctx.AUTHENTICATE()) is not None
        authentication = self._(ctx.AUTHENTICATION()) is not None
        automated_backup_preference = self._(ctx.AUTOMATED_BACKUP_PREFERENCE()) is not None
        automatic = self._(ctx.AUTOMATIC()) is not None
        availability_mode = self._(ctx.AVAILABILITY_MODE()) is not None
        before = self._(ctx.BEFORE()) is not None
        block = self._(ctx.BLOCK()) is not None
        blockers = self._(ctx.BLOCKERS()) is not None
        blocksize = self._(ctx.BLOCKSIZE()) is not None
        blocking_hierarchy = self._(ctx.BLOCKING_HIERARCHY()) is not None
        buffer = self._(ctx.BUFFER()) is not None
        buffercount = self._(ctx.BUFFERCOUNT()) is not None
        cache = self._(ctx.CACHE()) is not None
        called = self._(ctx.CALLED()) is not None
        certificate = self._(ctx.CERTIFICATE()) is not None
        changetable = self._(ctx.CHANGETABLE()) is not None
        changes = self._(ctx.CHANGES()) is not None
        check_policy = self._(ctx.CHECK_POLICY()) is not None
        check_expiration = self._(ctx.CHECK_EXPIRATION()) is not None
        classifier_function = self._(ctx.CLASSIFIER_FUNCTION()) is not None
        cluster = self._(ctx.CLUSTER()) is not None
        compress = self._(ctx.COMPRESS()) is not None
        compression = self._(ctx.COMPRESSION()) is not None
        connect = self._(ctx.CONNECT()) is not None
        connection = self._(ctx.CONNECTION()) is not None
        configuration = self._(ctx.CONFIGURATION()) is not None
        connectionproperty = self._(ctx.CONNECTIONPROPERTY()) is not None
        containment = self._(ctx.CONTAINMENT()) is not None
        context = self._(ctx.CONTEXT()) is not None
        context_info = self._(ctx.CONTEXT_INFO()) is not None
        continue_after_error = self._(ctx.CONTINUE_AFTER_ERROR()) is not None
        contract = self._(ctx.CONTRACT()) is not None
        contract_name = self._(ctx.CONTRACT_NAME()) is not None
        conversation = self._(ctx.CONVERSATION()) is not None
        copy_only = self._(ctx.COPY_ONLY()) is not None
        current_request_id = self._(ctx.CURRENT_REQUEST_ID()) is not None
        current_transaction_id = self._(ctx.CURRENT_TRANSACTION_ID()) is not None
        cycle = self._(ctx.CYCLE()) is not None
        data_compression = self._(ctx.DATA_COMPRESSION()) is not None
        data_source = self._(ctx.DATA_SOURCE()) is not None
        database_mirroring = self._(ctx.DATABASE_MIRRORING()) is not None
        dataspace = self._(ctx.DATASPACE()) is not None
        ddl = self._(ctx.DDL()) is not None
        decompress = self._(ctx.DECOMPRESS()) is not None
        default_database = self._(ctx.DEFAULT_DATABASE()) is not None
        default_schema = self._(ctx.DEFAULT_SCHEMA()) is not None
        diagnostics = self._(ctx.DIAGNOSTICS()) is not None
        differential = self._(ctx.DIFFERENTIAL()) is not None
        distribution = self._(ctx.DISTRIBUTION()) is not None
        dtc_support = self._(ctx.DTC_SUPPORT()) is not None
        enabled = self._(ctx.ENABLED()) is not None
        endpoint = self._(ctx.ENDPOINT()) is not None
        error = self._(ctx.ERROR()) is not None
        error_line = self._(ctx.ERROR_LINE()) is not None
        error_message = self._(ctx.ERROR_MESSAGE()) is not None
        error_number = self._(ctx.ERROR_NUMBER()) is not None
        error_procedure = self._(ctx.ERROR_PROCEDURE()) is not None
        error_severity = self._(ctx.ERROR_SEVERITY()) is not None
        error_state = self._(ctx.ERROR_STATE()) is not None
        event = self._(ctx.EVENT()) is not None
        eventdata = self._(ctx.EVENTDATA()) is not None
        event_retention_mode = self._(ctx.EVENT_RETENTION_MODE()) is not None
        executable_file = self._(ctx.EXECUTABLE_FILE()) is not None
        expiredate = self._(ctx.EXPIREDATE()) is not None
        extension = self._(ctx.EXTENSION()) is not None
        external_access = self._(ctx.EXTERNAL_ACCESS()) is not None
        failover = self._(ctx.FAILOVER()) is not None
        failureconditionlevel = self._(ctx.FAILURECONDITIONLEVEL()) is not None
        fan_in = self._(ctx.FAN_IN()) is not None
        file_snapshot = self._(ctx.FILE_SNAPSHOT()) is not None
        forceseek = self._(ctx.FORCESEEK()) is not None
        force_service_allow_data_loss = self._(ctx.FORCE_SERVICE_ALLOW_DATA_LOSS()) is not None
        formatmessage = self._(ctx.FORMATMESSAGE()) is not None
        get = self._(ctx.GET()) is not None
        get_filestream_transaction_context = self._(ctx.GET_FILESTREAM_TRANSACTION_CONTEXT()) is not None
        getancestor = self._(ctx.GETANCESTOR()) is not None
        getansinull = self._(ctx.GETANSINULL()) is not None
        getdescendant = self._(ctx.GETDESCENDANT()) is not None
        getlevel = self._(ctx.GETLEVEL()) is not None
        getreparentedvalue = self._(ctx.GETREPARENTEDVALUE()) is not None
        getroot = self._(ctx.GETROOT()) is not None
        governor = self._(ctx.GOVERNOR()) is not None
        hashed = self._(ctx.HASHED()) is not None
        healthchecktimeout = self._(ctx.HEALTHCHECKTIMEOUT()) is not None
        heap = self._(ctx.HEAP()) is not None
        hierarchyid = self._(ctx.HIERARCHYID()) is not None
        host_id = self._(ctx.HOST_ID()) is not None
        host_name = self._(ctx.HOST_NAME()) is not None
        iif = self._(ctx.IIF()) is not None
        io = self._(ctx.IO()) is not None
        include = self._(ctx.INCLUDE()) is not None
        increment = self._(ctx.INCREMENT()) is not None
        infinite = self._(ctx.INFINITE()) is not None
        init = self._(ctx.INIT()) is not None
        instead = self._(ctx.INSTEAD()) is not None
        isdescendantof = self._(ctx.ISDESCENDANTOF()) is not None
        isnull = self._(ctx.ISNULL()) is not None
        isnumeric = self._(ctx.ISNUMERIC()) is not None
        kerberos = self._(ctx.KERBEROS()) is not None
        key_path = self._(ctx.KEY_PATH()) is not None
        key_store_provider_name = self._(ctx.KEY_STORE_PROVIDER_NAME()) is not None
        language = self._(ctx.LANGUAGE()) is not None
        library = self._(ctx.LIBRARY()) is not None
        lifetime = self._(ctx.LIFETIME()) is not None
        linked = self._(ctx.LINKED()) is not None
        linux = self._(ctx.LINUX()) is not None
        listener_ip = self._(ctx.LISTENER_IP()) is not None
        listener_port = self._(ctx.LISTENER_PORT()) is not None
        local_service_name = self._(ctx.LOCAL_SERVICE_NAME()) is not None
        log = self._(ctx.LOG()) is not None
        mask = self._(ctx.MASK()) is not None
        matched = self._(ctx.MATCHED()) is not None
        master = self._(ctx.MASTER()) is not None
        max_memory = self._(ctx.MAX_MEMORY()) is not None
        maxtransfer = self._(ctx.MAXTRANSFER()) is not None
        maxvalue = self._(ctx.MAXVALUE()) is not None
        max_dispatch_latency = self._(ctx.MAX_DISPATCH_LATENCY()) is not None
        max_duration = self._(ctx.MAX_DURATION()) is not None
        max_event_size = self._(ctx.MAX_EVENT_SIZE()) is not None
        max_size = self._(ctx.MAX_SIZE()) is not None
        max_outstanding_io_per_volume = self._(ctx.MAX_OUTSTANDING_IO_PER_VOLUME()) is not None
        mediadescription = self._(ctx.MEDIADESCRIPTION()) is not None
        medianame = self._(ctx.MEDIANAME()) is not None
        member = self._(ctx.MEMBER()) is not None
        memory_partition_mode = self._(ctx.MEMORY_PARTITION_MODE()) is not None
        message_forwarding = self._(ctx.MESSAGE_FORWARDING()) is not None
        message_forward_size = self._(ctx.MESSAGE_FORWARD_SIZE()) is not None
        minvalue = self._(ctx.MINVALUE()) is not None
        mirror = self._(ctx.MIRROR()) is not None
        must_change = self._(ctx.MUST_CHANGE()) is not None
        newid = self._(ctx.NEWID()) is not None
        newsequentialid = self._(ctx.NEWSEQUENTIALID()) is not None
        noformat = self._(ctx.NOFORMAT()) is not None
        noinit = self._(ctx.NOINIT()) is not None
        none = self._(ctx.NONE()) is not None
        norewind = self._(ctx.NOREWIND()) is not None
        noskip = self._(ctx.NOSKIP()) is not None
        nounload = self._(ctx.NOUNLOAD()) is not None
        no_checksum = self._(ctx.NO_CHECKSUM()) is not None
        no_compression = self._(ctx.NO_COMPRESSION()) is not None
        no_event_loss = self._(ctx.NO_EVENT_LOSS()) is not None
        notification = self._(ctx.NOTIFICATION()) is not None
        ntlm = self._(ctx.NTLM()) is not None
        old_password = self._(ctx.OLD_PASSWORD()) is not None
        on_failure = self._(ctx.ON_FAILURE()) is not None
        operations = self._(ctx.OPERATIONS()) is not None
        page = self._(ctx.PAGE()) is not None
        param_node = self._(ctx.PARAM_NODE()) is not None
        partial = self._(ctx.PARTIAL()) is not None
        password = self._(ctx.PASSWORD()) is not None
        permission_set = self._(ctx.PERMISSION_SET()) is not None
        per_cpu = self._(ctx.PER_CPU()) is not None
        per_db = self._(ctx.PER_DB()) is not None
        per_node = self._(ctx.PER_NODE()) is not None
        persisted = self._(ctx.PERSISTED()) is not None
        platform = self._(ctx.PLATFORM()) is not None
        policy = self._(ctx.POLICY()) is not None
        predicate = self._(ctx.PREDICATE()) is not None
        process = self._(ctx.PROCESS()) is not None
        profile = self._(ctx.PROFILE()) is not None
        python = self._(ctx.PYTHON()) is not None
        r = self._(ctx.R()) is not None
        read_write_filegroups = self._(ctx.READ_WRITE_FILEGROUPS()) is not None
        regenerate = self._(ctx.REGENERATE()) is not None
        related_conversation = self._(ctx.RELATED_CONVERSATION()) is not None
        related_conversation_group = self._(ctx.RELATED_CONVERSATION_GROUP()) is not None
        required = self._(ctx.REQUIRED()) is not None
        reset = self._(ctx.RESET()) is not None
        resources = self._(ctx.RESOURCES()) is not None
        restart = self._(ctx.RESTART()) is not None
        resume = self._(ctx.RESUME()) is not None
        retaindays = self._(ctx.RETAINDAYS()) is not None
        returns = self._(ctx.RETURNS()) is not None
        rewind = self._(ctx.REWIND()) is not None
        role = self._(ctx.ROLE()) is not None
        round_robin = self._(ctx.ROUND_ROBIN()) is not None
        rowcount_big = self._(ctx.ROWCOUNT_BIG()) is not None
        rsa_512 = self._(ctx.RSA_512()) is not None
        rsa_1024 = self._(ctx.RSA_1024()) is not None
        rsa_2048 = self._(ctx.RSA_2048()) is not None
        rsa_3072 = self._(ctx.RSA_3072()) is not None
        rsa_4096 = self._(ctx.RSA_4096()) is not None
        safety = self._(ctx.SAFETY()) is not None
        safe = self._(ctx.SAFE()) is not None
        scheduler = self._(ctx.SCHEDULER()) is not None
        scheme = self._(ctx.SCHEME()) is not None
        script = self._(ctx.SCRIPT()) is not None
        server = self._(ctx.SERVER()) is not None
        service = self._(ctx.SERVICE()) is not None
        service_broker = self._(ctx.SERVICE_BROKER()) is not None
        service_name = self._(ctx.SERVICE_NAME()) is not None
        session = self._(ctx.SESSION()) is not None
        session_context = self._(ctx.SESSION_CONTEXT()) is not None
        settings = self._(ctx.SETTINGS()) is not None
        shrinklog = self._(ctx.SHRINKLOG()) is not None
        sid = self._(ctx.SID()) is not None
        skip_keyword = self._(ctx.SKIP_KEYWORD()) is not None
        softnuma = self._(ctx.SOFTNUMA()) is not None
        source = self._(ctx.SOURCE()) is not None
        specification = self._(ctx.SPECIFICATION()) is not None
        split = self._(ctx.SPLIT()) is not None
        sql = self._(ctx.SQL()) is not None
        sqldumperflags = self._(ctx.SQLDUMPERFLAGS()) is not None
        sqldumperpath = self._(ctx.SQLDUMPERPATH()) is not None
        sqldumpertimeout = self._(ctx.SQLDUMPERTIMEOUT()) is not None
        state = self._(ctx.STATE()) is not None
        stats = self._(ctx.STATS()) is not None
        start = self._(ctx.START()) is not None
        started = self._(ctx.STARTED()) is not None
        startup_state = self._(ctx.STARTUP_STATE()) is not None
        stop = self._(ctx.STOP()) is not None
        stopped = self._(ctx.STOPPED()) is not None
        stop_on_error = self._(ctx.STOP_ON_ERROR()) is not None
        supported = self._(ctx.SUPPORTED()) is not None
        switch_ = self._(ctx.SWITCH()) is not None
        tape = self._(ctx.TAPE()) is not None
        target = self._(ctx.TARGET()) is not None
        tcp = self._(ctx.TCP()) is not None
        tostring = self._(ctx.TOSTRING()) is not None
        trace = self._(ctx.TRACE()) is not None
        track_causality = self._(ctx.TRACK_CAUSALITY()) is not None
        transfer = self._(ctx.TRANSFER()) is not None
        unchecked = self._(ctx.UNCHECKED()) is not None
        unlock = self._(ctx.UNLOCK()) is not None
        unsafe = self._(ctx.UNSAFE()) is not None
        url = self._(ctx.URL()) is not None
        used = self._(ctx.USED()) is not None
        verboselogging = self._(ctx.VERBOSELOGGING()) is not None
        visibility = self._(ctx.VISIBILITY()) is not None
        wait_at_low_priority = self._(ctx.WAIT_AT_LOW_PRIORITY()) is not None
        windows = self._(ctx.WINDOWS()) is not None
        without = self._(ctx.WITHOUT()) is not None
        witness = self._(ctx.WITNESS()) is not None
        xact_abort = self._(ctx.XACT_ABORT()) is not None
        xact_state = self._(ctx.XACT_STATE()) is not None
        abs = self._(ctx.ABS()) is not None
        acos = self._(ctx.ACOS()) is not None
        asin = self._(ctx.ASIN()) is not None
        atan = self._(ctx.ATAN()) is not None
        atn2 = self._(ctx.ATN2()) is not None
        ceiling = self._(ctx.CEILING()) is not None
        cos = self._(ctx.COS()) is not None
        cot = self._(ctx.COT()) is not None
        degrees = self._(ctx.DEGREES()) is not None
        exp = self._(ctx.EXP()) is not None
        floor = self._(ctx.FLOOR()) is not None
        log10 = self._(ctx.LOG10()) is not None
        pi = self._(ctx.PI()) is not None
        power = self._(ctx.POWER()) is not None
        radians = self._(ctx.RADIANS()) is not None
        rand = self._(ctx.RAND()) is not None
        round = self._(ctx.ROUND()) is not None
        sign = self._(ctx.SIGN()) is not None
        sin = self._(ctx.SIN()) is not None
        sqrt = self._(ctx.SQRT()) is not None
        square = self._(ctx.SQUARE()) is not None
        tan = self._(ctx.TAN()) is not None
        current_timezone = self._(ctx.CURRENT_TIMEZONE()) is not None
        current_timezone_id = self._(ctx.CURRENT_TIMEZONE_ID()) is not None
        date_bucket = self._(ctx.DATE_BUCKET()) is not None
        datediff_big = self._(ctx.DATEDIFF_BIG()) is not None
        datefromparts = self._(ctx.DATEFROMPARTS()) is not None
        datetime2fromparts = self._(ctx.DATETIME2FROMPARTS()) is not None
        datetimefromparts = self._(ctx.DATETIMEFROMPARTS()) is not None
        datetimeoffsetfromparts = self._(ctx.DATETIMEOFFSETFROMPARTS()) is not None
        datetrunc = self._(ctx.DATETRUNC()) is not None
        day = self._(ctx.DAY()) is not None
        eomonth = self._(ctx.EOMONTH()) is not None
        isdate = self._(ctx.ISDATE()) is not None
        month = self._(ctx.MONTH()) is not None
        smalldatetimefromparts = self._(ctx.SMALLDATETIMEFROMPARTS()) is not None
        switchoffset = self._(ctx.SWITCHOFFSET()) is not None
        sysdatetime = self._(ctx.SYSDATETIME()) is not None
        sysdatetimeoffset = self._(ctx.SYSDATETIMEOFFSET()) is not None
        sysutcdatetime = self._(ctx.SYSUTCDATETIME()) is not None
        timefromparts = self._(ctx.TIMEFROMPARTS()) is not None
        todatetimeoffset = self._(ctx.TODATETIMEOFFSET()) is not None
        year = self._(ctx.YEAR()) is not None
        quarter = self._(ctx.QUARTER()) is not None
        dayofyear = self._(ctx.DAYOFYEAR()) is not None
        week = self._(ctx.WEEK()) is not None
        hour = self._(ctx.HOUR()) is not None
        minute = self._(ctx.MINUTE()) is not None
        second = self._(ctx.SECOND()) is not None
        millisecond = self._(ctx.MILLISECOND()) is not None
        microsecond = self._(ctx.MICROSECOND()) is not None
        nanosecond = self._(ctx.NANOSECOND()) is not None
        tzoffset = self._(ctx.TZOFFSET()) is not None
        iso_week = self._(ctx.ISO_WEEK()) is not None
        weekday = self._(ctx.WEEKDAY()) is not None
        year_abbr = self._(ctx.YEAR_ABBR())
        quarter_abbr = self._(ctx.QUARTER_ABBR())
        month_abbr = self._(ctx.MONTH_ABBR())
        dayofyear_abbr = self._(ctx.DAYOFYEAR_ABBR())
        day_abbr = self._(ctx.DAY_ABBR())
        week_abbr = self._(ctx.WEEK_ABBR())
        hour_abbr = self._(ctx.HOUR_ABBR()) is not None
        minute_abbr = self._(ctx.MINUTE_ABBR())
        second_abbr = self._(ctx.SECOND_ABBR())
        millisecond_abbr = self._(ctx.MILLISECOND_ABBR()) is not None
        microsecond_abbr = self._(ctx.MICROSECOND_ABBR()) is not None
        nanosecond_abbr = self._(ctx.NANOSECOND_ABBR()) is not None
        tzoffset_abbr = self._(ctx.TZOFFSET_ABBR()) is not None
        iso_week_abbr = self._(ctx.ISO_WEEK_ABBR())
        weekday_abbr = self._(ctx.WEEKDAY_ABBR()) is not None
        sp_executesql = self._(ctx.SP_EXECUTESQL()) is not None
        varchar = self._(ctx.VARCHAR()) is not None
        nvarchar = self._(ctx.NVARCHAR()) is not None
        precision = self._(ctx.PRECISION()) is not None
        filestream_on = self._(ctx.FILESTREAM_ON()) is not None
        return Keyword(abort, absolute, accent_sensitivity, access, action, activation, active, add, address, aes_128, aes_192, aes_256, affinity, after, aggregate, algorithm, all_constraints, all_errormsgs, all_indexes, all_levels, allow_encrypted_value_modifications, allow_page_locks, allow_row_locks, allow_snapshot_isolation, allowed, always, ansi_defaults, ansi_null_default, ansi_null_dflt_off, ansi_null_dflt_on, ansi_nulls, ansi_padding, ansi_warnings, app_name, application_log, applock_mode, applock_test, apply, arithabort, arithignore, ascii, assembly, assemblyproperty, at_keyword, audit, audit_guid, auto, auto_cleanup, auto_close, auto_create_statistics, auto_drop, auto_shrink, auto_update_statistics, auto_update_statistics_async, autogrow_all_files, autogrow_single_file, availability, avg, backup_clonedb, backup_priority, base64, begin_dialog, bigint, binary_keyword, binary_checksum, binding, blob_storage, broker, broker_instance, bulk_logged, caller, cap_cpu_percent, cast, try_cast, catalog, catch, cert_id, certencoded, certprivatekey, change, change_retention, change_tracking, char, charindex, checkalloc, checkcatalog, checkconstraints, checkdb, checkfilegroup, checksum, checksum_agg, checktable, cleantable, cleanup, clonedatabase, col_length, col_name, collection, column_encryption_key, column_master_key, columnproperty, columns, columnstore, columnstore_archive, committed, compatibility_level, compress_all_row_groups, compression_delay, concat, concat_ws, concat_null_yields_null, content, control, cookie, count, count_big, counter, cpu, create_new, creation_disposition, credential, cryptographic, cume_dist, cursor_close_on_commit, cursor_default, cursor_status, data, data_purity, database_principal_id, databasepropertyex, datalength, date_correlation_optimization, dateadd, datediff, datename, datepart, days, db_chaining, db_failover, db_id, db_name, dbcc, dbreindex, decryption, default_double_quote, default_fulltext_language, default_language, definition, delay, delayed_durability, deleted, dense_rank, dependents, des, description, desx, deterministic, dhcp, dialog, difference, directory_name, disable, disable_broker, disabled, document, drop_existing, dropcleanbuffers, dynamic, elements, emergency, empty, enable, enable_broker, encrypted, encrypted_value, encryption, encryption_type, endpoint_url, error_broker_conversations, estimateonly, exclusive, executable, exist, exist_square_bracket, expand, expiry_date, explicit, extended_logical_checks, fail_operation, failover_mode, failure, failure_condition_level, fast, fast_forward, file_id, file_idex, file_name, filegroup, filegroup_id, filegroup_name, filegroupproperty, filegrowth, filename, filepath, fileproperty, filepropertyex, filestream, filter, first, first_value, fmtonly, following, force, force_failover_allow_data_loss, forced, forceplan, forcescan, format, forward_only, free, fullscan, fulltext, fulltextcatalogproperty, fulltextserviceproperty, gb, generated, getdate, getutcdate, global_, go_, greatest, group_max_requests, grouping, grouping_id, hadr, has_dbaccess, has_perms_by_name, hash, health_check_timeout, hidden_keyword, high, honor_broker_priority, hours, ident_current, ident_incr, ident_seed, identity_value, ignore_constraints, ignore_dup_key, ignore_nonclustered_columnstore_index, ignore_replicated_table_cache, ignore_triggers, immediate, impersonate, implicit_transactions, importance, include_null_values, incremental, index_col, indexkey_property, indexproperty, initiator, input, insensitive, inserted, int, ip, is_member, is_rolemember, is_srvrolemember, isjson, isolation, job, json, json_object, json_array, json_value, json_query, json_modify, json_path_exists, kb, keep, keepdefaults, keepfixed, keepidentity, key_source, keys, keyset, lag, last, last_value, lead, least, len_, level, list, listener, listener_url, lob_compaction, local, location, lock, lock_escalation, login, loginproperty, loop, low, lower, ltrim, manual, mark, masked, materialized, max, max_cpu_percent, max_dop, max_files, max_iops_per_volume, max_memory_percent, max_processes, max_queue_readers, max_rollover_files, maxdop, maxrecursion, maxsize, mb, medium, memory_optimized_data, message, min, min_active_rowversion, min_cpu_percent, min_iops_per_volume, min_memory_percent, minutes, mirror_address, mixed_page_allocation, mode, modify, modify_square_bracket, move, multi_user, name, nchar, nested_triggers, new_account, new_broker, new_password, newname, next, no, no_infomsgs, no_querystore, no_statistics, no_truncate, no_wait, nocount, nodes, noexec, noexpand, noindex, nolock, non_transacted_access, norecompute, norecovery, notifications, nowait, ntile, null_double_quote, numanode, number, numeric_roundabort, object, object_definition, object_id, object_name, object_schema_name, objectproperty, objectpropertyex, offline, offset, old_account, online, only, open_existing, openjson, optimistic, optimize, optimize_for_sequential_key, original_db_name, original_login, out, output, override, owner, ownership, pad_index, page_verify, pagecount, paglock, parameterization, parsename, parseonly, partition, partitions, partner, path, patindex, pause, pdw_showspaceused, percent_rank, percentile_cont, percentile_disc, permissions, persist_sample_percent, physical_only, poison_message_handling, pool, port, preceding, primary_role, prior, priority, priority_level, private, private_key, privileges, proccache, procedure_name, property, provider, provider_key_name, pwdcompare, pwdencrypt, query, query_square_bracket, queue, queue_delay, quoted_identifier, quotename, randomized, range_, rank, rc2, rc4, rc4_128, read_committed_snapshot, read_only, read_only_routing_list, read_write, readcommitted, readcommittedlock, readonly, readpast, readuncommitted, readwrite, rebuild, receive, recompile, recovery, recursive_triggers, relative, remote, remote_proc_transactions, remote_service_name, remove, reorganize, repair_allow_data_loss, repair_fast, repair_rebuild, repeatable, repeatableread, replace, replica, replicate, request_max_cpu_time_sec, request_max_memory_grant_percent, request_memory_grant_timeout_sec, required_synchronized_secondaries_to_commit, resample, reserve_disk_space, resource, resource_manager_location, restricted_user, resumable, retention, reverse, robust, root, route, row, row_number, rowguid, rowlock, rows, rtrim, sample, schema_id, schema_name, schemabinding, scope_identity, scoped, scroll, scroll_locks, search, secondary, secondary_only, secondary_role, seconds, secret, securables, security, security_log, seeding_mode, self, semi_sensitive, send, sent, sequence, sequence_number, serializable, serverproperty, servicebroker, sessionproperty, session_timeout, seterror, share, shared, showcontig, showplan, showplan_all, showplan_text, showplan_xml, signature, simple, single_user, size, smallint, snapshot, sort_in_tempdb, soundex, space_keyword, sparse, spatial_window_max_cells, sql_variant_property, standby, start_date, static, statistics_incremental, statistics_norecompute, stats_date, stats_stream, status, statusonly, stdev, stdevp, stoplist, str, string_agg, string_escape, stuff, subject, subscribe, subscription, substring, sum, suser_id, suser_name, suser_sid, suser_sname, suspend, symmetric, synchronous_commit, synonym, system, tableresults, tablock, tablockx, take, target_recovery_time, tb, textimage_on, throw, ties, time, timeout, timer, tinyint, torn_page_detection, tracking, transaction_id, transform_noise_words, translate, trim, triple_des, triple_des_3key, trustworthy, try_, tsql, two_digit_year_cutoff, type_, type_id, type_name, type_warning, typeproperty, unbounded, uncommitted, unicode, unknown, unlimited, unmask, uow, updlock, upper, user_id, user_name, using, valid_xml, validation, value, value_square_bracket, var_, varbinary_keyword, varp, verify_clonedb, version, view_metadata, views, wait, well_formed_xml, without_array_wrapper, work, workload, xlock, xml, xml_compression, xmldata, xmlnamespaces, xmlschema, xsinil, zone, abort_after_wait, absent, administer, aes, allow_connections, allow_multiple_event_loss, allow_single_event_loss, anonymous, append_, application, asymmetric, asynchronous_commit, authenticate, authentication, automated_backup_preference, automatic, availability_mode, before, block, blockers, blocksize, blocking_hierarchy, buffer, buffercount, cache, called, certificate, changetable, changes, check_policy, check_expiration, classifier_function, cluster, compress, compression, connect, connection, configuration, connectionproperty, containment, context, context_info, continue_after_error, contract, contract_name, conversation, copy_only, current_request_id, current_transaction_id, cycle, data_compression, data_source, database_mirroring, dataspace, ddl, decompress, default_database, default_schema, diagnostics, differential, distribution, dtc_support, enabled, endpoint, error, error_line, error_message, error_number, error_procedure, error_severity, error_state, event, eventdata, event_retention_mode, executable_file, expiredate, extension, external_access, failover, failureconditionlevel, fan_in, file_snapshot, forceseek, force_service_allow_data_loss, formatmessage, get, get_filestream_transaction_context, getancestor, getansinull, getdescendant, getlevel, getreparentedvalue, getroot, governor, hashed, healthchecktimeout, heap, hierarchyid, host_id, host_name, iif, io, include, increment, infinite, init, instead, isdescendantof, isnull, isnumeric, kerberos, key_path, key_store_provider_name, language, library, lifetime, linked, linux, listener_ip, listener_port, local_service_name, log, mask, matched, master, max_memory, maxtransfer, maxvalue, max_dispatch_latency, max_duration, max_event_size, max_size, max_outstanding_io_per_volume, mediadescription, medianame, member, memory_partition_mode, message_forwarding, message_forward_size, minvalue, mirror, must_change, newid, newsequentialid, noformat, noinit, none, norewind, noskip, nounload, no_checksum, no_compression, no_event_loss, notification, ntlm, old_password, on_failure, operations, page, param_node, partial, password, permission_set, per_cpu, per_db, per_node, persisted, platform, policy, predicate, process, profile, python, r, read_write_filegroups, regenerate, related_conversation, related_conversation_group, required, reset, resources, restart, resume, retaindays, returns, rewind, role, round_robin, rowcount_big, rsa_512, rsa_1024, rsa_2048, rsa_3072, rsa_4096, safety, safe, scheduler, scheme, script, server, service, service_broker, service_name, session, session_context, settings, shrinklog, sid, skip_keyword, softnuma, source, specification, split, sql, sqldumperflags, sqldumperpath, sqldumpertimeout, state, stats, start, started, startup_state, stop, stopped, stop_on_error, supported, switch_, tape, target, tcp, tostring, trace, track_causality, transfer, unchecked, unlock, unsafe, url, used, verboselogging, visibility, wait_at_low_priority, windows, without, witness, xact_abort, xact_state, abs, acos, asin, atan, atn2, ceiling, cos, cot, degrees, exp, floor, log10, pi, power, radians, rand, round, sign, sin, sqrt, square, tan, current_timezone, current_timezone_id, date_bucket, datediff_big, datefromparts, datetime2fromparts, datetimefromparts, datetimeoffsetfromparts, datetrunc, day, eomonth, isdate, month, smalldatetimefromparts, switchoffset, sysdatetime, sysdatetimeoffset, sysutcdatetime, timefromparts, todatetimeoffset, year, quarter, dayofyear, week, hour, minute, second, millisecond, microsecond, nanosecond, tzoffset, iso_week, weekday, year_abbr, quarter_abbr, month_abbr, dayofyear_abbr, day_abbr, week_abbr, hour_abbr, minute_abbr, second_abbr, millisecond_abbr, microsecond_abbr, nanosecond_abbr, tzoffset_abbr, iso_week_abbr, weekday_abbr, sp_executesql, varchar, nvarchar, precision, filestream_on)

    def visitId_(self, ctx: tsql.Id_Context):
        id = self._(ctx.ID())
        temp_id = self._(ctx.TEMP_ID())
        double_quote_id = self._(ctx.DOUBLE_QUOTE_ID())
        double_quote_blank = self._(ctx.DOUBLE_QUOTE_BLANK()) is not None
        square_bracket_id = self._(ctx.SQUARE_BRACKET_ID())
        keyword = self._(ctx.keyword())
        raw = self._(ctx.RAW()) is not None
        return Id(id, temp_id, double_quote_id, double_quote_blank, square_bracket_id, keyword, raw)

    def visitSimple_id(self, ctx: tsql.Simple_idContext):
        id = self._(ctx.ID())
        return SimpleId(id)

    def visitId_or_string(self, ctx: tsql.Id_or_stringContext):
        id = self._(ctx.id_())
        string = self._(ctx.STRING())
        return IdOrString(id, string)

    def visitFile_size(self, ctx: tsql.File_sizeContext):
        kb = self._(ctx.KB()) is not None
        mb = self._(ctx.MB()) is not None
        gb = self._(ctx.GB()) is not None
        tb = self._(ctx.TB()) is not None
        return FileSize(kb, mb, gb, tb)

    def visitRaiseerror_statement_msg(self, ctx: tsql.Raiseerror_statementContext):
        decimal = self._(ctx.DECIMAL()) is not None
        string = self._(ctx.STRING())
        local_id = self._(ctx.LOCAL_ID())
        return RaiseerrorStatementMsg(decimal, string, local_id)

    def visitRaiseerror_statement_formatstring(self, ctx: tsql.Raiseerror_statementContext):
        string = self._(ctx.STRING())
        local_id = self._(ctx.LOCAL_ID())
        double_quote_id = self._(ctx.DOUBLE_QUOTE_ID())
        return RaiseerrorStatementFormatstring(string, local_id, double_quote_id)

    def visitRaiseerror_statement_argument(self, ctx: tsql.Raiseerror_statementContext):
        decimal = self._(ctx.DECIMAL()) is not None
        string = self._(ctx.STRING())
        local_id = self._(ctx.LOCAL_ID())
        return RaiseerrorStatementArgument(decimal, string, local_id)

    def visitCreate_endpoint_state(self, ctx: tsql.Create_endpointContext):
        started = self._(ctx.STARTED()) is not None
        stopped = self._(ctx.STOPPED()) is not None
        disabled = self._(ctx.DISABLED()) is not None
        return CreateEndpointState(started, stopped, disabled)

    def visitAlter_server_audit_max_rollover_files(self, ctx: tsql.Alter_server_auditContext):
        decimal = self._(ctx.DECIMAL()) is not None
        unlimited = self._(ctx.UNLIMITED()) is not None
        return AlterServerAuditMaxRolloverFiles(decimal, unlimited)

    def visitCreate_server_audit_max_rollover_files(self, ctx: tsql.Create_server_auditContext):
        decimal = self._(ctx.DECIMAL()) is not None
        unlimited = self._(ctx.UNLIMITED()) is not None
        return CreateServerAuditMaxRolloverFiles(decimal, unlimited)

    def visitCreate_or_alter_procedure_proc(self, ctx: tsql.Create_or_alter_procedureContext):
        proc = self._(ctx.PROC()) is not None
        procedure = self._(ctx.PROCEDURE()) is not None
        return CreateOrAlterProcedureProc(proc, procedure)

    def visitLow_priority_lock_wait_abort_after_wait(self, ctx: tsql.Low_priority_lock_waitContext):
        none = self._(ctx.NONE()) is not None
        self = self._(ctx.SELF()) is not None
        blockers = self._(ctx.BLOCKERS()) is not None
        return LowPriorityLockWaitAbortAfterWait(none, self, blockers)

    def visitAlter_endpoint_state(self, ctx: tsql.Alter_endpointContext):
        started = self._(ctx.STARTED()) is not None
        stopped = self._(ctx.STOPPED()) is not None
        disabled = self._(ctx.DISABLED()) is not None
        return AlterEndpointState(started, stopped, disabled)

    def visitSnapshot_option_MEMORY_OPTIMIZED_ELEVATE_TO_SNAPSHOT(self, ctx: tsql.Snapshot_optionContext):
        on = self._(ctx.ON()) is not None
        off = self._(ctx.OFF()) is not None
        return SnapshotOptionMemoryOptimizedElevateToSnapshot(on, off)

    def visitDrop_procedure_proc(self, ctx: tsql.Drop_procedureContext):
        proc = self._(ctx.PROC()) is not None
        procedure = self._(ctx.PROCEDURE()) is not None
        return DropProcedureProc(proc, procedure)

    def visitKill_process_session_id(self, ctx: tsql.Kill_processContext):
        decimal = self._(ctx.DECIMAL()) is not None
        string = self._(ctx.STRING())
        return KillProcessSessionId(decimal, string)

    def visitExecute_clause_clause(self, ctx: tsql.Execute_clauseContext):
        caller = self._(ctx.CALLER()) is not None
        self = self._(ctx.SELF()) is not None
        owner = self._(ctx.OWNER()) is not None
        string = self._(ctx.STRING())
        return ExecuteClauseClause(caller, self, owner, string)

    def visitTop_percent_percent_constant(self, ctx: tsql.Top_percentContext):
        real = self._(ctx.REAL())
        float = self._(ctx.FLOAT()) is not None
        decimal = self._(ctx.DECIMAL()) is not None
        return TopPercentPercentConstant(real, float, decimal)

    def visitSelect_order_by_clause_offset_rows(self, ctx: tsql.Select_order_by_clauseContext):
        row = self._(ctx.ROW()) is not None
        rows = self._(ctx.ROWS()) is not None
        return SelectOrderByClauseOffsetRows(row, rows)

    def visitSelect_order_by_clause_fetch_offset(self, ctx: tsql.Select_order_by_clauseContext):
        first = self._(ctx.FIRST()) is not None
        next = self._(ctx.NEXT()) is not None
        return SelectOrderByClauseFetchOffset(first, next)

    def visitSelect_order_by_clause_fetch_rows(self, ctx: tsql.Select_order_by_clauseContext):
        row = self._(ctx.ROW()) is not None
        rows = self._(ctx.ROWS()) is not None
        return SelectOrderByClauseFetchRows(row, rows)

    def visitChange_table_changes_changesid(self, ctx: tsql.Change_table_changesContext):
        null = self._(ctx.NULL_()) is not None
        decimal = self._(ctx.DECIMAL()) is not None
        local_id = self._(ctx.LOCAL_ID())
        return ChangeTableChangesChangesid(null, decimal, local_id)

    def visitJoin_on_join_type(self, ctx: tsql.Join_onContext):
        left = self._(ctx.LEFT()) is not None
        right = self._(ctx.RIGHT()) is not None
        full = self._(ctx.FULL()) is not None
        return JoinOnJoinType(left, right, full)

    def visitJoin_on_join_hint(self, ctx: tsql.Join_onContext):
        loop = self._(ctx.LOOP()) is not None
        hash = self._(ctx.HASH()) is not None
        merge = self._(ctx.MERGE()) is not None
        remote = self._(ctx.REMOTE()) is not None
        return JoinOnJoinHint(loop, hash, merge, remote)

    def visitApply__apply_style(self, ctx: tsql.Apply_Context):
        cross = self._(ctx.CROSS()) is not None
        outer = self._(ctx.OUTER()) is not None
        return ApplyApplyStyle(cross, outer)

    def visitBulk_option_bulk_option_value(self, ctx: tsql.Bulk_optionContext):
        decimal = self._(ctx.DECIMAL()) is not None
        string = self._(ctx.STRING())
        return BulkOptionBulkOptionValue(decimal, string)

    def visitAggregate_windowed_function_agg_func(self, ctx: tsql.Aggregate_windowed_functionContext):
        avg = self._(ctx.AVG()) is not None
        max = self._(ctx.MAX()) is not None
        min = self._(ctx.MIN()) is not None
        sum = self._(ctx.SUM()) is not None
        stdev = self._(ctx.STDEV()) is not None
        stdevp = self._(ctx.STDEVP()) is not None
        var_ = self._(ctx.VAR()) is not None
        varp = self._(ctx.VARP()) is not None
        return AggregateWindowedFunctionAggFunc(avg, max, min, sum, stdev, stdevp, var_, varp)

    def visitAggregate_windowed_function_cnt(self, ctx: tsql.Aggregate_windowed_functionContext):
        count = self._(ctx.COUNT()) is not None
        count_big = self._(ctx.COUNT_BIG()) is not None
        return AggregateWindowedFunctionCnt(count, count_big)

    def visitEnd_conversation_faliure_code(self, ctx: tsql.End_conversationContext):
        local_id = self._(ctx.LOCAL_ID())
        string = self._(ctx.STRING())
        return EndConversationFaliureCode(local_id, string)

    def visitEnd_conversation_failure_text(self, ctx: tsql.End_conversationContext):
        local_id = self._(ctx.LOCAL_ID())
        string = self._(ctx.STRING())
        return EndConversationFailureText(local_id, string)

    def visitGet_conversation_conversation_group_id(self, ctx: tsql.Get_conversationContext):
        string = self._(ctx.STRING())
        local_id = self._(ctx.LOCAL_ID())
        return GetConversationConversationGroupId(string, local_id)

    def visitSend_conversation_conversation_handle(self, ctx: tsql.Send_conversationContext):
        string = self._(ctx.STRING())
        local_id = self._(ctx.LOCAL_ID())
        return SendConversationConversationHandle(string, local_id)

    def visitSend_conversation_message_body_expression(self, ctx: tsql.Send_conversationContext):
        string = self._(ctx.STRING())
        local_id = self._(ctx.LOCAL_ID())
        return SendConversationMessageBodyExpression(string, local_id)

    def visitData_type_scaled(self, ctx: tsql.Data_typeContext):
        varchar = self._(ctx.VARCHAR()) is not None
        nvarchar = self._(ctx.NVARCHAR()) is not None
        binary_keyword = self._(ctx.BINARY_KEYWORD()) is not None
        varbinary_keyword = self._(ctx.VARBINARY_KEYWORD()) is not None
        square_bracket_id = self._(ctx.SQUARE_BRACKET_ID())
        return DataTypeScaled(varchar, nvarchar, binary_keyword, varbinary_keyword, square_bracket_id)
