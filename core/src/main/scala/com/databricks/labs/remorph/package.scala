package com.databricks.labs

package object remorph {

  implicit class TransformationSeqOps[A](transformations: Seq[Transformation[A]]) extends TransformationConstructors {
    def sequence: Transformation[Seq[A]] = {
      transformations.foldLeft(ok(Seq.empty[A])) { case (agg, item) =>
        for {
          aggSeq <- agg
          i <- item
        } yield aggSeq :+ i
      }
    }
  }
}
