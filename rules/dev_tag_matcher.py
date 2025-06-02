class DevTagMatcher:
    def __init__(self):
        self.dev_tags = {
            "Spring Boot", "JPA", "TypeScript", "JavaScript", "React",
            "Next.js", "MyBatis", "Django", "Flask", "PyTorch",
            "TensorFlow", "GraphQL", "REST API", "OAuth2", "Kafka"
        }

    def extract(self, text: str) -> list:
        return [tag for tag in self.dev_tags if tag.lower() in text.lower()]
