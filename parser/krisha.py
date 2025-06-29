import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import re
import unidecode
import logging
from bot.utils.logging import setup_logging  # обновлённая функция логирования

# Настройка логов и конфигурации
setup_logging()
logger = logging.getLogger(__name__)

BASE_URL = "https://krisha.kz"

CITY_MAP = {
    "астана": "astana",
    "алматы": "almaty",
    "шымкент": "shymkent",
    "караганда": "karaganda",
    "актобе": "aktobe",
    "атырау": "atyrau",
    "усть-Каменогорск": "oskemen",
    "павлодар": "pavlodar",
    "тараз": "taraz",
    "костанай": "kostanay"
    # остальные по мере необходимости
}

def normalize_city(city: str) -> str:
    city = city.strip().lower()
    if city in CITY_MAP:
        return CITY_MAP[city]

    latin_city = unidecode.unidecode(city)
    latin_city = re.sub(r"[^a-z0-9-]", "", latin_city)
    return latin_city or "astana"

async def fetch_html(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
        ),
        "Accept-Language": "ru-RU,ru;q=0.9",
        "Accept": "text/html,application/xhtml+xml"
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            return await resp.text()

def build_search_url(city, operation_type, property_type, rooms, max_price, search_text=None, year_built=None, land_type=None):
    operation_map = {
        "аренда": "arenda",
        "покупка": "prodazha"
    }

    city_slug = normalize_city(city)
    op = operation_map.get(operation_type.lower(), "arenda")
    prop = "doma-dachi" if property_type == "дом" else "kvartiry"

    query = {}

    if max_price is not None:
        query["das[price][to]"] = max_price

    if rooms is not None:
        if property_type == "дом":
            query["das[live.rooms]"] = rooms
        else:
            query["das[rooms]"] = rooms

    if year_built and property_type == "дом":
        query["das[house.year][from]"] = year_built

    txt_parts = []
    if land_type == "ИЖС" and property_type == "дом":
        txt_parts.append("ИЖС")

    if search_text:
        txt_parts.extend(search_text.strip().split())

    manual_keywords = txt_parts[1:] if txt_parts else []

    if txt_parts:
        query["_txt_"] = txt_parts[0]  # Только первое слово — для Krisha

    url = f"{BASE_URL}/{op}/{prop}/{city_slug}/?{urlencode(query)}"
    return url, manual_keywords

async def parse_krisha(city, operation_type, property_type, rooms, max_price, search_text=None, year_built=None, land_type=None):
    url, manual_keywords = build_search_url(city, operation_type, property_type, rooms, max_price, search_text, year_built, land_type)
    logger.info("🔗 Krisha URL: %s", url)

    html = await fetch_html(url)
    if not html:
        logger.error("❌ Пустой HTML с URL: %s", url)
        return []

    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("div.a-card")

    if not cards:
        logger.error("❌ Krisha не вернула ни одной карточки! Возможно, сайт изменился или фильтр слишком узкий.")
    else:
        logger.info("🔍 Найдено карточек: %d", len(cards))

    items = []
    for card in cards:
        try:
            title_el = card.select_one("a.a-card__title")
            price_el = card.select_one("div.a-card__price")
            address_el = card.select_one("div.a-card__subtitle")
            desc_el = card.select_one("div.a-card__text-preview")

            if not title_el or not price_el:
                continue

            title = title_el.get_text(strip=True)
            price = price_el.get_text(strip=True)
            address = address_el.get_text(strip=True) if address_el else ""
            description = desc_el.get_text(strip=True) if desc_el else ""
            relative_url = title_el.get("href", "")
            full_url = BASE_URL + relative_url if relative_url.startswith("/") else relative_url

            full_text = f"{title.lower()} {description.lower()}"

            if manual_keywords and not all(kw.lower() in full_text for kw in manual_keywords):
                continue

            items.append({
                "title": title,
                "price": price,
                "url": full_url,
                "address": address,
                "description": description
            })

        except Exception as e:
            logger.warning("⚠️ Ошибка при парсинге карточки: %s", e)
            continue

    logger.info("✅ Отобрано %d карточек по фильтру", len(items))
    return items
