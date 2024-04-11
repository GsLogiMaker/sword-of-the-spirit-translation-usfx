
import sys
import readline # Adds up arrow handling to input() (not unused)

from bs4 import BeautifulSoup
from hotreload import Loader

doc:BeautifulSoup|None = None

def main():
	global doc

	script = Loader("build.py")

	while True:
		got = input("SOTS Builder > ").lower()
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


