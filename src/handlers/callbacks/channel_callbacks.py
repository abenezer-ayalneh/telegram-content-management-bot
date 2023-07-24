from src.root import Root
from misc import constants

class ChannelCallbacks:
  root: Root

  def __init__(self) -> None:
    self.root = Root()

  async def change_channel(self):
      text = 'Lets connect me to your new channel!\nHere are the two steps needed:\n\n<b>Step 1:</b> You have to add me as an admin to your channel with just the following permissions turned on:\n\t✅ Post Messages\n\t✅ Edit Messages\n\t✅ Delete Messages\n<b>Step 2:</b> Forward me any message from the channel'

      self.root.db.sessions.update_one({"chat_id": self.root.chat_id}, {
          "$set": {"question": constants.CONNECT_WITH_CHANNEL}}, upsert=True)

      await self.root.bot.send_message(text=text, chat_id=self.root.chat_id, parse_mode="HTML")
      await self.root.bot.send_message(text="I'm waiting...", chat_id=self.root.chat_id, parse_mode="HTML")