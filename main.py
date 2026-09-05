from storage import laad_voortgang
from menus import menu_hoofdscherm


def main():
    """Hoofdingang van de applicatie."""
    data = laad_voortgang()
    menu_hoofdscherm(data)


if __name__ == "__main__":
    main()