package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.VisitorCoordinator
import org.antlr.v4.runtime.Vocabulary

class TSqlVisitorCoordinator(lexerVocab: Vocabulary, parserVocab: Vocabulary)
    extends VisitorCoordinator(lexerVocab, parserVocab) {

  val astBuilder = new TSqlAstBuilder(this)
  val relationBuilder = new TSqlRelationBuilder(this)
  val expressionBuilder = new TSqlExpressionBuilder(this)
  val dmlBuilder = new TSqlDMLBuilder(this)
  val ddlBuilder = new TSqlDDLBuilder(this)
  val functionBuilder = new TSqlFunctionBuilder

  // TSQL extension
  val optionBuilder = new OptionBuilder(this)
}
