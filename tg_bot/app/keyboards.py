from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

time = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='1 день', callback_data='t1'),
        InlineKeyboardButton(text='3 дня', callback_data='t3'),
        InlineKeyboardButton(text='7 дней', callback_data='t7'),
        InlineKeyboardButton(text='14 дней', callback_data='t14')
    ]
])

choice_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Координаты', callback_data="Координаты"),
     InlineKeyboardButton(text='Города', callback_data="Города")],
    [InlineKeyboardButton(text='Геометки', callback_data="Геометки")]
])

param = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Температура', callback_data='temperature'),
        InlineKeyboardButton(text='Влажность', callback_data='humidity')
    ],
    [
        InlineKeyboardButton(text='Осадки', callback_data='precipitation'),
        InlineKeyboardButton(text='Скорость ветра', callback_data='wind_speed')
    ]
])

param_after_final = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Температура', callback_data='ftemperature'),
        InlineKeyboardButton(text='Влажность', callback_data='fhumidity')
    ],
    [
        InlineKeyboardButton(text='Осадки', callback_data='fprecipitation'),
        InlineKeyboardButton(text='Скорость ветра', callback_data='fwind_speed')
    ],
    [InlineKeyboardButton(text='Хватит', callback_data='end')]
])