import logging
from aiogram import Bot, Dispatcher, executor, types, filters
import os, asyncio, traceback
import requests

# Объект бота
bot = Bot(token=os.getenv('TOKEN'))
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


def staticmap(area, markers=None):
    url = 'https://maps.geoapify.com/v1/staticmap'
    params = dict(
        apiKey=os.getenv('GEOAPIFY'),
        style='osm-bright',
#         marker='|'.json(f"lonlat:{m['position']['lon']},{m['position']['lat']};type:material;color:grey;icon:bus;icontype:awesome;text:210;textsize:small;shadow:no" for m in (markers or [])),
        area='rect:'+area
    )
    with open('temp.jpg', 'wb') as f:
        f.write(requests.get(url, params).content)
        

@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
    await message.answer(f'{lon},{lat}', reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(commands=['locate_me'])
async def cmd_locate_me(message: types.Message):
    reply = "Click on the the button below to share your location"
    keyboard = types.ReplyKeyboardMarkup()
    button = types.KeyboardButton("Share Position", request_location=True)
    keyboard.add(button)
    await message.answer(reply, reply_markup=keyboard)
    
@dp.message_handler(commands=['show'])
async def cmd_show(message: types.Message):
    staticmap(message.get_args())
    await message.answer_photo(types.FSInputeFile('temp.jpg'))

@dp.message_handler(filters.CommandStart())
async def start(message: types.Message) -> None:
    await message.answer_photo(types.FSInputeFile('temp.jpg'))
        
@dp.message_handler(filters.IDFilter(chat_id=416507614))
async def message_(message: types.Message):
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
