import logging
import os
import pickle

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.types import ReplyKeyboardRemove
from bot import texts, keyboards
from bot.load_all import bot, dp
from bot.modules.state import UserState
import re
from datetime import datetime

from datetime import timedelta

from bot.edit_or_send_message import edit_or_send_message
from googleapiclient.discovery import build


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message):
    text = f"Здраствуйте! {message.from_user.first_name}\n"
    text += await texts.menu(bot)

    await edit_or_send_message(bot, message, text=text, kb=keyboards.menu, disable_web=True)


@dp.message_handler(Text(equals="Запись"), state="*")
async def entry(message: types.Message):
    await edit_or_send_message(bot, message, text=await texts.name(bot), kb=ReplyKeyboardRemove(), disable_web=True)
    await UserState.name.set()


@dp.message_handler(Text(equals="Как проехать?"), state="*")
async def map(message: types.Message):
   await bot.send_location(chat_id=message.chat.id,reply_markup=keyboards.menu,latitude=43.238416,longitude=76.970679)
   await bot.send_message(chat_id=message.chat.id,text="ул.Радлова 65, Алматы, Казахстан", reply_markup=keyboards.menu)

@dp.message_handler(state=UserState.name)
async def set_name(message: types.Message, state: FSMContext):
    await state.update_data(
        {"name": message.text}
    )
    text = await texts.phone(bot)
    await edit_or_send_message(bot, message, text=text, disable_web=True)
    await UserState.phone.set()


@dp.message_handler(state=UserState.phone)
async def start_(message: types.Message, state: FSMContext):
    result = message.text
    result = re.sub(r"\s+", "", result)
    result = re.findall(r"\+?[78]\(?\d\d\d\)?\d\d\d-?\d\d-?\d\d", result)

    if not result:
        await message.answer(text="Введите номер телефона в корректном формате (+79159402345)", reply=False)
        return
    else:
        result = result[0]

    await state.update_data(
        {"phone": result}
    )

    callback = types.CallbackQuery()
    callback.data, callback.message = None, message
    await month_keyboard(callback, state)
    await UserState.month.set()


@dp.callback_query_handler(state=UserState.month)
async def month_keyboard(callback: types.CallbackQuery, state: FSMContext):
    logging.info(callback.data)
    message = callback.message
    if callback.data is not None:
        if "set_month" in callback.data:
            month = int(re.findall(r"set_month (\d\d)\.\d\d\d\d", callback.data)[0])
            year = int(re.findall(r"set_month \d\d\.(\d\d\d\d)", callback.data)[0])
            reply_markup = keyboards.month(month, year)
            await message.edit_reply_markup(reply_markup=reply_markup)
        elif "choose_month" in callback.data:
            month = int(re.findall(r"choose_month (\d\d)\.\d\d\d\d", callback.data)[0])
            year = int(re.findall(r"choose_month \d\d\.(\d\d\d\d)", callback.data)[0])
            await state.update_data({"month": month, "year": year})
            await message.edit_text(text="Выберите дату", reply_markup=keyboards.day(month, year))
            await UserState.day.set()
    else:
        day_now = datetime.now()
        month, year = day_now.month, day_now.year
        reply_markup = keyboards.month(month, year)
        await bot.send_message(chat_id=message.chat.id, text="Выберите месяц записи", reply_markup=reply_markup)


@dp.callback_query_handler(state=UserState.day)
async def day_keyboard(callback: types.CallbackQuery, state: FSMContext):
    logging.info(callback.data)
    if (callback.data == "choose_month"):
        callback.data= None
        day_now = datetime.now()
        month, year = day_now.month, day_now.year
        await UserState.month.set()
        await callback.message.edit_text(text='Выберите месяц', reply_markup=keyboards.month(month, year))

        return
    day = int(re.findall(r"set_day (\d\d)", callback.data)[0])


    await state.update_data({"day": day})
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    service = build('calendar', 'v3', credentials=creds)
    # Call the Calendar API
    data = await state.get_data()
    day_int, month_int, year = data['day'], data['month'], data['year']
    day_now, month_now, year_now = data['day'], data['month'], data[
        'year'] = datetime.now().day, datetime.now().month, datetime.now().year
    if day_int == day_now and month_int == month_now and year == year_now:
        hour = datetime.now().hour
        minute = datetime.now().minute
        now = datetime(day=day_int, month=month_int, year=year, hour=hour, minute=minute).isoformat() + 'Z'
    else:
        now = datetime(day=day_int, month=month_int, year=year).isoformat() + 'Z'
    not_now = (datetime(day=day_int, month=month_int, year=year) + timedelta(
        days=1)).isoformat() + 'Z'

    events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=not_now,
                                          maxResults=100, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    keyboard_time = keyboards.time(events)
    if keyboard_time == None:
        await UserState.month.set()
        await callback.message.edit_text(
            text='"Свободного времени на выбранную дату нет, пожалуйста, попробуйте другую дату."',
            reply_markup=keyboards.month(month_now, year_now))
    else:
        await callback.message.edit_text(text='Выберите время', reply_markup=keyboard_time)
        await UserState.time.set()



@dp.callback_query_handler(state=UserState.time)
async def time(callback: types.CallbackQuery, state: FSMContext):
    event_id = callback.data
    data = await state.get_data()
    if(callback.data=="choose_day"):
        await callback.message.edit_text(text="Выберите дату", reply_markup=keyboards.day(data['month'], data['year']))
        await UserState.day.set()

        return
    logging.info(event_id)
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    service = build('calendar', 'v3', credentials=creds)
    event = service.events().get(calendarId='primary', eventId=event_id).execute()
    text_to_desc = f"{data['name']} {data['phone']}"
    event['description'] = f"{event['description']}\n{text_to_desc}" if 'description' in event.keys() else text_to_desc
    updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
    await callback.message.edit_text(text="Спасибо за регистрацию! Для новой записи нажмите: /start", reply_markup=None)


@dp.message_handler(state="*")
async def text(message: types.Message, state: FSMContext):
    await message.delete()
