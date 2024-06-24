package com.databricks.labs.remorph.parsers.intermediate

class Relation extends Plan {}

abstract class RelationCommon extends Relation {}

case class SQL(query: String, named_arguments: Map[String, Expression], pos_arguments: Seq[Expression])
    extends RelationCommon {}

abstract class Read(is_streaming: Boolean) extends RelationCommon {}

case class NamedTable(unparsed_identifier: String, options: Map[String, String], is_streaming: Boolean)
    extends Read(is_streaming) {}

case class DataSource(
    format: String,
    schema: String,
    options: Map[String, String],
    paths: Seq[String],
    predicates: Seq[String],
    is_streaming: Boolean)
    extends Read(is_streaming) {}

case class Project(input: Relation, expressions: Seq[Expression]) extends RelationCommon {}

case class Filter(input: Relation, condition: Expression) extends RelationCommon {}

abstract class JoinType
case object UnspecifiedJoin extends JoinType
case object InnerJoin extends JoinType
case object FullOuterJoin extends JoinType
case object LeftOuterJoin extends JoinType
case object RightOuterJoin extends JoinType
case object LeftAntiJoin extends JoinType
case object LeftSemiJoin extends JoinType
case object CrossJoin extends JoinType

case class JoinDataType(is_left_struct: Boolean, is_right_struct: Boolean)

case class Join(
    left: Relation,
    right: Relation,
    join_condition: Option[Expression],
    join_type: JoinType,
    using_columns: Seq[String],
    join_data_type: JoinDataType)
    extends RelationCommon {}

abstract class SetOpType
case object UnspecifiedSetOp extends SetOpType
case object IntersectSetOp extends SetOpType
case object UnionSetOp extends SetOpType
case object ExceptSetOp extends SetOpType

case class SetOperation(
    left_input: Relation,
    right_input: Relation,
    set_op_type: SetOpType,
    is_all: Boolean,
    by_name: Boolean,
    allow_missing_columns: Boolean)
    extends RelationCommon {}

case class Limit(input: Relation, limit: Int) extends RelationCommon {}

case class Offset(input: Relation, offset: Int) extends RelationCommon {}

case class Tail(input: Relation, limit: Int) extends RelationCommon {}

abstract class GroupType
case object UnspecifiedGroupType extends GroupType
case object GroupBy extends GroupType
case object Rollup extends GroupType
case object Cube extends GroupType
case object Pivot extends GroupType

case class Pivot(col: Expression, values: Seq[Literal])

case class Aggregate(
    input: Relation,
    group_type: GroupType,
    grouping_expressions: Seq[Expression],
    pivot: Option[Pivot])
    extends RelationCommon {}

case class Sort(input: Relation, order: Seq[SortOrder], is_global: Boolean) extends RelationCommon {}

case class Drop(input: Relation, columns: Seq[Expression], column_names: Seq[String]) extends RelationCommon {}

case class Deduplicate(input: Relation, column_names: Seq[Id], all_columns_as_keys: Boolean, within_watermark: Boolean)
    extends RelationCommon {}

case class LocalRelation(input: Relation, data: Array[Byte], schema: String) extends RelationCommon {}

case class CachedLocalRelation(hash: String) extends RelationCommon {}

case class CachedRemoteRelation(relation_id: String) extends RelationCommon {}

case class Sample(
    input: Relation,
    lower_bound: Double,
    upper_bound: Double,
    with_replacement: Boolean,
    seed: Long,
    deterministic_order: Boolean)
    extends RelationCommon {}

case class Range(start: Long, end: Long, step: Long, num_partitions: Int) extends RelationCommon {}

case class SubqueryAlias(input: Relation, alias: Id, qualifier: String) extends RelationCommon {}

case class Repartition(input: Relation, num_partitions: Int, shuffle: Boolean) extends RelationCommon {}

case class ShowString(input: Relation, num_rows: Int, truncate: Int, vertical: Boolean) extends RelationCommon {}

case class HtmlString(input: Relation, num_rows: Int, truncate: Int) extends RelationCommon {}

case class StatSummary(input: Relation, statistics: Seq[String]) extends RelationCommon {}

case class StatDescribe(input: Relation, cols: Seq[String]) extends RelationCommon {}

case class StatCrosstab(input: Relation, col1: String, col2: String) extends RelationCommon {}

case class StatCov(input: Relation, col1: String, col2: String) extends RelationCommon {}

case class StatCorr(input: Relation, col1: String, col2: String, method: String) extends RelationCommon {}

case class StatApproxQuantile(input: Relation, cols: Seq[String], probabilities: Seq[Double], relative_error: Double)
    extends RelationCommon {}

case class StatFreqItems(input: Relation, cols: Seq[String], support: Double) extends RelationCommon {}

case class Fraction(stratum: Literal, fraction: Double)

case class StatSampleBy(input: Relation, col: Expression, fractions: Seq[Fraction], seed: Long)
    extends RelationCommon {}

case class NAFill(input: Relation, cols: Seq[String], values: Seq[Literal]) extends RelationCommon {}

case class NADrop(input: Relation, cols: Seq[String], min_non_nulls: Int) extends RelationCommon {}

case class Replacement(old_value: Literal, new_value: Literal)

case class NAReplace(input: Relation, cols: Seq[String], replacements: Seq[Replacement]) extends RelationCommon {}

case class ToDF(input: Relation, column_names: Seq[String]) extends RelationCommon {}

case class WithColumnsRenamed(input: Relation, rename_columns_map: Map[String, String]) extends RelationCommon {}

case class WithColumns(input: Relation, aliases: Seq[Alias]) extends RelationCommon {}

case class WithWatermark(input: Relation, event_time: String, delay_threshold: String) extends RelationCommon {}

case class Hint(input: Relation, name: String, parameters: Seq[Expression]) extends RelationCommon {}

case class Values(values: Seq[Seq[Expression]]) extends RelationCommon {}

case class Unpivot(
    input: Relation,
    ids: Seq[Expression],
    values: Option[Values],
    variable_column_name: Id,
    value_column_name: Id)
    extends RelationCommon {}

case class ToSchema(input: Relation, schema: DataType) extends RelationCommon {}

case class RepartitionByExpression(input: Relation, partition_exprs: Seq[Expression], num_partitions: Int)
    extends RelationCommon {}

case class MapPartitions(input: Relation, func: CommonInlineUserDefinedTableFunction, is_barrier: Boolean)
    extends RelationCommon {}

case class GroupMap(
    input: Relation,
    grouping_expressions: Seq[Expression],
    func: CommonInlineUserDefinedFunction,
    sorting_expressions: Seq[Expression],
    initial_input: Relation,
    initial_grouping_expressions: Seq[Expression],
    is_map_groups_with_state: Boolean,
    output_mode: String,
    timeout_conf: String)
    extends RelationCommon {}

case class CoGroupMap(
    input: Relation,
    input_grouping_expressions: Seq[Expression],
    other: Relation,
    other_grouping_expressions: Seq[Expression],
    func: CommonInlineUserDefinedFunction,
    input_sorting_expressions: Seq[Expression],
    other_sorting_expressions: Seq[Expression])
    extends RelationCommon {}

case class ApplyInPandasWithState(
    input: Relation,
    grouping_expressions: Seq[Expression],
    func: CommonInlineUserDefinedFunction,
    output_schema: String,
    state_schema: String,
    output_mode: String,
    timeout_conf: String)
    extends RelationCommon {}

case class PythonUDTF(return_type: DataType, eval_type: Int, command: Array[Byte], python_ver: String)

case class CommonInlineUserDefinedTableFunction(
    function_name: String,
    deterministic: Boolean,
    arguments: Seq[Expression],
    python_udtf: Option[PythonUDTF])
    extends RelationCommon {}

case class CollectMetrics(input: Relation, name: String, metrics: Seq[Expression]) extends RelationCommon {}

abstract class ParseFormat
case object UnspecifiedFormat extends ParseFormat
case object JsonFormat extends ParseFormat
case object CsvFormat extends ParseFormat

case class Parse(input: Relation, format: ParseFormat, schema: Option[DataType], options: Map[String, String])
    extends RelationCommon {}

case class AsOfJoin(
    left: Relation,
    right: Relation,
    left_as_of: Expression,
    right_as_of: Expression,
    join_expr: Option[Expression],
    using_columns: Seq[String],
    join_type: String,
    tolerance: Option[Expression],
    allow_exact_matches: Boolean,
    direction: String)
    extends RelationCommon {}

case class Unknown() extends RelationCommon {}
