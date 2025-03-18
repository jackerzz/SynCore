import ray
from ray import serve
from pydub.playback import play

@serve.deployment
class AudioPlayService:
    async def __call__(self, audio_segment) -> dict:
        print("播放回复语音...")
        play(audio_segment)
        print("播放结束。")

app = AudioPlayService.bind()