from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from config.main_config import db_settings

class DepartmentMixin(object):
    id =                Column(Integer(32), primary_key=True)
    gogov_url =         Column(String(2048))
    full_name =         Column(String(4096))
    region =            Column(Integer(32), ForeignKey('region.id'))
    county =            Column(Integer(32), ForeignKey('county.id'))
    distinct =          Column(Integer(32), ForeignKey('distinct.id'))
    email =             Column(String(1024))
    address =           Column(String(4096))
    post_index =        Column(String(16))
    operating_mode =    Column(String(4096))
    website =           Column(String(256))
    
    def __init__(
        self,
        gogov_url,
        full_name,
        region,
        county,
        distinct,
        email,
        address,
        post_index,
        operating_mode,
        website,
    ):
        self.gogov_url =    gogov_url
        self.full_name =    full_name
        self.region =       region
        self.county =       county
        self.distinct =     distinct
        self.email =        email
        self.address =      address
        self.post_index =   post_index
        self.operating_mode = operating_mode
        self.website =      website
        
    def __repr__(self):
        return "<BaseDepartment(name: '%s',gogov_url: '%s')>" % (self.full_name, self.gogov_url)
    

