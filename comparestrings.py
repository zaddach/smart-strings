#
# This script compares the strings of two executables.
# It's a simple 'strings' wrapper.
#
# October 2013 - emdel
#

import sys, subprocess, hashlib


COMMAND = "strings"
NULL_MD5 = "d41d8cd98f00b204e9800998ecf8427e" 


def giveme_strings(arg):
    return subprocess.check_output(arg)


def giveme_md5(data):
    return hashlib.md5(data).hexdigest()


def is_null(hashish):
    if hashish == NULL_MD5:
        return True
    return False


def set_commands(pe, how):
    params = []
    if how == 0:
        params.append(COMMAND)
        params.append(pe)
    elif how == 1:
        params.append(COMMAND)
        params.append("-e")
        params.append("l")
        params.append(pe)
    else:
        print "Error - How value not supported."
        sys.exit(-1)
    return params


def main():
    if len(sys.argv) != 3:
        print "Usage %s <abs path pe1> <abs path pe2>" % sys.argv[0]
        sys.exit(1)

    # How: 0 means normal, 1 means utf strings
    arguments = set_commands(sys.argv[1], 0)
    data1 = giveme_strings(arguments)
    dig1 = giveme_md5(data1)
    print "%s - Strings MD5: %s" % (sys.argv[1], dig1)

    arguments = set_commands(sys.argv[2], 0)
    data2 = giveme_strings(arguments)
    dig2 = giveme_md5(data2)
    print "%s - Strings MD5: %s" % (sys.argv[2], dig2)

    if is_null(dig1): print "%s --> NULL string output!" % sys.argv[1]
    if is_null(dig2): print "%s --> NULL string output!" % sys.argv[2]

    # utf strings, let's do it.
    arguments = set_commands(sys.argv[1], 1)
    data3 = giveme_strings(arguments)
    dig3 = giveme_md5(data3)
    print "%s - UTF Strings MD5: %s" % (sys.argv[1], dig3)
    arguments = set_commands(sys.argv[2], 1)
    data4 = giveme_strings(arguments)
    dig4 = giveme_md5(data4)
    print "%s - UTF Strings MD5: %s" % (sys.argv[2], dig4)

    if is_null(dig3): print "%s --> NULL UTF string output!" % sys.argv[1]
    if is_null(dig4): print "%s --> NULL UTF string output!" % sys.argv[2]

    print "Normal string check"
    list1 = data1.split() 
    list2 = data2.split()
    pe1_in_pe2 = 0
    for l in list1:
        if l in list2:
            pe1_in_pe2 += 1
    print "\t>> similarity (1 over 2): %f" % (float(float(pe1_in_pe2)/float(len(list2))) * 100)

    pe2_in_pe1 = 0
    for l in list2:
        if l in list1:
            pe2_in_pe1 += 1
    print "\t>> similarity (2 over 1): %f" % (float(float(pe2_in_pe1)/float(len(list1))) * 100)

    print "UTF string check"
    if len(data3) != 0 and len(data4) != 0:
        list1 = data3.split() 
        list2 = data4.split()
        pe1_in_pe2 = 0
        for l in list1:
            if l in list2:
                pe1_in_pe2 += 1
        print "\t>> similarity (1 over 2): %f" % (float(float(pe1_in_pe2)/float(len(list2))) * 100)

        pe2_in_pe1 = 0
        for l in list2:
            if l in list1:
                pe2_in_pe1 += 1
        print "\t>> similarity (2 over 1): %f" % (float(float(pe2_in_pe1)/float(len(list1))) * 100)

        print ":: Looking for lame usernames..."
        for l in list1:
            args = l.split("\\")
            cnt = 0
            for a in args:
                cnt += 1
                if (a == "Users" or a == "Documents and Settings") and args[cnt] != "Administrator":
                   print "\t Nickname: %s" % args[cnt]


main()
