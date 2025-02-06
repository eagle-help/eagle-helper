from typing import TypedDict
import typing
import uuid

_manifest = {
    "id": "{plugin_id}",
    "version": "{version}",
    "platform": "{platform}",
    "arch": "{arch}",
    "name": "{name}",
    "logo": "{logo}",
    "keywords": "{keywords}",
    "devTools": True,
}


def manifest(
    plugin_id: str | None = None,
    version: str | None = None,
    platform: str | None = None,
    arch: str | None = None,
    name: str | None = None,
    logo: str | None = None,
    keywords: list | None = None,
):
    src = _manifest.copy()

    assert name, "name is required"
    # id
    if plugin_id is None:
        plugin_id = str(uuid.uuid4())

    # version
    if version is None:
        version = "1.0.0"

    # platform
    if platform is None:
        platform = "all"

    # arch
    if arch is None:
        arch = "all"

    # keywords
    assert keywords is None or isinstance(keywords, list), "keywords must be a list"

    # logo
    if logo is None:
        logo = "/logo.png"

    keywords = keywords or []

    src["id"] = plugin_id
    src["version"] = version
    src["platform"] = platform
    src["arch"] = arch
    src["name"] = name
    src["logo"] = logo
    src["keywords"] = keywords

    return src


class _WindowFields(TypedDict):
    url: str
    width: int | None
    height: int | None
    minWidth: int | None
    minHeight: int | None
    maxWidth: int | None
    maxHeight: int | None
    alwaysOnTop: bool | None
    frame: bool | None
    fullscreenable: bool | None
    maximizable: bool | None
    minimizable: bool | None
    resizable: bool | None
    backgroundColor: str | None
    multiple: bool | None
    runAfterInstall: bool | None
    devtools: bool

    @staticmethod
    def parseWindowFields(**kwargs):
        data = {}
        url = kwargs.pop("url")
        width = kwargs.pop("width", None)
        height = kwargs.pop("height", None)
        minWidth = kwargs.pop("minWidth", None)
        minHeight = kwargs.pop("minHeight", None)
        maxWidth = kwargs.pop("maxWidth", None)
        maxHeight = kwargs.pop("maxHeight", None)

        devtools = kwargs.pop("devtools", True)

        data["url"] = url

        if width is not None and height is not None:
            data["width"] = width
            data["height"] = height

        if minWidth is not None and minHeight is not None:
            data["minWidth"] = minWidth
            data["minHeight"] = minHeight

        if maxWidth is not None and maxHeight is not None:
            data["maxWidth"] = maxWidth
            data["maxHeight"] = maxHeight

        fields = [
            "alwaysOnTop",
            "frame",
            "fullscreenable",
            "maximizable",
            "minimizable",
            "resizable",
            "backgroundColor",
            "multiple",
            "runAfterInstall",
        ]
        for field in fields:
            if kwargs.get(field) is not None:
                data[field] = kwargs[field]

        data["devtools"] = devtools

        return data


def add_window(manifest: dict, **kwargs: typing.Unpack[_WindowFields]):
    if "main" in manifest:
        raise ValueError("main already exists")

    manifest["main"] = _WindowFields.parseWindowFields(**kwargs)

    return manifest


def add_background_service(manifest: dict, **kwargs: typing.Unpack[_WindowFields]):
    res = add_window(manifest, **kwargs)
    res["main"]["serviceMode"] = True

    return res


def add_format(
    manifest: dict,
    view_path: str,
    types: typing.Union[str, list[str]],
    thumbnail_path: str = None,
    thumbnail_size: int = 400,
    thumbnail_allow_zoom: bool = True,
):
    if "preview" not in manifest:
        manifest["preview"] = {}

    if isinstance(types, list):
        types = ",".join(types)

    if types not in manifest["preview"]:
        manifest["preview"][types] = {}

    if "viewer" in manifest["preview"][types]:
        raise ValueError(f"viewer for {types} already exists")

    manifest["preview"][types] = {}

    if thumbnail_path is not None:
        manifest["preview"][types]["thumbnail"] = {
            "path": thumbnail_path,
            "size": thumbnail_size,
            "allowZoom": thumbnail_allow_zoom,
        }

    manifest["preview"][types]["viewer"] = view_path

    return manifest


def add_inspector(
    manifest: dict,
    types: typing.Union[str, list[str]],
    path: str,
    height: int = 400,
    multiSelect: bool = False,
):
    types = ",".join(types) if isinstance(types, list) else types

    if "preview" not in manifest:
        manifest["preview"] = {}

    if types not in manifest["preview"]:
        manifest["preview"][types] = {}

    if "inspector" in manifest["preview"][types]:
        raise ValueError(f"inspector for {types} already exists")

    manifest["preview"][types]["inspector"] = {
        "path": path,
        "height": height,
        "multiSelect": multiSelect,
    }

    return manifest
