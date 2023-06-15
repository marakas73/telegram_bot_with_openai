# ChatGPT3.5 Telegram Bot
Telegram Bot with ChatGPT3.5 in Python, which takes into account the history of messages.
Telegram Bot is written on `PyTelegramBotApi`, for ChatGPT the official `openai` library was used.
Message histories are saved in .json format in the `chats/` folder.
## Bot commands
- `/new` – Start new dialog
- `/help` – Show help
## Setup
1. Get your [OpenAI API](https://platform.openai.com/docs/api-reference/authentication) key

2. Get your Telegram bot token from [@BotFather](https://t.me/BotFather)

3. Edit `settings.py` to set your tokens

4. Install requirments
```bash
pip3 install -r requirements.txt
```
5. And now run
```bash
python3 main.py
```
