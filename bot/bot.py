import asyncio
import io

import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, InputFile

from bot.config import BOT_TOKEN, BACKEND_URL
from bot.keyboards import main_keyboard


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Привет! 👋\n\nНажми кнопку ниже, чтобы получить VPN.",
        reply_markup=main_keyboard()
    )


@dp.callback_query(lambda c: c.data == "get_vpn")
async def get_vpn(callback: CallbackQuery):
    telegram_id = callback.from_user.id

    await callback.answer("Создаю VPN, подожди пару секунд...")

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{BACKEND_URL}/vpn/create",
            json={"telegram_id": telegram_id},
        )

    if resp.status_code != 201:
        await callback.message.answer(
            "❌ Не удалось создать VPN. Попробуй позже."
        )
        return

    config_text = resp.json()["config"]

    conf_bytes = io.BytesIO(config_text.encode())

    document = InputFile(
        conf_bytes,
        filename="vpn.conf"
    )

    await callback.message.answer_document(
        document=document,
        caption="Готово! 📄\nИмпортируй файл в WireGuard."
    )

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
