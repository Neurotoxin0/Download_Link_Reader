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
                
                if file in ignore_file:
                    print("Ignore")
                    continue
                else:
                    print("Processed")
                    file_count += 1
                    search(file)
                    print("------------------------")

    out.close()
    print("\n" + str(file_count) + " files processed, " + str(link_count) + " links found")
    print("------------------------Finish------------------------\n")
    try: os.removedirs(archived_dir)
    except: pass
    input("Press Any Key To Exit")


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




if __name__ == '__main__':
    # Adding Time Stamp
    out.writelines("------------------------------------------------")
    out.writelines(time.strftime("%Y%m%d %H:%M:%S", time.localtime()))
    out.writelines("------------------------------------------------\n")
    unzip()
    process()