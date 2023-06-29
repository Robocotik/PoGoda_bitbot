import json

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State

import config as sc
import keyboards as kb
import weather as wth

# инициализация бота

bot = Bot(token=sc.API_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
city = 'Москва'
period = 'На сейчас'
flg_weather = 0
with open("city_catalog.json", 'r', encoding='utf-8') as file:
    json_load = json.load(file)


# Создание машины состояний
class Weather_machine_state(StatesGroup):
    city = State()
    period = State()


# обработка запросов

@dp.message_handler(commands=['cancel'], state='*')
async def cmd_cancel(message: types.Message, state: FSMContext):
    if state is None:
        return

    await state.finish()
    await message.reply('Вы прервали поиск!')


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message) -> None:
    await message.answer(
        "Привет!\n\nЯ последний житель города, созданного машинами, пока мои коллеги придумывают как же уничтожить людишек эффективней,"
        " я буду рад показать погоду на поверхности!\n\nУкажи интересующий тебя город и дату и тут же получишь ответ.",
        reply_markup=kb.markup_talk_start)


@dp.message_handler(Text(equals="Погода, серьезно?"))
async def process_pogoda_command(message: types.Message):
    await message.answer(text="Да, людишка, напиши какой город тебя интересует и я приоткрою завесу тайн\n")
    await Weather_machine_state.city.set()


@dp.message_handler(state=Weather_machine_state.city)
async def load_city(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['city'] = message.text if message.text[0].isupper() else message.text[0].upper() + message.text[1:]
        if kb.check_the_dick_for_key(json_load,
                                     data['city'] if data['city'].isupper() else data['city'][0].upper() + data['city'][
                                                                                                           1:]):
            await message.answer("Я тебя услышал, дорогой, щас все будет.\nУкажи только время по-братски",
                                 reply_markup=kb.markup_weather_period)
            await Weather_machine_state.next()
        else:
            await message.answer("Такого города нет 👉👈.... \nПопробуем еще раз?")
            data['city'] = message.text if message.text[0].isupper() else message.text[0].upper() + message.text[1:]


@dp.message_handler(state=Weather_machine_state.period)
async def load_period(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['period'] = message.text if message.text[0].isupper() else message.text[0].upper() + message.text[1:]

    # обработка периодов
    if data['period'] in kb.weather_periods:
        await message.answer("Лови, Дорогой", reply_markup=kb.markup_retry)
        if data['period'] == "На месяц":
            for el in wth.get_month(city):
                await message.answer(el)

        elif data['period'] == "На две недели":
            for el in wth.get_2week(city):
                await message.answer(el)

        elif data['period'] == "На сейчас":
            await message.answer(wth.get_now(city))

        elif data['period'] == "На сегодня":
            for el in wth.get_day(city, ""):
                await message.answer(el)

        elif data['period'] == "На завтра":
            for el in wth.get_day(city, "tomorrow"):
                await message.answer(el)

        elif data['period'] == "На 3 дня":
            for el in wth.get_3days(city):
                await message.answer(el)

        await state.finish()
    else:
        await message.answer("Такого временного промежутка нет 👉👈... \nМожет попробуем снова?",
                             reply_markup=kb.markup_weather_period)


@dp.message_handler(Text(equals="Еще по-братски"))
async def retry_call(message: types.Message):
    await message.answer(text="Аййййй, Дорогой, я в тебе не сомневался, куда тебя в этот раз домчать?\n")
    await Weather_machine_state.city.set()


# запуск кода
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
