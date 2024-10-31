package com.databricks.labs.remorph.generators.orchestration.rules

import com.databricks.labs.remorph.generators.orchestration.rules.converted.{SuccessPy, SuccessSQL}
import com.databricks.labs.remorph.generators.orchestration.rules.history.Migration
import com.databricks.labs.remorph.intermediate.Rule
import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.labs.remorph.intermediate.workflows.jobs.JobSettings
import com.databricks.labs.remorph.intermediate.workflows.tasks.Task
import com.databricks.labs.remorph.intermediate.workflows.tasks.intermediate.{PythonNotebookTask, SqlNotebookTask}

class DefineJob extends Rule[JobNode] {
  override def apply(tree: JobNode): JobNode = tree transformUp {
    // TODO: SuccessPy to become child of PythonNotebookTask
    case SuccessPy(name, code) => PythonNotebookTask(code).toTask(s"notebooks/$name.py")
    case SuccessSQL(name, code) => SqlNotebookTask(code).toTask(s"notebooks/$name.sql")
    case Migration(children) =>
      // TODO: add task dependencies via com.databricks.labs.remorph.graph.TableGraph
      val tasks = children.filter(_.isInstanceOf[Task]).map(_.asInstanceOf[Task])
      val notTasks = children.filterNot(_.isInstanceOf[Task])
      Migration(notTasks :+ JobSettings("Migrated via Remorph", tasks, tags = Map("generator" -> "remorph")))
  }
}
