
class Movie:
    """ class for each movie in javbus website"""

    def __init__(self, avNum, title, coverImgUrl, date):
        self._avNum = avNum
        self._title = title
        self._cover_img = coverImgUrl
        self._release_date = date

    @property
    def avNum(self):
        return self._avNum

    @property
    def title(self):
        return self._title

    @property
    def cover_img(self):
        return self._cover_img

    @property
    def release_date(self):
        return self._release_date

    def __repr__(self):
        return '{} {} {} {}'.format(self._avNum, self._title, self._cover_img, self._release_date)


class Link:
    """ Class for magnet link"""

    def __init__(self, avNum, magnet, size):
        self._avNum = avNum
        self._magnet = magnet
        self._size = size

    @property
    def size(self):
        return self._size

    @property
    def magnet(self):
        return self._magnet

    @property
    def av_num(self):
        return self._avNum

    def __repr__(self):
        return '{} {} {}'.format(self._avNum, self._magnet, self._size)


class Counter:
    """ Class for counter"""
    def __init__(self):
        self._parsing_time = 0
        self._page_skip = 0
        self._movie_skip = 0

    @property
    def parsing_time(self):
        return self._parsing_time

    @property
    def page_skip(self):
        return self._page_skip

    @property
    def movie_skip(self):
        return self._movie_skip

    def reset_movie_skip(self):
        self._movie_skip = 0

    def increment_movie_skip(self):
        self._movie_skip += 1

    def increment_page_skip(self):
        self._page_skip += 1

    def increment_parse(self):
        self._parsing_time += 1
