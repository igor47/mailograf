from collections import Counter
from typing import Any, Dict
import socket
import subprocess

import typer

from mailograf.notmuch import db, tag_counts

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

@app.command()
def counts(inbox: bool = typer.Option(True, help="Only count messages in the inbox")):
    """Show counts of messages by tag"""
    typer.echo(typer.style("Counting messages....", fg="blue"))

    tc = tag_counts("tag:inbox" if inbox else "date:1Y..")
    for tag, count in tc.items():
        if inbox and tag == "inbox":
            continue

        tag = typer.style(tag, fg="green")
        typer.echo(f"\t{tag}: {count}")

@app.command()
def report():
    """report email metrics to telegraf"""
    tags = {
        "user": subprocess.check_output("whoami").strip().decode("utf-8"),
        "host": subprocess.check_output("hostname").strip().decode("utf-8"),
    }

    ct = tag_counts("tag:inbox")
    for tag, count in ct.items():
        report_measurement("emails", tags, tag, count)

    typer.echo(typer.style("Counts reported", fg="green"))

def report_measurement(mname: str, tags: Dict[str, Any], tag: str, count: int) -> None:
    """report email count to telegraf"""
    all_tags = dict({"tag": tag}, **tags)
    tag_str = ",".join(f"{t}={v}" for t, v in all_tags.items())

    line = f"{mname},{tag_str} count={count}"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(line.encode(), ("127.0.0.1", 8094))
