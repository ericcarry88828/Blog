from functools import wraps
from flask import Blueprint, abort, flash, g, redirect, render_template, request, session, url_for

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session.clear()
            session['user_id'] = 'admin'
            return redirect((url_for('admin.admin')))
        else:
            flash("You are not a admin")

    if g.user == "admin":
        return redirect(url_for("blog.index"))

    return render_template('login.html')


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('blog.index'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = "admin"


@bp.after_app_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


def admin_required(view):
    @wraps(view)
    def decorated_function(*args, **kwargs):
        if g.user != "admin":
            abort(403)
        return view(*args, **kwargs)
    return decorated_function


# def login_required(view):
#     @wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             return redirect(url_for('auth.login'))

#         return view(**kwargs)

    return wrapped_view
