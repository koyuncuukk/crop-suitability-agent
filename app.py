
import os, json
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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    lat  = float(data["latitude"])
    lon  = float(data["longitude"])
    crop = data["crop"]

    climate = get_climate_data(lat, lon)
    soil    = get_soil_data(lat, lon)

    # Sadece açık deniz/okyanus kontrolü (Türkiye iç suları hariç)
    if soil.get("is_sea", False):
        # Koordinat bazlı Türkiye kara kontrolü
        # Boğaz, Haliç, göller için tolerans tanı
        is_open_sea = (
            (lat > 41.5 and lon < 29.5) or   # Karadeniz kuzeyi
            (lat < 37.0 and lon < 27.0) or   # Ege güneyi
            (lat < 36.5)                      # Akdeniz güneyi
        )
        if is_open_sea:
            return jsonify({
                "suitability_score": 0,
                "rating": "Not Suitable — Sea/Ocean",
                "avg_temp": climate["avg_temp"],
                "annual_precip": climate["annual_precip"],
                "soil_ph": "N/A",
                "factors": {"Temperature": 0, "Precipitation": 0, "Soil pH": 0},
                "recommendation": "This location is in the sea or ocean. Please click on a land area in Turkey."
            })
        else:
            # Boğaz, Haliç, göl gibi iç su alanları — neutral pH kullan
            soil["soil_ph"] = 6.8
            soil["is_sea"] = False

    score = calculate_suitability(crop, climate["avg_temp"], climate["annual_precip"],
                                   soil["soil_ph"], CROP_REQUIREMENTS[crop])

    api_key = os.environ.get("GROQ_API_KEY", "")
    client  = groq_lib.Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a GeoAI agricultural expert agent."},
            {"role": "user", "content": f"""Analyze and give a 3-4 sentence practical recommendation.
Crop: {crop} | Location: {lat:.4f}, {lon:.4f}
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
        "recommendation":    response.choices[0].message.content
    })

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
