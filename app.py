import re

import requests
from flask import Flask, send_from_directory, request, redirect, url_for, render_template
import google.generativeai as genai
import os
import json 
from flask import jsonify

app = Flask(__name__)

app.config['REGISTER_FOLDER'] = 'static/res/register'
app.config['HOME_FOLDER'] = 'static/res/home'
app.config['MAP_FOLDER'] = 'static/res/map'
app.config['BOOKSLOT_FOLDER'] = 'static/res/bookslot'
app.config['API_FOLDER'] = 'static/res/apicalls'

API_KEY = "AIzaSyCA4__JMC_ZIQ9xQegIj5LOMLhSSrn3pMw"

# Placeholder function for Gemini API configuration
genai.configure(api_key=API_KEY)

# Function to dynamically generate itineraries based on different prompts
def generate_itinerary(prompt):
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 40,
        "max_output_tokens": 2048,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    # Replace this with actual model.generate_content([prompt]) call
    f"Generated itinerary based on prompt: {prompt}"

    return model.generate_content([prompt])


@app.route('/planTrips', methods=['GET', 'POST'])
def planTrips():
    itinerary_content = None  # Define itinerary_content with a default value
    if request.method == 'POST':
        source = request.form.get('source')
        destination = request.form.get('destination')
        battery_range = request.form.get('battery_range')
        start_time = request.form.get('start_time')
        vehicle_type = request.form.get('vehicle_type')
        preferences_text = request.form.get('preferences_text')

        prompt_itinerary = f"""
        Plan an optimal road trip from {source} to {destination} on a {battery_range}-range {vehicle_type}. I will be departing {source} at {start_time}.

        Please suggest the fastest route given current and forecasted traffic conditions, with necessary supercharging/charging stops along the way given my vehicle's rated driving efficiency. Optimize stops for {preferences_text}. Provide estimated arrival time at each supercharging location accounting for wait times, along with charge time, city location, address, and approximate cost based on current rates. 

        Additionally, list all available EV charging stations along the route. For each charging stop, recommend the top places to hang out and visit nearby to make efficient use of charging time. This may include cafes, restaurants, parks, or any interesting landmarks within walking distance.

        Include an overview of the complete trip time, total miles driven, energy consumption estimate, total charging costs, and recommended tire pressure setting for maximum efficiency.
        """


        # Ensure generate_itinerary actually returns a value or text to avoid another potential error
        response = generate_itinerary(prompt_itinerary)

        itinerary_content = response.text

        itinerary_content = format_response(itinerary_content)

    # Ensure itinerary_content is passed to the template, whether None or containing a value
    # return render_template('trips.html', itinerary=itinerary_content)
    return render_template('trips.html', itinerary=itinerary_content)

@app.route('/data')
def serve_data():
    return send_from_directory(app.static_folder, 'json/evCharger.json')

@app.route('/mumbai')
def mumbai():
    return app.send_static_file('json/mumbai.json')

@app.route('/search', methods=['POST'])
def search():
    location = request.json['location']
    url = "https://ev-charge-finder.p.rapidapi.com/search-by-location"
    querystring = {"near": location, "limit": "20"}
    headers = {
        "X-RapidAPI-Key": "b13e537b7amsh555fb8abecbffeap1bfc6cjsn6490a446c27e",
        "X-RapidAPI-Host": "ev-charge-finder.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch data"}), 500


@app.route('/pune')
def serve_pune_data():
    return send_from_directory(app.static_folder, 'json/pune.json')

@app.route('/bookSlot', methods=['GET', 'POST'])
def book_slot():
    if request.method == 'POST':
        # Handle the form submission here
        return redirect(url_for('book_slot'))
    return send_from_directory(app.config['BOOKSLOT_FOLDER'], 'bookSlot.html')

@app.route('/map')
def map_view():
    return send_from_directory(app.config['MAP_FOLDER'], 'map.html')

@app.route('/apicalls')
def apicalls():
    return send_from_directory(app.config['API_FOLDER'], 'apicalls.html')

@app.route('/register')
def register():
    return send_from_directory(app.config['REGISTER_FOLDER'], 'register.html')

# @app.route('/planTrips')
# def planTrips():
#     return send_from_directory(app.config['PLAN_FOLDER'], 'trips.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return send_from_directory(app.config['HOME_FOLDER'], 'home.html')

@app.route('/registerEVBranch', methods=['POST'])
def register_ev_branch():
    # Handle form submission here
    # You can access form data using request.form
    return 'Received the data successfully!'

def format_bold(text):
    # Convert text surrounded by ** into bold HTML tags
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)

def format_bullets(text):
    # Convert asterisk into unordered list items
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if line.strip().startswith('*'):
            lines[i] = f"<li>{line.strip()[1:].strip()}</li>"
    return '\n'.join(lines)

def format_table(text):
    # Convert markdown-like table to HTML table
    table = re.findall(r"\|(.*?)\|", text)
    if not table:
        return text

    headers, *rows = table
    header_html = "".join([f"<th>{h.strip()}</th>" for h in headers.split("|")])
    rows_html = "".join(["<tr>" + "".join([f"<td>{cell.strip()}</td>" for cell in row.split("|")]) + "</tr>" for row in rows])

    return f"<table class='table-auto w-full'><thead><tr>{header_html}</tr></thead><tbody>{rows_html}</tbody></table>"

def format_response(response):
    # Apply all formatting functions
    response = format_bold(response)
    response = format_bullets(response)
    response = format_table(response)
    return response.replace("\n", "<br>")


if __name__ == '__main__':
    app.run(port=3000)