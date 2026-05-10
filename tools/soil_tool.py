
import requests

def get_soil_data(latitude, longitude):
    params = {"lon": longitude, "lat": latitude, "property": ["phh2o"], "depth": ["0-5cm", "5-15cm"], "value": "mean"}
    try:
        resp = requests.get("https://rest.isric.org/soilgrids/v2.0/properties/query", params=params, timeout=20)
        ph_vals = []
        for layer in resp.json().get("properties", {}).get("layers", []):
            for d in layer.get("depths", []):
                v = d.get("values", {}).get("mean")
                if v: ph_vals.append(v/10)
        if not ph_vals:
            # Veri gelmedi ama deniz olduğu anlamına gelmez
            # Nominatim ile kontrol et
            try:
                r = requests.get(
                    "https://nominatim.openstreetmap.org/reverse",
                    params={"lat": latitude, "lon": longitude, "format": "json"},
                    headers={"User-Agent": "CropAgent/1.0"},
                    timeout=5
                )
                data = r.json()
                addr = data.get("address", {})
                # Gerçek deniz mi?
                if data.get("type") in ["bay", "strait", "sea"] or addr.get("body_of_water"):
                    return {"soil_ph": 6.8, "is_sea": True}
                else:
                    return {"soil_ph": 6.8, "is_sea": False}
            except:
                return {"soil_ph": 6.8, "is_sea": False}
        return {"soil_ph": round(sum(ph_vals)/len(ph_vals), 1), "is_sea": False}
    except:
        return {"soil_ph": 6.8, "is_sea": False}
