import os
import shutil

MOD_PATH = os.path.dirname(os.path.realpath(__file__))

LOCALES_DIR = os.path.join(MOD_PATH, "files", "i18n")

GIT_IS_INSTALLED = shutil.which("git") is not None

ABLE_TO_TRANSLATE = None

HOME_DIR = os.path.abspath(os.path.join(os.path.expanduser("~"), ".eagle_helper"))

__version__ = "1.0.0"

def _init_translate_check():
    global ABLE_TO_TRANSLATE
    import eagle_helper.config as _config
    if hasattr(_config, "able_to_translate") and _config.able_to_translate():
        ABLE_TO_TRANSLATE = True
    else:
        ABLE_TO_TRANSLATE = False

