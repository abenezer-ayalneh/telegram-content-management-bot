from fastapi import Request, FastAPI
from dotenv import dotenv_values
from telegram import Update, Bot
import chalk
from src.handlers.command_handler import CommandHandler
from src.handlers.message_handler import MessageHandler

app = FastAPI()
env = dotenv_values('.env')
token = env['TELEGRAM_BOT_TOKEN']
bot = Bot(token)

telegramUrl = 'https://api.telegram.org/bot{}'.format(token)

commands = CommandHandler(bot)
messages = MessageHandler(bot)

@app.post('/')
async def say_hello(request: Request):
    # Get data fro
    data = (await request.json())
    update = Update.de_json(data, bot)
    
    print(chalk.blue(update))
    print(chalk.red(update.message))


    if update.message != None:
        text = update.message.text
        if text.startswith('/'):
            await commands.decider(update)
        else:
            await messages.decider(update)
    

