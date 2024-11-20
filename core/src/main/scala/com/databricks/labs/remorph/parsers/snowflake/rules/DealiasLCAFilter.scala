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
      .collect{ case a: Alias => a}
      .filter(alias => alias.child.isInstanceOf[Id]) // TODO do we need to support more than that ?
      .map(alias => alias.name.id -> alias.child.asInstanceOf[Id].id)
      .toMap
    if (aliases.isEmpty) {
      project
    } else {
      dealiasProject(project, filter, aliases)
    }
  }

  private def dealiasProject(project: Project, filter: Filter, aliases: Map[String, String]): Project = {
    val transformed = dealiasFilter(filter, aliases)
    if (transformed eq filter) {
      project
    } else {
      project.makeCopy(Array(transformed, project.columns)).asInstanceOf[Project]
    }
  }

  private def dealiasFilter(filter: Filter, aliases: Map[String, String]): Filter = {
    val transformed = filter.condition transform { case binary: Binary =>
      dealiasBinary(binary, aliases)
    }
    if (transformed eq filter.condition) {
      filter
    } else {
      filter.makeCopy(Array(filter.input, transformed)).asInstanceOf[Filter]
    }
  }

  private def dealiasBinary(binary: Binary, aliases: Map[String, String]): Expression = {
    val head = dealiasBinaryItem(binary.children.head, aliases)
    val last = dealiasBinaryItem(binary.children.last, aliases)
    if ((head eq binary.children.head) && (last eq binary.children.last)) {
      binary
    } else {
      binary.makeCopy(Array(head, last))
    }
  }

  def dealiasBinaryItem(item: Expression, aliases: Map[String, String]): Expression = {
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
        val replacement = alias.get._2
        item transform {
          case name: Name => name.makeCopy(Array(replacement))
          case id: Id => id.makeCopy(Array(replacement.asInstanceOf[AnyRef], id.caseSensitive.asInstanceOf[AnyRef]))
        }
      }
    }
  }
}
