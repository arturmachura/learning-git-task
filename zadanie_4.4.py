import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")

dzialanie = int(input("Podaj działanie, posługując się odpowiednią liczbą: 1 Dodawanie, 2 Odejmowanie, 3 Mnożenie, 4 Dzielenie: "))

a = float(input("Podaj składnik 1. "))
b = float(input("Podaj składnik 2. "))

if dzialanie == 1:
    logging.info(f"Dodaję {a:.2f} i {b:.2f}")
    wynik = a + b
elif dzialanie == 2:
    logging.info(f"Odejmuję {a:.2f} i {b:.2f}")
    wynik = a - b
elif dzialanie == 3:
    logging.info(f"Mnożę {a:.2f} i {b:.2f}")
    wynik = a * b
elif dzialanie == 4:
    logging.info(f"Dzielę {a:.2f} i {b:.2f}")
    wynik = a / b

print(f"Wynik to {wynik:.2f}")
