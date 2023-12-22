import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

import config as cfg
import storage


dp = Dispatcher()


@dp.message(CommandStart())
async def register_and_greet(message: Message):
    acc = storage.get_user_accounts(message.from_user.id)
    if len(acc) == 0:
        storage.add_user(message.from_user.id)
    await message.answer("""Welcome to the <b>Gamerate</b> bot!
Available commands:
/list - discover all the game titles in the bot's library.
/view <i>&lt;game-title&gt;</i> - get some general info on the game.""")


@dp.message(Command('list'))
async def list_all_titles(message: Message):
    response = '\n'.join([title.title for title in storage.get_all_titles()])
    await message.answer(response)


@dp.message(Command('view'))
async def respond_title_overview(message: Message):
    if message.text.strip() == '/view':
        await message.answer('Specify a title you want to view.')
        return
    title = message.text[5:].lstrip()
    titles = storage.get_titles(title=title)
    if len(titles) != 0:
        for title_obj in titles:
            await message.answer_photo(
                title_obj.poster_id,
                f'<b>{title_obj.title}</b>\n'
                f'<b>Studio:</b> {title_obj.studio}\n'
                f'<b>Director:</b> {title_obj.director}\n'
                f'<b>Released:</b> {title_obj.release_date.strftime("%d %b %Y")}\n'
            )
    else:
        await message.answer(f"No match to {title} found.")


async def main():
    bot = Bot(cfg.token, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
