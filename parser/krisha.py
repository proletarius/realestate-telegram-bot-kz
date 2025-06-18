import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import re
import unidecode

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

    # Транслитерация кириллицы → латиница
    latin_city = unidecode.unidecode(city)
    # Удалим лишние символы
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


def build_search_url(city, operation_type, property_type, rooms, max_price):
    operation_map = {
        "аренда": "arenda",
        "покупка": "prodazha"
    }

    property_map = {
            "квартира": "kvartiry",
            "дом": "doma"
        }

    op = operation_map.get(operation_type.lower(), "arenda")
    prop = property_map.get(property_type.lower(), "kvartiry")
    city_slug = normalize_city(city)


    query = {
        "das[rooms]": rooms,
        "das[price][to]": max_price
    }
 
    return f"{BASE_URL}/{op}/{prop}/{city_slug}/?{urlencode(query)}"


async def parse_krisha(city, operation_type, property_type, rooms, max_price):
    url = build_search_url(city, operation_type, property_type, rooms, max_price)
    print("🔗 URL:", url)

    html = await fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")

    cards = soup.select("div.a-card")
    print(f"🔍 Найдено карточек: {len(cards)}")

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

            items.append({
                "title": title,
                "price": price,
                "url": full_url,
                "address": address,
                "description": description
            })
        except Exception as e:
            print("⚠️ Ошибка при парсинге объявления:", e)
            continue

    return items

"""
if __name__ == "__main__":
    import asyncio
    results = asyncio.run(parse_krisha(
        city="Алматы",
        operation_type="покупка",
        property_type="квартира",
        rooms=3,
        max_price=1500000
    ))

    for r in results:
        print(f"{r['price']} — {r['title']}")
        print(f"{r['address']}")
        print(f"{r['url']}")
        print(f"{r['description']}\n")
"""