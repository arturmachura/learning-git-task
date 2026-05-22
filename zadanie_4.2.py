"""
Zadanie 4.2 – Sprawdzanie palindromu

Funkcja is_palindrome przyjmuje jeden argument typu string i zwraca True,
jesli podany tekst jest palindromem (czytany tak samo od lewej i od prawej),
lub False w przeciwnym wypadku. Porownanie jest niewrazliwe na wielkosc liter.

Przyklady palindromow: "kajak", "potop", "Anna", "level"
"""


def is_palindrome(text: str) -> bool:
    """Zwraca True jeśli text jest palindromem, False w przeciwnym razie."""
    normalized = text.lower()
    return normalized == normalized[::-1]


if __name__ == "__main__":
    test_cases = [
        ("kajak", True),
        ("potop", True),
        ("Anna", True),
        ("level", True),
        ("python", False),
        ("hello", False),
    ]

    for word, expected in test_cases:
        result = is_palindrome(word)
        status = "OK" if result == expected else "FAIL"
        print(f"[{status}] is_palindrome({word!r}) = {result}")
