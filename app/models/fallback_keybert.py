from keybert import KeyBERT

class FallbackKeyBert:
    def __init__(self):
        self.model = KeyBERT(model="distiluse-base-multilingual-cased-v1")

    def extract(self, text: str, top_n: int = 5):
        keywords = self.model.extract_keywords(text, top_n=top_n, stop_words='english')
        return [kw for kw, _ in keywords]
