from typing import Union

from aiogram import F
from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from selection import process_selection_command, SelectionCallback

import storage
from title import GameTitle


router = Router()


class ReviewCallback(CallbackData, prefix='rate'):
    db_id: int
    score: int


@router.message(Command('rate'))
async def start_review_processing(message: Message):
    title = await process_selection_command(message, 'rate')
    if title is not None:
        await init_review(message, title)


@router.callback_query(SelectionCallback.filter(F.command == 'rate'))
async def capture_select_callback(callback: CallbackQuery,
                                  callback_data: SelectionCallback):
    await init_review(callback.message, callback_data.db_id)
    await callback.message.delete()
    await callback.answer()


async def init_review(message: Message, obj: Union[GameTitle, int]):
    title = storage.get_title_by_id(obj) if isinstance(obj, int) else obj
    builder = InlineKeyboardBuilder()
    for i in range(10, -1, -1):
        builder.button(
            text=str(i),
            callback_data=ReviewCallback(db_id=title.db_id, score=i)
        )
    builder.adjust(1, 5, 5)
    await message.answer(
        f'<b>{title.title}</b>\nWhat would you rate it?',
        reply_markup=builder.as_markup())


@router.callback_query(ReviewCallback.filter())
async def capture_review_callback(callback: CallbackQuery,
                                  callback_data: ReviewCallback):
    storage.add_review(callback_data.db_id,
                       storage.get_user_accounts(callback.from_user.id)[0][0],
                       callback_data.score)
    await callback.message.delete()
    await callback.answer()
