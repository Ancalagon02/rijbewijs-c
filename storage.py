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
        "rijbewijs": {"oefenvragen": {}, "examens": {}},
        "vakbekwaamheid": {"oefenvragen": {}, "examens": {}},
    }


def sla_voortgang_op(data):
    """Sla voortgang op in JSON bestand."""
    with open(BESTANDSNAAM, "w") as f:
        json.dump(data, f, indent=4)