ALTER EXTERNAL TABLE [ IF EXISTS ] <name> REFRESH [ '<relative-path>' ]

ALTER EXTERNAL TABLE [ IF EXISTS ] <name> ADD FILES ( '<path>/[<filename>]' [ , '<path>/[<filename>'] ] )

ALTER EXTERNAL TABLE [ IF EXISTS ] <name> REMOVE FILES ( '<path>/[<filename>]' [ , '<path>/[<filename>]' ] )

ALTER EXTERNAL TABLE [ IF EXISTS ] <name> SET
  [ AUTO_REFRESH = { TRUE | FALSE } ]
  [ TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ] ]

ALTER EXTERNAL TABLE [ IF EXISTS ] <name> UNSET
  TAG <tag_name> [ , <tag_name> ... ]