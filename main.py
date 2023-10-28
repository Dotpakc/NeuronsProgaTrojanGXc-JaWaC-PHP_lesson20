from aiogram import Bot, Dispatcher

from decouple import config

API_TOKEN = config('TELEGRAM_API_TOKEN')

# bot = Bot(token=API_TOKEN)

import asyncio
import logging
import sys


from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold



dp = Dispatcher()


users = []

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    print(message)
    print(message.chat)
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")
    print(message.chat.type)
    if message.chat.type == "private":
        await message.answer("This is a private chat.")
    elif message.chat.type == "group":
        await message.answer("This is a group chat.")

    if message.from_user.id not in [user.get('id', 0) for user in users]:
        users.append({'id': message.from_user.id, 'full_name': message.from_user.full_name})
        await message.answer(f"Рад вас бачити, ви тут вперше! Ви {len(users)}-й учасник!")
    else:
        await message.answer(f"Так ви ж вже тут були! Скільки разів ви будете мене вітати?")
    await message.answer(f"Для того щоб побачити список користувачів введіть команду /users")

@dp.message(Command('users'))
async def command_users_handler(message: Message) -> None:
    print(users)
    text = f'Список користувачів:\n'
    for i,user in enumerate(users, start=1):
        text += f"{i}. {user['id']} - {user['full_name']}\n"
    text += f'Всього користувачів: {len(users)}'
    await message.answer(text)



@dp.message()
async def echo_handler(message: types.Message) -> None:
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(API_TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())