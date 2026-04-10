import uuid

# state  = {}
# bookings = {}

def chatbot():
    print("Hello! I'm TicketingBot. How can I assist you today?")

    # ---- STATE ----
    # Tracks current user intent and extracted information
    state = {
        "intent": None,        # "book", "cancel", "reschedule"
        "destination": None,
        "month": None,
        "day": None,
        "booking_id": None
    }

    # ---- IN-MEMORY DATABASE ----
    # Stores all bookings using booking_id as key
    bookings = {}

    # ---- STATIC DATA ----
    places = {"delhi", "mumbai", "bangalore", "chennai", "kolkata"}
    months = {
        "january","february","march","april","may","june",
        "july","august","september","october","november","december"
    }
    days = {str(i) for i in range(1, 32)}

    # ---- HELPER FUNCTIONS ----

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

    # ---- MAIN LOOP ----
    while True:
        user_input = input("You: ").lower()
        words = user_input.split()

        # ---- EXIT CONDITION ----
        if any(x in user_input for x in ["exit", "quit", "bye"]):
            print("TicketingBot: Goodbye!")
            break
        

        # ---- ENTITY EXTRACTION ----
        place, month, day = extract_entities(words)

        if place:
            state["destination"] = place
        if month:
            state["month"] = month
        if day:
            state["day"] = day


        # ---- INTENT DETECTION ----
        if "book" in user_input:
            state["intent"] = "book"

        elif "cancel" in user_input:
            state["intent"] = "cancel"

        elif "reschedule" in user_input:
            state["intent"] = "reschedule"


        # ---- AUTO-TRIGGER BOOKING ----
        if state["intent"] is None:
            if place or month or day:
                state["intent"] = "book"

                if place:
                    state["destination"] = place
                if month:
                    state["month"] = month
                if day:
                    state["day"] = day

        # ---- BOOKING FLOW ----
        if state["intent"] == "book":

            # Validate destination
            if not state["destination"]:
                print("TicketingBot: Please provide destination.")
                continue

            if state["destination"] not in places:
                print("TicketingBot: Destination not supported.")
                reset_state()
                continue

            # Validate month
            if not state["month"]:
                print("TicketingBot: Please provide travel month.")
                continue

            # Validate day
            if not state["day"]:
                print("TicketingBot: Please provide travel day.")
                continue

            # Create booking
            booking_id = generate_booking_id()

            bookings[booking_id] = {
                "destination": state["destination"],
                "month": state["month"],
                "day": state["day"]
            }

            print(f"TicketingBot: Booking confirmed.")
            print(f"Booking ID: {booking_id}")
            print(f"Destination: {state['destination']}")
            print(f"Date: {state['month']} {state['day']}")

            reset_state()
            continue

        # ---- CANCELLATION FLOW ----
        if state["intent"] == "cancel":

            # Try to find booking ID in input
            possible_id = next((w for w in words if w in bookings), None)

            if possible_id:
                del bookings[possible_id]
                print(f"TicketingBot: Booking {possible_id} has been cancelled.")
                reset_state()
            else:
                print("TicketingBot: Please provide a valid booking ID.")
            continue

        # ---- RESCHEDULE FLOW ----
        if state["intent"] == "reschedule":

            # Extract booking ID
            possible_id = next((w for w in words if w in bookings), None)

            if not possible_id:
                print("TicketingBot: Please provide a valid booking ID.")
                continue

            # Validate new date
            if not state["month"]:
                print("TicketingBot: Please provide new month.")
                continue

            if not state["day"]:
                print("TicketingBot: Please provide new day.")
                continue

            # Update booking
            bookings[possible_id]["month"] = state["month"]
            bookings[possible_id]["day"] = state["day"]

            print(f"TicketingBot: Booking {possible_id} has been updated.")
            print(f"New Date: {state['month']} {state['day']}")

            reset_state()
            continue

        # ---- DEFAULT RESPONSE ----
        print("TicketingBot: I can help you book, cancel, or reschedule tickets.")


def main():
    chatbot()


if __name__ == "__main__":
    main()