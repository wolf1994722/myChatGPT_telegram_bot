# Telegram Bot to communicate with OpenAI API
# forked from juan-miii, modified by han3on

import logging
import autocookie
from os import environ as env
from dotenv import load_dotenv

import telebot
from openai import OpenAI


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

load_dotenv()
bot = telebot.TeleBot(env["BOT_API_KEY"])
# OpenAI.api_key = env["OPENAI_API_KEY"]
user_id = int(env["USER_KEY"])

print(user_id)


@bot.message_handler(func=lambda message: True)
def get_response(message):
  print(message.text)
  if int(message.chat.id) != user_id:
    bot.send_message("This bot is not for public but private use only.")
  else:
    client = OpenAI(
      api_key=env["OPENAI_API_KEY"]
    )
    response = ""
    
    if message.text.startswith(">>>"):
      # Use Codex API for code completion
      response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f'"""\n{message.text}\n"""',}],
        temperature=0,
        max_tokens=4000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=['"""'],
      )
      msg = response.choices[0].message.content
      
    else:
      # Use GPT API for text completion
      # Check if the question is about code or not
      if "code" in message.text.lower() or "python" in message.text.lower():
        # Use Codex API for code-related questions
        response = client.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=[{"role": "user", "content": f'"""\n{message.text}\n"""',}],
          temperature=0,
          max_tokens=4000,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0,
          stop=['"""'],
        )
        
        msg = response.choices[0].message.content
        
      elif "bard" in message.text.lower():
        print(message.text)
        msg = autocookie.chatting(message.text)
        
        
      else:
        # Use GPT API for non-code-related questions
        response = client.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=[{"role": "user", "content": f'"""\n{message.text}\n"""',}],
          temperature=0,
          max_tokens=4000,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0,
          stop=['"""'],
        )
        
        msg = response.choices[0].message.content

    bot.send_message(message.chat.id, f'{msg}', parse_mode="None")

bot.infinity_polling()