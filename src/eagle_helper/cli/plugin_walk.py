import os
import random
import uuid
import click
import json
from ..coms.files import setup_artifact_html, setup_template_files, setup_utils
import eagle_helper.coms.manifest as manifest_maker
import eagle_helper.coms.locales as locales_maker
from ..etc import i18n
from ..config import FULL_SET_OF_LOCALES, LITE_SET_OF_LOCALES


@click.command(
    "walk", help=i18n("cli.walk.help", "interactively walk through plugin init process")
)
@click.option(
    "-smd",
    "--skip-manifest-details",
    is_flag=True,
    help=i18n("cli.walk.help.skip-manifest-details", "Skip the manifest details step"),
)
@click.option(
    "-sl",
    "--skip-locales",
    is_flag=True,
    help=i18n("cli.walk.help.skip-locales", "Skip the locales step"),
)
@click.option(
    "-sw",
    "--skip-window",
    is_flag=True,
    help=i18n("cli.walk.help.skip-window", "Skip the window step"),
)
@click.option(
    "-sf",
    "--skip-format",
    is_flag=True,
    help=i18n("cli.walk.help.skip-format", "Skip the format step"),
)
def walk(skip_manifest_details, skip_locales, skip_window, skip_format):
    click.echo(i18n("walk.welcome", "Welcome to the plugin init process"))


    if os.path.exists("manifest.json"):
        return click.echo(
            i18n("walk.manifest_exists", "Manifest already exists, aborting"), err=True
        )

    name = click.prompt(i18n("walk.name", "What is the name of the plugin?"), type=str)

    if not skip_manifest_details and click.confirm(i18n("walk.id", "specify an ID?")):
        id = click.prompt(
            i18n("walk.id.prompt", "What is the ID of the plugin?"), type=str
        )
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
            i18n("walk.platform.prompt", "What is the platform of the plugin?"),
            type=str,
        )
    else:

        platform = "all"

    if not skip_manifest_details and click.confirm(
        i18n("walk.arch", "specify an architecture (or all)?")
    ):
        arch = click.prompt(
            i18n("walk.arch.prompt", "What is the architecture of the plugin?"),
            type=str,
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
            i18n("walk.keywords.prompt", "What are the keywords of the plugin?"),
            type=str,
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
        locales = click.confirm(
            i18n("walk.locales_support", "Do you want to support i8n?")
        )
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

    setup_template_files()

    # want to setup utils?
    if click.confirm(i18n("walk.utils", "Do you want to setup utils?")):
        setup_utils()

    # want to setup window?
    if not skip_window and click.confirm(i18n("walk.window", "Do you want to setup window?")):
        # type service/window?

        window_type = click.prompt(
            i18n("walk.window.type", "What is the type of the window?"),
            type=click.Choice(["service", "window"]),
            default="window",
        )
        if window_type == "service":
            manifest_maker.add_background_service(
                manifest,
                url="src/service.html",
            )
            setup_artifact_html("src/service.html")

        else:
            manifest_maker.add_window(manifest)
            setup_artifact_html("src/window.html")

    # want to setup inspector/format?
    if not skip_format and click.confirm(i18n("walk.format", "Do you want to setup inspector/format?")):
        while True:
            setup_format(manifest)
            if not click.confirm(i18n("walk.format.add", "Do you want to add another format?")):
                break

    click.echo(i18n("walk.done", "Done!"))

def setup_format(manifest: dict):
    # get eligible format types
    while True:
        try:
            format_types = click.prompt(
                i18n("walk.format.types", "What are the types of the format?"),
                type=str,
            )
            format_types = [x.strip() for x in format_types.split(",")]
            break
        except Exception:
            click.echo(i18n("walk.format.types.error", "Invalid format types"), err=True)

    
    shorthand = "".join([x[0] for x in format_types])
    longshort = str(format_types[0]) + "".join([x[0] for x in format_types[1:]])

    if not any(f"_{shorthand}.html" in x for x in os.listdir("src")):
        name = longshort
    elif not any(f"_{longshort}.html" in x for x in os.listdir("src")):
        name = longshort
    else:
        name = str(random.randint(10, 100))

    # add format
    confirm = click.confirm(i18n("walk.format.add", "Do you want to add a format?"))
    if confirm:
        manifest_maker.add_format(
            manifest,
            view_path=f"src/format_{name}.html",
            types=format_types,
        )

        setup_artifact_html(f"src/format_{name}.html")
    # add inspector
    confirm = click.confirm(i18n("walk.inspector.add", "Do you want to add an inspector?"))
    if confirm:
        manifest_maker.add_inspector(
            manifest,
            path=f"src/inspector_{name}.html",
            types=format_types,
        )

        setup_artifact_html(f"src/inspector_{name}.html")

