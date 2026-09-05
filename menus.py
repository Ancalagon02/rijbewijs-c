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
    """Reset voortgang voor een specifiek hoofdstuk in een module.

    Toon alleen hoofdstukken waarvoor al voortgang aanwezig is.
    """
    print("\nWelke module wil je resetten?")
    print("1. Gewoon Rijbewijs")
    print("2. Vakbekwaamheid")
    m = input("Keuze (1 of 2, of anders om te annuleren): ").strip()
    if m == "1":
        module = "rijbewijs"
        hoofdstukken_def = RIJBEWIJS_HOOFDSTUKKEN
    elif m == "2":
        module = "vakbekwaamheid"
        hoofdstukken_def = VAK_HOOFDSTUKKEN
    else:
        print("Annuleren.")
        return

    mod_data = data.get(module, {}).get("oefenvragen", {})
    if not mod_data:
        print("Er is geen voortgang voor deze module — niets om te resetten.")
        return

    # Toon alleen hoofdstukken met voortgang
    keys = list(mod_data.keys())
    print("\nKies hoofdstuk om te resetten:")
    for i, key in enumerate(keys, start=1):
        naam = hoofdstukken_def.get(key, {}).get("naam", key)
        print(f"{i}. {key} - {naam}")
    print(f"{len(keys)+1}. Annuleren")

    keuze = input("Keuze (nummer): ").strip()
    try:
        idx = int(keuze)
    except ValueError:
        print("Ongeldige keuze. Annuleren.")
        return
    if idx == len(keys) + 1:
        print("Annuleren.")
        return
    if idx < 1 or idx > len(keys):
        print("Ongeldige keuze. Annuleren.")
        return

    sel_key = keys[idx - 1]
    # Reset naar lege hoofdstuk voortgang
    mod_data[sel_key] = {"mc": {}, "cases": {}}
    sla_voortgang_op(data)
    naam = hoofdstukken_def.get(sel_key, {}).get("naam", sel_key)
    print(f"✅ Voortgang hoofdstuk {sel_key} ('{naam}') is gereset.")


def reset_examen(data):
    """Reset voortgang voor een specifiek examen.

    Toon alleen reeksen/examens die daadwerkelijk in de voortgang aanwezig zijn.
    """
    print("\nVoor welk examen wil je resetten?")
    print("1. Gewoon Rijbewijs (reeksen A-D)")
    print("2. Vakbekwaamheid (MC of Cases, reeksen A/B)")
    m = input("Keuze (1 of 2, of anders om te annuleren): ").strip()
    if m == "1":
        examens = data.get("rijbewijs", {}).get("examens", {})
        if not examens:
            print("Er is geen voortgang voor rijbewijs examens — niets om te resetten.")
            return
        # Toon alleen aanwezige reeksen
        keys = list(examens.keys())
        print("\nKies welke rijbewijs-examenreeks je wilt resetten:")
        for i, key in enumerate(keys, start=1):
            print(f"{i}. Reeks {key}")
        print(f"{len(keys)+1}. Annuleren")

        keuze = input("Keuze (nummer): ").strip()
        try:
            idx = int(keuze)
        except ValueError:
            print("Ongeldige keuze. Annuleren.")
            return
        if idx == len(keys) + 1:
            print("Annuleren.")
            return
        if idx < 1 or idx > len(keys):
            print("Ongeldige keuze. Annuleren.")
            return

        sel = keys[idx - 1]
        del examens[sel]
        sla_voortgang_op(data)
        print(f"✅ Examen {sel} (rijbewijs) is gereset.")

    elif m == "2":
        vak = data.get("vakbekwaamheid", {})
        examens_mc = vak.get("examens_mc", {})
        examens_cases = vak.get("examens_cases", {})

        print("\nWelke type vakbekwaamheid-examen?")
        if examens_mc:
            print("1. MC reeksen")
        if examens_cases:
            print("2. Cases reeksen")
        print("3. Annuleren")

        keuze = input("Keuze (nummer): ").strip()
        if keuze == "1" and examens_mc:
            keys = list(examens_mc.keys())
            print("\nKies MC-reeks om te resetten:")
            for i, key in enumerate(keys, start=1):
                print(f"{i}. Reeks {key}")
            print(f"{len(keys)+1}. Annuleren")

            sel_in = input("Keuze (nummer): ").strip()
            try:
                idx = int(sel_in)
            except ValueError:
                print("Ongeldige keuze. Annuleren.")
                return
            if idx == len(keys) + 1:
                print("Annuleren.")
                return
            if idx < 1 or idx > len(keys):
                print("Ongeldige keuze. Annuleren.")
                return
            sel = keys[idx - 1]
            del examens_mc[sel]
            sla_voortgang_op(data)
            print(f"✅ Vakbekwaamheid MC examen reeks {sel} is gereset.")

        elif keuze == "2" and examens_cases:
            keys = list(examens_cases.keys())
            print("\nKies Cases-reeks om te resetten:")
            for i, key in enumerate(keys, start=1):
                print(f"{i}. Reeks {key}")
            print(f"{len(keys)+1}. Annuleren")

            sel_in = input("Keuze (nummer): ").strip()
            try:
                idx = int(sel_in)
            except ValueError:
                print("Ongeldige keuze. Annuleren.")
                return
            if idx == len(keys) + 1:
                print("Annuleren.")
                return
            if idx < 1 or idx > len(keys):
                print("Ongeldige keuze. Annuleren.")
                return
            sel = keys[idx - 1]
            del examens_cases[sel]
            sla_voortgang_op(data)
            print(f"✅ Vakbekwaamheid Cases examen reeks {sel} is gereset.")

        else:
            print("Annuleren of geen reeksen aanwezig.")
            return

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
