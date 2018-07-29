# crawler_javbus
A Python web crawler that parse movie info from `JavBus` and store it in a [SQLite 3](https://www.sqlite.org/index.html) database

针对`JAVbus`的Python爬虫，爬取av信息，图片，还有磁链。所有数据使用[SQLite 3](https://www.sqlite.org/index.html)储存在本地

## Dependencies | 依赖包
* Python 3 is required
* before parsing, install all dependencies
```bash
$ pip3 i -r requirements.txt
```

* 需要安装Python 3
* 开始爬取之前，使用pip3安装`requirement.txt`里的包
```bash
$ pip3 i -r requirements.txt
```

## How to Use | 使用方法
* Go to crawler folder on terminal and run command
* 前往文件地址
```bash
$ cd .../crawler_javbus
```

* Run code below on terminal to start parsing
* 运行以下指令
```bash
$ python3 parser.py 1 999
```

 * The code above parse from page 1 to page 999
 * 所示指令会爬取第1到第999页
 
> Note: If you are using windows, the command lines will be different
> Note: windows的指令会有所不同

## Update | 更新数据库
* Run command below and parse the latest movies
* 获取最新发布的av
```bash
$ python3 update.py
```

## Data
* All parsing result are stored in `movies.db`
* 所以数据都会存在`movies.db`

## Problem
* If the website is down, try changing the entry url in the code
* 如果javbus的网址挂了，可以尝试更改代码中的entry url
