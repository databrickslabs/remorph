package com.databricks.labs.remorph.transpilers

case class TranspileException(msg: String) extends RuntimeException(msg)
