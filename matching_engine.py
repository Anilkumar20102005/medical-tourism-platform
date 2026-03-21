"""
HealinBelieve — AI Doctor Matching Engine
Weighted scoring algorithm that evaluates:
  Medical specialty match  (35%)
  Budget compatibility     (25%)
  Location/travel convenience (15%)
  Doctor experience level  (25%)
"""

# ─── Region / proximity map ──────────────────────────────────────────
REGION_MAP = {
    "India":        "South Asia",
    "Thailand":     "Southeast Asia",
    "Singapore":    "Southeast Asia",
    "Germany":      "Europe",
    "Turkey":       "Europe",
    "South Korea":  "East Asia",
    "USA":          "North America",
    "UK":           "Europe",
    "UAE":          "Middle East",
    "Brazil":       "South America",
    "Mexico":       "North America",
    "Japan":        "East Asia",
    "Malaysia":     "Southeast Asia",
    "Spain":        "Europe",
    "Australia":    "Oceania",
}

# Related specialties that still partially match
RELATED_SPECIALTIES = {
    "Orthopedics":    ["Sports Medicine", "Physiotherapy", "Rheumatology"],
    "Cardiology":     ["Cardiac Surgery", "Vascular Surgery", "Internal Medicine"],
    "Dermatology":    ["Cosmetic Surgery", "Plastic Surgery", "Allergy"],
    "Neurology":      ["Neurosurgery", "Psychiatry", "Pain Management"],
    "Oncology":       ["Radiation Therapy", "Hematology", "Surgical Oncology"],
    "Ophthalmology":  ["Optometry", "Oculoplastics", "Retinal Surgery"],
}

WEIGHTS = {
    "specialty":  0.35,
    "budget":     0.25,
    "location":   0.15,
    "experience": 0.25,
}


def _specialty_score(doctor_specialty: str, patient_specialty: str) -> float:
    """Return 0‑100 score for specialty match."""
    doc = doctor_specialty.lower().strip()
    pat = patient_specialty.lower().strip()

    if doc == pat:
        return 100.0

    # Check related specialties
    for main_spec, related in RELATED_SPECIALTIES.items():
        related_lower = [r.lower() for r in related]
        main_lower = main_spec.lower()

        # Patient wants main, doctor has related (or vice‑versa)
        if pat == main_lower and doc in related_lower:
            return 65.0
        if doc == main_lower and pat in related_lower:
            return 65.0
        # Both are in the same related group
        if pat in related_lower and doc in related_lower:
            return 50.0

    return 15.0  # no meaningful match


def _budget_score(consultation_fee: float, patient_budget: float) -> float:
    """Return 0‑100 score for budget compatibility."""
    if patient_budget <= 0:
        return 50.0
    if consultation_fee <= patient_budget:
        return 100.0
    ratio = patient_budget / consultation_fee
    if ratio >= 0.8:
        return 85.0
    if ratio >= 0.5:
        return 60.0
    if ratio >= 0.3:
        return 35.0
    return 10.0


def _location_score(doctor_country: str, patient_country: str) -> float:
    """Return 0‑100 score for location/travel convenience."""
    if doctor_country.lower().strip() == patient_country.lower().strip():
        return 100.0

    doc_region = REGION_MAP.get(doctor_country, "Other")
    pat_region = REGION_MAP.get(patient_country, "Other")

    if doc_region == pat_region:
        return 75.0

    # Adjacent region bonus
    adjacent = {
        ("South Asia", "Southeast Asia"),
        ("Southeast Asia", "East Asia"),
        ("Europe", "Middle East"),
        ("North America", "South America"),
    }
    pair = tuple(sorted([doc_region, pat_region]))
    if pair in adjacent:
        return 55.0

    return 30.0


def _experience_score(doctor_years: int, preferred_min: int) -> float:
    """Return 0‑100 score for experience level alignment."""
    if doctor_years >= preferred_min:
        return 100.0
    ratio = doctor_years / max(preferred_min, 1)
    return round(max(ratio * 100, 20), 1)


def calculate_match_scores(doctors: list, patient_info: dict) -> list:
    """
    Score every doctor against the patient's preferences.

    Parameters
    ----------
    doctors : list[dict]
        Each dict has keys: name, specialty, country, experience_years,
        consultation_fee, … (full doctor profile)
    patient_info : dict
        Keys: specialty, budget, country, min_experience

    Returns
    -------
    list[dict]  — sorted descending by overall_score, each dict contains:
        doctor (original dict), overall_score, breakdown {specialty, budget,
        location, experience} each with raw score and weighted contribution.
    """
    pat_specialty    = patient_info.get("specialty", "")
    pat_budget       = float(patient_info.get("budget", 0))
    pat_country      = patient_info.get("country", "")
    pat_min_exp      = int(patient_info.get("min_experience", 0))

    results = []
    for doc in doctors:
        sp = _specialty_score(doc["specialty"], pat_specialty)
        bu = _budget_score(doc["consultation_fee"], pat_budget)
        lo = _location_score(doc["country"], pat_country)
        ex = _experience_score(doc["experience_years"], pat_min_exp)

        overall = round(
            sp * WEIGHTS["specialty"]
            + bu * WEIGHTS["budget"]
            + lo * WEIGHTS["location"]
            + ex * WEIGHTS["experience"],
            1,
        )

        results.append({
            "doctor": doc,
            "overall_score": overall,
            "breakdown": {
                "specialty":  {"score": round(sp, 1), "weighted": round(sp * WEIGHTS["specialty"], 1)},
                "budget":     {"score": round(bu, 1), "weighted": round(bu * WEIGHTS["budget"], 1)},
                "location":   {"score": round(lo, 1), "weighted": round(lo * WEIGHTS["location"], 1)},
                "experience": {"score": round(ex, 1), "weighted": round(ex * WEIGHTS["experience"], 1)},
            },
        })

    results.sort(key=lambda r: r["overall_score"], reverse=True)
    return results
