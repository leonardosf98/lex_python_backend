from fastapi import FastAPI, HTTPException
from datetime import datetime, time
from typing import List

app = FastAPI()

appointments = [] 

SHIFT_START = time(9, 0)
SHIFT_END = time(18, 0)

@app.get("/appointments", response_model=List[dict])
def get_appointments():
    return appointments

@app.post("/appointments")
def create_appointment(appointment: dict):
    date = appointment["date"]
    time = appointment["time"]

    weekday = datetime.strptime(date, "%Y-%m-%d").weekday()
    if weekday > 5:  
        raise HTTPException(status_code=400, detail="Nutricionista não atende aos domingos")

    hour_object = datetime.strptime(time, "%H:%M").time()
    if not (SHIFT_START <= hour_object <= SHIFT_END):
        raise HTTPException(status_code=400, detail="Fora do horário de atendimento (9h-18h)")

    for c in appointments:
        if c["date"] == date and c["time"] == time:
            raise HTTPException(status_code=400, detail="Horário já ocupado")

    appointments.append({"date": date, "time": time})
    return {"message": "appointment agendada com sucesso!"}
