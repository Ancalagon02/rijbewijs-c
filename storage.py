import json
import os

from config import BESTANDSNAAM


def laad_voortgang():
    """Laad voortgang uit JSON bestand, return lege structuur als niet gevonden."""
    if os.path.exists(BESTANDSNAAM):
        try:
            with open(BESTANDSNAAM, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {
        "rijbewijs": {"oefenvragen": {}, "examens": {}, "completed_hoofdstukken": []},
        "vakbekwaamheid": {"oefenvragen": {}, "examens_mc": {}, "examens_cases": {}, "completed_hoofdstukken": []},
    }


def sla_voortgang_op(data):
    """Sla voortgang op in JSON bestand."""
    with open(BESTANDSNAAM, "w") as f:
        json.dump(data, f, indent=4)


def markeer_hoofdstuk_klaar(data, module, h_sleutel):
    """Markeer een hoofdstuk als volledig afgerond."""
    completed = data.get(module, {}).get("completed_hoofdstukken", [])
    if isinstance(completed, list):
        if h_sleutel not in completed:
            completed.append(h_sleutel)
    else:  # Als het een set is (JSON kan dit niet opslaan)
        completed = list(completed)
        if h_sleutel not in completed:
            completed.append(h_sleutel)
    
    if module not in data:
        data[module] = {}
    data[module]["completed_hoofdstukken"] = completed
    sla_voortgang_op(data)


def markeer_examen_geslaagd(data, module, exam_key, exam_type=None):
    """Markeer een examen als geslaagd."""
    if module not in data:
        data[module] = {}
    
    if module == "rijbewijs":
        examens_key = "examens"
    elif module == "vakbekwaamheid" and exam_type:
        examens_key = f"examens_{exam_type}"  # "examens_mc" of "examens_cases"
    else:
        return
    
    if examens_key not in data[module]:
        data[module][examens_key] = {}
    
    # Markeer examen als geslaagd
    if exam_key not in data[module][examens_key]:
        data[module][examens_key][exam_key] = {}
    
    data[module][examens_key][exam_key]["passed"] = True
    sla_voortgang_op(data)


def is_hoofdstuk_voltooid(data, module, h_sleutel):
    """Check of een hoofdstuk volledig is afgerond."""
    completed = data.get(module, {}).get("completed_hoofdstukken", [])
    return h_sleutel in completed


def is_examen_geslaagd(data, module, exam_key, exam_type=None):
    """Check of een examen als geslaagd is gemarkeerd."""
    if module == "rijbewijs":
        examens = data.get(module, {}).get("examens", {})
    elif module == "vakbekwaamheid" and exam_type:
        examens = data.get(module, {}).get(f"examens_{exam_type}", {})
    else:
        return False
    
    return examens.get(exam_key, {}).get("passed", False)
