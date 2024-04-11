package com.databricks.labs.remorph.parsers.intermediate

case class Origin(
    line: Option[Int] = None,
    startPosition: Option[Int] = None,
    startIndex: Option[Int] = None,
    stopIndex: Option[Int] = None,
    sqlText: Option[String] = None,
    objectType: Option[String] = None,
    objectName: Option[String] = None)

abstract class TreeNode
