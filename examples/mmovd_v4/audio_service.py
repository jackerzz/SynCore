import ray
import queue
import time
import sounddevice as sd
import numpy as np
import soundfile as sf
from ray import serve


@serve.deployment()
class AudioService:
    async def save_audio(self, input_audio_path: str) -> str:
        q = queue.Queue()
        def callback(indata, frames, time_info, status):
            if status:
                print(status, flush=True)
            q.put(indata.copy())

        samplerate = 16000
        duration = 10
        print(input_audio_path)
        print("请开始说话... ")
        audio_chunks = []
        with sd.InputStream(samplerate=samplerate, channels=1, callback=callback):
            start_time = time.time()
            while time.time() - start_time < duration:
                audio_chunks.append(q.get())
        audio_data = np.concatenate(audio_chunks, axis=0)
        
        sf.write(input_audio_path, audio_data, samplerate)
        print(f"录音完成，已保存到 {input_audio_path}")
        return input_audio_path
    
app = AudioService.bind()