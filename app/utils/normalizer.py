from konlpy.tag import Okt
from typing import List, Set

okt = Okt()

def _is_dev_term(tag: str) -> bool:
    """개발 용어인지 확인"""
    dev_terms = {
        "Spring Boot", "JPA", "React", "Next.js", "Django", "Flask",
        "PyTorch", "TensorFlow", "Node.js", "Express", "Vue.js", "Angular",
        "Python", "Java", "JavaScript", "TypeScript", "Go", "Rust", "C++", "Kotlin",
        "REST API", "GraphQL", "OAuth2", "JWT", "Docker", "Kubernetes",
        "CI/CD", "Git", "AWS", "Azure", "GCP", "MongoDB", "Redis", "MySQL",
        "PostgreSQL", "Kafka", "RabbitMQ", "WebSocket", "gRPC"
    }
    return tag in dev_terms

def normalize_tags(tags: List[str]) -> List[str]:
    normalized: Set[str] = set()
    
    for tag in tags:
        # 개발 용어는 그대로 유지
        if _is_dev_term(tag):
            normalized.add(tag)
            continue
            
        # 일반 키워드는 명사 추출
        nouns = okt.nouns(tag)
        if nouns:
            # 2음절 이상의 명사만 추가
            normalized.update(noun for noun in nouns if len(noun) >= 2)
    
    return sorted(normalized)
