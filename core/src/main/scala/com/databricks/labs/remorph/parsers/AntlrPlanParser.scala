package com.databricks.labs.remorph.parsers

import com.databricks.labs.remorph.{BuildingAst, KoResult, Parsing, Transformation, WorkflowStage}
import com.databricks.labs.remorph.intermediate.{LogicalPlan, ParsingErrors, PlanGenerationFailure}
import org.antlr.v4.runtime.{Parser, ParserRuleContext}

import scala.util.control.NonFatal

trait AntlrPlanParser extends PlanParser {

  def setErrorListener(parser: Parser, listener: ProductionErrorCollector): ProductionErrorCollector = {
    parser.removeErrorListeners()
    parser.addErrorListener(listener)
    listener
  }

  def generatePlan(
      context: ParserRuleContext,
      createPlan: () => LogicalPlan,
      errListener: ProductionErrorCollector): Transformation[LogicalPlan] = {
    if (errListener.errorCount > 0) {
      lift(KoResult(stage = WorkflowStage.PARSE, ParsingErrors(errListener.errors)))
    } else {
      update {
        case p: Parsing => BuildingAst(context, Some(p))
        case _ => BuildingAst(context)
      }.flatMap { _ =>
        try {
          ok(createPlan())
        } catch {
          case NonFatal(e) =>
            lift(KoResult(stage = WorkflowStage.PLAN, PlanGenerationFailure(e)))
        }
      }
    }
  }

}
