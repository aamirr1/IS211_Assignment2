#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS-211 Week 2 Assignment 2"""

import datetime
import csv
import urllib2
import argparse
import logging


parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', help="Enter a URL linking to a .csv file.")
args = parser.parse_args()

logging.basicConfig(filename='errors.log', level=logging.ERROR)
logger = logging.getLogger('assignment2')


def downloadData(url):
    """This function will open an url provided by user"""
    
    file1 = urllib2.urlopen(url)
    return file1


def processData(datafile):
    """This function will return all the information from csv file located in the web"""
    
    readfile = csv.DictReader(datafile)
    newdict = {}

    for exp, line in enumerate(readfile):
        try:
            born = datetime.datetime.strptime(line['birthday'], '%d/%m/%Y')
            newdict[line['id']] = (line['name'], born)
        except:
            logging.error('Error processing line #{} for ID# {}'.format(
                exp, line['id']))

    return newdict


def displayPerson(id, personData):
    """This function will search for ID in the list and return the name associated with requested ID"""
    
    id_number = str(id)
    if id_number in personData.keys():
        print 'Person #{} is {} with a birthday of {}'.format(id, personData[id_number][0], datetime.datetime.strftime(personData[id_number][1], '%Y-%m-%d'))
    else:
        print 'No user found with that ID.'


def main():
    """This main function will combine few other functions to form a one full program"""
    
    if not args.url:
        raise SystemExit
    try:
        csvData = downloadData(args.url)
    except urllib2.URLError:
        print 'This URL is not valid. Please enter a valid URL.'
        raise
    else:
        personData = processData(csvData)
        Selected_ID = raw_input('Please enter an ID# for lookup:')
        print Selected_ID
        Selected_ID = int(Selected_ID)
        if Selected_ID <= 0:
            print 'Exiting program.'
            raise SystemExit
        else:
            displayPerson(Selected_ID, personData)
            main()

if __name__ == '__main__':
    main()
