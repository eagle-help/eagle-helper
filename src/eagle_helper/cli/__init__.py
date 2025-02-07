import sys

import click
import eagle_helper.etc


def load():
    # analyze sys.argv and check if there is -l at 2nd place
    if len(sys.argv) > 1 and sys.argv[1] == "-l":
        language = sys.argv[2]
        click.echo(f"Setting language to {language}")
        eagle_helper.etc.LANGUAGE_MODE = language
        eagle_helper.etc.I18N_CACHE.clear()

    from .__main__ import cli

    cli()


if __name__ == "__main__":
    load()
