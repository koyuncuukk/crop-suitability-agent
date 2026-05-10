
import os
from flask import Flask, request, jsonify, render_template
import groq as groq_lib
from tools.climate_tool import get_climate_data
from tools.soil_tool import get_soil_data
from tools.scoring_tool import calculate_suitability

app = Flask(__name__)

CROP_REQUIREMENTS = {
    "wheat":     {"temp_min": 5,  "temp_max": 24, "precip_min": 300, "precip_max": 900,  "ph_min": 6.0, "ph_max": 7.5},
    "corn":      {"temp_min": 15, "temp_max": 32, "precip_min": 500, "precip_max": 1200, "ph_min": 5.8, "ph_max": 7.0},
    "sunflower": {"temp_min": 16, "temp_max": 30, "precip_min": 400, "precip_max": 900,  "ph_min": 6.0, "ph_max": 7.5},
    "tomato":    {"temp_min": 18, "temp_max": 29, "precip_min": 400, "precip_max": 800,  "ph_min": 6.0, "ph_max": 7.0},
    "potato":    {"temp_min": 10, "temp_max": 22, "precip_min": 500, "precip_max": 1000, "ph_min": 5.0, "ph_max": 6.5},
    "barley":    {"temp_min": 5,  "temp_max": 22, "precip_min": 250, "precip_max": 700,  "ph_min": 6.0, "ph_max": 8.0},
    "soybean":   {"temp_min": 20, "temp_max": 30, "precip_min": 450, "precip_max": 900,  "ph_min": 6.0, "ph_max": 7.0},
    "grape":     {"temp_min": 12, "temp_max": 28, "precip_min": 300, "precip_max": 700,  "ph_min": 5.5, "ph_max": 7.0},
}

def is_in_turkey(lat, lon):
    """Nominatim ile gerçek Türkiye kontrolü"""
    import requests as req
    try:
        r = req.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={"lat": lat, "lon": lon, "format": "json"},
            headers={"User-Agent": "CropAgent/1.0"},
            timeout=5
        )
        data = r.json()
        country = data.get("address", {}).get("country_code", "")
        return country == "tr"
    except:
        # Fallback bbox kontrolü
        return 35.8 <= lat <= 42.2 and 25.6 <= lon <= 44.8

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    lat  = float(data["latitude"])
    lon  = float(data["longitude"])
    crop = data["crop"]

    # Türkiye kontrolü
    if not is_in_turkey(lat, lon):
        return jsonify({
            "suitability_score": 0,
            "rating": "Not in Turkey",
            "avg_temp": "N/A",
            "annual_precip": "N/A",
            "soil_ph": "N/A",
            "factors": {"Temperature": 0, "Precipitation": 0, "Soil pH": 0},
            "recommendation": "This location is outside Turkey. Please click inside Turkey borders.",
            "location_name": "Outside Turkey"
        })

    climate = get_climate_data(lat, lon)
    soil    = get_soil_data(lat, lon)

    # Deniz kontrolü
    if soil.get("is_sea", False):
        return jsonify({
            "suitability_score": 0,
            "rating": "Sea / Water Body",
            "avg_temp": climate["avg_temp"],
            "annual_precip": climate["annual_precip"],
            "soil_ph": "N/A",
            "factors": {"Temperature": 0, "Precipitation": 0, "Soil pH": 0},
            "recommendation": "This location is in the sea or a water body. Please click on land.",
            "location_name": "Sea / Water"
        })

    score = calculate_suitability(crop, climate["avg_temp"], climate["annual_precip"],
                                   soil["soil_ph"], CROP_REQUIREMENTS[crop])

    # Konum adı al
    import requests as req
    location_name = f"{lat:.4f}, {lon:.4f}"
    try:
        r = req.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={"lat": lat, "lon": lon, "format": "json", "accept-language": "tr"},
            headers={"User-Agent": "CropAgent/1.0"},
            timeout=5
        )
        addr = r.json().get("address", {})
        city    = addr.get("province") or addr.get("city") or addr.get("state") or ""
        district = addr.get("county") or addr.get("district") or addr.get("suburb") or ""
        if city and district:
            location_name = f"{district}, {city}"
        elif city:
            location_name = city
    except:
        pass

    api_key = os.environ.get("GROQ_API_KEY", "")
    client  = groq_lib.Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a GeoAI agricultural expert agent."},
            {"role": "user", "content": f"""Analyze and give a 3-4 sentence practical recommendation.
Crop: {crop} | Location: {location_name} ({lat:.4f}, {lon:.4f})
Temperature: {climate["avg_temp"]}C | Precipitation: {climate["annual_precip"]}mm | Soil pH: {soil["soil_ph"]}
Suitability Score: {score["suitability_score"]}/100 | Rating: {score["rating"]}
Factors: {score["factors"]}"""}
        ]
    )

    return jsonify({
        "suitability_score": score["suitability_score"],
        "rating":            score["rating"],
        "avg_temp":          climate["avg_temp"],
        "annual_precip":     climate["annual_precip"],
        "soil_ph":           soil["soil_ph"],
        "factors":           score["factors"],
        "recommendation":    response.choices[0].message.content,
        "location_name":     location_name
    })

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
