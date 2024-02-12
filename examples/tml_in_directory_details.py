#!/usr/bin/env python3

import os
import sys
#import argparse

from thoughtspot_tml import *
from thoughtspot_tml.utils import *
from thoughtspot_tml.exceptions import *

# Command line script to parse local directory with TML files and display back useful information
# Necessary when storing TML just with GUID for filename in a SDLC process

# Look for a directory or filename as 1st argument, otherwise use local working directory
if len(sys.argv) == 1:
    directory = os.getcwd()
else:
    directory = sys.argv[1]
    # Correct for additional slash at the end
    if directory[-1] == "/":
        directory = directory[0:-1]

def parse_tml_file(filename, directory=None):
    output_lines = []
    if filename.find('.tml') != -1:
        if directory is None:
            file_path = filename
        else:
            file_path = directory + "/" + filename

        tml_cls = determine_tml_type(path=file_path)
        try:
            tml_obj = tml_cls.load(path=file_path)

            guid = tml_obj.guid
            content_name = tml_obj.name

            # You could get additional details here from tml_obj and then print them:

            output_lines.append("{} | {} | {}".format(filename, content_name, guid))
        except TMLDecodeError as e:

            print("Skipping {} due to error:".format(file_path))
            print(e)

        for line in output_lines:
            print(line)



# parse single file
if directory.find('.tml') != -1:
    parse_tml_file(filename=directory)
else:
    dir_list = os.listdir(directory)
    for filename in dir_list:
        parse_tml_file(filename=filename, directory=directory)