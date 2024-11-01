package com.databricks.labs.remorph.generators.orchestration.rules

import com.databricks.labs.remorph.generators.orchestration.rules.bundles.Schema
import com.databricks.labs.remorph.generators.orchestration.rules.converted.{CreatedFile, NeedsVariables, PythonNotebookTask, SqlNotebookTask, SuccessPy, SuccessSQL, ToTask}
import com.databricks.labs.remorph.generators.orchestration.rules.history.Migration
import com.databricks.labs.remorph.intermediate.Rule
import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.labs.remorph.intermediate.workflows.jobs.JobSettings
import com.databricks.labs.remorph.intermediate.workflows.tasks.Task

class DefineJob extends Rule[JobNode] {
  override def apply(tree: JobNode): JobNode = tree transformUp {
    case NeedsVariables(SuccessPy(name, code), variables) =>
      PythonNotebookTask(CreatedFile(s"notebooks/$name.py", code), variables.map(_ -> "FILL_ME").toMap)
    case SuccessPy(name, code) =>
      PythonNotebookTask(CreatedFile(s"notebooks/$name.py", code))
    case NeedsVariables(SuccessSQL(name, code), variables) =>
      SqlNotebookTask(CreatedFile(s"notebooks/$name.sql", code), variables.map(_ -> "FILL_ME").toMap)
    case SuccessSQL(name, code) =>
      SqlNotebookTask(CreatedFile(s"notebooks/$name.sql", code))
    case m: Migration =>
      // TODO: create multiple jobs, once we realise we need that
      // TODO: add task dependencies via com.databricks.labs.remorph.graph.TableGraph
      var tasks = Seq[Task]()
      var other = Seq[JobNode]()
      m foreachUp {
        case toTask: ToTask =>
          tasks +:= toTask.toTask
        case task: Task =>
          tasks +:= task
        case file: CreatedFile =>
          other +:= file
        case schema: Schema =>
          other +:= schema
        case _ => // noop
      }
      val job = JobSettings("Migrated via Remorph", tasks.sortBy(_.taskKey), tags = Map("generator" -> "remorph"))
      Migration(other :+ job)
  }
}
