select v AS hex_encoded_binary_value 
    from varbin 
    where is_binary(v);