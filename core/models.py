from sqlalchemy import Column, Integer, String, Boolean
from core.database import Base


class URL(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    last_status = Column(String, default='unknown')
