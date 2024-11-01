package com.databricks.labs.remorph.generators

import com.databricks.labs.remorph.{Generating, KoResult, OkResult, Transformation, TransformationConstructors, WorkflowStage}
import com.databricks.labs.remorph.intermediate.{IncoherentState, TreeNode, UnexpectedNode}

trait Generator[In <: TreeNode[In], Out] extends TransformationConstructors {
  def generate(tree: In): Transformation[Out]
  def unknown(tree: In): Transformation[Nothing] =
    ko(WorkflowStage.GENERATE, UnexpectedNode(tree.getClass.getSimpleName))
}

trait CodeGenerator[In <: TreeNode[In]] extends Generator[In, String] {

  private def generateAndJoin(trees: Seq[In], separator: String): Transformation[String] = {
    trees.map(generate).sequence.map(_.mkString(separator))
  }

  /**
   * Apply the generator to the input nodes and join the results with commas.
   */
  def commas(trees: Seq[In]): Transformation[String] = generateAndJoin(trees, ", ")

  /**
   * Apply the generator to the input nodes and join the results with whitespaces.
   */
  def spaces(trees: Seq[In]): Transformation[String] = generateAndJoin(trees, " ")

  /**
   * When the current Phase is Generating, update its GeneratorContext with the provided function.
   * @param f
   *   A function for updating a GeneratorContext.
   * @return
   *   A transformation that:
   *     - updates the state according to f and produces no meaningful output when the current Phase is Generating.
   *     - fails if the current Phase is different from Generating.
   */
  def updateGenCtx(f: GeneratorContext => GeneratorContext): Transformation[Unit] = new Transformation({
    case g: Generating => OkResult((g.copy(ctx = f(g.ctx)), ()))
    case p => KoResult(WorkflowStage.GENERATE, IncoherentState(p, classOf[Generating]))
  })

  /**
   * When the current Phase is Generating, update the GeneratorContext by incrementing the indentation level.
   * @return
   *   A tranformation that increases the indentation level when the current Phase is Generating and fails otherwise.
   */
  def nest: Transformation[Unit] = updateGenCtx(_.nest)

  /**
   * When the current Phase is Generating, update the GeneratorContext by decrementing the indentation level.
   * @return
   *    A tranformation that decreases the indentation level when the current Phase is Generating and fails otherwise.
   */
  def unnest: Transformation[Unit] = updateGenCtx(_.unnest)

  /**
   * When the current Phase is Generating, produce a block of code where the provided body is nested under the header.
   * @param header
   *   A transformation that produces the header, which will remain unindented. Could be a function signature,
   *   a class definition, etc.
   * @param body
   *   A transformation that produces the body, which will be indented one level under the header.
   * @return
   *   A transformation that produces the header followed by the indented body (separated by a newline) and restores
   *   the indentation level to its original value. Said transformation will fail if the current Phase isn't
   *   Generating.
   */
  def withIndentedBlock(header: Transformation[String], body: Transformation[String]): Transformation[String] =
    for {
      h <- header
      _ <- nest
      b <- body
      _ <- unnest
    } yield h + "\n" + b

  /**
   * When the current Phase is Generating, allows for building transformations that use the current GeneratorContext.
   * @param transfoUsingCtx
   *   A function that will receive the current GeneratorContext and produce a Transformation.
   * @return
   *   A transformation that uses the current GeneratorContext if the current Phase is Generating and fails otherwise.
   */
  def withGenCtx(transfoUsingCtx: GeneratorContext => Transformation[String]): Transformation[String] =
    new Transformation[GeneratorContext]({
      case g: Generating => OkResult((g, g.ctx))
      case p => KoResult(WorkflowStage.GENERATE, IncoherentState(p, classOf[Generating]))
    }).flatMap(transfoUsingCtx)
}
