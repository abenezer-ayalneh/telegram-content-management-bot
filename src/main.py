from fastapi import Request, FastAPI
from telegram import Update
import chalk
from src.handlers.command_decider import CommandDecider
from src.handlers.message_decider import MessageDecider
from src.handlers.callback_decider import CallbackDecider
from src.root import Root

app = FastAPI()

commands = CommandDecider()
messages = MessageDecider()
callbacks = CallbackDecider()
root = Root()


@app.post('/')
async def say_hello(request: Request):
    # Get data from webhook request
    data = (await request.json())
    update = Update.de_json(data, root.bot)
    root.set_update(update)

    if update.message != None and update.message.text != None:
        text = update.message.text
        if text.startswith('/'):
            await commands.decider()
        else:
            await messages.decider()
    elif update.callback_query != None:
        await callbacks.decider()
