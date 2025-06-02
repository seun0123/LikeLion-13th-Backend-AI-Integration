from models.general_model import GeneralKeywordGenerator
from rules.dev_tag_matcher import DevTagMatcher
from utils.tag_merger import merge_tags

def recommend_tags(text: str):
    general_model = GeneralKeywordGenerator()
    dev_matcher = DevTagMatcher()

    general_tags = general_model.extract(text)
    dev_tags = dev_matcher.extract(text)

    final_tags = merge_tags(general_tags, dev_tags)
    return final_tags

