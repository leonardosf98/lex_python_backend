import requests
import logging
from datetime import datetime, date, time as dtime

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

API_URL = ""

SHIFT_START = dtime(9, 0)
SHIFT_END = dtime(18, 0)


SHIFT_START = dtime(9, 0)
SHIFT_END = dtime(18, 0)

def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        "sessionState": {
            "dialogAction": {"type": "ElicitSlot", "slotToElicit": slot_to_elicit},
            "intent": {"name": intent_name, "slots": slots},
            "sessionAttributes": session_attributes,
        },
        "messages": [{"contentType": "PlainText", "content": message}],
    }

def close(session_attributes, intent_name, slots, fulfillment_state, message):
    return {
        "sessionState": {
            "dialogAction": {"type": "Close"},
            "intent": {"name": intent_name, "slots": slots, "state": fulfillment_state},
            "sessionAttributes": session_attributes,
        },
        "messages": [{"contentType": "PlainText", "content": message}],
    }

def lambda_handler(event, context):
    logger.debug(f"Received event: {event}")

    intent_name = event["sessionState"]["intent"]["name"]
    slots = event["sessionState"]["intent"]["slots"]
    session_attributes = event.get("sessionState", {}).get("sessionAttributes", {})

    appointment_type = slots.get("AppointmentType", {}).get("value", {}).get("interpretedValue")
    appointment_date = slots.get("Date", {}).get("value", {}).get("interpretedValue")
    appointment_time = slots.get("Time", {}).get("value", {}).get("interpretedValue")

    if appointment_date:
        today = date.today()
        selected_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()

        if selected_date < today:
            return elicit_slot(session_attributes, intent_name, slots, "Date",
                               "A data escolhida já passou. Por favor, informe outra data.")

        if selected_date.weekday() == 6:
            return elicit_slot(session_attributes, intent_name, slots, "Date",
                               "O dentista não atende aos domingos. Escolha outro dia, por favor.")

    if appointment_date and appointment_time:
        selected_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()
        selected_time = datetime.strptime(appointment_time, "%H:%M").time()

        if selected_date == date.today() and selected_time <= datetime.now().time():
            return elicit_slot(session_attributes, intent_name, slots, "Time",
                               "O horário informado já passou para hoje. Escolha outro horário.")

        if not (SHIFT_START <= selected_time <= SHIFT_END):
            return elicit_slot(session_attributes, intent_name, slots, "Time",
                               "O horário deve ser entre 09:00 e 18:00. Informe outro horário, por favor.")

    if appointment_date and appointment_time and appointment_type:
        try:
            payload = {
                "date": appointment_date,
                "time": appointment_time,
                "appointment_type": appointment_type
            }
            response = requests.post(f"{API_URL}/appointments", json=payload)

            if response.status_code == 200:
                return close(
                    session_attributes,
                    intent_name,
                    slots,
                    "Fulfilled",
                    f"Sua consulta de {appointment_type} foi marcada para {appointment_date} às {appointment_time}."
                )
            else:
                return close(
                    session_attributes,
                    intent_name,
                    slots,
                    "Failed",
                    f"Ocorreu um erro ao registrar a consulta: {response.json().get('detail', 'Erro desconhecido')}"
                )
        except Exception as e:
            logger.error(f"Erro ao chamar API: {e}")
            return close(
                session_attributes,
                intent_name,
                slots,
                "Failed",
                "Não foi possível registrar a consulta no momento. Tente novamente mais tarde."
            )

    return elicit_slot(session_attributes, intent_name, slots, "Date", "Para quando devo marcar sua consulta?")