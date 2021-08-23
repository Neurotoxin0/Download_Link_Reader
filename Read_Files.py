import os, shutil, time, zipfile, tarfile, gzip
path = (os.path.split(os.path.realpath(__file__))[0] + "/").replace("\\\\", "/").replace("\\", "/")
archived_dir = path + "Archived/"  
zip_dir = archived_dir+ "Zip_Files/"
file_dir = archived_dir + "Processed_Files/"                 
os.chdir(path)                                            
out = open("output.txt", "a", encoding='utf-8')
file_count, link_count = 0, 0


keyword = ["ed2k://","magnet:"]                         # 下载链接关键字 | keyword for download link
ignore_dir = ["Archived", "__pycache__"]                # 忽略的文件夹 | ignore certain dirs
ignore_file = ["output.txt"]                            # 忽略的文件 | ignore txt files with certain names
ignore_content = []                                     # 忽略的内容 | ignore certain contents
RAR_Support = False                                     # RAR 支持


def CLI(lan):
    global RAR_Support
    # 添加时间戳到输出文件 | Add time stamp to output.txt
    out.writelines("##################################################")
    out.writelines(time.strftime("%Y%m%d %H:%M:%S", time.localtime()))
    out.writelines("##################################################\n")

    while True:
        os.system('cls')

        print(\
"\n--------------------------------------------------\n" + \
["当前下载链接关键字: ", "Current keyword for download link: "][lan] + str(keyword) + "\n" + \
["当前忽略的文件夹: ", "Current ignored dirs: "][lan] + str(ignore_dir) + "\n" + \
["当前忽略的文件: ", "Current ignored files: "][lan] + str(ignore_file) + "\n" + \
["当前忽略的内容: ", "Current ignored contents: "][lan] + str(ignore_content) + "\n" + \
["RAR 支持(需要手动安装RAR支持包!): ", "RAR Support(RAR scripts are required!): "][lan] + str(RAR_Support) + "\n\n" + \

["命令选项: ", "Command Options: "][lan] + "\n" + \
    "0\t" + ["开始执行", "Executing"][lan] + "\n" + \
    "1\t" + ["修改下载链接关键", "Edit keyword for download link"][lan] + "\n" + \
    "2\t" + ["修改当前忽略的文件夹", "Add dir that need to be ignored"][lan] + "\n" + \
    "3\t" + ["修改当前忽略的文件", "Add file name that need to be ignored"][lan] + "\n" + \
    "4\t" + ["修改当前忽略的内容", "Add contents that need to be ignored"][lan] + "\n" + \
    "5\t" + ["切换 RAR 支持选项", "Switch RAR Support"][lan] + "\n" + \
    "6\t" + ["结束脚本", "End Script"][lan] + "\n"  \
            )
        
        cmd = input(["请输入命令: ", "Please input command: "][lan])

        # 开始执行 | Executing
        if cmd == "0":
            os.system('cls')
            unzip(lan)
            process(lan)
            rmdirs(lan)
            return end(lan)
        
        # 修改下载链接关键字 | Edit keyword for download link
        elif cmd == "1":
            while True:
                os.system('cls')
                
                print(\
"\n-------------------------\n" + \
["修改下载链接关键字", "Edit keyword for download link"][lan] + \
"\n-------------------------\n" + \
["当前下载链接关键字: ", "Current keyword for download link: "][lan] + str(keyword) + "\n\n" + \
    "1\t" + ["添加下载链接关键字", "Add keyword for download link"][lan] + "\n" + \
    "2\t" + ["移除下载链接关键字", "Remove keyword for download link"][lan] + "\n" + \
    "3\t" + ["返回主菜单", "Back to Main Menu"][lan] + "\n" \
                    )
                
                cmd = input(["请输入命令: ", "Please input command: "][lan])
                
                if cmd == "3":  break
                else:
                    if not (cmd == "1" or cmd == "2"): 
                        print("\n-------------------------\n" + ["无效命令", "Invalid Command"][lan], end = '')
                        input(["按任意键来返回","Press Any Key To Go Back"][lan])
                        continue
                    
                    while True:
                        key = str(input("\n" + ["请输入一个关键字，留空来返回: ", "Please enter keyword, once a time and put space to end: "][lan]))

                        if key == "" or key == " ": break

                        if cmd == "1": 
                            if not key in keyword: keyword.append(key)
                            else: print(["关键字已存在!", "Keyword Exist!"][lan])
                           
                        else:   # cmd == "2"
                            try:    keyword.remove(key)
                            except: print("\n-------------------------\n" + ["关键字不存在!", "Keyword Not Exist!"][lan], end = '')
        
        # 修改忽略文件夹 | Edit dir that need to be ignore
        elif cmd == "2":
            while True:
                os.system('cls')
                
                print(\
"\n-------------------------\n" + \
["修改忽略的文件夹", "Edit dir that need to be ignore"][lan] + \
"\n-------------------------\n" + \
["当前忽略的文件夹: ", "Current ignored dirs: "][lan] + str(ignore_dir) + "\n\n" + \
    "1\t" + ["添加忽略的文件", "Add dir name into ignore list"][lan] + "\n" + \
    "2\t" + ["移除忽略的文件夹", "Remove dir name from ignore list"][lan] + "\n" + \
    "3\t" + ["回到主菜单", "Back to Main Menu"][lan] + "\n" \
                    )
                
                cmd = input(["请输入命令: ", "Please input command: "][lan])
                
                if cmd == "3":  break
                else:
                    if not (cmd == "1" or cmd == "2"): 
                        print("\n-------------------------\n" + ["无效命令", "Invalid Command"][lan], end = '')
                        input(["按任意键来返回", "Press Any Key To Go Back"][lan])
                        continue
                    
                    while True:
                        key = str(input("\n" + ["请输入一个文件夹名，留空来返回: ", "Please enter dir name, once a time and put space to end: "][lan]))

                        if key == "" or key == " ": break

                        if cmd == "1": 
                            if not key in ignore_dir: ignore_dir.append(key)
                            else: print(["文件夹名已存在", "Dir Name Exist!"][lan])
                           
                        else:
                            try:    ignore_dir.remove(key)
                            except: print("\n-------------------------\n" + ["文件夹名不存在!", "Dir Name Not Exist!"][lan], end = '')
        
        # 修改忽略文件 | Edit file name that need to be ignored
        elif cmd == "3":
            while True:
                os.system('cls')
                
                print(\
"\n-------------------------\n" + \
["修改忽略的文件", "Edit file name that need to be ignored"][lan] + \
"\n-------------------------\n" + \
["当前忽略的文件: ", "Current ignored files: "][lan] + str(ignore_file) + "\n\n" + \
    "1\t" + ["添加忽略的文件", "Add file into ignore list"][lan] + "\n" + \
    "2\t" + ["移除忽略的文件", "Remove file from ignore list"][lan] + "\n" + \
    "3\t" + ["返回主界菜单", "Back to Main Menu"][lan] + "\n" \
                    )
                
                cmd = input(["请输入命令: ", "Please input command: "][lan])
                
                if cmd == "3":  break
                else:
                    if not (cmd == "1" or cmd == "2"): 
                        print("\n-------------------------\n" + ["无效命令", "Invalid Command"][lan], end = '')
                        input(["按任意键来返回", "Press Any Key To Go Back"][lan]) 
                        continue
                    
                    while True:
                        key = str(input("\n" + ["请输入一个文件名，留空来返回: ", "Please enter file name, once a time and put space to end: "][lan]))

                        if key == "" or key == " ": break

                        if cmd == "1": 
                            if not key in ignore_file: ignore_file.append(key)
                            else: print(["文件名已存在!", "File Name Exist!"][lan])
                           
                        else:
                            try:    ignore_file.remove(key)
                            except: print("\n-------------------------\n" + ["文件名不存在!", "File Name Not Exist!"][lan], end = '')    
        
        # 修改忽略内容 | Edit contents that need to be ignored
        elif cmd == "4":
            while True:
                os.system('cls')
                
                print(\
"\n-------------------------\n" + \
["修改忽略的内容", "Edit contents that need to be ignored"][lan] + \
"\n-------------------------\n" + \
["当前忽略的内容: ", "Current ignored contents: "][lan] + str(ignore_content) + "\n\n" + \
    "1\t" + ["添加忽略的内容", "Add content into ignore list"][lan] + "\n" + \
    "2\t" + ["移除忽略的内容", "Remove content from ignore list"][lan] + "\n" + \
    "3\t" + ["回到主菜", "Back to Main Menu"][lan] + "\n" \
                    )
                
                cmd = input(["请输入命令: ", "Please input command: "][lan])
                
                if cmd == "3":  break
                else:
                    if not (cmd == "1" or cmd == "2"): 
                        print("\n-------------------------\n" + ["无效命令", "Invalid Command"][lan], end = '')
                        input(["按任意键来返回", "Press Any Key To Go Back"][lan])
                        continue
                    
                    while True:
                        key = str(input("\n" + ["请输入一个内容，留空来返回: ", "Please enter content, once a time and put space to end: "][lan]))

                        if key == "" or key == " ": break

                        if cmd == "1": 
                            if not key in ignore_content: ignore_content.append(key)
                            else: print(["内容已存在!", "Content Exist!"][lan])
                           
                        else:
                            try:    ignore_content.remove(key)
                            except: print("\n-------------------------\n" + ["内容不存在!", "Content Not Exist!"][lan], end = '') 

        # 切换 RAR 支持 | Switch RAR Support
        elif cmd == "5":
            print("\n==================================================")
            print(["请确保额外的RAR脚本已经被安装至 python/scripts!", "Please Make Sure Extra RAR Scripts have been install to python/scripts!"][lan] + "\n")
            print(["RAR 支持选项已被切换", "RAR Support Switched"][lan])
            print("==================================================\n")
            input(["按任意键来返回", "Press Any Key To Go Back"][lan])
            if not RAR_Support: RAR_Support = True
            else:               RAR_Support = False
        
        # 结束脚本 | End script
        elif cmd == "6": return            

        # Catch
        else: 
            print("\n-------------------------\n" + ["无效命令", "Invalid Command"][lan], end = '')
            input(["按任意键来返回", "Press Any Key To Go Back"][lan])


# 处理压缩文件 | Process Zip File
def unzip(lan):
    print("\n------------------------" + ["解压", "Unziping"][lan] + "------------------------")
    if not os.path.exists(archived_dir): os.makedirs(archived_dir)
    if not os.path.exists(zip_dir): os.makedirs(zip_dir)
    
    for root, dirs, files in os.walk(path):
        
        for file in files:
            if any(key if key in root else False for key in ignore_dir): continue
            else: os.chdir(root)
            
            if file.endswith(('zip','.tar','.rar', '.gz', '.7z')):  
                print("Unziping File: " + file, end = '\t') 
            
                # Zip File
                if file.endswith('.zip'): tmp = zipfile.ZipFile(file)
                # Tar File
                elif file.endswith('.tar'): tmp = tarfile.open(file)
                # RAR File
                elif file.endswith('.rar'): 
                    if RAR_Support:
                        import rarfile 
                        tmp = rarfile.RarFile(file)
                # GZ / 7z File
                else:   print(["需要手动解压", "Manual Unzip Required"][lan] + "\t", end = '')
            
                try:  
                    tmp.extractall()
                    tmp.close()
                except: print(["失败", "Failed"][lan])
                else:
                    print(["成功", "Success"][lan])
                    try: shutil.move(file, zip_dir)
                    except: pass
    print("------------------------" + ["完成", "Finish"][lan] + "------------------------\n\n")


# 处理文件 | Process Files
def process(lan):
    print("------------------------" + ["开始处理", "Processing"][lan] + "------------------------")
    global file_count
    if not os.path.exists(file_dir): os.makedirs(file_dir)
    
    for root, dirs, files in os.walk(path):

        for file in files:
            if any(key if key in root else False for key in ignore_dir): continue
            else: os.chdir(root)
            
            if file.endswith('.txt'):
                print(["处理文件: ", "Processing File: "][lan] + file, end = '\t')
                
                if file in ignore_file: print(["忽略", "Ignore"][lan])
                else:
                    print(["已处理", "Processed"][lan])
                    file_count += 1
                    search(file)
                    try: shutil.move(file, file_dir)
                    except: pass
                    print("------------------------")
    print("------------------------" + ["完成", "Finish"][lan] + "------------------------\n\n")


# 寻找下载链接 | Looking For Download Link        
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


def rmdirs(lan):
    print("------------------------" + ["删除空文件夹以及缓存文件", "Deleting Empty Dirs & Caches"][lan] + "------------------------")
    for item in os.listdir(path):
        tmp = path + item

        if os.path.isdir(tmp): 
            print(item + "\t", end = '')
            if item == "__pycache__":
                print(["将在命令行结束后自动删除", "Scheduled After CLI Ends"][lan])
            else:
                try:    os.removedirs(tmp)
                except: print("pass"); pass
                else:   print("success")

    
    print("------------------------" + ["完成", "Finish"][lan] + "------------------------\n\n")


def end(lan):
    out.close()
    print("\n==================================================")
    print(str(file_count) + [" 个文件已处理，找到 ", " files processed, "][lan] + str(link_count) + [" 个链接", " links found"][lan])
    print("==================================================\n")
    input(["按任意键退出并打开输出文件...", "Press Any Key To Exit And Open Output File..."][lan])
    os.startfile(path + "output.txt")
    return  