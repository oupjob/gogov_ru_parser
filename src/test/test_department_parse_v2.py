import requests
from lxml import html
import lxml
import re

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
# url = 'https://gogov.ru/mfc/msk/m569685'
# url = 'https://gogov.ru/gibdd/msk/g667020'
# url = 'https://gogov.ru/gibdd/msk/g99231'
url = ''

import sys
if not url: url = sys.argv[1]

r = requests.get(url, headers=headers, proxies={})
lxml_tree = html.fromstring(r.text)

data_table_fields = lxml_tree.xpath('//table[@class = "data"]/tr/td[not(@class)]') # /tr[not(@class)]/td[@class!=first]')
print(data_table_fields)

simple_fields = ['fullname', 'shortname', 'district', 'locality', 'index', 'ceo', 'address-ex']

re_coverage = re.compile('^[\r\n\t]+$')

for field in data_table_fields:
	v_name = field.xpath('.//@id')
	v_value = field.xpath('.//text()')
	print(v_name, v_value)
	
print('== PARSING FIELDS ', 44 * '==')
for field in data_table_fields:
	field_parsed = False

	v_name = field.xpath('.//@id')
	v_value = field.xpath('.//text()')
	
	# simple fields
	if len(v_name) and v_name[0] in simple_fields:
		print('[SIMPLE] name: %s, value: %s' % (v_name[0], v_value[0]))
		field_parsed = True
		continue

	# array fields
	if len(v_name) and v_name[0] == 'email':
		print('[A_EMAIL] name: %s, value: %s' % (v_name[0], v_value))
		field_parsed = True
		continue

	if len(v_name) and v_name[0] == 'site':
		print('[A_WEBSITE] name: %s, value: %s' % (v_name[0], v_value))
		field_parsed = True
		continue
	
	if len(v_name) and v_name[0] == 'phone':
		print('[A_PHONE] name: %s, value: %s' % (v_name[0], v_value))
		field_parsed = True
		continue
	
	if len(v_name) and v_name[0] == 'coverage':
		v_value = list(filter(lambda s: not re_coverage.match(s), v_value))
		print('[A_COVERAGE] name: %s, value: %s' % (v_name[0], v_value))
		field_parsed = True
		continue


	# address 
	if len(v_name) and v_name[0] == 'address':
		print('[ADDRESS] name: %s, value: %s' % (v_name[0], v_value[0]))
		field_parsed = True
		continue
	
	# address-ex	
	if len(v_name) and v_name[0] == 'address':
		print('[ADDRESS] name: %s, value: %s' % (v_name[0], v_value[0]))
		field_parsed = True
		continue

	# mode
	if len(v_name) and v_name[0] == 'mode':
		value = ''.join(v_value)
		print('[MODE] name: %s, value:\n>>>\n%s\n>>>' % (v_name[0], value))
		field_parsed = True
		continue

	# direction
	if len(v_name) and v_name[0] == 'offices-gu':
		a_link_field = field.xpath('.//*/a')
		av_value = a_link_field[0].xpath('.//text()')
		av_link = a_link_field[0].xpath('.//@href')
		
		print('[DIRECTION] link: %s, value:\n>>>\n%s\n>>>' % (av_link[0], v_value[0]))
		field_parsed = True
		continue

	if not field_parsed and  len(v_name):
		print('FIELD NOT PARSED: %s, %s' % (v_name, v_value))


print('== PARSING SERVICES ', 44 * '==')

import pprint

table_row_data_services = lxml_tree.xpath('//table[@class = "data"]/tr/td[text()[contains(.,"Сервисы")]]/..')
table_row_data_services = table_row_data_services[0]

svcs = table_row_data_services.xpath('.//td/div/div') # [@class="ab-li"]')
n = len(svcs)
services_tree = {}
i_last_fl_svc = 0
for i in range(n):	
	svc_name = ''
	svc_url = ''
	# print(svcs[i].attrib)

	if svcs[i].attrib.has_key('class') and 'ab-li' in svcs[i].attrib['class']: # svcs[i].xpath('.//[@class="ab-li"]'):
		svc_name = svcs[i].xpath('./a/text()')[0]
		svc_url = svcs[i].xpath('./a/@href')[0]

		services_tree[svc_name] = {'url': svc_url}
	else:
		svc_name = svcs[i].xpath('./text()')
		svc_url = ''

		if not len(svc_name):
			continue

		svc_name = svc_name[0]
		
		services_tree[svc_name] = {}		

		subservices = svcs[i].xpath('following-sibling::*[@class="svc-list"]/div[@class="ab-li"]')
		for s_svc in subservices:
			s_svc_name = s_svc.xpath('./a/text()')[0]
			s_svc_url = s_svc.xpath('./a/@href')[0]

			services_tree[svc_name][s_svc_name] = { 'url': s_svc_url }
					
	print('svc_name: %s, svc_url: %s' % (svc_name, svc_url))
#	 services[svc_name] = {'url': svc_url}
pprint.pprint(services_tree)
