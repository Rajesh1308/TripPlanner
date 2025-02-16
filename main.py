from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from groq import Groq
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# Set up Groq client
client = Groq(
    api_key="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",
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate-itinerary", methods=["POST"])
def generate_trip_plan():
    data = request.json
    destination = data.get("destination")
    number_of_days = data.get("number_of_days")
    activities = data.get("activities", [])
    budget = data.get("budget")

    if not destination or not number_of_days or not budget:
        return jsonify({"error": "Missing required fields"}), 400
    
    prompt = f"""
    You are an AI-powered travel assistant helping users plan their trips efficiently. Based on the given details, provide a well-structured trip itinerary with optimized travel routes, accommodation, and activities within the specified budget. The response must be in valid JSON format with minimal nesting.
    
    ### User Inputs:
    - Destination: {destination}
    - Number of Days: {number_of_days}
    - Activities: {', '.join(activities)}
    - Budget: {budget}
    
    ### Instructions:
    - Generate a {number_of_days}-day itinerary based on the provided activities and budget.
    - Include suggested accommodations with estimated pricing.
    - Recommend must-visit places such as museums, restaurants, and markets.
    - Provide local transportation details and estimated costs.
    - Output JSON with a flat structure for readability.
    - The format of JSON should strictly follow the example JSON format.
    
    ### Example Responses:
    1. {{
        "destination": "Tokyo",
        "numDays": 3,
        "budget": 1200,
        "activities": ["sightseeing", "food tasting", "shopping"],
        "itinerary": [
            {{"day": 1, "location": "Shibuya Crossing", "activity": "sightseeing", "accommodation": "Hotel Shibuya", "cost": 150, "transport": "Metro ($3)"}},
            {{"day": 2, "location": "Tsukiji Outer Market", "activity": "food tasting", "accommodation": "Capsule Hotel", "cost": 50, "transport": "Taxi ($10)"}},
            {{"day": 3, "location": "Ginza", "activity": "shopping", "accommodation": "Airbnb", "cost": 80, "transport": "Bus ($2)"}}
        ],
        "mustVisit": ["Tokyo Tower", "Meiji Shrine", "Akihabara"]
    }}
    
    2. {{
        "destination": "New York",
        "numDays": 5,
        "budget": 2000,
        "activities": ["theater", "sightseeing", "food tasting"],
        "itinerary": [
            {{"day": 1, "location": "Broadway", "activity": "theater", "accommodation": "Hotel Manhattan", "cost": 250, "transport": "Subway ($2.75)"}},
            {{"day": 2, "location": "Statue of Liberty", "activity": "sightseeing", "accommodation": "Hotel Brooklyn", "cost": 180, "transport": "Ferry ($12)"}},
            {{"day": 3, "location": "Central Park", "activity": "relaxing", "accommodation": "Airbnb", "cost": 100, "transport": "Bus ($3)"}},
            {{"day": 4, "location": "Times Square", "activity": "shopping", "accommodation": "Hotel Hilton", "cost": 220, "transport": "Taxi ($15)"}},
            {{"day": 5, "location": "Chelsea Market", "activity": "food tasting", "accommodation": "Boutique Hotel", "cost": 150, "transport": "Walk (Free)"}}
        ],
        "mustVisit": ["Empire State Building", "Brooklyn Bridge", "Metropolitan Museum"]
    }}
    
    3. {{
        "destination": "Paris",
        "numDays": 4,
        "budget": 1600,
        "activities": ["museum visits", "food tasting", "shopping"],
        "itinerary": [
            {{"day": 1, "location": "Louvre Museum", "activity": "museum visits", "accommodation": "Hotel Louvre", "cost": 180, "transport": "Metro ($2)"}},
            {{"day": 2, "location": "Eiffel Tower", "activity": "sightseeing", "accommodation": "Hostel Paris", "cost": 90, "transport": "Bus ($3)"}},
            {{"day": 3, "location": "Champs-Élysées", "activity": "shopping", "accommodation": "Airbnb", "cost": 120, "transport": "Taxi ($10)"}},
            {{"day": 4, "location": "Montmartre", "activity": "food tasting", "accommodation": "Boutique Hotel", "cost": 150, "transport": "Walk (Free)"}}
        ],
        "mustVisit": ["Notre-Dame Cathedral", "Seine River Cruise", "Versailles"]
    }}
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful travel planner."},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"}
        )
        
        trip_plan = response.choices[0].message.content
        # json_response = jsonify(trip_plan)
        # print(json_response)
        return json.loads(trip_plan)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
