from konlpy.tag import Okt

okt = Okt()

def normalize_tags(tags: list[str]) -> list[str]:
    normalized = []
    for tag in tags:
        nouns = okt.nouns(tag)
        if nouns:
            normalized.append(nouns[0])  # 대표 명사 하나만 사용
    return sorted(set(normalized))
