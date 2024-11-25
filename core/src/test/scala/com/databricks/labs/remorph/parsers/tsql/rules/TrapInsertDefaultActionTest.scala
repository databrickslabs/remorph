package com.databricks.labs.remorph.parsers.tsql.rules

import com.databricks.labs.remorph.parsers.PlanComparison
import com.databricks.labs.remorph.intermediate._
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class TrapInsertDefaultActionTest extends AnyWordSpec with PlanComparison with Matchers with IRHelpers {
  "TrapInsertDefaultsAction" should {
    "throw an exception when the MERGE WHEN NOT MATCHED action is 'INSERT DEFAULT VALUES'" in {
      val merge = MergeIntoTable(
        namedTable("table"),
        namedTable("table2"),
        Noop,
        Seq.empty,
        Seq(InsertDefaultsAction(None)),
        Seq.empty)
      assertThrows[IllegalArgumentException] {
        TrapInsertDefaultsAction(merge)
      }
    }
  }

}
