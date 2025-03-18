import os
import torch
from cosyvoice.cli.cosyvoice import CosyVoice, CosyVoice2
from cosyvoice.utils.file_utils import load_wav
from modelscope import snapshot_download
from ray import serve
import numpy as np
# 改成全局配置
base_path = os.path.dirname(os.path.abspath(__file__))
model_dir=f"{base_path}/pretrained_models/CosyVoice-300M"

def generate_data(model_output):
    for i in model_output:
        tts_audio = (i['tts_speech'].numpy() * (2 ** 15)).astype(np.int16).tobytes()
        yield tts_audio

@serve.deployment()
class CosyvoiceService:
    def __init__(self):
        self.clear()
        try:
            self.cosyvoice = CosyVoice(model_dir)
        except Exception:
            try:
                self.cosyvoice = CosyVoice2(model_dir)
            except Exception:
                raise TypeError('no valid model_type!')
    
    async def __call__(self, text: str) -> str:
        translation_text = self.translator(text)[0]["translation_text"]
        print(f"翻译后的文字: {translation_text}")
        return translation_text
    
    async def clear(self,):
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    
    async def download_models(self,):
        # snapshot_download('iic/CosyVoice2-0.5B', local_dir='pretrained_models/CosyVoice2-0.5B')
        snapshot_download('iic/CosyVoice-300M', local_dir=model_dir)
        # snapshot_download('iic/CosyVoice-300M-25Hz', local_dir='pretrained_models/CosyVoice-300M-25Hz')
        # snapshot_download('iic/CosyVoice-300M-SFT', local_dir='pretrained_models/CosyVoice-300M-SFT')
        # snapshot_download('iic/CosyVoice-300M-Instruct', local_dir='pretrained_models/CosyVoice-300M-Instruct')
        # snapshot_download('iic/CosyVoice-ttsfrd', local_dir='pretrained_models/CosyVoice-ttsfrd')
    
    async def inference_sft(self,tts_text, spk_id):
        model_output = self.cosyvoice.inference_sft(tts_text, spk_id)
        return model_output
    
    async def inference_zero_shot(self,tts_text, prompt_text, prompt_speech_16k):
        model_output = self.cosyvoice.inference_zero_shot(tts_text, prompt_text, prompt_speech_16k)
        return model_output
    
    async def inference_cross_lingual(self,tts_text, prompt_speech_16k):
        model_output = self.cosyvoice.inference_cross_lingual(tts_text, prompt_speech_16k)
        return model_output
    
    async def inference_instruct(self,tts_text, spk_id, instruct_text):
        model_output = self.cosyvoice.inference_instruct(tts_text, spk_id, instruct_text)
        return model_output
    
    async def inference_instruct(self,tts_text, instruct_text, prompt_speech_16k):
        model_output = self.cosyvoice.inference_instruct2(tts_text, instruct_text, prompt_speech_16k)
        return model_output
    
        
app = CosyvoiceService.bind()