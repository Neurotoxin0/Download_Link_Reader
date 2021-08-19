import os, shutil, zipfile, time
path = os.path.split(os.path.realpath(__file__))[0] + '\\'
archived_dir = path + 'archived'                            
os.chdir(path)                                            
out = open("output.txt", "a", encoding='utf-8')
file_count, link_count = 0, 0


keyword = ["ed2k://","magnet:"]                         # keyword for download link
ignore_dir = ["archived"]                               # ignore certain dirs
ignore_file = ["output.txt"]                            # ignore txt files with certain names
ignore_content = []                                     # ignore certain contents


def CLI():
    # Add time stamp to output.txt
    out.writelines("##################################################")
    out.writelines(time.strftime("%Y%m%d %H:%M:%S", time.localtime()))
    out.writelines("##################################################\n")

    # Looping CLI
    while True:
        os.system('cls')
        print("\
\n--------------------------------------------------\n\
Current keyword for download link: " + str(keyword) + "\n\
Current ignored dirs: " + str(ignore_dir) + "\n\
Current ignored files: " + str(ignore_file) + "\n\
Current ignored contents: " + str(ignore_content) + "\n\
-------------------------\
            ")
        print("\
Command Options: \n\
    0\tProceed with default\n\
    1\tEdit keyword for download link\n\
    2\tAdd dir that need to be ignored\n\
    3\tAdd file name that need to be ignored\n\
    4\tAdd contents that need to be ignored\n\
    5\tEnd Script\n\
            ")
        cmd = input("Please input command: ")

        # Default Setting
        if cmd == "0":
            os.system('cls')
            unzip()
            process()
            return end()
        
        # Edit keyword for download link
        elif cmd == "1":
            while True:
                os.system('cls')
                print("\
\n-------------------------\n\
Edit keyword for download link\
\n-------------------------\n\
Current keyword for download link: " + str(keyword) + "\n\n\
    1\tAdd keyword for download link\n\
    2\tRemove keyword for download link\n\
    3\tBack to Main Menu\n\
                    ")
                cmd = input("Please input command: ")
                if cmd == "3":  break
                else:
                    if not (cmd == "1" or cmd == "2"): 
                        print("\n-------------------------\nInvalid Command", end = '')
                        "Press Any Key To Go Back"
                        continue
                    while True:
                        key = str(input("\nPlease enter keyword, once a time and put space to end: "))

                        if key == "" or key == " ": break

                        if cmd == "1": 
                            if not key in keyword: keyword.append(key)
                            else: print("Keyword Exist!")
                           
                        else:   # cmd == "2"
                            try:    keyword.remove(key)
                            except: print("\n-------------------------\nKeyword Not Exist!", end = '')
        
        # Edit dir that need to be ignore
        elif cmd == "2":
            while True:
                os.system('cls')
                print("\
\n-------------------------\n\
Add dir that need to be ignore\
\n-------------------------\n\
Current ignored dirs: " + str(ignore_dir) + "\n\n\
    1\tAdd dir name into ignore list\n\
    2\tRemove dir name from ignore list\n\
    3\tBack to Main Menu\n\
                    ")
                cmd = input("Please input command: ")
                if cmd == "3":  break
                else:
                    if not (cmd == "1" or cmd == "2"): 
                        print("\n-------------------------\nInvalid Command", end = '')
                        "Press Any Key To Go Back"
                        continue
                    while True:
                        key = str(input("\nPlease enter dir name, once a time and put space to end: "))

                        if key == "" or key == " ": break

                        if cmd == "1": 
                            if not key in ignore_dir: ignore_dir.append(key)
                            else: print("Dir Name Exist!")
                           
                        else:
                            try:    ignore_dir.remove(key)
                            except: print("\n-------------------------\nDir Name Not Exist!", end = '')
        
        # Edit file name that need to be ignored
        elif cmd == "3":
            while True:
                os.system('cls')
                print("\
\n-------------------------\n\
Add file name that need to be ignored\
\n-------------------------\n\
Current ignored files: " + str(ignore_file) + "\n\n\
    1\tAdd file into ignore list\n\
    2\tRemove file from ignore list\n\
    3\tBack to Main Menu\n\
                    ")
                cmd = input("Please input command: ")
                if cmd == "3":  break
                else:
                    if not (cmd == "1" or cmd == "2"): 
                        print("\n-------------------------\nInvalid Command", end = '')
                        "Press Any Key To Go Back"
                        continue
                    while True:
                        key = str(input("\nPlease enter file name, once a time and put space to end: "))

                        if key == "" or key == " ": break

                        if cmd == "1": 
                            if not key in ignore_file: ignore_file.append(key)
                            else: print("File Name Exist!")
                           
                        else:
                            try:    ignore_file.remove(key)
                            except: print("\n-------------------------\nFile Name Not Exist!", end = '')    
        
        # Edit contents that need to be ignored
        elif cmd == "4":
            while True:
                os.system('cls')
                print("\
\n-------------------------\n\
Add contents that need to be ignored\
\n-------------------------\n\
Current ignored contents: " + str(ignore_content) + "\n\n\
    1\tAdd content into ignore list\n\
    2\tRemove content from ignore list\n\
    3\tBack to Main Menu\n\
                    ")
                cmd = input("Please input command: ")
                if cmd == "3":  break
                else:
                    if not (cmd == "1" or cmd == "2"): 
                        print("\n-------------------------\nInvalid Command", end = '')
                        "Press Any Key To Go Back"
                        continue
                    while True:
                        key = str(input("\nPlease enter content, once a time and put space to end: "))

                        if key == "" or key == " ": break

                        if cmd == "1": 
                            if not key in ignore_content: ignore_content.append(key)
                            else: print("Content Exist!")
                           
                        else:
                            try:    ignore_content.remove(key)
                            except: print("\n-------------------------\nContent Not Exist!", end = '') 

        # End script
        elif cmd == "5": return end()           

        # Catch
        else: 
            print("\n-------------------------\nInvalid Command", end = '')
            input("Press Any Key To Go Back")


'''Process Zip File'''
def unzip():
    print("\n------------------------Unziping------------------------")
    if not os.path.exists(archived_dir): os.makedirs(archived_dir)
    
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(('zip','.rar','.tar', '.gz', '.7z')):  print("Unziping File: " + file, end = '\t') 
            
            # Zip File
            if file.endswith('.zip'): 
                try:
                    tmp = zipfile.ZipFile(file)
                    for files in tmp.namelist(): tmp.extract(files)
                    tmp.close()
                except: print("Failed")
                else:
                    print("Success")
                    shutil.move(file, archived_dir)
    print("------------------------Finish------------------------\n")


'''Process Files'''
def process():
    print("------------------------Processing------------------------")
    global file_count
    
    for root, dirs, files in os.walk(path):
        for file in files:
            os.chdir(root)
            
            if file.endswith('.txt'):
                print("Processing File: " + file, end = '\t')
                
                if file in ignore_file: print("Ignore")
                else:
                    print("Processed")
                    file_count += 1
                    search(file)
                    print("------------------------")


'''Looking For Download Link'''        
def search(txt_file):
    global link_count
    tmp = open(txt_file, "r", encoding='utf-8')
    
    for line in tmp.readlines():
        link = any(key if key in line else False for key in keyword)
        ignore = any(key if key in line else False for key in ignore_content)

        if link and not ignore:
            if '\n' in line: line = line.strip("\n")
            link_count += 1
            print(line + "\n")
            out.writelines(line + "\n")       
    tmp.close()


def end():
    out.close()
    print("\n" + str(file_count) + " files processed, " + str(link_count) + " links found")
    print("------------------------Finish------------------------\n")
    try: os.removedirs(archived_dir)
    except: pass
    input("Press Any Key To Exit")
    return  