import re
import requests
import configparser
from logzero import logger
from datetime import datetime, date, timedelta


def post_line_notify(message, token, img_path=None):
    line_notify_api = "https://notify-api.line.me/api/notify"
    line_notify_token = token
    headers = {"Authorization": "Bearer " + line_notify_token}
    payload = {"message": message}
    # TODO: This is used to send the analized image.
    files = None if img_path is None else {"imageFile": open(img_path, "rb")}
    res = requests.post(line_notify_api, data=payload, headers=headers, files=files)
    return res


# Because display more than 20 lessons is too much
def main(day, max_lessons=20, config_file="conf/config.txt"):
    config = configparser.ConfigParser()
    config.read(config_file)
    TUTORS_URL = config["SITE INFO"]["URL"]
    TOKEN = config["LINE NOTIFY"]["TOKEN"]
    SUBMIT_MESSAGE = config["LINE NOTIFY"]["SUBMIT_MESSAGE"]
    USER_NAME = config["USER INFO"]["NAME"]
    TUTORS_NAME_ID_MAP = config["TUTORS"]
    CONTENT_REC_PATH = f"/tmp/app/db/instead-db-tmp-for-{USER_NAME}.txt"
    # The reason for the numerical conversion is to use timedelta to calculate the date
    # Because Using "today" "tomorrow" as argument is more understandable than 0,1
    if day == "" or day == "today":
        days = 0
    elif day == "tomorrow":
        days = 1
    else:
        days = int(day)
    # date is set the number of days from today
    date = datetime.today() + timedelta(days=days)
    date = datetime.strftime(date, "%Y-%m-%d")
    logger.info("Search date: %s", date)
    # to extract lesson time
    time_re = re.compile(fr"[0-9]{{2}}:[0-9]{{2}}")
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
        # Date and word "予約可" are the conditions for reservation is possible
        yoyakuka = re.compile(fr"{date}.*?予約可</a>")
        yoyakuka_lessons = yoyakuka.findall(res.text)

        if not yoyakuka_lessons:
            continue

        lessons = ", ".join(
            [
                f"{time_re.search(lesson).group()}"
                for lesson in yoyakuka_lessons[:max_lessons]
                if time_re.search(lesson)
            ]
        )
        message += f"\n{TUTORS_URL}{id} \n{lessons} \n"
    if message == "":
        message += "\n予約可能枠なし\n"
    message += f"{SUBMIT_MESSAGE}\n"
    logger.info("今回のメッセージ:%s", message)
    if message != file_content:
        with open(CONTENT_REC_PATH, mode="w") as fw:
            fw.write(message)
        # the upper case "TODAY","TOMORROW" looks better than the lower case "today", "tomorrow"
        res = post_line_notify(f"@{USER_NAME}" + message + day.upper(), TOKEN)
        # The HTTP response status code will be good a log to fix problem
        logger.info("LINE通知:%s", res)


if __name__ == "__main__":
    import sys

    args = sys.argv
    if len(args) >= 3:
        main(args[1], config_file="conf/" + args[2])
    else:
        main(args[1])
