from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship

#engine = create_engine('mysql://{user}:{password}@{host}:{port}/{db_name}'.format(**DB_SETTINGS))
Base = declarative_base()

class DepartmentMixin(object):
	id =					Column(Integer, primary_key=True)
	fullname =	    		Column(String(1500))
	shortname =				Column(String(2048))
	ceo =					Column(String(128))
	direction =				Column(String(1500))
	address =				Column(String(1500))
	address_additional = 	Column(String(1500))
	post_index =			Column(String(16))
	operating_mode = 		Column(String(1500))
	email =					Column(String(1500)) # Column(JSON) # 
	phone = 				Column(String(1500)) # Column(JSON)
	website = 				Column(String(1500)) # Column(JSON)
	coverage = 				Column(String(1500)) # Column(JSON)
	source_url = 			Column(String(256))
	
	#id =					Column(Integer, primary_key=True)
	#fullname =	    		Column(TEXT(charset='utf8'))
	#shortname =				Column(TEXT(charset='utf8'))
	#ceo =					Column(TEXT(charset='utf8'))
	#direction =				Column(TEXT(charset='utf8'))
	#address =				Column(TEXT(charset='utf8'))
	#address_additional = 	Column(TEXT(charset='utf8'))
	#post_index =			Column(TEXT(charset='utf8'))
	#operating_mode = 		Column(TEXT(charset='utf8'))
	#email =					Column(TEXT(charset='utf8')) # Column(JSON) # 
	#phone = 				Column(TEXT(charset='utf8')) # Column(JSON)
	#website = 				Column(TEXT(charset='utf8')) # Column(JSON)
	#coverage = 				Column(TEXT(charset='utf8')) # Column(JSON)
	#source_url = 			Column(TEXT(charset='utf8'))
	   
	def __repr__(self):
		return "<%s(name: '%s', gogov_url: '%s')>" % (cls.__name__, self.fullname, self.gogov_url)
    
	@declared_attr
	def __tablename__(cls):
		return cls.__name__.lower()
	
	@declared_attr
	def region_id(cls):
		return Column(Integer, ForeignKey('region.id', ondelete='set null'))

	@declared_attr
	def county_id(cls):
		return Column(Integer, ForeignKey('county.id', ondelete='set null'))

	@declared_attr
	def district_id(cls):
		return Column(Integer, ForeignKey('district.id', ondelete='set null'))
	
	@declared_attr
	def region(cls):
		return relationship("Region")

	@declared_attr
	def county(cls):
		return relationship("County")

	@declared_attr
	def district(cls):
		return relationship("District")
	
	#@declared_attr
	#def email(cls):
		#return relationship("Email")
	
	#@declared_attr
	#def phone(cls):
		#return relationship("Phone")
	
	#@declared_attr
	#def website(cls):
		#return relationship("Website")
