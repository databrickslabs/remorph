package com.databricks.labs.remorph.intermediate

/**
 * A [[Plan]] is the structure that carries the runtime information for the execution from the client to the server. A
 * [[Plan]] can either be of the type [[Relation]] which is a reference to the underlying logical plan or it can be of
 * the [[Command]] type that is used to execute commands on the server. [[Plan]] is a union of Spark's LogicalPlan and
 * QueryPlan.
 */
abstract class Plan[PlanType <: Plan[PlanType]] extends TreeNode[PlanType] {
  self: PlanType =>

  def output: Seq[Attribute]

  /**
   * Returns the set of attributes that are output by this node.
   */
  @transient
  lazy val outputSet: AttributeSet = new AttributeSet(output: _*)

  /**
   * The set of all attributes that are child to this operator by its children.
   */
  def inputSet: AttributeSet = new AttributeSet(children.flatMap(_.asInstanceOf[Plan[PlanType]].output): _*)

  /**
   * The set of all attributes that are produced by this node.
   */
  def producedAttributes: AttributeSet = new AttributeSet()

  /**
   * All Attributes that appear in expressions from this operator. Note that this set does not include attributes that
   * are implicitly referenced by being passed through to the output tuple.
   */
  @transient
  lazy val references: AttributeSet = new AttributeSet(expressions.flatMap(_.references): _*) -- producedAttributes

  /**
   * Attributes that are referenced by expressions but not provided by this node's children.
   */
  final def missingInput: AttributeSet = references -- inputSet

  /**
   * Runs [[transformExpressionsDown]] with `rule` on all expressions present in this query operator. Users should not
   * expect a specific directionality. If a specific directionality is needed, transformExpressionsDown or
   * transformExpressionsUp should be used.
   *
   * @param rule
   *   the rule to be applied to every expression in this operator.
   */
  def transformExpressions(rule: PartialFunction[Expression, Expression]): this.type = {
    transformExpressionsDown(rule)
  }

  /**
   * Runs [[transformDown]] with `rule` on all expressions present in this query operator.
   *
   * @param rule
   *   the rule to be applied to every expression in this operator.
   */
  def transformExpressionsDown(rule: PartialFunction[Expression, Expression]): this.type = {
    mapExpressions(_.transformDown(rule))
  }

  /**
   * Runs [[transformUp]] with `rule` on all expressions present in this query operator.
   *
   * @param rule
   *   the rule to be applied to every expression in this operator.
   * @return
   */
  def transformExpressionsUp(rule: PartialFunction[Expression, Expression]): this.type = {
    mapExpressions(_.transformUp(rule))
  }

  /**
   * Apply a map function to each expression present in this query operator, and return a new query operator based on
   * the mapped expressions.
   */
  def mapExpressions(f: Expression => Expression): this.type = {
    var changed = false

    @inline def transformExpression(e: Expression): Expression = {
      val newE = CurrentOrigin.withOrigin(e.origin) {
        f(e)
      }
      if (newE.fastEquals(e)) {
        e
      } else {
        changed = true
        newE
      }
    }

    def recursiveTransform(arg: Any): AnyRef = arg match {
      case e: Expression => transformExpression(e)
      case Some(value) => Some(recursiveTransform(value))
      case m: Map[_, _] => m
      case d: DataType => d // Avoid unpacking Structs
      case stream: Stream[_] => stream.map(recursiveTransform).force
      case seq: Iterable[_] => seq.map(recursiveTransform)
      case other: AnyRef => other
      case null => null
    }

    val newArgs = mapProductIterator(recursiveTransform)

    if (changed) makeCopy(newArgs).asInstanceOf[this.type] else this
  }

  /**
   * Returns the result of running [[transformExpressions]] on this node and all its children. Note that this method
   * skips expressions inside subqueries.
   */
  def transformAllExpressions(rule: PartialFunction[Expression, Expression]): this.type = {
    transform { case q: Plan[_] =>
      q.transformExpressions(rule).asInstanceOf[PlanType]
    }.asInstanceOf[this.type]
  }

  /**
   * Returns all of the expressions present in this query (that is expression defined in this plan operator and in each
   * its descendants).
   */
  final def expressions: Seq[Expression] = {
    // Recursively find all expressions from a traversable.
    def seqToExpressions(seq: Iterable[Any]): Iterable[Expression] = seq.flatMap {
      case e: Expression => e :: Nil
      case p: Plan[_] => p.expressions
      case s: Iterable[_] => seqToExpressions(s)
      case other => Nil
    }

    productIterator.flatMap {
      case e: Expression => e :: Nil
      case s: Some[_] => seqToExpressions(s.toSeq)
      case seq: Iterable[_] => seqToExpressions(seq)
      case other => Nil
    }.toSeq
  }
}

abstract class LogicalPlan extends Plan[LogicalPlan] {

  /**
   * Returns true if this expression and all its children have been resolved to a specific schema and false if it still
   * contains any unresolved placeholders. Implementations of LogicalPlan can override this (e.g.[[UnresolvedRelation]]
   * should return `false`).
   */
  lazy val resolved: Boolean = expressions.forall(_.resolved) && childrenResolved

  /**
   * Returns true if all its children of this query plan have been resolved.
   */
  def childrenResolved: Boolean = children.forall(_.resolved)

  def schema: DataType = {
    val concrete = output.forall(_.isInstanceOf[Attribute])
    if (concrete) {
      StructType(output.map { a: Attribute =>
        StructField(a.name, a.dataType)
      })
    } else {
      UnresolvedType
    }
  }

}

abstract class LeafNode extends LogicalPlan {
  override def children: Seq[LogicalPlan] = Nil
  override def producedAttributes: AttributeSet = outputSet
}

abstract class UnaryNode extends LogicalPlan {
  def child: LogicalPlan
  override def children: Seq[LogicalPlan] = child :: Nil
}

abstract class BinaryNode extends LogicalPlan {
  def left: LogicalPlan
  def right: LogicalPlan
  override def children: Seq[LogicalPlan] = Seq(left, right)
}
