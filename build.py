
import bs4
import os
import urllib.request
import zipfile
from types import ModuleType
from bs4 import BeautifulSoup
from bs4.element import Tag
from bs4.element import NavigableString
from os.path import join as join_path

WEBU_FILES_URL:str = "https://ebible.org/Scriptures/engwebu_usfx.zip"

def build(mod:ModuleType) -> None:
	if not os.path.exists("webu/engwebu_usfx.xml"):
		download(mod)
	if mod.doc == None:
		load(mod)
	
	lord_name_to_hebrew(mod)
	save(mod)

	print(" *  Done!")

def download(mod:ModuleType, folder:str="webu") -> None:
	"""Downloads the World English Version Updated USFX files to use as a template
	Use `load` to load the files into memory."""
	tmp_file_name ="webu_usfx.zip"
	tmp_file_path = join_path(folder, tmp_file_name)

	print(f"... Downloading WEBU translation to \"{tmp_file_path}\"")
	try:
		os.makedirs(folder) if not os.path.isdir(folder) else None
		urllib.request.urlretrieve(WEBU_FILES_URL, tmp_file_path)

		print("... Unzipping files")
		with zipfile.ZipFile(tmp_file_path, "r") as zip:
			zip.extractall(folder)
	finally:
		os.remove(tmp_file_path)


def save(mod:ModuleType, file_name:str="eng_sots_usfx.xml", folder:str="bin") -> None:
	"""Saves an edited translation file to the file system"""
	print(f"... Saving translation file to \"{file_name}\"")

	doc:BeautifulSoup = mod.doc
	os.makedirs(folder) if not os.path.isdir(folder) else None
	with open(join_path(folder, file_name), "w") as file:
		file.write(str(doc))

def load(mod:ModuleType, file:str="webu/engwebu_usfx.xml") -> None:
	"""Loads a translation file for building and editing"""
	if not os.path.exists(file):
		print(f" !  No file exists at \"{file}\"")
		return
	print(f"... Loading \"{file}\"")
	with open(file, "r") as f:
		mod.doc = BeautifulSoup(f, "xml")

def textify(mod:ModuleType, book:str="", chapter:int=-1, folder:str="bin") -> None:
	doc:BeautifulSoup = mod.doc
	book = book.upper()
	
	print(f"... Finding verses for {book}:{chapter}")
	start_verse = doc.find("v", bcv=f"{book}.{chapter}.1")

	print(f"... Assembling text")
	text = ""
	target = start_verse.next
	while True:
		if target == None:
			break
		elif target.name == "book":
			break

		elif target.name == "ve":
			pass
		elif target.name == "v":
			if not target.attrs["bcv"].startswith(f"{book}.{chapter}"):
				break

		elif target.name == "f":
			text += "^1"
			target = target.next_sibling
			continue

		elif isinstance(target, NavigableString):
			if target.string == "\n":
				pass
			else:
				text += target.string

		target = target.next

	text = text.strip()
	file_name = f"{book}{chapter}.txt"

	print(f"... Saving text to \"{file_name}\"")
	os.makedirs(folder) if not os.path.isdir(folder) else None
	with open(join_path(folder, file_name), "w") as f:
		f.write(text)


def lord_name_to_hebrew(mod:ModuleType) -> None:
	print(f"... Finding instances of \"LORD\"")

	doc:BeautifulSoup = mod.doc
	words_lord:list[Tag] = doc.find_all("w", text="LORD")

	print(f"... Changing {len(words_lord)} instance(s) of \"LORD\" to \"יהוה\"")

	# Change instances of LORD to יהוה
	for word_lord in words_lord:
		pre_word = word_lord.find_previous_sibling()
		if pre_word != None and pre_word.text.lower() == "the":
			pre_word.decompose()
		word_lord.string = "יהוה"
	
	# Change footnotes referring to LORD
	ft_list:list[Tag] = doc.find_all("fr", text="LORD or GOD in all caps")
	for ft in words_lord:
		ft = "The name of God. TODO: Better note."

	
