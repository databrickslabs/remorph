def filter_list(input_list: list, remove_list: list | None) -> list:
    if remove_list:
        return filter(lambda ele: ele not in remove_list, input_list)
    else:
        return input_list
