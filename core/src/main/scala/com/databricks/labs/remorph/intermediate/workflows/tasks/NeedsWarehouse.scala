package com.databricks.labs.remorph.intermediate.workflows.tasks

trait NeedsWarehouse {
  final val DEFAULT_WAREHOUSE_ID = sys.env.getOrElse("DATABRICKS_WAREHOUSE_ID", "__DEFAULT_WAREHOUSE_ID__")
}
