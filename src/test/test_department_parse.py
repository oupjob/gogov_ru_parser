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
# proxy = {'https': '5.189.163.40:3128' }
url = 'https://gogov.ru/mfc/msk/m569685'

r = requests.get(url, headers=headers, proxies={})
lxml_tree = html.fromstring(r.text)

data_tables = lxml_tree.xpath('//table[@class = "data"]') # /tr[not(@class)]/td[@class!=first]')
print(data_tables)

simple_fields = ['district', 'locality', 'email', 'phone', 'index']

for data_table in data_tables:
	data_table_fields = data_table.xpath('.//tr/td[not(@class)]')

	# printout all fields
	for field in data_table_fields:
		print(field.xpath('.//@id'), field.xpath('.//text()'))

	# parse simple fields
	for field in data_table_fields:
		name = field.xpath('.//@id')
		name = name[0] if len(name) else ''
		value = field.xpath('.//text()')
		if name in simple_fields:
			value = value[0]
			print('name: %s, value: %s' % (name, value))
	
	# parse address
	for field in data_table_fields:
		if len(field) and field[0] == 'address':
			name = field[0]
			value = field.xpath('.//text()')[0]
			print('name: %s, value: %s' % (name, value))
		
	


#print(r.text)
#if not r.text:
#	print("not r.text")
