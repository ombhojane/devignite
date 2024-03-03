import re
from flask import Flask, render_template, request
import google.generativeai as genai
import os

app = Flask(__name__)

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


@app.route('/', methods=['GET', 'POST'])
def home():
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

        Please suggest the fastest route given current and forecasted traffic conditions, with necessary supercharging/charging stops along the way given my vehicle's rated driving efficiency. Optimize stops for {preferences_text}. Provide estimated arrival time at each supercharging location accounting for wait times, along with charge time, city location, address and approximate cost based on current rates.

        Include an overview of the complete trip time, total miles driven, energy consumption estimate, total charging costs, and recommended tire pressure setting for maximum efficiency.
        """

        # Ensure generate_itinerary actually returns a value or text to avoid another potential error
        response = generate_itinerary(prompt_itinerary)

        itinerary_content = response.text

        itinerary_content = format_response(itinerary_content)

    # Ensure itinerary_content is passed to the template, whether None or containing a value
    return render_template('index.html', itinerary=itinerary_content)

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
    app.run(debug=True)