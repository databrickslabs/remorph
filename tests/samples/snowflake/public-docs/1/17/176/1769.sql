select v, v regexp '.*\\s\\\\.*' AS MATCHES
    from strings
    order by v;