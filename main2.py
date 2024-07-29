import os
import google.generativeai as genai
import random

# This is the key generated from Gemini Google AI studio 
# Link: https://aistudio.google.com/app/apikey
google_api_key = os.getenv("GOOGLE_API_KEY")

# Configure API key for Google Generative AI
genai.configure(api_key=google_api_key)

# Function to convert text to plain format
def to_plain_text(text):
    lines = text.split('\n')
    formatted_lines = []
    for line in lines:
        line = line.strip()
        if line.startswith('*'):
            line = '- ' + line[1:].strip()
        formatted_lines.append(line)
    return '\n'.join(formatted_lines)

# Function to generate empathetic response
def generate_response(user_input):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"Empathize with the user and provide healthcare advice based on their input: {user_input}")
    return to_plain_text(response.text)

# Function to generate follow-up question
def generate_follow_up_question(user_input):
    model = genai.GenerativeModel('gemini-1.5-flash')
    follow_up = model.generate_content(f"Generate a follow-up question related to healthcare based on: {user_input}")
    return to_plain_text(follow_up.text)

# Function to generate options based on user input
def generate_options(user_input):
    model = genai.GenerativeModel('gemini-1.5-flash')
    options = model.generate_content(f"Generate options for follow-up based on: {user_input} only about health")
    return to_plain_text(options.text)

# Function to display the main menu
def main_menu():
    greetings = ["Hello there! How can I help you today?", "Welcome! I'm here to assist you with your health journey. What can I do for you?", "Hi! I'm excited to connect with you. How are you feeling today?"]
    print(random.choice(greetings))

def healthcare_advice(user_input):
    response = generate_response(user_input)
    print(f"{response} I am here to help. Can you please tell me more about your symptoms?")

    follow_up_question = generate_follow_up_question(user_input)
    print(follow_up_question)

    follow_up_response = input("You: ").strip().lower()
    response = generate_response(follow_up_response)
    print(response)

    options = generate_options(follow_up_response)
    print("Please select an option:")
    print(options)

    user_option = input("Select an option: ").strip().lower()

    # In a real scenario, you would process this option further. For now, just acknowledge the selection
    if user_option not in options.lower().split():
        print("Invalid option. Please select a valid option.")
        healthcare_advice(follow_up_response)
    else:
        response = generate_response(user_option)
        print(response)
        
        post_advice_options()

def post_advice_options():
    print("1. Great! Would you like to go back to the main menu or exit?")
    print("a) Main menu")
    print("b) Exit")

    option = input("Select an option (a, b): ").strip().lower()

    if option == 'a':
        main()
    elif option == 'b':
        print("Thank you! Take care and see a doctor if symptoms persist. Goodbye!")
        exit()
    else:
        print("Invalid option. Please select a valid option (a, b).")
        post_advice_options()

def main():
    main_menu()

    user_input = input("You: ").strip().lower()

    healthcare_advice(user_input)

if __name__ == "__main__":
    main()
