#!/usr/bin/python3
"""Wordle-like game for the Unix console

This is what the New York Times bought for over one million dollars :)

If you're tired of being tracked online when you play this wonderful little
game, use this small Python script instead.

You need to install the readchar module to make it work:

pip3 install readchar

The dictionary should be a flat files with one English word per line. Typically
dictionary files are installed in /usr/share/dict by most Linux distributions.

The larger the dictionary, the more varied the words of course.
"""

# Modules
import sys
import string
from random import randrange
from readchar import readchar



# Parameters
dictionary = "/usr/share/dict/american-english"
letters = 5
attempts = 6



# Defines:
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

# Keyboard
keyboard = [
  "_Q W E R T Y U I O P_",
  "__A S D F G H J K L__",
  "_< Z X C V B N M [=]_"]

# Special keys
BACKSPACE = "\x7f"
ESC = "\x1b"
RETURN = "\r"



# Routines
def colored_guess(word, guess, spent_letters):
  """Return a colored guessword
  """

  s = ""
  w = list(word)

  for i, c in enumerate(guess):

    if c == "_":
      s += color_letter_empty + " " + c + " "

    elif w[i] == c:
      s += color_letter_found + " " + c + " "
      w[i] = None

    elif c in w:
      s += color_letter_misplaced + " " + c + " "
      w[i] = None

    else:
      s += color_letter_spent + " " + c + " "

  return s + attribute_reset



def colored_kbdline(kbdline, spent_letters, found_letters):
  """Return a colored keyboard line
  """

  s = ""

  for i, c in enumerate(kbdline):

    if c == "_":
      s += color_letter_empty + c

    elif c not in spent_letters :
      s += color_letter_unused + c

    elif c in found_letters:
      s += color_letter_found + c

    elif c in word:
      s += color_letter_misplaced + c

    else:
      s += color_letter_spent + c

  return s + attribute_reset



# Main routine
if __name__ == "__main__":

  # Load words of the correct length without odd characters from the dictionary
  with open(dictionary, "r") as f:
    dictio = [w.upper() for w in f.read().splitlines() \
		if w.isalpha() and len(w) == letters]

  # Run the game continuously
  while True:

    # Pick a new word to find
    word = dictio[randrange(len(dictio))]

    guesses = ["_" * letters] * attempts
    spent_letters = ""
    found_letters = ""

    guess = ""

    print()

    k_offset =  int((letters * 3 - len(keyboard[0])) / 2)

    for t in range(attempts + 1):

      # Print the stack of guesswords
      for g in guesses:
        print(" " * -k_offset + colored_guess(word, g, spent_letters))

      print()

      # Print the keyboard
      for l in keyboard:
        print(" " * k_offset + colored_kbdline(l, spent_letters, found_letters))

      print()

      # If the user has ran out of attempts or has guessed right, stop trying
      if t == attempts or guess == word:
        print("\n")
        break

      # Ask the user their next guess. Only stop the user input when the user
      # hits ESC or enters a guessword that is in the dictionary
      guess = ""

      print("Enter guess:", "_" * letters + "\b" * letters, end = "")

      while True:

        # Make sure the display is up to date
        sys.stdout.flush()

        # Read a single character
        c = readchar().upper()
 
        # Erase a character from the guessword
        if c == BACKSPACE:
          if guess:
            guess = guess[:-1]
            print("\b_", end = "\b")

        # Validate the guess if it's in the dictionary
        elif c == RETURN:
          if guess in dictio:
            break

        # Quit
        elif c == ESC:
          print("\n\nBye...\n")
          quit()

        # Add a letter to the guessword
        elif len(guess) < letters and c.isalpha():
          guess += c
          print(c, end = "")

      # Add the new guessword to the list of guesswords
      guesses[t] = guess

      # Add the new guessword's letters to the list of spent letters
      spent_letters += guess

      # Add the new guessword's letters that match the word's letters at the
      # same position to the list of found letters
      for i, c in enumerate(guess):
        if word[i] == c:
          found_letters += c

      # Move the cursor back to the top of the stack of guesses, 1st column
      print(x_lines_up.format(attempts + len(keyboard) + 2) + "\r", end = "")

    # Display whether the user won or lost, and what the word was if they lost
    print("You win!" if guess == word else "You lose! The word was:\n" + \
		colored_guess(word, word, "") + attribute_reset, end = "\n\n")

    # Ask the user if they would like to play again
    print("Try again [Y/N]?")
    c = readchar()

    if c not in "yY" + RETURN:
      print("\nBye...\n")
      break
