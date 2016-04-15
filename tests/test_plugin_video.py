#!/usr/bin/env python
# coding: utf-8
# vim:fenc=utf-8:sts=0:ts=4:sw=4:et:tw=80

#
# Copyright © 2016 gr4ph3 <giraffeoncode@gmail.com>
#
# Distributed under terms of the MIT license.
#

import pytest
assert pytest
import re
import addon.plugin_video as plugin_video
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


def check_item(item):
    assert re.match(r'^[^\s]', item['li'].name)
    assert isinstance(item['url'], str)


def check_thumb(item):
    assert re.match(r'^http:\/\/cdn\.seasonvar\.ru\/oblojka\/\d+\.jpg',
                    item['li'].thumb)


def check_directory_item(item):
    check_item(item)
    assert item['is_dir'] is True


def check_thumb_directory_item(item):
    check_directory_item(item)
    check_thumb(item)


def check_thumb_item(item):
    check_item(item)
    check_thumb(item)


def test_screen_start(requests_mock, addon, kodi):
    plugin_video.screen_start({})
    # 7 date items from seasonvar site
    # 1 for search
    assert len(kodi.items) == 8
    for i in kodi.items:
        check_directory_item(i)
        assert i['count'] is None
    assert kodi.items[-1]['li'].name == u'Поиск'


def test_screen_date_bad_params(requests_mock, addon, kodi):
    requests_mock.respond(r'seasonvar.ru\/rss\.php$', 'assets/rss01.xml')
    plugin_video.screen_date({})
    assert len(kodi.items) == 0
    plugin_video.screen_date({'date': 'hello'})
    assert len(kodi.items) == 0


def test_screen_date(requests_mock, addon, kodi):
    requests_mock.respond(r'seasonvar.ru\/rss\.php$', 'assets/rss01.xml')
    plugin_video.screen_date({'date': '12.04.2016'})
    assert len(kodi.items) == 3
    for i in kodi.items:
        check_thumb_directory_item(i)


def test_screen_episodes_bad_params(requests_mock, addon, kodi):
    plugin_video.screen_episodes({})
    assert len(kodi.items) == 0


def test_screen_episodes(requests_mock, addon, kodi):
    requests_mock.respond(r'seasonvar.ru\/.*Skorpion.*\.html$',
                          'assets/scorpion.html')
    requests_mock.respond(r'seasonvar.ru\/playls2.*12394/list\.xml$',
                          'assets/playlist_scorpion.json')
    seasonurl = '/serial-12394-Skorpion_serial_2014_ndash_.html'
    plugin_video.screen_episodes({'url': seasonurl})
    assert len(kodi.items) == 23
    assert kodi.items[0]['li'].name == u'сезон 2/2'
    for i in kodi.items[1:]:
        check_thumb_item(i)


# def test_screen_date(requests_mock, addon, kodi):
#     requests_mock.respond(r'seasonvar.ru$', 'tests/samples/main_page.html')
#     seasonvar = Seasonvar()
#     plugin_video.screen_episodes({'name': 'Агентство Лунный Свет'}, seasonvar)
#     assert len(kodi.items) > 0
#     for i in kodi.items:
#         check_thumb_directory_item(i)
#     pprint.pprint(kodi.items)
