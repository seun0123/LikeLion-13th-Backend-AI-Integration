from konlpy.tag import Okt
import re

class DevTagMatcher:
    def __init__(self):
        self.dev_tags = {
            # 프레임워크/라이브러리
            "Spring Boot", "JPA", "React", "Next.js", "Django", "Flask",
            "PyTorch", "TensorFlow", "Node.js", "Express", "Vue.js", "Angular",
            # 언어
            "Python", "Java", "JavaScript", "TypeScript", "Go", "Rust", "C++", "Kotlin",
            # 기술/개념
            "REST API", "GraphQL", "OAuth2", "JWT", "Docker", "Kubernetes",
            "CI/CD", "Git", "AWS", "Azure", "GCP", "MongoDB", "Redis", "MySQL",
            "PostgreSQL", "Kafka", "RabbitMQ", "WebSocket", "gRPC",
            # AI/ML
            "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
            "Transformer", "BERT", "GPT", "CNN", "RNN", "LSTM"
        }
        self.okt = Okt()
        
    def _normalize_text(self, text: str) -> str:
        # 특수문자 처리 (점, 공백 등 정규화)
        text = re.sub(r'[.]\s*', '.', text)  # 점과 공백 정규화
        text = re.sub(r'\s+', ' ', text)     # 다중 공백 정규화
        return text.strip()
        
    def _remove_korean_postpositions(self, text: str) -> str:
        # 흔한 조사 패턴 제거
        postpositions = [
            r'이?[가]\\b', r'을?[를]\\b', r'[은는]\\b', r'[과와]\\b',
            r'[으]?로\\b', r'[에서]\\b', r'[에]\\b', r'[의]\\b'
        ]
        for pp in postpositions:
            text = re.sub(pp, '', text)
        return text

    def extract(self, text: str) -> list:
        text = self._normalize_text(text)
        # 명사 추출
        nouns = set(self.okt.nouns(text))
        
        # 전처리된 텍스트 생성 (조사 제거)
        processed_text = self._remove_korean_postpositions(text.lower())
        
        matched = []
        for tag in self.dev_tags:
            tag_lower = tag.lower()
            # 1. 정확한 매칭
            if tag_lower in processed_text:
                matched.append(tag)
                continue
                
            # 2. 명사 기반 매칭
            tag_nouns = set(self.okt.nouns(tag))
            if tag_nouns & nouns:
                matched.append(tag)
                continue
                
            # 3. 부분 문자열 매칭 (약어 및 변형 처리)
            tag_parts = tag_lower.split()
            if any(part in processed_text for part in tag_parts):
                matched.append(tag)

        return sorted(set(matched))
