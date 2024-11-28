import asyncio

from pyrogram import Client, filters
from oldpyro import Client as Client1
from oldpyro.errors import ApiIdInvalid as ApiIdInvalid1
from oldpyro.errors import PasswordHashInvalid as PasswordHashInvalid1
from oldpyro.errors import PhoneCodeExpired as PhoneCodeExpired1
from oldpyro.errors import PhoneCodeInvalid as PhoneCodeInvalid1
from oldpyro.errors import PhoneNumberInvalid as PhoneNumberInvalid1
from oldpyro.errors import SessionPasswordNeeded as SessionPasswordNeeded1
from pyrogram.errors import (
    ApiIdInvalid,
    FloodWait,
    PasswordHashInvalid,
    PhoneCodeExpired,
    PhoneCodeInvalid,
    PhoneNumberInvalid,
    SessionPasswordNeeded,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from telethon import TelegramClient
from telethon.errors import (
    ApiIdInvalidError,
    PasswordHashInvalidError,
    PhoneCodeExpiredError,
    PhoneCodeInvalidError,
    PhoneNumberInvalidError,
    SessionPasswordNeededError,
)
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest
from pyromod.listen.listen import ListenerTimeout

from config import SUPPORT_CHAT
from StringBot import Bad
from StringBot.utils import retry_key


async def gen_session(
    message, user_id: int, telethon: bool = False, old_pyro: bool = False
):
    ty = "ᴛᴇʟᴇᴛʜᴏɴ" if telethon else "ᴩʏʀᴏɢʀᴀᴍ v1" if old_pyro else "ᴩʏʀᴏɢʀᴀᴍ v2"

    await message.reply_text(f"» ᴛʀʏɪɴɢ ᴛᴏ sᴛᴀʀᴛ {ty} sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛᴏʀ...")

    try:
        # Ask for API ID
        api_id = await Bad.ask(
            identifier=(message.chat.id, user_id, None),
            text="» ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ʏᴏᴜʀ ᴀᴘɪ ɪᴅ ᴛᴏ ᴘʀᴏᴄᴇᴇᴅ :",
            filters=filters.text,
            timeout=300,
        )
        if await cancelled(api_id):
            return
        api_id = int(api_id.text)

        # Ask for API Hash
        api_hash = await Bad.ask(
            identifier=(message.chat.id, user_id, None),
            text="» ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ʏᴏᴜʀ ᴀᴘɪ ʜᴀsʜ ᴛᴏ ᴘʀᴏᴄᴇᴇᴅ :",
            filters=filters.text,
            timeout=300,
        )
        if await cancelled(api_hash):
            return
        api_hash = api_hash.text

        # Initialize client
        if telethon:
            client = TelegramClient(StringSession(), api_id, api_hash)
        elif old_pyro:
            client = Client1(":memory:", api_id=api_id, api_hash=api_hash)
        else:
            client = Client(name="Bad", api_id=api_id, api_hash=api_hash, in_memory=True)

        await client.connect()

        # Handle phone number input
        phone_number = await Bad.ask(
            identifier=(message.chat.id, user_id, None),
            text="» ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ʏᴏᴜʀ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ᴛᴏ ᴘʀᴏᴄᴇᴇᴅ :",
            filters=filters.text,
            timeout=300,
        )
        if await cancelled(phone_number):
            return
        phone_number = phone_number.text

        # Send OTP
        await Bad.send_message(user_id, "» ᴛʀʏɪɴɢ ᴛᴏ sᴇɴᴅ ᴏᴛᴩ...")
        code = await client.send_code(phone_number)

        # Receive OTP from user
        otp = await Bad.ask(
            identifier=(message.chat.id, user_id, None),
            text=f"ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ᴏᴛᴘ sᴇɴᴛ ᴛᴏ {phone_number}.",
            filters=filters.text,
            timeout=600,
        )
        if await cancelled(otp):
            return
        otp = otp.text.replace(" ", "")

        # Sign in using OTP
        await client.sign_in(phone_number, code.phone_code_hash, otp)

        # Generate and send session string
        string_session = await client.export_session_string()
        await Bad.send_message(
            user_id,
            f"ʜᴇʀᴇ ɪs ʏᴏᴜʀ {ty} sᴛʀɪɴɢ sᴇssɪᴏɴ\n\n<code>{string_session}</code>",
        )
    except Exception as ex:
        await Bad.send_message(user_id, f"ᴇʀʀᴏʀ: <code>{str(ex)}</code>")
    finally:
        await client.disconnect()
