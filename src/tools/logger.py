import logging
import datetime
from config.main_config import LOG_DIR, LOG_NAME_FORMAT

def main():
	log_filename = '%s/%s.log' % (LOG_DIR, datetime.datetime.today().strftime(LOG_NAME_FORMAT))
	logging.basicConfig(filename=log_filename, level=logging.CRITICAL)
	
	#logger = logging.getLogger('gogov_ru_parser')
	#logger.setLevel(logging.CRITICAL)

	## create the logging file handler
	#fh = logging.FileHandler('%s/%s.log' % (LOG_DIR, datetime.datetime.today().strftime(LOG_NAME_FORMAT)))

	#formatter = logging.Formatter('%(name)s : %(levelname)s : %(message)s')
	#fh.setFormatter(formatter)

	## add handler to logger object
	#logger.addHandler(fh)
	
if __name__ == "__main__":
    main()
