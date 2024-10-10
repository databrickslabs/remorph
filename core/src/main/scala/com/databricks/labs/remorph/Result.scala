package com.databricks.labs.remorph

sealed trait WorkflowStage
object WorkflowStage {
  case object PARSE extends WorkflowStage
  case object PLAN extends WorkflowStage
  case object OPTIMIZE extends WorkflowStage
  case object GENERATE extends WorkflowStage
}


sealed trait Result[+A] {
  def map[B](f: A => B): Result[B]
  def flatMap[B](f: A => Result[B]): Result[B]
}

object Result {
  case class Success[A](output: A) extends Result[A] {
    override def map[B](f: A => B): Result[B] = Success(f(output))

    override def flatMap[B](f: A => Result[B]): Result[B] = f(output)
  }

  case class Failure(stage: WorkflowStage, errorJson: String) extends Result[Nothing] {
    override def map[B](f: Nothing => B): Result[B] = this

    override def flatMap[B](f: Nothing => Result[B]): Result[B] = this
  }
}
