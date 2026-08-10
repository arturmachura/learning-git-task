import functools

from flask import flash, redirect, render_template, request, session, url_for

from blog import app, db
from blog.forms import EntryForm, LoginForm
from blog.models import Entry


def login_required(view_func):
    @functools.wraps(view_func)
    def check_permissions(*args, **kwargs):
        if session.get('logged_in'):
            return view_func(*args, **kwargs)
        return redirect(url_for('login', next=request.path))
    return check_permissions


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
@login_required
def create_entry():
    return _handle_entry_form()


@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
@login_required
def edit_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    return _handle_entry_form(entry)


@app.route("/delete-post/<int:entry_id>", methods=["POST"])
@login_required
def delete_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    db.session.delete(entry)
    db.session.commit()
    flash("Wpis został usunięty.", "success")
    return redirect(url_for("index"))


@app.route("/drafts/", methods=["GET"])
@login_required
def list_drafts():
    drafts = Entry.query.filter_by(is_published=False).order_by(
        Entry.pub_date.desc()
    )
    return render_template("drafts.html", drafts=drafts)


@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    errors = None
    next_url = request.args.get('next')
    if request.method == 'POST':
        if form.validate_on_submit():
            session['logged_in'] = True
            session.permanent = True
            flash('You are now logged in.', 'success')
            return redirect(next_url or url_for('index'))
        errors = form.errors
    return render_template("login_form.html", form=form, errors=errors)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        flash('You are now logged out.', 'success')
    return redirect(url_for('index'))
