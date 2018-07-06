"""Prosty tracker budżetu.
Użytkownik zadaje początek miesiąca rozliczeniowego,
wprowadza wydatki i zaróbki. Program pokazuje, ile jeszcze użytkownik ma
do wydania do końca miesiąca każdy dzień/tydień.
Interfejs programu jest tekstowy. Dane są zapisywane w pliku budget.log
w folderze programu. Nie prowadzi się historii zmian. Ewentualne korektury
użytkownik może dokonywać, wprowadzając kwoty z odwrotnym znakiem.
Wydatki/dochody zawsze się wprowadza za dzisiaj, nie można zadawać
wprzod/wstęcz. Zmiany zapisują się automatycznie.

Przykład zapisów (założmy, że dzisiaj jest 1.07.2018, początkowy staw 0):
z 12.07.2018 (wprowadzenie/zmiana początku miesiąca rozliczeniowego)
2500
-20.35
-15
15 (korekta poprzedniego zapisu)

Przykład odpowiedzi programu:
Do wydania 2479.65
Do wydania każdego dnia (bez dzisiaj): 206.63
Do wydania każdy tydzień
"""

import pickle
import datetime
import re

""" Ładowanie pliku z danymi.
Struktura danych w słowniku:
{'balance': aktualny bilans,
 'period': data następnej wypłaty}  
"""
def initialize(file):
    try:
        with open(file, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        # jeśli plik nie istnieje, to tworzę go z domyślnymi danymi
        with open(file, 'wb') as f:
            b = {'balance': 0, 'day': 0,
                  'week': 0, 'period':datetime.date.today()}
            pickle.dump(b, f)
        # załądowuję plik. Taki sposób został wybrany, aby mieć pewność,
        # że zapisanie pliku sie powiodło
        with open(file, 'rb') as f:
            return pickle.load(f)

        
"""drukuje statystykę:
Stan na dzisiaj: x
Każdy dzień można wydać: y
Każdy tydzień można wydać: z
Następna wypłata: dd-mm-yyyy
"""
def print_statistics(b):
    diff = b['period'] - datetime.date.today()
    d = round(b["balance"] / diff.days, 2)
    if diff.days < 7:
        w = b['balance']
    else:
        w = d * 7
    stats = "Stan na dzisiaj: {0}\n" \
            + "Każdy dzień można wydać: {1}\n" \
            + "Każdy tydzień można wydać: {2}\n" \
            + "Następna wypłata: {3}\n"
    print("*" * 35)
    print(stats.format(b['balance'], d, w, b['period'].strftime("%d-%m-%Y")))
    print("*" * 35)
    return None                         


"""rozlicza dzień następnej wypłaty
generalnie jest to ten samy dzień w następnym miesiącu
(każda firma ma swoje reguły, dlatego nie wprowadzam poprawki
na dni wolne od pracy)
Jeśli dzień wypłaty przypada na 29-31, a nastepny miesiąc jest
luty, to zmieniam datę na 28.02. Użytkownik potem poprawi ją
ręcznie
Argument jest datetime.date
"""
def add_period(b):
    if (29<= b.day <= 31) and (b.month + 1 == 2):
        return {'day': 28,
                'month': 2,
                'year': b.year}
    elif (b.month + 1 == 13):
        return {'day': b.day,
                'month': 1,
                'year': b.year + 1}
    else:
        return {'day': b.day,
                'month': b.month + 1,
                'year': b.year}
    
    
def main():
    file = "budget.log"
    budget = initialize(file)
    # jeśli dzisiaj jest dzien wypłaty, to przenieśc datę dalszej wypłaty
    if budget['period'] <= datetime.date.today():
        nextMoney = add_period(budget['period'])
        budget['period'] = datetime.date(nextMoney['year'], nextMoney['month'], nextMoney['day'])
    print_statistics(budget)
    print("Opcje: \n z dd-mm-yyyy - wprowadzić datę nastepnej wypłaty")
    print("liczba dodatnia, np. 500 - dodać dochód")
    print("liczba ujemna, np. -120 - dodać wydatek za dziś")
    print("koniec - zapisać zmiany i zamknąć program")
    print("staw - pokazać aktualny staw")
    while True:
        data = input("? ").lower().strip()
        # użytkownik chce wprowadzic datę?
        changes = re.fullmatch(r"^z (\d\d).(\d\d).(\d\d\d\d)$", data)
        # użytkownik chce wprowadzic kwotę?
        money = re.fullmatch(r"-?\d+[.,]?\d+", data)
        # użytkownik zamyka program
        end = (data == 'koniec')
        # użytkownik chce zobaczyć statystyki
        stats = (data == 'staw')
        if end:
            with open(file, "wb") as f:
                pickle.dump(budget, f)
            print("Do widzenia!")
            return None

        elif stats:
            print_statistics(budget)

        elif changes:
            try:
                changeDate = datetime.date(int(changes.group(3)),
                                           int(changes.group(2)),
                                           int(changes.group(1)))
                if changeDate > datetime.date.today():
                    budget['period'] = changeDate
                    print("Datum zmieniony")
                else:
                    print("Nie mozna zadać datum do tyłu.")
            except ValueError:
                print("Źle zadany datum")

        elif money:
            try:
                amount = float(money.group(0))
                budget['balance'] += amount                    
            except ValueError:
                print("Źle zadana kwota")

        else:
            print("Niepoprawne wprowadzone dane")
                

if __name__ == "__main__":
    main()
