"""Tjost helper functions"""


def deep_merge(dict1, dict2) -> dict:
    """
    Merge two dictionaries, including nested dictionaries.

    :param dict1: The first dictionary.
    :param dict2: The second dictionary.
    :return: The merged dictionary.
    """
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result:
            if isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = deep_merge(result[key], value)
            else:
                result[key] = value
        else:
            result[key] = value
    return result
