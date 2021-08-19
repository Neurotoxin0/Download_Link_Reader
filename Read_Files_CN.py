import os, shutil, zipfile, time
path = os.path.split(os.path.realpath(__file__))[0] + '\\'
archived_dir = path + 'archived'                            
os.chdir(path)                                            
out = open("output.txt", "a", encoding='utf-8')
file_count, link_count = 0, 0


keyword = ["ed2k://","magnet:"]                         # 下载链接关键字
ignore_dir = ["archived"]                               # 忽略的文件夹
ignore_file = ["output.txt"]                            # 忽略的文件
ignore_content = []                                     # 忽略的内容


def CLI():
    # 添加时间戳到输出文件
    out.writelines("##################################################")
    out.writelines(time.strftime("%Y%m%d %H:%M:%S", time.localtime()))
    out.writelines("##################################################\n")

    # 循环命令行
    while True:
        os.system('cls')
        print("\
\n--------------------------------------------------\n\
当前下载链接关键字: " + str(keyword) + "\n\
当前忽略的文件夹: " + str(ignore_dir) + "\n\
当前忽略的文件: " + str(ignore_file) + "\n\
当前忽略的内容: " + str(ignore_content) + "\n\
-------------------------\
            ")
        print("\
命令选项: \n\
    0\t开始执行\n\
    1\t修改下载链接关键字\n\
    2\t修改当前忽略的文件夹\n\
    3\t修改当前忽略的文件\n\
    4\t修改当前忽略的内容\n\
    5\t结束脚本\n\
            ")
        cmd = input("请输入命令: ")

        # 开始执行
        if cmd == "0":
            os.system('cls')
            unzip()
            process()
            return end()
        
        # 修改下载链接关键字
        elif cmd == "1":
            while True:
                os.system('cls')
                print("\
\n-------------------------\n\
修改下载链接关键字\
\n-------------------------\n\
当前下载链接关键字: " + str(keyword) + "\n\n\
    1\t添加下载链接关键字\n\
    2\t移除下载链接关键字\n\
    3\t返回主菜单\n\
                    ")
                cmd = input("请输入命令: ")
                if cmd == "3":  break
                else:
                    if not (cmd == "1" or cmd == "2"): 
                        print("\n-------------------------\n无效命令", end = '')
                        input("按任意键来返回")
                        continue
                    while True:
                        key = str(input("\n请输入一个关键字，留空来返回: "))

                        if key == "" or key == " ": break

                        if cmd == "1": 
                            if not key in keyword: keyword.append(key)
                            else: print("关键字已存在!")
                           
                        else:   # cmd == "2"
                            try:    keyword.remove(key)
                            except: print("\n-------------------------\n关键字不存在!", end = '')
        
        # 修改忽略文件夹
        elif cmd == "2":
            while True:
                os.system('cls')
                print("\
\n-------------------------\n\
修改忽略的文件夹\
\n-------------------------\n\
当前忽略的文件夹: " + str(ignore_dir) + "\n\n\
    1\t添加忽略的文件夹\n\
    2\t移除忽略的文件夹\n\
    3\t回到主菜单\n\
                    ")
                cmd = input("请输入命令: ")
                if cmd == "3":  break
                else:
                    if not (cmd == "1" or cmd == "2"): 
                        print("\n-------------------------\n无效命令", end = '')
                        input("按任意键来返回")
                        continue
                    while True:
                        key = str(input("\n请输入一个文件夹名，留空来返回: "))

                        if key == "" or key == " ": break

                        if cmd == "1": 
                            if not key in ignore_dir: ignore_dir.append(key)
                            else: print("文件夹名已存在")
                           
                        else:
                            try:    ignore_dir.remove(key)
                            except: print("\n-------------------------\n文件夹名不存在!", end = '')
        
        # 修改忽略文件
        elif cmd == "3":
            while True:
                os.system('cls')
                print("\
\n-------------------------\n\
修改忽略的文件\
\n-------------------------\n\
当前忽略的文件: " + str(ignore_file) + "\n\n\
    1\t添加忽略的文件\n\
    2\t移除忽略的文件\n\
    3\t返回主界菜单\n\
                    ")
                cmd = input("请输入命令: ")
                if cmd == "3":  break
                else:
                    if not (cmd == "1" or cmd == "2"): 
                        print("\n-------------------------\n无效命令", end = '')
                        input("按任意键来返回")
                        continue
                    while True:
                        key = str(input("\n请输入一个文件名，留空来返回: "))

                        if key == "" or key == " ": break

                        if cmd == "1": 
                            if not key in ignore_file: ignore_file.append(key)
                            else: print("文件名已存在!")
                           
                        else:
                            try:    ignore_file.remove(key)
                            except: print("\n-------------------------\n文件名不存在!", end = '')    
        
        # 修改忽略内容
        elif cmd == "4":
            while True:
                os.system('cls')
                print("\
\n-------------------------\n\
修改忽略的内容\
\n-------------------------\n\
当前忽略的内容: " + str(ignore_content) + "\n\n\
    1\t添加忽略的内容\n\
    2\t移除忽略的内容\n\
    3\t回到主菜单\n\
                    ")
                cmd = input("请输入命令: ")
                if cmd == "3":  break
                else:
                    if not (cmd == "1" or cmd == "2"): 
                        print("\n-------------------------\n无效命令", end = '')
                        input("按任意键来返回")
                        continue
                    while True:
                        key = str(input("\n请输入一个内容，留空来返回: "))

                        if key == "" or key == " ": break

                        if cmd == "1": 
                            if not key in ignore_content: ignore_content.append(key)
                            else: print("内容已存在!")
                           
                        else:
                            try:    ignore_content.remove(key)
                            except: print("\n-------------------------\n内容不存在!", end = '') 

        # 结束脚本
        elif cmd == "5": return end()           

        # Catch
        else: 
            print("\n-------------------------\n无效命令", end = '')
            input("按任意键来返回")


'''处理压缩文件'''
def unzip():
    print("\n------------------------解压------------------------")
    if not os.path.exists(archived_dir): os.makedirs(archived_dir)
    
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(('zip','.rar','.tar', '.gz', '.7z')):  print("解压文件: " + file, end = '\t') 
            
            # Zip File
            if file.endswith('.zip'): 
                try:
                    tmp = zipfile.ZipFile(file)
                    for files in tmp.namelist(): tmp.extract(files)
                    tmp.close()
                except: print("失败")
                else:
                    print("成功")
                    shutil.move(file, archived_dir)
    print("------------------------完成------------------------\n")


'''处理文件'''
def process():
    print("------------------------开始处理------------------------")
    global file_count
    
    for root, dirs, files in os.walk(path):
        for file in files:
            os.chdir(root)
            
            if file.endswith('.txt'):
                print("处理文件: " + file, end = '\t')
                
                if file in ignore_file: print("忽略")
                else:
                    print("已处理")
                    file_count += 1
                    search(file)
                    print("------------------------")


'''寻找下载链接'''        
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
    print("\n" + str(file_count) + " 个文件已处理，找到" + str(link_count) + " 个链接")
    print("------------------------Finish------------------------\n")
    try: os.removedirs(archived_dir)
    except: pass
    input("按任意键退出")
    return  