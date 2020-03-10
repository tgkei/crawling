# crawling

```
  ____                    _ _
 / ___|_ __ __ ___      _| (_)_ __   __ _
| |   | '__/ _` \ \ /\ / / | | '_ \ / _` |
| |___| | | (_| |\ V  V /| | | | | | (_| |
 \____|_|  \__,_| \_/\_/ |_|_|_| |_|\__, |
                                    |___/
```
## Setting-up:
### Pipenv
Git clone the repo
Install pipenv (https://pipenv-fork.readthedocs.io/en/latest/basics.html)

On mac :
```
brew install pipenv
```

(For Mac Users) If pipenv installation fails (due to psycopg2), run:

```
LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pipenv run pip install psycopg2
brew install pipenv
```

Then install packages through pipenv:

```
pipenv install
pipenv shell
```
### Chromedriver
Download [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/) and put it into root folder:
`./`

## How to run
```
python insta.py
```

## Structure

#### resources
The data that is extracted are installed. Including both data and images
