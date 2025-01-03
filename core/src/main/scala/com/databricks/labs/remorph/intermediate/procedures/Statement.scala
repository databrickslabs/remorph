package com.databricks.labs.remorph.intermediate.procedures

import com.databricks.labs.remorph.intermediate.{Command, LogicalPlan}

abstract class Statement extends LogicalPlan with Command
