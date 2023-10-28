select
        operator_id,
        operator_attributes,
        operator_statistics:output_rows / operator_statistics:input_rows as row_multiple
    from table(get_query_operator_stats($lid))
    where operator_type = 'Join'
    order by step_id, operator_id;
