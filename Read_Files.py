import os, shutil, zipfile

keyword = ["ed2k"]                                      # keywork for download link
ignore_list = ["output.txt"]                            # ignore txt file with certain names
path = os.path.split(os.path.realpath(__file__))[0]     
os.chdir(path)                                          


'''Process Zip File'''
def unzip():
    print("\n------------------------Unziping------------------------")
    
    archived_dir = './archived'
    if not os.path.exists(archived_dir):
        os.makedirs(archived_dir)

    for file in os.listdir(path):
        if file.endswith('.zip'):
            print("Unziping File: " + file)
            tmp = zipfile.ZipFile(file)
            
            for files in tmp.namelist(): 
                tmp.extract(files)
            
            tmp.close()
            shutil.move(file, archived_dir)
    
    print("------------------------Finish------------------------\n")


'''Process Files'''
def process():
    print("------------------------Processing------------------------")

    for root, dirs, files in os.walk(path):
        for file in files:
            os.chdir(root)
            
            if file.endswith('.txt'):
                for ignore in ignore_list:
                    if file != ignore:
                        print("------------------------")
                        search(file)
                        print("------------------------")

    out.close()

    print("------------------------Finish------------------------\n")


'''Looking For Download Link'''        
def search(txt_file):
    print("Processing File: " + txt_file)
    tmp = open(txt_file, "r")
    
    for line in tmp.readlines():
        for key in keyword:
            if key in line:
                print(line + "\n")
                out.writelines(line + "\n")
                
    tmp.close()
   



if __name__ == '__main__':
    unzip()
    out = open("output.txt", "a")
    process()