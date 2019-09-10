from sqlalchemy import create_engine, Column, Integer, String, Index
from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from src.model.base_department import Base
from sqlalchemy.orm import relationship
from config.main_config import DB_SETTINGS

#engine = create_engine('{engine}://{user}:{password}@{host}:{port}/{db_name}'.format(**DB_SETTINGS))

class TerritoryMixin(object):
	id =    Column(Integer, primary_key=True)
	name =  Column(String(512))
	
	#name =  Column(TEXT(512, charset='utf8'))

	def __init__(self, name):
		self.name = name
		
	def __repr__(self):
		return "<%s(name: '%s')>" % (cls.__name__, self.name)

	@declared_attr
	def __tablename__(cls):
		return cls.__name__.lower()
	
	@declared_attr
	def mfc_departments(cls):
		return relationship("MFC_Department", cascade='all, delete-orphan', back_populates="")

class Region(TerritoryMixin, Base):
	__table_args__ = (
		Index("name_idx", 'name', mysql_length=32, unique=True),
	)

class County(TerritoryMixin, Base):
	__table_args__ = (
		Index("name_idx", 'name', mysql_length=32, unique=True),
	)

class District(TerritoryMixin, Base):
	__table_args__ = (
		Index("name_idx", 'name', mysql_length=32, unique=True),
	)
