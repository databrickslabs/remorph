-- tsql sql:
WITH LoginsCTE AS ( SELECT 'myDomain\myLogin' AS LoginName ) SELECT * FROM LoginsCTE;
