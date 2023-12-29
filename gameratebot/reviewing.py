from typing import Union

from aiogram import F
from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from title import GameTitle
from selection import process_selection_command, SelectionCallback

import storage


router = Router()


class ReviewCallback(CallbackData, prefix='rate'):
    db_id: int
    score: int
    update: bool


@router.message(Command('rate'))
async def start_review_processing(message: Message):
    title = await process_selection_command(message, 'rate')
    if title is not None:
        await init_review(message, title)


@router.callback_query(SelectionCallback.filter(F.command == 'rate'))
async def capture_select_callback(callback: CallbackQuery,
                                  callback_data: SelectionCallback):
    await init_review(callback.message, callback_data.db_id,
                      callback.from_user.id)
    await callback.message.delete()
    await callback.answer()


async def init_review(message: Message, obj: Union[GameTitle, int],
                      user: int = None):
    if user is None:
        user = message.from_user.id
    title = storage.get_title_by_id(obj) if isinstance(obj, int) else obj
    reviews = storage.get_reviews(title=title.db_id, user=user)
    update = len(reviews) != 0
    builder = InlineKeyboardBuilder()
    for i in range(10, -1, -1):
        builder.button(
            text=str(i),
            callback_data=ReviewCallback(db_id=title.db_id, score=i,
                                         update=update)
        )
    builder.button(
        text='Cancel',
        callback_data=ReviewCallback(db_id=title.db_id, score=-1,
                                     update=update)
    )
    builder.adjust(1, 5, 5, 1)
    text = f'<b>{title.title}</b>\nWhat would you rate it?' \
           if not update else \
           f'<b>{title.title}</b>\n' \
           f'You have already rated it <b>{reviews[0][3]}</b>\n' \
           'Would you like to update the score?'
    await message.answer(text, reply_markup=builder.as_markup())


@router.callback_query(ReviewCallback.filter())
async def capture_review_callback(callback: CallbackQuery,
                                  callback_data: ReviewCallback):
    if callback_data.score == -1:
        await callback.answer('Ok, then.')
    elif callback_data.update:
        storage.update_review(
            callback_data.db_id,
            storage.get_user_accounts(callback.from_user.id)[0][0],
            callback_data.score
        )
    else:
        storage.add_review(
            callback_data.db_id,
            storage.get_user_accounts(callback.from_user.id)[0][0],
            callback_data.score
        )
    await callback.message.delete()
    await callback.answer()
