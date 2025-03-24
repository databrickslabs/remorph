--- Storage

SELECT pdw_node_id as node_id,
       (sum(reserved_page_count) * 8) / 1024 as ReservedSpaceMB,
       (sum(used_page_count)  * 8) / 1024 as UsedSpaceMB,
       CURRENT_TIMESTAMP as extract_ts
FROM SYS.DM_PDW_NODES_DB_PARTITION_STATS
group by pdw_node_id
