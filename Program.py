import ReadDocument
import BooleanModel

def main():

    path = 'C:/Docs/'

    docToContains = dict()

    ReadDocument.ReadDocuements(path, '.txt', docToContains)

    IBooleanModel = BooleanModel.BooleanModel()

    IBooleanModel.AddStopWords({'IN', 'AND', 'IT', 'OF', 'A', 'ON', 'FOR', 'IS', 'AN'})

    IBooleanModel.ConstructTermDocIncidenceMatrix(docToContains)

    while True:

        query = input("\nEnter your query :")

        if query == '':
            break

        resultIncidenceVector = IBooleanModel.QueryProcessor(query)

        print("\n\n Search Results are \n ")
        print(resultIncidenceVector, "\n\n")
        for index in range(len(resultIncidenceVector)):
            if resultIncidenceVector[index] == 1:
                print("\t doc id:", index, ": ", docToContains[index], "\n")

# End of main

# standard code to execute main when this script is executed.
if __name__ == '__main__':
    main()
