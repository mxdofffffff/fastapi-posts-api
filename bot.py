from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import asyncio
import httpx
from dotenv import load_dotenv
import os
import crud
from database import SessionLocal
from models import TGUser
from security import create_access_token
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

load_dotenv(".env")

TOKEN= os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()





keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Доступные команды")],
    ],
    resize_keyboard=True
)



async def send_help(message: Message):
    await message.answer("""/start - запуск бота\n 
/help - список команд\n
/login - вход\n
/my - посмотреть свои посты\n
/status - статус аккаунта\n
/posts - посмотреть все посты""")



async def send_posts(message: Message):
    db = SessionLocal()

    try:
        tg_user = db.query(TGUser).filter(
            TGUser.telegram_user_id == message.from_user.id
        ).first()

        if not tg_user:
            await message.answer("Сначала залогинься")
            return

        user = tg_user.user

        token = create_access_token({
            "sub": user.username
        })

    finally:
        db.close()

    url = "http://127.0.0.1:8000/posts"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        await message.answer(f"Ошибка: {response.status_code}")
        return

    posts = response.json()

    if not posts:
        await message.answer("Нет постов 😢")
        return

    text = ""

    for post in posts:
        text += f"Пост: {post['title']}\n"
        text += f"{post['content']}\n\n"

    await message.answer(text)





@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Hello",
        reply_markup=keyboard,
    )




@dp.message(lambda message: message.text == "Доступные команды")
async def get_help(message: Message):
    await send_help(message)




@dp.message(Command("login"))
async def login(message: Message):
    parts = message.text.strip().split()

    print("Parts", parts)

    if len(parts) != 3:
        await message.answer("Use /login <username> <password>")
        return

    _, username, password = parts[:3]

    url = "http://127.0.0.1:8000/token"

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            data={"username": username, "password": password}
        )
    print ("LOGIN TEXT:", message.text)

    if response.status_code != 200:
        await message.answer("Invalid username or password")
        return

    db = SessionLocal()
    try:
        db_user = crud.get_user_by_username(db, username)

        if not db_user:
            await message.answer("User not found in database")
            return

        tg_user = db.query(TGUser).filter(
            TGUser.telegram_user_id == message.from_user.id
        ).first()

        if tg_user:
            tg_user.user_id = db_user.id
        else:
            new_tg_user = TGUser(telegram_user_id=message.from_user.id,
                user_id=db_user.id)
            db.add(new_tg_user)
        db.commit()
        await message.answer("Successfully logged in")



    finally:
        db.close()




@dp.message(Command("my"))
async def my_posts(message: Message):
    db = SessionLocal()
    try:
        tg_user = db.query(TGUser).filter(TGUser.telegram_user_id ==message.from_user.id).first()
        if not tg_user:
            await message.answer("Firstly login")
            return

        user = tg_user.user

        token = create_access_token({"sub": user.username})

        url = "http://127.0.0.1:8000/my-posts"

        headers = {"Authorization": f"Bearer {token}"}

    finally:
        db.close()

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    print(user.username)
    print(token)

    if response.status_code != 200:
        await message.answer("Error")
        return
    posts = response.json()

    if not posts:
        await message.answer("No posts")
        return

    text = ""
    for post in posts:
        text += f"{post['title']}\n"
        text += f"{post['content']}\n\n"

    await message.answer(text)

@dp.message(Command("posts"))
async def posts(message: Message):
    await send_posts(message)


@dp.message(Command("help"))
async def help_command(message: Message):
    await send_help(message)



@dp.message()
async def fallback(message: Message):
    await message.answer("Please use available commands")



async def main():
    print("БОТ ЗАПУСКАЕТСЯ...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())