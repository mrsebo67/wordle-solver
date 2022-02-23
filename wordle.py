from tqdm import tqdm
import math

def generateIteration(n):
    if n == 0:
        return '', ''
    nums = []
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))
    tempString = ''.join(reversed(nums))

    while len(tempString) < 5:
        tempString = '0' + tempString

    guessedSpot = '1'
    guessedLetter = '1'
    for i in range(len(tempString)):
        if tempString[i] == '1':
            guessedSpot += str(i+1)
        elif tempString[i] == '2':
            guessedLetter += str(i+1)

    #print(tempString)
    return guessedSpot, guessedLetter
    
def getInformation(word, guessedSpot, guessedLetter, listOfWords):

    
    
    
    listOfWordsGuessedSpot = []

    listOfGoodWords = []
    
    for tryWord in listOfWords:

        if len(guessedSpot) == 0:
            listOfWordsGuessedSpot.append(tryWord)
            continue
        
        goodWord = True
        for i in range(len(guessedSpot)):
            if tryWord[int(guessedSpot[i])-1] != word[int(guessedSpot[i])-1]:
                goodWord = False
                break
        if goodWord:
            listOfWordsGuessedSpot.append(tryWord)
       
    for tryWord in listOfWordsGuessedSpot:

        if len(guessedLetter) == 0:
            listOfGoodWords.append(tryWord)
            continue
        
        goodWord = True
        for letter in guessedLetter:
            if word[int(letter)-1] not in tryWord or word[int(letter)-1] == tryWord[int(letter)-1]:
                goodWord = False
                break
        
        if goodWord:
            listOfGoodWords.append(tryWord)
    
    dictOfGoodLetters = set()
    for elem in guessedSpot:
        dictOfGoodLetters.add(elem)
    for elem in guessedLetter:
        dictOfGoodLetters.add(elem) 

    listOfGoodWordsV2 = []
    testLetters = '12345'
    for tryWord in listOfGoodWords:
        goodWord = True
        for letter in testLetters:
            if letter not in dictOfGoodLetters and word[int(letter)-1] in tryWord:
                goodWord = False
                break

        if goodWord:
            listOfGoodWordsV2.append(tryWord)
        
    return listOfGoodWordsV2

def getInformationOfWord(word, listOfWords):

    information = 0

    wordCount = len(listOfWords)

    for i in range(0, 243):

        guessedSpot, guessedLetter = generateIteration(i)

        numOfPossibleWords = len(getInformation(word, guessedSpot, guessedLetter, listOfWords))

        if numOfPossibleWords == 0:
            information += 0
        else:
            information += (numOfPossibleWords/wordCount)*math.log2(1/(numOfPossibleWords/wordCount))
        
    return information    

def getBestWord(currentWord, listOfGoodWords):

    if currentWord in listOfGoodWords:
        listOfGoodWords.remove(currentWord)
    bestWord = listOfGoodWords[1]
    bestWordInformation = getInformationOfWord(listOfGoodWords[1], listOfGoodWords)

    i = 0;
    for tryWord in tqdm(listOfGoodWords, ascii=True):
        tempInformation = getInformationOfWord(tryWord, listOfGoodWords)
        if tempInformation > bestWordInformation:
            bestWordInformation = tempInformation
            bestWord = tryWord

    return bestWord
             
with open('wordleWords.txt', 'r') as f:
    listWords = f.readlines()
    listPossibleAnswers = listWords[0].split(',')
    listPossibleTries = listWords[2].split(',')


for i in range(len(listPossibleAnswers)):
     listPossibleAnswers[i] = listPossibleAnswers[i].replace('"', '')

listPossibleAnswers[-1] = listPossibleAnswers[-1].replace('\n', '')

for i in range(len(listPossibleTries)):
    listPossibleTries[i] = listPossibleTries[i].replace('"', '')


#getInformationOfWord('crane')

listPossibleTries.extend(listPossibleAnswers)
oldWords = listPossibleTries

i = 0;
while i < 6:
    word = input('word: ')
    guessedSpot = input('guessedSpot: ')
    guessedLetter = input('guessedLetter: ')
    listWords = getInformation(word, guessedSpot, guessedLetter, oldWords)
    if(len(listWords)==1):
        print('you Won, gratz')
        break
    print(getBestWord(word, listWords))
    oldWords = listWords
    i += 1
