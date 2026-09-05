from config import INVOER_MAP


def valideer_invoer(invoer):
    """
    Valideer en zet invoer om naar letter (A, B, C, D).
    Return None als ongeldig.
    """
    invoer = invoer.strip().lower()
    return INVOER_MAP.get(invoer)


def get_voortgang_hoofdstuk(module_data, h_sleutel):
    """Haal of maak voortgang voor een specifiek hoofdstuk."""
    voortgang = module_data.setdefault("oefenvragen", {}).setdefault(
        h_sleutel, {"mc": {}, "cases": {}}
    )
    return voortgang


def bereken_stats_hoofdstuk(voortgang_h, mc_vragen, cases):
    """Bereken statistieken voor een hoofdstuk."""
    gemaakt_mc = len(voortgang_h["mc"])
    gemaakt_cases = sum(len(c_ans) for c_ans in voortgang_h["cases"].values())
    totaal_in_h = len(mc_vragen) + sum(len(c) for c in cases.values())
    return gemaakt_mc, gemaakt_cases, totaal_in_h