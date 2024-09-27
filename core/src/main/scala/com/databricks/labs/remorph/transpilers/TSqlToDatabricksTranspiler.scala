package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.parsers.tsql.TSqlPlanParser

class TSqlToDatabricksTranspiler extends BaseTranspiler {
  override val planParser = new TSqlPlanParser
}
