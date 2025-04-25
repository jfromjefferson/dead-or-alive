from sqlalchemy import Column, Integer, String, Boolean, DATETIME, func
from core.database import Base


class URL(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    last_status = Column(String, default='unknown')
    last_run = Column(DATETIME, nullable=True)
    created_at = Column(DATETIME, server_default=func.now())
