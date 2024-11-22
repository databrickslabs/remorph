package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.intermediate.{Expression, _}

import scala.collection.immutable.Map

class DealiasLCAs extends Rule[LogicalPlan] with IRHelpers {

  override def apply(plan: LogicalPlan): LogicalPlan = {
    plan transform { case project: Project =>
      dealiasProject(project)
    }
  }

  private def dealiasProject(project: Project): Project = {
    val aliases = collectAliases(project.columns)
    if (aliases.isEmpty) {
      project
    } else {
      val input = dealiasInput(aliases, project.input)
      val columns = dealiasColumns(aliases, project.columns)
      if ((input eq project.input) && (columns eq project.columns)) {
        project
      } else {
        project.makeCopy(Array(input, columns)).asInstanceOf[Project]
      }
    }
  }

  private def collectAliases(columns: Seq[Expression]): Map[String, Expression] = {
    columns
      .collect { case Alias(e, name) if !e.isInstanceOf[Literal]=> name.id -> e }
      .toMap

  }

  private def dealiasColumns(aliases: Map[String, Expression], columns: Seq[Expression]): Seq[Expression] = {
    columns map { col => dealiasColumn(aliases, col) }
  }

  private def dealiasColumn(aliases: Map[String, Expression], column: Expression): Expression = {
    column transform { case window: Window =>
      dealiasWindow(aliases, window)
    }
  }

  private def dealiasWindow(aliases: Map[String, Expression], window: Window): Expression = {
    val partition = dealiasPartition(aliases, window.partition_spec)
    val sort_order = dealiasSortOrder(aliases, window.sort_order)
    window.makeCopy(
      Array(
        window.window_function.asInstanceOf[AnyRef],
        partition.asInstanceOf[AnyRef],
        sort_order.asInstanceOf[AnyRef],
        window.frame_spec.asInstanceOf[AnyRef],
        window.ignore_nulls.asInstanceOf[AnyRef]))
  }

  private def dealiasPartition(aliases: Map[String, Expression], partition: Seq[Expression]): Seq[Expression] = {
    partition map { col => dealiasExpression(aliases, col) }
  }

  private def dealiasSortOrder(aliases: Map[String, Expression], sort_order: Seq[SortOrder]): Seq[SortOrder] = {
    sort_order map { sort => dealiasSortOrder(aliases, sort) }
  }

  private def dealiasSortOrder(aliases: Map[String, Expression], sort_order: SortOrder): SortOrder = {
    val transformed = dealiasExpression(aliases, sort_order.child)
    sort_order.makeCopy(Array(transformed, sort_order.direction, sort_order.nullOrdering)).asInstanceOf[SortOrder]
  }

  private def dealiasInput(aliases: Map[String, Expression], input: LogicalPlan): LogicalPlan = {
    input match {
      case filter: Filter => dealiasFilter(aliases, filter)
      case _ => input
    }
  }

  private def dealiasFilter(aliases: Map[String, Expression], filter: Filter): Filter = {
    val transformed = filter.condition transform {
      case in: In => dealiasIn(aliases, in)
      case binary: Binary => dealiasBinary(aliases, binary)
    }
    filter.makeCopy(Array(filter.input, transformed)).asInstanceOf[Filter]
  }

  private def dealiasIn(aliases: Map[String, Expression], in: In): Expression = {
    val transformed = dealiasExpression(aliases, in.left)
    in.makeCopy(Array(transformed, in.other))
  }

  private def dealiasBinary(aliases: Map[String, Expression], binary: Binary): Expression = {
    val head = dealiasExpression(aliases, binary.children.head)
    val last = dealiasExpression(aliases, binary.children.last)
    binary.makeCopy(Array(head, last))
  }

  private def dealiasCallFunction(aliases: Map[String, Expression], func: CallFunction): CallFunction = {
    val args = func.arguments map { arg => dealiasExpression(aliases, arg) }
    func.makeCopy(Array(func.function_name, args)).asInstanceOf[CallFunction]
  }

  private def dealiasName(aliases: Map[String, Expression], name: Name): Expression = {
    val alias = aliases.find(p => p._1 == name.name)
    if (alias.isEmpty) {
      name
    } else {
      alias.get._2
    }
  }

  private def dealiasId(aliases: Map[String, Expression], id: Id): Expression = {
    val alias = aliases.find(p => p._1 == id.id)
    if (alias.isEmpty) {
      id
    } else {
      alias.get._2
    }
  }

  private def dealiasExpression(aliases: Map[String, Expression], column: Expression): Expression = {
    column transform {
      case name: Name => dealiasName(aliases, name)
      case id: Id => dealiasId(aliases, id)
      case func: CallFunction => dealiasCallFunction(aliases, func)
    }
  }
}
