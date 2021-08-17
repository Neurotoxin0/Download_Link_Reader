import os

path = os.path.split(os.path.realpath(__file__))[0]     # get current path  (where script is located)
os.chdir(path)                                          # changine working dir to current path

'''Process Single File'''
def process(file):
    tmp = open(file, "r")
    lines = tmp.readlines()
    print(lines)
    tmp.close()

'''Main'''
for item in os.listdir(path):
    if item.endswith('txt'):
        print("\n------------------------")
        print("Processing File: " + item + "\n")
        process(item)
        print("\n------------------------")
