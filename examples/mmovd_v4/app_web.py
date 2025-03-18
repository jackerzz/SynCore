from fastapi import FastAPI, HTTPException
import torch
import ray
import os
from ray import serve
from ray.serve.handle import DeploymentHandle
from fastapi.responses import JSONResponse

base_path = os.path.dirname(os.path.abspath(__file__))

print(
    f'''
    ##########################################################
            # ray 模型即服务： 对话语音服务 微服务自动伸缩 版本 v4 # 
            # base_path: {base_path}
    ##########################################################
    '''
)
app = FastAPI()
# ray.init()
# serve.start()


@serve.deployment
@serve.ingress(app)
class DAGRunner:
    def __init__(self):
        self.audio_service = serve.get_app_handle("audio_service")
        self.asr_service = serve.get_app_handle("asr_service")
        self.translation_service = serve.get_app_handle("translation_service")
        self.tts_service = serve.get_app_handle("tts_service")
        self.audio_play = serve.get_app_handle("audio_play")

    
    async def dag_flows(self,input_audio_path,output_audio_path):
        saved_path = await self.audio_service.save_audio.remote(input_audio_path)
        asr_result = await self.asr_service.remote(saved_path)
        translated_text = await self.translation_service.remote(asr_result)
        tts_output = await self.tts_service.remote(translated_text,output_audio_path)
        await self.audio_play.remote(tts_output)
        
        result = {
            "语音保存位置": saved_path,
            "语音识别内容": asr_result,
            "语音翻译英文": translated_text,
            "英文转音频路径": output_audio_path

        }
        return result
        
    @app.post("/dag/execute")
    async def execute_dag(self,input_audio_path: str = "input.wav", output_audio_path: str = "output.mp3"):
        input_data = {
            "input_audio_path": f"{base_path}/data/{input_audio_path}",
            "output_audio_path": f"{base_path}/data/{output_audio_path}"
        }        

        results = await self.dag_flows(**input_data)
        return JSONResponse({
            "status": "success",
            "results":results
        })

        
APIIngress = DAGRunner.bind()
serve.run(APIIngress)       
#python app_web.py