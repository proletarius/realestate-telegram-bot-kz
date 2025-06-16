from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import JSONB
import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)  # Telegram user_id
    username = Column(String, nullable=True)
    is_premium = Column(Boolean, default=False)
    subscription_until = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    preferences = relationship("Preference", back_populates="user")


class Preference(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    city = Column(String)
    min_price = Column(Integer)
    max_price = Column(Integer)
    rooms = Column(Integer)
    districts = Column(JSONB)  # Список районов
    property_type = Column(String)  # "flat" / "house"

    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    user = relationship("User", back_populates="preferences")


class Listing(Base):
    __tablename__ = "listings"

    id = Column(String, primary_key=True)  # krisha_id или hash URL
    source = Column(String)  # krisha / olx / telegram
    url = Column(String, unique=True)
    price = Column(Integer)
    rooms = Column(Integer)
    city = Column(String)
    district = Column(String)
    description = Column(Text)
    photo_url = Column(String, nullable=True)
    date_published = Column(DateTime)
    raw_data = Column(JSONB)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))


class NotificationSent(Base):
    __tablename__ = "notifications_sent"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    listing_id = Column(String)
    sent_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
