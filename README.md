# wordle - v1.2.0
## Wordle game for the Unix console

This is a clone of the popular Wordle game playable on a regular Unix terminal

The main dictionary used in this game to pick words to find from is based on the frequency list produced in the Centre for Translation Studies, University of Leed and distributed under the Creative Commons (CC BY) Attribution license.
For more information see [http://corpus.leeds.ac.uk/list.html](http://corpus.leeds.ac.uk/list.html)

In addition, this game also uses extended, unsorted spellchecking dictionaries
to validate the user's guess entries. They allow the user to enter obscure
words that wouldn't normally be used as words to find, but that are valid
words.

Those unsorted spellchecking dictionary files should be flat files with one word per line. They are commonly installed in ```/usr/share/*spell/``` or ```/usr/share/dict/```. If you don't see files there, try installing ```hunspell-en-us``` or ```wamerican```. The program tries to load as many of the files listed in the parameters.

The larger the spellchecking dictionaries, the more varied the words the user
may enter as guesses.



[Debian](https://github.com/Giraut/ppa) and [RPM](https://github.com/Giraut/rpm) Linux packages are also available.
