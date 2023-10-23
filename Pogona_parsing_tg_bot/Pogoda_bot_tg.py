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
    cur_date = State()


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
        "Привет! 👋\n\nЯ последний представитель цивилизации Кефтемее 🌌, \nнаши бархатные тяги достигли такого развития, что мы прилетели к вам сквозь само пространство-время с планеты Нибиру для налаживания контакта.\n\n"
        "Мы уже давно наблюдаем за вашей планетой и знаем про нее даже больше чем вы. 🙃\n\nВот, например, укажи интересующий тебя город и дату и тут же получишь прогноз погоды. 👇",
        reply_markup=kb.markup_talk_start)


@dp.message_handler(Text(equals="Погода, серьезно?"))
async def process_pogoda_command(message: types.Message):
    await message.answer(text="Да, братишка, а ты что хотел?\nОтправь город, я тебе все покажу")
    await Weather_machine_state.city.set()


@dp.message_handler(lambda message: message.text, state=Weather_machine_state.city)
async def load_city(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['city'] = message.text if message.text[0].isupper() else message.text[0].upper() + message.text[1:]
        city = data['city']
        if kb.check_the_dick_for_key(json_load,
                                     data['city'] if data['city'].isupper() else data['city'][0].upper() + data['city'][
                                                                                                           1:]):
            await message.answer("КЕФТЕМЕЕ, щас все будет.\nУкажи только время по-братски.",
                                 reply_markup=kb.markup_weather_period)
            await Weather_machine_state.next()
        else:
            await message.answer("Такого города нет 👉👈.... \nПопробуем еще раз?")
            data['city'] = message.text if message.text[0].isupper() else message.text[0].upper() + message.text[1:]
            city = data['city']


@dp.message_handler(lambda message: message.text, state=Weather_machine_state.period)
async def load_period(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:

        data['period'] = message.text if message.text[0].isupper() else message.text[0].upper() + message.text[1:]
        data['city'] = city

    # обработка периодов
    if data['period'] in kb.weather_periods:
        if data['period'] == "На месяц":
            await message.answer("Лови, Дорогой")
            for el in wth.get_month(city):
                await message.answer(el)
            await message.answer("Что-то еще? :)", reply_markup=kb.markup_retry)
            await state.finish()

        elif data['period'] == "На две недели":
            await message.answer("Лови, Дорогой")
            for el in wth.get_2week(city):
                await message.answer(el)
            await message.answer("Что-то еще? :)", reply_markup=kb.markup_retry)
            await state.finish()

        elif data['period'] == "На сейчас":
            await message.answer("Лови, Дорогой")
            await message.answer(wth.get_now(city))
            await message.answer("Что-то еще? :)", reply_markup=kb.markup_retry)
            await state.finish()

        elif data['period'] == "На ближайший день":
            await message.answer("Какой именно денек тебя интересует?")

            for el in kb.find_10_day_periods(data['city']):
                await message.answer(el)
            await message.answer("Отправьте число чтобы продолжить")
            await Weather_machine_state.next()


    else:
        await message.answer("Такого временного промежутка нет 👉👈... \nМожет попробуем снова?",
                             reply_markup=kb.markup_weather_period)


@dp.message_handler(lambda message: message.text, state=Weather_machine_state.cur_date)
async def load_cur_date(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['cur_date'] = message.text
    await message.answer("Лови, Дорогой")
    for el in wth.get_one_from_ten(data['city'], int(data['cur_date'])):
        await message.answer(el)
    await message.answer("Что-то еще? :)", reply_markup=kb.markup_retry)
    await state.finish()


@dp.message_handler(Text(equals="Еще по-братски"))
async def retry_call(message: types.Message):
    await message.answer(text="КЕФТЕМЕЕ, щас все будет.\nУкажи только время по-братски.",
                         reply_markup=kb.markup_weather_period)
    await Weather_machine_state.period.set()


@dp.message_handler(Text(equals="Изменить город"))
async def change_city_call(message: types.Message):
    await message.answer(text="Как скажешь, братик, сейчас все организуем\nУкажи новый город и все будет сделано. 👇")
    await Weather_machine_state.city.set()



# запуск кода
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
