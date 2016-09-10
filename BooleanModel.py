# global variables

def PrintDictionary(dictionary):
    for key in dictionary:
        print(dictionary[key], key)
# End of PrintDictionary


class BooleanModel:
    __stopWords = set() # Set of stop words that can be configured by client
    # These terms will be filtered as they are common occur almost in all documents.

    __booleanOperators = {'AND', 'OR', 'NOT', 'BUT'}  # These are the boolean operators.  # BUT==AND

    __termDocIncidenceMatrix = dict()


    def AddStopWord(self, stopWord):
        ''' Add new stop word '''
        self.__stopWords.add(stopWord)


    def RemoveStopWord(self, stopWord):
        ''' Remove stop word '''
        self.__stopWords.remove(stopWord)


    def AddStopWords(self, stopWordSet):
        ''' Add new stop words '''
        self.__stopWords.update(stopWordSet)


    def RemoveStopWords(self, stopWordSet):
        ''' Remove stop words '''
        self.__stopWords.difference_update(stopWordSet)


    # This function creates term document incidence matrix from document to Contains map.
    def ConstructTermDocIncidenceMatrix(self, docToContaints):
        uniqueTerms = set()  # set of unique terms accross all docs
        docTodocTermsSet = dict()  # map of document to terms in document

        for doc in docToContaints:
            termlist = docToContaints[doc].upper().split(' ')  # split to find terms in file
            print("\n Terms in Doucment ", doc)
            print(termlist)
            docTermsSet = set()

            for term in termlist:
                # Filter Stop words and boolean operators
                if term not in self.__stopWords and term not in self.__booleanOperators:
                    uniqueTerms.add(term)
                    docTermsSet.add(term)

            docTodocTermsSet[doc] = docTermsSet

        print("\ndocument To document Terms Set")
        PrintDictionary(docTodocTermsSet)
        print("\n")

        for term in uniqueTerms:
            termIncidenceVector = list()

            self.__termDocIncidenceMatrix[term] = termIncidenceVector

            for doc in docTodocTermsSet:
                if term in docTodocTermsSet[doc]:
                    termIncidenceVector.append(1)
                else:
                    termIncidenceVector.append(0)
            print(termIncidenceVector, term)


    # End of ConstructTermDocIncidenceMatrix


    def __OperateBoolean(self, resultIncidenceVector, booleanOperator, hasNotOperator, nextTermIncidenceVector):
        if hasNotOperator:
            NotVector(nextTermIncidenceVector)

        if booleanOperator == "AND" or booleanOperator == "BUT":
            for index in range(len(resultIncidenceVector)):
                if resultIncidenceVector[index] == 1 and nextTermIncidenceVector[index] == 1:
                    resultIncidenceVector[index] = 1
                else:
                    resultIncidenceVector[index] = 0

        elif booleanOperator == "OR":
            for index in range(len(resultIncidenceVector)):
                if resultIncidenceVector[index] == 1 or nextTermIncidenceVector[index] == 1:
                    resultIncidenceVector[index] = 1
                else:
                    resultIncidenceVector[index] = 0

                    # print ("\n Result :", resultIncidenceVector)


    # end of booleanOperator


    def __NotVector(self, nextTermIncidenceVector):
        for n in range(len(nextTermIncidenceVector)):
            if nextTermIncidenceVector[n] == 1:
                nextTermIncidenceVector[n] = 0
            else:
                nextTermIncidenceVector[n] = 1
    # end of NotVector


    def QueryProcessor(self, query):
        upperQuery = query.upper()
        print("\nYour query is ", upperQuery)

        queryList = upperQuery.split(' ')
        print("\n Query List : ", queryList)

        booleanOperator = str()

        hasPrevTerm = False
        hasNextTerm = False
        hasOperator = False
        hasNotOperator = False

        nextTermIncidenceVector = []
        resultIncidenceVector = []

        # At start we will look for Term or NOT operator.
        searchForTerm = True
        searchForOperator = False
        searchForNot = True

        for term in queryList:
            '''
            print ("\nTerm is :", term, " Looking for : ")
            if searchForTerm:
                print ("Term ")
            if searchForOperator:
                print ("BitWiseOperator Other than NOT ")
            if searchForNot:
                print ("BitWise Not Operator ")'''

            foundSomething = False

            if searchForTerm and term in self.__termDocIncidenceMatrix:
                if not hasPrevTerm and not hasOperator and not hasNotOperator:
                    resultIncidenceVector = list(self.__termDocIncidenceMatrix[term])
                    hasPrevTerm = True

                    print("\n", resultIncidenceVector, " : ", term)
                else:  # There are operators or other terms before it so this is next term
                    nextTermIncidenceVector = list(self.__termDocIncidenceMatrix[term])
                    hasNextTerm = True
                    print("\n", nextTermIncidenceVector, " : ", term)

                searchForTerm = False  # stop looking for term, look for operator now
                searchForOperator = True
                searchForNot = False  # after term is should be AND or OR operator and not NOT.

                # print("Found : Term")
                foundSomething = True

            elif searchForOperator and term in self.__booleanOperators and not term == 'NOT':
                booleanOperator = term
                hasOperator = True
                print("\n Operator : ", term)

                # in next iteration look for Term or Not operator
                searchForTerm = True
                searchForOperator = False
                searchForNot = True

                # print("Found : BitWise Operator other than NOT")

                foundSomething = True

            elif searchForNot and term in self.__booleanOperators and term == 'NOT':
                if not hasNotOperator:
                    hasNotOperator = True
                else:
                    hasNotOperator = False  # multiple NOT NOT = Yes so will be ignored.

                print("\n Operator : ", term)

                # Not operator should be followed by Term of Another Not operator so search for them
                searchForTerm = True
                searchForOperator = False
                searchForNot = True

                # print("Found : BitWise Not Operator")

                foundSomething = True

            if not foundSomething:
                print("\n Did not find what we were looking for in query terms, ignoring ", term)

                continue

            if hasNotOperator and hasNextTerm and not hasPrevTerm:
                self.__NotVector(nextTermIncidenceVector)
                resultIncidenceVector = list(nextTermIncidenceVector)

                print("\n", resultIncidenceVector, " : Result")
                # Not is processed on nextTerm so reset them
                hasNotOperator = False
                hasNextTerm = False
                hasPrevTerm = True  # result is now previous term

            elif hasPrevTerm and hasOperator and hasNextTerm:
                self.__OperateBoolean(resultIncidenceVector, booleanOperator, hasNotOperator, nextTermIncidenceVector)

                print("\n", resultIncidenceVector, " : Result")
                # Operator is processed on next term so reset them
                hasOperator = False
                hasNextTerm = False


        return resultIncidenceVector

    # End of QueryProcessor
