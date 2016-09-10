import os


def PrintDictionary(dictionary):
    for key in dictionary:
        print(dictionary[key], key)


# This function read text files located at 'path' and returns map of documentId to containts of document
def ReadDocuements(path, extention,  docToContaints):
    docId = 0
    # lets walks all file in directory and read files that end with 'extention' specified
    for file in os.listdir(path):
        if file.endswith(extention):
            print(file)
            f = open(path + file, 'r')  # compose full file path by adding path and file name
            contains = f.read()  # read file to fetch contains
            print(contains)
            docToContaints[docId] = contains  # add docId to Contains in map
            docId += 1  # increment doc ID

    print("\n Document to contains of document")

    PrintDictionary(docToContaints)

    print("\n")


