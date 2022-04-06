
import os


def main(word):

    #get current directory
    cwd = os.getcwd()

    #get all subfolders of current directory
    subfolders = [ f.path for f in os.scandir(cwd) if f.is_dir() ]

    outputlist = []

    #traverse all files inside subfolders of the current directory
    for folder in subfolders:
        for filename in os.listdir(folder):
            f = os.path.join(folder, filename)
            
            # checking if it is a txt file
            if os.path.isfile(f) and f.find(".txt") != -1:

                #open file and read it
                file = open(f, 'r')
                text = file.read()

                var1 = " " + word + " "
                var2 = ";" + word + ";"
                var3 = " " + word + ";"
                var4 = ";" + word + " "

                count1 = text.count(var1)
                count2 = text.count(var2)
                count3 = text.count(var3)
                count4 = text.count(var4)

                totalcount = count1 + count2 + count3 + count4
                if totalcount != 0:

                    #adjust word
                    f = f.replace(str(cwd),"")
                    f = f[1:]
                    f = f.replace(".txt","")

                    if len(os.listdir(folder)) == 1:
                        slash = f.find("\\")
                        if slash != -1:
                            f = f[slash+1:]

                    if f.find("factotum") == -1:
                        outputlist.append((f, totalcount))
                    #print(f'{f}: occurrences: {totalcount}')

    #sort the list on value
    outputlist.sort(key=lambda y: y[1])

    #reverse it to start high
    outputlist.reverse()

    #print list
    for occ in outputlist[:5]:
        print(occ)

while True:
    word = input("Select a word to find domains for: \n")
    main(word)
    print("")
