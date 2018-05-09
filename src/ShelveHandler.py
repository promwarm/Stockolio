"""
A program to handle shelve-requests.
"""

import os
import shelve


def load_shelve(path_and_file, key):
    """ Retrieves the object in a shelve, but the shelve has to exist, otherwise returns None. """

    # If no path and file is given or no key is given, return None
    if not path_and_file or not key:
        return None

    path, file = os.path.split(path_and_file)

    # We could have entered a single file, without path, but if we do give a path, we have to know if it exists
    if path and not os.path.exists(path):
        return None

    # Check whether required shelve-files exist
    shelve_files = [f'{file}.bak', f'{file}.dat', f'{file}.dir']

    for filename in shelve_files:
        complete_filename = os.path.join(path, filename)
        if not(os.path.exists(complete_filename)):
            return None

    # Shelve exists, return its data, unless key is not found
    shelve_data = shelve.open(path_and_file)
    try:
        key_data = shelve_data[key]
    except KeyError:
        return None
    finally:
        shelve_data.close()

    return key_data


my_stocks = load_shelve('Data/Portfolio', 'myStocks')
print(my_stocks)

def saveShelve(file, key, object):
    print('hi')

    # def saveListOfStocks(list_of_stocks):
    #     d = shelve.open('Data/Portfolio')
    #     d['myStocks'] = list_of_stocks
    #     d.close()
    #

# myDir = 'D:\\Projecten\\Python\\AutomateTheBoringStuff_byPromwarm\\Chapter 8 - Reading and writing files\\textfiles'
# if os.path.exists(myDir):
#     print('file exists')
#     filelist = os.listdir((myDir))
#
# for filename in filelist:
#     completeFilename = os.path.join(myDir, filename)
#     if os.path.isfile(completeFilename) and completeFilename.lower().endswith('.txt'):
#         fileHandle = open(completeFilename)
#         content = fileHandle.read


