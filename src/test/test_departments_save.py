import sys
from src.parser.parser import *
from sqlalchemy.orm import sessionmaker
import json

from src.parser.parser import BaseFullOneDeptTypeParser
from config.main_config import *
from src.model.departments import *
from src.model.services import *
from src.model.territory import *

class TestDepartmentsSave:
	def __init__(self, url_list):
		self.url_list = url_list
		self.engine = create_engine('{engine}://{user}:{password}@{host}:{port}/{db_name}'.format(**DB_SETTINGS))
		Session = sessionmaker(bind=self.engine)
		self.session = Session()

	
	def saveServicesTree(self, department_ti, department):
		def saveService(svc_ti, parent = None):
			service = self.session.query(Service).filter_by(name=svc_ti.name).first()
			if not service:
				service = Service(name=svc_ti.name, destination_url = svc_ti.destination_url, parent=parent)
				department.services.append(service)
				self.session.add(service)
				
				print("new %s -> %s" % (department.shortname, service.name))
			else:
				print("exists %s -> %s" % (department.shortname, service.name))
				department.services.append(service)
			
			for c_ti in svc_ti.children:
				saveService(c_ti, service) 
			
		for svc_ti in department_ti.children:
			saveService(svc_ti)

	def get_or_create_unique_territory(self, Type, name=''):
		territory = self.session.query(Type).filter_by(name=name).first()
		return Type(name=name) if not territory else territory

	def saveDepartment(self, url):
		dept_tree_item = DepartmentTreeItem('', url)
		
		department_parser = BaseDepartmentParser(dept_tree_item)
		department_parser.exec()
		department_parser.tree_item.dump(print_fn=print)
		
		deparment = MFC_Department(
			fullname = department_parser.tree_item.fields.get('fullname'),
			shortname = department_parser.tree_item.fields.get('shortname'),
			address = department_parser.tree_item.fields.get('address'),
			post_index = department_parser.tree_item.fields.get('post_index'),
			ceo = department_parser.tree_item.fields.get('ceo'),
			direction = department_parser.tree_item.fields.get('direction', {}).get('name', ''),
			operating_mode = department_parser.tree_item.fields.get('operating_mode'),
			website = json.dumps(department_parser.tree_item.fields.get('website', []), ensure_ascii=False),
			email = json.dumps(department_parser.tree_item.fields.get('email', []), ensure_ascii=False),
			phone = json.dumps(department_parser.tree_item.fields.get('phone', []), ensure_ascii=False),
			coverage = json.dumps(department_parser.tree_item.fields.get('coverage', []), ensure_ascii=False),
			region = self.get_or_create_unique_territory(Region, name='Москва'),
			county = self.get_or_create_unique_territory(County, name=department_parser.tree_item.fields.get('county', '')),
			district =  self.get_or_create_unique_territory(District, name=department_parser.tree_item.fields.get('district', ''))
		)

		self.saveServicesTree(dept_tree_item, deparment)
		self.session.add(deparment)
		
	
	def exec(self):
		for url in self.url_list:
			self.saveDepartment(url)
		
		self.session.commit()
		self.session.close()
		
url_list = sys.argv[1:]
test_departments_save = TestDepartmentsSave(url_list)
test_departments_save.exec()
