import requests
from lxml import html

import os
print(os.path.dirname(os.path.abspath(__file__)))

print('https://gogov.ru/mfc'.split())

headers = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
	'Cache-Control': 'max-age=0',
	'Connection': 'keep-alive',
#	'Cookie': '_ym_uid=1565946121531196919; _ym_d=1565946121; _ym_visorc_32016646=w; _ym_isad=1',
	'DNT': '1',
#	'Host': 'gogov.ru',
#	'Referer': 'https://gogov.ru/mfc/msk/m569685',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36 OPR/56.0.3051.31'
}

r = requests.get('https://gogov.ru/mfc', headers=headers)
tree = html.fromstring(r.text)
tbl = tree.xpath('//div[@class = "tbl"]')[0]
region_list = tbl.xpath('.//div[@class = "rw-2"]/div[@class = "cl-2-1"]')

for reg in region_list:
#	print(reg.text)
#	name = reg.xpath('.//a/text()')[0]
#	link = reg.xpath('.//a/@href')[0]
	print(reg.xpath('.//a/text()'), reg.xpath('.//a/@href'))

	# print('name: %s, link: %s' % (name, link))


