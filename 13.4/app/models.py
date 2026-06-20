from datetime import datetime
from app import db

# tabela pośrednia dla relacji wiele-do-wielu Book <-> Author
book_authors = db.Table(
    "book_authors",
    db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True),
    db.Column("author_id", db.Integer, db.ForeignKey("author.id"), primary_key=True),
)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False, index=True)
    books = db.relationship("Book", secondary=book_authors, back_populates="authors")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    year = db.Column(db.Integer)
    isbn = db.Column(db.String(20), unique=True)
    authors = db.relationship("Author", secondary=book_authors, back_populates="books")
    loans = db.relationship("Loan", back_populates="book", lazy="dynamic")

    @property
    def is_available(self):
        return self.loans.filter_by(returned=False).first() is None

    @property
    def active_loan(self):
        return self.loans.filter_by(returned=False).first()

    def __str__(self):
        return f"{self.title} ({self.year})"


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    borrower = db.Column(db.String(200), nullable=False)
    loaned_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    returned_at = db.Column(db.DateTime)
    returned = db.Column(db.Boolean, default=False, nullable=False)
    book = db.relationship("Book", back_populates="loans")

    def __str__(self):
        return f"Loan({self.borrower}, {self.book.title})"
