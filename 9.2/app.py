import csv
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

NBP_URL = "https://api.nbp.pl/api/exchangerates/tables/C?format=json"
CSV_FILENAME = "kursy.csv"


def fetch_rates():
    response = requests.get(NBP_URL, timeout=5)
    response.raise_for_status()
    rates = response.json()[0]["rates"]
    for rate in rates:
        rate["bid"] = float(rate["bid"])
        rate["ask"] = float(rate["ask"])
    return rates


def load_cached_rates(filename=CSV_FILENAME):
    try:
        with open(filename, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")
            rates = list(reader)
    except FileNotFoundError:
        return []

    for rate in rates:
        rate["bid"] = float(rate["bid"])
        rate["ask"] = float(rate["ask"])
    return rates


def save_csv(rates, filename=CSV_FILENAME):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["currency", "code", "bid", "ask"], delimiter=";"
        )
        writer.writeheader()
        writer.writerows(rates)


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    try:
        rates = fetch_rates()
        save_csv(rates)
    except (requests.RequestException, ValueError, KeyError, IndexError):
        rates = load_cached_rates()
        if rates:
            error = (
                "Nie udało się pobrać aktualnych kursów z NBP. "
                "Wyświetlane są ostatnio zapisane dane."
            )
        else:
            error = (
                "Nie udało się pobrać kursów walut i nie ma zapisanych danych "
                "lokalnych. Spróbuj ponownie później."
            )

    result = None
    selected_code = request.form.get("currency")
    amount_raw = request.form.get("amount", "")

    if request.method == "POST" and selected_code and amount_raw:
        amount = float(amount_raw)
        rate = next((r for r in rates if r["code"] == selected_code), None)
        if rate:
            result = {
                "amount": amount,
                "code": selected_code,
                "ask": rate["ask"],
                "total": round(amount * rate["ask"], 2),
            }

    return render_template(
        "index.html",
        rates=rates,
        result=result,
        selected_code=selected_code,
        amount=amount_raw,
        error=error,
    )


if __name__ == "__main__":
    app.run(debug=True)
