from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ws_manager import ConnectionManager
from models import MachineStatus
from database import engine, SessionLocal
from models_db import Telemetry
import asyncio

# Initialize FastAPI app
app = FastAPI()

# Create DB tables (only once)
Telemetry.metadata.create_all(bind=engine)

# WebSocket manager
manager = ConnectionManager()

@app.get("/")
def root():
    return {"message": "Daikibo Dashboard Backend Running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    print("👋 WebSocket client connected")

    try:
        while True:
            await asyncio.sleep(5)

            # Generate simulated telemetry
            data = MachineStatus.factory_example()
            print("📦 Sending telemetry:", data.dict())

            # Save to SQLite database
            db = SessionLocal()
            try:
                db_entry = Telemetry(
                    factory=data.factory,
                    machine_id=data.machine_id,
                    temperature=data.temperature,
                    vibration=data.vibration,
                    status=data.status
                )
                db.add(db_entry)
                db.commit()
                print("💾 Inserted into DB")
            finally:
                db.close()

            # Broadcast to frontend
            await manager.broadcast(data.json())

    except WebSocketDisconnect:
        print("❌ WebSocket disconnected")
        manager.disconnect(websocket)
    except Exception as e:
        print("❌ WebSocket error:", e)

# ✅ REST API to fetch latest telemetry history
@app.get("/history")
def get_machine_history(machine_id: str = Query(...), limit: int = 10):
    db: Session = SessionLocal()
    try:
        results = (
            db.query(Telemetry)
            .filter(Telemetry.machine_id == machine_id)
            .order_by(Telemetry.timestamp.desc())
            .limit(limit)
            .all()
        )
        return JSONResponse(content=[
            {
                "id": r.id,
                "factory": r.factory,
                "machine_id": r.machine_id,
                "temperature": r.temperature,
                "vibration": r.vibration,
                "status": r.status,
                "timestamp": r.timestamp.isoformat()
            }
            for r in results
        ])
    finally:
        db.close()
