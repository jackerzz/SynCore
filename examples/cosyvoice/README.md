# CosyVoice2：具有大型语言模型的可扩展流式语音合成

## 依赖安装
```
conda install -c conda-forge pynini=2.1.5

pip install -q -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com
pip install matcha-tts
pip install ttsfrd_dependency-0.1-py3-none-any.whl
pip install ttsfrd-0.4.2-cp310-cp310-linux_x86_64.whl


```
## 下载模型
```
huggingface-cli download FunAudioLLM/CosyVoice-300M --quiet --local-dir /Users/zhouzhikai/autoTest/ray-cluster/app/data
```
## 参考资料
- [CosyVoice 2：具有大型语言模型的可扩展流式语音合成](https://funaudiollm.github.io/cosyvoice2/)
- [CosyVoice: github](https://github.com/FunAudioLLM/CosyVoice)