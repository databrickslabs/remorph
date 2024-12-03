--Query type: DCL
WITH FileNames AS ( SELECT 'old_file_name' AS old_name, 'new_file_name' AS new_name ) SELECT 'MODIFY FILE ( NAME = ''' + old_name + ''', NEWNAME = ''' + new_name + ''' )' AS command FROM FileNames;
