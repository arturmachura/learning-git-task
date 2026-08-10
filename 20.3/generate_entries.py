from faker import Faker

from blog import app, db
from blog.models import Entry


def generate_entries(how_many=10):
    fake = Faker()

    for _ in range(how_many):
        post = Entry(
            title=fake.sentence(),
            body='\n'.join(fake.paragraphs(15)),
            is_published=True,
        )
        db.session.add(post)
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        generate_entries()
        print("Done!")
