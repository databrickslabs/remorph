package com.databricks.labs.remorph.intermediate

abstract class SubqueryExpression(plan: LogicalPlan) extends Expression {
  override def children: Seq[Expression] = plan.expressions // TODO: not sure if this is a good idea
  override def dataType: DataType = plan.schema
}

// returns one column. TBD if we want to split between
// one row (scala) and ListQuery (many rows), as it makes
// little difference for SQL code generation.
// scalar: SELECT * FROM a WHERE id = (SELECT id FROM b LIMIT 1)
// list: SELECT * FROM a WHERE id IN(SELECT id FROM b)
case class ScalarSubquery(relation: LogicalPlan) extends SubqueryExpression(relation) {
  override def dataType: DataType = relation.schema
}

// checks if a row exists in a subquery given some condition
case class Exists(relation: LogicalPlan) extends SubqueryExpression(relation) {
  override def dataType: DataType = relation.schema
}
