import click
from flask import Blueprint, g, render_template, redirect, url_for, request
from flask.cli import with_appcontext

from .db.MongoDB import MongoDatabase as DBHandler
from team.model.captain import Captain
from .model.player import Player

bp = Blueprint('mongobp', __name__, template_folder='templates')


@bp.before_request
def pre_handler():
    if 'form_data' not in g:
        g.form_data = None


@bp.after_request
def post_handler(response):
    DBHandler.close_db()
    return response


@bp.route('/')
def index():
    trainers = DBHandler.get_records()
    return render_template("team.tpl", form_data=g.form_data, items=trainers)


@bp.route('/edit/<id>')
def edit(id):
    g.form_data = DBHandler.get_record(id)
    return index()


@bp.route('/confirm_edit', methods=['POST'])
def confirm_edit():
    record = Captain() if 'grade' in request.form else Player()
    record.input(request.form.to_dict())
    DBHandler.edit_record(record)
    return redirect(url_for('.index'))


@bp.route('/add', methods=['POST'])
def add():
    trainer = Captain()
    trainer.input(request.form.to_dict())
    DBHandler.add_record(trainer)
    return redirect(url_for('.index'))


@bp.route('/add_player', methods=['POST'])
def add_player():
    master = Captain()
    master.input(request.form.to_dict())
    DBHandler.add_record(master)
    return redirect(url_for('.index'))


@bp.route("/delete/<id>")
def delete(id):
    DBHandler.delete_record(id)
    return redirect(url_for('.index'))


@bp.route("/clear")
def clear():
    DBHandler.reset()
    return redirect(url_for('.index'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    DBHandler.init_db()
    click.echo('Initialized the database.')


bp.cli.add_command(init_db_command)
