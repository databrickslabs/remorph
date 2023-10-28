UPDATE jdemo2 SET
    variant1 = PARSE_JSON(varchar1),
    variant2 = TO_VARIANT(varchar1);