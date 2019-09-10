import requests
from lxml import html
import re
import logging
import json
from config.main_config import ROOT_URL
from src.tools.proxy_switcher import ProxySwitchRequest

def normalizeUrl(url):
	if not url:
		return url
	
	if not (ROOT_URL in url):
		delim = '/' if url[0] != '/' else ''
		url = ROOT_URL + delim + url
		
	return url
			

def nameFromUrl(url):
	s = url.split('/')
	n = len(s) - 1
	return s[n] if n >= 0 else None

""" 
Tree Structure

DepartmentType (such as mfc, ufms, gibdd) -> RegionList
RegionList = [Region, Region, ...]

DeparmentType
|-Region 1
| |- Department 1.1
| |  |- ServiceTree1.1
| |- Department 1.2
| |  |- ServiceTree1.2
| |- Department 1.M[1]
| ...
|-Region 2
| |- Department2.1
|    |- ServiceTree2.1
...
|-Region N
| |- Department N.1
|    |- ServiceTreeN.1

ServiceTree:

FirsLevelService
|- SecondLevelService
|- SecondLevelService
...

"""
class TreeItem:
	def __init__(self, name, src_url, children):
		self.name = name
		self.src_url = normalizeUrl(src_url)
			
		self.children = children
		
	def dump(self, offset=0, print_fn = print):
		print_fn((" " * offset) + "TreeItem: name: %s, src_url: %s" % (self.name, self.src_url))
		 
		for c in self.children: 
			c.dump(offset + 2, print_fn=print_fn)
			
	#def __repr__(self):
		#return "TreeItem<name=%s, src_url=%s>" % (self.name, self.src_url)


class DepartmentTreeItem(TreeItem):
	simple_fields = ['fullname', 'shortname', 'district', 'locality', 'index', 'ceo', 'address-ex']
	array_fields = ['site', 'phone', 'email', 'coverage']
	
	def __init__(self, name, src_url, fields={}, children=[]):
		super().__init__(name, src_url, children)
		self.fields = fields
		
	def dump(self, offset=0, print_fn = lambda x: print(x)):
		print_fn((" " * offset) + ("DepartmentTreeItem: name: %s, src_url: %s" % (self.name, self.src_url)))
		for k, v in self.fields.items():
			print_fn((" " * offset) + '"%s" : "%s"' % (k, v))
		 
		for c in self.children: 
			c.dump(offset + 2, print_fn=print_fn)
			
	#def __repr__(self):
		#s = "DeparmtentTreeItem<name=%s, src_url=%s>" % (self.name, self.src_url)
		#if not len(self.fields.items()):
			#return s
		#else:
			#s += '\n'
			
		#for k, v in self.fields.items():
			#s += ((" " * offset) + '"%s" : "%s"\n' % (k, v))

	
	
class ServiceTreeItem(TreeItem):
	def __init__(self, name, destination_url, children=[]):
		super().__init__(name, '', children)
		self.destination_url = normalizeUrl(destination_url)
		
	def dump(self, offset=0, print_fn = print):
		print_fn((" " * offset) + "ServiceTreeItem: name: %s, destination_url: %s" % (self.name, self.destination_url))
		
		for c in self.children: 
			c.dump(offset + 2, print_fn=print_fn)


class BaseParser:
	headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
		'Cache-Control': 'max-age=0',
		'Connection': 'keep-alive',
		'DNT': '1',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': ProxySwitchRequest.currentUserAgent()
	}
	# 		'User-Agent': '

	def exec(self):
		pass

	def msgInfo(self, message):
		print('%s: %s' % (self.__class__.__name__, message))

	def msgError(self, message):
		print('ERROR: %s: %s' % (self.__class__.__name__, message))
	
"""
BaseRegionListParser: DeparmentTypeTI(DeparmentType(url)) -> [RegionTI, RegionTI, ...]
where 	RegionTI is Region Tree Item
		DeparmentTypeTI is DeparmentType Tree Item
"""	

class BaseRegionListParser(BaseParser):	
	def __init__(self, parent_tree_item):
		self.parent_tree_item = parent_tree_item
		
	def exec(self):
		self.msgInfo('Starting: parsing region list from URL: "%s"' % (self.parent_tree_item.src_url))
#		try:
#			r = requests.get(self.parent_tree_item.src_url, headers=self.headers, proxies=proxySettings())
#		except Exception as e:
#			self.msgError("Could'nt get HTTP response %s" % str(e))
#			return

		r = ProxySwitchRequest.request(requests.get, url=self.parent_tree_item.src_url, headers=self.headers)
		
		lxml_tree = html.fromstring(r.text)
		tbl = lxml_tree.xpath('//div[@class = "tbl"]')
		if len(tbl):
			tbl = tbl[0]
		else:
			self.msgError("Could'nt get parent table div for region list")
			return
			
		region_list = tbl.xpath('.//div[@class = "rw-2"]/div[@class = "cl-2-1"]')

		i = 1
		for reg in region_list:
			name = reg.xpath('.//a/text()') 
			if len(name):
				name = str(name[0])
			else:
				self.msgError("Could'nt get region name of list item number %s" % (i))
				continue
			
			url = str(reg.xpath('.//a/@href'))
			if len(url):
				url = str(url[0])
			else:
				self.msgError("Could'nt get region url of list item number %s" % (i))
				continue
			
			tree_item = TreeItem(name, url, [])
			self.parent_tree_item.children.append(tree_item)
			
			self.msgInfo("Parsed Region Tree Item: ")
			tree_item.dump()
			
			i += 1
			
#		self.msgInfo('Completed: parsed %d regions to list from URL: "%s"' % (i - 1, self.parent_tree_item.src_url))
		self.msgInfo('Completed: parsed %d regions to list from URL: "%s"' % (i, self.parent_tree_item.src_url))
		
"""
DeparmentListParser: RegionTI -> RegionTI UNION [unfilled(Department), unfilled(Department), ...]
"""

class BaseDepartmentListParser(BaseParser):
	# regexps for parsing POST data for `loadmore` query
	re_var_data = re.compile('var\s+data')
	re_args = re.compile('\'(args)\'\s*:\s*\'(.*)\',')
	re_tmplt = re.compile('\'(tmplt)\'\s*:\s*\'(.*)\',')
	re_txnm = re.compile('\'(txnm)\'\s*:\s*\'(.*)\',')
	re_trmid = re.compile('\'(trmid)\'\s*:\s*\'(.*)\',')
	
	loadmore_post_data = {
		'action': 'loadmore',
		'args': '',
		'page': 1,
		'tmplt': '',
		'txnm': '',
		'trmid': ''
	}
	
	def __init__(self, parent_tree_item):
		self.parent_tree_item = parent_tree_item
		self.loadmore_url = 'https://gogov.ru/wp-admin/admin-ajax.php'
		
	def parseResponse(self, response):
		lxml_tree = html.fromstring(response.text)
		div_list = lxml_tree.xpath('//div[@class = "ta-211"]')
		i = 0
		for div in div_list:
			name = div.xpath('.//a/text()') 
			if len(name):
				name = str(name[0])
			else:
				self.msgError("Could'nt get department name of list item number %s" % (i))
				continue

			url = div.xpath('.//a/@href')
			if len(url):
				url = str(url[0])
			else:
				self.msgError("Could'nt get department url of list item number %s" % (i))
				continue

			tree_item = DepartmentTreeItem(name, url, {}, [])
			self.parent_tree_item.children.append(tree_item)
			
			self.msgInfo("Parsed basic data of Department Tree Item: ")
			tree_item.dump()
			
			i += 1
			
		return lxml_tree
		
	def primaryPageParse(self):
		self.msgInfo(
			'Starting: parsing primary page of department list from URL: "%s", Region: "%s"' % (self.parent_tree_item.src_url, self.parent_tree_item.name)
		)
		
#		try:
#			r = requests.get(self.parent_tree_item.src_url, headers=self.headers, proxies=proxySettings())
#		except Exception as e:
#			self.msgError("Could'nt get HTTP response : %s" % str(e))
#			return False
		r = ProxySwitchRequest.request(requests.get, url=self.parent_tree_item.src_url, headers=self.headers)

		lxml_tree = self.parseResponse(r)

		# grabbing POST query form data from inline document js script
		res = self.re_var_data.search(r.text)
		if not res:
			self.msgError("Could'nt parse loadmore action form data in response")
			return False
		pos = res.end()
		
		success = True
		
		# error handling closure
		def setLoadmoreFormData(key, res):
			if len(res) and len(res[0]) == 2:
				self.loadmore_post_data[key] = res[0][1]
			else:
				self.msgError("Could'nt parse loadmore action form data field '%s' in response" % (key))
				success = False
				
		setLoadmoreFormData('args',		self.re_args.findall(r.text, pos))
		setLoadmoreFormData('tmplt',	self.re_tmplt.findall(r.text, pos))
		setLoadmoreFormData('txnm',		self.re_txnm.findall(r.text, pos))
		setLoadmoreFormData('trmid',	self.re_trmid.findall(r.text, pos))
		
		return success
	
	def loadmorePagesParse(self):
		self.loadmore_post_data['page'] = 1
		
#		try:
		while True:
#				r = requests.post(self.loadmore_url, headers=self.headers, data=self.loadmore_post_data, proxies=proxySettings())

			r = ProxySwitchRequest.request(requests.post, url=self.loadmore_url, data=self.loadmore_post_data, headers=self.headers)
			if not r.text:
				break

			self.parseResponse(r)
			self.loadmore_post_data['page'] += 1
#		except Exception as e:
#			self.msgError("Could'nt get HTTP loadmore response: %s" % str(e))
#			self.loadmore_post_data['page'] = 1
#			return False

		self.loadmore_post_data['page'] = 1
		return True
		
		
	def exec(self):
		self.msgInfo('Started: Department list parsing from URL: "%s", Region: "%s"' % (self.parent_tree_item.src_url, self.parent_tree_item.name))
		
		parse_success = True
		def logResult(log_mess):	
			if not parse_success:
				self.msgError('Not correct: %s' % (log_mess))
			else:
				self.msgInfo('Completed: %s' % (log_mess))
		
		parse_success = self.primaryPageParse()
		logResult(
			'Parsing primary page of department list from URL: "%s", Region: %s' % (self.parent_tree_item.src_url, self.parent_tree_item.name)
		)
		if not parse_success:
			return
		
		parse_success = self.loadmorePagesParse()
		logResult(
			'Parsing loadmore pages of department list from URL: "%s", Region: %s' % (self.parent_tree_item.src_url, self.parent_tree_item.name)
		)

"""
DeparmentListParser: unfilled(Department) -> Department
	where:
	Department is (Fields and ServicesTree)
	unfilled(Department) is (Department source url and Deparmtent name)
"""

class BaseDepartmentParser(BaseParser):	
	#  table for replacement from tree_item field name to model field name
	fld_name_replacements = {
		'site': 'website',
		'district': 'county',
		'locality': 'district',
		'index': 'post_index',
		'mode': 'operating_mode',
		'address-ex': 'address_additional'
	}
	
	re_esqape_seqs = re.compile('^[\r\n\t]+$')
	
	def __init__(self, tree_item):
		self.tree_item = tree_item
		#super().__init__(tree_item)
		pass
		
	def parseFields(self, lxml_tree_data_table_fields):
		all_parsed = False
		
		for field in lxml_tree_data_table_fields:
			field_parsed = False
			    
			v_name = field.xpath('.//@id')
			v_value = field.xpath('.//text()')
			
			# simple fields
			if len(v_name) and v_name[0] in self.tree_item.simple_fields:
				#print('[SIMPLE] name: %s, value: %s' % (v_name[0], v_value[0]))
				self.tree_item.fields[self.replaceFieldName(v_name[0])] = str(v_value[0])
				
				field_parsed = True
				continue
			
			# array fields - site, phone, coverage, email
			if len(v_name) and v_name[0] in self.tree_item.array_fields:
				#print('[A_WEBSITE] name: %s, value: %s' % (v_name[0], v_value))
				v_value = list(filter(lambda s: not self.re_esqape_seqs.match(s), v_value))
				self.tree_item.fields[self.replaceFieldName(v_name[0])] = list(map(lambda v: str(v), v_value))
				
				field_parsed = True
				continue

			# mode
			if len(v_name) and v_name[0] == 'mode':
				value = ''.join(list(filter(lambda s: not self.re_esqape_seqs.match(s), v_value)))
				self.tree_item.fields[self.replaceFieldName(v_name[0])] = str(value)
				#print('[MODE] name: %s, value:\n>>>\n%s\n>>>' % (v_name[0], value))
				field_parsed = True
				continue
			
			if len(v_name) and v_name[0] == 'address':
				self.tree_item.fields[self.replaceFieldName(v_name[0])] = str(v_value[0])
				field_parsed = True
				continue

			# direction
			if len(v_name) and v_name[0] == 'offices-gu':
				a_url_field = field.xpath('.//*/a')
				av_value = a_url_field[0].xpath('.//text()')
				av_url = a_url_field[0].xpath('.//@href')
				
				self.tree_item.fields['direction'] = { 'name': str(av_value[0]), 'url': normalizeUrl(str(av_url[0])) }

				#print('[DIRECTION] url: %s, value:\n>>>\n%s\n>>>' % (av_url[0], v_value[0]))
				field_parsed = True
				continue

			if not field_parsed and  len(v_name):
				self.msgError('Field not parsed: %s, %s (%s)' % (v_name, v_value, self.tree_item.src_url))

	
	def parseServices(self, lxml_tree):
		lxml_tree_data_table_fld_services = lxml_tree.xpath('//table[@class = "data"]/tr/td[text()[contains(.,"Сервисы")]]/..')
		if not len(lxml_tree_data_table_fld_services):
			self.msgError('Could\'nt find data table services block')
			return

		svcs = lxml_tree_data_table_fld_services[0].xpath('.//td/div/div')
		
		for svc in svcs:
			svc_name = ''
			svc_url = ''

			# parse first level services without children ('ab-li' class)
			if svc.attrib.has_key('class') and 'ab-li' in svc.attrib['class']: # svc.xpath('.//[@class="ab-li"]'):
				svc_name = str(svc.xpath('./a/text()')[0])
				svc_url = str(svc.xpath('./a/@href')[0])

				svc_tree_item = ServiceTreeItem(svc_name, svc_url, [])
				self.tree_item.children.append(svc_tree_item)
				
				self.msgInfo("Parsed Service Tree Item: ")
				svc_tree_item.dump()
			# parse first level services with children (sibling of 'svc-list' class)
			else:
				svc_name = svc.xpath('./text()')
				svc_url = ''

				if not len(svc_name):
					continue

				svc_name = str(svc_name[0])
				svc_tree_item = ServiceTreeItem(svc_name, '', [])

				subservices = svc.xpath('following-sibling::*[@class="svc-list"]/div[@class="ab-li"]')
				for s_svc in subservices:
					s_svc_name = str(s_svc.xpath('./a/text()')[0])
					s_svc_url = str(s_svc.xpath('./a/@href')[0])
					
					s_svc_tree_item = ServiceTreeItem(s_svc_name, s_svc_url, [])
					svc_tree_item.children.append(s_svc_tree_item)
					
					self.msgInfo("Parsed Subervice Tree Item: ")
					s_svc_tree_item.dump()
					
				self.tree_item.children.append(svc_tree_item)
				
				self.msgInfo("Parsed Service Tree Item: ")
				svc_tree_item.dump()
		
		
	def exec(self):
#		try:
#			r = requests.get(self.tree_item.src_url, headers=self.headers, proxies=proxySettings())
#		except Exception as e:
#			self.msgError("Could'nt get HTTP response : %s" % str(e))
#			return False

		r = ProxySwitchRequest.request(requests.get, url=self.tree_item.src_url, headers=self.headers)
		
		lxml_tree = html.fromstring(r.text)
		lxml_tree_data_table_fields = lxml_tree.xpath('//table[@class = "data"]/tr/td[not(@class)]')
		
		self.parseFields(lxml_tree_data_table_fields)
		self.parseServices(lxml_tree)
		
		self.msgInfo("Parsed full data of Department Tree Item: ")
		self.tree_item.dump()
		
	def replaceFieldName(self, fld_name):
		return self.fld_name_replacements.get(fld_name, fld_name)


class BaseFullOneDeptTypeParser:
	def __init__(
		self,
		department_type_reglist_url = None,
		ClsRegionListParser = BaseRegionListParser, 	
		ClsDepartmentListParser = BaseDepartmentListParser,
		ClsDepartmentParser = BaseDepartmentParser
	):
		self.tree_root = TreeItem(nameFromUrl(department_type_reglist_url), department_type_reglist_url, [])
		
		self.ClsRegionListParser = ClsRegionListParser
		self.region_list_parser = ClsRegionListParser(self.tree_root)
		
		self.ClsDepartmentListParser = ClsDepartmentListParser
		self.ClsDepartmentParser = ClsDepartmentParser
		
	def exec(self):
		self.region_list_parser.exec()
		
		for region_tree_item in self.region_list_parser.parent_tree_item.children:
			department_list_parser = self.ClsDepartmentListParser(region_tree_item)
			department_list_parser.exec()
			
			for department_tree_item in department_list_parser.parent_tree_item.children:
				department_parser = self.ClsDepartmentParser(department_tree_item)
				department_parser.exec()
				
	def parsedTreeRoot(self):
		return self.region_list_parser.tree_item
	
