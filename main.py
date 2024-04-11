
import sys
import readline # Adds up arrow handling to input() (not unused)

from bs4 import BeautifulSoup
from hotreload import Loader

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

doc:BeautifulSoup|None = None

def main():
	global doc

	script = Loader("build.py")

	while True:
		got = input(f"{bcolors.OKCYAN}SOTS Builder > {bcolors.ENDC}").lower()
		args = got.split(" ")
		command = args.pop(0)

		if command == "exit":
			return
		elif command == "":
			continue

		try:
			func = script.__getattr__(command)
			func(sys.modules[__name__], *args)
		except KeyboardInterrupt as e:
			print(f" !  KeyboardInterrupt")
		except Exception as e:
			print(f" !  {e}")
		

if __name__ == "__main__":
	main()


