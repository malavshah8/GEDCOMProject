import argparse
import os
import sys

from src.parser import GEDCOMParser
from prettytable import PrettyTable
from src.userStoriesValidation import story_validation

#authors of the project
__author__ = "Parth Pandya, Malav Shah, Sukanya Rangarajan, Rajat Kinkhabwlal"
__email__ = "ppandya4@stevens.edu, mshah64@stevens.edu, srangar1@stevens.edu, rkinkhab@stevens.edu"

#default file path

FILENAME = 'gedcom_files/fail/Family_for_US17.ged'
#FILENAME = '/Users/malavshah/GEDCOMProject/gedcom_files/fail/Family.ged'

x = PrettyTable()
y = PrettyTable()

# main function for taking the file path
def main():
    # Allow for arguments to be passed for filename
    arg_parser = argparse.ArgumentParser()
    action = arg_parser.add_mutually_exclusive_group()
    action.add_argument("-f", "--file", nargs="?", const=FILENAME,
                        default=FILENAME,
                        help="Specify a specific file to run GEDCOM parser on. \
                        Default is " + FILENAME)

    arguments = arg_parser.parse_args()
    path = arguments.file
    if os.path.exists(path):
        print("Path accepted")
        individual, families = GEDCOMParser(path)
    else:
        print("[!!] File \"%s\" does not exist.\nExiting..." % path)
        exit(-1)

    # Check for user stories
    story_validation(individual, families)

    #printing values
    printSummary(individual, families)

# function for printing the list of individuals and families to
def printSummary(individual, families):
    print("\n")
    # for printing Individuals
    x.field_names = ["id","Name","Birthday","Sex","Death Date","Alive","Child","Spouse"]
    for line in individual:
        attrs = vars(line)
        x.add_row(attrs.values())

    print(x)

#    print(', '.join("%s: %s" % item for item in attrs.items()))

    print('----------------------------------------------------------------------------------------------------------------------------------------')
    # For printing Families
    y.field_names = ["Fid","Marriage","Husband","Husband Name","Wife","Wife Name","Children","Divorce"]
    for line in families:
        attrs = vars(line)
        y.add_row(attrs.values())
#        print (', '.join("%s: %s" % item for item in attrs.items()))
    print(y)

if __name__ == '__main__':
    sys.stdout = open("output.txt","w")
    main()
    sys.__stdout__.close()