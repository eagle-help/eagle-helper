LOCALES_DIR = "_locales"


def can_translate():
    try:
        import requests
    except ImportError:
        return False

    try:
        res = requests.get("http://localhost:1234/v1/models", timeout=0.4)
        if res.status_code == 200:
            return True

    except Exception:
        print("In order to use this default translation service")
        print(
            "You need to install LM Studio with following model deepseek-r1-distill-qwen-7b"
        )
        return False


def help_me_translate(text: str, target_language: str, src_language: str = "en") -> str:

    import requests
    import json

    magic = """
    func(
        src = {src_language},
        target = {target_language},
        text = {text}
    )
    """

    bg = """

    emulate a translator function,
    where you take in an input and output the result, with nothing else
    the format is like this:
    func(src, target, text)
    src is the source language code
    target is the target language code
    text is the text to translate
    you need to translate the text from src to target
    do not repeat the original text and do not reply that you understands
    output the result without any explanation and comments
    """

    url = "http://localhost:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}

    data = {
        "model": "deepseek-r1-distill-qwen-7b",
        "messages": [
            {"role": "system", "content": bg},
            {
                "role": "user",
                "content": magic.format(
                    src_language=src_language,
                    target_language=target_language,
                    text=text,
                ),
            },
        ],
        "temperature": 0.3,
        "max_tokens": 1000,
        "stream": False,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        res = response.json()["choices"][0]["message"]["content"]
        return res.split("</think>")[1].strip()
    else:
        raise Exception(f"Translation failed with status code {response.status_code}")


FULL_SET_OF_LOCALES = [
    "ja_JP",
    "ko_KR",
    "ru_RU",
    "zh_CN",
    "zh_TW",
    "de_DE",
    "en",
    "es_ES",
]
LITE_SET_OF_LOCALES = ["en", "zh_CN", "zh_TW", "ja_JP"]

UTILS_REPO = {
    "repo_url": "https://github.com/eagle-help/eagle-utils.git",
    "repo_name": "eagle-utils",
    "branch": "release",
}

TEMPLATE_REPO = {
    "repo_url": "https://github.com/eagle-help/eagle-plugin-template.git",
    "repo_name": "eagle-plugin-template",
}
