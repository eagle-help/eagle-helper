import os
import uuid
import click
import json
from ..coms.gitPull import git_pull
import eagle_helper.coms.manifest as manifest_maker
import eagle_helper.coms.locales as locales_maker
import inspect
import eagle_helper
import eagle_helper.utils
import eagle_helper.config
from ..utils import i18n
from ..config import FULL_SET_OF_LOCALES, LITE_SET_OF_LOCALES


def _filter_kwargs(kwargs, func):
    sig = inspect.signature(func)
    kw = {k: v for k, v in kwargs.items() if k in sig.parameters}
    return func(**kw)


@click.group(invoke_without_command=True)
@click.option("-l", "--language", type=str, help=i18n("cli.help.language", "Set the language of the plugin"))
@click.option("-v", "--version", is_flag=True, help=i18n("cli.help.version", "Show the version of the plugin"))
@click.option("-sc", "--skip-check", is_flag=True, help=i18n("cli.help.skip_check", "Skip the translate check"))
@click.option("-p", "--path", type=str, help=i18n("cli.help.path", "Set the path of the plugin"))
@click.pass_context
def cli(ctx, version, skip_check, language, path):

    if path:
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)

    if not skip_check:
        git_pull(**eagle_helper.config.UTILS_REPO)
        eagle_helper._init_translate_check()

    if language:
        eagle_helper.utils.LANGUAGE_MODE = language

    if version:
        from eagle_helper import __version__

        click.echo(f"Eagle Helper v{__version__}")
        os._exit(0)
    if not ctx.invoked_subcommand:
        click.echo(ctx.get_help())
        os._exit(0)


    ctx.ensure_object(dict)
    ctx.obj["manifest"] = {}

    if not eagle_helper.GIT_IS_INSTALLED:
        click.echo(
            i18n(
                "cli.git_not_installed",
                "Git is not installed, this helper functionality will be very limited.",
            ),
            err=True,
        )

@cli.group("internal", help=i18n("cli.internal.help", "Internal commands"))
def internal():
    pass

@internal.command("i18ncache", help=i18n("cli.builtin.i18ncache.help", "Show the i18n cache"))
def i18ncache():
    from pprint import pprint
    from ..utils import I18N_CACHE
    pprint(I18N_CACHE, width=1000)

@cli.group(
    "init",
    invoke_without_command=True,
    chain=True,
    help=i18n("cli.init.help", "Initialize a new plugin"),
)
@click.argument("name")
@click.option(
    "--id", type=str, default=None, help=i18n("cli.init.help.id", "The id of the plugin")
)
@click.option(
    "--version",
    type=str,
    default="1.0.0",
    help=i18n("cli.init.help.version", "The version of the plugin"),
)
@click.option(
    "--platform",
    type=click.Choice(["all", "mac", "win"]),
    default="all",
    help=i18n("cli.init.help.platform", "The platform of the plugin"),
)
@click.option(
    "--arch",
    type=click.Choice(["all", "arm", "x64"]),
    default="all",
    help=i18n("cli.init.help.arch", "The architecture of the plugin"),
)
@click.option(
    "--name",
    type=str,
    default=None,
    help=i18n("cli.init.help.name", "The name of the plugin"),
)
@click.option(
    "--logo",
    type=str,
    default=None,
    help=i18n("cli.init.help.logo", "The logo of the plugin"),
)
@click.option(
    "--keywords",
    type=str,
    default=None,
    help=i18n("cli.init.help.keywords", "The keywords of the plugin"),
)
@click.option(
    "-d",
    "--devtools",
    type=bool,
    default=True,
    help=i18n("cli.init.help.devtools", "Whether to use devtools"),
)
@click.option(
    "-l",
    "--use-locales",
    type=bool,
    default=False,
    help=i18n("cli.init.help.use_locales", "Whether to use locales"),
)
@click.option(
    "-ld",
    "--locales-default",
    type=str,
    default="en",
    help=i18n("cli.init.help.locales_default", "The default language of the plugin"),
)
@click.option(
    "-ll",
    "--locales-languages",
    type=str,
    default=LITE_SET_OF_LOCALES,
    help=i18n("cli.init.help.locales_languages", "The languages of the plugin"),
)
@click.option(
    "-lf",
    "--locales-full",
    is_flag=True,
    help=i18n(
        "cli.init.help.locales_full",
        "Whether to use the full set of locales marked in template projects",
    ),
)
@click.pass_obj
def init(obj, **kwargs):
    obj["manifest"] = _filter_kwargs(kwargs, manifest_maker.manifest)

    if kwargs.get("use_locales", False):
        languages = (
            kwargs.get("locales_languages", LITE_SET_OF_LOCALES)
            if kwargs.get("locales_full", False)
            else FULL_SET_OF_LOCALES
        )

        locales_maker.setup_locales(
            obj["manifest"], kwargs.get("locales_default", "en"), languages
        )

    with open("manifest.json", "w") as f:
        json.dump(obj["manifest"], f, indent=4)


def _window_options(f):
    @click.option(
        "--url",
        type=str,
        required=True,
        help=i18n("cli.init.window.help.url", "The URL of the window"),
    )
    @click.option(
        "--width",
        type=int,
        default=None,
        help=i18n("cli.init.window.help.width", "The width of the window"),
    )
    @click.option(
        "--height",
        type=int,
        default=None,
        help=i18n("cli.init.window.help.height", "The height of the window"),
    )
    @click.option(
        "--min-width",
        type=int,
        default=None,
        help=i18n("cli.init.window.help.min-width", "The minimum width of the window"),
    )
    @click.option(
        "--min-height",
        type=int,
        default=None,
        help=i18n("cli.init.window.help.min-height", "The minimum height of the window"),
    )
    @click.option(
        "--max-width",
        type=int,
        default=None,
        help=i18n("cli.init.window.help.max-width", "The maximum width of the window"),
    )
    @click.option(
        "--max-height",
        type=int,
        default=None,
        help=i18n("cli.init.window.help.max-height", "The maximum height of the window"),
    )
    @click.option(
        "--always-on-top",
        type=bool,
        default=None,
        help=i18n(
            "cli.init.window.help.always-on-top",
            "Whether the window should always be on top",
        ),
    )
    @click.option(
        "--frame",
        type=bool,
        default=None,
        help=i18n("cli.init.window.help.frame", "Whether the window should have a frame"),
    )
    @click.option(
        "--fullscreenable",
        type=bool,
        default=None,
        help=i18n(
            "cli.init.window.help.fullscreenable", "Whether the window can be fullscreened"
        ),
    )
    @click.option(
        "--maximizable",
        type=bool,
        default=None,
        help=i18n("cli.init.window.help.maximizable", "Whether the window can be maximized"),
    )
    @click.option(
        "--minimizable",
        type=bool,
        default=None,
        help=i18n("cli.init.window.help.minimizable", "Whether the window can be minimized"),
    )
    @click.option(
        "--resizable",
        type=bool,
        default=None,
        help=i18n("cli.init.window.help.resizable", "Whether the window can be resized"),
    )
    @click.option(
        "--background-color",
        type=str,
        default=None,
        help=i18n(
            "cli.init.window.help.background-color", "The background color of the window"
        ),
    )
    @click.option(
        "--multiple",
        type=bool,
        default=None,
        help=i18n("cli.init.window.help.multiple", "Whether multiple windows can be opened"),
    )
    @click.option(
        "--run-after-install",
        type=bool,
        default=None,
        help=i18n(
            "cli.init.window.help.run-after-install", "Whether to run after installation"
        ),
    )
    @click.option(
        "--devtools",
        type=bool,
        default=True,
        help=i18n("cli.init.window.help.devtools", "Whether to use devtools"),
    )
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    return wrapper


@init.command("window", help=i18n("cli.init.window.help", "Add a window to the plugin"))
@_window_options
@click.pass_obj
def window(obj, **kwargs):

    manifest_maker.add_window(
        obj["manifest"],
        url=kwargs.get("url"),
        width=kwargs.get("width"),
        height=kwargs.get("height"),
        minWidth=kwargs.get("min-width"),
        minHeight=kwargs.get("min-height"),
        maxWidth=kwargs.get("max-width"),
        maxHeight=kwargs.get("max-height"),
        alwaysOnTop=kwargs.get("always-on-top"),
        frame=kwargs.get("frame"),
        fullscreenable=kwargs.get("fullscreenable"),
        maximizable=kwargs.get("maximizable"),
        minimizable=kwargs.get("minimizable"),
        resizable=kwargs.get("resizable"),
        backgroundColor=kwargs.get("background-color"),
        multiple=kwargs.get("multiple"),
        runAfterInstall=kwargs.get("run-after-install"),
        devtools=kwargs.get("devtools", True),
    )


    with open("manifest.json", "w", encoding="utf-8") as f:
        json.dump(obj["manifest"], f, indent=4, ensure_ascii=False)


@init.command(
    "service", help=i18n("cli.service.help", "Add a background service to the plugin")
)
@_window_options
@click.pass_obj
def service(obj, **kwargs):

    manifest_maker.add_background_service(
        obj["manifest"],
        url=kwargs.get("url"),
        width=kwargs.get("width"),
        height=kwargs.get("height"),
        minWidth=kwargs.get("min-width"),
        minHeight=kwargs.get("min-height"),
        maxWidth=kwargs.get("max-width"),
        maxHeight=kwargs.get("max-height"),
        alwaysOnTop=kwargs.get("always-on-top"),
        frame=kwargs.get("frame"),
        fullscreenable=kwargs.get("fullscreenable"),
        maximizable=kwargs.get("maximizable"),
        minimizable=kwargs.get("minimizable"),
        resizable=kwargs.get("resizable"),
        backgroundColor=kwargs.get("background-color"),
        multiple=kwargs.get("multiple"),
        runAfterInstall=kwargs.get("run-after-install"),
        devtools=kwargs.get("devtools", True),
    )


    with open("manifest.json", "w", encoding="utf-8") as f:
        json.dump(obj["manifest"], f, indent=4, ensure_ascii=False)


@init.command(
    "inspector", help=i18n("cli.inspector.help", "Add a inspector to the plugin")
)
@click.option("--types", type=str, help=i18n("cli.inspector.help.types", "The types of the inspector"))
@click.pass_obj
def inspector(obj):

    with open("manifest.json", "w", encoding="utf-8") as f:
        json.dump(obj["manifest"], f, indent=4, ensure_ascii=False)


@cli.command("walk", help=i18n("cli.walk.help", "interactively walk through plugin init process"))
@click.option(
    "-smd",
    "--skip-manifest-details",
    is_flag=True,
    help=i18n("cli.walk.help.skip-manifest-details", "Skip the manifest details step"),
)

@click.option("-sl", "--skip-locales", is_flag=True, help=i18n("cli.walk.help.skip-locales", "Skip the locales step"))
def walk(skip_manifest_details, skip_locales):
    click.echo(i18n("walk.welcome", "Welcome to the plugin init process"))

    if os.path.exists("manifest.json"):
        return click.echo(i18n("walk.manifest_exists", "Manifest already exists, aborting"), err=True)

    name = click.prompt(i18n("walk.name", "What is the name of the plugin?"), type=str)

    if not skip_manifest_details and click.confirm(i18n("walk.id", "specify an ID?")):
        id = click.prompt(i18n("walk.id.prompt", "What is the ID of the plugin?"), type=str)
    else:
        id = str(uuid.uuid4())


    if not skip_manifest_details and click.confirm(
        i18n("walk.version", "specify a version (or v1.0.0)?")
    ):
        version = click.prompt(
            i18n("walk.version.prompt", "What is the version of the plugin?"), type=str
        )
    else:
        version = "1.0.0"

    if not skip_manifest_details and click.confirm(
        i18n("walk.platform", "specify a platform (or all)?")
    ):
        platform = click.prompt(
            i18n("walk.platform.prompt", "What is the platform of the plugin?"), type=str
        )
    else:

        platform = "all"

    if not skip_manifest_details and click.confirm(
        i18n("walk.arch", "specify an architecture (or all)?")
    ):
        arch = click.prompt(
            i18n("walk.arch.prompt", "What is the architecture of the plugin?"), type=str
        )
    else:
        arch = "all"

    if not skip_manifest_details and click.confirm(
        i18n("walk.logo", "specify a logo (or /logo.png)?")
    ):
        logo = click.prompt(
            i18n("walk.logo.prompt", "What is the logo of the plugin?"), type=str
        )
    else:
        logo = "/logo.png"

    if not skip_manifest_details and click.confirm(
        i18n("walk.keywords", "specify keywords (or [])?")
    ):
        keywords = click.prompt(
            i18n("walk.keywords.prompt", "What are the keywords of the plugin?"), type=str
        )
    else:
        keywords = []

    manifest = manifest_maker.manifest(
        plugin_id=id,
        version=version,
        platform=platform,
        arch=arch,
        name=name,
        logo=logo,
        keywords=keywords,
    )

    if not skip_locales:
        locales = click.confirm(i18n("walk.locales_support", "Do you want to support i8n?"))
        if locales:
            locales_default = click.prompt(
                i18n("walk.locales_default", "default language (or en)?"),
                type=str,
                default="en",
            )
            locales_set = click.prompt(
                i18n(
                    "walk.locales_set",
                    "support full set or lite set (en, zh_CN, zh_TW, ja_JP)?",
                ),
                type=click.Choice(["full", "lite", "custom"]),
                default="lite",
            )
            if locales_set == "full":
                locales_set = FULL_SET_OF_LOCALES
            elif locales_set == "lite":
                locales_set = LITE_SET_OF_LOCALES
            else:
                locales_set = click.prompt(
                    i18n(
                        "walk.locales_set",
                        "specify the locales (en, zh_CN, zh_TW, ja_JP)?",
                    ),
                    type=str,
                )
                locales_set = [x.strip() for x in locales_set.split(",")]

            locales_maker.setup_locales(manifest, locales_default, locales_set)
        
        with open("manifest.json", "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=4, ensure_ascii=False)

