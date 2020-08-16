from bot.modules.keyboard import KeyboardInline, KeyboardReply

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