from keybert import KeyBERT
from typing import List

class LightweightKeywordExtractor:
    def __init__(self):
        self.model = KeyBERT(model="paraphrase-MiniLM-L6-v2")
        self.stopwords = {
            "정말", "매우", "너무", "아주", "잘", "곧", "참", "자주", "이제", "계속", "다시", "이미", "벌써",
            "타고", "보고", "먹고", "가고", "오고", "되고", "하고",
            "그것", "이것", "저것", "그런", "이런", "저런", "이번", "다음"
        }

    def extract(self, text: str, top_n: int = 10) -> List[str]:
        keywords = self.model.extract_keywords(
            text,
            keyphrase_ngram_range=(1, 2),
            stop_words="english",
            top_n=top_n,
            use_maxsum=True,
            diversity=0.3
        )
        cleaned = set()
        for word, score in keywords:
            word = word.strip().lower()
            if len(word) >= 2 and word not in self.stopwords:
                cleaned.add(word)
        return sorted(cleaned)

class TagRecommenderService:
    def __init__(self):
        self.keyword_extractor = LightweightKeywordExtractor()

    def recommend_tags(self, content: str) -> List[str]:
        return self.keyword_extractor.extract(content, top_n=5)
