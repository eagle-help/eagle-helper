import os
from functools import cache
from eagle_helper import LOCALES_DIR
import json


def get_sys_language_code():

    import locale

    res = locale.getdefaultlocale()[0]
    if res.startswith("en"):
        return "en"

    return res


LANGUAGE_MODE = get_sys_language_code()


@cache
def load_i18n_file(lang: str):
    if not os.path.exists(os.path.join(LOCALES_DIR, f"{lang}.json")):
        return None

    with open(os.path.join(LOCALES_DIR, f"{lang}.json"), "r", encoding="utf-8") as f:
        return json.load(f)


I18N_CACHE = {}


def i18n(key: str, fallback: str = None):
    if key in I18N_CACHE:
        return I18N_CACHE[key]

    if LANGUAGE_MODE == "en" and fallback is not None:
        I18N_CACHE[key] = fallback
        return fallback

    data = load_i18n_file(LANGUAGE_MODE)
    if data is None:
        I18N_CACHE[key] = fallback
        return fallback

    I18N_CACHE[key] = data.get(key, fallback)
    return I18N_CACHE[key]
