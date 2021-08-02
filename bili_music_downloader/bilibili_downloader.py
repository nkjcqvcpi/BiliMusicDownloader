import argparse
import json
import os

import requests


class Downloader:
    def __init__(self):
        self.download_api = 'https://api.bilibili.com/x/player/playurl'
        self.info_api = 'https://api.bilibili.com/x/web-interface/view'
        self.params = {'cid': None, 'fnval': 16}
        self.header = {'Referer': 'https://www.bilibili.com/', 'User-Agent': None, 'Cookie':{'SESSDATA': None}}

    def download(self, id):
        if id[:2] == 'av':
            params = {'avid': id}
        elif id[:2] == 'BV':
            params = {'bvid': id}
        info = requests.get(self.info_api, params=params, cookies=self.header['Cookie'])
        j = json.loads(info.text)
        name = j['data']['title']
        cover = j['data']['pic']
        artists = j['data']['owner']['name']
        pages = [{'cid': i['cid'], 'name': i['part']} for i in j['data']['pages']]
        self.params.update(params)
        for p in pages:
            self.params['cid'] = p['cid']
            video = requests.get(self.download_api, params=self.params, cookies=self.header['Cookie'])
            vj = json.loads(video.text)
            url = vj['data']['dash']['audio'][0]['baseUrl']
            header = "$'Referer: {}\r\nUser-Agent: {}\r\nCookie: SESSDATA={}\r\n'".format(self.header['Referer'], self.header['User-Agent'], self.header['Cookie']['SESSDATA'])
            i = 'ffmpeg -headers {} -i "{}" -c copy {}.m4s'.format(header, url, str(p['cid']))
            os.system('ffmpeg -headers {} -i "{}" -acodec alac {}.m4a'.format(header, url, str(p['cid'])))

        i = 0


if __name__ == '__main__':
    pass
