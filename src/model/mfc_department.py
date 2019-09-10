from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.model.base_department import DepartmentMixin, Base
from src.model.services import Service
# from src.model.services import Department2ServiceMixin

#MFC_department2service = Table(
	#'MFC_department2service', 
	#Base.metadata,
    #Column('department_id', Integer, ForeignKey('MFC_department.id')),
    #Column('service_id', Integer, ForeignKey('service.id'))
#)


#class MFC_Department(DepartmentMixin, Base):
	#__tablename__ = 'MFC_department'
	#services = relationship("Service", secondary=MFC_department2service, back_populates="children")
	
	#def __init__(**kwargs):
		#DepartmentMixin.__init__(**kwargs)
		
	
#class MFC_DepartmentOneToManyFldMixin(object):
	#department_id = Column(Integer, ForeignKey('MFC_department.id'))
	
	#def __init__(self, department):
		#self.department = department
	
	#@declared_attr
	#def __tablename__(cls):
		#return cls.__name__.lower()

	#@declared_attr
	#def department(cls):
		#return relationship('MFC_Department')
	

#class MFC_Email(Base):
	#id =			Column(Integer, primary_key=True)
	#email =			Column(String(256))
	
	#def __init__(self, email, department):
		#super().__init__(department)
		#self.email = email


#class MFC_Website(Base):
	#id =			Column(Integer, primary_key=True)
	#website =		Column(String(256))
	
	#def __init__(self, website, department):
		#super().__init__(department)
		#self.website = website


#class MFC_Phone(Base):
	#id =			Column(Integer, primary_key=True)
	#phone =			Column(String(256))
	
	#def __init__(self, phone, department):
		#super().__init__(department)
		#self.phone = phone


#class MFC_Department2Service(Department2ServiceMixin, Base):
	#__tablename__ = 'MFC_department2service'
	
	#department_id = Column(Integer, ForeignKey('department.id'))
	
	#@declared_attr
	#def department_id(cls):
		#return relationship("MFC_Department")

