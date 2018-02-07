# Automatic Xlf Translator

Automatic .xlf translator tool written in python. Reads a xlf and transforms it in a tree data stracture
in order to translate it.

If using in an angular project translations will be automaticly stored in src/assets/locale/.

## Getting Started

### Prerequisites

Written in python, imports needed
```
from googletrans import Translator
from bs4 import BeautifulSoup
from optparse import OptionParser
```

### Running

Execute defining your original .xlf file, the path where you want to save it and
the language you wish. Special unicode characters such as chinesse not supported.

```
python translate.py -f origin.xlf -t translated.xlf -l de
```



## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


