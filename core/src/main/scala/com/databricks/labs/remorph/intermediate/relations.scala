package com.databricks.labs.remorph.intermediate

abstract class Relation extends LogicalPlan

abstract class RelationCommon extends Relation {}

case class SQL(query: String, named_arguments: Map[String, Expression], pos_arguments: Seq[Expression])
    extends LeafNode {
  override def output: Seq[Attribute] = Seq.empty
}

abstract class Read(is_streaming: Boolean) extends LeafNode

// TODO: replace it with TableIdentifier with catalog and schema filled
// TODO: replace most (if not all) occurrences with UnresolvedRelation
case class NamedTable(
    unparsed_identifier: String,
    options: Map[String, String] = Map.empty,
    is_streaming: Boolean = false)
    extends Read(is_streaming) {
  override def output: Seq[Attribute] = Seq.empty
}

case class DataSource(
    format: String,
    schemaString: String,
    options: Map[String, String],
    paths: Seq[String],
    predicates: Seq[String],
    is_streaming: Boolean)
    extends Read(is_streaming) {
  override def output: Seq[Attribute] = Seq.empty
}

case class Project(input: LogicalPlan, columns: Seq[Expression]) extends UnaryNode {
  override def child: LogicalPlan = input
  // TODO: add resolver for Star
  override def output: Seq[Attribute] = expressions.map {
    case a: Attribute => a
    case Alias(child, Id(name, _)) => AttributeReference(name, child.dataType)
    case Id(name, _) => AttributeReference(name, UnresolvedType)
    case Column(_, Id(name, _)) => AttributeReference(name, UnresolvedType)
    case expr: Expression => throw new UnsupportedOperationException(s"cannot convert to attribute: $expr")
  }
}

case class Filter(input: LogicalPlan, condition: Expression) extends UnaryNode {
  override def child: LogicalPlan = input
  override def output: Seq[Attribute] = input.output
}

abstract class JoinType

abstract class SetOpType

abstract class GroupType

abstract class ParseFormat

case class JoinDataType(is_left_struct: Boolean, is_right_struct: Boolean)

case class Join(
    left: LogicalPlan,
    right: LogicalPlan,
    join_condition: Option[Expression],
    join_type: JoinType,
    using_columns: Seq[String],
    join_data_type: JoinDataType)
    extends BinaryNode {
  override def output: Seq[Attribute] = left.output ++ right.output
}

case class SetOperation(
    left: LogicalPlan,
    right: LogicalPlan,
    set_op_type: SetOpType,
    is_all: Boolean,
    by_name: Boolean,
    allow_missing_columns: Boolean)
    extends BinaryNode {
  override def output: Seq[Attribute] = left.output ++ right.output
}

case class Limit(child: LogicalPlan, limit: Expression) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class Offset(child: LogicalPlan, offset: Expression) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class Tail(child: LogicalPlan, limit: Int) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class Pivot(col: Expression, values: Seq[Expression])

case class Aggregate(
    child: LogicalPlan,
    group_type: GroupType,
    grouping_expressions: Seq[Expression],
    pivot: Option[Pivot])
    extends UnaryNode {
  override def output: Seq[Attribute] = child.output ++ grouping_expressions.map(_.asInstanceOf[Attribute])
}

abstract class SortDirection(val sql: String)
case object UnspecifiedSortDirection extends SortDirection("")
case object Ascending extends SortDirection("ASC")
case object Descending extends SortDirection("DESC")

abstract class NullOrdering(val sql: String)
case object SortNullsUnspecified extends NullOrdering("")
case object NullsFirst extends NullOrdering("NULLS FIRST")
case object NullsLast extends NullOrdering("NULLS LAST")

case class SortOrder(
    expr: Expression,
    direction: SortDirection = UnspecifiedSortDirection,
    nullOrdering: NullOrdering = SortNullsUnspecified)
    extends Unary(expr) {
  override def dataType: DataType = child.dataType
}

case class Sort(child: LogicalPlan, order: Seq[SortOrder], is_global: Boolean = false) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class Drop(child: LogicalPlan, columns: Seq[Expression], column_names: Seq[String]) extends UnaryNode {
  override def output: Seq[Attribute] = child.output diff columns.map(_.asInstanceOf[Attribute])
}

case class Deduplicate(
    child: LogicalPlan,
    column_names: Seq[Expression],
    all_columns_as_keys: Boolean,
    within_watermark: Boolean)
    extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class LocalRelation(child: LogicalPlan, data: Array[Byte], schemaString: String) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class CachedLocalRelation(hash: String) extends LeafNode {
  override def output: Seq[Attribute] = Seq.empty
}

case class CachedRemoteRelation(relation_id: String) extends LeafNode {
  override def output: Seq[Attribute] = Seq.empty
}

case class Sample(
    child: LogicalPlan,
    lower_bound: Double,
    upper_bound: Double,
    with_replacement: Boolean,
    seed: Long,
    deterministic_order: Boolean)
    extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class Range(start: Long, end: Long, step: Long, num_partitions: Int) extends LeafNode {
  override def output: Seq[Attribute] = Seq(AttributeReference("id", LongType))
}

// TODO: most likely has to be SubqueryAlias(identifier: AliasIdentifier, child: LogicalPlan)
case class SubqueryAlias(child: LogicalPlan, alias: Id, columnNames: Seq[Id] = Seq.empty) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class Repartition(child: LogicalPlan, num_partitions: Int, shuffle: Boolean) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class ShowString(child: LogicalPlan, num_rows: Int, truncate: Int, vertical: Boolean) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class HtmlString(child: LogicalPlan, num_rows: Int, truncate: Int) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class StatSummary(child: LogicalPlan, statistics: Seq[String]) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class StatDescribe(child: LogicalPlan, cols: Seq[String]) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class StatCrosstab(child: LogicalPlan, col1: String, col2: String) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class StatCov(child: LogicalPlan, col1: String, col2: String) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class StatCorr(child: LogicalPlan, col1: String, col2: String, method: String) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class StatApproxQuantile(child: LogicalPlan, cols: Seq[String], probabilities: Seq[Double], relative_error: Double)
    extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class StatFreqItems(child: LogicalPlan, cols: Seq[String], support: Double) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class Fraction(stratum: Literal, fraction: Double)

case class StatSampleBy(child: LogicalPlan, col: Expression, fractions: Seq[Fraction], seed: Long) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class NAFill(child: LogicalPlan, cols: Seq[String], values: Seq[Literal]) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class NADrop(child: LogicalPlan, cols: Seq[String], min_non_nulls: Int) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class Replacement(old_value: Literal, new_value: Literal)

case class NAReplace(child: LogicalPlan, cols: Seq[String], replacements: Seq[Replacement]) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class ToDF(child: LogicalPlan, column_names: Seq[String]) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class WithColumnsRenamed(child: LogicalPlan, rename_columns_map: Map[String, String]) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class WithColumns(child: LogicalPlan, aliases: Seq[Alias]) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class WithWatermark(child: LogicalPlan, event_time: String, delay_threshold: String) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class Hint(child: LogicalPlan, name: String, parameters: Seq[Expression]) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class Values(values: Seq[Seq[Expression]]) extends LeafNode { // TODO: fix it
  override def output: Seq[Attribute] = Seq.empty
}

case class Unpivot(
    child: LogicalPlan,
    ids: Seq[Expression],
    values: Option[Values],
    variable_column_name: Id,
    value_column_name: Id)
    extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class ToSchema(child: LogicalPlan, dataType: DataType) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class RepartitionByExpression(child: LogicalPlan, partition_exprs: Seq[Expression], num_partitions: Int)
    extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class MapPartitions(child: LogicalPlan, func: CommonInlineUserDefinedTableFunction, is_barrier: Boolean)
    extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class GroupMap(
    child: LogicalPlan,
    grouping_expressions: Seq[Expression],
    func: CommonInlineUserDefinedFunction,
    sorting_expressions: Seq[Expression],
    initial_input: LogicalPlan,
    initial_grouping_expressions: Seq[Expression],
    is_map_groups_with_state: Boolean,
    output_mode: String,
    timeout_conf: String)
    extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class CoGroupMap(
    left: LogicalPlan,
    input_grouping_expressions: Seq[Expression],
    right: LogicalPlan,
    other_grouping_expressions: Seq[Expression],
    func: CommonInlineUserDefinedFunction,
    input_sorting_expressions: Seq[Expression],
    other_sorting_expressions: Seq[Expression])
    extends BinaryNode {
  override def output: Seq[Attribute] = left.output ++ right.output
}

case class ApplyInPandasWithState(
    child: LogicalPlan,
    grouping_expressions: Seq[Expression],
    func: CommonInlineUserDefinedFunction,
    output_schema: String,
    state_schema: String,
    output_mode: String,
    timeout_conf: String)
    extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class PythonUDTF(return_type: DataType, eval_type: Int, command: Array[Byte], python_ver: String)

case class CommonInlineUserDefinedTableFunction(
    function_name: String,
    deterministic: Boolean,
    arguments: Seq[Expression],
    python_udtf: Option[PythonUDTF])
    extends LeafNode {
  override def output: Seq[Attribute] = Seq.empty
}

case class CollectMetrics(child: LogicalPlan, name: String, metrics: Seq[Expression]) extends UnaryNode {
  override def output: Seq[Attribute] = child.output

}

case class Parse(child: LogicalPlan, format: ParseFormat, dataType: DataType, options: Map[String, String])
    extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class AsOfJoin(
    left: LogicalPlan,
    right: LogicalPlan,
    left_as_of: Expression,
    right_as_of: Expression,
    join_expr: Option[Expression],
    using_columns: Seq[String],
    join_type: String,
    tolerance: Option[Expression],
    allow_exact_matches: Boolean,
    direction: String)
    extends BinaryNode {
  override def output: Seq[Attribute] = left.output ++ right.output
}

case object Unknown extends LeafNode {
  override def output: Seq[Attribute] = Seq.empty
}

case object UnspecifiedJoin extends JoinType

case object InnerJoin extends JoinType

case object FullOuterJoin extends JoinType

case object LeftOuterJoin extends JoinType

case object RightOuterJoin extends JoinType

case object LeftAntiJoin extends JoinType

case object LeftSemiJoin extends JoinType

case object CrossJoin extends JoinType

case class NaturalJoin(joinType: JoinType) extends JoinType

case object UnspecifiedSetOp extends SetOpType

case object IntersectSetOp extends SetOpType

case object UnionSetOp extends SetOpType

case object ExceptSetOp extends SetOpType

case object UnspecifiedGroupType extends GroupType

case object GroupBy extends GroupType

case object GroupByAll extends GroupType

case object Pivot extends GroupType

case object UnspecifiedFormat extends ParseFormat

case object JsonFormat extends ParseFormat

case object CsvFormat extends ParseFormat
