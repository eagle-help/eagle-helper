import os
import shutil

MOD_PATH = os.path.dirname(os.path.realpath(__file__))

LOCALES_DIR = os.path.join(MOD_PATH, "i18n")

GIT_IS_INSTALLED = shutil.which("git") is not None


HOME_DIR = os.path.abspath(os.path.join(os.path.expanduser("~"), ".eagle_helper"))

__version__ = "1.0.0"

can_translate = None


def _init_translate_check():

    global can_translate
    import eagle_helper.config as _config

    if hasattr(_config, "can_translate") and _config.can_translate():
        can_translate = True
    else:
        can_translate = False
