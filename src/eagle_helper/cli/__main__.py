import os
import click
from .plugin_init import init
from .plugin_walk import walk
from ..etc.git import git_pull
import eagle_helper
import eagle_helper.etc
import eagle_helper.config
from ..etc import i18n
import subprocess


@click.group(invoke_without_command=True)
@click.option(
    "-l",
    "--language",
    type=str,
    help=i18n("cli.help.language", "Set the language of the tool"),
)
@click.option(
    "-v",
    "--version",
    is_flag=True,
    help=i18n("cli.help.version", "Show the version of the tool"),
)
@click.option(
    "-sc",
    "--skip-check",
    is_flag=True,
    help=i18n("cli.help.skip_check", "Skip the translate check"),
)
@click.option(
    "-sp", "--skip-pull", is_flag=True, help=i18n("cli.help.skip_pull", "Skip the pull")
)
@click.option(
    "-p", "--path", type=str, help=i18n("cli.help.path", "Set the path of the plugin")
)
@click.pass_context
def cli(ctx: click.Context, version, skip_check, language, path, skip_pull):
    if path:
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)

    if not skip_pull:
        git_pull(**eagle_helper.config.UTILS_REPO)
        git_pull(**eagle_helper.config.TEMPLATE_REPO)

    if not skip_check:
        eagle_helper._init_translate_check()

    if language:
        eagle_helper.etc.LANGUAGE_MODE = language

    if version:
        from eagle_helper import __version__

        click.echo(f"Eagle Helper v{__version__}")
        os._exit(0)
    if not ctx.invoked_subcommand:
        click.echo(ctx.get_help())
        os._exit(0)

    ctx.ensure_object(dict)
    ctx.obj["manifest"] = {}
    ctx.obj["skip_check"] = skip_check
    ctx.obj["skip_pull"] = skip_pull

    if not eagle_helper.GIT_IS_INSTALLED:
        click.echo(
            i18n(
                "cli.git_not_installed",
                "Git is not installed, this helper functionality will be very limited.",
            ),
            err=True,
        )


@cli.group("self", help=i18n("cli.internal.help", "Internal commands"))
def internal():
    pass


@internal.command(
    "i18ncache", help=i18n("cli.builtin.i18ncache.help", "Show the i18n cache")
)
def i18ncache():
    from pprint import pprint
    from ..etc import I18N_CACHE

    pprint(I18N_CACHE, width=1000)


@internal.command("config", help=i18n("cli.builtin.config.help", "Show the config"))
def config():
    try:
        subprocess.run(
            ["code", os.path.join(eagle_helper.MOD_PATH, "config.py")], shell=True
        )
    except Exception:
        subprocess.run(
            ["start", os.path.join(eagle_helper.MOD_PATH, "config.py")], shell=True
        )


@internal.command(
    "forcepull", help=i18n("cli.builtin.forcepull.help", "Force pull the repo")
)
def forcepull():
    git_pull(**eagle_helper.config.UTILS_REPO, force=True)
    git_pull(**eagle_helper.config.TEMPLATE_REPO, force=True)


cli.add_command(walk)
cli.add_command(init)
