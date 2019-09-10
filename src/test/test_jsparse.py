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

import re

re_var_data = re.compile('var\s+data')
re_args = re.compile('\'(args)\'\s*:(.+)')
re_tmplt = re.compile('\'(tmplt)\'\s*:(.+)')
re_txnm = re.compile('\'(txnm)\'\s*:(.+)')
re_trmid = re.compile('\'(trmid)\'\s*:(.+)')

r = requests.get('https://gogov.ru/msk/mfc', headers=headers)
#tree = html.fromstring(r.text)
#script_list = tree.xpath('//script')

#print(script_list[0].text_content())

# for script in script_list:

res = re_var_data.search(r.text)
# if not res: continue
pos = res.end()

res = re_args.findall(r.text, pos)
# if not res: continue
print(res)

res = re_tmplt.findall(r.text, pos)
# if not res: continue
print(res)

res = re_txnm.findall(r.text, pos)
# if not res: continue
print(res)

res = re_trmid.findall(r.text, pos)
# if not res: continue
print(res)

# if res: break
