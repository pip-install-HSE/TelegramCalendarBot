import calendar

from bot.modules.keyboard import KeyboardInline, KeyboardReply
from aiogram import types
from datetime import datetime, timedelta
import locale
import logging


def toArray(object):
    if type(object) == type([]):
        array = object
    elif type(object) == type("string") or type(object) == type(0):
        array = [object]
    else:
        array = []
    return array


def to2Array(object, toString = False):
    array = toArray(object)

    for i, data in enumerate(array):
        if type(data) == type("string") or type(data) == type(0):
            array[i] = [data]

    if toString == True:
        for i, line in enumerate(array):
            for j, object in enumerate(line):
                if type(object) == type(0):
                    array[i][j] = str(object)

                if type(array[i][j]) != type("string"):
                    # print(object, type(object))
                    array = [[]]
                    break

    return array


def reply(array, one_time_keyboard = False, resize_keyboard = True):
    array = to2Array(array, True)

    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True)

    for line in array:
        keyboard.row(*line)

    return keyboard


def remove():
    return types.ReplyKeyboardRemove()

def force_reply():
    return types.ForceReply()

def url(text, url):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text=text, url=url))
    return keyboard


def inline(array, callback = None):
    array = to2Array(array)
    if callback != None:
        callback = to2Array(callback)
    else:
        callback = array

    # print(array, callback)

    max_len = len(max(array, key=len))
    keyboard = types.InlineKeyboardMarkup(row_width = max_len)
    for i, line in enumerate(array):
        buttons = []
        for j, text in enumerate(line):
            button = types.InlineKeyboardButton(text = text, callback_data = callback[i][j])
            buttons.append(button)
        # print("new line")
        keyboard.add(*buttons)

    return keyboard

"""
keyboard v 1.0
:List of :Dicts where first is :Str name, last is :Str callback.
"""

menu = KeyboardReply([["Запись", "О нас"],
                    {"Наш адрес", "Полезная информация"}]).get()
# menu = KeyboardReply([{"\ud83d\udcc5 Запись", "\ud83d\udcfd О нас"},
#                        {"\ud83d\udccd Наш адрес", "\ud83d\udcd8 Полезная информация"}]).get()

matches = KeyboardInline([{"<-": "prev", "->": "next"},
                          {"Меню": "menu"}]).get()

back = KeyboardInline([{"Меню": "menu"}]).get()


async def info(bot, team_id):
    teams = []
    tmp = {}
    for i, team in enumerate(teams_db[team_id:][:9]):
        tmp.update({team.name: f"team:{team.id}"})
        if (i+1) % 3 == 0:
            teams.append(tmp)
            tmp = {}
    teams.append({"<-": "team:prev", "->": "team:next"})
    teams.append({"Меню": "menu"})
    return KeyboardInline(teams).get()


def month(month, year):
    locale.setlocale(locale.LC_ALL, "ru")

    today = datetime.today()
    current = datetime.today().replace(day=1, month=month, year=year)
    next = current + timedelta(days=31)
    prev = current - timedelta(days=1)

    month_str = current.strftime("%B")

    scroll_text = [f"{month_str} {current.year}"] + [">>"]
    scroll_callback = [f"choose_month {current.strftime('%m.%Y')}"] + [f"set_month {next.strftime('%m.%Y')}"]
    if current.year > today.year or (current.year == today.year and current.month > today.month):
        scroll_text = ["<<"] + scroll_text
        scroll_callback = [f"set_month {prev.strftime('%m.%Y')}"] + scroll_callback

    return inline(
        [
            scroll_text,
            ["Выбрать"]
        ],
        [
            scroll_callback,
            [f"choose_month {current.strftime('%m.%Y')}"]
        ]
    )

def day(month, year):
    today = datetime.today()
    current = datetime.today().replace(day=1, month=month, year=year)

    first_day = 1
    # next = current
    # while next
    count = calendar.mdays[current.month]
    logging.info(f"Days in month: {count}")
    if current.month == today.month and current.year == today.year:
        first_day = today.day
        count -= (today.day - 1)

    row_count = count // 8 + (1 if (count % 8) != 0 else 0)
    count_in_row = count // row_count
    keyboard = []
    for day in range(first_day, first_day + count):
        if (day - first_day) % count_in_row == 0:
            keyboard.append([])
        keyboard[-1].append(day)

    callback = [[f"set_day {button//10}{button%10}" for button in row] for row in keyboard]
    return inline(keyboard, callback)



