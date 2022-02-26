# wordle v1.4.4
## Wordle game for the Unix console

This is a clone of the popular Wordle game playable on a regular Unix terminal

Two dictionaries are used:

  - A frequency list - i.e. a list of words sorted by reverse usage frequency
  - A larger, unsorted list of extra words

The word to guess is picked from the frequency list more or less near the top according to the difficulty level. The guesswords the user is allowed to enter are checked against both lists, so the user can enter valid wild guesses to draw out letter matches.

Different lists and game parameters are used in different language packs:

  * en_GB (British English):

    The frequency list is based on the frequency list produced in the Centre for Translation Studies, University of Leed and distributed under the Creative Commons (CC BY) Attribution license. For more information see [http://corpus.leeds.ac.uk/list.html](http://corpus.leeds.ac.uk/list.html)

    The list of extra words is based on the British English Debian English word list package (wbritish), built from the SCOWL (Spell-Checker Oriented Word Lists) package, whose upstream editor is Kevin Atkinson [<kev‐ina@users.sourceforge.net>](mailto:<kev‐ina@users.sourceforge.net>).

  * fi_FI (Finnish):

    The frequency list is based on the 9996 most common lemmas in the language of Finnish newspapers (available under the terms of the Creative Commons
    Non Commercial license 1.0). (c) 2004 Kielipankki, CSC - Tieteellinen laskenta Oy

    The list of extra words is based on the contemporary Finnish words list from the Finnish Language Research center, version 1, published 12/15/06 under the terms of the GNU LGPL license.

  * fr_FR (France French):

    The frequency list is based on the ```Darkdadaah/Listes/Mots``` ```dump/frwiki/2016-02-03``` frequency list compiled by Wiktionnaire user Darkdabaah.

    The list of extra words is based on the ```wfrench``` Debian package compiled from various sources.



Use the ```-l``` or ```-L``` switches to change language.

Additionally, renaming or symlinking the program with the name ```sanuli``` or ```sanuli.py``` will automatically start the game in Finnish, and ```lemot``` or ```lemot.py``` will start the game in French.

Use ```-n``` to change the number of letters, ```-a``` to change the number of attempts and ```-d``` to change the level of difficulty.



[Debian](https://github.com/Giraut/ppa) and [RPM](https://github.com/Giraut/rpm) Linux packages are also available.
