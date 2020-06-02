FROM python:3.8

RUN apt update \
    curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python \
    source $HOME/.poetry/env \
    git clone https://github.com/KAZYPinkSaurus/kazy-english-class-notify.git \
    cd kazy-english-class-notify\
    poetry install \
    touch config.txt \