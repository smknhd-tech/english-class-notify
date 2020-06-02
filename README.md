# kazy-english-class-notify

`notify.py` checks tutor's scheduale and notify you via LINE Notify.

# VS.
- [dmm-eikaiwa-tsc](https://github.com/oinume/dmm-eikaiwa-tsc/)

# Requirement
- Python
- [poetry](https://cocoatomo.github.io/poetry-ja/)

# Usage

```
$ poetry run python notify.py [-d day] [-c configurationfile]
```

## Example
```
$ poetry run python notify.py today ../config.txt
```

# Config File Example

```
[DEFAULT]
LINE_NOTIFY_TOKEN = XXXXXXXXXXXXXXXX
TUTORS_URL = https://XXXXXXXXXXXXXXXXXXXX
```