
import os


def main(word):

    #get current directory
    cwd = os.getcwd()

    #get all subfolders of current directory
    subfolders = [ f.path for f in os.scandir(cwd) if f.is_dir() ]

    #traverse all files inside subfolders of the current directory
    for folder in subfolders:
        for filename in os.listdir(folder):
            f = os.path.join(folder, filename)
            
            # checking if it is a txt file
            if os.path.isfile(f) and f.find(".txt") != -1:

                #open file and read it
                file = open(f, 'r')
                text = file.read()

                #find word in file
                if text.find(word) != -1:
                    
                    #adjust word
                    f = f.replace(str(cwd),"")
                    f = f[1:]
                    f = f.replace(".txt","")

                    if len(os.listdir(folder)) == 1:
                        slash = f.find("\\")
                        if slash != -1:
                            f = f[slash+1:]
                            
                    print(f)
                    print(text.count(word))

word = input("Select a word to find domains for: \n")
main(word)
