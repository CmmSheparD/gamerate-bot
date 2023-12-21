import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

import config as cfg
import storage
from title import GameTitle


dp = Dispatcher()


@dp.message(CommandStart())
async def say_hello(message: Message):
    await message.answer("""Welcome to the <b>Gamerate</b> bot!
Available commands:
/list - discover all the game titles in the bot's library.
/view <i>&lt;game-title&gt;</i> - get some general info on the game.""")


@dp.message(Command('list'))
async def list_all_titles(message: Message):
    response = '\n'.join([title.title for title in storage.get_all()])
    await message.answer(response)


@dp.message(Command('view'))
async def respond_with_title(message: Message):
    if message.text.strip() == '/view':
        await message.answer('Specify a title you want to view.')
        return
    title = message.text.removeprefix('/view').lstrip()
    title_obj = storage.match_title(title)
    if title_obj is not None:
        await message.answer_photo(title_obj.poster_id,
                                   f'<b>{title_obj.title}</b>\n'
                                   f'<b>Studio:</b> {title_obj.studio}\n'
                                   f'<b>Director:</b> {title_obj.director}\n'
                                   f'<b>Released:</b> {title_obj.release_year}\n')
    else:
        await message.answer(f"No match to {title} found.")


async def main():
    bot = Bot(cfg.token, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == '__main__':
    storage.add_title(GameTitle("Demon's Souls",
                                'FromSoftware',
                                'Hidetaka Miyazaki',
                                2009,
                                'AgACAgIAAxkBAAIBAWVvH_ufieuvQjxtdspzpbFhchqZAAJl0zEbeul4S23IY3Go4JgkAQADAgADeQADMwQ'))
    storage.add_title(GameTitle("Demon's Souls (2020)",
                                'Bluepoint Games',
                                'Gavin Moore',
                                2020,
                                'AgACAgIAAxkBAAP8ZW8T8C_9d3tG8CCsGRLIm10VdL0AAtfSMRt66XhLJANLzH7KhdoBAAMCAAN5AAMzBA'))
    storage.add_title(GameTitle('DARK SOULS: Prepare to Die Edition',
                                'FromSoftware',
                                'Hidetaka Miyazaki',
                                2012,
                                'AgACAgIAAxkBAAIBA2VvIkBQW8angcNmMmvShBY3zdMkAAKu0zEb65yAS4pqQWxAhHhqAQADAgADeQADMwQ'))
    storage.add_title(GameTitle('DARK SOULS: REMASTERED',
                                'FromSoftware',
                                'Hidetaka Miyazaki',
                                2018,
                                'AgACAgIAAxkBAAP_ZW8eiBN-zy1dipL5dYr5AAHqVNx4AAJb0zEbeul4S00mTG59CaeFAQADAgADeQADMwQ'))
    storage.add_title(GameTitle('DARK SOULS 2: Scholar of the First Sin',
                                'FromSoftware',
                                'Yui Tanimura',
                                2015,
                                'AgACAgIAAxkBAAIBBWVvJNpvpvAJl5qo7S4ipGyDIQw6AAK80zEb65yAS8hDRUCrKhzFAQADAgADeAADMwQ'))
    storage.add_title(GameTitle('DARK SOULS 3',
                                'FromSoftware',
                                'Hidetaka Miyazaki',
                                2016,
                                'AgACAgIAAxkBAAIBC2Vvf5lP0hXQKwLn-0qAq8NH2MBvAALbzjEbeumAS2OmmPV9baeEAQADAgADeAADMwQ'))
    storage.add_title(GameTitle('Bloodborne',
                                'FromSoftware',
                                'Hidetaka Miyazaki',
                                2015,
                                'AgACAgIAAxkBAAIBCWVvfdMWhQRGnida-frrlkZ4xx3UAAKY1jEb65yAS9grQf2slZ_bAQADAgADeQADMwQ'))
    storage.add_title(GameTitle('Sekiro: Shadows Die Twice',
                                'FromSoftware',
                                'Hidetaka Miyazaki',
                                2019,
                                'AgACAgIAAxkBAAIBE2VvgKOZEBOvmDZ50W9rjU52sbqyAALpzjEbeumAS9vCF6EnEsNuAQADAgADeQADMwQ'))
    storage.add_title(GameTitle('ELDEN RING',
                                'FromSoftware',
                                'Hidetaka Miyazaki',
                                2020,
                                'AgACAgIAAxkBAAIBEWVvgHd5FM7ze1bZ-zaxbwHU3wABYgACstYxG-ucgEs7s3ak6ZqZkgEAAwIAA3kAAzME'))
    asyncio.run(main())
