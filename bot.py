import logging
from aiogram import Bot, Dispatcher, executor, types, filters
import os

# Объект бота
bot = Bot(token=os.getenv('TOKEN'))
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

@dp.message_handler(filters.CommandStart())
def start(message: types.Message) -> None:
    msg = await message.reply(f'Hello {message.from_user.first_name}\nI am a sample Telegram bot made with python-telegram-bot!')
    i = 1440
    while i > 0:
        time.sleep(120)
        i -= 2
        await msg.edit_text(time.strftime('%H:%M'))
        
@dp.message_handler(filters.IDFilter(chat_id=416507614))
def message_(message: types.Message):
    try:
        text = (message.text or message.caption).strip('!')
        print(text)
        text = repr(eval(text))
    except:
        text = traceback.format_exc()
    await message.reply(text)


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
