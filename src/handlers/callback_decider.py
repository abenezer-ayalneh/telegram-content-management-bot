from dotenv import load_dotenv
from misc import constants
from src.handlers.callbacks.channel_callbacks import ChannelCallbacks
from src.handlers.callbacks.new_post_callbacks import NewPostCallbacks
from src.root import Root

load_dotenv()


class CallbackDecider:
    root: Root
    new_post_callbacks: NewPostCallbacks
    channel_callbacks: ChannelCallbacks

    def __init__(self) -> None:
        self.root = Root()
        self.new_post_callbacks = NewPostCallbacks()
        self.channel_callbacks = ChannelCallbacks()

    async def decider(self):
        callback_data = self.root.update.callback_query.data

        match callback_data:
            case "new_post.update.title" | "new_post.update.description" | "new_post.update.images":
                await self.new_post_callbacks.update_attribute()
            case "new_post.back_to_post":
                await self.new_post_callbacks.back_to_post()
            case "new_post.post_confirmation":
                await self.new_post_callbacks.post_confirmation()
            case "new_post.confirm_post":
                await self.new_post_callbacks.confirm_post()
            case constants.CHANGE_CHANNEL:
                await self.channel_callbacks.change_channel()
            case _:
                await self.default()

    async def default(self):
        text = """Opps! This button doesn't have a purpose yet! Try another"""
        await self.bot.send_message(text=text, chat_id=self.chat_id, parse_mode="HTML")

