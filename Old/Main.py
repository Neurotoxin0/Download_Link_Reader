import os, sys, shutil, json


Path = (os.path.split(os.path.realpath(__file__))[0] + "/").replace("\\\\", "/").replace("\\", "/")
Language_Code = -1

if __name__ == "__main__":
    os.chdir(Path)
    sys.path.append('Working_Dir')
    
    try: import Read_Files
    except:
        print("\n------------------------- Read_Files Module Missing -------------------------\n")
        print(" \
===========================================================================\n \
------------------------- CRITICAL ERROR, EXIT ! -------------------------\n \
=========================================================================== \
            ")
    else:
        try:
            tmp = open(Path + "Working_Dir/config.json", "r", encoding='utf-8')
            config = json.loads(tmp.readlines()[0])
            tmp.close()
            Language_Code = 0 if config['Language'] == "zh_cn" else 1          
        except:
            while True:
                #os.chdir(Path) 
                os.system('cls')
            
                print("\
选择语言 | Select Language: \n\
    1\t中文\n\
    2\tEnglish\n\
    3\t退出 | Exit\n\
                    ")
            
                lan = input(">")

                if lan not in ["1", "2", "3", "debug"]:
                    print("\n------------------------- 无效选项 | Invalid Command -------------------------\n")
                    input("> 按任意键来返回 | Press Any Key To Go Back")
                else:
                    if lan == "1" or lan == "2":
                        Language_Code = int(lan) - 1
            
                    # ------------------------- TEST & DEBUG ONLY ------------------------
                    elif lan == "debug":
                        try:        
                            import Test
                            Test.main()
                            shutil.rmtree("__pycache__")
                        except:     print("\n------------------------- Debug Module Missing / Broken -------------------------\n")
                        else:       print("\n------------------------- Success -------------------------\n")
                        finally:    input("> 按任意键来返回 | Press Any Key To Go Back"); continue
                    # ------------------------- END -------------------------      
                    break   
        
        if Language_Code == 0 or Language_Code == 1:
            Read_Files.CLI(Language_Code)
        
        os.chdir(Path + "Working_Dir")
        shutil.rmtree("__pycache__")
        