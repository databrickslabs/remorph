CREATE TABLE c_compatible_whitespace (whitespace_char VARCHAR);
INSERT INTO c_compatible_whitespace (whitespace_char) SELECT 
    CHR(32) || -- Blank
    CHR(13) || -- Carriage Return
    CHR(12) || -- Form Feed
    CHR(10) || -- Line Feed
    CHR(11) || -- Vertical Tab
    CHR(09)    -- tab (aka Horizontal Tab)
    ;

CREATE TABLE t1 (V VARCHAR);
INSERT INTO t1 (v) VALUES
   ('NoBlanks'),
   (' OneLeadingBlank'),
   ('OneTrailingBlank '),
   (' OneLeadingAndOneTrailingBlank ')
   ;
INSERT INTO t1 (v) SELECT 
    (CHR(09) || -- tab (aka Horizontal Tab)
     CHR(10) || -- Line Feed
     CHR(11) || -- Vertical Tab
     CHR(12) || -- Form Feed
     CHR(13) || -- Carriage Return
     CHR(32)    -- Blank 
      || 'Leading whitespace'
    )
   ;