import json, os
import Process
from Common import Path, Log, Read_Config, Read, Message, Exit


Config, Language = None, None
# ========================= 默认配置 | Default Config =========================
Output = "output.txt"                                   # 输出文件名称 | Output File's Name
Archived = "Archived"                                   # 归档文件夹名称 | Archive Folder Name
Zip_Folder = "Zip_Files"                                # 处理过的压缩文件存放的文件夹名称 | Folder Name For Processed Zips
File_Folder = "Processed_Files"                         # 处理过的文件存放的文件夹名称 | Folder Name For Processed Files
Raw_Folder = "Unprocessed_Files"                        # 未处理过的文件存放的文件夹名称 | Folder Name For Unprocessed Files
Keyword = ["ed2k://", "magnet:"]                        # 下载链接关键字 | keyword for download link
Pattern = {}                                            # 下载链接特征  | pattern for download link
Ignore_dir = [Archived, "Log"]                          # 忽略的文件夹 | ignore certain dirs
Ignore_file = [Output, "config.json"]                   # 忽略的文件 | ignore txt files with certain names
Ignore_content = []                                     # 忽略的内容 | ignore certain contents
# ============================================================================


def Main():
    global  Config, Language, Output, Archived, Zip_Folder, File_Folder, Raw_Folder, \
            Keyword, Pattern, Ignore_dir, Ignore_file, Ignore_content
    
    # Load cfg
    Config = Read_Config()
    if Config: 
        try:
            Language = 0 if Config['Language'] == "zh_cn" else 1
            Output = Config['Output File']
            Archived = Config['Archived Folder']
            Zip_Folder = Config['Archived Zip Folder']
            File_Folder = Config['Archived File Folder']
            Raw_Folder = Config['Archived Raw Folder']
            Keyword = Config['KeyWord']
            Pattern = Config['Pattern']
            Ignore_dir = Config['Ignore Folder']
            Ignore_file = Config['Ignore File']
            Ignore_content = Config['Ignore Content']
        except: Bad_Config()    # Bad Config, Deletion
    else: Choose_Language()

    # Main Config
    Main_Menu()



def Choose_Language():
    global Language
    while True:
        os.system('cls')
        Log.logger.info(\
"选择语言 | Select Language: \n\
    1 中文\n\
    2 English\n\
    3 退出 | Exit")

        option = Read()
        if option not in ["1", "2", "3"]: Message(1, True)
        elif option == "1" or option == "2": Language = int(option) - 1; return 
        else: os._exit(0) 



def Main_Menu():
    while True:
        os.system('cls')
        Log.logger.info(\
["当前下载链接关键字: ", "Current Keywords For Download Link: "][Language] + str(Keyword) + "\n" + \
["当前下载链接特征: ", "Current Patterns For Download Link: "][Language] + str(Pattern) + "\n" + \
["当前忽略的文件夹: ", "Current Ignored Dirs: "][Language] + str(Ignore_dir) + "\n" + \
["当前忽略的文件: ", "Current Ignored Files: "][Language] + str(Ignore_file) + "\n" + \
["当前忽略的内容: ", "Current Ignored Contents: "][Language] + str(Ignore_content) + "\n\n" + \

["命令选项: ", "Command Options: "][Language] + "\n" + \
    "<Enter>\t" + ["保存并开始执行", "Save And Execute"][Language] + "\n" + \
    "1\t" + ["修改下载链接关键字", "Edit Keywords For Download Link"][Language] + "\n" + \
    "2\t" + ["修改下载链接特征", "Edit Patterns For Download Link"][Language] + "\n" + \
    "3\t" + ["修改当前忽略的文件夹", "Edit Dirs To Be Ignored"][Language] + "\n" + \
    "4\t" + ["修改当前忽略的文件", "Edit Files  To Be Ignored"][Language] + "\n" + \
    "5\t" + ["修改当前忽略的内容", "Edit Contents To Be Ignored"][Language] + "\n" + \
    "6\t" + ["储存&目录设置", "Archive & Dir Setting"][Language] + "\n" + \
    "7\t" + ["清除本地配置文件", "Remove Config File"][Language] + "\n" + \
    "0\t" + ["保存并退出", "Save And Exit"][Language])
        
        options = [str(i) for i in range(8)]; options += [""]   # Valid options
        option = Read()
        if option not in options: Message(1, True, Language); continue
        elif option == "": Save(); Choose_Mode()
        elif option == "1": Alter_Keywords()
        elif option == "2": Alter_Pattern()
        elif option == "3": Alter_Ignored_Folder()
        elif option == "4": Alter_Ignored_File()
        elif option == "5": Alter_Ignored_Content()
        elif option == "6": Alter_Utility()
        elif option == "7": 
            if Del_Config(): Exit()
        elif option == "0": Save(); Exit() 
        


def Choose_Mode():
    while True:
        os.system('cls')
        Log.logger.info(\
"\n------------------------- " + ["选择运行模式", "Select Process Mode"][Language] + " -------------------------\n\n" + \
    "1\t" + ["仅使用关键字", "Use Keywords Only"][Language] + "\n" + \
    "2\t" + ["仅使用特征", "Use Patterns Only"][Language] + "\n" + \
    "3\t" + ["使用关键字和特征", "Use Keywords And Patterns"][Language] + "\n" + \
    "4\t" + ["返回主菜单", "Back To Main Menu"][Language] + "\n\n")

        option = Read()
        if option == "4": return 
        else:
            if option not in ["1", "2", "3"]: Message(1, True, Language); continue
        
        code = None
        if option == "1": code = Process.Main(0)
        elif option == "2": code =  Process.Main(1)
        else: code =  Process.Main(-1)
        if not code: Bad_Config()
        else: 
            Log.logger.info(["按任意键退出并打开输出文件...", "Press Any Key To Exit And Open Output File..."][Language])
            Read()
            os.startfile(Path + Output)
            Exit()
    


def Alter_Content(array):
    option = Read()
    if option == "3":  Save(); return 1
    else:
        if option not in ["1", "2"]: Message(1, True, Language); return 0
        
        while True:
            Message(3, False, Language)
            
            key = Read()
            if key == "": return 1;
            
            if option == "1": 
                if not key in array: array.append(key)
                else: Message(4, True, Language)
            else:   # option == "2"
                try:    array.remove(key)
                except: Message(5, True, Language)

def Alter_Keywords():
    while True:
        os.system('cls')
        Log.logger.info(\
"\n------------------------- " + ["修改下载链接关键字", "Edit Keywords For Download Link"][Language] + " -------------------------\n\n" + \
["当前下载链接关键字: ", "Current Keywords For Download Link: "][Language] + str(Keyword) + "\n\n" + \
    "1\t" + ["添加下载链接关键字", "Add Keyword For Download Link"][Language] + "\n" + \
    "2\t" + ["移除下载链接关键字", "Remove Keyword For Download Link"][Language] + "\n" + \
    "3\t" + ["返回主菜单", "Back To Main Menu"][Language] + "\n")
        if Alter_Content(Keyword): return 
    
def Alter_Ignored_Folder():
    while True:
        os.system('cls')
        Log.logger.info(\
"\n------------------------- " + ["修改忽略的文件夹", "Edit Dirs To Be Ignored"][Language] + " -------------------------\n\n" + \
["当前忽略的文件: ", "Current Ignored Dirs: "][Language] + str(Ignore_file) + "\n\n" + \
    "1\t" + ["添加忽略的文件", "Add File Into Ignore List"][Language] + "\n" + \
    "2\t" + ["移除忽略的文件", "Remove File From Ignore List"][Language] + "\n" + \
    "3\t" + ["返回主界菜单", "Back To Main Menu"][Language] + "\n")
                
        if Alter_Content(Ignore_dir): return 
        
def Alter_Ignored_File():
    while True:
        os.system('cls')
        Log.logger.info(\
"\n------------------------- " + ["修改忽略的文件", "Edit Files To Be Ignored"][Language] + " -------------------------\n\n" + \
["当前忽略的文件: ", "Current Ignored Files: "][Language] + str(Ignore_file) + "\n\n" + \
    "1\t" + ["添加忽略的文件", "Add File Into Ignore List"][Language] + "\n" + \
    "2\t" + ["移除忽略的文件", "Remove File From Ignore List"][Language] + "\n" + \
    "3\t" + ["返回主界菜单", "Back To Main Menu"][Language] + "\n")

        if Alter_Content(Ignore_file): return 

def Alter_Ignored_Content():
    while True:
        os.system('cls')
        Log.logger.info(\
"\n------------------------- " + ["修改忽略的内容", "Edit Contents To Be Ignored"][Language] + " -------------------------\n\n" + \
["当前忽略的内容: ", "Current Ignored Contents: "][Language] + str(Ignore_content) + "\n\n" + \
    "1\t" + ["添加忽略的内容", "Add Content Into Ignore List"][Language] + "\n" + \
    "2\t" + ["移除忽略的内容", "Remove Content From Ignore List"][Language] + "\n" + \
    "3\t" + ["回到主菜单", "Back to Main Menu"][Language] + "\n")

        if Alter_Content(Ignore_content): return 



def Alter_Pattern():
    while True:
        os.system('cls')
        Log.logger.info(\
"\n------------------------- " + ["修改下载链接特征", "Edit Patterns For Download Link"][Language] + " -------------------------\n\n" + \
["程序在匹配到下载特征后会后面的所有 行 记录为链接, 直到遇到一行空行: ", "The program will record every line after a pattern was matched, until an empty line was encoutered"][Language] + "\n\n" + \
["当前下载链接特征: ", "Current Patterns For Download Link: "][Language] + str(Pattern) + "\n\n" + \
    "1\t" + ["添加/修改下载链接特征", "Add/Alter Pattern For Download Link"][Language] + "\n" + \
    "2\t" + ["移除下载链接特征", "Remove Pattern For Download Link"][Language] + "\n" + \
    "3\t" + ["返回主菜单", "Back To Main Menu"][Language] + "\n")

        option = Read()
        if option == "3":  Save(); return 
        else:
            if option not in ["1", "2"]: Message(1, True, Language); continue
        
        while True:
            if option == "1": 
                Message(3, False, Language)
                key = Read()
                if key == "":  return 
                if Pattern.get(key): Message(12, False, Language)

                Message(13, False, Language)
                line = Read()
                if line == "": Message(1, True, Language)
                else:
                    try: line = int(line)
                    except: Message(1, True, Language); continue
                    Pattern[key] = line
            
            else:   # option == "2"
                Message(3, False, Language)
                key = Read()
                if key == "":  return 
                try: Pattern.pop(key)
                except: Message(5, True, Language)

   

def Change_Value():
    Message(6, False, Language)
    key = Read()
    if key != "":  Message(2, True, Language); return key
    else: Message(7, True, Language)

def Alter_Utility(): 
    global Output, Archived, Zip_Folder, File_Folder, Raw_Folder

    while True:
        os.system('cls')
        Log.logger.info(\
"\n------------------------- " + ["储存&目录设置", "Archive & Dir Setting"][Language] + " -------------------------\n\n" + \
["当前输出文件名称: ", "Current Name For Output File: "][Language] + Output + "\n" + \
["当前归档文件夹名称: ", "Current Name For Archive Folder: "][Language] + Archived + "\n" + \
["处理过的压缩文件存放的文件夹名称: ", "Folder Name For Processed Zips: "][Language] + Zip_Folder + "\n" + \
["处理过的文件存放的文件夹名称: ", "Folder Name For Processed Files: "][Language] + File_Folder + "\n\n" + \

["命令选项: ", "Command Options: "][Language] + "\n" + \
    "1\t" + ["修改输出文件名称", "Edit Output File Name"][Language] + "\n" + \
    "2\t" + ["修改归档文件夹名称", "Edit Archive Folder Name"][Language] + "\n" + \
    "3\t" + ["处理压缩文件存档文件夹名称", "Edit Processed Zips' Folder Name"][Language] + "\n" + \
    "4\t" + ["处理文件存档文件夹名", "Edit Processed Files' Folder Name"][Language] + "\n" + \
    "5\t" + ["未处理文件存档文件夹名", "Edit Unprocessed Files' Folder Name"][Language] + "\n" + \
    "6\t" + ["返回菜单", "Back To Menu"][Language] \
                                )
        option = Read()
        if option == "6":  Save(); return 
        else:
            if option not in ["1", "2", "3", "4", "5"]: 
                Message(1, True, Language); continue
            
            if option == "1":   Output      = Change_Value()
            elif option == "2": Archived    = Change_Value()
            elif option == "3": Zip_Folder  = Change_Value()
            elif option == "4": File_Folder = Change_Value()
            elif option == "5": Raw_Folder = Change_Value()



def Save():
    config = open(Path + "config.json", "w", encoding='utf-8')
    Language_Code = "zh_cn" if Language == 0 else "en_us"

    data = {'Language' : Language_Code,
            'Output File' : Output,
            'Archived Folder' : Archived,
            'Archived Zip Folder' : Zip_Folder,
            'Archived File Folder' : File_Folder,
            'Archived Raw Folder' : Raw_Folder,
            'KeyWord' : Keyword,
            'Pattern' : Pattern,
            'Ignore Folder' : Ignore_dir,
            'Ignore File' : Ignore_file,
            'Ignore Content' : Ignore_content
            }

    config.write(json.dumps(data)); config.close()
    


def Bad_Config():
    Message(11, False, Language)
    if Del_Config(confirmed=True): Message(9, True, Language); Exit()

def Del_Config(confirmed = False):
    if not confirmed:
        Message(8, False, Language)
        confirm = Read()
        if confirm == "y": return Del_Config_Action()
        else: Message(10, True, Language); return 0
    
    else: return Del_Config_Action()
        
def Del_Config_Action():
    try: 
        os.remove(Path + "config.json")
        Message(9, True, Language)
        return 1
    except: 
        Log.logger.info("Exception On Deleting Config File!")
        return 0



if __name__ == "__main__":
    Main()
