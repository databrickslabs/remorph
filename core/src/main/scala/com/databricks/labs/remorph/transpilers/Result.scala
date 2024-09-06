package com.databricks.labs.remorph.transpilers

sealed trait Result[+A] {
  def stage: WorkflowStage
  def map[B](f: A => B): Result[B]
  def flatMap[B](f: A => Result[B]): Result[B]
}

object Result {
  case class Success[A](stage: WorkflowStage = WorkflowStage.PARSE, output: A) extends Result[A] {
    override def map[B](f: A => B): Result[B] = Success(stage, f(output))

    override def flatMap[B](f: A => Result[B]): Result[B] = f(output)
  }

  case class Failure(stage: WorkflowStage, errorJson: String) extends Result[Nothing] {
    override def map[B](f: Nothing => B): Result[B] = this

    override def flatMap[B](f: Nothing => Result[B]): Result[B] = this
  }

  implicit class ResultKleisli[A, B](f: A => Result[B]) {
    def >>[C](other: B => Result[C]): A => Result[C] = a => f(a).flatMap(other)
  }
}
