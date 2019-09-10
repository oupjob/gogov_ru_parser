import requests
from lxml import html

#import os
#print(os.path.dirname(os.path.abspath(__file__)))

#print('https://gogov.ru/mfc'.split())

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

# proxy = {'https': '66.82.22.79:80' }
proxy = {'https': '5.189.163.40:3128' }

loadmore_post_data = {
	'action': 'loadmore',
	'args': '',
	'page': 1,
	'tmplt': '',
	'txnm': '',
	'trmid': ''
}

import re

re_var_data = re.compile('var\s+data')
re_args = re.compile('\'(args)\'\s*:\s*\'(.*)\',')
re_tmplt = re.compile('\'(tmplt)\'\s*:\s*\'(.*)\',')
re_txnm = re.compile('\'(txnm)\'\s*:\s*\'(.*)\',')
re_trmid = re.compile('\'(trmid)\'\s*:\s*\'(.*)\',') 

r = requests.get('https://gogov.ru/msk/mfc', headers=headers, proxies=proxy)

res = re_var_data.search(r.text)
pos = res.end()

loadmore_post_data['args'] = re_args.findall(r.text, pos)[0][1]
loadmore_post_data['tmplt'] = re_tmplt.findall(r.text, pos)[0][1]
loadmore_post_data['txnm'] = re_txnm.findall(r.text, pos)[0][1]
loadmore_post_data['trmid'] = re_trmid.findall(r.text, pos)[0][1]

print(loadmore_post_data)

while True:
	r = requests.post('https://gogov.ru/wp-admin/admin-ajax.php', headers=headers, data=loadmore_post_data, proxies=proxy)
	if not r.text:
		break

	lxml_tree = html.fromstring(r.text)
	div_list = lxml_tree.xpath('//div[@class = "ta-211"]')
	for div in div_list:
		name = div.xpath('.//a/text()')
		link = div.xpath('.//a/@href')

		print('name: %s, link %s' % (name, link))

	loadmore_post_data['page'] += 1

#print(r.text)
#if not r.text:
#	print("not r.text")
