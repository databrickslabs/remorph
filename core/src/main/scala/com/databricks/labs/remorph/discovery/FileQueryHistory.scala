package com.databricks.labs.remorph.discovery

class FileQueryHistory extends QueryHistoryProvider {

  override def history(): QueryHistory = {
    val queries = Seq.empty[ExecutedQuery]
    QueryHistory(queries)
  }

}
