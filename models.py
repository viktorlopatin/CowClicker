from base import engine, session

from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Boolean, not_
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from aiogram.types import Message
from datetime import datetime, timedelta
from MyCows.keyboards import step_1_keyboard, step_2_keyboard, step_3_keyboard

from langs import f

Base = declarative_base()


def format_timedelta(td):
    # Получаем часы, минуты и секунды из timedelta
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Формируем список частей, убирая нулевые
    parts = []
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
    if seconds > 0:
        parts.append(f"{seconds} second{'s' if seconds > 1 else ''}")

    # Объединяем части в строку
    return ", ".join(parts)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True)
    name = Column(String)
    username = Column(String)
    language_code = Column(String)
    datetime = Column(DateTime, default=datetime.now().date)

    cow_status = Column(Boolean, default=True)
    cow_datetime = Column(DateTime)
    milk = Column(Integer, default=0)

    def __init__(self, chat_id, name, username, language_code):
        self.chat_id = chat_id
        self.name = name
        self.username = username
        self.language_code = language_code
        self.datetime = datetime.now().date()
        self.cow_datetime = datetime.now() + timedelta(minutes=3)
        self.milk = 0

    @staticmethod
    def create(chat_id: int, name: str, username: str, language_code: str):
        user = User(chat_id, name, username, language_code)
        session.add(user)
        session.commit()
        return user

    @staticmethod
    def get_by_chat_id(chat_id: int):
        return session.query(User).filter_by(chat_id=chat_id).first()

    @staticmethod
    def get_or_create(message: Message):
        chat_id = message.chat.id
        name = message.from_user.full_name
        username = message.from_user.username
        language_code = message.from_user.language_code

        user = User.get_by_chat_id(chat_id)
        if user is None:
            user = User.create(chat_id, name, username, language_code)
        return user

    def get_cow_status(self):
        if not self.cow_status:
            return 1, 0, step_1_keyboard()
        last_time = self.cow_datetime - datetime.now()

        if last_time.total_seconds() > 0:
            return 2, format_timedelta(last_time), step_2_keyboard()
        return 3, format_timedelta(last_time), step_3_keyboard()

    def send_cow(self):
        self.cow_status = True
        self.cow_datetime = datetime.now() + timedelta(hours=3)
        session.commit()

    def set_premium_cow(self):
        self.cow_status = True
        self.cow_datetime = datetime.now()
        session.commit()

    def collect_milk(self):
        self.milk += 1
        self.cow_status = False
        session.commit()


Base.metadata.create_all(engine)
