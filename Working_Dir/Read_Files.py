# /usr/bin/python
import os, shutil, time, zipfile, tarfile, json, logging
from logging import handlers


# ========================= 配置 | Config =========================
Output = "output.txt"                                   # 输出文件名称 | Output File's Name
Archived = "Archived"                                   # 归档文件夹名称 | Archive Folder Name
Zip_Folder = "Zip_Files"                                # 处理过的压缩文件存放的文件夹名称 | Folder Name For Processed Zips
File_Folder = "Processed_Files"                         # 处理过的文件存放的文件夹名称 | Folder Name For Processed Files
Keyword = ["ed2k://", "magnet:"]                        # 下载链接关键字 | keyword for download link
Ignore_dir = ["Working_Dir", "Archived"]                # 忽略的文件夹 | ignore certain dirs
Ignore_file = [Output]                                  # 忽略的文件 | ignore txt files with certain names
Ignore_content = []                                     # 忽略的内容 | ignore certain contents
RAR_Support = False                                     # RAR 支持
Debug = False                                           # Debug 模式
# =================================================================

# Env & Vars
Config_Exist = True
File_Count, Link_Count = 0, 0
Time = time.strftime("%Y.%m.%d@%H_%M_%S", time.localtime())   
Path = (os.path.split(os.path.realpath(__file__))[0] + "/").replace("\\\\", "/").replace("\\", "/")
Working_Path = Path.replace("/Working_Dir/", "/")
Archived_Dir = Working_Path + Archived + "/"
Zip_Dir = Archived_Dir + Zip_Folder + "/"
File_Dir = Archived_Dir + File_Folder + "/"
os.chdir(Path)               

# Logger
class Logger(object):
    level_relations = \
    {
        'debug':    logging.DEBUG,
        'info':     logging.INFO,
    }

    def __init__(self, log_file, level = 'info', format = "%(message)s"):
        self.logger = logging.getLogger(log_file)
        self.logger.setLevel(self.level_relations.get(level))
        format = logging.Formatter(format)
        
        # Output on CLI interface
        CLI = logging.StreamHandler()
        CLI.setFormatter(format)
        self.logger.addHandler(CLI)

        # Output to log file
        LOG = handlers.TimedRotatingFileHandler(filename = log_file, encoding = 'utf-8')
        LOG.setFormatter(format)
        self.logger.addHandler(LOG)

# Output & Log
Out = open("../" + Output, "a", encoding = 'utf-8')
if not os.path.exists("Log"): os.makedirs("Log")

try: tmp = open("config.json", "r", encoding='utf-8')
except: 
    Config_Exist = False; 
    pass
else:
    Debug = json.loads(tmp.readlines()[0])['Debug Mode']
    tmp.close()

if Debug:   Log = Logger("Log/" + Time + "---DEBUG.log", level = 'debug')
else:       Log = Logger("Log/" + Time + ".log")


# CLI
def CLI(lan):
    # Read Config
    if Config_Exist:
        Log.logger.info(["是否读取配置文件?", "Continue with local config?"][lan] + " (y/n) (" + ["默认: ", "Default: "][lan] + "y)\n> ")
        conf = Read()
    
        if conf == "n": pass
        else: Load(lan)

    # 添加时间戳到输出文件 | Add time stamp to output.txt
    Out.writelines("################################################## ")
    Out.writelines(Time)
    Out.writelines(" ##################################################\n")

    # CLI 开始 | CLI Start
    global RAR_Support, Debug
    while True:
        os.system('cls')

        Log.logger.info(\
"\n--------------------------------------------------\n" + \
["当前下载链接关键字: ", "Current keyword for download link: "][lan] + str(Keyword) + "\n" + \
["当前忽略的文件夹: ", "Current ignored dirs: "][lan] + str(Ignore_dir) + "\n" + \
["当前忽略的文件: ", "Current ignored files: "][lan] + str(Ignore_file) + "\n" + \
["当前忽略的内容: ", "Current ignored contents: "][lan] + str(Ignore_content) + "\n" + \
["RAR 支持(需要手动安装RAR支持包!): ", "RAR Support(RAR scripts are required!): "][lan] + str(RAR_Support) + "\n" + \
["Debug 模式: ", "Debug Mode: "][lan] + str(Debug) + "\n\n" + \

["命令选项: ", "Command Options: "][lan] + "\n" + \
    "Enter\t" + ["开始执行", "Executing"][lan] + "\n" + \
    "1\t" + ["修改下载链接关键", "Edit keyword for download link"][lan] + "\n" + \
    "2\t" + ["修改当前忽略的文件夹", "Edit dir that need to be ignored"][lan] + "\n" + \
    "3\t" + ["修改当前忽略的文件", "Edit file name that need to be ignored"][lan] + "\n" + \
    "4\t" + ["修改当前忽略的内容", "Edit contents that need to be ignored"][lan] + "\n" + \
    "5\t" + ["切换 RAR 支持选项", "Switch RAR Support"][lan] + "\n" + \
    "6\t" + ["储存&目录设置", "Archive & Dir Setting"][lan] + " (!)\n" + \
    "7\t" + ["清除本地配置文件", "Remove local config file"][lan] + "\n" + \
    "8\t" + ["切换 Debug 模式", "Switch Debug Mode"][lan] + "\n" + \
    "0\t" + ["保存并退出", "Save and Exit"][lan] + "\n"  \
            )
        
        Log.logger.info(["> 请输入命令: ", "> Please input command: "][lan])
        cmd = Read()

        # 开始执行 | Executing
        if cmd == " " or cmd == "" or cmd == "Enter":
            os.system('cls')
            Unzip(lan)
            Process(lan)
            Rmdirs(lan)
            return End(lan)
        
        # 修改下载链接关键字 | Edit keyword for download link
        elif cmd == "1":
            while True:
                os.system('cls')
                
                Log.logger.info(\
"\n------------------------- " + ["修改下载链接关键字", "Edit keyword for download link"][lan] + " -------------------------\n\n" + \
["当前下载链接关键字: ", "Current keyword for download link: "][lan] + str(Keyword) + "\n\n" + \
    "1\t" + ["添加下载链接关键字", "Add keyword for download link"][lan] + "\n" + \
    "2\t" + ["移除下载链接关键字", "Remove keyword for download link"][lan] + "\n" + \
    "3\t" + ["返回主菜单", "Back to Main Menu"][lan] + "\n" \
                    )
                
                Log.logger.info(["> 请输入命令: ", "> Please input command: "][lan])
                cmd = Read()

                if cmd == "3":  Save(lan); break
                else:
                    if not (cmd == "1" or cmd == "2"): 
                        Log.logger.info("\n------------------------- " + ["无效命令", "Invalid Command"][lan] + " -------------------------\n")
                        Back(lan); continue
                    
                    while True:
                        Log.logger.info("\n" + ["请输入一个关键字，留空来返回: ", "Please enter keyword, once a time and put space to end: "][lan])
                        key = Read()

                        if key == "" or key == " ": break

                        if cmd == "1": 
                            if not key in Keyword: Keyword.append(key)
                            else: Log.logger.info("\n------------------------- " + ["关键字已存在!", "Keyword Exist!"][lan] + " -------------------------\n")
                           
                        else:   # cmd == "2"
                            try:    Keyword.remove(key)
                            except: Log.logger.info("\n------------------------- " + ["关键字不存在!", "Keyword Not Exist!"][lan] + " -------------------------\n")
        
        # 修改忽略文件夹 | Edit dir that need to be ignore
        elif cmd == "2":
            while True:
                os.system('cls')
                
                Log.logger.info(\
"\n------------------------- " + ["修改忽略的文件夹", "Edit dir that need to be ignore"][lan] + " -------------------------\n\n" + \
["当前忽略的文件夹: ", "Current ignored dirs: "][lan] + str(Ignore_dir) + "\n\n" + \
    "1\t" + ["添加忽略的文件", "Add dir name into ignore list"][lan] + "\n" + \
    "2\t" + ["移除忽略的文件夹", "Remove dir name from ignore list"][lan] + "\n" + \
    "3\t" + ["回到主菜单", "Back to Main Menu"][lan] + "\n" \
                    )
                
                Log.logger.info(["> 请输入命令: ", "> Please input command: "][lan])
                cmd = Read()

                if cmd == "3":  Save(lan); break
                else:
                    if not (cmd == "1" or cmd == "2"): 
                        Log.logger.info("\n------------------------- " + ["无效命令", "Invalid Command"][lan] + " -------------------------\n")
                        Back(lan); continue
                    
                    while True:
                        Log.logger.info("\n" + ["请输入一个文件夹名，留空来返回: ", "Please enter dir name, once a time and put space to end: "][lan])
                        key = Read()

                        if key == "" or key == " ": break

                        if cmd == "1": 
                            if not key in Ignore_dir: Ignore_dir.append(key)
                            else: Log.logger.info("\n------------------------- " + ["文件夹名已存在", "Dir Name Exist!"][lan] + " -------------------------\n")
                           
                        else:
                            try:    Ignore_dir.remove(key)
                            except: Log.logger.info("\n------------------------- " + ["文件夹名不存在!", "Dir Name Not Exist!"][lan] + " -------------------------\n")
        
        # 修改忽略文件 | Edit file name that need to be ignored
        elif cmd == "3":
            while True:
                os.system('cls')
                
                Log.logger.info(\
"\n------------------------- " + ["修改忽略的文件", "Edit file name that need to be ignored"][lan] + " -------------------------\n\n" + \
["当前忽略的文件: ", "Current ignored files: "][lan] + str(Ignore_file) + "\n\n" + \
    "1\t" + ["添加忽略的文件", "Add file into ignore list"][lan] + "\n" + \
    "2\t" + ["移除忽略的文件", "Remove file from ignore list"][lan] + "\n" + \
    "3\t" + ["返回主界菜单", "Back to Main Menu"][lan] + "\n" \
                    )
                
                Log.logger.info(["> 请输入命令: ", "> Please input command: "][lan])
                cmd = Read()
                
                if cmd == "3":  Save(lan); break
                else:
                    if not (cmd == "1" or cmd == "2"): 
                        Log.logger.info("\n------------------------- " + ["无效命令", "Invalid Command"][lan] + " -------------------------\n")
                        Back(lan); continue
                    
                    while True:
                        Log.logger.info("\n" + ["请输入一个文件名，留空来返回: ", "Please enter file name, once a time and put space to end: "][lan])
                        key = Read()

                        if key == "" or key == " ": break

                        if cmd == "1": 
                            if not key in Ignore_file: Ignore_file.append(key)
                            else: Log.logger.info("\n------------------------- " + ["文件名已存在!", "File Name Exist!"][lan] + " -------------------------\n")
                           
                        else:
                            try:    Ignore_file.remove(key)
                            except: Log.logger.info("\n------------------------- " + ["文件名不存在!", "File Name Not Exist!"][lan] + " -------------------------\n")    
        
        # 修改忽略内容 | Edit contents that need to be ignored
        elif cmd == "4":
            while True:
                os.system('cls')
                
                Log.logger.info(\
"\n------------------------- " + ["修改忽略的内容", "Edit contents that need to be ignored"][lan] + " -------------------------\n\n" + \
["当前忽略的内容: ", "Current ignored contents: "][lan] + str(Ignore_content) + "\n\n" + \
    "1\t" + ["添加忽略的内容", "Add content into ignore list"][lan] + "\n" + \
    "2\t" + ["移除忽略的内容", "Remove content from ignore list"][lan] + "\n" + \
    "3\t" + ["回到主菜单", "Back to Main Menu"][lan] + "\n" \
                    )
                
                Log.logger.info(["> 请输入命令: ", "> Please input command: "][lan])
                cmd = Read()
                
                if cmd == "3":  Save(lan); break
                else:
                    if not (cmd == "1" or cmd == "2"): 
                        Log.logger.info("\n------------------------- " + ["无效命令", "Invalid Command"][lan] + " -------------------------\n")
                        Back(lan); continue
                    
                    while True:
                        Log.logger.info("\n" + ["请输入一个内容，留空来返回: ", "Please enter content, once a time and put space to end: "][lan])
                        key = Read()

                        if key == "" or key == " ": break

                        if cmd == "1": 
                            if not key in Ignore_content: Ignore_content.append(key)
                            else: Log.logger.info("\n------------------------- " + ["内容已存在!", "Content Exist!"][lan] + " -------------------------\n")
                           
                        else:
                            try:    Ignore_content.remove(key)
                            except: Log.logger.info("\n------------------------- " + ["内容不存在!", "Content Not Exist!"][lan] + " -------------------------\n") 

        # 切换 RAR 支持 | Switch RAR Support
        elif cmd == "5":
            if not RAR_Support: RAR_Support = True
            else:               RAR_Support = False

            Log.logger.info("\n==================================================")
            if RAR_Support: Log.logger.info(["请确保额外的RAR脚本已经被安装至 python/scripts!", "Please Make Sure Extra RAR Scripts have been install to python/scripts!"][lan] + "\n")
            Log.logger.info(["< RAR 支持选项已被切换 >", "< RAR Support Switched >"][lan])
            Log.logger.info("==================================================\n")
            Back(lan)
            
            
        
        # 储存&目录设置 | Archive & Dir Setting
        elif cmd == "6":
            global Output, Archived, Zip_Folder, File_Folder
            
            while True:
                os.system('cls')

                Log.logger.info(\
"\n------------------------- " + ["储存&目录设置", "Archive & Dir Setting"][lan] + " -------------------------\n\n" + \
["当前输出文件名称: ", "Current name for output file: "][lan] + Output + "\n" + \
["当前归档文件夹名称: ", "Current name for archive folder: "][lan] + Archived + "\n" + \
["处理过的压缩文件存放的文件夹名称: ", "Folder name for processed zips: "][lan] + Zip_Folder + "\n" + \
["处理过的文件存放的文件夹名称: ", "Folder name for processed files: "][lan] + File_Folder + "\n" + \

"\n===============" + \
["不建议修改，除非你知道自己在干什么", "Editting Not Recommand, MAKE SURE knowing what this does"][lan] + \
"===============\n\n" + \

["命令选项: ", "Command Options: "][lan] + "\n" + \
    "1\t" + ["修改输出文件名称", "Edit output file name"][lan] + "\n" + \
    "2\t" + ["修改归档文件夹名称", "Edit archive folder name"][lan] + "\n" + \
    "3\t" + ["处理压缩文件存档点名称", "Edit processed zips' folder name"][lan] + "\n" + \
    "4\t" + ["处理文件存档点名", "Edit processed files' folder name"][lan] + "\n" + \
    "5\t" + ["保存并退出脚本", "Save Changes and EXIT"][lan] + "\n" + \
    "6\t" + ["返回菜单", "Back to menu"][lan] \
                                )
                Log.logger.info(["> 请输入命令: ", "> Please input command: "][lan])
                cmd = Read()
                
                
                if cmd == "5":  Save(lan); return 
                elif cmd == "6": break
                else:
                    if cmd not in ["1", "2", "3", "4"]: 
                        Log.logger.info("\n------------------------- " + ["无效命令", "Invalid Command"][lan] + " -------------------------\n")
                        Back(lan); continue

                    if cmd == "1":   
                        Log.logger.info("\n" + ["请输入文件名: ", "Please enter file name: "][lan])   
                        key = Read()
                        
                        if (key != "") and (key != " "): 
                            Output = key
                            Log.logger.info("\n=========================\n" + ["已更改,将在脚本下次启动并读取后生效", "Set, Become effective when load config on next run"][lan] + "\n=========================\n")
                            Back(lan)
                        else: 
                            Log.logger.info("\n------------------------- " + ["无效名称", "Invalid Name"][lan] + " -------------------------\n")
                            Back(lan)

                    elif cmd == "2":  
                        Log.logger.info("\n" + ["请输入文件夹名: ", "Please enter folder name: "][lan])  
                        key = Read()
                        
                        if (key != "") and (key != " "): 
                            Archived = key
                            Log.logger.info("\n=========================\n" + ["已更改,将在脚本下次启动并读取后生效", "Set, Become effective when load config on next run"][lan] + "\n=========================\n")
                            Back(lan)
                        else: 
                            Log.logger.info("\n------------------------- " + ["无效名称", "Invalid Name"][lan] + " -------------------------\n")
                            Back(lan)

                    elif cmd == "3":    
                        Log.logger.info("\n" + ["请输入文件夹名: ", "Please enter folder name: "][lan])
                        key = Read()
                        
                        if (key != "") and (key != " "): 
                            Zip_Folder = key
                            Log.logger.info("\n=========================\n" + ["已更改,将在脚本下次启动并读取后生效", "Set, Become effective when load config on next run"][lan] + "\n=========================\n")
                            Back(lan)
                        else: 
                            Log.logger.info("\n------------------------- " + ["无效名称", "Invalid Name"][lan] + " -------------------------\n")
                            Back(lan)

                    elif cmd == "4":    
                        Log.logger.info("\n" + ["请输入文件夹名: ", "Please enter folder name: "][lan])
                        key = Read()
                        
                        if (key != "") and (key != " "): 
                            File_Folder = key
                            Log.logger.info("\n=========================\n" + ["已更改,将在脚本下次启动并读取后生效", "Set, Become effective when load config on next run"][lan] + "\n=========================\n")
                            Back(lan)
                        else: 
                            Log.logger.info("\n------------------------- " + ["无效名称", "Invalid Name"][lan] + " -------------------------\n")
                            Back(lan)

        # 清除本地配置文件 | Remove local config file
        elif cmd == "7":
            Log.logger.info(["是否确定删除?", "Confirm?"][lan] + " (y/n)\n >")
            confirm = Read()

            if confirm == "y": 
                try: 
                    os.remove("config.json")
                    Log.logger.info(["已删除, 将在下次启动时使用默认配置", "Deleted，use default config on next run"][lan])
                except: 
                    Log.logger.info(["删除失败, 可能原因: 配置文件被占用或不存在", "Failed to delete, possible reason: file is being used or do not exist"][lan])
                    pass
                
                return 0

        # Debug 模式 | Debug Mode
        elif cmd == "8":
            Log.logger.info("\n==================================================")
            Log.logger.info(["< 已切换 Debug 模式 >", "< Debug Mode Switched >"][lan])
            Log.logger.info("==================================================\n")
            Back(lan)
            
            if not Debug: Debug = True
            else:         Debug = False

        # 结束脚本 | End script
        elif cmd == "0": Save(lan); return            

        # Catch
        else: 
            Log.logger.info("\n------------------------- " + ["无效命令", "Invalid Command"][lan] + " -------------------------\n")
            Back(lan)

        # Save Config After Each Round
        Save(lan)  


# 处理压缩文件 | Process Zip File
def Unzip(lan):
    Log.logger.info("\n========================= " + ["解压", "Unzip "][lan] + " =========================")
    #if not os.path.exists(Archived_Dir): os.makedirs(Archived_Dir)
    if not os.path.exists(Zip_Dir): os.makedirs(Zip_Dir)
    
    for root, dirs, files in os.walk(Working_Path):    
        for file in files:
            if any(key if key in root else False for key in Ignore_dir): continue
            else: os.chdir(root)
            
            if file.endswith(('zip','.tar','.rar', '.gz', '.7z')):  
                Log.logger.info(["\n解压文件: ", "Unziping File: "][lan] + file) 
            
                # Zip File
                if file.endswith('.zip'): tmp = zipfile.ZipFile(file)
                # Tar File
                elif file.endswith('.tar'): tmp = tarfile.open(file)
                # RAR File
                elif file.endswith('.rar'): 
                    if RAR_Support:
                        import rarfile 
                        tmp = rarfile.RarFile(file)
                    else: Log.logger.info(["RAR支持未开启", "RAR Support is set to False"][lan])
                # GZ / 7z File
                else:   Log.logger.info(["需要手动解压", "Manual Unzip Action Required"][lan])
            
                try:  
                    tmp.extractall()
                    tmp.close()
                except: Log.logger.info(["失败", "Failed"][lan])
                else:
                    Log.logger.info(["成功", "Success"][lan])
                    try: shutil.move(file, Zip_Dir)
                    except: pass
    Log.logger.info("\n========================= " + ["完成", "Finish"][lan] + " =========================\n\n")


# 处理文件 | Process Files
def Process(lan):
    Log.logger.info("======================= " + ["开始处理", "Processing"][lan] + " =======================")
    global File_Count
    if not os.path.exists(File_Dir): os.makedirs(File_Dir)
    
    for root, dirs, files in os.walk(Working_Path):

        for file in files:
            if any(key if key in root else False for key in Ignore_dir): continue
            else: os.chdir(root)
            
            if file.endswith('.txt'):
                Log.logger.info(["\n处理文件: ", "Processing File: "][lan] + file + "\n")
                
                if file in Ignore_file: Log.logger.info(["忽略", "Ignore"][lan] + "\n")
                else:
                    File_Count += 1
                    Search(file)
                    try: shutil.move(file, File_Dir)
                    except: pass
                Log.logger.info("--------------------------------------------------")
    Log.logger.info("========================= " + ["完成", "Finish"][lan] + " =========================\n\n")


# 寻找下载链接 | Looking For Download Link        
def Search(txt_file):
    global Link_Count
    tmp = open(txt_file, "r", encoding='utf-8')
    
    for line in tmp.readlines():
        link = any(key if key in line else False for key in Keyword)
        Ignore = any(key if key in line else False for key in Ignore_content)

        if link and not Ignore:
            if '\n' in line: line = line.strip("\n")
            Link_Count += 1
            Log.logger.info(line + "\n")
            Out.writelines(line + "\n")       
    tmp.close()


# 清除空文件夹 | rm empty folders
def Rmdirs(lan):
    Log.logger.info("===================== " + ["删除空文件夹", "Deleting Empty Dirs"][lan] + " =====================")
    for item in os.listdir(Working_Path):
        tmp = Working_Path + item
        
        if os.path.isdir(tmp) and not (item in Ignore_dir):
            Rmdirs_sub(tmp, lan)
    Log.logger.info("\n========================= " + ["完成", "Finish"][lan] + " =========================\n\n")

def Rmdirs_sub(dir, lan):
    if os.listdir(dir):
        for item in os.listdir(dir):
            tmp = dir + "/" + item

            if os.path.isdir(tmp):
                Rmdirs_sub(tmp, lan)            

    try: 
        os.chdir(Working_Path)
        os.rmdir(dir)
    except:
        Log.logger.info("\n" + dir + [":\t忽略", ":\tpass"][lan])
    else:
        Log.logger.info("\n" + dir + [":\t成功", ":\tsuccess"][lan])


# 准备结束 | Prepare to end
def End(lan):
    Out.close()
    Log.logger.info("\n=========================================================")
    Log.logger.info(str(File_Count) + [" 个文件已处理，找到 ", " files processed, "][lan] + str(Link_Count) + [" 个链接", " links found"][lan])
    Log.logger.info("=========================================================\n")
    Log.logger.info(["按任意键退出并打开输出文件...", "Press Any Key To Exit And Open Output File..."][lan])
    Read()
    try: os.startfile(Working_Path + Output)
    except: Log.logger.info(["输出文件打开失败，可能原因: 修改了输出文件名称", "Output file failed to open, possible reason: Output file name has been changed"][lan])
    return 0


# 保存配置文件 | Save config file
def Save(lan):
    config = open(Path + "config.json", "w", encoding='utf-8')
    tmp = "zh_cn" if lan == 0 else "en_us"

    data =  { \
'Language' : tmp, \
'Output File' : Output, \
'Archived Folder' : Archived, \
'Archived Zip Folder' : Zip_Folder, \
'Archived File Folder' : File_Folder, \
'KeyWord' : Keyword, \
'Ignore Folder' : Ignore_dir, \
'Ignore File' : Ignore_file, \
'Ignore Content' : Ignore_content, \
'RAR Support' : RAR_Support, \
'Debug Mode' : Debug \
            }

    config.write(json.dumps(data))
    config.close()


# 读取配置文件 | Load config file
def Load(lan):
    global Output, Archived, Zip_Folder, File_Folder, Keyword, Ignore_dir, Ignore_file, Ignore_content, RAR_Support
    
    try: 
        tmp = open("config.json", "r", encoding='utf-8')
        config = json.loads(tmp.readlines()[0])
        tmp.close()

        Output = config['Output File']
        Archived = config['Archived Folder']
        Zip_Folder = config['Archived File Folder']
        File_Folder = config['Archived File Folder']
        Keyword = config['KeyWord']
        Ignore_dir = config['Ignore Folder']
        Ignore_file = config['Ignore File']
        Ignore_content = config['Ignore Content']
        RAR_Support = config['RAR Support']
    
    except: 
        Log.logger.info("\n------------------------- " +  ["失败", "Failed"][lan] + " -------------------------\n")
        Back(lan)


# 读取用户输入 | Read input from interface
def Read():
    key = input()
    if (key == "") or (key == " "): Log.logger.debug("INPUT: <Enter>") 
    else:                           Log.logger.debug("INPUT: " + key)
    return key


# <快捷键> 返回 | <shortcut> Back
def Back(lan):
    Log.logger.info(["> 按任意键来返回", "> Press Any Key To Go Back"][lan])
    key = input()
    if (key == "") or (key == " "):   Log.logger.info("INPUT: <Enter>")
    else:                           Log.logger.info("INPUT: " + key)