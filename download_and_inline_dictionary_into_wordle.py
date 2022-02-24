#!/usr/bin/python3
"""Download one of the frequency lists from http://corpus.leeds.ac.uk/list.html,
   remove unwanted entries, then inline the data as the dictionary in the
   wordle.py script
"""

### Modules
import re
import os
import requests

### Parameters
source_frequency_word_list = "http://corpus.leeds.ac.uk/frqc/reuters-forms.num"
attribution = [
  "The frequency list this dictionary is based on was produced in the Centre",
  "for Translation Studies, University of Leed and distributed under the",
  "Creative Commons (CC BY) Attribution license.",
  "For more information see http://corpus.leeds.ac.uk/list.html"
]
target_script = "./wordle.py"
temp_file = target_script + ".tmp"
dictionary_marker = "### Dictionary"



### Main routine
if __name__ == "__main__":

  # Download the source frequency word list
  dic = requests.get(source_frequency_word_list).content. \
		decode("ascii").splitlines()

  # Only keep common nouns from the list.
  # The list is already ordered by reverse usage frequency
  dic = [e.split()[2] for e in dic if re.match("^[0-9]+ +[0-9\.]+ +[a-z]+$", e)]

  # Open the wordle.py script for reading
  with open(target_script, "r") as ifile:

    # Open the temporary file for writing
    with open(temp_file, "w") as ofile:

      # Copy the script into the temporary file as is, but add the attribution
      # and the Python source-formatted dictionary after the marker
      copy_lines = True

      for l in ifile.read().splitlines():

        # If we had stopped copying lines, start copying again when an empty
        # line is encountered
        if not l:
          copy_lines = True

        # Copy lines from the source script to the temporary file
        if copy_lines:
          print(l, file = ofile)

        # Does the line contain the marker for the beginning of the dictionary's
        # declaration?
        if dictionary_marker in l:

          # Stop copying lines
          copy_lines = False

          # Write the attribution in the temporary file as a Python comment
          for al in attribution:
            print("# " + al, file = ofile)

          # Format the dictionary into a compact tuple declaration and write
          # this new declaration in the temporary file
          l = 'dictionary = ("{}",'.format(dic[0])
          pl = ""

          for w in dic[1:]:

            if pl:
              print(pl, file = ofile)
              pl = ""

            w = ' "' + w + '",'
            if len(l) + len(w) <= 80:
              l += w
            else:
              pl = l
              l = " " + w

          print(pl[:-1] + ")", file = ofile)

  # Open the temporary file for reading
  with open(temp_file, "r") as ifile:

    # Open the wordle.py script for writing
    with open(target_script, "w") as ofile:

      # Copy the content of the temporary file back into the target script
      for l in ifile.read().splitlines():
        print(l, file = ofile)

  # Delete the temporary file
  os.unlink(temp_file)
