from misc import constants
from src.handlers.messages.channel_messages import ChannelMessages
from src.handlers.messages.new_post_messages import NewPostMessages
from src.root import Root


class MessageDecider:
    root: Root
    new_post_messages: NewPostMessages
    channel_messages: ChannelMessages

    def __init__(self) -> None:
        self.root = Root()
        self.new_post_messages = NewPostMessages()
        self.channel_messages = ChannelMessages()

    async def decider(self):
        # Decide where to go
        session = self.root.db.sessions.find_one(
            {"chat_id": self.root.chat_id})

        if session != None and session['question'] != None:
            question = session["question"]

            match question:
                case constants.UPDATE_POST_ATTRIBUTE:
                    await self.new_post_messages.update_post_attribute()
                case constants.CONNECT_WITH_CHANNEL:
                    await self.channel_messages.connect_with_channel()
                case _:
                    await self.default()
        else:
            await self.default()

    async def default(self):
        text = f"""Wrong command/message or the wrong time!"""
        await self.root.bot.send_message(text=text, chat_id=self.root.chat_id, parse_mode="HTML")
