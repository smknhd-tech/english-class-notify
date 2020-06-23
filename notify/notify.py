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
        res = requests.post(line_notify_api, data=payload, headers=headers)
    else:
        # 画像
        files = {"imageFile": open(img_path, "rb")}
        res = requests.post(line_notify_api, data=payload, headers=headers, files=files)
    return res


# 最大表示数を20としたのは20以上のクラスが表示されると通知が長くなりすぎると思ったため
def main(day, max_lessons=20, config_file="conf/config.txt"):
    config = configparser.ConfigParser()
    config.read(config_file)
    TUTORS_URL = config["SITE INFO"]["URL"]
    TOKEN = config["LINE NOTIFY"]["TOKEN"]
    SUBMIT_MESSAGE = config["LINE NOTIFY"]["SUBMIT_MESSAGE"]
    USER_NAME = config["USER INFO"]["NAME"]
    TUTORS_NAME_ID_MAP = config["TUTORS"]
    CONTENT_REC_PATH = f"/tmp/app/db/instead-db-tmp-for-{USER_NAME}.txt"
    # today tomorrw といった引数を許容させたのは今日から何日後という意味で数字を引数をすると使いにくと考えたため
    # 数値変換しているのはtimedeltaを用いて日付の演算を行うため
    if day == "" or day == "today":
        days = 0
    elif day == "tomorrow":
        days = 1
    else:
        days = int(day)
    # 過去は予約不可能であるため 今日から何日後 を指定させるのが使い勝手が良いかなと思ったため
    date = datetime.today() + timedelta(days=days)
    date = datetime.strftime(date, "%Y-%m-%d")
    logger.info("Search date: %s", date)
    date_re = re.compile(fr"[0-9]{{2}}:[0-9]{{2}}")
    message = ""
    try:
        with open(CONTENT_REC_PATH, mode="x") as f:
            f.write("")
            file_content = ""
    except FileExistsError:
        with open(CONTENT_REC_PATH) as fr:
            file_content = fr.read()
    logger.info("前回のメッセージ: %s", file_content)
    for name, id in TUTORS_NAME_ID_MAP.items():
        res = requests.get(f"{TUTORS_URL}{id}")
        # 予約ページへのリンクを予約可能の判定条件としているため
        # パターンに日付を加えているのは対象としている日のみを抽出するため
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
        message += f"\n{TUTORS_URL}{id} \n{lessons} \n"
    message += f"{SUBMIT_MESSAGE}\n"
    logger.info("今回のメッセージ:%s", message)
    if message != file_content:
        with open(CONTENT_REC_PATH, mode="w") as fw:
            fw.write(message)
        # 大文字変換はtoday tomorrowよりTODAY TOMORROWのほうが見やすいかなと思ったため
        res = PythonNotify(f"@{USER_NAME}" + message + day.upper(), TOKEN)
        # HTTP レスポンスステータスコードをログとして残しておくと障害対応が行いやすくなるため
        logger.info("LINE通知:%s", res)


if __name__ == "__main__":
    import sys

    args = sys.argv
    if len(args) >= 3:
        main(args[1], config_file="conf/" + args[2])
    else:
        main(args[1])
