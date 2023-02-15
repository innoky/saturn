import telebot

import openai

# Load secrets
openai.api_key = "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"

# Create telebot object
bot = telebot.TeleBot("6010226043:AAGKtq_B73MFUjbCFL8v0yDVeoudxWI0IEw")

@bot.message_handler(commands=["start"])
def start(message):
     bot.send_message(message.chat.id, 'Здравствуй, я - Saturn, telegram бот на базе нейросети ChatGpt3. \n\nПопросите у меня написать код программы на Python по описанию или придумать сочинение на тему: «Мораль мультисериала Щенячий патруль».')
# Create function to generate response to message
def generate_response(message):
    prompt = message.text
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=1024,
        n=1,
        stop=None,
        timeout=20,
    )
    return response.choices[0].text

# Define handler for incoming messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_message(message.chat.id, 'Подождите... Сигнал летит до Сатурна')
    response = generate_response(message)
    bot.reply_to(message, response)

# Start bot
bot.polling()
