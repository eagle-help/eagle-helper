from functools import cache
import shutil
import os
import eagle_helper
import eagle_helper.config


def setup_template_files():
    shutil.copytree(
        os.path.join(
            eagle_helper.HOME_DIR, eagle_helper.config.TEMPLATE_REPO["repo_name"]
        ),
        os.getcwd(),
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns('.git', '.git/*')
    )

def setup_utils():
    shutil.copytree(
        os.path.join(
            eagle_helper.HOME_DIR, eagle_helper.config.UTILS_REPO["repo_name"]
        ),
        os.path.join(os.getcwd(), "utils"),
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns('.git', '.git/*')
    )


ARTIFACT_HTML_PATH = os.path.join(
    eagle_helper.HOME_DIR,
    eagle_helper.config.TEMPLATE_REPO["repo_name"],
    ".github",
    "artifacts",
    "app.html",
)


@cache
def ARTIFACT_HTML_CONTENT():
    with open(ARTIFACT_HTML_PATH, "r", encoding="utf-8") as f:
        return f.readlines()


def setup_artifact_html(path: str):
    if path.startswith("/"):
        path = path[1:]

    if os.path.exists(path):
        print(f"File {path} already exists, skipping...")
        return

    basename = os.path.splitext(os.path.basename(path))[0]

    pathpart = os.path.dirname(path)

    targetjsname = f"{basename}.js"
    targetjspath = os.path.join(pathpart, targetjsname)

    with open(targetjspath, "w", encoding="utf-8") as f:
        f.write("")

    lines = ARTIFACT_HTML_CONTENT().copy()
    lines[7] = f'\t<script src="{targetjsname}"></script>\n'

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
