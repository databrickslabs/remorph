select tag_name, tag_value, domain, object_id
from snowflake.account_usage.tag_references
where object_deleted is null
order by tag_name, domain, object_id;