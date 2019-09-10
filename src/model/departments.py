from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.model.base_department import DepartmentMixin, Base
from src.model.services import Service
# from src.model.services import Department2ServiceMixin

MFC_department2service = Table(
	'MFC_department2service', 
	Base.metadata,
    Column('department_id', Integer, ForeignKey('MFC_department.id', ondelete='cascade')),
    Column('service_id', Integer, ForeignKey('service.id', ondelete='cascade'))
)


class MFC_Department(DepartmentMixin, Base):
	__tablename__ = 'MFC_department'
	services = relationship(
		"Service", 
		secondary=MFC_department2service, 
		#cascade='save-update, merge, delete', 
		back_populates="mfc_departments"
	)
	
	#def __init__(self, **kwargs):
		#DepartmentMixin.__init__(self, **kwargs)


