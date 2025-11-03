import datetime
from zoneinfo import ZoneInfo

# OBGYN Clinic In-Memory Storage
APPOINTMENT_DB = {"appointments": {}, "next_id": 1}
PATIENT_DB = {}  # Store patient information
CALL_LOG = []  # Log for tracking calls

# Available time slots for appointments (clinic hours: 8 AM - 5 PM, weekdays)
AVAILABLE_SLOTS = {
    "morning": ["8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM"],
    "afternoon": ["1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM"]
}


def lookup_time(timezone_offset=-4):
    """Get current time in specified timezone (EST/EDT by default).

    Args:
        timezone_offset: Hours offset from UTC (default -4 for EST/EDT)

    Returns:
        Dict with current time, day of week, and military time format
    """
    try:
        # Get current UTC time
        utc_now = datetime.datetime.now(datetime.timezone.utc)

        # Apply timezone offset
        est = utc_now.astimezone(ZoneInfo("America/New_York"))

        return {
            "current_time": est.strftime("%I:%M %p"),  # 12:34 PM
            "mil_time": float(est.strftime("%H.%M")),  # 12.34 format
            "mil_time_est": float(est.strftime("%H.%M")),
            "day_of_week": est.strftime("%A"),  # Monday, Tuesday, etc.
            "date": est.strftime("%m/%d/%Y"),
            "timezone": "EST/EDT",
            "is_office_open": est.weekday() < 5 and 8 <= est.hour < 17  # Mon-Fri, 8-5
        }
    except Exception as e:
        return {"error": f"Could not get time: {str(e)}"}


def schedule_appointment(patient_name, date, time, reason, phone=None):
    """Schedule a patient appointment.

    Args:
        patient_name: Full name of patient
        date: Appointment date (MM/DD/YYYY or "next Monday")
        time: Appointment time (hour number 8-17)
        reason: Reason for visit
        phone: Phone number (optional)

    Returns:
        Confirmation with appointment ID and details
    """
    try:
        appointment_id = APPOINTMENT_DB["next_id"]
        APPOINTMENT_DB["next_id"] += 1

        appointment = {
            "id": appointment_id,
            "patient_name": patient_name,
            "date": date,
            "time": time,
            "reason": reason,
            "phone": phone,
            "status": "confirmed",
            "created_at": datetime.datetime.now().isoformat()
        }

        APPOINTMENT_DB["appointments"][appointment_id] = appointment

        return {
            "success": True,
            "appointment_id": appointment_id,
            "message": f"Appointment confirmed for {patient_name} on {date} at {time}",
            "reason": reason,
            "status": "confirmed"
        }
    except Exception as e:
        return {"error": f"Could not schedule appointment: {str(e)}"}


def lookup_appointment(appointment_id):
    """Look up appointment details by ID.

    Args:
        appointment_id: The appointment ID to look up

    Returns:
        Appointment details or error message
    """
    try:
        appointment_id = int(appointment_id)
        appointment = APPOINTMENT_DB["appointments"].get(appointment_id)

        if appointment:
            return {
                "appointment_id": appointment_id,
                "patient_name": appointment["patient_name"],
                "date": appointment["date"],
                "time": appointment["time"],
                "reason": appointment["reason"],
                "status": appointment["status"]
            }
        return {"error": f"Appointment {appointment_id} not found"}
    except Exception as e:
        return {"error": f"Could not lookup appointment: {str(e)}"}


def transfer_call(reason="Patient requested transfer to live agent"):
    """Transfer call to live agent.

    Args:
        reason: Reason for transfer

    Returns:
        Transfer confirmation
    """
    return {
        "action": "transfer_to_agent",
        "message": "Transferring to live agent. Please hold.",
        "reason": reason,
        "status": "transferring"
    }


def end_call_emergency(emergency_type="severe_medical"):
    """End call and route to emergency services.

    Args:
        emergency_type: Type of emergency situation

    Returns:
        Emergency routing confirmation
    """
    return {
        "action": "end_call_emergency",
        "message": "Please go to the nearest emergency room or call 911 immediately.",
        "emergency_type": emergency_type,
        "status": "emergency_routed"
    }


def end_call_tool(reason="Call ended normally"):
    """End the call normally.

    Args:
        reason: Reason for ending call

    Returns:
        Call termination confirmation
    """
    return {
        "action": "end_call",
        "message": "Thank you for calling Capital Women's Care Ashburn. Goodbye.",
        "reason": reason,
        "status": "call_ended"
    }


def get_available_slots(date):
    """Get available appointment slots for a specific date.

    Args:
        date: Date to check availability (MM/DD/YYYY format)

    Returns:
        List of available time slots
    """
    # In a real system, this would check against a database
    # For now, return standard available slots
    return {
        "date": date,
        "available_slots": AVAILABLE_SLOTS["morning"] + AVAILABLE_SLOTS["afternoon"],
        "office_hours": "8:00 AM - 5:00 PM"
    }


# Function mapping dictionary for Deepgram agent
FUNCTION_MAP = {
    'lookup_time': lookup_time,
    'schedule_appointment': schedule_appointment,
    'lookup_appointment': lookup_appointment,
    'transfer_call': transfer_call,
    'end_call_emergency': end_call_emergency,
    'end_call_tool': end_call_tool,
    'get_available_slots': get_available_slots
}