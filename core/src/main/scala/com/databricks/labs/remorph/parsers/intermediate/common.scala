package com.databricks.labs.remorph.parsers.intermediate

case class StorageLevel(
    use_disk: Boolean,
    use_memory: Boolean,
    use_off_heap: Boolean,
    deserialized: Boolean,
    replication: Int)

case class ResourceInformation(name: String, addresses: Seq[String])

case class FunctionIdentifier(catalog: Option[String], schema: Option[String], funcName: String)
