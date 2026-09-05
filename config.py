# ==============================================================================
# CONFIGURATIE / TIJDLIMIETEN (IN MINUTEN)
# ==============================================================================

BESTANDSNAAM = "voortgang_totaal.json"

TIJDLIMIET_GEWOON_EXAMEN_MIN = 50
TIJDLIMIET_VAK_MC_MIN = 50
TIJDLIMIET_VAK_CASES_MIN = 80

# ==============================================================================
# SLAGINGSCRITERIA
# ==============================================================================

SLAGINGSCRITERIUM_RIJBEWIJS = 41  # Minimaal 41 van 50 voor rijbewijs examen
SLAGINGSCRITERIUM_VAK_MC = 41      # Minimaal 41 van 50 voor vakbekwaamheid MC
SLAGINGSCRITERIUM_VAK_CASES = 32   # Minimaal 32 van 40 voor vakbekwaamheid Cases

INVOER_MAP = {
    "1": "A",
    "a": "A",
    "2": "B",
    "b": "B",
    "3": "C",
    "c": "C",
    "4": "D",
    "d": "D",
}
