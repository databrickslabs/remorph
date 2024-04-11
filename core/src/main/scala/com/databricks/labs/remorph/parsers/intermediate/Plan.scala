package com.databricks.labs.remorph.parsers.intermediate

// A [[Plan]] is the structure that carries the runtime information for the execution from the
// client to the server. A [[Plan]] can either be of the type [[Relation]] which is a reference
// to the underlying logical plan or it can be of the [[Command]] type that is used to execute
// commands on the server.
abstract class Plan extends TreeNode
