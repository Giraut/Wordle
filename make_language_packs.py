#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Creete Wordle language packs for different languages from various sources.
"""

### Modules
import re
import os
import requests
import argparse



### Parameters
language_pack_file_ext = ".langpack"



### Language definitions
languages = {

  "en_GB": {
    "description": [
      "Wordle British English language pack"
    ],
    "charset": "[A-Z]",
    "keyboard": [
      "_Q W E R T Y U I O P_",
      "__A S D F G H J K L__",
      "_< Z X C V B N M [=]_"
    ],
    "default_nb_letters": 5,
    "default_nb_attempts": 6,
    "default_difficulty": 5,
    "messages": {
      "difficulty": "Difficulty level: ",
      "poswords": " possible words!",
      "howquit": "(ESC twice to quit)",
      "guess": "Enter guess: ",
      "won": "You win!",
      "lost": "You lose! The word was:",
      "again": "Try again [Y/N]? ",
      "yes": "Y",
      "bye": "Bye..."
    },
    "frequency_list": {
      "src": "http://corpus.leeds.ac.uk/frqc/reuters-forms.num",
      "attribution": [
        "This frequency list is based on the frequency list produced in the",
        "Centre for Translation Studies, University of Leed and distributed",
        "under the Creative Commons (CC BY) Attribution license.",
        "For more information see http://corpus.leeds.ac.uk/list.html"
      ],
      "normalize": lambda lst, cs:
         [w.upper() for w in [e.split()[2] for e in lst \
         if re.match("^[0-9]+ +[0-9\.]+ +[^ ]+$", e)] \
         if re.match("^{}+$".format(cs), w.upper()) and w[0] == w[0].lower()]
    },
    "extra_words_list": {
      "src": "file:///usr/share/dict/british-english",
      "attribution": [
        "This list of extra words is based on the British English Debian",
        "English word list package (wbritish), built from the SCOWL",
        "(Spell-Checker Oriented Word Lists) package, whose upstream editor is",
        "Kevin Atkinson <kev‐ina@users.sourceforge.net>."
      ],
      "normalize": lambda lst, cs:
         [w.upper() for w in lst \
         if re.match("^{}+$".format(cs), w.upper()) and w[0] == w[0].lower()]
    }
  },

  "fi_FI": {
    "description": [
      "Suomen kielipaketti Worldlelle"
    ],
    "charset": "[A-ZÖÄÅ]",
    "keyboard": [
      "_Q W E R T Y U I O P Å_",
      "_A S D F G H J K L Ö Ä_",
      "__< Z X C V B N M [=]__"
    ],
    "default_nb_letters": 5,
    "default_nb_attempts": 6,
    "default_difficulty": 5,
    "messages": {
      "difficulty": "Vaikeusaste: ",
      "poswords": " mahdollista sanaa!",
      "howquit": "(ESC kahdesti lopettamaan)",
      "guess": "Anna arvaus: ",
      "won": "Voitat!!",
      "lost": "Häviät! Sana oli:",
      "again": "Yritä uudelleen [K/E]? ",
      "yes": "K",
      "bye": "Heippa..."
    },
    "frequency_list": {
      "src": "https://korp.csc.fi/korp/suomen-sanomalehtikielen-taajuussanasto-B9996.txt",
      "attribution": [
        "Suomen sanomalehtikielen 9996 yleisintä lemmaa (käytettävissä Commons",
        "Nimeä-Epäkaupallinen-Ei muutettuja teoksia 1.0 Suomi-lisenssin",
        "ehdoin). (c) 2004 Kielipankki, CSC - Tieteellinen laskenta Oy"
      ],
      "normalize": lambda lst, cs:
        [e[3].upper() for e in [e.split() for e in lst \
        if re.match("^ +[0-9]+ +[0-9]+ [0-9,]+ +[^ ]+ +\(.+\)$", e)] \
        if re.match("^{}+$".format(cs), e[3].upper()) and \
	"erisnimi" not in e[4]]
    },
    "extra_words_list": {
      "src": "https://raw.githubusercontent.com/hugovk/everyfinnishword/master/kaikkisanat.txt",
      "attribution": [
        "Copyright (c) Kotimaisten kielten tutkimuskeskus 2006",
        "Kotimaisten kielten tutkimuskeskuksen nykysuomen sanalista, versio 1",
        "Julkaistu 15.12.2006",
        "Sanalista julkaistaan GNU LGPL -lisenssillä. Lisenssiteksti ",
        "luettavissa osoitteessa http://www.gnu.org/licenses/lgpl.html"
      ],
      "normalize": lambda lst, cs:
         [w.upper() for w in lst if re.match("^{}+$".format(cs), w.upper())]
    }
  },

  "fr_FR": {
    "description": [
      "Paquet linguistique pour Wordle"
    ],
    "charset": "[A-ZÉËÊÈÎÏÇÀÔÙ]",
    "keyboard": [
      "_É Ë Ê È Î Ï Ç À_Ô_Ù_",
      "_A Z E R T Y U I O P_",
      "_Q S D F G H J K L M_",
      "__< W X C V B N [=]__"
    ],
    "default_nb_letters": 5,
    "default_nb_attempts": 6,
    "default_difficulty": 5,
    "messages": {
      "difficulty": "Difficulté: ",
      "poswords": " mots possibles!",
      "howquit": "(2 fois ESC pour quitter)",
      "guess": "Entrer essai : ",
      "won": "Gagné !",
      "lost": "Perdu ! Le mot était :",
      "again": "Réessayer [O/N]? ",
      "yes": "O",
      "bye": "Au revoir..."
    },
    "frequency_list": {
      "src": "https://fr.wiktionary.org/wiki/Utilisateur:Darkdadaah/Listes/Mots_dump/frwiki/2016-02-03",
      "attribution": [
        "Cette liste est basée sur la liste de fréquence lexicale",
        "Darkdadaah/Listes/Mots dump/frwiki/2016-02-03 compilée par",
        "l'utilisateur Wiktionnaire Darkdadaah. Recherche basée sur le",
        "dump de Wikipédia frwiki-20160203-pages-articles.xml.bz2 avec",
        "le script get_words_from_dump.pl d'Anagrimes."
      ],
      "normalize": lambda lst, cs:
        [w for w in [re.sub('^.*title=".+">(.+)</a>.*$', "\\1", w).upper() \
        for w in lst \
        if re.match('^<td><a href=".+" title=".+">.+</a></td>$', w)] \
        if re.match("^{}+$".format(cs), w)]
    },
    "extra_words_list": {
      "src": "file:///usr/share/dict/french",
      "attribution": [
        "Cette liste de mots supplémentaires est basée sur le paquet Debian",
        "wfrench compilé de sources variées."
      ],
      "normalize": lambda lst, cs:
         [w.upper() for w in lst \
         if re.match("^{}+$".format(cs), w.upper()) and w[0] == w[0].lower()]
    }
  },
}



### Routines
def load_src(src):
  """Load a source text file from various sources and return the lines as a list
  of strings
  """

  m = re.findall("^(file|http|https):\/\/(.*)$", src)
  if m:

    if m[0][0].startswith("http"):
      lines = requests.get(src).content.decode("utf-8").splitlines()

    elif m[0][0].startswith("file"):
      with open(m[0][1], "r") as f:
        lines = f.read().splitlines()

    return lines



def print_tuple_declaration_cols_formatted(name, lst, cols, f):
  """Print a tuple declaration as compactly as possibly within a certain number
  of columns per line into a file
  """

  l = '{} = ("{}"'.format(name, lst[0])

  for w in lst[1:]:

    if len(l) + len(w) + 4 < cols:
      l += ', "{}"'.format(w)

    else:
      print(l + ",", file = f)
      l = '  "{}"'.format(w)

  print(l + ")", file = f)



### Main routine
if __name__ == "__main__":

  # Parse the command line arguments
  argparser = argparse.ArgumentParser()

  argparser.add_argument(
	"-l", "--language",
	help = "Only build language pack for one language (default all)",
	type = str)

  args = argparser.parse_args()

  if args.language and args.language not in languages:
    print("Unknown language {}. Available: {}".format(args.language,
		", ".join(languages)))
    exit(-1)

  # Iterate over the languages definitions
  for lang in (args.language,) if args.language else languages:

    charset = languages[lang]["charset"]

    # Load and process the frequency list
    fl = load_src(languages[lang]["frequency_list"]["src"])
    fl = languages[lang]["frequency_list"]["normalize"](fl, charset)

    # Load and process the extra words list
    ewl = load_src(languages[lang]["extra_words_list"]["src"])
    ewl = languages[lang]["extra_words_list"]["normalize"](ewl, charset)
    ewl = sorted(set(ewl) - set(fl))

    # Open the language pack file for writing
    with open(lang + language_pack_file_ext, "w") as f:

      print("# -*- coding: utf-8 -*-", file = f)

      # Generate the description of the pack
      for l in languages[lang]["description"]:
        print("# " + l, file = f)

      print(file = f)

      # Generate the charset declaration
      print('charset = "{}"'.format(charset), file = f)

      print(file = f)

      # Generate the keyboard declaration
      print("keyboard = [", file = f)
      for i, l in enumerate(languages[lang]["keyboard"]):
        if i:
          print(",", file = f)
        print('  "{}"'.format(l), end = "", file = f)
      print("]", file = f)

      print(file = f)

      # Generate the default_nb_letters declaration
      print("default_nb_letters = {}".
		format(languages[lang]["default_nb_letters"]), file = f)

      # Generate the default_nb_attempts declaration
      print("default_nb_attempts = {}".
		format(languages[lang]["default_nb_attempts"]), file = f)

      # Generate the default_difficulty declaration
      print("default_difficulty = {}".
		format(languages[lang]["default_difficulty"]), file = f)

      print(file = f)

      # Generate the messages declaration
      for k in languages[lang]["messages"]:
        print('{} = "{}"'.format(k, languages[lang]["messages"][k]), file = f)

      print(file = f)

      # Generate the frequency list attribution
      for l in languages[lang]["frequency_list"]["attribution"]:
        print("# " + l, file = f)

      # Generate the frequency list declaration (80 columns-formatted)
      print_tuple_declaration_cols_formatted("frequency_list", fl, 80, f)

      print(file = f)

      # Generate the extra words list attribution
      for l in languages[lang]["extra_words_list"]["attribution"]:
        print("# " + l, file = f)

      # Generate the extra words list declaration (80 columns-formatted)
      print_tuple_declaration_cols_formatted("extra_words_list", ewl, 80, f)
