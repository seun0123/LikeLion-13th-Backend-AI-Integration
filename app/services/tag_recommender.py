from typing import List
from app.rules.dev_tag_matcher import DevTagMatcher
from app.utils.tag_merger import merge_tags
from app.utils.cleaner import clean_tags
from app.utils.normalizer import normalize_tags
from app.models.fallback_keybert import KeywordExtractor

class TagRecommenderService:
    def __init__(self):
        self.keyword_extractor = KeywordExtractor()
        self.dev_matcher = DevTagMatcher()

    def recommend_tags(self, content: str) -> List[str]:
        dev_tags = self.dev_matcher.extract(content)
        general_tags = self.keyword_extractor.extract(content, top_n=5)

        merged = merge_tags(dev_tags + general_tags)
        cleaned = clean_tags(merged)
        normalized = normalize_tags(cleaned)

        return normalized[:5]
