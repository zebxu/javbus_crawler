#! /usr/bin/env python3

import bs4
import requests
from object_prototye import Movie, Link
import crawler
import os


def get_main_page_soup(home_url):
    """ parse main page soup"""

    # request to javbus
    res = requests.get(home_url)
    res.raise_for_status()

    # init beautiful soup
    soup = bs4.BeautifulSoup(res.text, 'lxml')

    return soup


def get_next_page_url(soup):
    """ Get next page url from main page soup"""

    next_page_elements = soup.select('a[id="next"]')

    if len(next_page_elements) < 1:
        # reach the last page
        return False
    else:
        next_page = 'https://www.javbus2.pw' + next_page_elements[0]['href']

    return next_page


def get_movie_page_list(soup):
    """ Get view page link list form main page soup"""

    # select all movie box
    url_elements = soup.select('a[class="movie-box"]')

    # url_list = []

    for u in url_elements:
        yield u['href']
        # url_list.append(u['href'])

    # print the number of movies in this page
    # print('项目数：' + str(len(url_list)))

    # return url_list


def get_link_soup(link):
    """ get the soup of given link"""
    viewPageRes = requests.get(link)
    viewPageRes.raise_for_status()

    # make soup of view page
    viewPageSoup = bs4.BeautifulSoup(viewPageRes.text, 'html.parser')

    return viewPageSoup


def get_av_num(link):
    """ get av num"""

    av_num = link.split('/')[-1]

    return av_num


def get_movie(soup, avNum):
    """ Get movie info from view page"""

    # don't get soup too often, the server will rufuse request
    # soup = get_link_soup(link)

    # get cover and title
    bigImgElems = soup.select('.bigImage img')

    # get title
    title = bigImgElems[0].get('title')

    # get cover image url
    cover_img = bigImgElems[0].get('src')

    dateElems = soup.find('span', text="發行日期:")
    date = dateElems.next_sibling[1:]

    movie = Movie(avNum, title, cover_img, date)

    return movie


def get_star_list(soup):
    """ Get star list from view page"""

    # don't get soup too often, the server will rufused request
    # soup = get_link_soup(link)

    # stars = []

    star_elements = soup.select('div[class="star-name"]')
    for s in star_elements:
        yield s.text
        # stars.append(s.text)

    # return stars


def get_sample_img_list(soup):
    """ Get sample images from view page"""

    # don't get soup too often, the server will rufused request
    # soup = get_link_soup(link)

    # sampleImgs = []

    sampleImgElems = soup.select('a[class="sample-box"]')

    for n in sampleImgElems:
        yield n['href']
        # sampleImgs.append(n['href'])

    # return sampleImgs


def get_download_link(soup, home_url, avNum):
    """ get download link"""

    # don't get soup too often, the server will rufused request
    # soup = get_link_soup(link)

    paramsElems = soup.find_all('script')[8]
    text = paramsElems.text
    gid = text[12:24]
    reqUrl = 'https://www.javbus2.pw/ajax/uncledatoolsbyajax.php'
    header = {'referer': home_url}

    payload = {'gid': gid, 'uc': 0}

    tableRes = requests.get(reqUrl, params=payload, headers=header)
    tableRes.raise_for_status()

    magnetSoup = bs4.BeautifulSoup(tableRes.text, 'html.parser')
    magnetElems = magnetSoup.select('a[style="color:#333"]')
    m = 1

    # links = []

    while m < len(magnetElems):
        magnetLink = magnetElems[m].get('href')
        movieSize = magnetElems[m].text
        m = m + 3

        yield Link(avNum, magnetLink, movieSize)
        # links.append(Link(avNum, magnetLink, movieSize))

    # return links


# function testing
if __name__ == '__main__':
    print('testing')
    entry = 'https://www.javbus2.pw/'
    tSoup = get_main_page_soup(entry)

    tUrl = get_next_page_url(tSoup)
    print(tUrl)
    tMovList = get_movie_page_list(tSoup)
    print(tMovList)

    l = next(tMovList)

    tLinkSoup = get_link_soup(l)

    tAvNum = get_av_num(l)
    print(tAvNum)
    tMov = get_movie(tLinkSoup, tAvNum)
    print(tMov)
    tStarList = get_star_list(tLinkSoup)
    print(tStarList)
    for s in tStarList:
        print(s)
    tImgList = get_sample_img_list(tLinkSoup)
    print(tImgList)
    print(next(tImgList))
    tDownLink = get_download_link(tLinkSoup, entry, tAvNum)
    print(tDownLink)
    print(next(tDownLink))

