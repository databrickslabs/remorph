package com.databricks.labs.remorph.parsers.tsql

class TSqlVisitorCoordinator {

  val relationBuilder: TSqlRelationBuilder = new TSqlRelationBuilder(this)
  val expressionBuilder = new TSqlExpressionBuilder(this)
  val dmlBuilder = new TSqlDMLBuilder(this)
  val optionBuilder = new OptionBuilder(this)
  val ddlBuilder = new TSqlDDLBuilder(this)
  val dataTypeBuilder: DataTypeBuilder = new DataTypeBuilder
  val functionBuilder = new TSqlFunctionBuilder
  val astBuilder = new TSqlAstBuilder(this)
}
