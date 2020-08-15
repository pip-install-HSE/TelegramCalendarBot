from load_all import bot, dp

# @dp.message_handler(commands=['start'], state='*')
# async def start_(message: types.Message):
    # user, is_created_now = BotUser.objects.get_or_create(tg_id=message.chat.id)
    # text = ""
    # # Если пользователь новый то создаёт его в базе данных
    # if is_created_now:
    #     user.referral = message.get_args() if message.get_args() else None
    #     user.username = message.from_user.username
    #     user.full_name = message.from_user.full_name
    #     user.save()
    #     text += f"Здраствуйте! {user.full_name}\n"
    # else:
    #     text += f"С возвращением! {user.full_name}\n"
    # text += await texts.menu(BotUser, user, bot)
    # await edit_or_send_message(bot, message, text=text, kb=keyboards.menu, photo=random.choice(photos), disable_web=True)
