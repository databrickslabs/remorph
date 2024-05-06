def alias_column_str(alias: str, columns: list[str]) -> list[str]:
    return [f"{alias}.{column}" for column in columns]
