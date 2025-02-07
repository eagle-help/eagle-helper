import os
import typing

import click
import json
from ..config import LOCALES_DIR
import eagle_helper

_placeholder_dict = {"manifest": {"app": {"name": None}}}


def _assert_locales_name(plugin_name: str, lang: str):

    placeholder_dict = _placeholder_dict.copy()
    placeholder_dict["manifest"]["app"]["name"] = plugin_name

    if not os.path.exists(os.path.join(LOCALES_DIR, f"{lang}.json")):
        with open(
            os.path.join(LOCALES_DIR, f"{lang}.json"), "w", encoding="utf-8"
        ) as f:
            json.dump(placeholder_dict, f, indent=4, ensure_ascii=False)

    else:
        with open(
            os.path.join(LOCALES_DIR, f"{lang}.json"), "r", encoding="utf-8"
        ) as f:
            data = json.load(f)

            if data.get("manifest", {}).get("app", {}).get("name", None) is None:
                data.setdefault("manifest", {}).setdefault("app", {})
                data["manifest"]["app"]["name"] = plugin_name
                with open(
                    os.path.join(LOCALES_DIR, f"{lang}.json"), "w", encoding="utf-8"
                ) as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)


def setup_locales(
    manifest: dict,
    main_language: str = "en",
    languages: typing.List[str] = [
        "ja_JP",
        "ko_KR",
        "ru_RU",
        "zh_CN",
        "zh_TW",
        "de_DE",
        "en",
        "es_ES",
    ],
):
    plugin_name = manifest["name"]

    manifest["name"] = "{{manifest.app.name}}"
    with open("manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4, ensure_ascii=False)

    os.makedirs(LOCALES_DIR, exist_ok=True)

    _assert_locales_name(plugin_name, main_language)

    for language in languages:

        if language == main_language:
            continue

        if eagle_helper.can_translate:
            from ..config import help_me_translate

            try:
                click.echo(f"Translating plugin name to {language}...")
                result = help_me_translate(plugin_name, language)
            except Exception as e:
                print(f"Error translating plugin name: {e}")
                result = plugin_name
        else:
            result = plugin_name

        _assert_locales_name(result, language)
