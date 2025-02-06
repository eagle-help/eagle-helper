import sys

import click
import eagle_helper.utils

def load():
    # analyze sys.argv and check if there is -l at 2nd place
    if len(sys.argv) > 1 and sys.argv[1] == "-l":
        language = sys.argv[2]
        click.echo(f"Setting language to {language}")
        eagle_helper.utils.LANGUAGE_MODE = language
        eagle_helper.utils.I18N_CACHE.clear()

    from .base import cli
    cli()


if __name__ == "__main__":
    load()

