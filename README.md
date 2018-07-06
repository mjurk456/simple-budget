# simple-budget
Prosty tracker budżetu.
Użytkownik zadaje początek miesiąca rozliczeniowego,wprowadza wydatki i zaróbki. Program pokazuje, ile jeszcze użytkownik ma
do wydania do końca miesiąca każdy dzień/tydień.
Interfejs programu jest tekstowy. Dane są zapisywane w pliku budget.log w folderze programu. Nie prowadzi się historii zmian. Ewentualne korektury użytkownik może dokonywać, wprowadzając kwoty z odwrotnym znakiem.
Wydatki/dochody zawsze się wprowadza za dzisiaj, nie można zadawać wprzod/wstęcz. Zmiany zapisują się przy wyjściu z programu z użyciem komandy "koniec".

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
