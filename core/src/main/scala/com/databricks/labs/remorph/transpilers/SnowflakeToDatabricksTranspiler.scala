package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.parsers.snowflake.SnowflakePlanParser

class SnowflakeToDatabricksTranspiler extends BaseTranspiler {
  override val planParser = new SnowflakePlanParser
}
