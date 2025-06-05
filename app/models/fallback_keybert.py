from keybert import KeyBERT
from typing import List, Tuple
import numpy as np
from konlpy.tag import Okt
import re

class KeywordExtractor:
    def __init__(self):
        self.model = KeyBERT(model='paraphrase-multilingual-mpnet-base-v2')
        self.min_score = 0.3
        self.okt = Okt()
        
        # 조사 패턴 정의 - 더 정확한 패턴으로 개선
        self.particle_pattern = re.compile(r'(?:이?가|을?를|에서|으?로|와|과|이?랑|이?나|도|에|께|서|의|이?란)$')
        
    def _clean_word(self, word: str) -> str:
        """조사와 특수문자 제거"""
        # 조사 제거
        word = self.particle_pattern.sub('', word)
        # 특수문자 제거
        word = re.sub(r'[^\w\s]', '', word)
        return word.strip()
        
    def _extract_nouns(self, text: str) -> List[str]:
        # 텍스트 정규화
        normalized = self.okt.normalize(text)
        
        # 품사 태깅
        tagged = self.okt.pos(normalized, stem=True)
        
        # 제외할 단어들 (불용어)
        stop_words = {
            # 부사
            '정말', '매우', '너무', '아주', '잘', '곧', '참', '자주', '이제', '계속', '다시', '이미', '벌써',
            # 동사/형용사 활용형으로 자주 쓰이는 단어
            '타고', '보고', '먹고', '가고', '오고', '되고', '하고', '했어요', '합니다', '입니다',
            # 기타 불용어
            '그것', '이것', '저것', '그런', '이런', '저런', '이번', '다음',
            # 개발 관련 불용어
            '활용', '사용', '통해', '위해',
            # 시간 관련 불용어
            '오늘', '내일', '모레', '어제', '그제', '지금'
        }
        
        nouns = []
        for word, pos in tagged:
            if pos == 'Noun':
                # 불용어 체크
                if word not in stop_words:
                    # 동사/형용사 활용형 체크
                    if not word.endswith(('하다', '되다', '있다', '없다', '요', '죠', '네', '데', '게')):
                        # 조사/어미 체크
                        if not (len(word) <= 2 and word.endswith(('이', '것', '수', '데', '말'))):
                            # 조사 제거
                            cleaned_word = self._clean_word(word)
                            if len(cleaned_word) >= 2:
                                nouns.append(cleaned_word)
        
        return sorted(set(nouns))
        
    def extract(self, text: str, top_n: int = 10, diversity: float = 0.3) -> List[str]:
        # 메모리 사용량 감소를 위해 n-gram 범위를 (1, 1)로 제한
        keywords = self.model.extract_keywords(
            text,
            keyphrase_ngram_range=(1, 1),  # 단일 단어만 추출
            stop_words='english',
            top_n=min(top_n, 20),  # 최대 20개로 제한
            diversity=diversity,
            use_maxsum=True,
        )
        
        cleaned_keywords = set()
        for keyword, score in keywords:
            if score >= self.min_score:
                nouns = self._extract_nouns(keyword)
                cleaned_keywords.update(nouns)
                    
        return sorted(cleaned_keywords)

    def extract_with_scores(self, text: str, top_n: int = 10) -> List[Tuple[str, float]]:
        keywords = self.model.extract_keywords(
            text,
            keyphrase_ngram_range=(1, 1),
            stop_words='english',
            top_n=min(top_n, 20)
        )
        
        cleaned_keywords = []
        for keyword, score in keywords:
            if score >= self.min_score:
                nouns = self._extract_nouns(keyword)
                cleaned_keywords.extend((noun, score) for noun in nouns)
                    
        return sorted(set(cleaned_keywords), key=lambda x: x[1], reverse=True)
