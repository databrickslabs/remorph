-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/char-transact-sql?view=sql-server-ver16

CREATE DATABASE [multibyte-char-context]
  COLLATE Japanese_CI_AI
GO
USE [multibyte-char-context]
GO
SELECT NCHAR(0x266A) AS [eighth-note]
  , CONVERT(CHAR(2), 0x81F4) AS [context-dependent-convert]
  , CAST(0x81F4 AS CHAR(2)) AS [context-dependent-cast]