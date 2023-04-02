from util import *
import datetime
import re

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

        instruction = f"당신은 지금부터 일본어 선생님입니다. 저와 가벼운 대화를 하면서 자연스럽게 일본어를 익히도록 도와주세요. 지금은 {formatted_time()}입니다. 먼저 인사를 건네고, 일상적인 질문으로 대화를 이끌어 주세요."
        self.messages = [
            {"role": "system", "content": self.translate(instruction, 'JA')},
        ]


    def chat(self, message):
        self.messages.append({"role": "user", "content": message})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        
        memory = 7 
        if len(self.messages) > memory:
            self.messages = [self.messages[0]] + self.messages[1 - memory : -1]
        self.messages.append({"role": "assistant", "content": response["choices"][0]["message"].content})
        return response["choices"][0]["message"]["content"]


    def translate(self, text, lang):
        prompt = f'Translate into {lang}:\n\n{text}'

        response = openai.Completion.create(
          model="text-davinci-003",
          prompt=prompt,
          temperature=0.3,
          max_tokens=1000,
          top_p=1.0,
          frequency_penalty=0.0,
          presence_penalty=0.0
        )
        return response['choices'][0]['text'].strip()


    def speak(self, text):
        tts = gTTS(text, lang='ja')
        filename = "speaking.mp3"
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)
    
    
    def listen(self):
        r = sr.Recognizer()
        r.energy_threshold = 300
        r.pause_threshold = 1.8 
        r.dynamic_energy_threshold = False
    
        with sr.Microphone(sample_rate=16000) as source:
            audio_model = whisper.load_model("base")
            prmpt = "(말씀하세요)"
            print(prmpt, end='\r')

            audio = r.listen(source)
            audio_data = torch.from_numpy(np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
            text = audio_model.transcribe(audio_data, fp16=False)["text"]
    
            print(' ' * (len(prmpt) + 3), end='\r')
            return text.ljust(len(prmpt))


def main():

    app = ChatApp()
    tutors_word = app.chat('')
    print('先生: ' + tutors_word)
    app.speak(tutors_word)
    print('선생님: ' + app.translate(tutors_word, 'KO') + '\n')

    while True:
        my_word = app.listen().lstrip()
        
        print('나: ' + my_word + '\n')

        graceful_exit = 0
        if re.search('さようなら|おやすみなさい|お休みなさい', my_word):
            graceful_exit = 2

        tutors_word = app.chat(my_word)
        print('先生: ' + tutors_word)
        app.speak(tutors_word)
        print('선생님: ' + app.translate(tutors_word, 'KO') + '\n')

        if graceful_exit:
            graceful_exit -= 1
            if re.search('さようなら|またいつかお話しましょう|また今度お話しましょうね|おやすみなさい|お休みなさい', tutors_word):
                print('프로그램을 종료합니다.')
                break

main()

