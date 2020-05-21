import re
import requests
import configparser
from logzero import logger
from datetime import datetime, date, timedelta


def PythonNotify(message, token, img_path=""):
    # 諸々の設定
    line_notify_api = "https://notify-api.line.me/api/notify"
    line_notify_token = token
    headers = {"Authorization": "Bearer " + line_notify_token}
    # メッセージ
    payload = {"message": message}
    # 画像を含むか否か
    if img_path == "":
        requests.post(line_notify_api, data=payload, headers=headers)
    else:
        # 画像
        files = {"imageFile": open(img_path, "rb")}
        requests.post(line_notify_api, data=payload, headers=headers, files=files)


def main(day, config_file="config.txt"):
    config = configparser.ConfigParser()
    config.read(config_file)
    TOKEN = config["DEFAULT"]["LINE_NOTIFY_TOKEN"]
    BASE_URL = config["DEFAULT"]["BASE_URL"]

    if day == "" or day == "today":
        days = 0
    elif day == "tomorrow":
        days = 1
    else:
        days = int(day)
    date = datetime.today() + timedelta(days=days)
    date = datetime.strftime(date, "%Y-%m-%d")
    print(f"search date: {date}")
    date = re.compile(fr"{date} [0-9]{{1,2}}:[0-9]{{1,2}}")
    # 任意のリスト
    FAVORITE_TEACHER_ID_MAP = {
        "29618": "Kylle",
        "36569": "Jena",
        "31562": "Zsei",
        "37181": "Kye",
    }
    messege = ""
    for id, name in FAVORITE_TEACHER_ID_MAP.items():
        # logger.info(f"name:{name}")
        res = requests.get(f"{BASE_URL}{id}")
        yoyakuka = re.compile(rf"<a href.*?.*?予約可</a>")
        yoyakuka_lessons = yoyakuka.findall(res.text)

        print(yoyakuka_lessons)
        if not yoyakuka_lessons:
            resp = re.findall(r".{500}予約可</a>.{10}", res.text)
            continue

        lessons = "\n".join(
            [
                f"{date.search(lesson).group()} {BASE_URL}{id}"
                if date.search(lesson)
                else ""
                for lesson in yoyakuka_lessons
            ]
        )
        messege += f"\n*Found {name} lessons!*\n{lessons}\n"

    if messege:
        PythonNotify(messege)


if __name__ == "__main__":
    import sys

    args = sys.argv
    if len(args) >= 3:
        main(args[1], args[2])
    else:
        main(args[1])
