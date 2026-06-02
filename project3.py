import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

TOKEN = "8703197070:AAErdlUutyTTMBaFiPdx9ifNNC3Tx174PA0".strip()

bot = Bot(token=TOKEN)
dp = Dispatcher()

users = {}
user_states = {}


async def reminder_loop(user_id: int):
    while True:
        if user_id not in users:
            break

        interval = users[user_id].get("interval", 0)

        if interval > 0:
            await asyncio.sleep(interval * 3600)

            if user_id in users:
                await bot.send_message(
                    user_id,
                    "💧 Не забывай пить воду! Выпей стакан воды"
                )
        else:
            await asyncio.sleep(5)


@dp.message(Command("start"))
async def start(message: Message):
    user_id = message.from_user.id

    users[user_id] = {
        "water": 0,
        "interval": 0
    }

    await message.answer(
        "Привет! Я бот для напоминания пить воду 💧\n\n"
        "Команды:\n"
        "/setreminder 1 — напоминание каждый час\n"
        "/drank 300 — записать выпитую воду\n"
        "/status — посмотреть прогресс\n"
        "/helpwater — рекомендации\n"
        "/tips — советы\n"
        "/fact — факт\n"
        "/motivation — мотивация"
    )


@dp.message(Command("setreminder"))
async def set_reminder(message: Message):
    user_id = message.from_user.id

    try:
        hours = int(message.text.split()[1])

        if user_id not in users:
            users[user_id] = {"water": 0, "interval": 0}

        users[user_id]["interval"] = hours

        asyncio.create_task(reminder_loop(user_id))

        await message.answer(
            f"⏰ Напоминание установлено каждые {hours} час(а)"
        )

    except:
        await message.answer("Напиши так: /setreminder 1")


@dp.message(Command("drank"))
async def drank(message: Message):
    user_id = message.from_user.id

    try:
        amount = int(message.text.split()[1])

        if user_id not in users:
            users[user_id] = {"water": 0, "interval": 0}

        users[user_id]["water"] += amount

        await message.answer(f"💧 Записано: {amount} мл")

    except:
        await message.answer("Напиши так: /drank 300")


@dp.message(Command("status"))
async def status(message: Message):
    user_id = message.from_user.id

    if user_id not in users:
        await message.answer("Сначала напиши /start")
        return

    water = users[user_id]["water"]
    left = 2000 - water

    if left > 0:
        await message.answer(
            f"Ты выпил(а) {water} мл воды.\n"
            f"Осталось: {left} мл 💧"
        )
    else:
        await message.answer(
            f"🔥 Круто! Ты выпил(а) {water} мл\n"
            "Норма выполнена!"
        )


@dp.message(Command("tips"))
async def tips(message: Message):
    await message.answer(
        "💡 Советы:\n"
        "1. Пей маленькими порциями\n"
        "2. Носи бутылку воды\n"
        "3. После спорта пей больше\n"
        "4. Не жди сильной жажды"
    )


@dp.message(Command("fact"))
async def fact(message: Message):
    await message.answer(
        "📚 Факт:\nЧеловек примерно на 60% состоит из воды."
    )


@dp.message(Command("motivation"))
async def motivation(message: Message):
    await message.answer(
        "🌿 Каждый стакан воды делает тебя сильнее!"
    )


@dp.message(Command("helpwater"))
async def help_water(message: Message):
    user_states[message.from_user.id] = "age"
    await message.answer("Сколько тебе лет?")


@dp.message()
async def dialog(message: Message):
    user_id = message.from_user.id

    if user_id not in user_states:
        return

    if user_states[user_id] == "age":
        users.setdefault(user_id, {"water": 0, "interval": 0})
        users[user_id]["age"] = message.text

        user_states[user_id] = "sport"
        await message.answer("Ты занимаешься спортом? (да/нет)")
        return

    if user_states[user_id] == "sport":
        sport = message.text.lower()

        if sport == "да":
            await message.answer("💧 Рекомендуется: 2–2.5 литра воды в день")
        else:await message.answer("💧 Рекомендуется: 1.5–2 литра воды в день")

        del user_states[user_id]


async def main():
    print("Бот запущен 🚀")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

