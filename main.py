import telebot
from telebot import types

from subprocess import Popen
from speech_recognition import (Recognizer, AudioFile)
from speech_recognition import (UnknownValueError, RequestError)
import speech_recognition as sr
import soundfile as sf

import openai
import os
import os.path



class SpeechOggAudioFileToText:
    def __init__(self):
        self.recognizer = Recognizer()

    def ogg_to_wav(self, file):
        args = ['ffmpeg','-i', file, 'test.wav']
        process = Popen(args)
        process.wait()
        return 'test.wav'

    @property
    def text(self):
        files = os.listdir(os.curdir)
        AUDIO_FILE = self.ogg_to_wav(files[-1])
        with AudioFile(AUDIO_FILE) as source:
            audio = self.recognizer.record(source)
        try:
            text = self.recognizer.recognize_google(audio, language='RU')
            return text
        except UnknownValueError:
            print("Не удаётся распознать аудио файл")
        except RequestError as error:
            print("Не удалось запросить результаты: {0}".format(error))

openai.api_key = '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'
bot = telebot.TeleBot('6010226043:AAGKtq_B73MFUjbCFL8v0yDVeoudxWI0IEw')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Здравствуй, я - Saturn, telegram бот на базе нейросети ChatGpt3. \n\nПопросите у меня написать код программы на Python по описанию или придумать сочинение на тему: «Мораль мультисериала Щенячий патруль». \n\nТакже я умею распозновать голосовые сообщения.')

@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == "private":
        bot.send_message(message.chat.id, "Запрос отправлен, подождите... До Сатурна сигналу долго лететь")
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message.text,
        temperature=0.9,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=["You:"]
    )
        bot.send_message(message.chat.id, response['choices'][0]['text'])

@bot.message_handler(content_types=['voice'])

def voice_processing(message):
    file_info = bot.get_file(message.voice.file_id)
    user_id = message.from_user.id
    downloaded_file = bot.download_file(file_info.file_path)
    files = os.listdir(os.curdir)
    with open(str(user_id) + str(len(files)) +'.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)


    speech_ogg = SpeechOggAudioFileToText()
    speech_ogg.ogg_to_wav(str(user_id) + str(len(files)) +'.ogg')

    bot.send_message(message.chat.id, "Запрос отправлен, подождите... До Сатурна сигналу долго лететь")
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=speech_ogg.text,
    temperature=0.9,
    max_tokens=1000,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.6,
    stop=["You:"]
)
    bot.send_message(message.chat.id, response['choices'][0]['text'])


bot.polling(none_stop=True)
