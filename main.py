# before starting, you need to change the settings.py file (add the necessary tokens, etc.)

import settings
from gpt import ChatGPT

import os # check path exists and remove path
import json # load and dumps chats histories
import telebot # telegram bot library


# bot initialization
bot=telebot.TeleBot(settings.BOT_API_TOKEN)

# class with assistant init
assistant = ChatGPT(settings.OPENAI_API_KEY, settings.ORG_ID)


# returns whether the given user had a chat history (bool) and create it if is not
def check_and_create_user_chat_history_if_not_exist(user_id: str) -> bool:
    chat_history_path = os.getcwd() + f"\\chats\\{user_id}.json"

    if not os.path.exists(chat_history_path):
        with open(chat_history_path, "w") as file:
            json.dump([], file, indent=4) # empty chat history
        return False
    else:
        return True

def get_user_chat_history(user_id: str) -> dict:
    chat_history_path = os.getcwd() + f"\\chats\\{user_id}.json" 
    with open(chat_history_path, "r") as file:
        chat_history = json.load(file)
    return chat_history

def save_new_chat_history(user_id: str, new_chat_history: list) -> None:
    chat_history_path = os.getcwd() + f"\\chats\\{user_id}.json" 
    with open(chat_history_path, "w") as file:
        json.dump(new_chat_history, file, indent=4)

def delete_current_chat_history(user_id: str) -> None:
    chat_history_path = os.getcwd() + f"\\chats\\{user_id}.json"
    os.remove(chat_history_path)


# welcome message with keyboard markup initialization after command /start
@bot.message_handler(commands=["start"])
def start_message(message):

    bot.send_message(
        chat_id=message.from_user.id,
        text="Привет! Я телеграмм бот с ChatGPT3.5 на борту.\nОтправь мне сообщение и это уже будет твоим чатом с Ассистентом от OpenAI!\nЧтобы начать новый чат и удалить текущий напишите команду /new"
    )

# giving some info by command /help
@bot.message_handler(commands=["help"])
def start_message(message):

    bot.send_message(
        chat_id=message.from_user.id,
        text="Привет! Я телеграмм бот с ChatGPT3.5 на борту. Я учитываю всю историю текущего чата для полноценного и корректного ответа.\n/new чтобы начать новый чат и удалить текущий\n/help чтобы показать это сообщение"
    )

# erase current user chat history (command /new)
@bot.message_handler(commands=["new"])
def start_message(message):

    delete_current_chat_history(message.from_user.id)

    bot.send_message(
        chat_id=message.from_user.id,
        text="Хорошо, теперь вся история текущего чата удалена.\nНачни новый чат своим сообщением"
    )

# other text messages except commands will be questions for the assistant
@bot.message_handler(content_types="text")
def message_reply(message):

    response_message = bot.send_message(
        chat_id=message.from_user.id,
        text="Я думаю что ответить..."
    )

    user_id = message.from_user.id
    check_and_create_user_chat_history_if_not_exist(user_id)

    chat_history = get_user_chat_history(user_id)
    
    try:
        new_chat_history = assistant.generate_openai_json_answer(message.text, chat_history)
    except: # any error
        bot.edit_message_text(
            text="Произошла ошибка, попробуйте позже.",
            chat_id=user_id,
            message_id=response_message.message_id
        )
    else: # if no error
        bot.edit_message_text(
            text=new_chat_history[-1]["content"],
            chat_id=user_id,
            message_id=response_message.message_id
        )

    save_new_chat_history(user_id, new_chat_history)


# start bot
bot.infinity_polling()