import sys
from src.parser.parser import BaseFullOneDeptTypeParser

url = sys.argv[1]

one_dept_type_parser = BaseFullOneDeptTypeParser(url)
one_dept_type_parser.exec()

logg
one_dept_type_parser.tree_root.dump(print_fn=logging.info)

saver = BaseTreeSaver(root_ti, MFC_Department)
saver.exec()
