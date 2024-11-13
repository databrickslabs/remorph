package com.databricks.labs.remorph.intermediate

trait Command extends LogicalPlan {
  def output: Seq[Attribute] = Seq.empty
}

case class SqlCommand(sql: String, named_arguments: Map[String, Expression], pos_arguments: Seq[Expression])
    extends LeafNode
    with Command

case class CreateDataFrameViewCommand(child: Relation, name: String, is_global: Boolean, replace: Boolean)
    extends LeafNode
    with Command

abstract class TableSaveMethod
case object UnspecifiedSaveMethod extends TableSaveMethod
case object SaveAsTableSaveMethod extends TableSaveMethod
case object InsertIntoSaveMethod extends TableSaveMethod

abstract class SaveMode
case object UnspecifiedSaveMode extends SaveMode
case object AppendSaveMode extends SaveMode
case object OverwriteSaveMode extends SaveMode
case object ErrorIfExistsSaveMode extends SaveMode
case object IgnoreSaveMode extends SaveMode

case class SaveTable(table_name: String, save_method: TableSaveMethod) extends LeafNode with Command

case class BucketBy(bucket_column_names: Seq[String], num_buckets: Int)

case class WriteOperation(
    child: Relation,
    source: Option[String],
    path: Option[String],
    table: Option[SaveTable],
    mode: SaveMode,
    sort_column_names: Seq[String],
    partitioning_columns: Seq[String],
    bucket_by: Option[BucketBy],
    options: Map[String, String],
    clustering_columns: Seq[String])
    extends LeafNode
    with Command

abstract class Mode
case object UnspecifiedMode extends Mode
case object CreateMode extends Mode
case object OverwriteMode extends Mode
case object OverwritePartitionsMode extends Mode
case object AppendMode extends Mode
case object ReplaceMode extends Mode
case object CreateOrReplaceMode extends Mode

case class WriteOperationV2(
    child: Relation,
    table_name: String,
    provider: Option[String],
    partitioning_columns: Seq[Expression],
    options: Map[String, String],
    table_properties: Map[String, String],
    mode: Mode,
    overwrite_condition: Option[Expression],
    clustering_columns: Seq[String])
    extends LeafNode
    with Command

case class Trigger(
    processing_time_interval: Option[String],
    available_now: Boolean = false,
    once: Boolean = false,
    continuous_checkpoint_interval: Option[String])

case class SinkDestination(path: Option[String], table_name: Option[String])

case class StreamingForeachFunction(python_udf: Option[PythonUDF], scala_function: Option[ScalarScalaUDF])

case class WriteStreamOperationStart(
    child: Relation,
    format: String,
    options: Map[String, String],
    partitioning_column_names: Seq[String],
    trigger: Trigger,
    output_mode: String,
    query_name: String,
    sink_destination: SinkDestination,
    foreach_writer: Option[StreamingForeachFunction],
    foreach_batch: Option[StreamingForeachFunction])
    extends LeafNode
    with Command

// TODO: align snowflake and common IR implementations for `CreateVariable`
case class CreateVariable(name: Id, dataType: DataType, defaultExpr: Option[Expression] = None, replace: Boolean)
    extends LeafNode
    with Command

