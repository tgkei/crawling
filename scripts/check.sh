#!/bin/bash

set -e

# 지금 virtual environment 에 있는지 확인
if [ -z "$VIRTUAL_ENV" ]; then

    # pipenv 설치되어 있는지 확인
    if ! [ -x "$(command -v pipenv)" ]; then
        echo "'pipenv' is not installed." >&2
        echo "https://pipenv.readthedocs.io/en/latest/#install-pipenv-today" >&2
        exit 1
    fi

    PIPENV="pipenv run"
else
    PIPENV=""
fi

echo "[1/4] ✨  Running black"
$PIPENV black --check insta.py 

echo "[2/4] 🔍  Running pylint"
$PIPENV pylint -f colorized --ignore migrations,tests ai_api image_loader core base lms grpc_server

echo "[3/4] 💭  Running mypy"
$PIPENV mypy ml --ignore-missing-imports --check-untyped-defs

echo "[4/4] 🚀  Running pytest"
$PIPENV python manage.py test -v 2 --force-color
$PIPENV py.test -v --color=yes --disable-warnings test|
