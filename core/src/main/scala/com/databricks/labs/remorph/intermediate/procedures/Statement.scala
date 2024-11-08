package com.databricks.labs.remorph.intermediate.procedures

import com.databricks.labs.remorph.intermediate.{Command, LogicalPlan, Origin}

abstract class Statement extends LogicalPlan(origin = Origin.empty) with Command
