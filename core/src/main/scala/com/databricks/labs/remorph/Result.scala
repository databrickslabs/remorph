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

final class TBA[S, +A](val runF: Result[S => Result[(S, A)]]) {
  def map[B](f: A => B): TBA[S, B] = new TBA(runF.map(_.andThen(_.map { case (s, a) => (s, f(a)) })))
  def flatMap[B](f: A => TBA[S, B]): TBA[S, B] = new TBA(runF.map(_.andThen(_.flatMap { case (s, a) =>
    f(a).runF.flatMap(_.apply(s))
  })))
  def run(initialState: S): Result[(S, A)] = runF.flatMap(_.apply(initialState))
}

trait TBAS[S] {
  def ok[A](a: A): TBA[S, A] = new TBA(OkResult(s => OkResult((s, a))))
  def ko(stage: WorkflowStage, err: RemorphError): TBA[S, Nothing] = new TBA(OkResult(s => KoResult(stage, err)))
  def lift[X](res: Result[X]): TBA[S, X] = new TBA(OkResult(s => res.map(x => (s, x))))
  def get: TBA[S, S] = new TBA(OkResult(s => OkResult((s, s))))
  def set(newState: S): TBA[S, Unit] = new TBA(OkResult(_ => OkResult((newState, ()))))
  def update[T](f: PartialFunction[S, S]): TBA[S, Unit] = new TBA(
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
