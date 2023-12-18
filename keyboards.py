"""all keyboards for bot"""
import asyncio
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.utils.markdown import hbold, hitalic

from lexicon import MATH_COMMAND, INLINE_BUTTONS_FOR_X, INLINE_BUTTONS_FOR_AB

async def markup_start() -> ReplyKeyboardMarkup:
    """keyboard for start message"""
    builder = ReplyKeyboardBuilder()
    builder.button(text="Составить пример")
    return builder.as_markup(resize_keyboard=True)

async def markup_edit_math_mess(last_button: str | None = None, data: str | None = None) -> InlineKeyboardMarkup:
    """keyboard for edit math message"""
    builder = InlineKeyboardBuilder()

    for command in MATH_COMMAND:
        try:
            MATH_COMMAND[MATH_COMMAND.index(command)] = InlineKeyboardButton(text=command, callback_data=command)
        except:
            break
    builder.row(*MATH_COMMAND, width=8)
    builder.adjust(8, 8, 8, 5, 4, 1)

    if last_button:
        builder.row(InlineKeyboardButton(
            text=last_button,
            callback_data=last_button
        ))
    if data == "Определить a":
        builder.row(*[
            InlineKeyboardButton(
                text="Определить b",
                callback_data="Определить b"
            ),
            InlineKeyboardButton(
                text="Вернуться",
                callback_data="back"
            )
        ], width=1)
    elif data == "Определить b":
        builder.row(*[
            InlineKeyboardButton(
                text="Определить a",
                callback_data="Определить a"
            ),
            InlineKeyboardButton(
                text="Вернуться",
                callback_data="back"
            )
        ], width=1)
    return builder.as_markup()

async def markup_for_x() -> InlineKeyboardMarkup:
    """keyboard for x"""
    builder = InlineKeyboardBuilder()

    for button in INLINE_BUTTONS_FOR_X:
        try:
            INLINE_BUTTONS_FOR_X[INLINE_BUTTONS_FOR_X.index(button)] = InlineKeyboardButton(text=button, callback_data=button)
        except:
            break
    builder.row(*INLINE_BUTTONS_FOR_X, width=1)
    return builder.as_markup()

async def markup_for_ab() -> InlineKeyboardMarkup:
    """keyboard for a and b"""
    builder = InlineKeyboardBuilder()

    for button in INLINE_BUTTONS_FOR_AB:
        try:
            if button == "Вернуться":
                data = "back"
            else:
                data = button
            INLINE_BUTTONS_FOR_AB[INLINE_BUTTONS_FOR_AB.index(button)] = InlineKeyboardButton(text=button, callback_data=data)
        except:
            break
    builder.row(*INLINE_BUTTONS_FOR_AB, width=1)
    return builder.as_markup()

async def mapkup_for_sub() -> InlineKeyboardMarkup:
    """keyboard for check subscribe"""
    builder = InlineKeyboardBuilder()
    builder.row(*[
        InlineKeyboardButton(
            text="Подписаться",
            url="https://t.me/school_aid"
        ),
        InlineKeyboardButton(
            text="Подписался",
            callback_data="is_sub"
        )
    ], width=1)
    return builder.as_markup()