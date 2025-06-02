from app.models.general_model import GeneralKeywordGenerator
from app.models.fallback_keybert import KeywordExtractor
from app.rules.dev_tag_matcher import DevTagMatcher
from app.utils.tag_merger import merge_tags
from app.utils.cleaner import clean_tags
from app.utils.normalizer import normalize_tags
from typing import List, Dict

class TagRecommenderService:
    def __init__(self):
        self.keyword_extractor = KeywordExtractor()
        self.dev_matcher = DevTagMatcher()

    def recommend_tags(self, content: str) -> List[str]:
        print(f"[입력] {content}")
        
        # 1. 개발 용어 매칭 (정확도 높은 매칭 우선)
        dev_tags = self.dev_matcher.extract(content)
        print(f"[개발용어] {dev_tags}")
        
        # 2. 일반 키워드 추출 (KeyBERT)
        general_tags = self.keyword_extractor.extract(content, top_n=5)
        print(f"[일반키워드] {general_tags}")
        
        # 3. 태그 병합 및 정제
        merged = merge_tags(dev_tags + general_tags)
        cleaned = clean_tags(merged)
        normalized = normalize_tags(cleaned)
        
        # 4. 최종 결과 반환 (최대 5개)
        return normalized[:5]
        
    def recommend_tags_with_metadata(self, content: str) -> Dict:
        """디버깅을 위한 메타데이터 포함 버전"""
        dev_tags = self.dev_matcher.extract(content)
        general_tags_with_scores = self.keyword_extractor.extract_with_scores(content)
        
        merged = merge_tags(dev_tags + [tag for tag, _ in general_tags_with_scores])
        cleaned = clean_tags(merged)
        normalized = normalize_tags(cleaned)
        
        return {
            "final_tags": normalized[:5],
            "dev_tags": dev_tags,
            "general_tags": general_tags_with_scores,
            "raw_merged": merged,
            "cleaned": cleaned
        }
