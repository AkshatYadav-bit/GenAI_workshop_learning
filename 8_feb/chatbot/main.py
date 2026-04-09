def chatbot():
    print("Hello! I'm a chatbot. How can I assist you today?")
    while True:
        user_input = input("You: ")
        if 'exit'  in  user_input.lower() or 'quit'  in  user_input.lower() or  'bye' in  user_input.lower():
            print("Chatbot: Goodbye! Have a great day!")
            break
        elif "hello" in user_input or "hi" in user_input:
            print(f"Chatbot: hello! how can i help you?")
        elif "how are you" in user_input:
            print("Chatbot: i am doing fine.")
        elif "your name" in user_input:
            print("Chatbot: I am simple chatbot")
        elif "help" in user_input:
            print("Chatbot: yes tell your query")
        else:
            print("Chatbot: sorry I don't understand")

def main():
    chatbot()

if __name__ == "__main__":
    main()
