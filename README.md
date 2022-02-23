# Wordle game for the Unix console

This is what the New York Times paid $1.7M for :)

If you're tired of being tracked online when you play this wonderful little game, use this Python script instead.

The dictionary files should be flat files with one word per line. They are commonly installed in ```/usr/share/*spell/``` or ```/usr/share/dict/```. If you don't see files there, try installing ```hunspell-en-us``` or ```wamerican```.
The program tries to load as many of the files listed in the parameters.

The larger the final combined dictionary, the more varied the words of course.
