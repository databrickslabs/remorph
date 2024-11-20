package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.intermediate._

class DealiasLCAFilter extends Rule[LogicalPlan] with IRHelpers {

  override def apply(plan: LogicalPlan): LogicalPlan = plan transform { case project: Project =>
    dealiasProject(project)
  }

  private def dealiasProject(project: Project): Project = {
    project.input match {
      case filter: Filter => dealiasProject(project, filter)
      case _ => project
    }
  }

  def dealiasProject(project: Project, filter: Filter): Project = {
    val aliases = project.columns
      .collect { case a: Alias => a }
      .filter(alias => !alias.child.isInstanceOf[Literal])
      .map(alias => alias.name.id -> alias.child)
      .toMap
    if (aliases.isEmpty) {
      project
    } else {
      dealiasProject(project, filter, aliases)
    }
  }

  private def dealiasProject(project: Project, filter: Filter, aliases: Map[String, Expression]): Project = {
    val transformed = dealiasFilter(filter, aliases)
    if (transformed eq filter) {
      project
    } else {
      project.makeCopy(Array(transformed, project.columns)).asInstanceOf[Project]
    }
  }

  private def dealiasFilter(filter: Filter, aliases: Map[String, Expression]): Filter = {
    val transformed = filter.condition transform {
      case in: In => dealiasIn(in, aliases)
      case binary: Binary => dealiasBinary(binary, aliases)
    }
    if (transformed eq filter.condition) {
      filter
    } else {
      filter.makeCopy(Array(filter.input, transformed)).asInstanceOf[Filter]
    }
  }

  private def dealiasIn(in: In, aliases: Map[String, Expression]): Expression = {
    val transformed = dealiasColumnRef(in.left, aliases)
    if (transformed eq in.left) {
      in
    } else {
      in.makeCopy(Array(transformed, in.other))
    }
  }

  private def dealiasBinary(binary: Binary, aliases: Map[String, Expression]): Expression = {
    val head = dealiasColumnRef(binary.children.head, aliases)
    val last = dealiasColumnRef(binary.children.last, aliases)
    if ((head eq binary.children.head) && (last eq binary.children.last)) {
      binary
    } else {
      binary.makeCopy(Array(head, last))
    }
  }

  def dealiasColumnRef(item: Expression, aliases: Map[String, Expression]): Expression = {
    val key = item match {
      case name: Name => name.name
      case id: Id => id.id
      case _ => null
    }
    if (key == null) {
      item
    } else {
      val alias = aliases.find(p => p._1 == key)
      if (alias.isEmpty) {
        item
      } else {
        alias.get._2
      }
    }
  }
}
