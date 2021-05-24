import typer

from mailograf.notmuch import db

app = typer.Typer()

@app.callback()
def callback():
    """Logging notmuch mail stats to telegraf"""

@app.command()
def tags(inbox: bool = typer.Option(False, help="Only show tags in the inbox")):
    """Show the available tags and counts"""
    typer.echo("showing tags:")
    tags = db.get_all_tags()
    for tag in tags:
        typer.echo(tag)

