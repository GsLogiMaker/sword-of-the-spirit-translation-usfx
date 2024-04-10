
import bs4
from types import ModuleType
from bs4 import BeautifulSoup

def build(mod:ModuleType) -> None:
	lord_name_to_hebrew(mod)
	save(mod)

	print("*   Done!")

def save(mod:ModuleType) -> None:
	print("... Saving translation file to \"out.xml\"")

	doc:BeautifulSoup = mod.doc
	with open("out.xml", "w") as file:
		file.write(str(doc))

def load(mod:ModuleType) -> None:
	print("... Loading \"eng_sots_usfx\"")
	with open("eng_sots_usfx.xml", "r") as f:
		mod.doc = BeautifulSoup(f, "xml")

def lord_name_to_hebrew(mod:ModuleType) -> None:
	print(f"... Finding instances of \"LORD\"")

	doc:BeautifulSoup = mod.doc
	words_lord:list[bs4.element.Tag] = doc.find_all("w", text="LORD")

	print(f"... Changing {len(words_lord)} instance(s) of \"LORD\" to \"יהוה\"")

	# Change instances of LORD to יהוה
	for word_lord in words_lord:
		pre_word = word_lord.find_previous_sibling()
		if pre_word != None and pre_word.text.lower() == "the":
			pre_word.decompose()
		word_lord.string = "יהוה"
	
	# Change footnotes referring to LORD
	ft_list:list[bs4.element.Tag] = doc.find_all("fr", text="LORD or GOD in all caps")
	for ft in words_lord:
		ft = "The name of God. TODO: Better note."

	
