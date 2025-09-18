from fastapi import FastAPI, HTTPException
from datetime import datetime, time as dt_time
from schema import Appointment
import boto3

app = FastAPI()

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("Appointments")

SHIFT_START = dt_time(9, 0)
SHIFT_END = dt_time(18, 0)


@app.get("/appointments", response_model=list[Appointment])
def get_appointments():
    resp = table.scan()
    items = resp.get("Items", [])
    return items

@app.post("/appointments", response_model=Appointment)
def create_appointment(appointment: Appointment):
    date = appointment.date
    time_str = appointment.time
    appointment_type = appointment.appointment_type.strip()

    weekday = datetime.strptime(date, "%Y-%m-%d").weekday()
    if weekday == 6:
        raise HTTPException(status_code=400, detail="Dentista não atende aos domingos")

    hour_object = datetime.strptime(time_str, "%H:%M").time()
    if not (SHIFT_START <= hour_object <= SHIFT_END):
        raise HTTPException(status_code=400, detail="Fora do horário de atendimento (9h-18h)")

    existing = table.get_item(Key={"date": date, "time": time_str})
    if "Item" in existing:
        raise HTTPException(status_code=400, detail="Horário já ocupado")

    item = {"date": date, "time": time_str, "appointment_type": appointment_type}
    table.put_item(Item=item)
    return item