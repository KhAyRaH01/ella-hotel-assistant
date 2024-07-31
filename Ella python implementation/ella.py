#Imported necessary packages
import ella3
import os
import google.generativeai as genai
from textblob import TextBlob

#get api key by environment file
google_api_key = os.getenv("GOOGLE_API_KEY")

# Configure API key for Google Generative AI
genai.configure(api_key= google_api_key)

# convert text to plain format
def to_plain_text(text):
    lines = text.split('\n')
    formatted_lines = []
    for line in lines:
        line = line.strip()
        if line.startswith('*'):
            line = '- ' + line[1:].strip()
        formatted_lines.append(line)
    return '\n'.join(formatted_lines)

# generate response from the AI
def generate_response(user_input, context):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"{context} {user_input}"
    response = model.generate_content(prompt)
    return to_plain_text(response.text)

# analyze sentiment of user input
def analyze_sentiment(user_input):
    analysis = TextBlob(user_input)
    sentiment = analysis.sentiment.polarity
    if sentiment > 0:
        return "positive"
    elif sentiment < 0:
        return "negative"
    else:
        return "neutral"

# handle predefined questions and hotel details
def handle_hotel_details():
    print("Hello! I am Ella, your best hotel assistant to find any hotel in Nigeria.")
    print("You can ask me about hotels in Nigeria, and I'll provide you with detailed information.")

    while True:
        print("\nPlease choose one of the following options:")
        print("1. Find out hotel around you")
        print("2. Get recommendations based on budget")
        print("3. Exit")

        option = input("Select an option (1, 2, 3): ").strip()

        if option == '1':
           ella3.main()
      
        elif option == '2':
            print("Please enter your preferred hotel destination.")
            destination = input("You: ").strip()
            print("Great! Now please select your budget range:")
            print("1. High budget (over $300 per night)")
            print("2. Mid budget ($150 - $300 per night)")
            print("3. Low budget (below $150 per night)")

            budget = input("Select an option (1, 2, 3): ").strip()
            if budget == '1':
                budget_range = "high budget"
            elif budget == '2':
                budget_range = "mid budget"
            elif budget == '3':
                budget_range = "low budget"
            else:
                print("Invalid budget option. Please try again.")
                continue

            # Generate recommendations from AI based on location and budget
            response = generate_response(destination, f"Provide hotel recommendations in {destination} for a {budget_range} range. Include address and features if possible.")
            print(f"Response from Ella:\n{response}")

        elif option == '3':
            print("Thank you! Feel free to ask if you need more information about hotels in Nigeria. Goodbye!")
            break

        else:
            print("Invalid option. Please select a valid option (1, 2, 3).")
            continue

        # Satisfaction question with sentiment analysis
        print("\nHow satisfied are you with the information provided by Ella? \nAnswer(Satisfied, Not satisfied, Neutral)")
        satisfaction = input("You: ").strip()
        sentiment = analyze_sentiment(satisfaction)
        
        if sentiment == "positive":
            print("Thank you for your feedback! We will continue to improve Ella's responses.")
        elif sentiment == "negative":
            print("Sorry to hear that you are not satisfied. Please provide more information about what we can help you with.")
        else:
            print("Thank you for your feedback! We will continue to improve Ella's responses.")


if __name__ == "__main__":
    handle_hotel_details()