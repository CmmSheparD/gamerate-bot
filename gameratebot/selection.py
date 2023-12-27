from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

import storage


class SelectionCallback(CallbackData, prefix='select'):
    command: str
    db_id: int


async def process_selection_command(message: Message, command: str):
    if message.text.strip() == f'/{command}':
        await message.answer(f'Specify a title you want to {command}.')
        return
    title = message.text[len(command) + 1:].lstrip()
    if len(title) < 4:
        await message.answer(
            'Too short search value!\n'
            'The query must be <b>at least 4</b> characters long.'
        )
        return
    titles = storage.get_titles(title=title)
    if len(titles) == 0:
        await message.answer(f"No match to {title} found.")
    elif len(titles) == 1:
        return titles[0]
    else:
        builder = InlineKeyboardBuilder()
        for title in titles:
            builder.button(
                text=title.title,
                callback_data=SelectionCallback(
                    command=command,
                    db_id=title.db_id
                )
            )
        builder.adjust(1)
        reply = f'<b>{len(titles)}</b> titles found:\n' \
                + '\n'.join(map(lambda t: t.title, titles)) \
                + '\nChoose one with the buttons below.'
        await message.answer(reply, reply_markup=builder.as_markup())
