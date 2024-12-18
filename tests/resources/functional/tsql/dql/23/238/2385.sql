-- tsql sql:
WITH DateCTE AS ( SELECT @@DATEFIRST AS DateFirstSetting ) SELECT DateFirstSetting FROM DateCTE;
