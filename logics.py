"""function logics for bot"""
import asyncio
import aiofiles
from typing import *
from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram.exceptions import TelegramBadRequest
import json

from keyboards import markup_edit_math_mess, markup_for_x, markup_for_ab
from lexicon import LAST_BUTTON, PLUG_FOR_X, PLUG_FOR_AB, PLUG_FOR_USERS, MESSAGE_KEYBOARD_START

async def logics_for_X(callback: CallbackQuery, id: str) -> CallbackQuery:
    """logics for math elements with x var"""
    content = await logics_open_json()
    value = json.loads(content)
    value[str(id)]['message_edit'] = callback.data
    value[str(id)]['message_for_x'] = callback.data
    await logics_write_json(value)
    return await callback.message.edit_text(text=PLUG_FOR_X, reply_markup=await markup_for_x())

async def logics_for_nums(callback: CallbackQuery, id: str) -> CallbackQuery:
    """logics for math elements with nums var"""
    content = await logics_open_json()
    value = json.loads(content)
    MESSAGE_FOR_X = value[str(id)]['message_for_x']
    MESSAGE_EDIT = value[str(id)]['message_edit']
    if MESSAGE_FOR_X != "":
        value[str(id)]['message_for_x'] += callback.data
        await logics_write_json(value)
        if "log(a)(b)" in MESSAGE_FOR_X:
            try:
                return await callback.message.edit_text(text=PLUG_FOR_AB, reply_markup=await markup_edit_math_mess(data=value[str(id)]['message_memory']))
            except TelegramBadRequest:
                return await callback.answer()
        else:
            try:
                return await callback.message.edit_text(text=PLUG_FOR_X, reply_markup=await markup_edit_math_mess(LAST_BUTTON))
            except TelegramBadRequest:
                return await callback.answer()
    else:
        value[str(id)]['message_cancel'] += callback.data
        await logics_write_json(value)
        try:
            return await callback.message.edit_text(text=value[str(id)]['message_cancel'], reply_markup=await markup_edit_math_mess())
        except TelegramBadRequest as ex:
            print(ex)
            return await callback.answer()

async def logics_backspace(callback: CallbackQuery, id: str) -> CallbackQuery:
    """logics backspace for elements"""
    content = await logics_open_json()
    value = json.loads(content)
    MESSAGE_CANCEL = value[str(id)]['message_cancel']
    if MESSAGE_CANCEL != "":
        MESSAGE_CANCEL = MESSAGE_CANCEL[:-1]
        value[str(id)]['message_cancel'] = MESSAGE_CANCEL
        await logics_write_json(value)
        if MESSAGE_CANCEL == "":
            MESSAGE_CANCEL = MESSAGE_KEYBOARD_START
        return await callback.message.edit_text(text=MESSAGE_CANCEL, reply_markup=await markup_edit_math_mess())
    else:
        return await callback.answer()

async def logics_log_ab(callback: CallbackQuery, id: str) -> CallbackQuery:
    """logics for math elemens where value log(a)(b)"""
    content = await logics_open_json()
    value = json.loads(content)
    value[str(id)]['message_for_x'] = callback.data
    value[str(id)]['message_edit'] = callback.data
    await logics_write_json(value)
    await callback.message.edit_text(text=PLUG_FOR_AB, reply_markup=await markup_for_ab())

async def logics_check_users(id: str, file: str = "files/USERS.json", encoding: str = 'utf-8', command_start: bool | None = None) -> NoReturn:
    """start logics for json"""
    content = await logics_open_json()
    id = str(id)

    if content == "":
        value = {id : PLUG_FOR_USERS}
    else:
        value = json.loads(content)
        if id not in value:
            value[id] = PLUG_FOR_USERS
        elif command_start:
            value[id]['message_edit'] = ""
            value[id]['message_for_x'] = ""
            value[id]['message_cancel'] = ""
            value[id]['message_memory'] = ""
    await logics_write_json(value=value)

async def logics_write_json(value: dict[int, dict[str, str]], file: str = "files/USERS.json", encoding: str = 'utf-8') -> NoReturn:
    """write json function"""
    async with aiofiles.open(file, 'w', encoding=encoding) as file:
        await file.write(json.dumps(value, ensure_ascii=False, indent=4))

async def logics_open_json(file: str = "files/USERS.json", encoding: str = 'utf-8') -> Awaitable[str]:
    """open json function"""
    async with aiofiles.open(file, 'r', encoding=encoding) as file:
        content = await file.read()
    return content

async def logics_who_is_user(bot: Bot, chat_id: str, user_id: str) -> Awaitable[bool]:
    """logics for check user on his status"""
    chat_status = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    if chat_status.status == ChatMemberStatus.ADMINISTRATOR:
        return True
    elif chat_status.status == ChatMemberStatus.CREATOR:
        return True
    elif chat_status.status == ChatMemberStatus.MEMBER:
        return True
    else:
        return False
    
async def logics_clear(callback: CallbackQuery, id: str) -> CallbackQuery:
    """logics for clear math quest"""
    content = await logics_open_json()
    value = json.loads(content)
    MESSAGE_CANCEL = value[str(id)]['message_cancel']
    if MESSAGE_CANCEL != "":
        MESSAGE_CANCEL = MESSAGE_KEYBOARD_START
        value[str(id)]['message_cancel'] = ""
        await logics_write_json(value)
        return await callback.message.edit_text(text=MESSAGE_CANCEL, reply_markup=await markup_edit_math_mess())
    else:
        return await callback.answer()

async def logics_Preparation(id: str) -> Awaitable[dict[str, str]]:
    """logics for easy reading code"""
    content = await logics_open_json()
    value = json.loads(content)
    MESSAGES_FOR_GPT = value[str(id)]['messages_gpt']
    MESSAGES_FOR_GPT.append({"role": "user", "content": value[str(id)]['message_cancel']})
    await logics_write_json(value)
    content = await logics_open_json()
    value = json.loads(content)
    return value[str(id)]['messages_gpt']

    
