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
        'SELECT a.id, name, description, created, author_id, username, aircraft_type, manufacturer'
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


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    db = get_db()
    aircrafts = db.execute(
        'SELECT * FROM aircrafts WHERE id = ? AND author_id = ?',
        (id, g.user['id'])
    ).fetchone()

    if aircrafts is None:
        abort(404, "Aircraft id {0} doesn't exist or you don't have permission.".format(id))

    if request.method == 'POST':
        name = request.form['name']
        aircraft_type = request.form['aircraft_type']
        manufacturer = request.form['manufacturer']
        description = request.form['description']
        error = None

        if not name:
            error = 'Aircraft name is required.'

        if error is not None:
            flash(error)
        else:
            db.execute(
                'UPDATE aircrafts SET name = ?, aircraft_type = ?, manufacturer = ?, description = ? WHERE id = ?',
                (name, aircraft_type, manufacturer, description, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', aircraft=aircrafts)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    db = get_db()
    aircrafts = db.execute(
        'SELECT id FROM aircrafts WHERE id = ? AND author_id = ?',
        (id, g.user['id'])
    ).fetchone()

    if aircrafts is None:
        abort(404, "Aircraft id {0} doesn't exist or you don't have permission.".format(id))

    db.execute('DELETE FROM aircrafts WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
