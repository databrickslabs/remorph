from typing import Optional


def filter_list(input_list: list, remove_list: Optional[list]) -> list:
    if remove_list:
        return filter(lambda ele: ele not in remove_list, input_list)
    else:
        return input_list
