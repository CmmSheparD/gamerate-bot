from typing import Union

import asyncio
from aiogram import F
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from selection import process_selection_command, SelectionCallback

import config as cfg
import storage
from title import GameTitle

import reviewing


dp = Dispatcher()


@dp.message(CommandStart())
async def register_and_greet(message: Message):
    acc = storage.get_user_accounts(message.from_user.id)
    if len(acc) == 0:
        storage.add_user(message.from_user.id)
    await message.answer("""Welcome to the <b>Gamerate</b> bot!
Available commands:
/list - discover all the game titles in the bot's library.
/view <i>&lt;game-title&gt;</i> - get some general info on the game.
/rate <u>&lt;game-title&gt;</i> - rate the game.""")


@dp.message(Command('list'))
async def list_all_titles(message: Message):
    response = '\n'.join([title.title for title in storage.get_all_titles()])
    await message.answer(response)


@dp.message(Command('view'))
async def start_view_processing(message: Message):
    title = await process_selection_command(message, 'view')
    if title is not None:
        await send_title_view(message, title)


@dp.callback_query(SelectionCallback.filter(F.command == 'view'))
async def capture_select_callback(callback: CallbackQuery,
                                  callback_data: SelectionCallback):
    await send_title_view(callback.message, callback_data.db_id)
    await callback.message.delete()
    await callback.answer()


async def send_title_view(message: Message, obj: Union[GameTitle, int]):
    title = storage.get_title_by_id(obj) if isinstance(obj, int) else obj
    await message.answer_photo(
        title.poster_id,
        f'''<b>{title.title}</b>
<b>Studio:</b> {title.studio}
<b>Director:</b> {title.director}
<b>Released:</b> {title.release_date.strftime("%d %b %Y")}
<b>Average score: {title.average_score if title.average_score is not None else "-/-"}</b>'''
    )


async def main():
    bot = Bot(cfg.token, parse_mode=ParseMode.HTML)
    dp.include_router(reviewing.router)

    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
