# models.py

from pydantic import BaseModel
from datetime import datetime
import random

class MachineStatus(BaseModel):
    factory: str
    machine_id: str
    temperature: float
    vibration: float
    status: str
    timestamp: int

    @classmethod
    def factory_example(cls):
        return cls(
            factory=random.choice(["A", "B", "C", "D"]),
            machine_id=f"M{random.randint(1,9)}",
            temperature=round(random.uniform(60, 100), 1),
            vibration=round(random.uniform(0.1, 1.5), 2),
            status=random.choice(["OK", "WARNING", "ERROR"]),
            timestamp=int(datetime.utcnow().timestamp() * 1000)
        )
