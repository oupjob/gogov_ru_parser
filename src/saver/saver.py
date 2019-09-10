from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import json

from src.model.base_department import *
from src.model.mfc_department import *
from src.model.services import *
from src.model.territory import *
from config.main_config import DB_SETTINGS


class BaseTreeSaver:	
	def __init__(self, 
		tree_root, 
		ClsModelDepartment
	):
		self.tree_root = tree_root
		self.engine = create_engine('{engine}://{user}:{password}@{host}:{port}/{db_name}'.format(**DB_SETTINGS))
		self.session = Session(self.engine)
		
		self.ClsModelDepartment = ClsModelDepartment
		self.region_saved_counter = 0
		self.deparment_saved_counter = 0
		
	def exec(self):
		for region_ti in self.tree_root.children:
			region = self.getOrCreateUniqueTerritory(Region, name=region_ti.name)
			region_has_parsed_departments = False
			
			for department_ti in region_ti.children:
				if not department_ti.fields:
					continue
				
				department = self.ClsModelDepartment(
					fullname 			= department_ti.fields.get('fullname', department_ti.name),
					shortname 			= department_ti.fields.get('shortname'),
					address 			= department_ti.fields.get('address'),
					address_additional 	= department_ti.fields.get('address_additional', ''),
					post_index 			= department_ti.fields.get('post_index'),
					ceo 				= department_ti.fields.get('ceo'),
					direction 			= department_ti.fields.get('direction', {}).get('name', ''),
					operating_mode 		= department_ti.fields.get('operating_mode'),
					website 			= json.dumps(department_ti.fields.get('website', []), ensure_ascii=False),
					email 				= json.dumps(department_ti.fields.get('email', []), ensure_ascii=False),
					phone 				= json.dumps(department_ti.fields.get('phone', []), ensure_ascii=False),
					coverage 			= json.dumps(department_ti.fields.get('coverage', []), ensure_ascii=False),
					region 				= region,
					county 				= self.getOrCreateUniqueTerritory(County, name=department_ti.fields.get('county', '')),
					district 			= self.getOrCreateUniqueTerritory(District, name=department_ti.fields.get('district', '')),
					source_url			= department_ti.src_url
				)
				
				self.saveServicesTree(department_ti, department)
				self.session.add(department)
				self.deparment_saved_counter += 1
				region_has_parsed_departments = True
			
			if region_has_parsed_departments:
				self.session.add(region)
			self.region_saved_counter += 1
			
		self.session.commit()
				
	def saveServicesTree(self, department_ti, department):
		def saveService(svc_ti, parent = None):
			service = self.session.query(Service).filter_by(name=svc_ti.name).first()
			if not service:
				service = Service(name=svc_ti.name, destination_url = svc_ti.destination_url, parent=parent)
				department.services.append(service)
				self.session.add(service)
			else:
				department.services.append(service)
			
			for c_ti in svc_ti.children:
				saveService(c_ti, service) 
			
		for svc_ti in department_ti.children:
			saveService(svc_ti)
			
	def getOrCreateUniqueTerritory(self, Type, name=''):
		territory = self.session.query(Type).filter_by(name=name).first()
		return Type(name=name) if not territory else territory


class TreeToJsonSaver:
	def __init__(self, tree_root, output_file):
		self.tree_root = tree_root
		self.output_file = output_file
		
	def exec(self):
		fh = open(self.output_file, 'w')
		
		name = self.tree_root.name.replace('"', '\\"')
		src_url = self.tree_root.src_url.replace('"', '\\"')
		fh.write('{ "name": "%s", "src_url": "%s", "children": \n[\n' % (name, src_url))
		
		i_region_ti = 0
		n_region_ti = len(self.tree_root.children) - 1
		for region_ti in self.tree_root.children:
			name = region_ti.name.replace('"', '\\"')
			src_url = region_ti.src_url.replace('"', '\\"')

			fh.write('\n\t{ "name": "%s", "src_url": "%s"' % (region_ti.name, region_ti.src_url))
			i_department_ti = 0
			n_department_ti = len(region_ti.children)
			if n_department_ti:
				 fh.write(', "children": \n\t[\n')
				 
			for department_ti in region_ti.children:
				name = department_ti.name.replace('"', '\\"')
				src_url = department_ti.src_url.replace('"', '\\"')
				
				fh.write('\n\t\t{ "name": "%s", "src_url": "%s", ' % (name, src_url))
				json_fields = json.dumps(department_ti.fields, ensure_ascii=False, indent=16)
				json_services = json.dumps([self.servicesTreeToDict(svc_ti) for svc_ti in department_ti.children], ensure_ascii=False, indent=16)

				json_fields = json_fields.replace('^\}','\t\t\t}')
				json_services = json_services.replace('^\]','\t\t\t]')
				
				fh.write('\n\t\t\t"fields": %s,\n\t\t\t"children": %s\n\t\t}' % (json_fields, json_services))
				
				if i_department_ti < n_department_ti - 1:
					fh.write(',')
				i_department_ti += 1
				
			fh.write('\n\t]}' if n_department_ti else '\n\t}')
			if i_region_ti < n_region_ti - 1:
				fh.write(',')
			i_region_ti += 1
		
		fh.write('\n]\n}')
		
	def servicesTreeToDict(self, svc_ti):
		#name = svc_ti.name.replace('"', '\\"')
		#src_url = svc_ti.src_url.replace('"', '\\"')
		json_svc = { "name": svc_ti.name, "destination_url": svc_ti.destination_url, 'children': [] }
		
		for s_svc in svc_ti.children:
			json_svc.children.append(self.servicesTreeToJson(s_svc))
				
		return json_svc
