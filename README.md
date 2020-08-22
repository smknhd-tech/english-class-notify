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
```

## Test
```
$ pytest tests/test_notify.py -v
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