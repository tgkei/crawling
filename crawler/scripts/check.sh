#!/bin/bash

set -e
echo '  ___ _   _ ____ _____  _'
echo ' |_ _| \ | / ___|_   _|/ \'
echo '  | ||  \| \___ \ | | / _ \'
echo '  | || |\  |___) || |/ ___ \'
echo ' |___|_| \_|____/ |_/_/   \_\'

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

echo "[1/2] ✨  Running black"
$PIPENV black --check insta.py 

echo "[2/2] 🔍  Running pylint"
$PIPENV pylint -f colorized insta.py 
