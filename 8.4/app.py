from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/mypage/me")
def me():
    return render_template("me.html")


@app.route("/mypage/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("imie")
        email = request.form.get("email")
        subject = request.form.get("temat")
        message = request.form.get("wiadomosc")
        print(f"Nowa wiadomość od: {name} <{email}>")
        print(f"Temat: {subject}")
        print(f"Treść: {message}")
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
