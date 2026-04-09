def chatbot():
    isAskedForBooking = False
    common_place = []
    common_month = []      
    common_day = []
    print("Hello! I'm a ticketingbot. How can I assist you today?")
    while True:
        user_input = input("You: ")
        if not isAskedForBooking:
              isAskedForBooking = "book" in user_input.lower()
        user_words = user_input.lower().split()
        places = ["delhi", "mumbai", "bangalore", "chennai", "kolkata"]
        months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
        days = [str(i) for i in range(1, 32)]
        has_overlap = any(x in places for x in user_words)
        has_month = any(x in months for x in user_words)
        has_day = any(x in days for x in user_words)
        if(len(common_place)==0):
            common_place = list(set(places) & set(user_words))
        if(len(common_month)==0):
            common_month = list(set(months) & set(user_words))
        if(len(common_day)==0):
            common_day = list(set(days) & set(user_words))
        if (len(common_place) > 0 or len(common_month) > 0 or len(common_day) > 0):
             isAskedForBooking = True

        if 'exit'  in  user_input.lower() or 'quit'  in  user_input.lower() or  'bye' in  user_input.lower():
            print("Ticketingbot: Goodbye! Have a great journey!")
            break
        elif not isAskedForBooking and ("hello" in user_input or "hi" in user_input):
            print(f"Ticketingbot: hello! tell me which place you want to visit?")
        elif  not isAskedForBooking and "how are you" in user_input:
            print("Ticketingbot: i am doing fine.")
        elif not isAskedForBooking and "your name" in user_input:
            print("Ticketingbot: I am simple ticketingbot")
        elif not isAskedForBooking and "help" in user_input:
            print("Ticketingbot: yes tell your query")
        elif "cancel" in user_input:
            print("Ticketingbot: sure tell me your booking id")
        elif "reschedule" in user_input:
            print("Ticketingbot: sure tell me your booking id and new date of travel")
        elif isAskedForBooking and not has_overlap and not has_month and not has_day:
            print("Ticketingbot: sure tell me your destination and date of travel")
            isAskedForBooking = True 
        elif (isAskedForBooking and has_overlap and has_month and has_day) and (len(common_place) > 0 and len(common_month) > 0 and len(common_day) > 0):
                print(f"Ticketingbot: your ticket has been booked successfully to {', '.join(common_place)} on {common_month[0]} {common_day[0]}")
                common_place = []
                common_month = []       
                common_day = []
                isAskedForBooking = False
        elif (len(common_place) > 0 and len(common_month) > 0 and len(common_day) > 0):
                print(f"Ticketingbot: your ticket has been booked successfully to {', '.join(common_place)} on {common_month[0]} {common_day[0]}")
                common_place = []
                common_month = []       
                common_day = []
                isAskedForBooking = False
        elif isAskedForBooking and has_overlap and not has_month and not has_day:
                print("Ticketingbot: please specify the month and day of travel")
                isAskedForBooking = True 
        elif isAskedForBooking and has_overlap and has_month and not has_day:
                print("Ticketingbot: please specify the day of travel")
                isAskedForBooking = True 
        elif isAskedForBooking and not has_month:
                print("Ticketingbot: please specify the month of travel")
                isAskedForBooking = True 
        elif isAskedForBooking and not has_day:
                print("Ticketingbot: please specify the day of travel")
                isAskedForBooking = True
        elif isAskedForBooking and not has_overlap:
                print("Ticketingbot: sorry we don't have tickets to that destination")
                isAskedForBooking = True 
        else:
            print("Ticketingbot: sorry I don't understand")
        

def main():
    chatbot()

if __name__ == "__main__":
    main()
