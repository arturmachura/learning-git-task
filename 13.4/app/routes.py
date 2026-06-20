from datetime import datetime
from flask import render_template, redirect, url_for, request, flash, abort
from app import app, db
from app.models import Book, Author, Loan


# ── Strona główna ──────────────────────────────────────────────────────────────

@app.route("/")
def index():
    books = Book.query.order_by(Book.title).all()
    return render_template("index.html", books=books)


# ── Autorzy ───────────────────────────────────────────────────────────────────

@app.route("/authors")
def authors():
    all_authors = Author.query.order_by(Author.last_name).all()
    return render_template("authors.html", authors=all_authors)


@app.route("/authors/add", methods=["GET", "POST"])
def add_author():
    if request.method == "POST":
        first = request.form.get("first_name", "").strip()
        last = request.form.get("last_name", "").strip()
        if not first or not last:
            flash("Imię i nazwisko są wymagane.", "danger")
            return redirect(url_for("add_author"))
        author = Author(first_name=first, last_name=last)
        db.session.add(author)
        db.session.commit()
        flash(f"Dodano autora: {author}", "success")
        return redirect(url_for("authors"))
    return render_template("add_author.html")


# ── Książki ───────────────────────────────────────────────────────────────────

@app.route("/books/add", methods=["GET", "POST"])
def add_book():
    authors = Author.query.order_by(Author.last_name).all()
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        year = request.form.get("year", "").strip()
        isbn = request.form.get("isbn", "").strip() or None
        author_ids = request.form.getlist("author_ids")

        if not title:
            flash("Tytuł jest wymagany.", "danger")
            return render_template("add_book.html", authors=authors)

        book = Book(
            title=title,
            year=int(year) if year.isdigit() else None,
            isbn=isbn,
        )
        for aid in author_ids:
            author = Author.query.get(int(aid))
            if author:
                book.authors.append(author)

        db.session.add(book)
        db.session.commit()
        flash(f"Dodano książkę: {book.title}", "success")
        return redirect(url_for("index"))
    return render_template("add_book.html", authors=authors)


@app.route("/books/<int:book_id>")
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    loans = book.loans.order_by(Loan.loaned_at.desc()).all()
    return render_template("book_detail.html", book=book, loans=loans)


# ── Wypożyczenia ──────────────────────────────────────────────────────────────

@app.route("/books/<int:book_id>/loan", methods=["POST"])
def loan_book(book_id):
    book = Book.query.get_or_404(book_id)
    if not book.is_available:
        flash("Książka jest już wypożyczona.", "warning")
        return redirect(url_for("book_detail", book_id=book_id))
    borrower = request.form.get("borrower", "").strip()
    if not borrower:
        flash("Podaj imię osoby.", "danger")
        return redirect(url_for("book_detail", book_id=book_id))
    loan = Loan(book=book, borrower=borrower)
    db.session.add(loan)
    db.session.commit()
    flash(f'Wypożyczono "{book.title}" dla {borrower}.', "success")
    return redirect(url_for("book_detail", book_id=book_id))


@app.route("/loans/<int:loan_id>/return", methods=["POST"])
def return_book(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    if loan.returned:
        abort(400)
    loan.returned = True
    loan.returned_at = datetime.utcnow()
    db.session.commit()
    flash(f'Zwrócono "{loan.book.title}".', "success")
    return redirect(url_for("book_detail", book_id=loan.book_id))
