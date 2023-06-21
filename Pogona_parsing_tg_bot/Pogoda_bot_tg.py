from aiogram import Bot, Dispatcher, executor, types

import keyboards as kb

API_TOKEN = '6117325444:AAGrLR9pVGX-y-nwmA6Nlr705NTShKxwMIY'
# инициализация бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет!\n\nЯ последний житель города, созданного машинами, пока мои коллеги придумывают как же уничтожить людишек эффективней,"
        " я буду рад показать погоду на поверхности!\n\nУкажи интересующий тебя город и дату и тут же получишь ответ.",
        reply_markup=kb.markup_talk_start)


@dp.message_handler()
async def process_pogoda_command(message: types.Message):
    if message.text == 'Погода, серьезно?':
        await message.answer(text="Да, людишка, я могу показать следующие города:\n", reply_markup=kb.markup_cities)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
