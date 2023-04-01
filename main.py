import util

import speech_recognition as sr
import whisper
import os
import torch
import numpy as np
import openai
from gtts import gTTS
import playsound


class ChatApp:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.messages = [
            {"role": "system", "content": "당신은 지금부터 일본어 선생님입니다. 저와 가벼운 대화를 하면서 자연스럽게 일본어를 익히도록 도와주세요. 항상 다음 형식에 따라 말씀해 주세요.\n\n---\n\n<일본어>(<일본어 문장을 한국어로 번역>)\n\n---\n\n먼저 인사를 건네고, 일상적인 질문으로 대화를 이끌어 주세요."},
        ]


    def chat(self, message):
        self.messages.append({"role": "user", "content": message})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        
        memory = 10
        if len(self.messages) > memory:
            self.messages = [self.messages[0]] + self.messages[1 - memory : -1]
        self.messages.append({"role": "assistant", "content": response["choices"][0]["message"].content})
        return self.extract_contents(response["choices"][0]["message"]["content"])


    def extract_contents(self, text):
        lines = text.strip().split('\n')
        contents = {}
        current_key = "UNK"
    
        for line in lines:
            if '(' in line:
                contents["JA"], contents["KO"] = line.rstrip(')').split('(')
            elif util.contains_japanese(line):
                contents["JA"] = line
            elif util.contains_korean(line):
                contents["KO"] = line
            else:
                contents["UNK"] = line
    
        return contents


    def speak(self, answer):
        def play(text, lang):
            tts = gTTS(text, lang=lang)
            filename = "speaking.mp3"
            tts.save(filename)
            playsound.playsound(filename)
            os.remove(filename)
        
        if 'JA' in answer and 'KO' in answer:
            print(f"先生: {answer['JA']} (선생님: {answer['KO']})")
            play(answer['JA'], 'ja')
        elif 'JA' in answer:
            print(f"先生: {answer['JA']}")
            play(answer['JA'], 'ja')
        elif 'KO' in answer:
            print('선생님: ' + answer['KO'])
        elif 'UNK' in answer:
            print('선생님: ' + answer['UNK'])
        else:
            pass

        print('')
    
    
    def listen(self):
        r = sr.Recognizer()
        r.energy_threshold = 300
        r.pause_threshold = 1.8 
        r.dynamic_energy_threshold = False
    
        with sr.Microphone(sample_rate=16000) as source:
            audio_model = whisper.load_model("base")
            print("(말씀하세요)", end='\r')

            audio = r.listen(source)
            audio_data = torch.from_numpy(np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
            result = audio_model.transcribe(audio_data, fp16=False)
    
            print(' ' * len("(말씀하세요)"), end='\r')
            return result["text"]


def main():

    app = ChatApp()
    tutors_word = app.chat('')
    app.speak(tutors_word)

    while True:
        my_word = app.listen()
        print('나: ' + my_word + '\n')
        if my_word.strip() == 'Exit' or my_word.strip() == '종료':
            print('프로그램을 종료합니다.')
            break

        tutors_word = app.chat(my_word)
        app.speak(tutors_word)

main()

