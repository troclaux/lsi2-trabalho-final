import logging
import sys

# log wrapper class
# use f-strings for formatted messages
# i.e. f'hello {name}'
class Log:

	myLogger = logging.getLogger(__name__)

	@staticmethod
	def Configure() -> None:
		handler = logging.StreamHandler(sys.stdout)
		formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
		handler.setFormatter(formatter)
		Log.myLogger.addHandler(handler)
		Log.myLogger.setLevel(logging.DEBUG)

	@staticmethod
	def Info(message: str) -> None:
		Log.myLogger.info(message)

	@staticmethod
	def Debug(message: str) -> None:
		Log.myLogger.debug(message)

	@staticmethod
	def Error(message: str) -> None:
		Log.myLogger.error(message, exc_info=True)

	@staticmethod
	def Warning(message: str) -> None:
		Log.myLogger.warning(message)

	@staticmethod
	def Critical(message: str) -> None:
		Log.myLogger.critical(message, exc_info=True)
