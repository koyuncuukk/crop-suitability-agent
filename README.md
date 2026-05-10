[README.md](https://github.com/user-attachments/files/27572806/README.md)
# 🌾 AI Crop Suitability Agent

> A **GeoAI-Powered Agricultural Land Analysis System** for Turkey

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-Visit_Website-2e7d32?style=for-the-badge)](https://crop-suitability-agent.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-black?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Groq](https://img.shields.io/badge/AI-Groq_LLaMA_3.1-orange?style=for-the-badge)](https://groq.com/)

---

## 🌍 Live Application

👉 **[crop-suitability-agent.onrender.com](https://crop-suitability-agent.onrender.com)**

> *Click anywhere on the map of Turkey, select a crop, and let the AI Agent analyze the agricultural suitability of that location in real-time.*

---

## 📖 Project Overview

**MYZ 305E – Artificial Intelligence for Geomatics Engineering**  
*2025-2026 Spring Term Project*  
**Istanbul Technical University**

This project presents an **autonomous AI agent** that evaluates agricultural land suitability across Turkey by integrating real-time geospatial data and large language models. With a single click on the map, users receive:

- 🌡️ **Climate analysis** (temperature, precipitation)
- 🌱 **Soil properties** (pH levels)
- 📊 **Suitability score** (0-100, with rating)
- 💬 **AI-generated farming recommendations**

---

## 🤖 AI Agent Architecture

The system implements an **LLM-powered orchestrator agent** that autonomously:

1. **Receives** user location and crop selection
2. **Detects** sea, lake, or out-of-Turkey clicks using Shapely polygon analysis
3. **Calls** specialized geospatial tools sequentially:
   - `get_climate_data()` → Open-Meteo API
   - `get_soil_data()` → SoilGrids (ISRIC) API
   - `calculate_suitability()` → Multi-factor scoring engine
4. **Generates** natural-language recommendations via Groq LLaMA 3.1
5. **Returns** structured results with actionable insights

---

## 🗺️ Geospatial Data Sources

| Dataset | Source | Variables |
|---------|--------|-----------|
| Historical Climate | [Open-Meteo Archive API](https://open-meteo.com/) | Avg. temperature (°C), Annual precipitation (mm) |
| Soil Properties | [SoilGrids v2.0 (ISRIC)](https://www.isric.org/explore/soilgrids) | Soil pH (0–30 cm depth) |
| Land Boundaries | GeoJSON / Shapely | Turkey country border polygon |
| Water Bodies | OpenStreetMap (Overpass API) | Lakes, reservoirs, straits, bays |
| Reverse Geocoding | [Nominatim](https://nominatim.openstreetmap.org/) | Province / district name resolution |

---

## 🌾 Supported Crops

🌾 Wheat · 🌽 Corn · 🌻 Sunflower · 🍅 Tomato · 🥔 Potato · 🌿 Barley · 🫘 Soybean · 🍇 Grape

Each crop has scientifically defined optimal ranges for temperature, precipitation, and soil pH.

---

## 📊 Scoring Methodology

The suitability score is calculated using a **weighted multi-factor model**:

| Factor | Weight | Optimal Range Source |
|--------|--------|----------------------|
| Temperature match | **40%** | Open-Meteo annual average |
| Precipitation match | **35%** | Open-Meteo annual total |
| Soil pH match | **25%** | SoilGrids 0–30 cm mean |

**Rating scale:**
- 🟢 **Excellent** (75–100)
- 🟡 **Good** (55–74)
- 🟠 **Moderate** (35–54)
- 🔴 **Poor** (0–34)

Special cases (deniz, göl, baraj, yurt dışı) automatically receive a score of **0** with appropriate warnings.

---

## 🛠️ Technology Stack

**Backend:**
- Python 3.11+
- Flask 3.0 (REST API)
- Gunicorn (WSGI server)

**AI / Agent:**
- Groq API (LLaMA 3.1 8B Instant)
- Tool-calling agent pattern

**Geospatial:**
- Shapely (polygon containment)
- GeoJSON (Turkey boundaries)
- Leaflet.js + CartoDB (interactive map)

**APIs:**
- Open-Meteo (climate)
- SoilGrids / ISRIC (soil)
- Nominatim / OpenStreetMap (geocoding)
- Overpass API (water bodies)

**Deployment:**
- Render.com (cloud hosting)
- GitHub (version control)

---

## 📁 Project Structure

```
crop-suitability-agent/
├── app.py                      # Flask backend + agent orchestration
├── tools/
│   ├── climate_tool.py         # Open-Meteo wrapper
│   ├── soil_tool.py            # SoilGrids wrapper
│   └── scoring_tool.py         # Suitability scoring engine
├── templates/
│   └── index.html              # Frontend UI (Leaflet + Vanilla JS)
├── turkey_border.json          # Turkey GeoJSON boundary
├── turkey_water.json           # Lakes / reservoirs polygons
├── notebooks/
│   └── crop_agent_test.ipynb   # Initial agent testing notebook
├── requirements.txt
├── Procfile                    # Render deployment config
└── README.md
```

---

## 🚀 Local Development

```bash
# Clone the repository
git clone https://github.com/koyuncuukk/crop-suitability-agent.git
cd crop-suitability-agent

# Install dependencies
pip install -r requirements.txt

# Set your Groq API key
export GROQ_API_KEY="gsk_your_key_here"   # Linux/macOS
set GROQ_API_KEY=gsk_your_key_here        # Windows

# Run the application
python app.py

# Open http://localhost:5000 in your browser
```

---

## 🎬 Demo Video

A 2-3 minute demonstration video showcasing the agent in action.

🎥 *See the `demo/` folder for the full screencast.*

---

## 📋 Assignment Requirements Checklist

- ✅ **AI Agent Integration** — Groq LLaMA 3.1 with autonomous tool orchestration
- ✅ **Source Code & Demo** — GitHub repository with screencast
- ✅ **Geospatial Datasets** — Open-Meteo, SoilGrids, OSM
- ✅ **Data Sources Documented** — In poster and README
- ✅ **Tables & Figures** — Workflow diagrams, results tables, application screenshots
- ✅ **Poster (English, PDF)** — Submitted via NINOVA

---

## 👤 Author

**Abdülkadir Koyuncu**  
Geomatics Engineering, Istanbul Technical University

---

## 📜 License

This project is developed as part of an academic course project.  
Educational use permitted.

---

## 🙏 Acknowledgments

- **Open-Meteo** for free, no-key climate data
- **ISRIC SoilGrids** for global soil property data
- **OpenStreetMap** contributors for map tiles and water body data
- **Groq** for fast, free LLM inference
- **Render.com** for free cloud hosting
