from database import SessionLocal
from models_db import Telemetry

db = SessionLocal()
try:
    records = db.query(Telemetry).all()
    for r in records:
        print(r.id, r.factory, r.machine_id, r.status)
finally:
    db.close()
