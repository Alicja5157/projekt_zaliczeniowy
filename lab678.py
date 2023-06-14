import argparse
import json
import yaml
import xmltodict
import os

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


def json_zapisz(obiekt, typ_obiektu):
    if typ_obiektu == "yml" or typ_obiektu == "yaml":
        try:
            dane_json = json.dumps(obiekt, indent=2, separators=(", ", ": "))
            return dane_json
        except yaml.YAMLError as e:
            print("Wystąpił błąd podczas przetwarzania YAML:", e)
    elif typ_obiektu == "xml":
        try:
            dane_xml = xmltodict.parse(obiekt)
            dane_json = json.dumps(dane_xml)
            return dane_json
        except Exception as e:
            print("Wystąpił błąd podczas przetwarzania XML:", e)
    elif typ_obiektu == "json":
        try:
            dane_json = json.dumps(obiekt)
            return dane_json
        except Exception as e:
            print("Wystąpił błąd podczas przetwarzania JSON:", e)


def yml_wczytaj(plik_yml):
    yml_ok = sprawdz(plik_yml, "yml")
    if yml_ok:
        with open(plik_yml.name, "r") as plik:
            tresc_yml = plik.read()
        dane = yaml.safe_load(tresc_yml)
        return dane
    else:
        return False
        

def yml_zapisz(obiekt, typ_obiektu):
    if typ_obiektu == "json":
        try:
            dane_yml = yaml.dump(obiekt)
            return dane_yml
        except Exception as e:
            print("Wystąpił błąd podczas przetwarzania JSON:", e)
    elif typ_obiektu == "xml":
        try:
            dane_xml = xmltodict.parse(obiekt)
            dane_yml = yaml.dump(dane_xml)
            return dane_yml
        except Exception as e:
            print("Wystąpił błąd podczas przetwarzania XML:", e)
    elif typ_obiektu == "yml" or typ_obiektu == "yaml":
        try:
            dane_yml = yaml.dump(obiekt)
            return dane_yml
        except Exception as e:
            print("Wystąpił błąd podczas przetwarzania YAML:", e)


def xml_wczytaj(plik_xml):
    xml_ok = sprawdz(plik_xml, "xml")
    if xml_ok:
        with open(plik_xml.name, "r") as plik:
            tresc_xml = plik.read()
        dane = xmltodict.parse(tresc_xml)
        return dane
    else:
        return False


def xml_zapisz(obiekt, typ_obiektu):
    if typ_obiektu == "json":
        try:
            dane_json = json.dumps(obiekt)
            dane_json = "[" + dane_json + "]"
            dane_json = json.loads(dane_json)
            dane_xml = xmltodict.unparse({'root': dane_json}, pretty=True)
            return dane_xml
        except Exception as e:
            print("Wystąpił błąd podczas przetwarzania JSON:", e)
    elif typ_obiektu == "yml" or typ_obiektu == "yaml":
        try:
            dane_yml = yaml.safe_dump(obiekt)
            dane_xml = xmltodict.unparse({'root': dane_yml}, pretty=True)
            return dane_xml
        except Exception as e:
            print("Wystąpił błąd podczas przetwarzania YAML:", e)
    elif typ_obiektu == "xml":
        try:
            dane_xml = xmltodict.unparse(obiekt, pretty=True)
            return dane_xml
        except Exception as e:
            print("Wystąpił błąd podczas przetwarzania XML:", e)
                    
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
        elif typ_pliku_1 == "yml" or typ_pliku_1 == "yaml":
            obiekt_yml = yml_wczytaj(plik_1)
        elif typ_pliku_1 == "xml":
            obiekt_xml = xml_wczytaj(plik_1)
        else:
            obiekt_json = None
            obiekt_yml = None
            obiekt_xml = None
    
    if not obiekt_json and not obiekt_yml and not obiekt_xml:
        print("Błąd wczytywania pliku")
        exit(1)
        
    if typ_pliku_2 == "json":
        if typ_pliku_1 == "yaml" or typ_pliku_1 == "yml":
            dane_json = json_zapisz(obiekt_yml, typ_pliku_1)
            with open(plik_2.name, "w") as plik_json:
                plik_json.write(dane_json)
        elif typ_pliku_1 == "xml":
            dane_json = json_zapisz(obiekt_xml, typ_pliku_1)
            with open(plik_2.name, "w") as plik_json:
                plik_json.write(dane_json)
    elif typ_pliku_2 == "yaml" or typ_pliku_2 == "yml":
        if typ_pliku_1 == "json":
            dane_yml = yml_zapisz(obiekt_json, typ_pliku_1)
            with open(plik_2.name, "w") as plik_yml:
                plik_yml.write(dane_yml)
        elif typ_pliku_1 == "xml":
            dane_yml = yml_zapisz(obiekt_xml, typ_pliku_1)
            with open(plik_2.name, "w") as plik_yml:
                plik_yml.write(dane_yml)
    elif typ_pliku_2 == "xml":
        if typ_pliku_1 == "json":
            dane_xml = xml_zapisz(obiekt_json, typ_pliku_1)
            with open(plik_2.name, "w") as plik_xml:
                plik_xml.write(dane_xml)
        elif typ_pliku_1 == "yaml" or typ_pliku_1 == "yml":
            dane_xml = xml_zapisz(obiekt_yml, typ_pliku_1)
            with open(plik_2.name, "w") as plik_xml:
                plik_xml.write(dane_xml)

print("Konwersja zakończona")
