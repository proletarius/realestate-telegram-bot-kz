import asyncio
import os
import logging
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from sqlalchemy import select
from db.database import AsyncSessionLocal
from db.models import Preference, SentAd, User
from parser.krisha import parse_krisha
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.utils.logging import setup_logging  # обновлённая функция логирования


load_dotenv()

# Настройка логов и конфигурации
setup_logging()
logger = logging.getLogger(__name__)

# Конфигурация бота
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def send_ads_to_users():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Preference).join(User))
        preferences = result.scalars().all()

        total_sent = 0

        for pref in preferences:
            user_id = pref.user_id
            try:
                listings = await parse_krisha(
                    city=pref.city,
                    operation_type=pref.operation_type,
                    property_type=pref.property_type,
                    rooms=pref.rooms,
                    max_price=pref.max_price,
                    search_text=pref.search_text,
                    year_built=pref.year_built,
                    land_type=pref.land_type
                )

                user_sent = 0
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
                        f"\U0001F4CD {ad['address']}\n"
                        f"\U0001F4B0 {ad['price']}\n\n"
                        f"{ad['description']}\n"
                        f"<a href=\"{ad['url']}\">\U0001F517 Смотреть объявление</a>"
                    )

                    await bot.send_message(chat_id=user_id, text=text, disable_web_page_preview=True)

                    session.add(SentAd(user_id=user_id, ad_url=ad["url"]))
                    await session.commit()
                    await asyncio.sleep(1)

                    logger.info(f"✅ Отправлено пользователю {user_id}: {ad['url']}")
                    user_sent += 1
                    total_sent += 1

                if user_sent:
                    logger.info(f"📨 Всего {user_sent} объявлений отправлено пользователю {user_id}")

            except Exception as e:
                logger.error(f"Ошибка для пользователя {user_id}: {e}")
                
        logger.info(f"📊 Итого отправлено {total_sent} новых объявлений")


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_ads_to_users, trigger="interval", minutes=15)
    scheduler.start()
    logger.info("✅ Планировщик запущен — рассылка каждые 15 минут")

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
