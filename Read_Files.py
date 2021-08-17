import os, zipfile

path = os.path.split(os.path.realpath(__file__))[0]     # get current path  (where script is located)
os.chdir(path)                                          # changing working dir to current path


'''Process Single File'''
def process(txt_file):
    tmp = open(txt_file, "r")
    lines = tmp.readlines()
    print(lines)
    tmp.close()


'''Process Zip File'''
def unzip():
    print("\n------------------------")
    for file in os.listdir(path):
        if file.endswith('zip'):
            print("Unziping File: " + file)
            tmp = zipfile.ZipFile(file)
            for files in tmp.namelist(): tmp.extract(files)
            tmp.close()
    print("------------------------")


unzip()
