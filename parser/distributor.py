import asyncio
from aiogram import Bot
from sqlalchemy import select
from db.database import AsyncSessionLocal
from db.models import Preference, User
from parser.krisha import parse_krisha
from dotenv import load_dotenv
import os

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))

# временно: список уже отправленных URL
sent_ads = set()

async def send_ads_to_users():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Preference).join(User))
        preferences = result.scalars().all()

        for pref in preferences:
            user_id = pref.user_id
            try:
                listings = await parse_krisha(
                    city=pref.city,
                    operation_type=pref.operation_type,
                    rooms=pref.rooms,
                    max_price=pref.max_price
                )

                for ad in listings:
                    if ad["url"] in sent_ads:
                        continue

                    text = (
                        f"<b>{ad['title']}</b>\n"
                        f"📍 {ad['address']}\n"
                        f"💰 {ad['price']}\n\n"
                        f"{ad['description']}\n"
                        f"<a href=\"{ad['url']}\">🔗 Смотреть объявление</a>"
                    )

                    await bot.send_message(chat_id=user_id, text=text, parse_mode="HTML", disable_web_page_preview=True)
                    sent_ads.add(ad["url"])
                    await asyncio.sleep(1)  # чтобы не спамить

            except Exception as e:
                print(f"⚠️ Ошибка отправки пользователю {user_id}: {e}")

if __name__ == "__main__":
    asyncio.run(send_ads_to_users())