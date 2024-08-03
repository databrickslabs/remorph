package com.databricks.labs.remorph.utils

import java.io.{ByteArrayOutputStream, File, FileInputStream}
import java.nio.charset.Charset
import java.nio.charset.StandardCharsets.UTF_8

/**
 * This utility object is based on org.apache.spark.sql.catalyst.util
 */
object Strings {
  def fileToString(file: File, encoding: Charset = UTF_8): String = {
    val inStream = new FileInputStream(file)
    val outStream = new ByteArrayOutputStream
    try {
      var reading = true
      while (reading) {
        inStream.read() match {
          case -1 => reading = false
          case c => outStream.write(c)
        }
      }
      outStream.flush()
    } finally {
      inStream.close()
    }
    new String(outStream.toByteArray, encoding)
  }

  def sideBySide(left: String, right: String): Seq[String] = {
    sideBySide(left.split("\n"), right.split("\n"))
  }

  def sideBySide(left: Seq[String], right: Seq[String]): Seq[String] = {
    val maxLeftSize = left.map(_.length).max
    val leftPadded = left ++ Seq.fill(math.max(right.size - left.size, 0))("")
    val rightPadded = right ++ Seq.fill(math.max(left.size - right.size, 0))("")

    leftPadded.zip(rightPadded).map { case (l, r) =>
      (if (l == r) " " else "!") + l + (" " * ((maxLeftSize - l.length) + 3)) + r
    }
  }

  /** Shorthand for calling truncatedString() without start or end strings. */
  def truncatedString[T](seq: Seq[T], sep: String, maxFields: Int): String = {
    truncatedString(seq, "", sep, "", maxFields)
  }

  /**
   * Format a sequence with semantics similar to calling .mkString(). Any elements beyond maxNumToStringFields will be
   * dropped and replaced by a "... N more fields" placeholder.
   *
   * @return
   *   the trimmed and formatted string.
   */
  def truncatedString[T](seq: Seq[T], start: String, sep: String, end: String, maxFields: Int): String = {
    if (seq.length > maxFields) {
      val numFields = math.max(0, maxFields - 1)
      seq.take(numFields).mkString(start, sep, sep + "... " + (seq.length - numFields) + " more fields" + end)
    } else {
      seq.mkString(start, sep, end)
    }
  }
}
