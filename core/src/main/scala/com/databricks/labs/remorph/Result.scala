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
 * Represents a stateful computation that will eventually produce an output of type Out. It manages a state of
 * type Phase along the way. Moreover, by relying on the semantics of Result, it is also able to handle
 * errors in a controlled way.
 *
 * It is important to note that nothing won't get evaluated until the run or runAndDiscardState are called.
 * @param run
 *   The computation that will be carried out by this computation. It is basically a function that takes a Phase as
 *   parameter and returns a Result containing the, possibly updated, State along with the Output.
 * @tparam Output
 *   The type of the produced output.
 */
final class Transformation[+Output](val run: Phase => Result[(Phase, Output)]) {

  /**
   * Modify the output of this transformation using the provided function, without changing the managed state.
   *
   * If this transformation results in a KoResult, the provided function won't be evaluated.
   */
  def map[B](f: Output => B): Transformation[B] = new Transformation(run.andThen(_.map { case (s, a) => (s, f(a)) }))

  /**
   * Chain this transformation with another one by passing this transformation's output to the provided function.
   *
   * If this transformation results in a KoResult, the provided function won't be evaluated.
   */
  def flatMap[B](f: Output => Transformation[B]): Transformation[B] = new Transformation(run.andThen {
    case OkResult((s, a)) => f(a).run(s)
    case p @ PartialResult((s, a), err) => p.flatMap { _ => f(a).run(s.recordError(err)) }
    case ko: KoResult => ko
  })

  /**
   * Runs the computation using the provided initial state and return a Result containing the transformation's output,
   * discarding the final state.
   */
  def runAndDiscardState(initialState: Phase): Result[Output] = run(initialState).map(_._2)
}

trait TransformationConstructors {

  /**
   * Wraps a value into a successful transformation that ignores its state.
   */
  def ok[A](a: A): Transformation[A] = new Transformation(s => OkResult((s, a)))

  /**
   * Wraps an error into a failed transformation.
   */
  def ko(stage: WorkflowStage, err: RemorphError): Transformation[Nothing] = new Transformation(s =>
    KoResult(stage, err))

  /**
   * Wraps a Result into a transformation that ignores its state.
   */
  def lift[X](res: Result[X]): Transformation[X] = new Transformation(s => res.map(x => (s, x)))

  /**
   * A tranformation whose output is the current state.
   */
  def get: Transformation[Phase] = new Transformation(s => OkResult((s, s)))

  /**
   * A transformation that replaces the current state with the provided one, and produces no meaningful output.
   */
  def set(newState: Phase): Transformation[Unit] = new Transformation(_ => OkResult((newState, ())))

  /**
   * A transformation that updates the current state using the provided partial function, and produces no meaningful
   * output. If the provided partial function cannot be applied to the current state, it remains unchanged.
   */
  def update(f: PartialFunction[Phase, Phase]): Transformation[Unit] = new Transformation(s =>
    OkResult((f.applyOrElse(s, identity[Phase]), ())))
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
