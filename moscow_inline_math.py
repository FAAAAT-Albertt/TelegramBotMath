"""main file"""
import asyncio
import logging
import sys
from typing import *
import json
import datetime

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold

from config import TOKEN, GROUP_ID
from keyboards import markup_start, markup_edit_math_mess, mapkup_for_sub
from lexicon import PLUG_FOR_X, PLUG_FOR_AB, START_MESSAGE, MESSAGE_KEYBOARD_START, \
MESSAGE_SUB, MESSAGE_IS_SUB, MESSAGE_IS_NOT_SUB
from logics import logics_for_X, logics_for_nums, \
logics_backspace, logics_log_ab, logics_check_users, logics_open_json, \
logics_write_json, logics_who_is_user, logics_Preparation, logics_clear
from gpt_settings import generate_response

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> NoReturn:
    """start command and next road"""

    if await logics_who_is_user(bot=bot, chat_id=GROUP_ID, user_id=message.from_user.id):
        await logics_check_users(id=message.from_user.id, file="files/USERS.json", command_start=True)
        await message.answer(text=START_MESSAGE, reply_markup=await markup_start())
        await message.delete()
    else:
        await message.answer(text=MESSAGE_SUB, reply_markup=await mapkup_for_sub())

@dp.message(F.text == "Составить пример")
async def edit_math_handler(message: Message) -> NoReturn:
    """answer message for math quest"""

    id = message.from_user.id
    if await logics_who_is_user(bot=bot, chat_id=GROUP_ID, user_id=id):
        await logics_check_users(id=id, file="files/USERS.json")
        await message.answer(text=MESSAGE_KEYBOARD_START, reply_markup=await markup_edit_math_mess())
        await message.delete()
    else:
        await message.answer(text=MESSAGE_SUB, reply_markup=await mapkup_for_sub())

@dp.callback_query(F.data.in_({"sin(x)", "cos(x)", "tg(x)", "ctg(x)", "lg(x)", "ln(x)"}))
async def callback_trigonometry_edit_handler(callback: CallbackQuery) -> NoReturn:
    """edit message for math quest, if sin(x) output"""
    
    id = callback.message.chat.id
    if await logics_who_is_user(bot=bot, chat_id=GROUP_ID, user_id=id):
        await logics_check_users(id=id, file="files/USERS.json")
        await logics_for_X(callback, id)
    else:
        await callback.message.answer(text=MESSAGE_SUB, reply_markup=await mapkup_for_sub())

@dp.callback_query(F.data == "Определить x")
async def callback_for_x_handler(callback: CallbackQuery) -> NoReturn:
    """edit message for x in math quest"""
    
    id = callback.message.chat.id
    if await logics_who_is_user(bot=bot, chat_id=GROUP_ID, user_id=id):
        await logics_check_users(id=id, file="files/USERS.json")
        content = await logics_open_json()
        value = json.loads(content)
        value[str(id)]['message_for_x'] += " | "
        await logics_write_json(value)
        await callback.message.edit_text(text=PLUG_FOR_X, reply_markup=await markup_edit_math_mess())
    else:
        await callback.message.answer(text=MESSAGE_SUB, reply_markup=await mapkup_for_sub())

@dp.callback_query(F.data.in_({"Определить a", "Определить b"}))
async def callback_for_ab_handler(callback: CallbackQuery) -> NoReturn:
    """edit message for a in math quest"""

    id = callback.message.chat.id
    if await logics_who_is_user(bot=bot, chat_id=GROUP_ID, user_id=id):
        await logics_check_users(id=id, file="files/USERS.json")
        content = await logics_open_json()
        value = json.loads(content)
        value[str(id)]['message_for_x'] += " | "
        value[str(id)]['message_memory'] = callback.data
        await logics_write_json(value)
        if callback.data == "Определить a":
            await callback.message.edit_text(text=PLUG_FOR_AB, reply_markup=await markup_edit_math_mess(data=callback.data))
        else:
            await callback.message.edit_text(text=PLUG_FOR_AB, reply_markup=await markup_edit_math_mess(data=callback.data))
    else:
        await callback.message.answer(text=MESSAGE_SUB, reply_markup=await mapkup_for_sub())

@dp.callback_query(F.data == "Вернуться")
async def callback_for_x_handler(callback: CallbackQuery) -> NoReturn:
    """cancel to math keyboard"""

    id = callback.message.chat.id
    if await logics_who_is_user(bot=bot, chat_id=GROUP_ID, user_id=id):
        await logics_check_users(id=id, file="files/USERS.json")
        content = await logics_open_json()
        value = json.loads(content)
        MESSAGE_EDIT = value[str(id)]["message_edit"]
        MESSAGE_FOR_X = value[str(id)]['message_for_x']

        try:
            MESSAGE_EDIT = MESSAGE_EDIT.replace(MESSAGE_FOR_X.split("|")[0].strip(), f"{MESSAGE_FOR_X.split('|')[0].split('(')[0]}({MESSAGE_FOR_X.split('|')[1].strip()})")
            value[str(id)]["message_edit"] = MESSAGE_EDIT
            value[str(id)]['message_cancel'] += MESSAGE_EDIT
            await logics_write_json(value)
            await callback.message.edit_text(text=value[str(id)]['message_cancel'], reply_markup=await markup_edit_math_mess())
        except:
            if value[str(id)]['message_cancel'] == "":
                await callback.message.edit_text(text=MESSAGE_KEYBOARD_START, reply_markup=await markup_edit_math_mess())
            else:
                await callback.message.edit_text(text=value[str(id)]['message_cancel'], reply_markup=await markup_edit_math_mess())
        value[str(id)]["message_edit"] = ""
        value[str(id)]["message_for_x"] = ""
        await logics_write_json(value)
    else:
        await callback.message.answer(text=MESSAGE_SUB, reply_markup=await mapkup_for_sub())

@dp.callback_query(F.data == "back")
async def callback_for_ab_back_handler(callback: CallbackQuery) -> NoReturn:
    """cancel to math keyboard where value log(a)(b)"""

    id = callback.message.chat.id
    if await logics_who_is_user(bot=bot, chat_id=GROUP_ID, user_id=id):
        await logics_check_users(id=id, file="files/USERS.json")
        content = await logics_open_json()
        value = json.loads(content)
        MESSAGE_EDIT = value[str(id)]["message_edit"]
        MESSAGE_FOR_X = value[str(id)]['message_for_x']
        try:
            MESSAGE_EDIT = MESSAGE_EDIT.replace(
                MESSAGE_FOR_X.split("|")[0].strip(),
                f'{MESSAGE_FOR_X.split("|")[0].split("(")[0]}({MESSAGE_FOR_X.split("|")[1].strip()})({MESSAGE_FOR_X.split("|")[2].strip()})'
            )
            value[str(id)]["message_edit"] = MESSAGE_EDIT
            value[str(id)]['message_cancel'] += MESSAGE_EDIT
            await logics_write_json(value)
            await callback.message.edit_text(text=value[str(id)]['message_cancel'], reply_markup=await markup_edit_math_mess())
        except:
            if value[str(id)]['message_cancel'] == "":
                await callback.message.edit_text(text=MESSAGE_KEYBOARD_START, reply_markup=await markup_edit_math_mess())
            else:
                await callback.message.edit_text(text=value[str(id)]['message_cancel'], reply_markup=await markup_edit_math_mess())
        value[str(id)]["message_edit"] = ""
        value[str(id)]["message_for_x"] = ""
        await logics_write_json(value)
    else:
        await callback.message.answer(text=MESSAGE_SUB, reply_markup=await mapkup_for_sub())

@dp.callback_query(F.data.in_({"1", "2", "3", "x", "+", "×", "=", "›",
                               "4", "5", "6", "y", "-", "÷", "(", ")",
                               "7", "8", "9", "0", "^", "√", "'", "π",
                               "‹"
                            }))
async def callback_edit1_math_handler(callback: CallbackQuery) -> NoReturn:
    """edit message for math quest where value 1"""

    id = callback.message.chat.id
    if await logics_who_is_user(bot=bot, chat_id=GROUP_ID, user_id=id):
        await logics_check_users(id=id, file="files/USERS.json")
        await logics_for_nums(callback, id)
    else:
        await callback.message.answer(text=MESSAGE_SUB, reply_markup=await mapkup_for_sub())

@dp.callback_query(F.data == "log(a)(b)")
async def callback_log_a_b_handler(callback: CallbackQuery) -> NoReturn:
    """deit meessage for math quest where value log(a)(b)"""

    id = callback.message.chat.id
    if await logics_who_is_user(bot=bot, chat_id=GROUP_ID, user_id=id):
        await logics_check_users(id=id, file="files/USERS.json")
        await logics_log_ab(callback, id)
    else:
        await callback.message.answer(text=MESSAGE_SUB, reply_markup=await mapkup_for_sub())

@dp.callback_query(F.data == "←")
async def callback_backspace_handler(callback: CallbackQuery) -> NoReturn:
    """backspace one symbol in message"""

    id = callback.message.chat.id
    if await logics_who_is_user(bot=bot, chat_id=GROUP_ID, user_id=id):
        await logics_check_users(id=id, file="files/USERS.json")
        await logics_backspace(callback, id)
    else:
        await callback.message.answer(text=MESSAGE_SUB, reply_markup=await mapkup_for_sub())

@dp.callback_query(F.data == "is_sub")
async def callback_sub_handler(callback: CallbackQuery) -> NoReturn:
    """hander for check user is sub or not"""

    id = callback.message.chat.id
    if await logics_who_is_user(bot=bot, chat_id=GROUP_ID, user_id=id):
        await logics_check_users(id=id, file="files/USERS.json")
        await callback.message.answer(text=MESSAGE_IS_SUB, reply_markup=await markup_start())
        await callback.answer()
    else:
        await callback.message.answer(text=MESSAGE_IS_NOT_SUB, reply_markup=await mapkup_for_sub())

@dp.callback_query(F.data == "Решить")
async def callback_work_handler(callback: CallbackQuery) -> NoReturn:
    """go work math quest"""

    id = callback.message.chat.id
    if await logics_who_is_user(bot=bot, chat_id=GROUP_ID, user_id=id):
        await logics_check_users(id=id, file="files/USERS.json")
        await generate_response(messages=await logics_Preparation(id=id))
    else:
        await callback.message.answer(text=MESSAGE_SUB, reply_markup=await mapkup_for_sub())

@dp.callback_query(F.data == "Очистить поле")
async def callback_clear_handler(callback: CallbackQuery) -> NoReturn:
    """clear math quest"""

    id = callback.message.chat.id
    if await logics_who_is_user(bot=bot, chat_id=GROUP_ID, user_id=id):
        await logics_check_users(id=id, file="files/USERS.json")
        await logics_clear(callback, id)
    else:
        await callback.message.answer(text=MESSAGE_SUB, reply_markup=await mapkup_for_sub())
    


async def main() -> None:
    """main function"""
    global bot
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())