import re
from requests.exceptions import ConnectionError

from config.main_config import HTTPS_PROXY_LIST_FILE, USERAGENT_LIST_FILE, ROOT_URL

class ProxyListOverException(Exception):
	def __init__(self, message):
		self.message = message


class ProxySwitchRequest:
	i_proxy = 0
	i_useragent = 0
	proxy_count = 0
	useragent_count = 0
	CONNECT_ATTEMPT_MAX = 2
	
	re_captcha = re.compile('recaptcha')
	https_proxy_list = []
	useragent_list = []
	
	@classmethod
	def readConfig(cls):
		cls.https_proxy_list = [line.rstrip('\n') for line in open(HTTPS_PROXY_LIST_FILE, 'r')]
		cls.proxy_count = len(cls.https_proxy_list)
		cls.useragent_list = [line.rstrip('\n') for line in open(USERAGENT_LIST_FILE, 'r')]
		cls.useragent_count = len(cls.useragent_list) 
	
	@classmethod
	def request(cls, requests_method, **kwargs):
		if not kwargs.get('proxies', None) and cls.https_proxy_list:
			kwargs['proxies'] = { 'https': cls.https_proxy_list[cls.i_proxy] }
			
		if not kwargs.get('timeout', 0):
			kwargs['timeout'] = (4, 4)

		def switchNext(reason=''):
			cls.i_proxy += 1
			if cls.i_proxy >= cls.proxy_count:
				raise ProxyListOverException('ProxySwitchRequest: Proxy list is over')
			
			cls.i_useragent += 1
			if cls.i_useragent >= cls.useragent_count:
				cls.i_useragent = 0
			
			if kwargs.get('headers', None):
				kwargs['headers']['User-Agent'] = cls.useragent_list[cls.i_useragent]
			if kwargs.get('proxies', None) and cls.https_proxy_list:
				kwargs['proxies']['https'] = cls.https_proxy_list[cls.i_proxy]
			
			print('ProxySwitchRequest: switched to %d\'s proxy: %s (Reason: %s)' % (cls.i_proxy, cls.https_proxy_list[cls.i_proxy], reason))
		
		connect_attempt = 0
		while True:
			try:
				r = requests_method(**kwargs)
			except:
				if connect_attempt < cls.CONNECT_ATTEMPT_MAX:
					connect_attempt += 1
				else:
					connect_attempt = 0
					switchNext('Bad proxy')
				
				continue
			
			connect_attempt = 0
			if cls.re_captcha.search(r.text):
				switchNext('Capthca')
				continue
			
			return r
			

	@classmethod
	def currentHttpsProxy(cls):
		return cls.https_proxy_list[cls.i_proxy]
	
	@classmethod
	def currentUserAgent(cls):
		return cls.useragent_list[cls.i_useragent]
				
				
ProxySwitchRequest.readConfig()
