from typing import List, Tuple
from konlpy.tag import Okt
import re
import gc

class KeywordExtractor:
    def __init__(self):
        self.okt = Okt(jvmpath=None)  # JVM 메모리 사용량 최적화
        
        # 조사 패턴 정의
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
            '내일', '모레', '어제', '그제', '지금'
        }
        
        # 중요 키워드 가중치
        important_words = {
            '부모님': 1.0, '가족': 1.0, '친구': 1.0,
            '회사': 1.0, '학교': 1.0, '직장': 1.0,
            '운동': 0.9, '공부': 0.9, '취미': 0.9,
            '여행': 0.9, '음식': 0.9, '영화': 0.9,
            '책': 0.9, '음악': 0.9, '게임': 0.9,
        }
        
        word_scores = {}
        for word, pos in tagged:
            if pos in ('Noun', 'Verb', 'Adjective'):
                if word not in stop_words:
                    if not word.endswith(('요', '죠', '네', '게')):
                        if not (len(word) <= 2 and word.endswith(('이', '것', '수', '데', '말'))):
                            cleaned_word = self._clean_word(word)
                            if len(cleaned_word) >= 2:
                                # 중요 키워드는 가중치 부여
                                score = important_words.get(cleaned_word, 0.5)
                                # 명사는 추가 가중치
                                if pos == 'Noun':
                                    score += 0.3
                                word_scores[cleaned_word] = score
        
        # 상위 점수 키워드 선택
        sorted_words = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)
        return [word for word, _ in sorted_words]
        
    def extract(self, text: str, top_n: int = 10) -> List[str]:
        try:
            nouns = self._extract_nouns(text)
            # 메모리 정리
            gc.collect()
            return nouns[:top_n]
        except Exception as e:
            print(f"키워드 추출 중 오류 발생: {e}")
            return []

    def extract_with_scores(self, text: str, top_n: int = 10) -> List[Tuple[str, float]]:
        try:
            nouns = self._extract_nouns(text)
            # 단순 순서 기반 점수 부여
            scored = [(noun, 1.0 - (i * 0.1)) for i, noun in enumerate(nouns)]
            # 메모리 정리
            gc.collect()
            return scored[:top_n]
        except Exception as e:
            print(f"키워드 추출 중 오류 발생: {e}")
            return []
