from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .user import User
from .message import Message