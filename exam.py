import time

from config import (
    SLAGINGSCRITERIUM_RIJBEWIJS,
    SLAGINGSCRITERIUM_VAK_CASES,
    SLAGINGSCRITERIUM_VAK_MC,
    TIJDLIMIET_GEWOON_EXAMEN_MIN,
    TIJDLIMIET_VAK_CASES_MIN,
    TIJDLIMIET_VAK_MC_MIN,
)
from storage import markeer_examen_geslaagd, sla_voortgang_op
from utils import valideer_invoer


def voer_examen_onderdeel_uit(
    vragen_dict, opslag_dict, start_tijd, tijdslimiet_minuten, label_prefix=""
):
    """
    Universele functie om vragen te stellen met een actieve timer.
    """
    tijdslimiet_sec = tijdslimiet_minuten * 60

    for q_nr in range(1, len(vragen_dict) + 1):
        if str(q_nr) in opslag_dict:
            continue

        verstreken = time.time() - start_tijd
        resterend = tijdslimiet_sec - verstreken

        if resterend <= 0:
            print("\n⏰ Tijd is om! Het examen wordt afgesloten.")
            return False  # Tijd verstreken

        m, s = divmod(int(resterend), 60)
        tijd_str = f"[{m:02d}:{s:02d} over]"

        while True:
            invoer = (
                input(
                    f"{tijd_str} {label_prefix}Vraag {q_nr}/{len(vragen_dict)} (A/B/C/D): "
                )
                .strip()
                .lower()
            )

            # Controleer direct na invoer opnieuw op tijd
            if (time.time() - start_tijd) >= tijdslimiet_sec:
                print("\n⏰ Tijd is om! Dit antwoord telt niet meer mee.")
                return False

            if invoer == "stop":
                return None  # Gestopt door gebruiker

            let = valideer_invoer(invoer)
            if let:
                opslag_dict[str(q_nr)] = let
                break
            print("Ongeldige invoer. Voer A, B, C, D in (of 1, 2, 3, 4).")

    return True


def check_slagingsstatus(score, totaal, exam_type):
    """
    Controleer of de score aan het slagingscriterium voldoet.
    Retourneert (geslaagd: bool, minimale_score: int)
    """
    if exam_type == "rijbewijs":
        minimaal = SLAGINGSCRITERIUM_RIJBEWIJS
    elif exam_type == "vak_mc":
        minimaal = SLAGINGSCRITERIUM_VAK_MC
    elif exam_type == "vak_cases":
        minimaal = SLAGINGSCRITERIUM_VAK_CASES
    else:
        minimaal = 0

    return score >= minimaal, minimaal


def start_rijbewijs_examen(data, reeks):
    """Gewoon Rijbewijs Examen met timer."""
    examens = data["rijbewijs"].setdefault("examens", {})
    if reeks not in examens:
        examens[reeks] = {"antwoorden": {}, "score": 0, "start_tijd": time.time()}
    ex_data = examens[reeks]

    if len(ex_data["antwoorden"]) > 0:
        print(f"\nEr is al voortgang voor Examen {reeks}.")
        print("1. Verdergaan\n2. Herstarten")
        if input("Keuze (1 of 2): ").strip() == "2":
            examens[reeks] = {"antwoorden": {}, "score": 0, "start_tijd": time.time()}
            ex_data = examens[reeks]
            sla_voortgang_op(data)

    from database import RIJBEWIJS_EXAMEN_REEKSEN

    sleutel = RIJBEWIJS_EXAMEN_REEKSEN[reeks]
    print("\n==========================================")
    print(f"  START GEWOON RIJBEWIJS EXAMEN {reeks}")
    print(f"  Tijdslimiet: {TIJDLIMIET_GEWOON_EXAMEN_MIN} minuten (50 vragen)")
    print(f"  Slagingscriterium: minstens {SLAGINGSCRITERIUM_RIJBEWIJS}/50")
    print("==========================================")

    start_tijd = ex_data.get("start_tijd", time.time())
    res = voer_examen_onderdeel_uit(
        sleutel, ex_data["antwoorden"], start_tijd, TIJDLIMIET_GEWOON_EXAMEN_MIN
    )

    if res is None:
        sla_voortgang_op(data)
        return

    juist = sum(1 for q, a in ex_data["antwoorden"].items() if sleutel[int(q)] == a)
    ex_data["score"] = juist
    sla_voortgang_op(data)

    geslaagd, minimaal = check_slagingsstatus(juist, 50, "rijbewijs")
    if geslaagd:
        print(f"\n🎉 EXAMEN VOLTOOID! Score: {juist} / 50")
        print("✅ JE BENT GESLAAGD!")
        # Mark exam as passed
        markeer_examen_geslaagd(data, "rijbewijs", reeks)
    else:
        print(f"\n🎉 EXAMEN VOLTOOID! Score: {juist} / 50")
        print(f"❌ JE BENT NIET GESLAAGD. Je had minstens {minimaal} punten nodig.")


def start_vakbekwaamheid_mc_examen(data, reeks):
    """Vakbekwaamheid MC Examen met timer."""
    examens = data["vakbekwaamheid"].setdefault("examens_mc", {})
    r_data = examens.setdefault(
        reeks, {"antwoorden": {}, "score": 0, "start_tijd": time.time()}
    )

    if len(r_data["antwoorden"]) > 0:
        print(f"\nEr is al voortgang voor MC Examen Reeks {reeks}.")
        print("1. Verdergaan\n2. Herstarten")
        if input("Keuze (1 of 2): ").strip() == "2":
            examens[reeks] = {"antwoorden": {}, "score": 0, "start_tijd": time.time()}
            r_data = examens[reeks]
            sla_voortgang_op(data)

    from database import VAK_EXAMEN_REEKSEN

    ex_def = VAK_EXAMEN_REEKSEN[reeks]["mc"]
    print("\n==========================================")
    print(f"  VAKBEKWAAMHEID MC EXAMEN REEKS {reeks}")
    print(f"  Tijdslimiet: {TIJDLIMIET_VAK_MC_MIN} minuten (50 vragen)")
    print(f"  Slagingscriterium: minstens {SLAGINGSCRITERIUM_VAK_MC}/50")
    print("==========================================")

    start_tijd = r_data.get("start_tijd", time.time())
    res = voer_examen_onderdeel_uit(
        ex_def, r_data["antwoorden"], start_tijd, TIJDLIMIET_VAK_MC_MIN
    )

    if res is None:
        sla_voortgang_op(data)
        return

    juist = sum(1 for q, a in r_data["antwoorden"].items() if ex_def[int(q)] == a)
    r_data["score"] = juist
    sla_voortgang_op(data)

    geslaagd, minimaal = check_slagingsstatus(juist, 50, "vak_mc")
    if geslaagd:
        print(f"\n🎉 MC EXAMEN VOLTOOID! Score: {juist} / 50")
        print("✅ JE BENT GESLAAGD!")
        # Mark exam as passed
        markeer_examen_geslaagd(data, "vakbekwaamheid", reeks, "mc")
    else:
        print(f"\n🎉 MC EXAMEN VOLTOOID! Score: {juist} / 50")
        print(f"❌ JE BENT NIET GESLAAGD. Je had minstens {minimaal} punten nodig.")


def start_vakbekwaamheid_cases_examen(data, reeks):
    """Vakbekwaamheid Cases Examen met timer."""
    examens = data["vakbekwaamheid"].setdefault("examens_cases", {})
    r_data = examens.setdefault(
        reeks, {"cases": {}, "score": 0, "start_tijd": time.time()}
    )

    if len(r_data["cases"]) > 0:
        print(f"\nEr is al voortgang voor Cases Examen Reeks {reeks}.")
        print("1. Verdergaan\n2. Herstarten")
        if input("Keuze (1 of 2): ").strip() == "2":
            examens[reeks] = {"cases": {}, "score": 0, "start_tijd": time.time()}
            r_data = examens[reeks]
            sla_voortgang_op(data)

    from database import VAK_EXAMEN_REEKSEN

    ex_def = VAK_EXAMEN_REEKSEN[reeks]["cases"]
    print("\n==========================================")
    print(f"  VAKBEKWAAMHEID CASES EXAMEN REEKS {reeks}")
    print(f"  Tijdslimiet: {TIJDLIMIET_VAK_CASES_MIN} minuten (8 Cases / 40 vragen)")
    print(f"  Slagingscriterium: minstens {SLAGINGSCRITERIUM_VAK_CASES}/40")
    print("==========================================")

    start_tijd = r_data.get("start_tijd", time.time())

    for c_naam, c_vragen in ex_def.items():
        print(f"\n--- {c_naam.upper()} ---")
        c_saved = r_data["cases"].setdefault(c_naam, {})
        res = voer_examen_onderdeel_uit(
            c_vragen,
            c_saved,
            start_tijd,
            TIJDLIMIET_VAK_CASES_MIN,
            label_prefix=f"{c_naam} ",
        )
        if res is False or res is None:
            break

    # Berekenen Resultaat
    juist = 0
    totaal_vragen = sum(len(v) for v in ex_def.values())
    for c_naam, c_vragen in ex_def.items():
        for q_nr, corr in c_vragen.items():
            if r_data["cases"].get(c_naam, {}).get(str(q_nr)) == corr:
                juist += 1

    r_data["score"] = juist
    sla_voortgang_op(data)

    geslaagd, minimaal = check_slagingsstatus(juist, totaal_vragen, "vak_cases")
    if geslaagd:
        print(f"\n🎉 CASES EXAMEN VOLTOOID! Score: {juist} / {totaal_vragen}")
        print("✅ JE BENT GESLAAGD!")
        # Mark exam as passed
        markeer_examen_geslaagd(data, "vakbekwaamheid", reeks, "cases")
    else:
        print(f"\n🎉 CASES EXAMEN VOLTOOID! Score: {juist} / {totaal_vragen}")
        print(f"❌ JE BENT NIET GESLAAGD. Je had minstens {minimaal} punten nodig.")
