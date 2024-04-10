
import sys
import readline

from bs4 import BeautifulSoup
from hotreload import Loader

doc:BeautifulSoup|None = None

def main():
	global doc

	script = Loader("build.py")

	script.load(sys.modules[__name__])

	while True:
		got = input("SOTS Builder > ").lower()
		if " " in got:
			args = got.split("")
		else:
			args = [got]

		if args[0] == "exit":
			return

		try:
			func = script.__getattr__(args[0])
			func(sys.modules[__name__])
		except KeyboardInterrupt as e:
			print(f"	KeyboardInterrupt")
		except Exception as e:
			print(f"	Unexpected error: {e}")
		

if __name__ == "__main__":
	main()


