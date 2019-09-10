from config.main_config import DB_SETTINGS
from src.model import departments, territory, services, base_department
from src.model.base_department import Base
from sqlalchemy import create_engine

# engine = create_engine('{engine}://{user}:{password}@{host}:{port}/{db_name}'.format(**DB_SETTINGS))
engine = create_engine('{engine}://{user}:{password}@{host}:{port}'.format(**DB_SETTINGS))
conn = engine.connect()
conn.execute('commit')
conn.execute("drop database if exists %s;" % DB_SETTINGS['db_name'])
conn.execute("create database %s;" % DB_SETTINGS['db_name'])
conn.close()

engine = create_engine('{engine}://{user}:{password}@{host}:{port}/{db_name}'.format(**DB_SETTINGS))
conn = engine.connect()

#Base.metadata.create_all(engine)

#base_department.Email.metadata.create_all(engine)
#base_department.Phone.metadata.create_all(engine)
#base_department.Website.metadata.create_all(engine)
#mfc_department.MFC_Department2Service.metadata.create_all(engine)

territory.Region.metadata.create_all(engine)
territory.County.metadata.create_all(engine)
territory.District.metadata.create_all(engine)

services.Service.metadata.create_all(engine)

departments.MFC_Department.metadata.create_all(engine)


conn.close()

