import argparse
import json

def sprawdz(plik, typ_pliku):
    if typ_pliku == "json":
        try:
            json.load(plik)
        except ValueError as e:
            print("Nieprawidłowa składnia JSON")
            print("Szczegóły:", e)
            return False
        except FileNotFoundError:
            print("Nie można odnaleźć pliku:", plik.name)
            return False
        return True
    elif typ_pliku == "yml":
        try:
            yaml.safe_load(plik)
            return True
        except yaml.YAMLError as e:
            print("Wystąpił błąd podczas analizy YAML:", e)
            return False
    elif typ_pliku == "xml":
        try:
            xml_data = plik.read()
            xmltodict.parse(xml_data)
            return True
        except Exception as e:
            print("Wystąpił błąd podczas analizy XML:", e)
            return False


def json_wczytaj(plik_json):
    json_ok = sprawdz(plik_json, "json")
    if json_ok:
        with open(plik_json.name) as plik:
            dane = json.load(plik)
        return dane
    else:
        return False

arg_parser = argparse.ArgumentParser(
    prog='Konwerter Konfiguracji',
    description='Konwertuje pliki konfiguracyjne w formatach xml, json i yml(yaml)')
arg_parser.add_argument('sciezka_pliku1')
arg_parser.add_argument('sciezka_pliku2')
args = arg_parser.parse_args()
sciezka_pliku_1 = args.sciezka_pliku1
sciezka_pliku_2 = args.sciezka_pliku2

with open(sciezka_pliku_1, "r") as plik_1:
    typ_pliku_1 = (plik_1.name.split(".", 1))[1]
    
if os.path.exists(sciezka_pliku_2):
    with open(sciezka_pliku_2, "r") as plik_2:
        typ_pliku_2 = (plik_2.name.split(".", 1))[1]
        plik_2_istnieje = True
else:
    with open(sciezka_pliku_2, "w") as plik_2:
        typ_pliku_2 = (plik_2.name.split(".", 1))[1]
        plik_2_istnieje = False

if plik_2_istnieje:
    if (typ_pliku_1 == "yaml" or typ_pliku_1 == "yml") and (typ_pliku_2 == "yaml" or typ_pliku_2 == "yml"):
        print(plik_1.name, "jest już w formacie pliku YAML")
    elif typ_pliku_1 == typ_pliku_2:
        print(plik_1.name, "jest już w formacie", typ_pliku_1)
else:
    with open(sciezka_pliku_1, "r") as plik_1:
        if typ_pliku_1 == "json":
			obiekt_json = json_wczytaj(plik_1)
		else:
            obiekt_json = None
    
    if not obiekt_json:
        print("Błąd wczytywania pliku")
        exit(1)

print("Konwersja zakończona")
