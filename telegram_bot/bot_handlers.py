from telethon import events
from loguru import logger

async def start_handler(event):
    """Send a message when the command /start is issued."""
    await event.respond('Hi!')
    logger.info("responding")
    raise events.StopPropagation

async def send_message_as_bot(user, message: str):
    logger.info(f"Sending message as bot to {user}: {str(message)}")
    await bot.send_message(user, message)


def get_bot_events():
    bot_events = {
        "start": (start_handler, events.NewMessage(pattern='/start')),
    }
    return bot_events
