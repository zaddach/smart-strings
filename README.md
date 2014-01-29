smart-strings
=============

An implementation of the unix 'strings' utility in python that has some more advanced features

Usage examples
--------------

- *./smart_strings.py <file>* will search for sequences of at least 5 readable characters in
  the whole file (contrary to the strings utility object files are not treated specially).
- *./smart_strings.py -d en_US -n 6 <file>* will print all strings that have at least one word
   with six characters or more which is contained in the US-English dictionary of enchant.
- *./smart_strings.py -r <file>* will search for character sequences that contain at least
  80% of letters and digits (You can use a different percentage with the 
  *--readable-percentage* switch).
- *./smart_strings.py -d ?* displays the dictionaries that are available on the system.
- *./smart_strings.py -c UTF-16LE <file>* will search for UTF-16 strings with little endian
  encoding in <file> (Unfortunately there is no nice way to enumerate encodings in python,
  but you can use the same encoding names that you would use when opening a file in python). 

