def merge_tags(general_tags: list, dev_tags: list) -> list:
    return sorted(set(general_tags + dev_tags))
