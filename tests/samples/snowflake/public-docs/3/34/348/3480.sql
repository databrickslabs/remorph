CREATE TABLE <name> ... ( <col1_name> <col1_type>
                         [ , <col2_name> <col2_type> , ... ]
                         [ , { outoflineUniquePK | outoflineFK } ]
                         [ , { outoflineUniquePK | outoflineFK } ]
                         [ , ... ] )

ALTER TABLE <name> ... ADD { outoflineUniquePK | outoflineFK }