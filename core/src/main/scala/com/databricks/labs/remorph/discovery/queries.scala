package com.databricks.labs.remorph.discovery

import com.databricks.labs.remorph.parsers.intermediate.StructField

import java.sql.Timestamp
import java.time.Duration

case class ExecutedQuery(timestamp: Timestamp, source: String, duration: Duration, user: String)

case class QueryHistory(queries: Seq[ExecutedQuery])

case class UnparsedQuery(timestamp: Timestamp, source: String)

case class TableDefinition(
    catalog: String,
    schema: String,
    table: String,
    location: Option[String] = None,
    tableFormat: Option[String] = None,
    viewText: Option[String] = None,
    columns: Seq[StructField] = Seq.empty,
    sizeGb: Int = 0)

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
