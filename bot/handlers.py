import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.types import ReplyKeyboardRemove
from bot import texts, keyboards
from bot.load_all import bot, dp
from bot.modules.state import UserState

from datetime import timedelta

from bot.edit_or_send_message import edit_or_send_message
from database.functions import create_user


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message):
    # Если пользователь новый то создаёт его в базе данных
    text = f"Здраствуйте! {message.from_user.first_name}\n"
    text += await texts.menu(bot)

    await edit_or_send_message(bot, message, text=text, kb=keyboards.menu, disable_web=True)


@dp.message_handler(Text(equals="Запись"), state="*")
async def entry(message: types.Message):
    await edit_or_send_message(bot, message, text=await texts.name(bot), kb=ReplyKeyboardRemove(), disable_web=True)
    await UserState.name.set()


@dp.message_handler(state=UserState.name)
async def set_name(message: types.Message, state: FSMContext):
    # Вариант 1 сохранения переменных - записываем через key=var
    await state.update_data(
        {"name": message.text}
    )
    text = await texts.phone(bot)
    await edit_or_send_message(bot, message, text=text, disable_web=True)
    await UserState.phone.set()


@dp.message_handler(state=UserState.phone)
async def start_(message: types.Message, state: FSMContext):
    await state.update_data(
        {"phone": message.text}
    )
    data = await state.get_data()
    logging.info(f"{data['name']} {data['phone']}")

    await edit_or_send_message(bot, message, text="Выберите месяц", kb=keyboards.month, disable_web=True)
    await UserState.month.set()


# @dp.message_handler(Text(equals=['Декабрь', 'Январь', 'Февраль',
#                                  'Март', 'Апрель', 'Май',
#                                  'Июнь', 'Июль', 'Август',
#                                  'Сентябрь', 'Октябрь', 'Ноябрь']), state=UserState.month)
# async def start_(message: types.Message, state: FSMContext):
#     await state.update_data(
#         {"month": message.text}
#     )
#
#     await edit_or_send_message(bot, message, text="Выберите день", disable_web=True)
#     await UserState.month.set()

@dp.callback_query_handler(state=UserState.month)
async def start_(callback: types.CallbackQuery, state: FSMContext):
    if callback.data=="previous_month":
        kb=keyboards.month()
    await edit_or_send_message(bot, message, text="Выберите день", disable_web=True)
    await UserState.month.set()



# @dp.message_handler(commands=['start'], state='*')
# async def start_(message: types.Message):
#     user, is_created_now =
#     text = ""
#     # Если пользователь новый то создаёт его в базе данных
#     if is_created_now:
#         user.username = message.from_user.username
#         user.full_name = message.from_user.full_name
#         user.save()
#         text += f"Здраствуйте! {user.full_name}\n"
#     else:
#         text += f"С возвращением! {user.full_name}\n"
#     text += await texts.menu(user, bot)
#     await edit_or_send_message(bot, message, text=text, kb=keyboards.menu, disable_web=True)
