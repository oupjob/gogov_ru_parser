from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey, Index
from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship, backref
from config.main_config import DB_SETTINGS
from src.model.base_department import DepartmentMixin, Base

#engine = create_engine('{engine}://{user}:{password}@{host}:{port}/{db_name}'.format(**DB_SETTINGS))
# Base = declarative_base()

class Service(Base):
	__tablename__ = 'service'
	__table_args__ = (
		Index("name_idx", 'name', mysql_length=32, unique=True),
	)

	id =    				Column(Integer, primary_key=True) 
	destination_url =		Column(String(512)) 
	name =  				Column(String(256))
	#destination_url =		Column(TEXT(charset='utf8')) 
	#name =  				Column(TEXT(charset='utf8'))
	parent_id = 			Column(Integer, ForeignKey('service.id', ondelete='cascade'))
	children = 				relationship('Service', cascade='all, delete', backref=backref("parent", remote_side=id))
	
	mfc_departments = 		relationship(
#		"MFC_Department", secondary="MFC_department2service", cascade='save-update, merge, delete', back_populates="services"
		"MFC_Department", secondary="MFC_department2service", back_populates="services"
	)
	
	def __init__(self, name, destination_url, parent):
		self.name = name
		self.destionation_url = destination_url
		self.parent = parent
        
	def __repr__(self):
		return "<%s(name: '%s', url: '%s')>" % (cls.__name__, self.name, self.url)

	@declared_attr
	def __tablename__(cls):
		return cls.__name__.lower()

#class Department2ServiceMixin(object):
##    department_id = Column(Integer, ForeignKey('department.id'))
	#id =    		Column(Integer, primary_key=True)
	#service_id =    Column(Integer, ForeignKey('service.id'))

	#def __init__(self, department_id, service_id):
		#self.department_id = department_id
		#self.service_id = service_id
		
	#@declared_attr
	#def __tablename__(cls):
		#return cls.__name__.lower()
	
	#@declared_attr
	#def service_id(cls):
		#return relationship("Service")
