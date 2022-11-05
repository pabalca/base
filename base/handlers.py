import click

from base import app
from base.models import User, Secret, db


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Secret=Secret, User=User)


@app.cli.command()
@click.option("--drop", is_flag=True, help="Create after drop.")
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("Initialized database.")

