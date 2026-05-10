
def calculate_suitability(crop, avg_temp, annual_precip, soil_ph, requirements):
    def score(val, mn, mx, amn, amx):
        if mn <= val <= mx:
            mid = (mn + mx) / 2
            distance = abs(val - mid) / ((mx - mn) / 2)
            return round(100 - distance * 15)
        if val < mn: return max(0, round(100*(val-amn)/(mn-amn))) if amn < mn else 0
        return max(0, round(100*(amx-val)/(amx-mx))) if amx > mx else 0
    r = requirements
    t  = score(avg_temp,      r["temp_min"], r["temp_max"], r["temp_min"]-8,   r["temp_max"]+8)
    p  = score(annual_precip, r["precip_min"],r["precip_max"],r["precip_min"]-150,r["precip_max"]+300)
    ph = score(soil_ph,       r["ph_min"],   r["ph_max"],   r["ph_min"]-1.5,   r["ph_max"]+1.5)
    composite = round(0.4*t + 0.35*p + 0.25*ph)
    rating = "Excellent" if composite>=75 else "Good" if composite>=55 else "Moderate" if composite>=35 else "Poor"
    return {"suitability_score": composite, "rating": rating,
            "factors": {"Temperature": round(t), "Precipitation": round(p), "Soil pH": round(ph)}}
