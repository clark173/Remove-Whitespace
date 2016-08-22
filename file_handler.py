#!/usr/bin/env python2
import os
import sys

from shutil import copyfile


FILE_ERROR = 1
EMPTY_FILE = 2
KEYBOARD_INTERRUPT = 3


class FileHandler:
    def __init__(self, filename):
        self.filename = filename

        input_file = self._open_file(filename)
        self._copy_file()
        self.lines = self._read_file(input_file)
        input_file.close()

    def _open_file(self, filename):
        if not os.path.isabs(filename):
            directory = os.path.dirname(os.path.realpath(__file__))
            self.filename = os.path.join(directory, filename)

        try:
            f = open(self.filename, 'r')
        except IOError:
            print "Error: '%s' does not appear to be a valid file"\
                  % (filename)
            print "Please try again with a valid filepath"
            sys.exit(FILE_ERROR)

        return f

    def _read_file(self, input_file):
        lines = input_file.readlines()

        if len(lines) < 1:
            print "Error: File is empty - nothing to do"
            print "Please try again with a populated file"
            sys.exit(EMPTY_FILE)

        return lines

    def _save_new_file(self):
        while True:
            new_filename = get_input("Please enter a new filename: ")
            if os.path.isfile(new_filename):
                response = get_input("'%s' already exists. Overwrite file? "
                                     "[y/n] " % (new_filename))
                if response.lower() == 'y':
                    return new_filename
                else:
                    continue
            else:
                return new_filename

    def _copy_file(self):
        backup = '%s.backup' % (self.filename)

        if os.path.isfile(backup):
            while True:
                response = get_input("'%s' already exists. Overwrite file? "
                                     "[y/n] " % (backup))
                if response.lower() == 'y':
                    break
                elif response.lower() == 'n':
                    backup = self._save_new_file()
                    break
                else:
                    continue

        copyfile(self.filename, backup)

    def save_file(self, lines, verbose):
        f = open(self.filename, 'w')

        for line in lines:
            f.write(line)

        if verbose:
            print "File saved at '%s'" % (self.filename)

        f.close()


def keyboard_input(func):
    def wrapper(prompt):
        try:
            return func(prompt)
        except KeyboardInterrupt:
            print "\nExiting script"
            sys.exit(KEYBOARD_INTERRUPT)
    return wrapper


@keyboard_input
def get_input(prompt):
    return raw_input(prompt)
