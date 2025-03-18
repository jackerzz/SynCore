import ray
from ray import serve
from transformers import pipeline

@serve.deployment()
class TranslationService:
    def __init__(self):
        self.translator = pipeline("translation", model="Helsinki-NLP/opus-mt-zh-en")
    
    async def __call__(self, text: str) -> str:
        translation_text = self.translator(text)[0]["translation_text"]
        print(f"翻译后的文字: {translation_text}")
        return translation_text
    
app = TranslationService.bind()