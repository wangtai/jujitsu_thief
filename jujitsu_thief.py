#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last modified: Wang Tai (i@wangtai.me)

"""
https://www.artofjiujitsu.com/online-training-program
POST
acao:login
members_userid:XXXX
members_password:PPPP
"""

__revision__ = '0.1'

from HTMLParser import HTMLParser

import requests


cookies = {'PHPSESSID': 'qas0pb48pgkdgh6v6hshj9o094'}


def get_video_url(url):
    # print url
    r = requests.get(url=url, cookies=cookies)

    urls = []
    for line in r.text.split('\n'):
        if line.find('mp4') != -1:
            url = line.split('"')[1]
            urls.append(url)
            print url
    return urls


class HTML(HTMLParser):
    url_list = []

    def __init__(self):
        HTMLParser.__init__(self)

        self.in_h2 = False
        self.url_list=[]

    def handle_starttag(self, tag, attrs):
        if tag == 'h2' and ('class', 'titulo') in attrs:
            self.in_h2 = True
        if tag == 'a' and self.in_h2:
            for attr in attrs:
                if attr[0] == 'href':
                    self.url_list.append(attr[1])
            self.in_h2 = False


if __name__ == '__main__':
    all_page_url = []
    for i in range(6):
        # print 'https://www.artofjiujitsu.com/online-training-program/filter/?&page={0}'.format(i + 1)
        r = requests.get(url='https://www.artofjiujitsu.com/online-training-program/filter/?&page={0}'.format(i + 1),
                         cookies=cookies)
        parser = HTML()
        parser.feed(r.text)
        print parser.url_list
        all_page_url.extend(parser.url_list)
        # for url in parser.url_list:
        #     get_video_url(url)

    all_page_url = list(set(all_page_url))

    for page_url in all_page_url:
        get_video_url(page_url)
