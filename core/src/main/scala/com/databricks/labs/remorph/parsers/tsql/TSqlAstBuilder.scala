package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.tsql.TSqlParser._
import com.databricks.labs.remorph.parsers.{intermediate => ir}

import scala.collection.JavaConverters._
class TSqlAstBuilder extends TSqlParserBaseVisitor[ir.TreeNode]{
// noop
}
