from keybert import KeyBERT
from typing import List, Tuple
import numpy as np
from konlpy.tag import Okt

class KeywordExtractor:
    def __init__(self):
        # 다국어 지원을 위한 모델 선택
        self.model = KeyBERT(model='paraphrase-multilingual-mpnet-base-v2')
        self.min_score = 0.3  # 최소 유사도 점수
        self.okt = Okt()
        
    def _extract_nouns(self, text: str) -> List[str]:
        """명사만 추출"""
        # 텍스트 정규화 (이모티콘, 반복 문자 등 처리)
        normalized = self.okt.normalize(text)
        
        # 품사 태깅 후 의미있는 명사만 추출
        tagged = self.okt.pos(normalized, stem=True)
        
        # 제외할 단어들
        stop_words = {'정말', '매우', '너무', '아주', '잘', '곧', '참', '자주', '이제', '계속', '다시', '이미', '벌써'}
        
        nouns = [word for word, pos in tagged 
                if (pos == 'Noun'  # 일반 명사
                    and not word.endswith(('요', '죠', '네', '데', '게'))  # 동사/형용사 활용형 제외
                    and not (len(word) <= 2 and word.endswith(('이', '것', '수', '데', '말')))  # 조사/어미로 쓰이는 짧은 단어 제외
                    and word not in stop_words  # 불용어 제외
                    and len(word) >= 2)]  # 2글자 이상
        
        return sorted(set(nouns))  # 중복 제거 및 정렬
        
    def extract(self, text: str, top_n: int = 10, diversity: float = 0.3) -> List[str]:
        # 키워드 추출 with MMR (Maximal Marginal Relevance)
        keywords = self.model.extract_keywords(
            text,
            keyphrase_ngram_range=(1, 2),  # 1-2개 단어 키워드 추출
            stop_words='english',  # 영어 불용어 제거
            top_n=top_n,
            diversity=diversity,  # MMR diversity 파라미터
            use_maxsum=True,  # MaxSum 알고리즘 사용
        )
        
        # 키워드에서 명사만 추출
        cleaned_keywords = set()
        for keyword, score in keywords:
            if score >= self.min_score:
                nouns = self._extract_nouns(keyword)
                cleaned_keywords.update(nouns)
                    
        return sorted(cleaned_keywords)

    def extract_with_scores(self, text: str, top_n: int = 10) -> List[Tuple[str, float]]:
        """스코어와 함께 키워드 반환 (디버깅용)"""
        keywords = self.model.extract_keywords(
            text,
            keyphrase_ngram_range=(1, 2),
            stop_words='english',
            top_n=top_n
        )
        
        cleaned_keywords = []
        for keyword, score in keywords:
            if score >= self.min_score:
                nouns = self._extract_nouns(keyword)
                cleaned_keywords.extend((noun, score) for noun in nouns)
                    
        return sorted(set(cleaned_keywords), key=lambda x: x[1], reverse=True)
