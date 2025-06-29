from sqlalchemy import delete
from db.models import Preference
from db.database import AsyncSessionLocal

async def save_filter(user_id, state):
    data = await state.get_data()

    async with AsyncSessionLocal() as session:
        await session.execute(delete(Preference).where(Preference.user_id == user_id))

        pref = Preference(
            user_id=user_id,
            city=data["city"],
            operation_type=data["operation_type"],
            property_type=data["property_type"],
            max_price=data["max_price"],
            rooms=data.get("rooms"),
            search_text=data.get("search_text"),
            land_type=data.get("land_type"),
            year_built=data.get("year_built")
        )
        session.add(pref)
        await session.commit()
