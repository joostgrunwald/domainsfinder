
import os


def main(word):

    cwd = os.getcwd()

    subfolders = [ f.path for f in os.scandir(cwd) if f.is_dir() ]

    for folder in subfolders:
        for filename in os.listdir(folder):
            f = os.path.join(folder, filename)
            
            # checking if it is a file
            if os.path.isfile(f) and f.find(".txt") != -1:
                text = f.read()
                if text.find(word) != -1:
                    print(f)

word = input("Select a word to find domains for: \n")
main(word)
