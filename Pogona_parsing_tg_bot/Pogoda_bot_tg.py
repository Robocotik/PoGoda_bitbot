from aiogram import Bot, Dispatcher, executor, types

import keyboards as kb
import secure as sc
import weather as wth

# инициализация бота
bot = Bot(token=sc.API_TOKEN)
dp = Dispatcher(bot)
city = ''
period = ''


# обработка запросов
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
    if message.text[3:] in kb.cities:
        city = message.text[3:]
        await message.answer(text="ну что ж, как скажешь, приятель\n", reply_markup=kb.markup_weather_period)
    if message.text in kb.weather_periods:
        period = message.text
        if period == "На месяц":
            for el in wth.get_month():
                await message.answer(el)
        elif period == "На две недели":
            wth.get_2week()


# запуск кода
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
