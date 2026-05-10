
import requests
from datetime import date

def get_climate_data(latitude, longitude):
    end_year = date.today().year - 1
    params = {
        "latitude": latitude, "longitude": longitude,
        "start_date": f"{end_year}-01-01", "end_date": f"{end_year}-12-31",
        "daily": ["temperature_2m_mean", "precipitation_sum"],
        "timezone": "auto",
    }
    try:
        resp = requests.get("https://archive-api.open-meteo.com/v1/archive", params=params, timeout=15)
        data = resp.json()["daily"]
        temps = [t for t in data.get("temperature_2m_mean", []) if t]
        precip = [p for p in data.get("precipitation_sum", []) if p]
        return {
            "avg_temp": round(sum(temps)/len(temps), 1) if temps else 15.0,
            "annual_precip": round(sum(precip), 1) if precip else 500.0
        }
    except:
        return {"avg_temp": 15.0, "annual_precip": 500.0}
