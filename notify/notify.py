import re
import requests
import configparser
from logzero import logger
from datetime import datetime, date, timedelta


def PythonNotify(message, token, img_path=""):
    line_notify_api = "https://notify-api.line.me/api/notify"
    line_notify_token = token
    headers = {"Authorization": "Bearer " + line_notify_token}
    payload = {"message": message}
    # Whether the image is included or not
    if img_path == "":
        res = requests.post(line_notify_api, data=payload, headers=headers)
    else:
        # image
        files = {"imageFile": open(img_path, "rb")}
        res = requests.post(line_notify_api, data=payload, headers=headers, files=files)
    return res


# The reason why I set the maximum number of displays to 20 is because I thought the notification would be too long if more than 20 classes were displayed.
def main(day, max_lessons=20, config_file="conf/config.txt"):
    config = configparser.ConfigParser()
    config.read(config_file)
    TUTORS_URL = config["SITE INFO"]["URL"]
    TOKEN = config["LINE NOTIFY"]["TOKEN"]
    SUBMIT_MESSAGE = config["LINE NOTIFY"]["SUBMIT_MESSAGE"]
    USER_NAME = config["USER INFO"]["NAME"]
    TUTORS_NAME_ID_MAP = config["TUTORS"]
    CONTENT_REC_PATH = f"/tmp/app/db/instead-db-tmp-for-{USER_NAME}.txt"
    # The reason we allow arguments like today tomorrw is that we thought it would be difficult to use a number as an argument to say how many days from today.
    # The reason for the numerical conversion is to use timedelta to calculate the date
    if day == "" or day == "today":
        days = 0
    elif day == "tomorrow":
        days = 1
    else:
        days = int(day)
    # Since the past is unavailable, I thought it would be more convenient to specify the number of days from today
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
        # Because the link to the reservation page is a condition for determining whether a reservation is possible.
        # The date is added to the pattern in order to extract only the dates we are interested in.
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
        # I thought it would be easier to see the capitalization conversions in TODAY TOMORROW than in today tomorrow
        res = PythonNotify(f"@{USER_NAME}" + message + day.upper(), TOKEN)
        # The HTTP response status code is kept in a log to make it easier to respond to problems.
        logger.info("LINE通知:%s", res)


if __name__ == "__main__":
    import sys

    args = sys.argv
    if len(args) >= 3:
        main(args[1], config_file="conf/" + args[2])
    else:
        main(args[1])
