import os, shutil
import Keyword, Pattern
from Common import Path, Log, Time, Read_Config


Language, Output, Archived, Zip_Folder, File_Folder, Raw_Folder, Ignore_dir, Ignore_file, Ignore_content = None, None, None, None, None, None, None, None, None
Archived_Dir, Zip_Folder, Processed_File_Folder, Unprocessed_File_Folder, File_Count, Link_Count, Links = None, None, None, None, 0, [0,0], [[], {}]


def Main(mode):
    global  Language, Output, Archived, Zip_Folder, File_Folder, Raw_Folder, Ignore_dir, Ignore_file, \
            Ignore_content, Archived_Dir, Zip_Folder, Processed_File_Folder, Unprocessed_File_Folder

    # Load cfg
    Config = Read_Config()
    try:
        Language = 0 if Config['Language'] == "zh_cn" else 1
        Output = open(Path + Config['Output File'], "a", encoding = 'utf-8')  
        Archived = Config['Archived Folder']
        Zip_Folder = Config['Archived Zip Folder']
        File_Folder = Config['Archived File Folder']
        Raw_Folder = Config['Archived Raw Folder']
        Ignore_dir = Config['Ignore Folder']
        Ignore_file = Config['Ignore File']
        Ignore_content = Config['Ignore Content']
    except: input("Process rreturn 0"); return 0    # Bad Config
        

    # Set Path
    Archived_Dir = Path + Archived + "/"
    Zip_Folder = Archived_Dir + Zip_Folder + "/"
    Processed_File_Folder = Archived_Dir + File_Folder + "/"
    Unprocessed_File_Folder = Archived_Dir + Raw_Folder + "/"
    # Add time stamp to output.txt
    Output.writelines("################################################## ")
    Output.writelines(Time)
    Output.writelines(" ##################################################\n")
    
    if not Process(mode): return 0
    else: return 1



def Process(mode):
    Log.logger.info("======================= " + ["开始处理", "Processing"][Language] + " =======================")
    global File_Count, Link_Count, Links
    
    # Process File
    for root, dirs, files in os.walk(Path):
        for file in files:
            if not(file.endswith('.txt')) or (file in Ignore_file) or ( any(key if key in root else False for key in Ignore_dir) ): continue
            else: 
                Log.logger.info(["\n处理文件: ", "\nProcessing File: "][Language] + file + "\n")
                filepath = root + "/" + file
                File_Count += 1

                links, count = None, None
                if mode == 0:   # Keyword
                    links, count = Keyword.Main(filepath)
                    if not count == -1:
                        Links[0] += links
                        Link_Count[0] += count
                    else: return 0
                
                elif mode == 1: # Pattern
                    if not count == -1:
                        links, count = Pattern.Main(filepath)
                        Merge_Dic(Links[1], links)
                        Link_Count[1] += count
                    else: return 0
                
                elif mode == -1: # Keywork + Pattern
                    links, count = Keyword.Main(filepath)
                    if not count == -1:
                        Links[0] += links
                        Link_Count[0] += count
                    else: return 0

                    if not count == -1:
                        links, count = Pattern.Main(filepath)
                        Merge_Dic(Links[1], links)
                        Link_Count[1] += count
                    else: return 0

                # move processed file
                if not os.path.exists(Processed_File_Folder): os.makedirs(Processed_File_Folder)
                try: shutil.move(filepath, Processed_File_Folder)
                except: shutil.move(filepath, Processed_File_Folder + file + "~1")
                Log.logger.info("--------------------------------------------------")
        

    # Move dirs
    if not os.path.exists(Archived_Dir): os.makedirs(Archived_Dir)
    for root, dirs, files in os.walk(Path):
        for dir in dirs:
            move = True
            for ignore in Ignore_dir:
                if ignore in dir: move = False

            if move:
                try: shutil.move(root + dir, Unprocessed_File_Folder)
                except: shutil.move(root + dir, Unprocessed_File_Folder + dir +"~1")
                
        break   # only iter the root dir

    Log.logger.info("========================= " + ["完成", "Finish"][Language] + " =========================\n")  
    Write()
    return 1

def Merge_Dic(Main_Dic, Dic1):
    for key in Dic1:
        if not Main_Dic.get(key): Main_Dic[key] = Dic1[key]
        else: 
            tmp = Main_Dic[key] + Dic1[key]
            Main_Dic[key] = tmp



def Write():
    Write_Line("\n===== Keyword =====\n")
    for link in Links[0]: Write_Line(link + "\n")
    Write_Line("\nTotal Links Found Using Keyword: " + str(Link_Count[0]))
    Write_Line("\n====================\n")
    
    Write_Line("\n===== Pattern =====\n")
    for pattern in Links[1]: 
        Write_Line(pattern + "\n")
        links = Links[1][pattern]
        for link in links: Write_Line(link + "\n")
        Write_Line("\n")
    Write_Line("\nTotal Links Found Using Pattern: " + str(Link_Count[1]))
    Write_Line("\n====================\n")

    Write_Line("\nTotal Files Processed: " + str(File_Count) + "; Total Links Found: " + str(Link_Count[0] + Link_Count[1]))
    Write_Line("\n====================\n")
    Output.close()

def Write_Line(string):
    Log.logger.info(string)
    Output.writelines(string)
