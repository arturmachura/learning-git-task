import csv
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

NBP_URL = "https://api.nbp.pl/api/exchangerates/tables/C?format=json"


def fetch_rates():
    response = requests.get(NBP_URL)
    return response.json()[0]["rates"]


def save_csv(rates, filename="kursy.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["currency", "code", "bid", "ask"], delimiter=";"
        )
        writer.writeheader()
        writer.writerows(rates)


@app.route("/", methods=["GET", "POST"])
def index():
    rates = fetch_rates()
    save_csv(rates)

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
    )


if __name__ == "__main__":
    app.run(debug=True)
