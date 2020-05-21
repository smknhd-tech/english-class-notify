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


def main(day, max_lessons=20, config_file="config.txt"):
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
    date_re = re.compile(fr"[0-9]{{2}}:[0-9]{{2}}")

    # 任意のリスト
    FAVORITE_TEACHER_ID_MAP1 = {
        "29618": "Kylle",
        "36569": "Jena",
        "31562": "Zsei",
        # "37260": "test",
    }
    FAVORITE_TEACHER_ID_MAP2 = {
        "25336": "Louelle",
        "35071": "Tamara",
        "36755": "Alina",
        "36846": "Allie",
        "36775": "Celine",
    }

    FAVORITE_TEACHER_ID_MAPS = [FAVORITE_TEACHER_ID_MAP1, FAVORITE_TEACHER_ID_MAP2]

    USERS = ["KAZY", "YUKKY"]
    for id_map, user in zip(FAVORITE_TEACHER_ID_MAPS, USERS):
        messege = ""
        for id, name in id_map.items():
            # logger.info(f"name:{name}")
            res = requests.get(f"{BASE_URL}{id}")
            yoyakuka = re.compile(fr"{date}.*?予約可</a>")
            yoyakuka_lessons = yoyakuka.findall(res.text)

            if not yoyakuka_lessons:
                continue

            lessons = ", ".join(
                [
                    f"{date_re.search(lesson).group()}"
                    for lesson in yoyakuka_lessons[:max_lessons]
                    if date_re.search(lesson)
                ]
            )
            messege += f"\n{BASE_URL}{id} \n{lessons}\n"

        if messege:
            PythonNotify(f"@{user}" + messege + day.upper(), TOKEN)


if __name__ == "__main__":
    import sys

    args = sys.argv
    if len(args) >= 3:
        main(args[1], config_file=args[2])
    else:
        main(args[1])
