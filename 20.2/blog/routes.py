from flask import flash, redirect, render_template, request, url_for

from blog import app, db
from blog.forms import EntryForm
from blog.models import Entry


@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(
        Entry.pub_date.desc()
    )
    return render_template("homepage.html", all_posts=all_posts)


def _handle_entry_form(entry=None):
    """Shared logic for creating and editing an Entry.

    If `entry` is None, a new Entry is created on successful submission.
    Otherwise, the given Entry is updated in place.
    """
    form = EntryForm(obj=entry)
    errors = None

    if request.method == "POST":
        if form.validate_on_submit():
            if entry is None:
                entry = Entry()
                db.session.add(entry)
            form.populate_obj(entry)
            db.session.commit()
            flash("Wpis został zapisany!", "success")
            return redirect(url_for("index"))
        errors = form.errors

    return render_template("entry_form.html", form=form, errors=errors)


@app.route("/new-post/", methods=["GET", "POST"])
def create_entry():
    return _handle_entry_form()


@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    return _handle_entry_form(entry)
