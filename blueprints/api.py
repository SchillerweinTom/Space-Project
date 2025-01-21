from flask import Flask, Blueprint, jsonify, request, send_file
import requests
import math
import os
from models.models import DeltaV
import matplotlib.pyplot as plt
import io

app = Blueprint("api", __name__)

# Costanti
G0 = 9.81
ISP = 450
AVG_SPEED = 30000
UPLOAD_DIR = os.path.join(os.getcwd(), 'static\\uploads')


def get_distance_from_earth(body):
    if body == "leo":
        return 200, "Low Earth Orbit"
    elif body == "geo":
        return 35786, "Geostationary Earth Orbit"
    elif body == "sso":
        return 700, "Sun Synchronous Orbit"
    else:
        response = requests.get("https://api.le-systeme-solaire.net/rest/bodies/" + body)
        response.raise_for_status()
        data = response.json()
        return data['semimajorAxis'], data['englishName']


def get_rocket_info(name):
    response = requests.get("https://api.spacexdata.com/v3/rockets/" + name)
    response.raise_for_status()
    data = response.json()
    return data


def get_rockets_name():
    response = requests.get("https://api.spacexdata.com/v3/rockets/")
    response.raise_for_status()
    data = response.json()
    return [rocket['rocket_name'] for rocket in data]


@app.route('/distance/<body>')
def get_distance_earth_body(body):
    try:
        distance, name = get_distance_from_earth(body)
        return {"name": name, "distance_km": distance}, 200
    except Exception as e:
        return {"error": f"Error while fetching data: {str(e)}"}, 500


# Not dynamic because its more complicated to make dynamic than in this way (problem to filter the api, as there is no
# "is solar system" property)
@app.route('/destinations/<opt>')
def get_destinations(opt):
    if opt == "all":
        dest = ['leo', 'geo', 'sso', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus',
                'Neptune']
        return jsonify(dest), 200
    else:
        dest = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
        return jsonify(dest), 200

    
@app.route('/rocket/<name>')
def get_rocket(name):
    try:
        data = get_rocket_info(name)
        payload_weights = data['payload_weights']
        cost = data['cost_per_launch']
        mass = data['mass']
        flickr_images = data['flickr_images']
        return {"Payload": payload_weights, "Cost": cost, "Mass": mass['kg'], "flickr_images": flickr_images  }, 200
    except Exception as e:
        return {"error": f"Error while fetching data: {str(e)}"}, 500


@app.route('/rockets')
def get_rockets():
    try:
        data = get_rockets_name()
        return {"names": data}, 200
    except Exception as e:
        return {"error": f"Error while fetching data: {str(e)}"}, 500


@app.route('/fuel', methods=['POST'])
def calculate_fuel_and_time():
    try:
        data = request.json
        body = data['destination']
        payload_mass = data['payload_mass']
        dry_mass = data.get('dry_mass', 10000)
        
        distance_km, name = get_distance_from_earth(body)
        
        distance_m = distance_km * 1000

        delta_v_entry = DeltaV.query.filter_by(name=body.lower()).first()
        delta_v = delta_v_entry.value if delta_v_entry else None
        if delta_v is None:
            return {"error": f"Destination '{body}' not supported."}, 400

        initial_mass = dry_mass + payload_mass

        # Calcolo del carburante richiesto con Tsiolkovsky  
        fuel_mass = initial_mass * (math.exp(delta_v / (ISP * G0)) - 1)

        travel_time_seconds = distance_m / AVG_SPEED
        travel_time_days = travel_time_seconds / (60 * 60 * 24)

        return jsonify({
            "destination": name,
            "distance_km": distance_km,
            "fuel_needed_kg": round(fuel_mass, 2),
            "travel_time_days": round(travel_time_days, 2)
        }), 200
    except KeyError:
        return {"error": "Data is incomplete. Include 'destination' and 'payload_mass'."}, 400
    except Exception as e:
        return {"error": f"Error: {str(e)}"}, 500


def format_large_number(value):
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f} billion"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.1f} million"
    else:
        return value


@app.route('/cost_estimate', methods=['POST'])
def estimate_cost():
    try:
        data = request.json
        rocket = data['rocket'].lower().replace(" ", "")
        payload_mass = data['payload_mass']

        rocket_data = get_rocket_info(rocket)
        cost_per_kg = rocket_data['cost_per_launch'] / rocket_data['payload_weights'][0]['kg']

        total_cost = math.ceil(cost_per_kg * payload_mass)
        formatted_cost = format_large_number(total_cost)

        return jsonify({"estimated_cost": formatted_cost}), 200
    except Exception as e:
        return {"error": f"Error estimating cost: {str(e)}"}, 500
    

# Great improvement would be to get the real position of the planets,
# the next level would be to make the route elliptical
@app.route('/route', methods=['POST'])
def generate_route_map():
    try:
        data = request.json
        destination = data['destination'].lower()

        solar_system_distances = {
            "sun": 0.0, "mercury": 0.39, "venus": 0.72, "earth": 1.0, "mars": 1.52,
            "jupiter": 5.2, "saturn": 9.58, "uranus": 19.22, "neptune": 30.05
        }

        if destination not in solar_system_distances:
            return {"error": f"Destination '{destination}' not found in Solar System planets."}, 400

        destination_distance = solar_system_distances[destination]

        max_distance = max(1.0, destination_distance)
        filtered_distances = {body: dist for body, dist in solar_system_distances.items() if dist <= max_distance}

        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_facecolor("black")
        ax.set_aspect('equal')
        ax.set_xlim(-max_distance - 1, max_distance + 1)
        ax.set_ylim(-max_distance - 1, max_distance + 1)

        for body, distance in filtered_distances.items():
            if distance > 0:
                circle = plt.Circle((0, 0), distance, color="white", fill=False, linestyle='--', alpha=0.3)
                ax.add_artist(circle)

        for body, distance in filtered_distances.items():
            if body != "sun":
                size = 12 if body in ["earth", destination] else 8
                color = "blue" if body == "earth" else "red" if body == destination else "gray"
                label = body.capitalize() if body in ["earth", destination] else None
                ax.plot(distance, 0, 'o', color=color, markersize=size, zorder=10)
                if label:
                    ax.text(distance, 0.1, label, color="white", fontsize=10, ha="center")

        sun_marker = plt.Circle((0, 0), 0.1, color="yellow", zorder=5)
        ax.add_artist(sun_marker)

        ax.plot([1.0, destination_distance], [0, 0], color="yellow", linewidth=2, linestyle='--', alpha=0.8)

        ax.set_title(f"Route from Earth to {destination.capitalize()}", fontsize=16, color="white", pad=20)
        ax.set_xlabel("Distance in Astronomical Units (AU)", fontsize=12, color="white")
        ax.set_ylabel("Relative Position (AU)", fontsize=12, color="white")
        ax.tick_params(colors='white', labelsize=10)

        image_path = os.path.join(UPLOAD_DIR, 'temp_route.png')
        plt.savefig(image_path, format='png', bbox_inches='tight', facecolor="black")
        rotate_images(image_path)

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', facecolor="black")
        buf.seek(0)
        plt.close(fig)

        return send_file(buf, mimetype='image/png', as_attachment=False, download_name="route_map.png")

    except KeyError:
        return {"error": "Payload data is incomplete. Include 'destination'."}, 400
    except Exception as e:
        return {"error": f"Error: {str(e)}"}, 500


def rotate_images(new_image_path):
    images = sorted([f for f in os.listdir(UPLOAD_DIR) if f.endswith('.png')])
    if len(images) >= 3:
        os.remove(os.path.join(UPLOAD_DIR, images[0]))

    for i, img in enumerate(images[1:], 1):
        os.rename(os.path.join(UPLOAD_DIR, img), os.path.join(UPLOAD_DIR, f'img{i}.png'))