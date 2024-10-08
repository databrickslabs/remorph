package com.databricks.labs.remorph.discovery

import com.databricks.labs.remorph.parsers.intermediate.ColumnDetail

import java.sql.Timestamp
import java.time.Duration

case class ExecutedQuery(id: String, timestamp: Timestamp, source: String, duration: Duration, user: String)

case class QueryHistory(queries: Seq[ExecutedQuery])

case class UnparsedQuery(timestamp: Timestamp, source: String)

case class TableDefinition(
    catalog: String,
    schema: String,
    table: String,
    location: Option[String] = None,
    tableFormat: Option[String] = None,
    viewText: Option[String] = None,
    columns: Seq[ColumnDetail] = Seq.empty,
    sizeGb: Int = 0,
    comments: Option[String] = None)

case class Grant(objectType: String, objectKey: String, principal: String, action: String)

case class ComputeCapacity(
    startTs: Timestamp,
    endTs: Timestamp,
    name: String,
    availableCPUs: Int,
    availableMemoryGb: Int,
    usedCPUs: Int,
    usedMemoryGb: Int,
    listPrice: Double)
