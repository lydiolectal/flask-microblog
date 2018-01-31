from app import flaskApp
import os

# translation command group using Click
# cli.group() decorator creates a root for several other sub-commands.
@flaskApp.cli.group()
def translate():
    # help message that is exposed in terminal.
    """Translation and Localization Commands"""
    pass

# decorators for sub-commands of parent command 'translate' derive the name.
@translate.command()
def update():
    """Update all languages."""
    # extraction step.
    # if command executes correctly, return value should be 0. Non-0: error.
    if os.system("pybabel extract -F babel.cfg -k _l -o messages.pot ."):
        raise RuntimeError("extract command failed")
    # update step.
    if os.system("pybabel update -i messages.pot -d app/translations"):
        raise RuntimeError("update command failed")
    os.remove("messages.pot")

@translate.command()
def compile():
    """Compile all languages."""
    if os.system("pybabel compile -d app/translations"):
        raise RuntimeError("compile command failed")

@translate.command()
# defines language code. 'lang' gets passed to handler init() as an argument,
# where it gets passed as part of the pybabel command.
@click.argument("lang")
def init(lang):
    """Initialize a new language."""
    if os.system("pybabel extract -F babel.cfg -k _l -o messages.pot ."):
        raise RuntimeError("extract command failed")
    if os.system("pybabel init -i messages.pot -d app/translations -l " + lang):
        raise RuntimeError("init command failed")
    os.remove("messages.pot")
