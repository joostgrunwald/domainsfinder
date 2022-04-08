
import os
from collections import defaultdict

badwords = ["in", "de", "het", "een", "zijn", "hebben", "heb", "ben", "bent", "hebt", "heeft", "had", "was", "waren", "hadden", "ik", "jij", "wij", "hij", "zij", "hun",
            "hen", "elk", "wel", "ja", "nee", "of", "aan", "uit", "open", "dicht","klaar","voor","je","jouw","me","mijn","zijn","haar"]

sentence = "ik heb pech"

outputlist = []
sentencelist = []

fulldomains = False

def outputevaluator(outputlist):
    global sentencelist
    #add top 3 elements with top 3 scores to sentencelist
    if len(outputlist) == 1:
        sentencelist.append((outputlist[0][0],4))
        return
    
    if len(outputlist) == 2:
        if outputlist[0][1] == outputlist[1][1]:
            sentencelist.append((outputlist[0][0],3))
            sentencelist.append((outputlist[1][0],3))
        else:
            sentencelist.append((outputlist[0][0],3))
            sentencelist.append((outputlist[1][0],2))
        return
    
    if len(outputlist) >= 3:
        if outputlist[0][1] == outputlist[1][1]:
            sentencelist.append((outputlist[0][0],3))
            sentencelist.append((outputlist[1][0],3))
            if outputlist[1][1] == outputlist[2][1]:
                sentencelist.append((outputlist[2][0],3))
            else:
                sentencelist.append((outputlist[2][0],1))
        else: 
            sentencelist.append((outputlist[0][0],3))
            if outputlist[1][1] == outputlist[2][1]:
                sentencelist.append((outputlist[1][0],2))
                sentencelist.append((outputlist[2][0],2))
            else:
                sentencelist.append((outputlist[1][0],2))
                sentencelist.append((outputlist[2][0],1))                
        return
        
def trim_cat(cwd, f, le):

    f = f.replace(str(cwd),"")
    f = f[1:]
    f = f.replace(".txt","")

    if fulldomains == True:
        if le == 1:
            slash = f.find("\\")
            if slash != -1:
                f = f[slash+1:]
    else:
        slash = f.find("\\")
        if slash != -1:
            f = f[:slash]

    return f
                            
def get_counts(word):
    #get current directory
    cwd = os.getcwd()

    #get all subfolders of current directory
    subfolders = [ f.path for f in os.scandir(cwd) if f.is_dir() ]

    #create search terms
    var1 = " " + word + " "
    var2 = ";" + word + ";"
    var3 = " " + word + ";"
    var4 = ";" + word + " "

    global outputlist

    #traverse all files inside subfolders of the current directory
    for folder in subfolders:
        for filename in os.listdir(folder):
            f = os.path.join(folder, filename)
            
            # checking if it is a txt file
            if os.path.isfile(f) and f.find(".txt") != -1:

                #open file and read it
                file = open(f, 'r')
                text = file.read()

                count1 = text.count(var1)
                count2 = text.count(var2)
                count3 = text.count(var3)
                count4 = text.count(var4)
                #print(str(count1), str(count2), str(count3), str(count4))

                totalcount = count1 + count2 + count3 + count4

                f = trim_cat(cwd, f, len(os.listdir(folder)))

                if totalcount > 0 and (f.find("alg") == -1): #and not (count3 == 1 and totalcount == 1)): #f.find("factotum") == -1 and
                    outputlist.append((f, totalcount))

def sentencehandler(sentence):
    global sentencelist
    global outputlist
    
    words = sentence.split()
    for word in words:
         out = main_sen(word)

    #assemble list
    res = defaultdict(int)
    for i in sentencelist:
        res[i[0]] += int(i[1])
            
    #print list
    print(list(res.items()))

    #reset list and dict
    sentencelist = []
    outputlist = []
    res.clear()
        
def main_sen(word):
    global outputlist
    global sentencelist
    
    if word in badwords:
        return None

    #stores counts inside outputlist
    get_counts(word)

    #sort the list on value
    outputlist.sort(key=lambda y: y[1])

    #reverse it to start high
    outputlist.reverse()

    #evaluate output
    outputevaluator(outputlist)

def main(word):
    global outputlist
    
    if word in badwords:
        print("word does not have domain")
        return

    #stores counts inside outputlist
    get_counts(word)

    #sort the list on value
    outputlist.sort(key=lambda y: y[1])

    #reverse it to start high
    outputlist.reverse()

    #print list
    for occ in outputlist[:5]:
        print(occ)

    #reset list
    outputlist = []

while True:
    inp = input("Do you want to predict domain for a word or a sentence? \nType s for sentence and w for word. \n")
    if (inp == "s"):
        sent = input("Select a sentence to find domains for: \n")
        sentencehandler(sent)
        print("")
    elif (inp == "w"):
        word = input("Select a word to find domains for: \n")
        main(word)
        print("")
    else:
        print("you should select either w or s")
    
