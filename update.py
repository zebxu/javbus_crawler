#! /usr/bin/env python3

# This is a Single-thread crawler starts from javbus2.pw/page/1

import parser
import crawler
import database
import timeit
import requests
import os
from object_prototye import Counter
import datetime


def update(url, counter):
    """ parse function for each page"""

    # get main page soup
    main_page_soup = parser.get_main_page_soup(url)

    # request the website and get the elements
    movie_links = parser.get_movie_page_list(main_page_soup)

    # get next page url
    next_page = parser.get_next_page_url(main_page_soup)

    # loop through each movie box in the main page
    for i in movie_links:

        if counter.page_skip >= 5:
            print('已有过多重复电影，停止更新')
            return False

        # get av num from the soup
        av_num = parser.get_av_num(i)

        if database.check_existence(av_num):
            print('* 已存在 %s 停止爬取 *' % av_num)
            counter.increment_movie_skip()
            continue

        # get view page soup
        soup = parser.get_link_soup(i)

        # show current working status
        print('正在扒取：第' + str(os.path.basename(url)) + '页' + ' 番号：' + av_num)

        # get movie object info
        movie = parser.get_movie(soup, av_num)

        # show movie object
        # print(movie)

        stars = parser.get_star_list(soup)
        links = parser.get_download_link(soup, url, av_num)

        images = parser.get_sample_img_list(soup)

        # store movie info to database
        database.insert_movie(movie)

        # store star info to database
        for s in stars:
            database.insert_star(s, av_num)

        # store links info to database
        for l in links:
            database.insert_magnet(l)

        # store images url to database
        for g in images:
            database.insert_img(g, av_num)

        counter.increment_parse()

    if counter.movie_skip >= 30:
        counter.increment_page_skip()

    print('第 ' + str(os.path.basename(url)) + ' 页扒取完毕')
    print('-------------------------')

    return next_page


def main_update(start_page_url, counter):

    # log start time
    with open('update_parsing_log.txt', 'a') as f:
        f.write('Start time:' + str(datetime.datetime.now()) + '\n')

    next_page = start_page_url

    print(next_page)

    # If next page is a FALSE value, the function return
    if next_page:
        while next_page:
            print('Entering URL:' + next_page)

            try:
                # parse the given page
                next_page = update(next_page, counter)
            except Exception as e:
                print('-------------------------------- {} : {}'.format(e, next_page))
                log_fail_movie(next_page, e)
                next_page = crawler.skip_page(next_page)
                continue


def log_fail_movie(failed_url, error):
    with open('update_parsing_log.txt', 'a') as f:
        f.write('{} \n {}\n'.format(failed_url, error))


def main():
    # start the timer
    start_time = timeit.default_timer()

    # entry must contains /hd/page
    entry_url = 'https://www.javbus2.pw/page/1'

    count = Counter()

    try:
        # start main parsing
        main_update(entry_url, count)
    except KeyboardInterrupt:
        print('Stop by user')

    # calculate run time
    stop_time = timeit.default_timer()

    time_spent = stop_time - start_time

    # log end time
    with open('update_parsing_log.txt', 'a') as f:
        f.write('End Time: ' + str(datetime.datetime.now()) + '\n')
        f.write('Time Spent：' + str(time_spent / 60) + ' mins\n')
        f.write('已扒取 {} 部电影\n\n\n'.format(count.parsing_time))
        f.write('********************************************************\n')

    print('用时：%s mins' % str(time_spent / 60))

    print('已扒取 %s 部电影' % count.parsing_time)

    print('Complete Parsing')


if __name__ == '__main__':
    main()
