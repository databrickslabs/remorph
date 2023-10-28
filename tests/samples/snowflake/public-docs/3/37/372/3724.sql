select tag_name, tag_value, domain, object_id
from snowflake.account_usage.tag_references
order by tag_name, domain, object_id;