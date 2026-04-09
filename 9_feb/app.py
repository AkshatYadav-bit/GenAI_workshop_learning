import uuid
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- STATE ----
# Tracks current user intent and extracted information
state = {
    "intent": None,        # "book", "cancel", "reschedule"
    "destination": None,
    "month": None,
    "day": None,
    "booking_id": None
}

# IN-MEMORY DATABASE
# Stores all bookings using booking_id as key
bookings = {}


# STATIC DATA 
places = {"delhi", "mumbai", "bangalore", "chennai", "kolkata"}
months = {
    "january","february","march","april","may","june",
    "july","august","september","october","november","december"
}
days = {str(i) for i in range(1, 32)}
 
# REQUEST MODEL
class Message(BaseModel):
    text: str

@app.get("/bookings")
def get_bookings():
    return bookings

# Reset conversation state after completing an operation
def reset_state():
    for key in state:
        state[key] = None

# Extract entities from user input
def extract_entities(words):
    place = next((w for w in words if w in places), None)
    month = next((w for w in words if w in months), None)
    day = next((w for w in words if w in days), None)
    return place, month, day

# Generate unique booking ID
def generate_booking_id():
    return str(uuid.uuid4())[:8]

#  MAIN LOOP
@app.post('/chat')
def process_message(msg:Message):
    user_input = msg.text.lower()
    if not user_input.strip():
        return {"reply": "Please enter a message."}
    words = user_input.split()

    # EXIT CONDITION
    if any(x in user_input for x in ["exit", "quit", "bye"]):
        return {"reply":"TicketingBot: Goodbye!"}
        
    

    # ENTITY EXTRACTION 
    place, month, day = extract_entities(words)

    if place:
        state["destination"] = place
    if month:
        state["month"] = month
    if day:
        state["day"] = day


    # INTENT DETECTION
    if "book" in user_input:
        state["intent"] = "book"

    elif "cancel" in user_input:
        state["intent"] = "cancel"
        return {"reply": "Please provide booking ID."}

    elif "reschedule" in user_input:
        state["intent"] = "reschedule"


    # AUTO-TRIGGER BOOKING
    if state["intent"] is None:
        if place or month or day:
            state["intent"] = "book"

            if place:
                state["destination"] = place
            if month:
                state["month"] = month
            if day:
                state["day"] = day

    # BOOKING FLOW 
    if state["intent"] == "book":

        # Validate destination
        if not state["destination"]:
            return {"reply":"TicketingBot: Please provide destination."}

        if state["destination"] not in places:
            reset_state()
            return {"reply":"TicketingBot: Destination not supported."}

        # Validate month
        if not state["month"]:
            return {"reply":"TicketingBot: Please provide travel month."}

        # Validate day
        if not state["day"]:
            return {"reply":"TicketingBot: Please provide travel day."}

        # Create booking
        booking_id = generate_booking_id()

        bookings[booking_id] = {
            "destination": state["destination"],
            "month": state["month"],
            "day": state["day"]
        }

        reply = f"Booking confirmed. ID: {booking_id}, {state['destination']} on {state['month']} {state['day']}"

        reset_state()
        return {"reply": reply}

    #  CANCELLATION FLOW 
    if state["intent"] == "cancel":

        # Try to find booking ID in input
        possible_id = next((w for w in words if w in bookings), None)

        if possible_id:
            del bookings[possible_id]
            reset_state()
            return {"reply":f"TicketingBot: Booking {possible_id} has been cancelled."}
            
        else:
            return {"reply":"TicketingBot: Please provide a valid booking ID."}

    # RESCHEDULE FLOW 
    if state["intent"] == "reschedule":

        # Extract booking ID
        possible_id = next((w for w in words if w in bookings), None)

        if not possible_id:
            return {"reply":"TicketingBot: Please provide a valid booking ID."}

        # Validate new date
        if not state["month"]:
            return {"reply":"TicketingBot: Please provide new month."}

        if not state["day"]:
            return {"reply":"TicketingBot: Please provide new day."}

        # Update booking
        bookings[possible_id]["month"] = state["month"]
        bookings[possible_id]["day"] = state["day"]

        reply = f"Booking {possible_id} updated to {state['month']} {state['day']}"


        reset_state()
        return {"reply": reply}

    # DEFAULT RESPONSE
    return {"reply": "TicketingBot: I can help you book, cancel, or reschedule tickets."}
