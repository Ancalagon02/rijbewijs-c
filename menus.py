from config import (
    TIJDLIMIET_GEWOON_EXAMEN_MIN,
    TIJDLIMIET_VAK_CASES_MIN,
    TIJDLIMIET_VAK_MC_MIN,
)
from database import RIJBEWIJS_HOOFDSTUKKEN, VAK_HOOFDSTUKKEN
from exam import (
    start_rijbewijs_examen,
    start_vakbekwaamheid_cases_examen,
    start_vakbekwaamheid_mc_examen,
)
from practice import oefen_hoofdstuk


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


def menu_hoofdscherm(data):
    """Hoofdmenu van de applicatie."""
    while True:
        print("\n==================================")
        print("      HOOFDMENU SELECTIE          ")
        print("==================================")
        print("1. Gewoon Rijbewijs")
        print("2. Vakbekwaamheid")
        print("3. Afsluiten")

        keuze = input("\nWaarvoor wil je oefenen? (1-3): ").strip()
        if keuze == "1":
            menu_rijbewijs(data)
        elif keuze == "2":
            menu_vakbekwaamheid(data)
        elif keuze == "3":
            print("Tot ziens!")
            break
