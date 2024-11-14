package com.databricks.labs.remorph.intermediate

abstract class CommentNode(val text: String) extends TreeNode[CommentNode] {
  override def children: Seq[CommentNode] = Seq.empty
}

case class LineCommentNode(override val text: String) extends CommentNode(text) {
  override def canEqual(that: Any): Boolean = that.isInstanceOf[LineCommentNode]
}
