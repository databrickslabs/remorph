package com.databricks.labs.remorph.parsers.intermediate

// Catalog API (experimental / unstable)
abstract class Catalog extends RelationCommon
case class CurrentDatabase() extends Catalog {}
case class SetCurrentDatabase(db_name: String) extends Catalog {}
case class ListDatabases(pattern: Option[String]) extends Catalog {}
case class ListTables(db_name: Option[String], pattern: Option[String]) extends Catalog {}
case class ListFunctions(db_name: Option[String], pattern: Option[String]) extends Catalog {}
case class ListColumns(table_name: String, db_name: Option[String]) extends Catalog {}
case class GetDatabase(db_name: String) extends Catalog {}
case class GetTable(table_name: String, db_name: Option[String]) extends Catalog {}
case class GetFunction(function_name: String, db_name: Option[String]) extends Catalog {}
case class DatabaseExists(db_name: String) extends Catalog {}
case class TableExists(table_name: String, db_name: Option[String]) extends Catalog {}
case class FunctionExists(function_name: String, db_name: Option[String]) extends Catalog {}
case class CreateExternalTable(
    table_name: String,
    path: Option[String],
    source: Option[String],
    schema: Option[DataType],
    options: Map[String, String])
    extends Catalog {}
case class CreateTable(
    table_name: String,
    path: Option[String],
    source: Option[String],
    description: Option[String],
    schema: Option[DataType],
    options: Map[String, String])
    extends Catalog {}
case class DropTempView(view_name: String) extends Catalog {}
case class DropGlobalTempView(view_name: String) extends Catalog {}
case class RecoverPartitions(table_name: String) extends Catalog {}
case class IsCached(table_name: String) extends Catalog {}
case class CacheTable(table_name: String, storage_level: StorageLevel) extends Catalog {}
case class UncacheTable(table_name: String) extends Catalog {}
case class ClearCache() extends Catalog {}
case class RefreshTable(table_name: String) extends Catalog {}
case class RefreshByPath(path: String) extends Catalog {}
case class CurrentCatalog() extends Catalog {}
case class SetCurrentCatalog(catalog_name: String) extends Catalog {}
case class ListCatalogs(pattern: Option[String]) extends Catalog {}
