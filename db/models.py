from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text, Float, UniqueConstraint, BigInteger
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import JSONB
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)  # Telegram user_id
    username = Column(String, nullable=True)
    is_premium = Column(Boolean, default=False)
    subscription_until = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.now(datetime.timezone.utc))

    preferences = relationship("Preference", back_populates="user")


class Preference(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    city = Column(String, nullable=False)
    operation_type = Column(String, nullable=False)  # аренда / покупка
    property_type = Column(String, nullable=False)        # квартира / дом
    max_price = Column(Integer, nullable=False)
    rooms = Column(Integer, nullable=True)
    search_text = Column(String, nullable=True)           # ключевые слова
    land_type = Column(String, nullable=True)             # ИЖС / None
    year_built = Column(Integer, nullable=True)           # 1970 / 1980 / ... / None

    created_at = Column(DateTime(timezone=True), default=datetime.datetime.now(datetime.timezone.utc))

    user = relationship("User", back_populates="preferences")


class SentAd(Base):
    __tablename__ = "sent_ads"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    ad_url = Column(String, nullable=False)
    sent_at = Column(DateTime(timezone=True), default=datetime.datetime.now(datetime.timezone.utc))

    __table_args__ = (UniqueConstraint("user_id", "ad_url", name="uix_user_ad"),)