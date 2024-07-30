package com.databricks.labs.remorph.parsers.intermediate

abstract class SubqueryExpression(plan: LogicalPlan) extends Expression {
  override def children: Seq[Expression] = plan.expressions // TODO: not sure if this is a good idea
}

// returns one column. TBD if we want to split between
// one row (scala) and ListQuery (many rows), as it makes
// little difference for SQL code generation.
// scalar: SELECT * FROM a WHERE id = (SELECT id FROM b LIMIT 1)
// list: SELECT * FROM a WHERE id IN(SELECT id FROM b)
case class ScalarSubquery(relation: LogicalPlan) extends SubqueryExpression(relation) {
  // TODO: we need to resolve schema of the plan
  //  before we get the type of this expression
  override def dataType: DataType = UnresolvedType
}

// checks if a row exists in a subquery given some condition
case class Exists(relation: LogicalPlan) extends SubqueryExpression(relation) {
  // TODO: we need to resolve schema of the plan
  //  before we get the type of this expression
  override def dataType: DataType = UnresolvedType
}
