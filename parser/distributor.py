import asyncio
import os
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from sqlalchemy import select
from db.database import AsyncSessionLocal
from db.models import Preference, SentAd, User
from parser.krisha import parse_krisha
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


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
                    property_type=pref.property_type,
                    rooms=pref.rooms,
                    max_price=pref.max_price
                )

                for ad in listings:
                    existing = await session.execute(
                        select(SentAd).where(
                            SentAd.user_id == user_id,
                            SentAd.ad_url == ad["url"]
                        )
                    )
                    if existing.first():
                        continue

                    text = (
                        f"<b>{ad['title']}</b>\n"
                        f"📍 {ad['address']}\n"
                        f"💰 {ad['price']}\n\n"
                        f"{ad['description']}\n"
                        f"<a href=\"{ad['url']}\">🔗 Смотреть объявление</a>"
                    )

                    await bot.send_message(chat_id=user_id, text=text, disable_web_page_preview=True)

                    session.add(SentAd(user_id=user_id, ad_url=ad["url"]))
                    await session.commit()
                    await asyncio.sleep(1)

            except Exception as e:
                print(f"⚠️ Ошибка при отправке пользователю {user_id}: {e}")


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_ads_to_users, trigger="interval", minutes=5)
    scheduler.start()
    print("✅ Планировщик запущен — рассылка каждые 5 минут")

    while True:
        await asyncio.sleep(3600)  # не даём скрипту завершиться


if __name__ == "__main__":
    asyncio.run(main())