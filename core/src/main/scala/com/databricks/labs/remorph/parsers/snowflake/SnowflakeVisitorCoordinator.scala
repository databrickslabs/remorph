package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.VisitorCoordinator
import org.antlr.v4.runtime.Vocabulary

class SnowflakeVisitorCoordinator(parserVocab: Vocabulary, ruleNames: Array[String])
    extends VisitorCoordinator(parserVocab, ruleNames) {

  val astBuilder = new SnowflakeAstBuilder(this)
  val relationBuilder = new SnowflakeRelationBuilder(this)
  val expressionBuilder = new SnowflakeExpressionBuilder(this)
  val dmlBuilder = new SnowflakeDMLBuilder(this)
  val ddlBuilder = new SnowflakeDDLBuilder(this)
  val functionBuilder = new SnowflakeFunctionBuilder

  // Snowflake extensions
  val commandBuilder = new SnowflakeCommandBuilder(this)
  val typeBuilder = new SnowflakeTypeBuilder
}
