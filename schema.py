from pydantic import BaseModel, constr

class Appointment(BaseModel):
    date: str
    time: str
    appointment_type: str