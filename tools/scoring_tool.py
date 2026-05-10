
def calculate_suitability(crop, avg_temp, annual_precip, soil_ph, requirements):
    def score(val, mn, mx, amn, amx):
        if mn <= val <= mx:
            mid = (mn + mx) / 2
            half = (mx - mn) / 2
            distance = abs(val - mid) / half
            return round(100 - distance * 25)  # daha katı
        if val < mn:
            return max(0, round(80 * (val - amn) / (mn - amn))) if amn < mn else 0
        return max(0, round(80 * (amx - val) / (amx - mx))) if amx > mx else 0

    r = requirements
    t  = score(avg_temp,      r["temp_min"],   r["temp_max"],   r["temp_min"]-6,   r["temp_max"]+6)
    p  = score(annual_precip, r["precip_min"],  r["precip_max"], r["precip_min"]-100, r["precip_max"]+200)
    ph = score(soil_ph,       r["ph_min"],      r["ph_max"],     r["ph_min"]-1.0,   r["ph_max"]+1.0)

    # Eğer herhangi bir faktör çok düşükse ceza ver
    min_factor = min(t, p, ph)
    if min_factor < 20:
        composite = round(0.4*t + 0.35*p + 0.25*ph) - 15
    else:
        composite = round(0.4*t + 0.35*p + 0.25*ph)

    composite = max(0, composite)
    rating = "Excellent" if composite>=75 else "Good" if composite>=55 else "Moderate" if composite>=35 else "Poor"
    return {"suitability_score": composite, "rating": rating,
            "factors": {"Temperature": round(t), "Precipitation": round(p), "Soil pH": round(ph)}}
