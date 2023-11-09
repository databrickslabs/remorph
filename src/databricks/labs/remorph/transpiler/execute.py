from databricks.labs.remorph.helpers.execution_time import timeit


@timeit
def morph(
    source,
    input_sql,
    output_folder,
    skip_validation="false",
    validation_mode="LOCAL_REMOTE",
    catalog_nm="transpiler_test",
    schema_nm="convertor_test",
):
    # Ignore T201
    print(source)  # noqa: T201
    print(input_sql)  # noqa: T201
    print(output_folder)  # noqa: T201
    print(skip_validation)  # noqa: T201
    print(validation_mode)  # noqa: T201
    print(catalog_nm)  # noqa: T201
    print(schema_nm)  # noqa: T201
    pass
