#! /usr/bin/env python3

# This is a four threads crawler starts from javbus2.pw/genre/hd/1

import parser
import database
import os
import timeit
import threading
import sys
import datetime
from object_prototye import Counter


def parse_page(url, thread_num, counter):
    """ parse function for each page"""

    # get main page soup
    main_page_soup = parser.get_main_page_soup(url)

    # request the website and get the elements
    movie_links = parser.get_movie_page_list(main_page_soup)

    # get next page url
    next_page = parser.get_next_page_url(main_page_soup)

    # loop through each movie box in the main page
    for i in movie_links:

        # get av num from the soup
        av_num = parser.get_av_num(i)

        # skip existed movie
        if database.check_existence(av_num):
            print('* 已存在 %s 停止爬取 *' % av_num)
            continue

        # get view page soup
        soup = parser.get_link_soup(i)

        # show current working status
        print('Thread {} 正在扒取：第 {} 页 番号：{}'.format(str(thread_num),
                                                            str(os.path.basename(url)), av_num))

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

    print('第 ' + str(os.path.basename(url)) + ' 页扒取完毕')
    print('-------------------------')

    return next_page


def main(start_page_url, end_page_num, thread_num, counter):

    # create a new database at "movies.db"
    database.init()

    next_page = start_page_url

    # If next page is a FALSE value, the function return

    while int(os.path.basename(next_page)) <= end_page_num:
        print('Thread {} Entering URL:{}'.format(thread_num, next_page))

        try:
            # parse the given page
            next_page = parse_page(next_page, thread_num, counter)
        except Exception as e:
            print('Thread {} facing exception:'.format(thread_num))
            print('************************************* {}: '.format(e) + next_page)
            log_fail_movie(next_page, e, thread_num)
            next_page = skip_page(next_page)
            print('Thread {} skip page'.format(thread_num))
            continue
        except KeyboardInterrupt:
            print('Exit by user')
            return

    # log thread complete time
    with open('failed_movies.txt', 'a') as f:
        f.write('Thread {} complete at {}\n'.format(thread_num, str(datetime.datetime.now().time())))


def skip_page(this_page_url):
    """ Get next page url from given url"""

    next_num = int(os.path.basename(this_page_url)) + 1
    next_page_url = get_page_url(next_num)

    return next_page_url


def get_page_url(page_num):
    """ generate a javbus page url when assign different page for multi-threading"""
    page_url = 'https://www.javbus2.pw/genre/hd/' + str(page_num)

    return page_url


def log_fail_movie(failed_url, error, thread):
    with open('failed_movies.txt', 'a') as f:
        f.write('\nThread {}: {}\n  {}\n'.format(thread, failed_url, error))


def multi_threads_main():
    # initialize the counter object
    count = Counter()

    # start the timer
    start_time = timeit.default_timer()

    try:
        # first page number
        first_page = int(sys.argv[1])

        # max page number 1325
        max_page = int(sys.argv[2])

        # log start status
        with open('failed_movies.txt', 'a') as f:
            f.write('Parse from page {} to page {}\n'.format(sys.argv[1], sys.argv[2]))
            f.write('Start time:' + str(datetime.datetime.now()) + '\n')

    except IndexError:
        print('No arguments to indicate what pages to parse, use default params')
        first_page = 1
        max_page = 10

        with open('failed_movies.txt', 'a') as f:
            f.write('Parse from page 1 to page 2\n')
            f.write('Start time:' + str(datetime.datetime.now()) + '\n')

    # calculate page assignment for each thread
    # entry must contains /hd/page
    entry_url = 'https://www.javbus2.pw/genre/hd/' + str(first_page)
    half_page = int((max_page + first_page) / 2)
    quarter_page = int((first_page + half_page) / 2)
    third_quarter_page = int((half_page + max_page) / 2)
    thread_2_url = get_page_url(quarter_page + 1)
    thread_3_url = get_page_url(half_page + 1)
    thread_4_url = get_page_url(third_quarter_page + 1)

    # sub thread objects
    second_thread = threading.Thread(target=main, args=[thread_2_url, half_page, 2, count])

    third_thread = threading.Thread(target=main, args=[thread_3_url, third_quarter_page, 3, count])

    fourth_thread = threading.Thread(target=main, args=[thread_4_url, max_page, 4, count])

    # start sub parsing threads
    second_thread.start()

    third_thread.start()

    fourth_thread.start()

    # start main parsing
    main(entry_url, quarter_page, 1, count)

    # calculate run time
    stop_time = timeit.default_timer()

    time_spent = stop_time - start_time

    # wait for all threads to end
    second_thread.join()
    third_thread.join()
    fourth_thread.join()

    # log end status
    with open('failed_movies.txt', 'a') as f:
        f.write('End Time: ' + str(datetime.datetime.now()) + '\n')
        f.write('Time Spent：' + str(time_spent / 60) + ' mins\n\n\n\n\n')
        f.write(str(count.parsing_time) + ' new movies were parsed\n')
        f.write('********************************************************\n')

    print('用时：' + str(time_spent / 60) + ' mins')

    print(str(count.parsing_time) + ' new movies were parsed')

    print('Parsing Complete')


if __name__ == '__main__':
    multi_threads_main()
