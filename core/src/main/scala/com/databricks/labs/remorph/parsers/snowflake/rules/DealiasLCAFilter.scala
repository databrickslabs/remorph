package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.intermediate.{Expression, _}

import scala.collection.immutable.Map

class DealiasLCAFilter extends Rule[LogicalPlan] with IRHelpers {

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
      .collect { case a: Alias => a }
      .filter(alias => !alias.child.isInstanceOf[Literal])
      .map(alias => alias.name.id -> alias.child)
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
    // above create new sequences so need a deep equal
    if ((partition == window.partition_spec) && (sort_order == window.sort_order)) {
      window
    } else {
      window.makeCopy(
        Array(
          window.window_function.asInstanceOf[AnyRef],
          partition.asInstanceOf[AnyRef],
          sort_order.asInstanceOf[AnyRef],
          window.frame_spec.asInstanceOf[AnyRef],
          window.ignore_nulls.asInstanceOf[AnyRef]))
    }
  }

  private def dealiasPartition(aliases: Map[String, Expression], partition: Seq[Expression]): Seq[Expression] = {
    partition map { col => dealiasColumnRef(aliases, col) }
  }

  private def dealiasSortOrder(aliases: Map[String, Expression], sort_order: Seq[SortOrder]): Seq[SortOrder] = {
    sort_order map { sort => dealiasSortOrder(aliases, sort) }
  }

  private def dealiasSortOrder(aliases: Map[String, Expression], sort_order: SortOrder): SortOrder = {
    val transformed = dealiasColumnRef(aliases, sort_order.child)
    if (transformed eq sort_order.child) {
      sort_order
    } else {
      sort_order.makeCopy(Array(transformed, sort_order.direction, sort_order.nullOrdering)).asInstanceOf[SortOrder]
    }
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
    if (transformed eq filter.condition) {
      filter
    } else {
      filter.makeCopy(Array(filter.input, transformed)).asInstanceOf[Filter]
    }
  }

  private def dealiasIn(aliases: Map[String, Expression], in: In): Expression = {
    val transformed = dealiasColumnRef(aliases, in.left)
    if (transformed eq in.left) {
      in
    } else {
      in.makeCopy(Array(transformed, in.other))
    }
  }

  private def dealiasBinary(aliases: Map[String, Expression], binary: Binary): Expression = {
    val head = dealiasColumnRef(aliases, binary.children.head)
    val last = dealiasColumnRef(aliases, binary.children.last)
    if ((head eq binary.children.head) && (last eq binary.children.last)) {
      binary
    } else {
      binary.makeCopy(Array(head, last))
    }
  }

  def dealiasColumnRef(aliases: Map[String, Expression], column: Expression): Expression = {
    val key = column match {
      case name: Name => name.name
      case id: Id => id.id
      case _ => null
    }
    if (key == null) {
      column
    } else {
      val alias = aliases.find(p => p._1 == key)
      if (alias.isEmpty) {
        column
      } else {
        alias.get._2
      }
    }
  }
}
