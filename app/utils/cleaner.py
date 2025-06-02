def clean_tags(tags: list[str]) -> list[str]:
    ignore = {"extract keyphrases", "keywords", "none"}
    cleaned = []

    # 1차 정제: 불용어 제거, 소문자화, 기호 제거
    for tag in tags:
        tag = tag.strip().strip(".,;:").lower()
        if len(tag) >= 2 and tag not in ignore:
            formatted = " ".join([w.capitalize() for w in tag.split()])
            cleaned.append(formatted)

    # 중복 제거
    unique_tags = sorted(set(cleaned))

    # 복합태그 제거: 기존 단일 태그의 조합만으로 된 복합어는 제거
    base_words = set()
    for tag in unique_tags:
        if len(tag.split()) == 1:
            base_words.add(tag.lower())

    final_tags = []
    for tag in unique_tags:
        words = tag.lower().split()
        if len(words) == 1:
            final_tags.append(tag)
        else:
            if not all(word in base_words for word in words):
                final_tags.append(tag)

    return final_tags
