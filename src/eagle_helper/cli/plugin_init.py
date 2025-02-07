import click

from ..coms.files import setup_artifact_html, setup_template_files, setup_utils
from ..etc import i18n
from ..config import FULL_SET_OF_LOCALES, LITE_SET_OF_LOCALES
import inspect
import json
import eagle_helper.coms.manifest as manifest_maker
import eagle_helper.coms.locales as locales_maker


def _filter_kwargs(kwargs, func):
    sig = inspect.signature(func)

    kw = {k: v for k, v in kwargs.items() if k in sig.parameters}
    return func(**kw)


@click.group(
    "init",
    invoke_without_command=True,
    chain=True,
    help=i18n("cli.init.help", "Initialize a new plugin"),
)
@click.option(
    "--id",
    type=str,
    default=None,
    help=i18n("cli.init.help.id", "The id of the plugin"),
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
    required=True,
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
@click.option(
    "-nu","--no-utils",
    is_flag=True,
    help=i18n("cli.init.help.no_utils", "Whether not to setup the utils"),
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

    setup_template_files()

    if not kwargs.get("no_utils", False):
        setup_utils()

def _window_options(f):

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
        help=i18n(
            "cli.init.window.help.min-height", "The minimum height of the window"
        ),
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
        help=i18n(
            "cli.init.window.help.max-height", "The maximum height of the window"
        ),
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
        help=i18n(
            "cli.init.window.help.frame", "Whether the window should have a frame"
        ),
    )
    @click.option(
        "--fullscreenable",
        type=bool,
        default=None,
        help=i18n(
            "cli.init.window.help.fullscreenable",
            "Whether the window can be fullscreened",
        ),
    )
    @click.option(
        "--maximizable",
        type=bool,
        default=None,
        help=i18n(
            "cli.init.window.help.maximizable", "Whether the window can be maximized"
        ),
    )
    @click.option(
        "--minimizable",
        type=bool,
        default=None,
        help=i18n(
            "cli.init.window.help.minimizable", "Whether the window can be minimized"
        ),
    )
    @click.option(
        "--resizable",
        type=bool,
        default=None,
        help=i18n(
            "cli.init.window.help.resizable", "Whether the window can be resized"
        ),
    )
    @click.option(
        "--background-color",
        type=str,
        default=None,
        help=i18n(
            "cli.init.window.help.background-color",
            "The background color of the window",
        ),
    )
    @click.option(
        "--multiple",
        type=bool,
        default=None,
        help=i18n(
            "cli.init.window.help.multiple", "Whether multiple windows can be opened"
        ),
    )
    @click.option(
        "--run-after-install",
        type=bool,
        default=None,
        help=i18n(
            "cli.init.window.help.run-after-install",
            "Whether to run after installation",
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


@init.command(
    "add-window", help=i18n("cli.init.window.help", "Add a window to the plugin")
)
@click.option(
    "--url",
    default="src/window.html",
    type=str,
    help=i18n("cli.init.window.help.url", "The path of the window"),
)
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
    "add-service",
    help=i18n("cli.service.help", "Add a background service to the plugin"),
)
@click.option(
    "--url",
    default="src/service.html",
    type=str,
    help=i18n("cli.init.window.help.url", "The path of the window"),
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

    setup_artifact_html(kwargs.get("url"))

@init.command(
    "add-format", help=i18n("cli.format.help", "Add a format to the plugin")
)
@click.option(
    "--path",
    "--view-path",
    default="src/format.html",
    type=str,
    help=i18n("cli.init.window.help.url", "The path of the window"),
)
@click.option(
    "--types",
    type=str,
    help=i18n("cli.format.help.types", "The types of the format, comma separated"),
    required=True,
)
@click.option(
    "--thumbnail-path",
    type=str,
    help=i18n("cli.format.help.thumbnail-path", "The path of the thumbnail"),
)
@click.option(
    "--thumbnail-size",
    type=int,
    help=i18n("cli.format.help.thumbnail-size", "The size of the thumbnail"),
    default=400,
)
@click.option(
    "--thumbnail-allow-zoom",
    type=bool,
    help=i18n(
        "cli.format.help.thumbnail-allow-zoom",
        "Whether the thumbnail should allow zoom",
    ),
    default=True,
)
@click.pass_obj
def format(obj, **kwargs):
    manifest_maker.add_format(
        obj["manifest"],
        view_path=kwargs.get("path"),
        types=kwargs.get("types").split(","),
        thumbnail_path=kwargs.get("thumbnail-path", None),
        thumbnail_size=kwargs.get("thumbnail-size", None),
        thumbnail_allow_zoom=kwargs.get("thumbnail-allow-zoom", None),
    )

    with open("manifest.json", "w", encoding="utf-8") as f:
        json.dump(obj["manifest"], f, indent=4, ensure_ascii=False)

    setup_artifact_html(kwargs.get("path"))

    if kwargs.get("thumbnail-path", None) is not None:
        setup_artifact_html(kwargs.get("thumbnail-path"))


@init.command(
    "add-inspector", help=i18n("cli.inspector.help", "Add a inspector to the plugin")
)
@click.option(
    "--path",
    default="src/inspector.html",
    type=str,
    help=i18n("cli.init.window.help.url", "The path of the inspector"),
)
@click.option(
    "--height",
    type=int,
    help=i18n("cli.inspector.help.height", "The height of the inspector"),
    default=400,
)
@click.option(
    "--multi-select",
    type=bool,
    help=i18n("cli.inspector.help.multi-select", "Whether the inspector should allow multiple selection"),
    default=False,
)
@click.pass_obj
def inspector(obj, **kwargs):
    manifest_maker.add_inspector(
        obj["manifest"],
        path=kwargs.get("path"),
        height=kwargs.get("height"),
        multiSelect=kwargs.get("multi-select"),
    )

    with open("manifest.json", "w", encoding="utf-8") as f:
        json.dump(obj["manifest"], f, indent=4, ensure_ascii=False)

    setup_artifact_html(kwargs.get("path"))

