# mmovd_v4 ray 分布式微服务

# 使用的语音模型

## SenseVoice-Small
```
多语言识别： 采用超过 40 万小时数据训练，支持超过 50 种语言，识别效果上优于 Whisper 模型。
富文本识别：
具备优秀的情感识别，能够在测试数据上达到和超过目前最佳情感识别模型的效果。
支持声音事件检测能力，支持音乐、掌声、笑声、哭声、咳嗽、喷嚏等多种常见人机交互事件进行检测。
高效推理： SenseVoice-Small 模型采用非自回归端到端框架，推理延迟极低，10s 音频推理仅耗时 70ms，15 倍优于 Whisper-Large。
微调定制： 具备便捷的微调脚本与策略，方便用户根据业务场景修复长尾样本问题。
服务部署： 具有完整的服务部署链路，支持多并发请求，支持客户端语言有，python、c++、html、java 与 c# 等。
```
[SenseVoice 专注于高精度多语言语音识别、情感辨识和音频事件检测](https://github.com/FunAudioLLM/SenseVoice/blob/main/README_zh.md)

## CosyVoice2：具有大型语言模型的可扩展流式语音合成

- [CosyVoice 2：具有大型语言模型的可扩展流式语音合成](https://funaudiollm.github.io/cosyvoice2/)
- [CosyVoice: github](https://github.com/FunAudioLLM/CosyVoice)

```
pip install matcha-tts
```

## FunASR: 希望在语音识别的学术研究和工业应用之间架起一座桥梁
- [FunASR: github](https://github.com/modelscope/FunASR/blob/main/README_zh.md)

## 使用的模型
- [语音模型仓库](https://github.com/modelscope/FunASR/blob/main/README_zh.md#%E6%A8%A1%E5%9E%8B%E4%BB%93%E5%BA%93)

# 检索增强生成（RAG） LlamaIndex
- [LlamaIndex](https://qwen.readthedocs.io/zh-cn/latest/framework/LlamaIndex.html)
```bash
pip install llama-index llama-index-llms-huggingface  llama-index-readers-web
```

# ray 服务部署

## 打包生成`config.yaml`
- 生成包含这两个应用程序的多应用程序配置文件并将其保存到。
```bash
serve build image_classifier:app text_translator:app -o config.yaml
```

## 启动集群
```bash
ray start --head
```

## 部署服务
```bash
serve deploy script/config.yaml
```
## serve 其他命令
```
serve status 
```
# 参考资料
- [ray multi-app deploy](https://docs.ray.io/en/releases-2.42.0/serve/multi-app.html)
- [ray multi app updates ](https://docs.ray.io/en/releases-2.42.0/serve/advanced-guides/inplace-updates.html#serve-inplace-updates)