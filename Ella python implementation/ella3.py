import googlemaps
import google.generativeai as genai
import os



gmapsKey = os.getenv('GOOGLE_MAPS_API_KEY')
# Initialize clients with your API keys
gmaps = googlemaps.Client(key=gmapsKey)


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

def get_hotels_near_location(location):
    # Geocode the input location
    geocode_result = gmaps.geocode(location)
    if not geocode_result:
        print("Location not found.")
        return None

    # Get the latitude and longitude
    latlng = geocode_result[0]['geometry']['location']
    lat, lng = latlng['lat'], latlng['lng']

    # Search for hotels nearby
    places_result = gmaps.places_nearby(location=(lat, lng), type='lodging', radius=5000)
    
    # List the hotels with numeric options
    hotels = []
    for i, place in enumerate(places_result['results'], start=1):
        hotels.append((i, place['name'], place['place_id']))
        print(f"{i}. {place['name']}")

    return hotels

def get_hotel_details(place_id):
    # Get details of a selected hotel
    place_details = gmaps.place(place_id=place_id)

    if not place_details or 'result' not in place_details:
        print("Hotel details not found.")
        return None

    details = place_details['result']
    name = details.get('name', 'N/A')
    price_level = details.get('price_level', 'N/A')
    features = ', '.join(details.get('types', []))
    rating = details.get('rating', 'N/A')

    return {
        'name': name,
        'price': price_level,
        'features': features,
        'rating': rating
    }

def generate_detailed_information(hotel_info):
    # Use generative AI to generate detailed information
    prompt = (
        f"Provide a detailed description of {hotel_info['name']}. "
        f"It has a price level of {hotel_info['price']}, features like {hotel_info['features']}, "
        f"and an average rating of {hotel_info['rating']}."
    )

    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return to_plain_text(response.text)

def main():
    location = input("Please Enter your current location: ")
    hotels = get_hotels_near_location(location)

    if hotels:
        choice = int(input("Above is a list of hotels based on the location you provided \nSelect a hotel by entering the corresponding number: "))
        selected_hotel = hotels[choice - 1]
        hotel_info = get_hotel_details(selected_hotel[2])

        if hotel_info:
            print("Fetching detailed information...")
            detailed_info = generate_detailed_information(hotel_info)
            print(detailed_info)

if __name__ == "__main__":
    main()
