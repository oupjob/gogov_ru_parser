import sys
import datetime
import json

from src.tools.proxy_switcher import ProxySwitchRequest

from src.model.departments import *
from src.parser.parser import BaseFullOneDeptTypeParser
from src.saver.saver import *
from src.parser.parsing_mapper import *
from config.main_config import *

help_usage = """
USAGE COMANDS: 
	parser.py [full|create_parsingmap|from_parsingmap|help] [--url https://gogov.ru/dept_type/region][-o|-i /path/to/parsing_map --json result_file]
	
	parser.py full --url https://gogov.ru/dept_type/region [--json result_file]
		parse full tree without creating parsing parsing_map and save results
		
	parser.py create_parsingmap --url https://gogov.ru/dept_type/region -o /path/to/parsing_map
		parse base tree of departments by regions of type given by --url parameter
		 -- url - department type region list url
		 -o - output parsing map file
		 
	parser.py from_parsingmap -i /path/to/parsing_map [--json result_file]
		parse full tree from parsing map file
		-i - input parsing map file
		
	parser.py help - show this message
	
OPTIONS:
	--json result_file - this option goes parser to save results to `result_file` json file instead database
"""

def dumpSettings():
	print('\nDatabase settings:\n%s' % json.dumps(DB_SETTINGS, indent=4))
	n = len(ProxySwitchRequest.https_proxy_list)
	if n < 26:
		print('\nHTTPS Proxy List:\n%s' % json.dumps(ProxySwitchRequest.https_proxy_list, indent=4)) 
	else:
		print('\nHTTPS Proxy contains %d proxies' % n)
		
	print('\nUseragent List:\n%s' % json.dumps(ProxySwitchRequest.useragent_list, indent=4)) 
	
def getPassedJsonOutputFile():
	index = -1
	try:
		index = sys.argv.index('--json')
		return sys.argv[index + 1] if len(sys.argv) >= index + 2 else None
	except:
		return None


if len(sys.argv) < 2:
	print(help_usage)

if sys.argv[1] == 'full':
	url = ''
	if sys.argv[2] == '--url' and len(sys.argv) >= 4:
		url = sys.argv[3]
	else:
		print(help_usage)
		exit()
		
		
	print("Starting gogov.ru Full parsing, base dpartmemt type (region list) URL: %s" % url)
	dumpSettings()
	
	json_output_file = getPassedJsonOutputFile()
	if json_output_file:
		saver = TreeToJsonSaver(pm_based_parser.tree_root, json_output_file)
	else:
		saver = BaseTreeSaver(pm_based_parser.tree_root, MFC_Department)
	
	try:
		one_dept_type_parser = BaseFullOneDeptTypeParser(department_type_reglist_url=url)
		one_dept_type_parser.exec()
	except ProxyListOverException as e:
		answer = input(e.message + "\nSave result? (y\\n) > ")
		if (answer == 'y'):
			saver.exec()

		saver.exec()
	
elif sys.argv[1] == 'create_parsingmap':
	url = ''
	output_file = ''
	
	if  len(sys.argv) >= 6:
		if sys.argv[2] == '--url':
			url = sys.argv[3]
			if sys.argv[4] == '-o':
				output_file = sys.argv[5]
			else:
				print(help_usage)
			
		elif sys.argv[2] == '-o':
			output_file = sys.argv[3]
			if sys.argv[4] == '--url':
				url = sys.argv[5]
			else:
				print(help_usage)
				exit()
		else:
			print(help_usage)
			exit()
			
		print("Starting gogov.ru parsing map building, base dpartmemt type (region list) URL: %s" % url)
		dumpSettings()
		
		parsing_map_creator = BaseParsingMapCreator(output_file=output_file, url=url)
		parsing_map_creator.exec()
		
	else:
		print(help_usage)
		exit()

elif sys.argv[1] == 'from_parsingmap':
	input_file = ''
	if sys.argv[2] == '-i' and len(sys.argv) >= 4:
		input_file = sys.argv[3]
		
		pm_based_parser = BaseParsingMapBasedParser(input_file, BaseDepartmentParser)
		
		json_output_file = getPassedJsonOutputFile()
		if json_output_file:
			saver = TreeToJsonSaver(pm_based_parser.tree_root, json_output_file)
		else:
			saver = BaseTreeSaver(pm_based_parser.tree_root, MFC_Department)
			
		print("Starting gogov.ru parsing map based parsing, base dpartmemt type (region list) URL: %s" % pm_based_parser.tree_root.src_url)
		dumpSettings()
		
		try:
			pm_based_parser.exec()
		except ProxyListOverException as e:
			answer = input(e.message + "\nSave result? (y\\n) > ")
			if (answer == 'y'):
				saver.exec()
			saver.exec()
		
		saver.exec()
		
	else:
		print(help_usage)
		exit()
		
else:
	print(help_usage)
