package com.databricks.labs.remorph

import com.databricks.labs.remorph.intermediate.RemorphError

sealed trait WorkflowStage
object WorkflowStage {
  case object PARSE extends WorkflowStage
  case object PLAN extends WorkflowStage
  case object OPTIMIZE extends WorkflowStage
  case object GENERATE extends WorkflowStage
  case object FORMAT extends WorkflowStage
}

/**
 * Represents a stateful computation that will eventually produce an output of type Out. It manages a state of an
 * arbitrary type State along the way. Moreover, by relying on the semantics of Result, it is also able to handle
 * errors in a controlled way.
 *
 * It is important to note that nothing won't get evaluated until the run or runAndDiscardState are called.
 * @param runF
 *   The computation that will be carried out by this computation. It is basically a function that takes a State as
 *   parameter and returns a Result containing the, possibly updated, State along with the Output.
 *   The astute reader would have noticed that Result appears two times in the type of runF. They both have the same
 *   effect, in the sense of a KoResult will make any subsequent Transformation be ignored in both cases. The innermost
 *   Result allows for indicating that something went wrong while performing a given transformation, while the outermost
 *   one allows for indicating that something went wrong while combining to Transformation into a bigger one.
 * @tparam State
 *   The type of state this transformation will carry on.
 * @tparam Output
 *   The type of the produced output.
 */
final class Transformation[State, +Output](val runF: Result[State => Result[(State, Output)]]) {

  /**
   * Modify the output of this transformation using the provided function, without changing the managed state.
   *
   * If this transformation results in a KoResult, the provided function won't be evaluated.
   */
  def map[B](f: Output => B): Transformation[State, B] = new Transformation(runF.map(_.andThen(_.map { case (s, a) =>
    (s, f(a))
  })))

  /**
   * Chain this transformation with another one by passing this transformation's output to the provided function.
   *
   * If this transformation results in a KoResult, the provided function won't be evaluated.
   */
  def flatMap[B](f: Output => Transformation[State, B]): Transformation[State, B] = new Transformation(
    runF.map(_.andThen(_.flatMap { case (s, a) =>
      f(a).runF.flatMap(_.apply(s))
    })))

  /**
   * Run this transformation with the provided initial state. Produces a Result containing the final state and the
   * transformation's output.
   */
  def run(initialState: State): Result[(State, Output)] = runF.flatMap(_.apply(initialState))

  /**
   * Runs the computation using the provided initial state and return a Result containing the transformation's output,
   * discarding the final state.
   */
  def runAndDiscardState(initialState: State): Result[Output] = run(initialState).map(_._2)
}

trait TransformationConstructors[S <: Phase] {

  /**
   * Wraps a value into a successful transformation that ignores its state.
   */
  def ok[A](a: A): Transformation[S, A] = new Transformation(OkResult(s => OkResult((s, a))))

  /**
   * Wraps an error into a failed transformation.
   */
  def ko(stage: WorkflowStage, err: RemorphError): Transformation[S, Nothing] = new Transformation(
    OkResult(s => KoResult(stage, err)))

  /**
   * Wraps a Result into a transformation that ignores its state.
   */
  def lift[X](res: Result[X]): Transformation[S, X] = new Transformation(OkResult(s => res.map(x => (s, x))))

  /**
   * A tranformation whose output is the current state.
   */
  def get: Transformation[S, S] = new Transformation(OkResult(s => OkResult((s, s))))

  /**
   * A transformation that replaces the current state with the provided one, and produces no meaningful output.
   */
  def set(newState: S): Transformation[S, Unit] = new Transformation(OkResult(_ => OkResult((newState, ()))))

  /**
   * A transformation that updates the current state using the provided partial function, and produces no meaningful
   * output. If the provided partial function cannot be applied to the current state, it remains unchanged.
   */
  def update[T](f: PartialFunction[S, S]): Transformation[S, Unit] = new Transformation(
    OkResult(s => OkResult((f.applyOrElse(s, identity[S]), ()))))
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
