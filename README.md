# crawler_javbus
A Python web crawler that parse movie info from `JavBus` and store it in a [SQLite 3](https://www.sqlite.org/index.html) database

## Dependencies
> Python 3 is required
before parsing, install all dependencies
```bash
$ pip3 i -r requirements.txt
```

## How to Use
> If you are using windows, the command lines will be different
* Go to crawler folder on terminal
```bash
$ cd .../crawler_javbus
```

* Run code below on terminal to start parsing
```bash
$ python3 parser.py 1 999
```
 The code above parse from page 1 to page 999

## Update
* Run command below and parse the latest movies
```bash
$ python3 update.py
```

## Data
All parsing result are stored in `movies.db`

## Problem
If the website is down, try changing the entry url in the code
