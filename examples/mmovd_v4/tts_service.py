import ray
from ray import serve
import torch
from transformers import pipeline
from pydub import AudioSegment
import numpy as np

@serve.deployment()
class TTSService:
    def __init__(self):
        self.tts = pipeline("text-to-speech", model="facebook/mms-tts-eng",device="cpu")
    
    async def __call__(self, text: str,output_audio_path:str) -> bytes:
        output = self.tts(text)
        audio = (output["audio"] * 32767).astype(np.int16)
        # print("[Debug] 数据类型:", audio.dtype)
        # print("[Debug] 最大值:", np.max(audio))
        # print("[Debug] 最小值:", np.min(audio))
        # print("[Debug] NaN检查:", np.isnan(audio).any())
        # print("[Debug] Inf检查:", np.isinf(audio).any())
        audio_segment = AudioSegment(
            audio.tobytes(),
            frame_rate=16000,
            sample_width=2,
            channels=1
        )
        audio_segment.export(output_audio_path, format="mp3")
        return audio_segment
app = TTSService.bind()