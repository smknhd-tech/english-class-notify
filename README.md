# english-class-notify

`notify.py` checks tutor's scheduale and notify you via LINE Notify.

# VS.
- [dmm-eikaiwa-tsc](https://github.com/oinume/dmm-eikaiwa-tsc/)

# Requirement
- Python
- [poetry](https://cocoatomo.github.io/poetry-ja/)
- [pytest](https://pypi.org/project/pytest/)

# Usage

```
$ poetry run python notify.py [-d day] [-c configurationfile]
```

## Example
```
$ poetry run python notify.py today ../config.txt
```

## Via Docker 
```
$ docker build -t notifyimage:(tag) -f .docker/containers/app/Dockerfile .
$ docker run --rm \
--mount type=volume,src=english-class-notify-instead-db-tmp,dst=/tmp/app/db \
--mount type=bind,src="$(pwd)"/conf,dst=/tmp/app/conf \
notifyimage:(tag) today config.txt

$ docker-compose build
$ docker-compose up -d

$ make start
$ docker-compose run app today config.txt
```

## Test
### Via Docker
```
$ docker run --env LINE_NOTIFY_TOKEN_TEST=anylinenotifytoken --rm --entrypoint=pytest notifyimage:latest -v
```
### Via Terminal
```
$ export LINE_NOTIFY_TOKEN_TEST=anylinenotifytoken
$ pytest -v
```

# Config File Example

```
[SITE INFO]
URL = XXXXX

[LINE NOTIFY]
TOKEN = XXXXX
SUBMIT_MESSAGE = XXXXX

[USER INFO]
NAME=XXXX

[TUTORS]
# name id
tutor1 = 12345
tutor2 = 54321
```

# Tips
- `docker compose up -d` 後に、http://localhost にアクセスで、pgAdmin使用可能。
    - サーバへの接続情報は次。
        ```
        ホスト名/アドレス:db
        ポート番号:5432
        データベースの管理:postgres
        ユーザ名:root
        パスワード:root
        ```
- 
