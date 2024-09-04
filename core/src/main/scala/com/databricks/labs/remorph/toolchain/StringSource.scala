package com.databricks.labs.remorph.toolchain

class StringSource(source: String, filename: String) extends Source {
  private var processed = false

  override def hasNext: Boolean = !processed

  override def next(): SourceCode = {
    if (processed) throw new NoSuchElementException("No more source entities")
    processed = true
    SourceCode(source, filename)
  }
}
