from src.saver.saver import *
from src.parser.parser import *
from src.model.departments import *

root_ti = TreeItem(src_url='https://gogov.ru/gibdd', name='ГИБДД', children=[])

region_ti = TreeItem(src_url='https://gogov.ru/msk/gibdd', name='Москва', children=[])
root_ti.children.append(region_ti)

region_ti.children.append(
	DepartmentTreeItem(
		src_url='https://gogov.ru/gibdd/msk/g667019', 
		name='Отделение регистрации МО ГИБДД ТНРЭР № 5 ГУ МВД России по городу Москве',
		children=[]
	)
)
region_ti.children.append(
	DepartmentTreeItem(
		src_url='https://gogov.ru/gibdd/msk/g667021', 
		name='ОР МО ГИБДД ТНРЭР № 5 ГУ МВД России по городу Москве',
		children=[]
	)
)

parser = BaseDepartmentParser(region_ti.children[0])
parser.exec()

parser = BaseDepartmentParser(region_ti.children[1])
parser.exec()

root_ti.dump()

saver = BaseTreeSaver(root_ti, MFC_Department)
saver.exec()
