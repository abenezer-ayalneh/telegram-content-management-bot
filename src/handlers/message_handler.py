from telegram import Update, Bot


class MessageHandler:
    bot: Bot
    update: Update

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def decider(self, update: Update):
        # Decide where to go
        self.update = update
        command = update.message.text

        match command:
            case 'hello':
                await self.hello()
            case '/help':
                await self.help()
            case _:
                await self.default()

    async def helloHel(self):
        id = self.update.message.from_user.id
        text = f"""Hello back at ya!"""
        await self.bot.send_message(text=text, chat_id=id, parse_mode="HTML")
    
    
    async def help(self):
        id = self.update.message.from_user.id
        text = f""" Did I hear you say HEEEEEEELP!?"""
        await self.bot.send_message(text=text, chat_id=id, parse_mode="HTML")


    async def default(self):
        id = self.update.message.from_user.id
        text = f"""You are tripping! There is no command with this name."""
        await self.bot.send_message(text=text, chat_id=id, parse_mode="HTML")
