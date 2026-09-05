from config import INVOER_MAP
from storage import sla_voortgang_op
from utils import valideer_invoer, get_voortgang_hoofdstuk, bereken_stats_hoofdstuk


def oefen_hoofdstuk(data, module_sleutel, database, h_sleutel):
    """Oefenen per hoofdstuk zonder tijdslimiet."""
    module_data = data[module_sleutel]
    h_info = database[h_sleutel]
    h_naam = h_info["naam"]
    mc_vragen = h_info["mc"]
    cases = h_info.get("cases", {})

    voortgang_h = get_voortgang_hoofdstuk(module_data, h_sleutel)
    gemaakt_mc, gemaakt_cases, totaal_in_h = bereken_stats_hoofdstuk(
        voortgang_h, mc_vragen, cases
    )

    # Toon voortgang en vraag of gebruiker wil herstarten
    if (gemaakt_mc + gemaakt_cases) > 0:
        print(
            f"\nJe hebt al {gemaakt_mc + gemaakt_cases} van de {totaal_in_h} vragen gemaakt in '{h_naam}'."
        )
        print("1. Verdergaan waar je gebleven was")
        print("2. Hoofdstuk herstarten (voortgang van dit hoofdstuk wissen)")

        while True:
            k = input("Maak een keuze (1 of 2): ").strip()
            if k == "1":
                break
            elif k == "2":
                module_data["oefenvragen"][h_sleutel] = {"mc": {}, "cases": {}}
                sla_voortgang_op(data)
                print(f"✅ Voortgang van '{h_naam}' is gereset.")
                break

    print("\n==========================================")
    print(f"  HOOFDSTUK {h_sleutel}: {h_naam.upper()}")
    print("  Type 'stop' om de sessie te beëindigen")
    print("==========================================")

    # MC Vragen
    if mc_vragen:
        print("\n--- MEERKEUZEVRAGEN ---")
        for q_nr, corr in mc_vragen.items():
            if str(q_nr) in voortgang_h["mc"]:
                continue

            while True:
                invoer = (
                    input(f"Antwoord Vraag {q_nr} (A/B/C/D of 1/2/3/4): ")
                    .strip()
                    .lower()
                )
                if invoer == "stop":
                    return

                let = valideer_invoer(invoer)
                if let:
                    is_c = let == corr
                    voortgang_h["mc"][str(q_nr)] = {"gegeven": let, "correct": is_c}
                    sla_voortgang_op(data)
                    if is_c:
                        print(f"✅ GOED! Antwoord is {corr}.")
                    else:
                        print(f"❌ FOUT! Jouw antwoord: {let} | Juist: {corr}")
                    break
                else:
                    print("Ongeldige invoer. Voer A, B, C, D in (of 1, 2, 3, 4).")

    # Cases
    for c_naam, c_vragen in cases.items():
        print(f"\n--- {c_naam.upper()} ---")
        c_saved = voortgang_h["cases"].setdefault(c_naam, {})
        for q_nr, corr in c_vragen.items():
            if str(q_nr) in c_saved:
                continue

            while True:
                invoer = (
                    input(f"Antwoord Vraag {q_nr} (A/B/C/D of 1/2/3/4): ")
                    .strip()
                    .lower()
                )
                if invoer == "stop":
                    return

                let = valideer_invoer(invoer)
                if let:
                    is_c = let == corr
                    c_saved[str(q_nr)] = {"gegeven": let, "correct": is_c}
                    sla_voortgang_op(data)
                    if is_c:
                        print(f"✅ GOED! Antwoord is {corr}.")
                    else:
                        print(f"❌ FOUT! Jouw antwoord: {let} | Juist: {corr}")
                    break
                else:
                    print("Ongeldige invoer. Voer A, B, C, D in (of 1, 2, 3, 4).")