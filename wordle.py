#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Wordle game for the Unix console

This is a clone of the popular Wordle game playable on a regular Unix terminal
"""

### Modules
import re
import os
import sys
import tty
import random
import termios
import argparse
import importlib.util
import importlib.machinery



### Parameters
# Paths to language packs
language_packs_path = ("/usr/local/games/wordle", ".")

# Default language packs attached to plain language names
languages = {
  "english":	"en_GB",
  "suomi":	"fi_FI"}

# What language pack we should load depending on the name of the program
alternative_program_name_language_packs = {
  r"sanuli(\.py)?":	"fi_FI",
  ".+":			"en_GB"}



### Defines:
# ANSI standard color selection sequence
set_colors = "\033[{};{}m"

# ANSI attributes reset
attribute_reset = "\033[0m"

# ANSI x lines up
x_lines_up = "\033[{}A"

# Standard ANSI 4-bit colors
bg_color_black = 40
bg_color_green = 42
bg_color_yellow = 43
bg_color_lightgrey =47
bg_color_grey = 100
bg_color_white = 107

fg_color_black = 30
fg_color_white = 97

# Colors for each type of letter
color_letter_found = set_colors.format(bg_color_green, fg_color_white)
color_letter_misplaced = set_colors.format(bg_color_yellow, fg_color_white)
color_letter_spent = set_colors.format(bg_color_grey, fg_color_white)
color_letter_unused = set_colors.format(bg_color_lightgrey, fg_color_black)
color_letter_empty = set_colors.format(bg_color_white, fg_color_white)
color_letter_normal = attribute_reset

# Special keys
RETURN = "\r"
ESCAPE = "\x1b"
BACKSPACE = "\x7f"



### Routines
def load_language_pack(lpfile):
  """Load a Wordle language pack
  """

  loader = importlib.machinery.SourceFileLoader("lp", lpfile)
  spec = importlib.util.spec_from_loader("lp", loader)
  lp = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(lp)

  return lp



def colored_guess(word, guess, spent_letters):
  """Return a colored guessword
  """

  s = [" " + (" " if c == "_" else c) + " " for c in guess]
  w = list(word)
  g = list(guess)

  for i, c in enumerate(g):

    if w[i] == c:
      s[i] = color_letter_found + s[i]
      w[i] = "0"
      g[i] = "1"

  for i, c in enumerate(g):

    if c == "_":
      s[i] = color_letter_empty + s[i]

    elif c in w:
      s[i] = color_letter_misplaced + s[i]
      w[w.index(c)] = "0"

    elif c != "1":
      s[i] = color_letter_spent + s[i]

  return "".join(s) + attribute_reset



def colored_kbdline(word, kbdline, spent_letters, found_letters):
  """Return a colored keyboard line
  """

  s = ""

  for i, c in enumerate(kbdline):

    if c == "_":
      s += color_letter_empty + " "

    elif c not in spent_letters :
      s += color_letter_unused + c

    elif c in found_letters:
      s += color_letter_found + c

    elif c in word:
      s += color_letter_misplaced + c

    else:
      s += color_letter_spent + c

  return s + attribute_reset



def readchar():
  """Read one character raw
  """
  ss = termios.tcgetattr(sys.stdin.fileno())

  try:
    tty.setraw(sys.stdin.fileno())
    return sys.stdin.read(1)

  finally:
    termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, ss)



def game(letters, attempt, difficulty):
  """Wordle game proper
  """

  # Calculate the spacing to center the guesswords and the keyboard
  sp =  int((letters * 3 - len(lp.keyboard[0])) / 2)

  # Calculate the maximum line length
  max_ll = max(letters * 3 + max(0, -sp),
		len(lp.keyboard[0]) + max(0, sp),
		len(lp.guess) + letters, len(lp.won), len(lp.lost),
		len(lp.again))

  # Isolate the list of words to choose from from the frequency list
  # and reduce it according to the difficulty level
  pws = [w for w in lp.frequency_list if len(w) == letters]
  pws = pws[:max(1, int(len(pws) /5 * difficulty))]

  # Display the difficulty level and size of the list of words to choose from
  print("\n{}{}/5".format(lp.difficulty, difficulty))
  print("{}{}\n".format(len(pws), lp.poswords))

  # The list of words to choose from should have at least one entry
  if len(pws) < 1:
    return -1

  print(lp.howquit + "\n")

  # Run the game continuously
  while True:

    # Pick a new word to find
    word =  random.sample(pws, 1)[0]

    # Reset guesses and lists of spent and found letters
    guesses = ["_" * letters] * attempts
    spent_letters = ""
    found_letters = ""

    guess = ""

    # Wipe the game area clean and move the cursor back to the top left
    print((" " * max_ll + "\n") * (attempts + len(lp.keyboard) + 8), end = "")
    print(x_lines_up.format(attempts + len(lp.keyboard) + 8), end = "\r")

    for t in range(attempts + 1):

      # Print the stack of guesswords
      for g in guesses:
        print(" " * -sp + colored_guess(word, g, spent_letters))

      print()

      # Print the keyboard
      for l in lp.keyboard:
        print(" " * sp + colored_kbdline(word, l, spent_letters, found_letters))

      print()

      # If the user has run out of attempts or has guessed right, stop trying
      if t == attempts or guess == word:
        print("\n")
        break

      # Ask the user their next guess. Only stop the user input when the user
      # hits ESC or enters a guessword that is in the frequency list or in the
      # extra words list
      guess = ""
      escapes = 0

      print(lp.guess + "_" * letters + "\b" * letters, end = "")

      while True:

        # Make sure the display is up to date
        sys.stdout.flush()

        # Read a single character
        c = readchar().upper()

        # Count successive ESC characters
        escapes = escapes + 1 if c == ESCAPE else 0

        # Erase a character from the guessword
        if c == BACKSPACE:
          if guess:
            guess = guess[:-1]
            print("\b_", end = "\b")

        # Validate the guess if it's in the frequency list or extra words list
        elif c == RETURN:
          if guess in lp.frequency_list or guess in lp.extra_words_list:
            break

        # Add a letter to the guessword if there's still room
        elif re.match("^{}$".format(lp.charset), c):
          if len(guess) < letters:
            guess += c
            print(c, end = "")

        # Quit if ESC twice
        elif escapes == 2:
          print("\n\n" + lp.bye + "\n")
          return 0

      # Add the new guessword to the list of guesswords
      guesses[t] = guess

      # Add the new guessword's letters to the list of spent letters
      spent_letters += guess

      # Add the new guessword's letters that match the word's letters at the
      # same position to the list of found letters
      for i, c in enumerate(guess):
        if word[i] == c:
          found_letters += c

      # Move the cursor back to the top left
      print(x_lines_up.format(attempts + len(lp.keyboard) + 2), end = "\r")

    # Display whether the user won or lost, and what the word was if they lost
    print((re.won + "\n") if guess == word else lp.lost + "\n" + \
		colored_guess(word, word, "") + attribute_reset, end = "\n\n")

    # Ask the user if they would like to play again
    print(lp.again)
    c = readchar()

    if c.upper() != lp.yes and c != RETURN:
      print("\n" + lp.bye + "\n")
      break

    # Move the cursor back to the top left
    print(x_lines_up.format(attempts + len(lp.keyboard) + 8), end = "\r")

  return 0



### Main routine
if __name__ == "__main__":

  # Get the list of all available language packs
  lps = {f.split(".")[0]: os.path.join(p, f) for p in language_packs_path \
	if os.path.exists(p) for f in os.listdir(p) \
	if os.path.isfile(os.path.join(p, f)) and \
	re.match("^[a-zA-Z_-]+\.langpack$", f)}

  # Remove languages for which we don't have a language pack
  languages = {l: languages[l] for l in languages if languages[l] in lps}



  # Parse the command line arguments
  argparser = argparse.ArgumentParser()

  argparser.add_argument(
	"-l", "--language",
	help = "Language to use. Available: {}".format(", ".join(languages)),
	type = str)

  argparser.add_argument(
	"-L", "--language-pack",
	help = "Language pack use. Available: {}".format(", ".join(lps)),
	type = str)

  argparser.add_argument(
	"-n", "--nb-letters",
	help = "Number of letters in the words",
	type = int)

  argparser.add_argument(
	"-a", "--attempts",
	help = "Number of attempts",
	type = int)

  argparser.add_argument(
	"-d", "--difficulty",
	help = "1 -> 5 - Word chosen between most common and rarest words",
	type = int)

  args = argparser.parse_args()



  # Did the user specify a language pack to load?
  if args.language_pack:
    lpname = args.language_pack

  # Did the user specify a language to load a language pack for?
  elif args.language:
    if args.language not in languages:
      print("Language {} not available".format(args.language))
      exit(-1)
    lpname = languages[args.language]

  # Otherwise determine the default language pack and load it
  else:
    for pn in alternative_program_name_language_packs:
      if re.match("^{}$".format(pn), os.path.split(sys.argv[0])[1]):
        lpname = alternative_program_name_language_packs[pn]
        break

  # Load the language pack
  if lpname not in lps:
    print("Language pack {} not available".format(lpname))
    exit(-1)
  lp = load_language_pack(lps[lpname])

  # Did the user specify a number of letters?
  letters = lp.default_nb_letters
  if args.nb_letters is not None:
    if args.nb_letters < 2 or \
	args.nb_letters > sorted(len(w) for w in lp.frequency_list)[-1]:
      print("Invalid number of letters {}".format(args.nb_letters))
      exit(-1)
    letters = args.nb_letters

  # Did the user specify a number of attempts?
  attempts = lp.default_nb_attempts
  if args.attempts is not None:
    if args.attempts < 1:
      print("Invalid number of attempts {}".format(args.attempts))
      exit(-1)
    attempts = args.attempts

  difficulty = lp.default_difficulty
  if args.difficulty is not None:
    if args.difficulty < 1 or args.difficulty > 5:
      print("Invalid difficulty level {}".format(args.difficulty))
      exit(-1)
    difficulty = args.difficulty



  # Run the game
  exit(game(letters, attempts, difficulty))
