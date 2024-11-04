package com.databricks.labs.remorph.generators.orchestration.rules

import com.databricks.labs.remorph.discovery.ExecutedQuery
import com.databricks.labs.remorph.generators.orchestration.rules.converted.CreatedFile
import com.databricks.labs.remorph.generators.orchestration.rules.history.{FailedQuery, Migration, PartialQuery}
import com.databricks.labs.remorph.intermediate.Rule
import com.databricks.labs.remorph.intermediate.workflows.JobNode

class TrySummarizeFailures extends Rule[JobNode] {

  override def apply(tree: JobNode): JobNode = {
    var partials = Seq.empty[(ExecutedQuery, String)]
    val removedPartials = tree transformUp { case PartialQuery(executed, message, query) =>
      partials = partials :+ ((executed, message))
      query
    }
    removedPartials transformUp { case Migration(queries) =>
      var children = queries.filterNot(_.isInstanceOf[FailedQuery])
      val failedQueries = queries.filter(_.isInstanceOf[FailedQuery]).map(_.asInstanceOf[FailedQuery])
      if (failedQueries.nonEmpty) {
        children = children :+ failedQueryInfo(failedQueries.sortBy(_.query.id))
      }
      if (partials.nonEmpty) {
        children = children :+ partialQueryInfo(partials.distinct.sortBy(_._1.id))
      }
      Migration(children)
    }
  }

  private def failedQueryInfo(failedQueries: Seq[FailedQuery]): CreatedFile = {
    CreatedFile(
      "failed_queries.md",
      failedQueries map { case FailedQuery(query, message, stage) =>
        s"""
             |# query: `${query.id}`
             |$stage: $message
             |
             |```sql
             |${query.source}
             |```
             |""".stripMargin
      } mkString "\n")
  }

  private def partialQueryInfo(partials: Seq[(ExecutedQuery, String)]): CreatedFile = {
    CreatedFile(
      "partial_failures.md",
      partials map { case (query, message) =>
        s"""
             |# query: `${query.id}`
             |$message
             |
             |```sql
             |${query.source}
             |```
             |""".stripMargin
      } mkString "\n")
  }
}
