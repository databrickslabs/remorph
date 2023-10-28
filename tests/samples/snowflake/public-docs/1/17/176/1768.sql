select v, v regexp 'San\\b.*' AS MATCHES
    from strings
    order by v;