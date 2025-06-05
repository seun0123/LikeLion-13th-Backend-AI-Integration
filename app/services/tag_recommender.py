from typing import List, Optional
from app.rules.dev_tag_matcher import DevTagMatcher
from app.utils.tag_merger import merge_tags
from app.utils.cleaner import clean_tags
from app.utils.normalizer import normalize_tags
from app.models.fallback_keybert import KeywordExtractor
import gc

class TagRecommenderService:
    _instance: Optional['TagRecommenderService'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TagRecommenderService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.keyword_extractor = KeywordExtractor()
            self.dev_matcher = DevTagMatcher()
            self._initialized = True
    
    def recommend_tags(self, content: str) -> List[str]:
        try:
            # 입력 텍스트 전처리
            content = content.strip()
            if not content:
                return []
                
            # 개발 관련 태그 추출
            dev_tags = self.dev_matcher.extract(content)
            
            # 일반 키워드 추출
            general_tags = self.keyword_extractor.extract(content, top_n=5)
            
            # 태그 병합 및 정제
            merged = merge_tags(dev_tags + general_tags)
            cleaned = clean_tags(merged)
            normalized = normalize_tags(cleaned)
            
            # 메모리 정리
            gc.collect()
            
            return normalized[:5]
            
        except Exception as e:
            print(f"태그 추천 중 오류 발생: {e}")
            return []
            
    def cleanup(self):
        """메모리 정리를 위한 명시적인 정리 메서드"""
        gc.collect()
