# Jarvis-using-VLM-Vision-Language-Chatbot-
A fun experiment with Qwen2-VL-2B-Instruct and text to speech Jarvis voice python module. To chat with it normally, you can ask anything (works as text-to-text) and if want to trigger its vision capability you need to write keyword "see" in input prompt. 
![vlm_chatbot](https://github.com/user-attachments/assets/b684d096-2b93-4421-9c98-6e9908b703f6)

![vlm drawio](https://github.com/user-attachments/assets/5cd1a6d2-45fc-472b-98de-ca557be037b4)

Steps to use it:

0. Install the vllm requirements on the server on which you are going to run the VLM model. Install requirements.txt on the machine on which you want to run the app.

1. Host the VLM using vllm, I have used Qwen2-VL-2B-Instruct which is one of the smallest VLMs. Following is the command that I used. You may need to change it as you change the model.

CUDA_VISIBLE_DEVICES=1 vllm serve Qwen/Qwen2-VL-2B-Instruct --host X.X.X.X --port 8080 --gpu-memory-utilization 0.95 --trust-remote-code --download_dir /path/to/save_model/qwen_vl_2b  --limit-mm-per-prompt image=1 --max-model-len 4000 --max-num-seqs 4 --enforce-eager --dtype=half

2. Set the config file as per the model, you can play with the prompt as well. Put the right details about the vllm server like host machine address and port used in above step.

3. Run the chat_app_video.py to start the app!

To use normal chat (text-to-text) you can type in text and get the response in Jarvis voice! If you want to ask about visual information that camera gets at the moment of asking question, you must add keyword "see" in the query. Like "What do you see?", "From the feed you see, how many people are there?", etc. Feel free to add in Speech-to-text and tool calling as well (I doubt if we can use tool calling with great accuracy with Qwen2-VL-2B). Cheers! 

