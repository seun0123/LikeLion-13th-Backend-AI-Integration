def merge_tags(general_tags: list, dev_tags: list) -> list:
    combined = list(set(general_tags + dev_tags))
    return sorted(combined)
