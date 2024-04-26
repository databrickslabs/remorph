package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.databricks.labs.remorph.parsers.tsql.TSqlParser._

class TSqlRelationBuilder extends TSqlParserBaseVisitor[ir.Relation] {

  override def visitTable_source_item(ctx: Table_source_itemContext): ir.Relation = {
    val table = ctx.full_table_name().getText
    // [TODO]: Handle Table Alias ctx.table_alias().getText
    ir.NamedTable(table, Map.empty, is_streaming = false)
  }

}
