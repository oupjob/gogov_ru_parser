DB_SETTINGS = {
	'engine': 'mysql+mysqlconnector',
	'user': 'admin',
	'host': 'localhost',
	'port': '3306',
	'password': 'multiC',
	'db_name': 'gogov_ru'
}

#USER_AGENTS = [
	#'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',
	#'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36',
	#'Mozilla/5.0 (Linux; Android 6.0.1; SM-G935S Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36',
	#'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36',
#]



## only HTTPS proxy
#HTTPS_PROXY_LIST = [
	#'165.22.108.166:3128',
	#'119.161.78.100:3128',
	#'195.122.185.95:3128',
	#'107.191.45.149:8156'
#]

# root site url
ROOT_URL = 'https://gogov.ru'

import os
PROJ_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_DIR = PROJ_ROOT + '/logs'
LOG_NAME_FORMAT = '%Y-%m-%d-%H.%M.%S'

HTTPS_PROXY_LIST_FILE = PROJ_ROOT + '/https_proxy_list.txt'
USERAGENT_LIST_FILE = PROJ_ROOT + '/useragent_list.txt'



