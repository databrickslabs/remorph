package com.databricks.labs.remorph

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.intermediate.{IncoherentState, RemorphError}

sealed trait WorkflowStage
object WorkflowStage {
  case object PARSE extends WorkflowStage
  case object PLAN extends WorkflowStage
  case object OPTIMIZE extends WorkflowStage
  case object GENERATE extends WorkflowStage
  case object FORMAT extends WorkflowStage
}

/**
 * Represents a stateful computation
 * @param runF
 * @tparam State
 * @tparam Out
 */
final class Transformation[State, +Out](val runF: Result[State => Result[(State, Out)]]) {

  def map[B](f: Out => B): Transformation[State, B] = new Transformation(runF.map(_.andThen(_.map { case (s, a) =>
    (s, f(a))
  })))

  def flatMap[B](f: Out => Transformation[State, B]): Transformation[State, B] = new Transformation(
    runF.map(_.andThen(_.flatMap { case (s, a) =>
      f(a).runF.flatMap(_.apply(s))
    })))

  def run(initialState: State): Result[(State, Out)] = runF.flatMap(_.apply(initialState))

  /**
   * Runs the computation and discard the final state,
   * @param initialState
   * @return
   */
  def runAndDiscardState(initialState: State): Result[Out] = run(initialState).map(_._2)
}

trait TransformationConstructors[S <: Phase] {
  def ok[A](a: A): Transformation[S, A] = new Transformation(OkResult(s => OkResult((s, a))))
  def ko(stage: WorkflowStage, err: RemorphError): Transformation[S, Nothing] = new Transformation(
    OkResult(s => KoResult(stage, err)))
  def lift[X](res: Result[X]): Transformation[S, X] = new Transformation(OkResult(s => res.map(x => (s, x))))
  def get: Transformation[S, S] = new Transformation(OkResult(s => OkResult((s, s))))
  def set(newState: S): Transformation[S, Unit] = new Transformation(OkResult(_ => OkResult((newState, ()))))
  def update[T](f: PartialFunction[S, S]): Transformation[S, Unit] = new Transformation(
    OkResult(s => OkResult((f.applyOrElse(s, identity[S]), ()))))

  def updateGenCtx(f: GeneratorContext => GeneratorContext): Transformation[Phase, Unit] = new Transformation(OkResult {
    case g: Generating => OkResult((g.copy(ctx = f(g.ctx)), ()))
    case p => KoResult(WorkflowStage.GENERATE, IncoherentState(p, classOf[Generating]))
  })

  def nest: Transformation[Phase, Unit] = updateGenCtx(_.nest)

  def unnest: Transformation[Phase, Unit] = updateGenCtx(_.unnest)

  def withIndentedBlock(
      header: Transformation[Phase, String],
      body: Transformation[Phase, String]): Transformation[Phase, String] =
    for {
      h <- header
      _ <- nest
      b <- body
      _ <- unnest
    } yield h + "\n" + b

  def withGenCtx: Transformation[Phase, GeneratorContext] = new Transformation(OkResult {
    case g: Generating => OkResult((g, g.ctx))
    case p => KoResult(WorkflowStage.GENERATE, IncoherentState(p, classOf[Generating]))
  })
}

sealed trait Result[+A] {
  def map[B](f: A => B): Result[B]
  def flatMap[B](f: A => Result[B]): Result[B]
  def isSuccess: Boolean
  def withNonBlockingError(error: RemorphError): Result[A]
}

case class OkResult[A](output: A) extends Result[A] {
  override def map[B](f: A => B): Result[B] = OkResult(f(output))

  override def flatMap[B](f: A => Result[B]): Result[B] = f(output)

  override def isSuccess: Boolean = true

  override def withNonBlockingError(error: RemorphError): Result[A] = PartialResult(output, error)
}

case class PartialResult[A](output: A, error: RemorphError) extends Result[A] {

  override def map[B](f: A => B): Result[B] = PartialResult(f(output), error)

  override def flatMap[B](f: A => Result[B]): Result[B] = f(output) match {
    case OkResult(res) => PartialResult(res, error)
    case PartialResult(res, err) => PartialResult(res, RemorphError.merge(error, err))
    case KoResult(stage, err) => KoResult(stage, RemorphError.merge(error, err))
  }

  override def isSuccess: Boolean = true

  override def withNonBlockingError(newError: RemorphError): Result[A] =
    PartialResult(output, RemorphError.merge(error, newError))
}

case class KoResult(stage: WorkflowStage, error: RemorphError) extends Result[Nothing] {
  override def map[B](f: Nothing => B): Result[B] = this

  override def flatMap[B](f: Nothing => Result[B]): Result[B] = this

  override def isSuccess: Boolean = false

  override def withNonBlockingError(newError: RemorphError): Result[Nothing] =
    KoResult(stage, RemorphError.merge(error, newError))
}
