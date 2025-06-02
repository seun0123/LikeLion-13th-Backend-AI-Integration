from app.models.general_model import GeneralKeywordGenerator
from app.rules.dev_tag_matcher import DevTagMatcher
from app.utils.tag_merger import merge_tags

class TagRecommenderService:
    def __init__(self):
        self.general_model = GeneralKeywordGenerator()
        self.dev_matcher = DevTagMatcher()

    def recommend_tags(self, content: str) -> list:
        general_tags = self.general_model.extract(content)
        dev_tags = self.dev_matcher.extract(content)
        return merge_tags(general_tags, dev_tags)
