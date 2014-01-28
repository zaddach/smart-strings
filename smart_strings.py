#!/usr/bin/env python3

import sys
import string
import argparse
import codecs
try:
    import enchant
    ENCHANT_AVAILABLE = True
except ImportError as err:
    ENCHANT_AVAILABLE = False

READABLE_CHARACTERS = string.ascii_letters + string.digits
CLEAN_STRING_CHARACTERS = string.ascii_letters + string.digits + "'-"
PRINTABLE_CHARACTERS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t'

class FloatRange():
    def __init__(self, start, end):
        self._start = start
        self._end = end
        
    def __eq__(self, value):
        return value >= self._start and value <= self._end
        
    def __str__(self):
        return "[%0.2f, %0.2f]" % (self._start, self._end)

def find_printables(input_stream):
    offset = 0
    cur_string = None
    strings = []
    for char in input_stream.read():
        if char in string.printable:
            if cur_string:
                cur_string[1].append(char)
            else:
                cur_string = (offset, [char])
        else:
            if cur_string:
                yield (cur_string[0], "".join(cur_string[1]))
                cur_string = None
        offset += 1
        
def is_readable_string(value, percentage):
    readable_characters = 0
    for letter in value:
        if letter in READABLE_CHARACTERS:
            readable_characters += 1
            
    return float(readable_characters) / float(len(value)) >= percentage
        

def main(argv):
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-r", "--readable", nargs = '?', dest = "readable_percentage", const = 0.8, default = 0.0, type = float, choices = [FloatRange(0.0, 1.0)], help = "Part of the string that needs to consist of letters or digits")
    parser.add_argument("-o", "--offset", action = "store_true", dest = "print_offset", help = "Print offset where string occurs")
    parser.add_argument("-c", "--charset", type = str, default = "iso-8859-1", dest = "charset", help = "Input character set used for input stream in python (iso-8859-1, UTF-8, UTF-16, ...)")
    parser.add_argument("-n", "--min", type = int, default = 5, dest = "min", help = "Minimum number of characters in the string, or in case of dictionary checking the minimum length of words")
    parser.add_argument("-m", "--max", type = int, default = -1, dest = "max", help = "Maximum number of characters in the string")
    parser.add_argument("-f", "--filter-nonprintables", action = "store_true", dest = "filter_nonprintables", help = "Replace nonprintable characters with spaces")
    if ENCHANT_AVAILABLE:
        parser.add_argument("-d", "--dict", dest = "dicts", action = "append", help = "Use this dictionary to test if words exist (can be specified multiple times to use several dictionaries; use '?' to get a list of installed dictionaries)")
    parser.add_argument("input_file", type = str, metavar = "FILE", nargs = '?', const = None, default = None, help = "File to read from; do not specify to read from stdin")

    args = parser.parse_args(argv[1:])
    
    if ENCHANT_AVAILABLE:
        if len(args.dicts) == 1 and args.dicts[0] == '?':
            print("Installed dictionaries: %s" % (", ".join(enchant.list_languages()), ))
            sys.exit(0)
        
        dicts = list(map(enchant.request_dict, args.dicts))
    else:
        dicts = []
    
    if not args.input_file is None:
        input_stream = open(args.input_file, 'r', encoding = args.charset)
    else:
        input_stream = codecs.getwriter(args.charset)(sys.stdin.buffer)
        
    for (offset, value) in find_printables(input_stream):
        if not is_readable_string(value, args.readable_percentage):
            continue
        if len(value) < args.min:
            continue
        if args.max != -1 and len(value) > args.max:
            continue
        
        #Try to isolate words in the string and see if they are present in the dictionaries
        #If the word could not be found, skip the string
        if dicts:
            word_found = False
            cleaned_string = "".join([x in CLEAN_STRING_CHARACTERS and x or " " for x in value])
            for word in cleaned_string.split():
                if len(word) < args.min:
                    continue
                
                for dictionary in dicts:
                    if dictionary.check(word.lower()):
#                       print("Found word %s" % word)
                       word_found = True
            if not word_found:
                continue
        
        if args.filter_nonprintables:
            value = "".join([x in PRINTABLE_CHARACTERS and x or " " for x in value.strip()])
        else:
            value = value.strip()
        
        if args.print_offset:
            print("% 5d: %s" % (offset, value))
        else:
            print("%s" % (value, ))
            
    input_stream.close()

if __name__ == "__main__":
    main(sys.argv)
#    print(find_printables(sys.argv[1]))
