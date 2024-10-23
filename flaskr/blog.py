from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    aircrafts = db.execute(
        'SELECT a.id, name, description, created, author_id, username'
        ' FROM aircrafts a JOIN user u ON a.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', aircrafts=aircrafts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        aircraft_type = request.form['aircraft_type']
        manufacturer = request.form['manufacturer']
        error = None

        if not name:
            error = 'Aircraft name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO aircrafts (name, aircraft_type, manufacturer, description, author_id)'
                ' VALUES (?, ?, ?, ?, ?)',
                (name, aircraft_type, manufacturer, description, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')
