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
