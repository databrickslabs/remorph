package com.databricks.labs.remorph.generators.orchestration.rules

import com.databricks.labs.remorph.TranspilerState
import com.databricks.labs.remorph.generators.orchestration.rules.bundles.Schema
import com.databricks.labs.remorph.generators.orchestration.rules.converted.{CreatedFile, PythonNotebookTask}
import com.databricks.labs.remorph.generators.orchestration.rules.history.Migration
import com.databricks.labs.remorph.intermediate.Noop
import com.databricks.labs.remorph.intermediate.workflows.jobs.JobSettings
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class GenerateBundleFileTest extends AnyWordSpec with Matchers {
  private[this] val rule = new GenerateBundleFile

  "GenerateBundleFile" should {
    "skip nulls" in {
      val task = PythonNotebookTask(CreatedFile("notebooks/foo.py", "import foo")).toTask
      val plan = Migration(Seq(Schema("main", "foo"), Schema("main", "bar"), JobSettings("main workflow", Seq(task))))
      val tree = rule.apply(plan).runAndDiscardState(TranspilerState())

      tree.getOrElse(Noop).find(_.isInstanceOf[CreatedFile]).get shouldBe CreatedFile(
        "databricks.yml",
        s"""---
           |bundle:
           |  name: "remorphed"
           |targets:
           |  dev:
           |    mode: "development"
           |    default: true
           |  prod:
           |    mode: "production"
           |resources:
           |  jobs:
           |    main_workflow:
           |      name: "[$${bundle.target}] main workflow"
           |      tasks:
           |      - notebook_task:
           |          notebook_path: "notebooks/foo.py"
           |        task_key: "foo"
           |  schemas:
           |    foo:
           |      catalog_name: "main"
           |      name: "foo"
           |    bar:
           |      catalog_name: "main"
           |      name: "bar"
           |""".stripMargin)
    }
  }
}
