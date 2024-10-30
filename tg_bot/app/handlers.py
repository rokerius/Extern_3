from aiogram.filters import Command
from aiogram.types import Message, Location, CallbackQuery
from aiogram import Router, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

import app.keyboards as kb

from tg_bot.app.funcs_for_showing_weather import *

router = Router()
path = "picture_to_send.png"


class Reg(StatesGroup):
    time = State()
    param = State()
    choice = State()
    city_1 = State()
    city_2 = State()
    point_1 = State()
    point_2 = State()
    geo_1 = State()
    geo_2 = State()
    final = State()


@router.message(Command('start'))
async def start(message: Message):
    await message.answer('Привет, этот бот показывает погоду для двух точек или городов, '
                         'пропиши /help, чтобы увидеть все  возможности.\n\n'
                         'Чтобы получить данные о погоде пропиши /weather')


@router.message(Command('help'))
async def start(message: Message):
    await message.answer('/help - список всех команд\n'
                         '/start - приветственное сообщение\n'
                         '/weather - вывод погоды по двум указанным точкам\n')


@router.message(Command('weather'))
async def weather(message: Message, state: FSMContext):
    await message.answer('Сейчас нужно будет ввести временной промежуток, параметр по которому будем строить '
                         'график, два города или точки. \n\n'
                         'Выбери временной промежуток:', reply_markup=kb.time)


# Инлайн с временным промежутком
@router.callback_query(lambda c: c.data in ['t1', 't3', 't7', 't14'])
async def process_time_selection(callback_query: CallbackQuery, state: FSMContext):
    selected_time = callback_query.data
    await state.update_data(time=selected_time)
    await callback_query.answer()
    await callback_query.message.answer(f'Выбери по какому параметру будем строить графики:', reply_markup=kb.param)


# Инлайн с параметром
@router.callback_query(lambda c: c.data in ['temperature', 'humidity', 'precipitation', 'wind_speed'])
async def process_time_selection(callback_query: CallbackQuery, state: FSMContext):
    selected_param = callback_query.data
    await state.update_data(param=selected_param)
    await callback_query.answer()
    await state.set_state(Reg.choice)
    await callback_query.message.answer(f'Выбери как будешь задавать точки:', reply_markup=kb.choice_inline)


# Инлайн с типом ввода
@router.callback_query(lambda c: c.data in ["Города", "Геометки", 'Координаты'])
async def process_time_selection(callback_query: CallbackQuery, state: FSMContext):
    selected_param = callback_query.data
    await state.update_data(choice=selected_param)
    await callback_query.answer()
    if selected_param == "Города":
        await state.set_state(Reg.city_1)
        await callback_query.message.answer(f'Напиши первый город')

    elif selected_param == "Геометки":
        await state.set_state(Reg.geo_1)
        await callback_query.message.answer(f'Скинь первую метку')

    elif selected_param == "Координаты":
        await state.set_state(Reg.point_1)
        await callback_query.message.answer(f'Напиши координаты первой точки через пробел')


# Считываем первые координаты
@router.message(Reg.point_1)
async def reg_point_1(message: Message, state: FSMContext):
    try:
        await state.update_data(point_1=message.text)
        await state.set_state(Reg.final)
        await message.answer(f'Напиши координаты второй точки через пробел')
    except:
        await message.answer('Проверь корректность введенной точки')
        await state.set_state(Reg.point_1)


# считываем первый город
@router.message(Reg.city_1)
async def reg_city_1(message: Message, state: FSMContext):
    try:
        await state.update_data(city_1=message.text)
        await state.set_state(Reg.final)
        await message.answer(f'Напиши второй город')
    except:
        await message.answer('Проверь корректность введенного города')
        await state.set_state(Reg.city_1)


# считываем первую геометку
@router.message(Reg.geo_1)
async def reg_geo_1(message: Location, state: FSMContext):
    try:
        await state.update_data(geo_1=str(message.location.longitude) + " " + str(message.location.latitude))
        await state.set_state(Reg.final)
        await message.answer(f'Скинь вторую геометку:')
    except:
        await message.answer("Что-то ты не то ввел, попробуй скинуть первую метку еще раз:")
        await state.set_state(Reg.geo_1)


# Получили все данные, выводим график
@router.message(Reg.final)
async def final(message: Location, state: FSMContext):
    data = await state.get_data()
    if data['choice'] == "Координаты":
        await state.update_data(point_2=message.text)
    if data['choice'] == "Города":
        await state.update_data(city_2=message.text)
    if data['choice'] == "Геометки":
        try:
            await state.update_data(geo_2=str(message.location.longitude) + " " + str(message.location.latitude))
        except:
            await message.answer("Что-то ты не то ввел, попробуй еще раз (выбери тип ввода точек)", reply_markup=kb.choice_inline)
            await state.set_state(Reg.choice)
            return 0
    try:
        data = await state.get_data()
        await message.answer(f'Сейчас посмотрю, что можно найти, это может занять какое-то время...')

        try:
            error = ""
            if data['choice'] == "Координаты":
                error = make_weather_picture_for_points(data['point_1'], data['point_2'], int(data['time'][1:]),
                                                data['param'], path)
            if data['choice'] == "Города":
                error = make_weather_picture_for_cities(data['city_1'], data['city_2'], int(data['time'][1:]),
                                                data['param'], path)
            if data['choice'] == "Геометки":
                error = make_weather_picture_for_points(data['geo_1'], data['geo_2'], int(data['time'][1:]),
                                                data['param'], path)

            if error == "":
                photo = FSInputFile(path)
                await message.answer_photo(photo)
                await message.answer(f'Ты можешь прямо сейчас выбрать по какому '
                                 f'параметру перестроить график:', reply_markup=kb.param_after_final)
            else:
                await message.answer(f'Произошла ошибка: ({error})\n\n Попробуйте еще раз: ', reply_markup=kb.choice_inline)
        except:
            await message.answer('Произошла ошибка, проблема на стороне API или некорректно введены точки')
    except:
        await message.answer("Что-то ты не то ввел, попробуй еще раз (выбери тип ввода точек):", reply_markup=kb.choice_inline)


# После того, как график вывели, добавляем возможность редактировать
@router.callback_query(lambda c: c.data in ['ftemperature', 'fhumidity', 'fprecipitation', 'fwind_speed'])
async def param_after_final(callback_query: CallbackQuery, state: FSMContext):
    selected_param = callback_query.data
    await state.update_data(param=selected_param[1:])
    await callback_query.answer()
    await state.set_state(Reg.final)
    try:
        data = await state.get_data()
        await callback_query.message.answer(f'Это может занять какое-то время...')
        try:
            error = ""
            if data['choice'] == "Координаты":
                error = make_weather_picture_for_points(data['point_1'], data['point_2'], int(data['time'][1:]),
                                                data['param'], path)
            if data['choice'] == "Города":
                error = make_weather_picture_for_cities(data['city_1'], data['city_2'], int(data['time'][1:]),
                                                data['param'], path)
            if data['choice'] == "Геометки":
                error = make_weather_picture_for_points(data['geo_1'], data['geo_2'], int(data['time'][1:]),
                                                data['param'], path)

            if error == "":
                photo = FSInputFile(path)
                await callback_query.message.answer_photo(photo)
                await callback_query.message.answer(f'Ещё?', reply_markup=kb.param_after_final)
            else:
                await callback_query.message.answer(error)

        except:
            await callback_query.message.answer('Произошла ошибка, проблема на стороне API или в обработке данных')
    except:
        await callback_query.message.answer("Что-то ты не то ввел, попробуй еще раз (выбери тип ввода точек)", reply_markup=kb.choice_inline)


@router.callback_query(lambda c: c.data in ['end'])
async def param_after_final(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Рад помочь)\n\nЕсли хотите начать заново, пишите /weather')
    await callback_query.answer()
    await state.clear()