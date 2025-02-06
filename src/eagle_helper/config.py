LOCALES_DIR = "_locales"


def able_to_translate():
    try:
        import requests
    except ImportError:
        return False

    try:
        res = requests.get("http://localhost:1234/v1/models", timeout=0.4)
        if res.status_code == 200:
            return True

    except Exception:
        print("Error checking if DeepSeek is running")
        return False


def help_me_translate(text: str, target_language: str, src_language: str = "en") -> str:

    import requests
    import json

    magic = """
    Translate the following text from {src_language} to {target_language} accurately
    {text}
    """

    bg = """
    you are a professional language translator
    you are given a text and you need to translate it to the target language
    the first line of the request will include the language code of source and target language
    you need to translate the text accurately
    do not add any other text or comments
    do not repeat the original text
    only return the translated text without any input including the language code
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
        "temperature": 0.7,
        "max_tokens": 5000,
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
    "repo_url" : "https://github.com/eagle-help/eagle-utils.git",
    "repo_name" : "eagle-utils",
    "branch" : "release"
}

