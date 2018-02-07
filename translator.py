import re
import fileinput
import shutil

from googletrans import Translator
from bs4 import BeautifulSoup
from optparse import OptionParser

global bs
global translator

def cleanlxml(raw_lxml):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_lxml)
  return re.split("[,]", cleantext)

def getWordsToTranslateFromTag(tag):
    to_translate = cleanlxml(str(bs.findAll("source")))
    return to_translate

def generateTranslatedTag(to_translate, translations_id, missing_ids, lang):
    translated = []
    for i in range(len(to_translate)):
        if translations_id[i] in missing_ids:
            translated.append("""<target state="translated">{0}</target>""".format(translator.translate(to_translate[i], dest=lang).text))
        else:
            translated.append("")
    return translated

def getTranslationIds(translations):
    ids = []
    for i in range(len(translations)):
        ids.append((bs.find_all('trans-unit'))[i]['id'])
    return ids

def getMissingTranslations(ids):
    modify_ids = []
    for i in ids:
        trans = (bs.find_all("trans-unit", id=i))
        tar = trans[0].find_all('target')
        if not tar:
            modify_ids.append(i)
    return modify_ids

def writeTranslatedTags(source_file, words_translated, missing_ids, translations_id):
    i = 0
    for line in fileinput.FileInput(source_file,inplace=1):
        if "<source>" in line:
            if translations_id[i] in missing_ids:
                line=line.replace(line,line+str(words_translated[i]))
            i += 1
        print(line, end='')

def main():
    global bs
    global translator

    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename", help="write translation from FILE", metavar="FILE")
    parser.add_option("-t", "--to", dest="output", help="write translation to FILE", metavar="FILE")
    parser.add_option("-l", "--lang", dest="language", help="select language to translate", metavar="LANG")

    (options, args) = parser.parse_args()

    if ((options.filename == None or options.language == None)):
        print ("""Wrong parameters, example usage: python translate.py -f messages.xlf -l de""")
        exit(0)

    shutil.copy2('options.filename', 'src/assets/locale/' + str(options.output)))

    translator = Translator()
    source_file = options.output
    lang = options.language
    format_file = "lxml"
    tag = "source"

    bs = BeautifulSoup(open(source_file, "r").read(), format_file)
    translations = (bs.find_all('trans-unit'))
    print ("Number of translations: {0}".format(len(translations)))
    translations_id = getTranslationIds(translations)
    print ("Number of ids to translate: {0}".format(len(translations_id)))

    words_to_translate = getWordsToTranslateFromTag(tag)
    print ("Number of words to translate: {0}".format(len(words_to_translate)))
    missing_ids = getMissingTranslations(translations_id)
    print ("Number of missing translations: {0}".format(len(missing_ids)))
    words_translated = generateTranslatedTag(words_to_translate, translations_id, missing_ids, lang)
    print ("Number of translated tags generated: {0}".format(len(words_translated)))

    writeTranslatedTags(source_file, words_translated, missing_ids, translations_id)

if __name__ == '__main__':
    main()