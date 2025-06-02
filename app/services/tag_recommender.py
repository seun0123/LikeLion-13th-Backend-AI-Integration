from app.models.general_model import GeneralKeywordGenerator
from app.models.fallback_keybert import FallbackKeyBert
from app.rules.dev_tag_matcher import DevTagMatcher
from app.utils.tag_merger import merge_tags
from app.utils.cleaner import clean_tags
from app.utils.normalizer import normalize_tags

class TagRecommenderService:
    def __init__(self):
        self.general_model = GeneralKeywordGenerator()
        self.fallback_model = FallbackKeyBert()
        self.dev_matcher = DevTagMatcher()

    def recommend_tags(self, content: str) -> list:
        general_tags = self.general_model.extract(content)
        dev_tags = self.dev_matcher.extract(content)
        fallback_tags = []

        if len(general_tags + dev_tags) < 3:
            fallback_tags = self.fallback_model.extract(content)

        merged = merge_tags(general_tags + dev_tags + fallback_tags)
        cleaned = clean_tags(merged)

        return normalize_tags(cleaned)
