class DevTagMatcher:
    def __init__(self):
        self.dev_tags = {
            "Spring Boot", "JPA", "React", "Next.js", "Django",
            "Flask", "PyTorch", "TensorFlow", "OAuth2", "Kafka",
            "REST API", "TypeScript", "GraphQL"
        }

    def extract(self, text: str) -> list:
        return [tag for tag in self.dev_tags if tag.lower() in text.lower()]
