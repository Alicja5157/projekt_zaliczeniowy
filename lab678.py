import argparse

arg_parser = argparse.ArgumentParser(
    prog='Konwerter Konfiguracji',
    description='Konwertuje pliki konfiguracyjne w formatach xml, json i yml(yaml)')
arg_parser.add_argument('sciezka_pliku1')
arg_parser.add_argument('sciezka_pliku2')
args = arg_parser.parse_args()
sciezka_pliku_1 = args.sciezka_pliku1
sciezka_pliku_2 = args.sciezka_pliku2

print("Konwersja zakończona")
