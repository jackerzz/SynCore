import ray
from ray import serve
from transformers import pipeline


@serve.deployment()
class ASRService:
    def __init__(self):
        self.asr = pipeline("automatic-speech-recognition", model="openai/whisper-small")
        # [SenseVoice是具有音频理解能力的音频基础模型，包括语音识别（ASR）、语种识别（LID）、语音情感识别（SER）和声学事件分类（AEC）或声学事件检测（AED）。本项目提供SenseVoice模型的介绍以及在多个任务测试集上的benchmark，以及体验模型所需的环境安装的与推理方式。](https://huggingface.co/FunAudioLLM/SenseVoiceSmall/blob/main/README_zh.md)
        # self.asr = pipeline("automatic-speech-recognition", model="FunAudioLLM/SenseVoiceSmall")
    async def __call__(self, input_path: str) -> str:
        asr_result = self.asr(input_path)
        print(f'识别出来的文字: {asr_result["text"]}')
        return asr_result["text"]
app = ASRService.bind()