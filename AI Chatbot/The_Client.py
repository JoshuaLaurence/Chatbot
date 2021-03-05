#Person-Based Chatbot
import time
from math import *
import random
from rake_nltk import Rake
import os
import secrets
from random import randrange

General_Conversation_Questions = []
General_Conversation_Answers = []
Default_Responses = []
Personal_Math_Messages =[]
When_You_Do_Not_Know = []
Information_Database = {}
All_Users = []
All_Users_List = []
FirstName = ""

AllFiles = os.listdir()
for e in AllFiles:
    if e.endswith(".htd"):
        All_Users_List.append(e)

for d in All_Users_List:
    All_Users_List[All_Users_List.index(d)] = ((d.split(".")[0]).title()).replace("_"," ")

All_Users = All_Users_List

#Chatbot Introduction Menu
Chatbot_Identity = ""
while True:
    Chatbot_Identity_Temp = str(input("Who would you like to speak to (Full Name), or type 'users' for a User List: "))
    usersTriedUserList = False
    if Chatbot_Identity_Temp == "users":
        print(" ")
        usersTriedUserList = True
        for c in All_Users:
            print("-",c,"\n")
    if (Chatbot_Identity_Temp in All_Users) and (usersTriedUserList == False):
        FirstName = str((Chatbot_Identity_Temp.split(" ")[0] + ": ").upper())
        Chatbot_Identity_Temp = Chatbot_Identity_Temp.lower()
        Chatbot_Identity_Temp = str(Chatbot_Identity_Temp.replace(" ","_") + ".htd")
        Chatbot_Identity = Chatbot_Identity_Temp
        print("Loading Personality...\n")
        break
    elif (Chatbot_Identity_Temp not in All_Users) and (usersTriedUserList == False):
        print("Sorry we don't appear to have a User by that name. Please Try Again")

#Make Usable Data from Chatbot File
file = open(Chatbot_Identity, "r")
Chatbot_Information = file.readlines()
file.close()
Chatbot_Information = [i for i in Chatbot_Information if i != "\n"]
for j in range(len(Chatbot_Information)):
    if "\n" in Chatbot_Information[j]:
        Chatbot_Information[j] = Chatbot_Information[j].strip("\n")

indexOfGeneralConversation = Chatbot_Information.index("GENERAL CONVERSATION:")
indexOfInformationDatabase = Chatbot_Information.index("INFORMATION DATABASE:")
for p in range(1, indexOfGeneralConversation):
    if Chatbot_Information[p].endswith(", "):
        Default_Responses.append(Chatbot_Information[p])
    elif Chatbot_Information[p].endswith("... "):
        Personal_Math_Messages.append(Chatbot_Information[p])
    else:
        When_You_Do_Not_Know.append(Chatbot_Information[p])

#Create Information Index
for k in range(indexOfInformationDatabase + 1, len(Chatbot_Information)):
    if Chatbot_Information[k].startswith("*S,* "):
        subjectTitle = Chatbot_Information[k][5:]
        Information_Database[subjectTitle] = []
    else:
        if "." in Chatbot_Information[k]:
            SentencesOfInformation = Chatbot_Information[k].split(". ")
            for l in SentencesOfInformation:
                Information_Database[subjectTitle].append(l)
        else:
            Information_Database[subjectTitle].append(Chatbot_Information[k])

#Filter General Conversation
for m in range(indexOfGeneralConversation + 1, indexOfInformationDatabase - 1):
    if Chatbot_Information[m].startswith("*T,* "):
        General_Conversation_Questions.append([])
        General_Conversation_Answers.append([])
        currentList = len(General_Conversation_Questions) - 1
    elif Chatbot_Information[m].startswith("*Q,* "):
        question = (Chatbot_Information[m][5:]).lower()
        General_Conversation_Questions[currentList].append(question)
    elif Chatbot_Information[m].startswith("*A,* "):
        answer = (Chatbot_Information[m][5:])
        General_Conversation_Answers[currentList].append(answer)

def validateSyntax(expression):
    functions = {'__builtins__': None}
    variables = {'__builtins__': None}
    functions = {'acos': acos,
                'asin': asin,
                'atan': atan,
                'atan2': atan2,
                'ceil': ceil,
                'cos': cos,
                'cosh': cosh,
                'degrees': degrees,
                'exp': exp,
                'fabs':fabs,
                'floor': floor,
                'fmod': fmod,
                'frexp': frexp,
                'hypot': hypot,
                'ldexp': ldexp,
                'log': log,
                'log10': log10,
                'modf': modf,
                'pow': pow,
                'radians': radians,
                'sin': sin,
                'sinh': sinh,
                'sqrt': sqrt,
                'tan': tan,
                'tanh': tanh}
    variables = {'e': e, 'pi': pi}
    try:
        eval(expression, variables, functions)
    except (SyntaxError, NameError, ZeroDivisionError):
        return "Error"
    else:
        return eval(expression, variables, functions)

def informationDatabaseAdvanceSearch(wordsToSearch, sentenceList, currentIndex):
    global chosenSentence
    chosenSentence = ""
    newSentenceList = sentenceList
    if (len(newSentenceList) == 0) or(len(newSentenceList) < 5 and len(newSentenceList) > 1) or (currentIndex == len(wordsToSearch)):
        if len(newSentenceList) == 0:
            chosenSentence = ""
        else:
            choice = random.choice(newSentenceList)
            chosenSentence = choice
    else:
        forDeletion = []
        for a in range(0, len(sentenceList)):
            if wordsToSearch[currentIndex] not in newSentenceList[a].lower():
                forDeletion.append(a)
        forDeletion.reverse()   
        for b in forDeletion:
            del newSentenceList[b]
        currentIndex += 1
        informationDatabaseAdvanceSearch(wordsToSearch, newSentenceList, currentIndex)
    
        

def chatting():
    User_Input = str(input("YOU: "))
    if User_Input.lower() == "bye":
        quit()
    fullResponse = ""
    repsonse = "NOT FOUND IN GENERAL CONVERSATION DATABASE"
    mathResult = validateSyntax(User_Input.lower())
    if mathResult != "Error":
        fullResponse = str(FirstName + random.choice(Personal_Math_Messages) + str(mathResult))
    else:
        for n in General_Conversation_Questions:
            r = Rake()
            r.extract_keywords_from_text(User_Input)
            searchableWords = r.get_ranked_phrases()
            for o in n:
                if (User_Input.lower() == o.lower()) or (User_Input.lower() in o.lower()) or any(str(v) in o.lower() for v in searchableWords):
                    currentAnswerList = General_Conversation_Questions.index(n)
                    repsonse = random.choice(General_Conversation_Answers[currentAnswerList])
                    fullResponse = str(FirstName + repsonse)
                    break
        if repsonse == "NOT FOUND IN GENERAL CONVERSATION DATABASE":
            r = Rake()
            r.extract_keywords_from_text(User_Input)
            searchableWords = r.get_ranked_phrases()
            listOfChosenSentences = []
            starterPhrase = random.choice(Default_Responses)
            for q in list(Information_Database.keys()):
                informationDatabaseAdvanceSearch(searchableWords, Information_Database[q], 0)
                listOfChosenSentences.append(chosenSentence)
            listOfChosenSentences = [x for x in listOfChosenSentences if x]
            if not len(listOfChosenSentences):
                fullResponse = FirstName
            else:
                response = str(starterPhrase + random.choice(listOfChosenSentences))
                fullResponse = str(FirstName + response)
        if fullResponse == FirstName:
            fullResponse = str(FirstName + random.choice(When_You_Do_Not_Know))
    print(fullResponse)

                

while True:
    chatting()
    
