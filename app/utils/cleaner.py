def clean_tags(tags: list[str]) -> list[str]:
    ignore = {"extract keyphrases", "keywords", "none"}
    cleaned = []

    for tag in tags:
        tag = tag.strip().strip(".,;:").lower()

        # 중복 허용 방지용 소문자 통일
        if len(tag) >= 2 and tag not in ignore:
            # 대소문자 복구 및 공백 정리
            formatted = " ".join([w.capitalize() for w in tag.split()])
            cleaned.append(formatted)

    # 중복 제거 후 정렬
    return sorted(set(cleaned))
