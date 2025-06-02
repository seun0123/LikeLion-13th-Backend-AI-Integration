from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class GeneralKeywordGenerator:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("MaRiOrOsSi/keyphrase-generation-t5-small-kpTimes")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("MaRiOrOsSi/keyphrase-generation-t5-small-kpTimes")

    def extract(self, text: str, max_len: int = 512) -> list:
        input_text = f"extract keyphrases: {text}"
        inputs = self.tokenizer(input_text, return_tensors="pt", truncation=True, max_length=max_len)
        outputs = self.model.generate(**inputs, max_length=64, num_beams=5, num_return_sequences=1)
        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return [tag.strip() for tag in decoded.split(";") if tag.strip()]
