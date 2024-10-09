package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.intermediate.RemorphError

case class TranspileException(err: RemorphError) extends RuntimeException(err.msg)
