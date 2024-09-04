package com.databricks.labs.remorph.toolchain

  trait Source extends Iterator[SourceCode]

  case class SourceCode(source: String, filename: String = "-- test source --")
