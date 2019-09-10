import json

from src.parser.parser import *
from src.tools.proxy_switcher import *
""" 
BaseParsingMapCreator - class provides parsing map file collecting
Parsing map - is a tree of items with base information for full parsing
at this tree. Department Tree Items not contains fields and services
This tree must be saved into file.

"""	
class BaseParsingMapCreator:
	def __init__(
		self,
		output_file = '',
		url = None,
		ClsRegionListParser = BaseRegionListParser, 	
		ClsDepartmentListParser = BaseDepartmentListParser
	):
		self.tree_root = TreeItem(nameFromUrl(url), url, [])
		self.output_file = output_file
		
		self.ClsRegionListParser = ClsRegionListParser
		self.region_list_parser = ClsRegionListParser(self.tree_root)
		
		self.ClsDepartmentListParser = ClsDepartmentListParser
		
	def exec(self):
		try:
			self.region_list_parser.exec()
			
			for region_tree_item in self.region_list_parser.parent_tree_item.children:
				department_list_parser = self.ClsDepartmentListParser(region_tree_item)
				department_list_parser.exec()
				
			self.saveParsingMap()
		except ProxyListOverException as e:
			answer = input(e.message + "\nSave result? (y\\n) > ")
			if (answer == 'y'):
				self.saveParsingMap()
			
		
	def saveParsingMap(self):
		fh = open(self.output_file, 'w')
				
		name = self.tree_root.name.replace('"', '\\"')
		src_url = self.tree_root.src_url.replace('"', '\\"')
		fh.write('{ "name": "%s", "src_url": "%s", "children": \n[\n' % (name, src_url))
		
		i_region_ti = 0
		n_region_ti = len(self.tree_root.children) - 1
		for region_ti in self.tree_root.children:
			name = region_ti.name.replace('"', '\\"')
			src_url = region_ti.src_url.replace('"', '\\"')
			
			fh.write('\n\t{ "name": "%s", "src_url": "%s", "children": \n\t[\n' % (name, src_url))
			i_department_ti = 0
			n_department_ti = len(region_ti.children)
			for department_ti in region_ti.children:
				name = department_ti.name.replace('"', '\\"')
				src_url = department_ti.src_url.replace('"', '\\"')
			
				fh.write('\n\t\t"{ "name": "%s", "src_url": "%s" }' % (name, src_url))
				if i_department_ti < n_department_ti - 1:
					fh.write(',')
				i_department_ti += 1
				
			fh.write('\n\t]}')
			if i_region_ti < n_region_ti - 1:
				fh.write(',')
			i_region_ti += 1
		
		fh.write('\n]\n}')
		
""" 
BaseParsingMapCreator - class provides parsing departments from parsing map
Parsing map - is a tree of items with base information for full parsing
at this tree. Department Tree Items not contains fields and services
This tree must be saved into file.

"""	
		
class BaseParsingMapBasedParser:
	def __init__(
		self,
		input_file,
		ClsDepartmentParser = 		BaseDepartmentParser
	):
		self.tree_root = None
		self.input_file = input_file
		self.dict_tree = None
		self.ClsDepartmentParser = ClsDepartmentParser
		
		self.readParsingMap()
		
	def readParsingMap(self):
		fh = open(self.input_file, 'r')
		json_dt_dict = json.load(fh)
		
		self.tree_root = TreeItem(json_dt_dict.get('name'), json_dt_dict.get('src_url'), [])
		for region in json_dt_dict['children']:
			region_ti = TreeItem(region.get('name'), region.get('src_url'), [])
			self.tree_root.children.append(region_ti)
			
			for department in region.get('children', []):
				department_ti = DepartmentTreeItem(department.get('name'), department.get('src_url'), {}, [])
				region_ti.children.append(department_ti)

	def exec(self):
		self.msgInfo('Starting: parsing map based parsing region list from URL: "%s"' % (self.tree_root.src_url))
	
		for region_tree_item in self.tree_root.children:
			self.msgInfo(
				'Starting: parsing map based department list parsing from URL: "%s", Region: "%s"' 
				% (self.tree_root.src_url, self.tree_root.name)
			)
			
			for department_tree_item in region_tree_item.children:
				department_parser = self.ClsDepartmentParser(department_tree_item)
				department_parser.exec()

	def msgInfo(self, message):
		print('%s: %s' % (self.__class__.__name__, message))

	def msgError(self, message):
		print('ERROR: %s: %s' % (self.__class__.__name__, message))
