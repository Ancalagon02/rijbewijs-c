from config import (
    TIJDLIMIET_GEWOON_EXAMEN_MIN,
    TIJDLIMIET_VAK_CASES_MIN,
    TIJDLIMIET_VAK_MC_MIN,
    BESTANDSNAAM,
)
from database import RIJBEWIJS_HOOFDSTUKKEN, VAK_HOOFDSTUKKEN
from exam import (
    start_rijbewijs_examen,
    start_vakbekwaamheid_cases_examen,
    start_vakbekwaamheid_mc_examen,
)
from practice import oefen_hoofdstuk
from storage import sla_voortgang_op, laad_voortgang
import time
import os


def menu_vakbekwaamheid_oefen(data):
    """Menu voor oefenen per Vakbekwaamheid hoofdstuk."""
    while True:
        print("\n==================================")
        print("  VAKBEKWAAMHEID: HOOFDSTUKKEN    ")
        print("==================================")
        for key, info in VAK_HOOFDSTUKKEN.items():
            print(f"{key}. {info['naam']}")
        print("8. Terug")

        k = input("\nKies een hoofdstuk (1-8): ").strip()
        if k in VAK_HOOFDSTUKKEN:
            oefen_hoofdstuk(data, "vakbekwaamheid", VAK_HOOFDSTUKKEN, k)
        elif k == "8":
            break


def menu_vakbekwaamheid(data):
    """Hoofdmenu Vakbekwaamheid module."""
    while True:
        print("\n==================================")
        print("  MODULE: VAKBEKWAAMHEID C/D     ")
        print("==================================")
        print("1. Oefenvragen per Hoofdstuk")
        print(f"2. MC Examen Reeks A ({TIJDLIMIET_VAK_MC_MIN} min)")
        print(f"3. MC Examen Reeks B ({TIJDLIMIET_VAK_MC_MIN} min)")
        print(f"4. Casus Examen Reeks A ({TIJDLIMIET_VAK_CASES_MIN} min)")
        print(f"5. Casus Examen Reeks B ({TIJDLIMIET_VAK_CASES_MIN} min)")
        print("6. Terug naar Hoofdmenu")

        k = input("\nMaak een keuze (1-6): ").strip()
        if k == "1":
            menu_vakbekwaamheid_oefen(data)
        elif k == "2":
            start_vakbekwaamheid_mc_examen(data, "A")
        elif k == "3":
            start_vakbekwaamheid_mc_examen(data, "B")
        elif k == "4":
            start_vakbekwaamheid_cases_examen(data, "A")
        elif k == "5":
            start_vakbekwaamheid_cases_examen(data, "B")
        elif k == "6":
            break


def menu_rijbewijs(data):
    """Hoofdmenu Rijbewijs module."""
    while True:
        print("\n==================================")
        print("  MODULE: GEWOON RIJBEWIJS        ")
        print("==================================")
        print("1. Oefenvragen per Hoofdstuk")
        print(f"2. Examenreeksen ({TIJDLIMIET_GEWOON_EXAMEN_MIN} min per reeks)")
        print("3. Terug naar Hoofdmenu")

        k = input("\nMaak een keuze (1-3): ").strip()
        if k == "1":
            while True:
                print("\nKies Hoofdstuk (1-16) of 17 om terug te gaan:")
                for key, info in RIJBEWIJS_HOOFDSTUKKEN.items():
                    print(f"{key}. {info['naam']}")
                print("17. Terug")

                h_k = input("Keuze: ").strip()
                if h_k in RIJBEWIJS_HOOFDSTUKKEN:
                    oefen_hoofdstuk(data, "rijbewijs", RIJBEWIJS_HOOFDSTUKKEN, h_k)
                elif h_k == "17":
                    break
        elif k == "2":
            r_k = input("Kies reeks (A, B, C, D): ").strip().upper()
            if r_k in ["A", "B", "C", "D"]:
                start_rijbewijs_examen(data, r_k)
        elif k == "3":
            break


# ------------------ Reset functionaliteit ------------------

def reset_hoofdstuk(data):
    """Reset voortgang voor een specifiek hoofdstuk in een module."""
    print("\nWelke module wil je resetten?")
    print("1. Gewoon Rijbewijs")
    print("2. Vakbekwaamheid")
    m = input("Keuze (1 of 2, of anders om te annuleren): ").strip()
    if m == "1":
        module = "rijbewijs"
        hoofdstukken = RIJBEWIJS_HOOFDSTUKKEN
    elif m == "2":
        module = "vakbekwaamheid"
        hoofdstukken = VAK_HOOFDSTUKKEN
    else:
        print("Annuleren.")
        return

    print("\nKies hoofdstuk:")
    for key, info in hoofdstukken.items():
        print(f"{key}. {info['naam']}")
    keuze = input("Hoofdstuk (nummer): ").strip()
    if keuze not in hoofdstukken:
        print("Ongeldige keuze. Annuleren.")
        return

    mod_data = data.setdefault(module, {}).setdefault("oefenvragen", {})
    mod_data[keuze] = {"mc": {}, "cases": {}}
    sla_voortgang_op(data)
    print(f"✅ Voortgang hoofdstuk {keuze} ('{hoofdstukken[keuze]['naam']}') is gereset.")


def reset_examen(data):
    """Reset voortgang voor een specifiek examen."""
    print("\nVoor welk examen wil je resetten?")
    print("1. Gewoon Rijbewijs (reeksen A-D)")
    print("2. Vakbekwaamheid (MC of Cases, reeksen A/B)")
    m = input("Keuze (1 of 2, of anders om te annuleren): ").strip()
    if m == "1":
        # Rijbewijs examens
        reeks = input("Kies reeks (A, B, C, D): ").strip().upper()
        if reeks not in ["A", "B", "C", "D"]:
            print("Ongeldige reeks. Annuleren.")
            return
        examens = data.setdefault("rijbewijs", {}).setdefault("examens", {})
        if reeks in examens:
            del examens[reeks]
            sla_voortgang_op(data)
            print(f"✅ Examen {reeks} (rijbewijs) is gereset.")
        else:
            print("Er was geen voortgang voor dat examen. Niets te doen.")
    elif m == "2":
        t = input("Type examen: MC of Cases? (mc/cases): ").strip().lower()
        if t not in ["mc", "cases"]:
            print("Ongeldige keuze. Annuleren.")
            return
        reeks = input("Kies reeks (A of B): ").strip().upper()
        if reeks not in ["A", "B"]:
            print("Ongeldige reeks. Annuleren.")
            return
        if t == "mc":
            examens = data.setdefault("vakbekwaamheid", {}).setdefault("examens_mc", {})
        else:
            examens = data.setdefault("vakbekwaamheid", {}).setdefault("examens_cases", {})
        if reeks in examens:
            del examens[reeks]
            sla_voortgang_op(data)
            print(f"✅ Vakbekwaamheid {t.upper()} examen reeks {reeks} is gereset.")
        else:
            print("Er was geen voortgang voor dat examen. Niets te doen.")
    else:
        print("Annuleren.")
        return


def reset_volledig(data):
    """Reset alle voortgang — volledige reset van de applicatie."""
    confirm = input("\nWeet je zeker dat je ALLES wilt resetten? Dit kan niet ongedaan gemaakt worden. (ja/nee): ").strip().lower()
    if confirm not in ["ja", "j", "yes", "y"]:
        print("Annuleren.")
        return

    # Verwijder het voortgangsbestand als het bestaat (gebruikerswens)
    if os.path.exists(BESTANDSNAAM):
        try:
            os.remove(BESTANDSNAAM)
            print(f"✅ Bestand '{BESTANDSNAAM}' is verwijderd.")
        except OSError:
            print(f"⚠️ Kon '{BESTANDSNAAM}' niet verwijderen. Annuleren.")
            return
    else:
        print("Geen voortgangsbestand gevonden — niets te verwijderen.")

    # Werk ook de in-memory data bij naar lege structuur
    default = laad_voortgang()
    data.clear()
    data.update(default)

    print("✅ Alle voortgang is verwijderd. Je kunt nu opnieuw beginnen.")


def menu_reset_options(data):
    """Hoofdmenu voor reset opties (toegankelijk vanuit hoofdmenu)."""
    while True:
        print("\n==================================")
        print("      RESET OPTIES                ")
        print("==================================")
        print("1. Reset oefeningen per Hoofdstuk")
        print("2. Reset per Examen")
        print("3. Volledige reset (alles)")
        print("4. Terug naar Hoofdmenu")

        k = input("\nMaak een keuze (1-4): ").strip()
        if k == "1":
            reset_hoofdstuk(data)
        elif k == "2":
            reset_examen(data)
        elif k == "3":
            reset_volledig(data)
        elif k == "4":
            break


def menu_hoofdscherm(data):
    """Hoofdmenu van de applicatie."""
    while True:
        print("\n==================================")
        print("      HOOFDMENU SELECTIE          ")
        print("==================================")
        print("1. Gewoon Rijbewijs")
        print("2. Vakbekwaamheid")
        print("3. Reset opties")
        print("4. Afsluiten")

        keuze = input("\nWaarvoor wil je oefenen? (1-4): ").strip()
        if keuze == "1":
            menu_rijbewijs(data)
        elif keuze == "2":
            menu_vakbekwaamheid(data)
        elif keuze == "3":
            menu_reset_options(data)
        elif keuze == "4":
            print("Tot ziens!")
            break
