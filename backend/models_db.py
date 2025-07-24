from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from datetime import datetime

class Telemetry(Base):
    __tablename__ = "telemetry"

    id = Column(Integer, primary_key=True, index=True)
    factory = Column(String)
    machine_id = Column(String)
    temperature = Column(Float)
    vibration = Column(Float)
    status = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
