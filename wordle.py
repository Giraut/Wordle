#!/usr/bin/python3
"""Wordle game for the Unix console

This is what the New York Times paid $1.7M for :)

If you're tired of being tracked online when you play this wonderful little
game, use this Python script instead.

The dictionary files should be flat files with one word per line.
They are commonly installed in /usr/share/*spell/ or /usr/share/dict/.
If you don't see files there, try installing hunspell-en-us or wamerican.
The program tries to load as many of the files listed in the parameters.

The larger the final combined dictionary, the more varied the words of course.
"""

# Modules
import sys
import tty
import random
import termios


# Parameters
dictionaries = [
  "/usr/share/hunspell/en_US.dic",
  "/usr/share/myspell/en_US.dic",
  "/usr/share/dict/american-english"]
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
RETURN = "\r"



# Routines
def colored_guess(word, guess, spent_letters):
  """Return a colored guessword
  """

  s = [" " + c + " " for c in guess]
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



def readchar():
  """Read one character raw
  """
  ss = termios.tcgetattr(sys.stdin.fileno())

  try:
    tty.setraw(sys.stdin.fileno())
    return sys.stdin.read(1)

  finally:
    termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, ss)



# Main routine
if __name__ == "__main__":

  # Load words of the right length without odd characters from the dictionaries
  dic = set()
  for d in dictionaries:
    try:
      with open(d, "r") as f:
        dic = dic.union(set([w.upper() for w in \
			[w.split("/")[0] for w in f.read().splitlines()] \
			if w.isalpha() and len(w) == letters]))
    except:
      pass

  # Run the game continuously
  while True:

    # Pick a new word to find
    word = random.sample(list(dic), 1)[0]

    # Reset guesses and lists of spent and found letters
    guesses = ["_" * letters] * attempts
    spent_letters = ""
    found_letters = ""

    guess = ""

    print()

    # Spacing to center the guesswords and the keyboard
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

      # If the user has run out of attempts or has guessed right, stop trying
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
          if guess in dic:
            break

        # Add a letter to the guessword if there's still room
        elif c.isalpha():
          if len(guess) < letters:
            guess += c
            print(c, end = "")

        # Any other key: quit
        else:
          print("\n\nBye...\n")
          quit()

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
