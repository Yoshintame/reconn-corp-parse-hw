from loguru import logger
from aiogram import Bot, Dispatcher, executor, types, filters

from config import TELEGRAM_BOT_API_TOKEN, TELEGRAM_ACCESS_ID
from telegram_bot.middlewares import AccessMiddleware
from parser.parser import parse_hw_page_by_hw_number
from telegram_bot.utils import create_hw_data_message

bot = Bot(token=TELEGRAM_BOT_API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(TELEGRAM_ACCESS_ID))



@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    await message.answer(
        "Получить информацию о HW: /hw[number]\n"
        "HW в любом регистре, после чего 1-4 цифры\n"
    )


@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=['(?i)hw([0-9]{1,4})']))
async def hw_info(message: types.Message, regexp_command):
    await send_hw_info(int(regexp_command.group(1)), message.from_user.id)

async def send_hw_info(hw_number: int | str, to_user_id: int = TELEGRAM_ACCESS_ID):
    hw_data = parse_hw_page_by_hw_number(hw_number)
    hw_message = create_hw_data_message(hw_data)
    await bot.send_message(to_user_id, hw_message, parse_mode="HTML")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
