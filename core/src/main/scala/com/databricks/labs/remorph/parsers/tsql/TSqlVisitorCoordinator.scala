package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.VisitorCoordinator

class TSqlVisitorCoordinator extends VisitorCoordinator {

  val astBuilder = new TSqlAstBuilder(this)
  val relationBuilder = new TSqlRelationBuilder(this)
  val expressionBuilder = new TSqlExpressionBuilder(this)
  val dmlBuilder = new TSqlDMLBuilder(this)
  val ddlBuilder = new TSqlDDLBuilder(this)
  val functionBuilder = new TSqlFunctionBuilder

  // TSQL extension
  val optionBuilder = new OptionBuilder(this)
}
