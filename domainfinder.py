
import itertools
import os
from collections import defaultdict

# alpino parsing
import spacy_alpino

badwords = ["in", "de", "het", "een", "zijn", "hebben", "heb", "ben", "bent", "hebt", "heeft", "had", "was", "waren", "hadden", "ik", "jij", "wij", "hij", "zij", "hun",
            "hen", "elk", "wel", "ja", "nee", "of", "aan", "uit", "open", "dicht", "klaar", "voor", "je", "jouw", "me", "mijn", "zijn", "haar", "met"]

coronawords = ["corona", "covid", "covid-19", "ncov", "biontech", "astrazeneca", "moderna", "pfizer", "immuniteit", "intensive", "care", "quarantaine", "viroloog", "vaccin",
               "reproductiefactor", "rivm", "prik", "epidemie", "ic-patienten", "ic", "ic-opname", "sars", "ic-arts", "1.5 meter", "1,5 meter", "isolatie", "besmettingsgraad",
               "beademing", "besmettingen", "wuhan", "pandemie", "lockdown"]

sentence = "ik heb pech"

outputlist = []
sentencelist = []

fulldomains = False

nlp = spacy_alpino.load()

# Newest updates: we add corona words
# Newest upgrades: we disregard words that are not nouns, verbs, adjectives or proper nouns
# Newest upgrades: we convert to lower() first
# Newest upgrades: in our evaluation, we take the difference slightly into account


def outputevaluator(outputlist):
    global sentencelist

    # If there is only one output, we add substantial weight to it
    if len(outputlist) == 1:
        sentencelist.append((outputlist[0][0], 4))
        return

    if len(outputlist) == 2:
        if outputlist[0][1] == outputlist[1][1]:
            sentencelist.append((outputlist[0][0], 3))
            sentencelist.append((outputlist[1][0], 3))
        else:
            sentencelist.append((outputlist[0][0], 3))

            # if the the first one is 2 times the second one
            if outputlist[0][1] > outputlist[1][1] * 2:
                sentencelist.append((outputlist[1][0], 1))
            else:
                sentencelist.append((outputlist[1][0], 2))
        return

    if len(outputlist) >= 3:

        if outputlist[0][1] == outputlist[1][1]:
            sentencelist.append((outputlist[0][0], 3))
            sentencelist.append((outputlist[1][0], 3))
            if outputlist[1][1] == outputlist[2][1]:
                sentencelist.append((outputlist[2][0], 3))
            else:
                sentencelist.append((outputlist[2][0], 1))
        else:
            sentencelist.append((outputlist[0][0], 3))
            if outputlist[1][1] == outputlist[2][1]:

                #if the the first is twice or more the second one
                if outputlist[0][1] > outputlist[1][1] * 2:
                    sentencelist.append((outputlist[1][0], 1))
                    sentencelist.append((outputlist[2][0], 1))
                else:
                    sentencelist.append((outputlist[1][0], 2))
                    sentencelist.append((outputlist[2][0], 2))
            else:
                sentencelist.append((outputlist[1][0], 2))
                sentencelist.append((outputlist[2][0], 1))

        if len(outputlist) > 3 and outputlist[3][1] == outputlist[2][1]:
            sentencelist.append((outputlist[3][0], 1))

        if len(outputlist) > 4 and outputlist[4][1] == outputlist[2][1]:
            sentencelist.append((outputlist[4][0], 1))

        if len(outputlist) > 5 and outputlist[5][1] == outputlist[2][1]:
            sentencelist.append((outputlist[5][0], 1))

        if len(outputlist) > 6 and outputlist[6][1] == outputlist[2][1]:
            sentencelist.append((outputlist[6][0], 1))
        return

    # if len(outputlist) > 4:
     #   if outputlist[3][1] == outputlist[4][1]:
      #      sentencelist.append((outputlist[4][0], 1))


def trim_cat(cwd, f, le):

    f = f.replace(str(cwd), "")
    f = f[1:]
    f = f.replace(".txt", "")

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
    # get current directory
    cwd = os.getcwd()

    # get all subfolders of current directory
    subfolders = [f.path for f in os.scandir(cwd) if f.is_dir()]

    # create search terms
    var1 = f" {word} "
    var2 = f";{word};"
    var3 = f" {word};"
    var4 = f";{word} "

    global outputlist

    # traverse all files inside subfolders of the current directory
    for folder in subfolders:
        for filename in os.listdir(folder):
            f = os.path.join(folder, filename)

            # checking if it is a txt file
            if os.path.isfile(f) and f.find(".txt") != -1:

                # open file and read it
                file = open(f, 'r')
                text = file.read()

                count1 = text.count(var1)
                count2 = text.count(var2)
                count3 = text.count(var3)
                count4 = text.count(var4)
                #print(str(count1), str(count2), str(count3), str(count4))

                totalcount = count1 + count2 + count3 + count4

                f = trim_cat(cwd, f, len(os.listdir(folder)))

                # and not (count3 == 1 and totalcount == 1)): #f.find("factotum") == -1 and
                if totalcount > 0 and (f.find("alg") == -1):
                    outputlist.append((f, totalcount))


def sentencehandler(sentence):
    global sentencelist
    global outputlist

    alpinosen = nlp(sentence)

    for i in range(len(alpinosen)):
        t = alpinosen[i]
        word = str(t.orth_).lower()
        pos = t.pos_
        print(word, pos)
        if str(pos) in {"VERB", "NOUN", "ADJ", "PROPN"} or word in coronawords:
            print(f"MATCH:{word} {str(pos)}")
            outputlist = []
            main_sen(word)

    # assemble list
    res = defaultdict(int)
    for i in sentencelist:
        res[i[0]] += int(i[1])

    toshow = dict(sorted(res.items(), key=lambda item: item[1]))
    print(toshow)

    # reset list and dict
    sentencelist = []
    outputlist = []
    res.clear()


def main_sen(word):
    global outputlist
    global sentencelist

    if word in badwords:
        return None

    # stores counts inside outputlist
    get_counts(word)

    # sort the list on value
    outputlist.sort(key=lambda y: y[1])

    # reverse it to start high
    outputlist.reverse()

    print(outputlist)

    # evaluate output
    outputevaluator(outputlist)


def main(word):
    global outputlist

    if word in badwords:
        print("word does not have domain")
        return

    # stores counts inside outputlist
    get_counts(word)

    # sort the list on value
    outputlist.sort(key=lambda y: y[1])

    # reverse it to start high
    outputlist.reverse()

    # print list
    for occ in outputlist[:5]:
        print(occ)

    # reset list
    outputlist = []


while True:
    inp = input(
        "Do you want to predict domain for a word or a sentence? \nType s for sentence and w for word. \n")
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
